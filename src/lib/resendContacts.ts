import { Resend } from "resend";

/**
 * Newsletter contact upsert against the GLOBAL Resend contacts API (not the
 * deprecated audience-scoped endpoint). A new contact is created with its
 * signup attribution (signup_source / signup_set), added to the newsletter
 * segment (RESEND_AUDIENCE_ID), and opted into the Weekly Newsletter topic
 * (RESEND_TOPIC_NEWSLETTER).
 *
 * Resend's global contacts.create is an UPSERT — for an existing contact it
 * succeeds and OVERWRITES properties rather than erroring. So we GET first:
 * create only when the contact is new; for an existing contact we reconcile —
 * add to the segment and opt into the topic (both idempotent), and set the
 * signup_source / signup_set properties ONLY when the contact has no value for
 * them yet, so a later footer signup can't erase an earlier odds-alert + set
 * attribution. (A create that still races into a duplicate also reconciles.)
 *
 * Env: RESEND_NEWSLETTER_API_KEY, RESEND_AUDIENCE_ID, RESEND_TOPIC_NEWSLETTER.
 */

type UpsertResult = { status: "ok" | "missing_config" | "error"; error?: unknown };

const DUP_RE = /already|exists|duplicate/i;

function isDuplicateError(error: unknown): boolean {
  const msg = String((error as { message?: string })?.message ?? "").toLowerCase();
  const code = (error as { statusCode?: number })?.statusCode;
  return code === 409 || DUP_RE.test(msg);
}

// A property is "already set" only when present with a non-empty value.
function hasValue(prop: { value?: unknown } | undefined): boolean {
  if (!prop) return false;
  const v = prop.value;
  return v !== undefined && v !== null && String(v).trim() !== "";
}

export async function upsertNewsletterContact(opts: {
  email: string;
  source: string; // signup_source
  set?: string | null; // signup_set — omit for non-set signups (footer/updates)
}): Promise<UpsertResult> {
  const apiKey = process.env.RESEND_NEWSLETTER_API_KEY;
  const audienceId = process.env.RESEND_AUDIENCE_ID; // newsletter segment id
  const topicId = process.env.RESEND_TOPIC_NEWSLETTER;
  if (!apiKey || !audienceId || !topicId) {
    console.error(
      "[newsletter] missing env:",
      !apiKey ? "RESEND_NEWSLETTER_API_KEY" : "",
      !audienceId ? "RESEND_AUDIENCE_ID" : "",
      !topicId ? "RESEND_TOPIC_NEWSLETTER" : ""
    );
    return { status: "missing_config" };
  }

  const resend = new Resend(apiKey);
  const desired: Record<string, string> = { signup_source: opts.source };
  if (opts.set) desired.signup_set = opts.set;

  // GET first — create() upserts and would clobber existing properties.
  let existingProps: Record<string, { value?: unknown } | undefined> | null = null;
  try {
    const { data, error } = await resend.contacts.get({ email: opts.email });
    if (!error && data?.id) {
      existingProps = (data.properties ?? {}) as Record<string, { value?: unknown } | undefined>;
    }
  } catch (e) {
    // Get threw (e.g. network/not-found surfaced as throw) → fall through to create.
    console.error("[newsletter] get threw (will attempt create):", e);
  }

  // Existing contact → reconcile without clobbering prior attribution.
  if (existingProps) {
    await reconcileExisting(resend, opts.email, audienceId, topicId, desired, existingProps);
    return { status: "ok" };
  }

  // New contact → create with full attribution, segment, and topic opt-in.
  try {
    const { error } = await resend.contacts.create({
      email: opts.email,
      unsubscribed: false,
      properties: desired,
      segments: [{ id: audienceId }],
      topics: [{ id: topicId, subscription: "opt_in" }],
    });
    if (!error) return { status: "ok" };
    // Raced with a concurrent create → reconcile (re-reads current state).
    if (isDuplicateError(error)) {
      await reconcileExisting(resend, opts.email, audienceId, topicId, desired);
      return { status: "ok" };
    }
    console.error("[newsletter] create error:", error);
    return { status: "error", error };
  } catch (err) {
    console.error("[newsletter] create threw:", err);
    return { status: "error", error: err };
  }
}

async function reconcileExisting(
  resend: Resend,
  email: string,
  segmentId: string,
  topicId: string,
  desired: Record<string, string>,
  knownProps?: Record<string, { value?: unknown } | undefined>
): Promise<void> {
  // 1) Fill signup_source / signup_set only where the contact has no value yet.
  const toSet: Record<string, string> = {};
  let existing = knownProps ?? null;
  if (!existing) {
    try {
      const { data, error } = await resend.contacts.get({ email });
      if (error) {
        console.error("[newsletter] get for reconcile failed (skipping props):", error);
      } else {
        existing = (data?.properties ?? {}) as Record<string, { value?: unknown } | undefined>;
      }
    } catch (e) {
      console.error("[newsletter] get for reconcile threw (skipping props):", e);
    }
  }
  if (existing) {
    for (const key of Object.keys(desired)) {
      if (!hasValue(existing[key])) toSet[key] = desired[key];
    }
  }
  if (Object.keys(toSet).length > 0) {
    try {
      const { error } = await resend.contacts.update({ email, properties: toSet });
      if (error) console.error("[newsletter] property update error (non-fatal):", error);
    } catch (e) {
      console.error("[newsletter] property update threw (non-fatal):", e);
    }
  }

  // 2) Ensure segment membership (idempotent; already-a-member is fine).
  try {
    const { error } = await resend.contacts.segments.add({ email, segmentId });
    if (error && !isDuplicateError(error)) console.error("[newsletter] segment add error (non-fatal):", error);
  } catch (e) {
    console.error("[newsletter] segment add threw (non-fatal):", e);
  }

  // 3) Opt into the newsletter topic.
  try {
    const { error } = await resend.contacts.topics.update({ email, topics: [{ id: topicId, subscription: "opt_in" }] });
    if (error) console.error("[newsletter] topic opt-in error (non-fatal):", error);
  } catch (e) {
    console.error("[newsletter] topic opt-in threw (non-fatal):", e);
  }
}
