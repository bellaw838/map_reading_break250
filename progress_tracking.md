# progress_tracking.md — Component-level checklist

> One row per atomic component. Each row is sized so a single developer (human or agent) can pick it up, deliver it, and have it reviewed in isolation. Status updated as work progresses.
>
> Mapped to phases in `project_plan.md`. Content authoring tracked in `content/STATUS.md` (created in P0-3).

Status legend: `Not Started` · `In Progress` · `In Review` · `Complete` · `Blocked`

---

## Phase 0 — Foundations

| ID | Component | Deliverable | Tests | Status | Notes |
|---|---|---|---|---|---|
| P0-1 | Lesson CSV schema | Documented column list + Zod (or equivalent) validator | Validator unit tests pass on a sample row | **Complete** | 26 cols; doc at `docs/csv_schemas.md` v1.0 |
| P0-2 | Quiz CSV schema | Documented column list + validator | Validator passes 10 rows | **Complete** | 14 cols; same doc |
| P0-3 | Content directory + STATUS file | `content/lessons/`, `content/quizzes/` directories; `content/STATUS.md` tracks per-sub-concept content state | n/a | **Complete** | `content/{lessons,quizzes}/m0..m7/` created; `content/STATUS.md` tracks 31 content packs across 3 waves |
| P0-4 | Worked sample: Tone 4.3 | Full mini-lesson CSV + 10 quizzes CSV for `tone/03-neutral-vs-skeptical` | Both validate; render in next phase | **In Review** | Drafted by architect 2026-05-27. Validates against schema. Needs SME review for pedagogical quality. Known issue: correct-answer position is B-heavy (7 of 10). |
| P0-5 | Stack lock | Decision recorded in `context.md` + initial repo scaffold | Smoke: dev server boots | **Complete** | **Stack v0 = pure static (HTML + vanilla JS ESM + Tailwind CDN + CSV fetch + localStorage). v1 will rewrite against mywordbank.net's stack later.** |
| P0-6 | CI | Typecheck + lint + validator-pass on every PR | Green CI on first PR | **Complete** | `.github/workflows/ci.yml` runs `scripts/validate-content.py` on every push/PR. Validator covers schemas v1.1 including Module 0 exception. |
| P0-7 | Dev docs | `README.md` setup, `docs/STRUCTURE.md` skeleton, `docs/Diary.md` started | n/a | **Complete (README done)** | `README.md` covers stack, run instructions, validator usage, layout, doc reading order. STRUCTURE.md and Diary.md still optional — can add when project grows. |

---

## Phase 1 — Core lesson/quiz flow (single sub-concept)

| ID | Component | Deliverable | Tests | Status | Notes |
|---|---|---|---|---|---|
| P1-1 | CSV loader | Fetches lesson + quiz CSV for a given `{module}/{sub-concept-slug}` key; returns typed objects | Unit + integration | **Complete** | `src/loader.js` — RFC-4180 CSV parser, validator (mirrors `csv_schemas.md` v1.1 including Module 0 exception), shaped objects for UI. Tested against B4.1. |
| P1-2 | Mini-lesson page | Renders title, concept, examples, traps, quick_ref reminder | Component snapshot | **Complete** | `src/views/lesson.js` — renders title, quick_ref callout, markdown mini-lesson (paragraphs, bullets, **bold**), worked examples, common traps. Route `#/learn/{moduleId}/{fileBasename}` in `main.js`. B4.1 renders end-to-end. |
| P1-3 | MCQ component | 4-option MCQ, idle → answered → submitted → reviewed state machine | Unit + interaction | **Complete** | Implemented inline in `src/views/quiz.js` — buttons with selection state, disabled after submit, color-coded correct/incorrect on review. |
| P1-4 | Feedback panel | Shows correct answer, per-choice feedback for the picked choice, trap explanation | Component snapshot | **Complete** | Renders inside `src/views/quiz.js`. Shows "why X is wrong/right" for selected choice and additionally for correct choice when student gets it wrong. The teaching engine. |
| P1-5 | Quiz flow | Step 1 of 10 → 10 of 10; advances on submit; end-of-quiz score | E2E + state test | **Complete** | `renderQuizPage` in `src/views/quiz.js`. In-memory session state (answers + submitted flags + currentIndex). Progress bar, Submit/Next buttons. Route `#/quiz/{module}/{slug}`. localStorage persistence deferred to Phase 3. |
| P1-6 | Score + status band | Compute 0–10 score, map to status band (Mastered / Good / Review / Needs Practice); display at end | Unit (golden cases) | **Complete** | `statusBand()` in `src/views/quiz.js`. Bands per curriculum (9-10 Mastered / 7-8 Good / 5-6 Review / 0-4 Needs Practice). Color-coded end screen. **Module 0 is special-cased** — shows "Orientation Complete" with no score (per curriculum doc). |

---

## Phase 2 — Scaling + navigation

| ID | Component | Deliverable | Tests | Status | Notes |
|---|---|---|---|---|---|
| P2-1 | Home page | Lists all 8 modules with status badges | Snapshot | Not Started | |
| P2-2 | Module page | Lists sub-concepts in that module with status badges | Snapshot | Not Started | |
| P2-3 | URL scheme | `/learn/{module}/{slug}`; `/m/0` (Module 0); `/reference` | Routing test | Not Started | |
| P2-4 | All-30 P0 content load | Loader handles all 30 P0 sub-concept content packs | Integration | Not Started | Depends on content team shipping CSVs |
| P2-5 | Sub-concept ordering within module | Reads from a `module-order.json` or numeric prefix in slug | Unit | Not Started | Numeric prefix is simpler — `03-neutral-vs-skeptical.csv` etc. |

---

## Phase 3 — Progress tracking + dashboard

| ID | Component | Deliverable | Tests | Status | Notes |
|---|---|---|---|---|---|
| P3-1 | localStorage schema | Typed shape: `{ subConceptId, lastScore, bestScore, attempts, lastAttemptedAt }` | Round-trip test | **Complete** | `src/progress.js` — root key `break250.progress.v1`, map of sub-concepts keyed by `{module}/{basename}`. |
| P3-2 | Progress write/read | Save after each quiz attempt; read on page load | Integration | **Complete** | `recordAttempt()` called in `renderEndScreen()` of `src/views/quiz.js`. `getProgress()` and `statusBadge()` for reads. |
| P3-3 | Status band per sub-concept | Roll-up: best score → status | Unit | **Complete** | `statusFromScore()` and `statusBadge()` in `src/progress.js`. Module 0 special-cased (never scored). |
| P3-4 | Module-level roll-up | Aggregate sub-concept statuses to module status | Unit | **Complete** | `renderRollup()` in `src/main.js` — counts by status label and renders "X/Y attempted · counts" line per category. |
| P3-5 | Dashboard | Status grid + "Continue" CTA + reset button | Snapshot + E2E | **Complete** | Home page enhanced with status badges per sub-concept + per-category roll-up. "Reset progress" button with confirm. End-of-quiz screen shows best + attempt count on retake. |

---

## Phase 4 — Module 0 special handling

| ID | Component | Deliverable | Tests | Status | Notes |
|---|---|---|---|---|---|
| P4-1 | Module 0 lesson page | Special layout: 8-tool preview, "basic vs advanced reader" table | Snapshot | Not Started | Different from sub-concept lesson page |
| P4-2 | Module 0 quiz flow | 10 recognition quizzes (reuses P1-3, P1-4 components) | E2E | Not Started | |
| P4-3 | Completion-only status | After all 10 attempted, status = "Orientation Complete"; **no score displayed** | E2E + visual | Not Started | Per design; UI must respect |
| P4-4 | Dashboard segregation | Module 0 visually separate from Modules 1–7 mastery | Snapshot | Not Started | |

---

## Phase 5 — Quick Reference page

| ID | Component | Deliverable | Tests | Status | Notes |
|---|---|---|---|---|---|
| P5-1 | `/reference` route | Loads all P0 lesson CSVs, extracts `quick_ref`, renders grouped by module | Integration + perf | **Complete** | `src/views/reference.js` loads all 23 lessons in parallel, renders grouped by category, click any line to open the full mini-lesson. Print button included. |
| P5-2 | Always-on nav link | Top-nav link to `/reference` from every page | Manual | **Complete** | Top nav in `index.html` includes "Quick Reference" link. |

---

## Phase 6 — Polish, mobile, a11y, performance, pilot prep

| ID | Component | Deliverable | Tests | Status | Notes |
|---|---|---|---|---|---|
| P6-1 | Mobile lesson + quiz pass | Layout works on iOS Safari + Chrome Android | Manual cross-device | Not Started | |
| P6-2 | Keyboard nav | Full flow keyboard-only | Manual + Playwright keyboard test | **Partial** | Quiz: `1`-`4` select choices, `Enter` submits/advances. Buttons have `focus:ring`. Skip-to-content link in nav. Full keyboard E2E test still TBD. |
| P6-3 | A11y audit | Axe-core via Playwright; zero serious violations | CI gate | **Partial** | Added: `aria-live="polite"` on feedback panel, `role="status"` on score, `role="radiogroup"` on choices, `role="progressbar"` on progress bar, programmatic focus on new questions, skip-to-content link. Axe-core scan not yet run. |
| P6-4 | Lighthouse CWV | LCP < 2.5s, INP < 200ms, CLS < 0.1 on lesson, dashboard, reference | CI gate | Not Started | |
| P6-5 | Error monitoring | Sentry or equivalent with PII scrubbing | Smoke (forced error) | Not Started | |
| P6-6 | Pilot consent + privacy disclosure | Parent consent doc + in-app privacy disclosure for localStorage progress | Legal review | **Partial** | In-app privacy disclosure added to footer of `index.html` — explains localStorage scope, no tracking, no third-party scripts beyond Tailwind CDN, Reset Progress wipes everything. Parent consent doc for pilot still TBD. |

---

## Content workstream (parallel — does not block engineering phases except where noted)

Tracked at sub-concept granularity. Wave grouping per `project_plan.md` release ladder.

| ID | Sub-concept | Module | Wave | Status |
|---|---|---|---|---|
| C-M0 | Module 0 mini-lesson + 10 quizzes | 0 | 1 | Not Started |
| C-1.1 | Topic vs Main Idea | 1 | 1 | Not Started |
| C-1.2 | Main Idea vs Supporting Detail | 1 | 1 | Not Started |
| C-1.6 | Theme Is a Message, Not a Topic | 1 | 1 | Not Started |
| C-2.1 | Evidence Must Be Traceable to the Text | 2 | 1 | Not Started |
| C-2.2 | Best-Supported Answer | 2 | 1 | Not Started |
| C-2.3 | Proof vs Related Information | 2 | 1 | Not Started |
| C-2.6 | Inference = Clue + Reasoning | 2 | 1 | Not Started |
| C-2.10 | Avoiding Over-Inference | 2 | 1 | Not Started |
| C-4.1 | Tone vs Topic | 4 | 2 | Not Started |
| C-4.2 | Identifying Tone Words | 4 | 2 | Not Started |
| C-4.3 | Neutral vs Skeptical | 4 | 2 | **Sample — P0-4 worked example, Not Started** |
| C-4.6 | Mood vs Tone | 4 | 2 | Not Started |
| C-4.7 | Connotation | 4 | 2 | Not Started |
| C-4.8 | Word Choice Creates Tone | 4 | 2 | Not Started |
| C-5.1 | Five Common Structures | 5 | 2 | Not Started |
| C-5.2 | Signal Words | 5 | 2 | Not Started |
| C-5.3 | Paragraph Function | 5 | 2 | Not Started |
| C-5.4 | Sequence vs Cause/Effect | 5 | 2 | Not Started |
| C-3.1 | Three Core Purposes | 3 | 3 | Not Started |
| C-3.2 | Finer Purposes | 3 | 3 | Not Started |
| C-3.3 | Purpose vs Main Idea | 3 | 3 | Not Started |
| C-3.6 | Narrator vs Author | 3 | 3 | Not Started |
| C-6.1 | Claim, Evidence, Reasoning | 6 | 3 | Not Started |
| C-6.2 | Assumption | 6 | 3 | Not Started |
| C-6.3 | Counterclaim and Rebuttal | 6 | 3 | Not Started |
| C-7.1 | Imagery Creates Meaning | 7 | 3 | Not Started |
| C-7.2 | Symbolism | 7 | 3 | Not Started |
| C-7.4 | Speaker, not the Poet | 7 | 3 | Not Started |
| C-7.5 | Line Break | 7 | 3 | Not Started |
| C-7.9 | Tone Shift in Poetry | 7 | 3 | Not Started |
| C-8.1 | Context Meaning | 8 | 1 | Not Started |
| C-8.2 | Connotation from Context | 8 | 1 | Not Started |
| C-8.3 | Academic Verbs | 8 | 1 | Not Started |
| C-8.4 | Tone Vocabulary | 8 | 1 | Not Started |

**Totals:** 34 P0 sub-concepts + Module 0 = 35 content packs. **350 quizzes** + 35 mini-lessons. (Bumped 2026-05-27 in v2.4 with Module 8 addition.)

C-4.3 doubles as the **worked sample** in P0-4: shipping it first validates the CSV schemas end-to-end.

---

## Component dependency notes

- P0-4 (sample sub-concept) blocks P0-5 (stack lock). Don't pick a framework until the schema is proven against a real worked sample.
- P1-4 (Feedback panel) is the highest-risk UI component. Worth a code review before P1-5 (quiz flow) builds on it.
- P3-3 (`computeStatus`) is reused by P2-1 (home), P2-2 (module page), P3-5 (dashboard). Build it as a pure function early.
- P4-3 (Module 0 completion-only status) is a UX rule, not just code — review the dashboard mock with the curriculum doc open to make sure "Orientation Complete" never reads as a score.
- C-4.3 (sample content) gates P0-4, P1 testing, and all of Phase 2.
