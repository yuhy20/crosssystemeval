"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import {
  BookOpen,
  ClipboardList,
  FileText,
  FlaskConical,
  Home,
  ListChecks,
  Network,
} from "lucide-react";

const nav = [
  { href: "/", label: "Overview", icon: Home },
  { href: "/agenda", label: "Research Agenda", icon: FileText },
  { href: "/literature", label: "Literature", icon: BookOpen },
  { href: "/worklog", label: "Worklog", icon: ListChecks },
  { href: "/trident", label: "TRIDENT Calibration", icon: FlaskConical },
  { href: "/pilot", label: "Rubric Pilot", icon: ClipboardList },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sticky top-0 flex h-screen w-64 shrink-0 flex-col border-r border-ink-hairline/70 bg-surface/60 backdrop-blur-xl">
      <div className="flex h-16 items-center gap-2.5 px-6">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent text-white shadow-[0_0_0_1px_rgba(255,255,255,0.08)]">
          <Network className="h-4 w-4" strokeWidth={2.25} />
        </div>
        <div className="leading-tight">
          <div className="font-display text-[15px] font-semibold tracking-tight text-ink">
            CrossSystemEval
          </div>
          <div className="text-[11px] text-ink-muted">Phase 1 Sprint</div>
        </div>
      </div>

      <nav className="mt-2 flex-1 px-3">
        <ul className="space-y-0.5">
          {nav.map((item) => {
            const active =
              item.href === "/"
                ? pathname === "/"
                : pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={clsx(
                    "group flex items-center gap-3 rounded-lg px-3 py-2 text-[13.5px] font-medium transition-all duration-150",
                    active
                      ? "bg-surface-muted text-ink shadow-subtle"
                      : "text-ink-secondary hover:bg-surface-elevated hover:text-ink",
                  )}
                >
                  <Icon
                    className={clsx(
                      "h-4 w-4 transition-colors",
                      active
                        ? "text-accent"
                        : "text-ink-muted group-hover:text-ink-secondary",
                    )}
                    strokeWidth={2}
                  />
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="border-t border-ink-hairline/70 p-5 text-[11px] leading-relaxed text-ink-muted">
        <div className="font-medium text-ink-secondary">BlueDot TAIS Sprint</div>
        <div className="mt-0.5">2026-04-20 → 2026-05-18</div>
      </div>
    </aside>
  );
}
