import Link from "next/link";
import { Footer } from "./Footer";

interface PageShellProps {
  breadcrumb: { label: string; href: string };
  title: string;
  description?: string;
  children: React.ReactNode;
}

export function PageShell({ breadcrumb, title, description, children }: PageShellProps) {
  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-[1000px] mx-auto px-6 py-10 space-y-8">
        <div>
          <Link
            href={breadcrumb.href}
            className="inline-flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors mb-4"
          >
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            {breadcrumb.label}
          </Link>
          <h1 className="text-2xl font-bold text-white tracking-tight">{title}</h1>
          {description && <p className="text-sm text-zinc-500 mt-1">{description}</p>}
        </div>
        {children}
      </div>
      <Footer />
    </div>
  );
}
