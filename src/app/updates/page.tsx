import type { Metadata } from "next";
import { updates } from "@/lib/updates";
import { UpdatesFeed } from "./UpdatesFeed";
import { PageShell } from "@/components/PageShell";

export const metadata: Metadata = {
  title: "Updates — Checklist2",
  description: "A changelog of every checklist, box config, odds update, and feature launch on Checklist2.",
};

export default function UpdatesPage() {
  return (
    <PageShell
      breadcrumb={{ label: "Home", href: "/checklists" }}
      title="Updates"
      description="The latest additions and improvements to Checklist\u00B2"
    >
        <UpdatesFeed updates={updates} />
    </PageShell>
  );
}
