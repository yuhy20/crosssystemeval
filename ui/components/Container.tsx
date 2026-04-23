import clsx from "clsx";
import { ReactNode } from "react";

export function Page({ children }: { children: ReactNode }) {
  return (
    <main className="min-h-screen flex-1 bg-surface">
      <div className="mx-auto w-full max-w-page px-10 py-14">{children}</div>
    </main>
  );
}

export function PageHeader({
  eyebrow,
  title,
  description,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
}) {
  return (
    <header className="mb-12 animate-fade-up">
      {eyebrow && (
        <div className="mb-3 text-[12px] font-semibold uppercase tracking-[0.08em] text-accent">
          {eyebrow}
        </div>
      )}
      <h1 className="font-display text-[44px] font-semibold leading-[1.08] tracking-tightest text-ink">
        {title}
      </h1>
      {description && (
        <p className="mt-4 max-w-prose text-[17px] leading-relaxed text-ink-secondary">
          {description}
        </p>
      )}
    </header>
  );
}

export function Section({
  title,
  children,
  className,
}: {
  title?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={clsx("mb-12", className)}>
      {title && (
        <h2 className="mb-5 font-display text-[22px] font-semibold tracking-tighter text-ink">
          {title}
        </h2>
      )}
      {children}
    </section>
  );
}
