import clsx from "clsx";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { ReactNode } from "react";

interface LinkCardProps {
  href: string;
  eyebrow?: string;
  title: string;
  description?: string;
  meta?: string;
  status?: "ready" | "draft" | "blocked" | "pending";
}

const statusStyle: Record<NonNullable<LinkCardProps["status"]>, string> = {
  ready: "bg-status-success/15 text-status-success ring-1 ring-inset ring-status-success/25",
  draft: "bg-status-info/15 text-status-info ring-1 ring-inset ring-status-info/25",
  blocked:
    "bg-status-danger/15 text-status-danger ring-1 ring-inset ring-status-danger/25",
  pending: "bg-ink-faint/30 text-ink-secondary ring-1 ring-inset ring-ink-faint/40",
};

export function LinkCard({
  href,
  eyebrow,
  title,
  description,
  meta,
  status,
}: LinkCardProps) {
  return (
    <Link
      href={href}
      className="group relative block rounded-xl bg-surface-elevated p-6 shadow-card transition-all duration-200 hover:-translate-y-[2px] hover:shadow-card-hover"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          {eyebrow && (
            <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
              {eyebrow}
            </div>
          )}
          <h3 className="font-display text-[19px] font-semibold leading-snug tracking-tight text-ink">
            {title}
          </h3>
          {description && (
            <p className="mt-2 text-[14px] leading-relaxed text-ink-secondary">
              {description}
            </p>
          )}
        </div>
        <ArrowUpRight
          className="h-5 w-5 shrink-0 text-ink-muted transition-all group-hover:text-accent group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
          strokeWidth={2}
        />
      </div>
      {(meta || status) && (
        <div className="mt-5 flex items-center justify-between gap-3 text-[12.5px]">
          <span className="text-ink-muted">{meta}</span>
          {status && (
            <span
              className={clsx(
                "rounded-full px-2 py-0.5 text-[11px] font-medium capitalize",
                statusStyle[status],
              )}
            >
              {status}
            </span>
          )}
        </div>
      )}
    </Link>
  );
}

export function Stat({
  label,
  value,
  hint,
}: {
  label: string;
  value: string | number;
  hint?: string;
}) {
  return (
    <div className="rounded-xl bg-surface-elevated p-6 shadow-card">
      <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
        {label}
      </div>
      <div className="mt-2 font-display text-[34px] font-semibold leading-none tracking-tightest text-ink">
        {value}
      </div>
      {hint && (
        <div className="mt-2 text-[13px] leading-snug text-ink-secondary">
          {hint}
        </div>
      )}
    </div>
  );
}

export function SoftCard({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      className={clsx(
        "rounded-xl bg-surface-elevated p-7 shadow-card",
        className,
      )}
    >
      {children}
    </div>
  );
}
