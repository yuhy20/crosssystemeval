# CrossSystemEval — UI

Apple-inspired research dashboard for navigating CrossSystemEval findings. Next.js 14 (App Router) + Tailwind + react-markdown.

## Setup

```bash
cd ui
npm install
npm run dev
```

Then open http://localhost:3000.

## Navigation

- `/` — Overview (stats + deep links to every artifact)
- `/agenda` — Research agenda (rendered from `../research_agenda.md`)
- `/literature` — Four annotated bibliographies (rendered from `../lit_review/*.md`)
- `/worklog` — Weekly worklog entries (rendered from `../worklog/*.md`)
- `/trident` — TRIDENT replication harness status

## How content is loaded

Content lives in `../*/*.md` (project root, not under `/ui`). `lib/content.ts` reads markdown via `gray-matter`, exposes typed helpers. No database, no CMS — update the markdown, refresh the page.

## Design system

- **Typography**: SF Pro stack (system-ui fallback). Display weight for headings with tight letter-spacing; Text weight for body.
- **Color**: `#fbfbfd` surface, `#1d1d1f` ink, `#0071e3` accent. Status colors match Apple's semantic palette (success/warning/danger/info).
- **Motion**: Fade-up entrance animations with 50ms stagger; 200ms hover lift on cards.
- **Radius**: 0.625–1.125rem, with 10mm of whitespace gutter everywhere.

## Extending

Add a new page: create `app/<route>/page.tsx` and include it in `components/Sidebar.tsx`'s `nav` array. Add a new lit review: drop a `.md` file in `../lit_review/` with frontmatter `slug`, `title`, `subtitle`, `papers`, `date`.
