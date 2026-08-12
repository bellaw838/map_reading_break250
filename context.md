# context.md — Break 250 Reading Lab

> Quick-load context for any AI assistant resuming work. Read this before touching code.

## What this project is

**Break 250 Reading Lab** — a focused close-reading concept trainer for advanced middle-school readers (Grade 5–8, MAP Reading ~230–249) trying to break into 250+. It is **not** a generic reading app. The product thesis is "turn ELA terms (tone, evidence, inference, structure, purpose, etc.) into usable reading tools."

Core loop: **concept → micro-example → short text → first read → second read → MAP-style questions → prove with exact text → wrong-answer diagnosis → targeted next practice.**

The single most important product feature is NOT a large passage library — it is the **wrong-answer diagnosis** layer that explains why a tempting wrong answer is wrong.

Full product spec: `design1.md`.

## Status (2026-05-29)

- **Stage:** MVP built and browser-verified on Stack v0. Three learning surfaces live: Lessons+Quizzes, Reading Lab, Reading Library.
- **Content:** 24 lessons (22 graded sub-concepts + 2 orientation) + 240 quizzes · 15 Reading Lab texts (127 annotations) · 3 Reading Library works (Macbeth, Sherlock, Moonstone; 252 annotations). Validator green: `24 lesson · 24 quiz · 15 lab · 3 library`.
- **Verified 2026-05-29:** every page rendered and screenshotted headless — no broken pages, no console errors. See `docs/Diary.md`.
- **Architecture detail:** see `docs/STRUCTURE.md` (routes, module-by-module reference, execution flows).
- **Known gaps:** quiz page lacks visual parity with the redesigned lesson page; Moonstone annotations still sparse (~1/section); mobile/a11y/Lighthouse audits partial.
- **Note:** the Next.js/Supabase plan below is the *original* proposal, superseded by the Stack v0 lock. It remains only as the candidate target for a future v1 rewrite.

## Stack — LOCKED v0 (2026-05-27)

**Stack v0 (current): Pure static.**
- HTML + vanilla JS (ES modules) + Tailwind CSS via CDN
- Content as CSV files in `content/`, fetched at runtime
- Progress in `localStorage`; no backend
- Any static HTTP server (Python's `http.server`, GitHub Pages, Netlify)

Rationale: smallest possible surface to validate the content schema and UX end-to-end without a build pipeline. Once validated, **stack v1 will rewrite against mywordbank.net's stack** (TBD when known).

## Original proposal (now superseded by v0 lock)

Per design §20, and confirmed by architect review:

- **Frontend:** Next.js (App Router) + TypeScript + Tailwind CSS
- **Backend:** Next.js API routes (single deployable) — FastAPI only if/when scoring becomes ML-heavy
- **Database:** PostgreSQL via Supabase (also handles auth)
- **Auth:** Supabase Auth (email + magic link; parent-linked student accounts later)
- **Hosting:** Vercel (web) + Supabase (DB/auth/storage)
- **Content authoring:** seed via JSON files in repo (`/content/`) before building admin UI; admin UI is Phase 5

Rationale: single-language stack (TypeScript end-to-end) reduces context cost for AI-assisted development, matches design recommendation, and Supabase removes auth + DB boilerplate. FastAPI is deferred until a real ML need appears (e.g. AI explanation scoring) — premature for MVP.

## Architecture at a glance

```
┌─────────────────────────────────────────────────────────────────┐
│  Next.js App (Vercel)                                           │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │ Student UI   │  │ Parent/Teacher   │  │ Admin Console    │   │
│  │ (lesson      │  │ Dashboard        │  │ (lesson editor)  │   │
│  │  player)     │  │ (read-only)      │  │                  │   │
│  └──────┬───────┘  └────────┬─────────┘  └────────┬─────────┘   │
│         └────────────┬──────┴─────────────────────┘             │
│                      ▼                                          │
│              /api/* route handlers                              │
│         (attempts, scoring, recommend, admin)                   │
└──────────────────────┬──────────────────────────────────────────┘
                       ▼
        ┌────────────────────────────────┐
        │  Supabase                      │
        │  - Postgres (content + state)  │
        │  - Auth (users, roles)         │
        │  - Storage (passage assets)    │
        │  - Row-level security          │
        └────────────────────────────────┘
```

Key boundaries:

1. **Content layer** (modules, lessons, passages, questions, evidence keys) — mostly read-only at runtime, edited via admin/seed.
2. **Attempt layer** (attempts, responses, evidence selections, explanations) — student-write, parent/teacher-read.
3. **Progress layer** (skill_progress, mistake aggregates) — derived; recomputed on attempt completion.
4. **Recommendation layer** — pure function over progress; no ML in MVP.

## File map (actual, 2026-05-29)

```
reading_app/
├── index.html                  # entry: Tailwind CDN, top nav, #app mount
├── src/
│   ├── main.js                 # hash router + home page + catalogs
│   ├── loader.js               # fetch+parse+validate (CSV lessons/quizzes, JSON lab/library)
│   ├── progress.js             # localStorage scores + status bands
│   └── views/
│       ├── lesson.js           # mini-lesson (markdown renderer)
│       ├── quiz.js             # 10-quiz flow + per-choice feedback
│       ├── lab.js              # Reading Lab dense-annotation passage
│       ├── library.js          # Library index / overview / section page
│       ├── reference.js        # Quick Reference (1-min checklist)
│       └── marking-guide.js    # 20-item marking guide
├── content/
│   ├── lessons/{m0,a1-a5,b1-b6,c1-c3}/*.csv   # 23 mini-lessons
│   ├── quizzes/{…}/*.csv                       # 24 × 10 = 240 quizzes
│   ├── lab/*.json                              # 15 dense-annotation texts
│   └── library/*.json                          # 3 long-form works
├── scripts/
│   ├── validate-content.py     # CI gate — validates all 4 content types
│   ├── gen_library_*.py        # one-shot Gutenberg parsers (macbeth/sherlock/moonstone)
│   ├── fix_lab_offsets.py      # substring re-anchor for annotation offsets
│   └── rewrite_library_annotations.py  # marking-code normalization + audit
├── docs/
│   ├── STRUCTURE.md            # architecture overview (read after this file)
│   ├── Diary.md                # dated development log
│   ├── curriculum_design.md    # curriculum spec (v3.1.3)
│   ├── csv_schemas.md          # locked CSV schemas (v1.1)
│   ├── marking.md              # 20-item marking code system
│   ├── article_marking_guide.md# Lab/Library annotation conventions
│   └── why_250.md · review_packet.md · …
├── design1.md                  # original product spec
├── context.md (this) · status.md · progress.md · project_plan.md
└── progress_tracking.md · feedback.md · review.md · test_status.md
```

Note: `progress_tracking.md` predates the Lab/Library work and tracks only the original phase plan — `docs/STRUCTURE.md` §9 is the current implemented-vs-planned source of truth.

## Key invariants to preserve

- **Evidence is non-negotiable.** Every higher-level question must require evidence selection. Schema must support `evidence_keys` per question from day 1.
- **Wrong-answer-type is a first-class field on every choice**, not an afterthought. The product differentiator depends on it.
- **One concept per lesson.** UI and content schema should make multi-concept lessons hard to build.
- **No speed-based rewards.** Gamification rewards precision (evidence accuracy, explanation quality) only.
- **Child privacy:** minimum PII (nickname + grade), parent email optional, no open-ended AI chat in MVP.
- **Content quality > content quantity.** 12 strong lessons beat 36 mediocre ones.

## What to read on session start

1. `design1.md` — product spec (long, but authoritative)
2. `context.md` (this file) — pointers and decisions
3. `status.md` — current focus
4. `progress_tracking.md` — component checklist
5. `review.md` — open architectural questions
6. `feedback.md` — most recent code review notes

## Out of scope for MVP (do not build)

- Live AI tutor / open-ended chat
- Student text upload (CommonLit/A3000 ingestion)
- Native iOS/Android app
- Adaptive difficulty engine
- Teacher classroom mode
- Heavy gamification (XP economies, leaderboards)
- MAP score guarantees or claims
