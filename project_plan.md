# project_plan.md — Break 250 Reading

> Phased plan for the **mywordbank-pattern v1** of Break 250 Reading. Curriculum locked v3.1 (`docs/curriculum_design.md`): 3 MAP-aligned categories (A Literary, B Informational, C Vocabulary), 14 modules + Module 0.
>
> **Two ship targets:**
> - **MVP first ship:** 22 P0 sub-concepts + Module 0 = **230 quizzes** (vocab-first; hits all 3 MAP categories from day one).
> - **Launch v1 (full P0):** 40 P0 sub-concepts + Module 0 = **410 quizzes**.
>
> Phase plan below is unchanged from v3.0 — same loader, same UI, same flow. Only the content-workstream taxonomy and the wave structure shift.
>
> This plan **supersedes** the earlier 6-phase Supabase plan (now archived in git history). The product is dramatically simpler than the original `design1.md` envisioned: CSV-driven static-leaning web app, no backend DB, no auth in v1, no admin CMS, no diagnostic, no parent dashboard.

Phase ordering is dependency-driven. Components in `progress_tracking.md` are sized so a single developer (human or agent) can pick one up, deliver, and have it reviewed in isolation.

---

## Phase 0 — Foundations

**Goal:** Lock CSV schemas, validate with one worked sample, lock the tech stack, scaffold the repo, and get CI running.

**Success Criteria:**
- Lesson CSV schema and Quiz CSV schema written down with one row of every field documented.
- One worked sample sub-concept exists in `content/` — mini-lesson + 10 quizzes that load, parse, and validate. **Recommended sample: Tone 4.3 Neutral vs Skeptical** (highest-leverage, highest-trap).
- Stack locked and recorded in `context.md`.
- Repo scaffolded; `pnpm dev` (or equivalent) brings up a hello-world page.
- CI runs typecheck + lint on every push.

**Tests:**
- CSV-validator unit test: every shipped CSV passes Zod (or equivalent) validation.
- Smoke test: hello-world page returns 200 in dev.

**Dependencies:** Curriculum locked (DONE 2026-05-27).

**Status:** Not Started.

**Components:** P0-1 … P0-7.

---

## Phase 1 — Core lesson/quiz flow (single sub-concept)

**Goal:** A student can open one sub-concept's URL, read the mini-lesson, take the 10 quizzes, and see per-choice feedback. End-to-end works for one sub-concept only.

**Success Criteria:**
- CSV loader fetches lesson + quizzes for a given sub-concept key (e.g., `tone/4.3-neutral-vs-skeptical`).
- Mini-lesson page renders: title, concept text, examples, quick_ref reminder.
- Quiz flow: 1 of 10 → 10 of 10, MCQ, per-choice feedback shown after submit.
- Feedback panel surfaces the wrong-answer trap (`feedback_a`/`b`/`c`/`d`) for the choice the student picked.
- Score reported at end of 10 quizzes (e.g., "8/10 — Good").
- Status band mapping applied: 9–10 Mastered · 7–8 Good · 5–6 Review · 0–4 Needs Practice.

**Tests:**
- Component tests for MCQ, FeedbackPanel.
- E2E (Playwright): open sub-concept URL → submit one correct + one incorrect answer → see correct per-choice feedback → finish 10 → see end-of-quiz score.
- Manual: try on mobile viewport.

**Dependencies:** Phase 0 complete.

**Status:** Not Started.

**Components:** P1-1 … P1-6.

---

## Phase 2 — Scaling to multiple sub-concepts + navigation

**Goal:** All 30 P0 sub-concepts + Module 0 load and render. Student can navigate between modules and sub-concepts.

**Success Criteria:**
- Home page lists all 8 modules with progress badges.
- Module page lists all sub-concepts in that module with status badges.
- Sub-concept URLs are predictable: `/learn/{module}/{sub-concept-slug}`.
- Loader handles all 31 sub-concept content packs (30 P0 + Module 0).
- Module 0 routes to its special-format page (different from sub-concept lesson page).

**Tests:**
- E2E: navigate home → module → sub-concept → finish 10 quizzes → return to module list → see status updated.
- Snapshot test on each module's listing page.

**Dependencies:** Phase 1 complete; Phase 4 (Module 0) can run in parallel.

**Status:** Not Started.

**Components:** P2-1 … P2-5.

---

## Phase 3 — Progress tracking + dashboard

**Goal:** Progress persists across sessions (localStorage) and is summarized on the dashboard.

**Success Criteria:**
- Sub-concept results stored in localStorage as `{ module, subConcept, lastScore, bestScore, attempts, lastAttemptedAt }`.
- Dashboard shows per-sub-concept status, per-module roll-up, and the next recommended sub-concept.
- "Continue where I left off" button on home.
- Reset progress button (for the student or parent).
- Module 0 status displays as "Orientation Complete" or "Not Started" — never a score.

**Tests:**
- Unit: `computeStatus(score)` → returns correct band (Mastered / Good / Review / Needs Practice).
- Unit: localStorage round-trip (write → read → validate against schema).
- E2E: complete sub-concept → refresh page → see status persisted.

**Dependencies:** Phase 2 complete.

**Status:** Not Started.

**Components:** P3-1 … P3-5.

---

## Phase 4 — Module 0 special handling

**Goal:** Module 0 ships with its different shape — one mini-lesson covering all 8 tools, 10 recognition-format quizzes, completion-only status.

**Success Criteria:**
- Module 0 page renders the 8-tool preview lesson (different layout from sub-concept lessons).
- 10 recognition quizzes load and run.
- After all 10 attempted, status changes to "Orientation Complete." **No score appears anywhere** for Module 0.
- Dashboard segregates Module 0 visually from Modules 1–7.
- Student-facing module name comes from a single string (so it can be renamed later without code changes — see open Q13).

**Tests:**
- E2E: complete Module 0 → status shows "Orientation Complete," not a score.
- Visual diff: Module 0 layout distinct from sub-concept lesson layout.

**Dependencies:** Phase 1 complete (reuses MCQ + Feedback components). Can run in parallel with Phase 2.

**Status:** Not Started.

**Components:** P4-1 … P4-4.

---

## Phase 5 — Quick Reference page

**Goal:** Always-on `/reference` page renders the 1-minute pre-read checklist drawn from each lesson's `quick_ref` column.

**Success Criteria:**
- `/reference` loads all 30 P0 sub-concept CSVs (and Module 0) and renders the `quick_ref` field.
- Reference is grouped by module.
- Always-on link in top nav.
- Page loads in <1 second on a mid-tier mobile device.

**Tests:**
- Snapshot test on the rendered reference.
- Performance: TTI < 1s on emulated mid-tier mobile.

**Dependencies:** Phase 0 (loader) complete. Can run after Phase 1.

**Status:** Not Started.

**Components:** P5-1, P5-2.

---

## Phase 6 — Polish, mobile, a11y, performance, pilot prep

**Goal:** Ready to put in front of 5–10 real students.

**Success Criteria:**
- Mobile lesson + quiz flow works smoothly on iOS Safari and Chrome Android.
- Keyboard nav: full lesson → quiz → feedback achievable with keyboard only.
- Axe-core a11y scan: zero serious violations on lesson, quiz, dashboard, reference.
- Lighthouse CWV targets met: LCP < 2.5s, INP < 200ms, CLS < 0.1.
- Reset-progress + privacy disclosures present.
- Error monitoring (Sentry or equivalent) wired with PII scrubbing.
- Pilot recruitment doc + parent consent draft.

**Tests:**
- Lighthouse CI on lesson, dashboard, reference.
- Axe-core via Playwright on the same pages.
- Manual cross-browser: Chromium, Firefox, WebKit; mobile Chrome + Safari.

**Dependencies:** Phases 1–5 complete.

**Status:** Not Started.

**Components:** P6-1 … P6-6.

---

## Content workstream (parallel)

Engineering can finish Phases 0–6 in weeks. Content authoring (310 quizzes at the wrong-answer-trap quality bar) is months of careful work. Content runs in parallel from the moment Phase 0 sample is validated.

**Deliverables:**

| Item | Count |
|---|---:|
| Module 0 mini-lesson + recognition quizzes | 1 lesson + 10 quizzes |
| P0 sub-concept mini-lessons (Modules 1–8) | 34 |
| P0 quizzes | 340 |
| `quick_ref` one-liners (one per lesson, lives in lesson CSV) | 34 |

**Release ladder:** the app can launch with Module 0 + a single category's P0 sub-concepts and grow from there. Suggested first ship (after engineering is done):

| Wave | Sub-concepts | Quizzes |
|---|---|---:|
| Wave 1: Module 0 + Module 1 P0 (3) + Module 2 P0 (5) + **Module 8 P0 (4)** | 12 + Module 0 | 130 |
| Wave 2: Module 4 P0 (6) + Module 5 P0 (4) | +10 | +100 |
| Wave 3: remaining P0 (Modules 3, 6, 7) | +12 | +120 |
| **Full Launch v1** | **34 + Module 0** | **350** |

Wave 1 is enough to be useful to a pilot user. **Module 8 P0 sub-concepts ship in Wave 1** because vocabulary nuance is the highest-leverage area per MAP analysis — without it, Wave 1 lacks the most direct path to breaking 250.

---

## Cross-cutting workstreams

| Workstream | Notes |
|---|---|
| **Documentation** | `progress.md`, `docs/Diary.md`, `STRUCTURE.md`, `README.md` updated each session per global rules. |
| **Code review** | After every phase, `code-reviewer` + `typescript-reviewer` (or stack-equivalent reviewer) agents run. |
| **Curriculum updates** | Reviewers may still push back on Q1–Q14. Apply updates to `docs/curriculum_design.md` as a separate change; do not entangle with engineering phases. |

---

## Risk register (top 5)

1. **Content authoring throughput.** 310 quizzes at trap-led quality is the long pole. *Mitigation:* incremental release waves (see above), worked sample early to nail style.
2. **Mobile UX for two-column reading.** A short mini-lesson + 10 quizzes on a phone is far more tractable than the original two-pass close-reading flow, but still needs early testing. *Mitigation:* test mobile in Phase 1, not Phase 6.
3. **CSV editing pain.** Multi-line mini-lesson text in a quoted CSV cell is awkward to author. *Mitigation:* if it gets painful, promote `mini_lesson` to a sibling `.md` file without touching the rest of the schema.
4. **Module 0 quizzes feel too easy.** Recognition-only quizzes can be passed without learning the tools. *Mitigation:* UI labels Module 0 as "Orientation Complete," never a score (already designed in).
5. **Privacy & age gating.** Even without accounts, the app collects progress in localStorage. Consent disclosure required before pilot. *Mitigation:* Phase 6 includes consent draft.

---

## Phase exit checklist (apply to every phase)

- [ ] All components in `progress_tracking.md` for the phase marked Complete
- [ ] Tests passing
- [ ] `code-reviewer` agent run; findings addressed or triaged to `feedback.md`
- [ ] `progress.md` updated with what shipped and what slipped
- [ ] `status.md` points at the next phase's first component
