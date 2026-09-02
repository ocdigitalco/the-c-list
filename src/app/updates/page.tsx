import type { Metadata } from "next";
import { updates } from "@/lib/updates";
import { UpdatesFeed } from "./UpdatesFeed";
import { PageShell } from "@/components/PageShell";
import { NewsletterSignup } from "@/components/NewsletterSignup";

export const metadata: Metadata = {
  title: "Updates — Checklist2",
  description: "A changelog of every checklist, box config, odds update, and feature launch on Checklist2.",
};

export default function UpdatesPage() {
  return (
    <PageShell
      wide
      breadcrumb={{ label: "Home", href: "/checklists" }}
      title="Updates"
      description="The latest additions and improvements to Checklist²"
    >
        {/* Newsletter signup card — above the filter pills */}
        <div className="mb-8 rounded-xl border border-[var(--brand-line)] bg-[var(--brand-card)] px-6 py-5">
          <p className="text-sm text-[var(--brand-ink-soft)] mb-3">
            New sets, odds, and features — occasionally, no spam.
          </p>
          <NewsletterSignup />
        </div>

        <UpdatesFeed updates={updates} />
    </PageShell>
  );
}
