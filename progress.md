# progress.md — Development progress log

> Narrative log of what shipped, what slipped, and decisions made each session. Updated by the architect after each review pass.

Cross-reference with `project_plan.md` (phase definitions) and `progress_tracking.md` (component checklist).

---

## 2026-05-26 — Architect pass: initial setup

**Phase:** Pre-Phase-0 (planning only).

**What happened:**
- Architect reviewed `design1.md` (1823-line product spec).
- Created `context.md`, `project_plan.md`, `progress_tracking.md`, `status.md`, `test_status.md`, `feedback.md`, `review.md`, `progress.md`.
- No code written; no schema migrated; no stack locked yet.

**Decisions captured (proposed, awaiting confirmation):**
- Single-language TypeScript stack: Next.js (App Router) + Supabase.
- Defer FastAPI / Python until ML scoring becomes a real need (post-MVP).
- Defer admin UI to Phase 5; seed content via JSON in `/content/` for Phases 1–4.
- Manual explanation scoring only for MVP; AI rubric scoring is post-MVP.
- 6 phases, 51 atomic components.

**Open questions (see `review.md`):**
1. Confirm Next.js + Supabase vs alternative stack before P0-2.
2. Confirm rolling-window size for `computeMastery()` (suggest last 20 responses per skill).
3. Who owns content writing? Engineering cannot ship without 3 lessons by end of Phase 1.
4. Is React Native deferred to truly post-MVP, or do we want a thin wrapper after pilot?

**What slipped:** nothing — this is the first pass.

**Next action:** see `status.md`. Owner needs to confirm stack and resource content authoring before Phase 0 starts.

---

---

## 2026-05-26 — Direction pivot + curriculum design doc

**Phase:** Pre-Phase-0 (still planning).

**What happened:**
- User clarified product direction: **mywordbank.net pattern**. One concept = one mini-lesson + exactly 10 quizzes. No backend DB. No passages library. No AI tutor. CSV-driven content.
- This **supersedes** the 6-phase plan in `project_plan.md` — that plan was designed against `design1.md`'s fuller scope. Most of it (RLS, Supabase auth, diagnostic engine, parent dashboard, admin CMS) collapses or disappears for v1.
- Concept count reduced from 12 to **10** (Poetry and Paired Texts cut for MVP).
- File structure: `content/lessons/{concept}.csv` (1 wide row) + `content/quizzes/{concept}.csv` (10 rows).
- Added a **Quick Reference** page (`/reference`) — 1-minute pre-read checklist drawn from a new `quick_ref` column on each lesson CSV.
- Stack decision deferred (tried to fetch mywordbank.net to mirror its stack; couldn't extract from public HTML).
- Curriculum design doc written: `docs/curriculum_design.md`. Self-contained — reviewers don't need `design1.md` or chat history to engage.

**Decisions captured:**
- 10 concepts, ~5 sub-concepts each.
- One mini-lesson per concept (covers all sub-concepts in one read).
- 10 quizzes per concept, with default mix: 2 concept-id + 2 sentence example + 4 short-passage + 1 trap-focus + 1 evidence.
- Per-choice feedback (`feedback_a`, `feedback_b`, …) is non-negotiable — it's the teaching engine.
- Status bands: 9–10 Mastered / 7–8 Good / 5–6 Review / 0–4 Needs Practice.
- Lesson CSV: wide single row, max 5 example slots, N/A for empty.
- Quiz CSV: 10 rows, tabular.
- Cross-concept overlaps (Tone↔Word Choice, Inference↔Evidence, etc.) are intentional features.

**What slipped:**
- `project_plan.md` and `progress_tracking.md` are now stale — they assume Supabase + RLS + 6 phases. They need rewriting once curriculum is reviewer-approved.

**Open / blocked on:**
- External reviewer feedback on `docs/curriculum_design.md` (user is circulating to ELA SMEs / other devs).
- Stack decision (deferred until content shape is locked).

**Next action:**
- Wait for reviewer feedback on curriculum.
- Once curriculum locks: rewrite `project_plan.md` and `progress_tracking.md` to match the simpler v1 scope, then either (a) draft a sample lesson + quiz CSV for one concept as a worked-example check, or (b) lock the stack and scaffold.

---

---

## 2026-05-26 (later same day) — Sub-concept granularity resolved

**Phase:** Pre-Phase-0.

**What happened:**
- User challenged two assumptions in the curriculum doc: (a) the arbitrary "~5 sub-concepts" cap, (b) whether 10 quizzes was per concept or per sub-concept.
- Resolution: **per sub-concept**, no cap on count. This is the genuine mywordbank "per knowledge point" pattern.
- Curriculum doc updated: §2 product context, §3 design principles, §5 sub-concepts intro, §7 quiz coverage, §9 open questions (Q3 removed since answered, Q1 reframed).
- H-4 in `feedback.md` resolved.

**Decisions captured:**
- **Sub-concept = atomic unit.** One mini-lesson + 10 quizzes per sub-concept. Concept is just a category folder.
- **No cap on sub-concept count per concept.** Reviewer-driven. Likely 3–7 in practice.
- **File structure: nested.** `content/lessons/{concept}/{NN-slug}.csv` + `content/quizzes/{concept}/{NN-slug}.csv`.
- **Volume target for v1:** ~50 mini-lessons + ~500 quizzes (5x earlier estimate). Content authoring is the long pole; architecture supports incremental shipping.
- **Progress tracking:** per sub-concept; concept-level mastery is a roll-up display.

**What slipped:**
- Nothing new — `project_plan.md` and `progress_tracking.md` were already stale. They now need to be rewritten against a 500-quiz content backlog (vs 100 previously).

**Next action:** unchanged — wait for reviewer feedback on `docs/curriculum_design.md`.

---

---

## 2026-05-26 (later same day) — External reviewer feedback received

**Phase:** Pre-Phase-0.

**What happened:**
- External reviewer (relayed by user) returned a substantial proposal: add **Module 0 (Reading-Analysis Abstract)** + restructure from 10 concepts to **8 modules** (Module 0 + 7 categorized modules).
- Reviewer-proposed module structure:
  - 0. Reading-Analysis Abstract (one mini-lesson + 10 recognition quizzes)
  - 1. Central Idea / Theme (merges Main Idea + Theme)
  - 2. Evidence & Inference (merges Evidence + Inference)
  - 3. Author's Purpose & Point of View (adds POV)
  - 4. Tone & Word Choice (merges — answers open Q4)
  - 5. Text Structure & Development
  - 6. Argument & Comparison (adds Comparison)
  - 7. Figurative Language & Poetry (restores Poetry)
- Reviewer also proposed quiz volume options: 170 (full) or 100 (minimal) — but these are **per module**, not per sub-concept, which conflicts with our earlier resolution.

**Tensions surfaced:**
- **Granularity contradiction.** Reviewer's "17 lessons × 10 quizzes" model contradicts the per-sub-concept decision from earlier today. Both consistent internally but produce different products.
- **Framing drift.** Reviewer's sub-concept lists are topic vocabularies (e.g., "topic, main idea, detail, summary"); my doc treats sub-concepts as trap-disarming atomic tools. Trap-led is the product differentiator.

**Architect recommendation back to user:**
- Path C (hybrid): Module 0 is one all-up lesson by design; Modules 1–7 keep per-sub-concept granularity. Keep trap-led framing throughout.
- Accept reviewer's 8-module structure (Module 0 + merges + restored concepts).
- Update curriculum doc once user confirms path.

**Decisions captured (pending user confirmation):**
- Add Module 0 (Reading-Analysis Abstract) — YES (user explicitly approved).
- Module 0 quizzes are recognition-format (identify which tool a question tests), not mastery-format.
- Merge Tone + Word Choice — recommended YES (resolves open Q4).

**What slipped:** nothing new.

**Open / blocked on:**
- User to choose granularity Path A / B / C.
- Then curriculum doc rewrite (substantial — 8-module structure, Module 0, retranslate sub-concept lists with traps).

**Next action:** wait for user's path choice; then rewrite `docs/curriculum_design.md`.

---

---

## 2026-05-26 (later same day) — Curriculum doc v2 written

**Phase:** Pre-Phase-0.

**What happened:**
- User picked the combined path (Path C hybrid + accept reviewer structure + keep trap-led framing).
- Rewrote `docs/curriculum_design.md` from v1 (10 concepts, ~50 sub-concepts) to **v2** (8 modules: Module 0 + 7, ~59 sub-concepts).

**Key v2 changes:**
- Added §5.0 Module 0 (Reading-Analysis Abstract) with explicit special-case rules (one lesson, 10 recognition quizzes, UI labels as "Orientation" not "Mastered").
- Restructured to 8-module layout per external reviewer.
- Applied merges: Tone+Word Choice (Module 4, 11 sub-concepts), Main Idea+Theme (Module 1, 10), Evidence+Inference (Module 2, 10).
- Restored coverage: POV as Module 3 sub-concepts 3.6–3.8 (Narrator vs Author, Reliability, Bias); Mood vs Tone as 4.6; Compare Viewpoints as 6.6; Poetry tools as 7.6–7.9 (Speaker, Line Break, Repetition, Tone Shift in Poetry).
- Kept trap-led framing throughout (architect priority) — every sub-concept names a specific trap.
- Resolved v1 Q3 (granularity = Path C hybrid) and v1 Q4 (Tone+WC merge = YES) in §9.
- Added 12 v2 open questions for reviewers, including new Q11 (Module 0 scoring approach) and Q12 (Argument & Comparison grouping).
- Added Appendix A change log.

**Decisions captured:**
- Module 0 is a one-lesson special case; recognition quizzes only; UI label "Orientation."
- Modules 1–7 keep one-sub-concept-per-lesson rule.
- Volume: ~600 quizzes total (10 Module 0 + 590 across Modules 1–7).
- Trap-led sub-concept design preserved (product differentiator).

**What slipped:** nothing new — `project_plan.md` and `progress_tracking.md` still stale (now against 600-quiz target, up from earlier 500).

**Open / blocked on:**
- External reviewer feedback on `docs/curriculum_design.md` v2.

**Next action:** wait for reviewer feedback; then rewrite plan + tracker; then lock CSV schemas; then draft a sample sub-concept end-to-end.

---

---

## 2026-05-26 (later same day, round 2 reviewer feedback) — Curriculum v2.1

**Phase:** Pre-Phase-0.

**What happened:**
- External reviewer returned round-2 feedback. Strong approval of the overall design (Module 0, sub-concept-as-atomic-unit, trap-led framing, module structure). Main pushback: 600 quizzes is too ambitious for launch quality.
- Rewrote `docs/curriculum_design.md` from v2 → **v2.1**.

**Key v2.1 changes:**

*Priority system (new):*
- Added P0/P1/P2 labels to every sub-concept.
- New §4.1 Launch v1 scope: P0 = launch, P0+P1 = full v1, all = master curriculum.
- Volume tiers: Launch 310 / Full v1 500 / Master 610.

*Content / sub-concept changes:*
- Module 1: merged 1.6 (Theme vs Topic) + 1.7 (Theme as Complete Sentence) → **"Theme Is a Message, Not a Topic"** (P0). Module 1 now has 9 sub-concepts (was 10).
- Module 2: softened 2.1 — evidence must be **traceable**, not strictly quoted.
- Module 5: added new **5.4 Sequence vs Cause/Effect** (P0). Module 5 now has 6 sub-concepts.
- Module 6: renamed 6.5 "Basic Logical Moves" → **"Emotional Appeal vs Logical Evidence"** (P1).
- Module 7: reordered so Imagery / Symbolism / Speaker / Line Break lead. Simile vs Metaphor demoted to P1.
- Module 0: changed from scored to **completion-only** — UI shows "Orientation Complete," never a score. Resolves v2 open Q11.
- §5.4 Tone intro softened ("likely one of the highest-leverage" vs absolute claim).

*Resolved questions:*
- v2 Q11 (Module 0 scoring) → completion-only, no score.

*Net effect:*
- Sub-concept count effectively unchanged (~60).
- Quiz volume tiered: 310 launch / 500 full v1 / 610 master.
- Launch scope is **roughly half** of what v2 implied.

**Decisions captured:**
- Launch v1 = P0 only = ~310 quizzes (30 sub-concepts + Module 0).
- Module 0 not scored; "Orientation Complete" status only.
- Priority labels reviewer-editable but architect-recommended.
- Trap-led framing preserved (still the differentiator).

**What slipped:**
- `project_plan.md` and `progress_tracking.md` continue to be stale. Rewrite must now target **310-quiz** launch (not 500 or 600). Must include an explicit content-release ladder per finding M-7.

**Open / blocked on:**
- Reviewer round-3 sign-off on v2.1 priority labels and Launch v1 size.

**Next action:** wait for sign-off; then rewrite plan + tracker for 310-quiz launch; lock CSV schemas; lock stack; draft sample sub-concept (likely Tone 4.3 Neutral vs Skeptical) end-to-end.

---

---

## 2026-05-26 (later, GPT reviewer pass) — Curriculum v2.2

**Phase:** Pre-Phase-0.

**What happened:**
- GPT reviewer feedback received in `docs/gpt_feeback.md`.
- GPT caught two real errors (count off by one; Module 7 Simile narrative-vs-table contradiction) plus several sharp recommendations.
- Rewrote `docs/curriculum_design.md` from v2.1 → **v2.2** to apply fixes and reviewer-approved recommendations.

**Key v2.2 changes:**

*Arithmetic fixes:*
- Full v1 rollup corrected: 48 + Module 0 / 490 quizzes (was 49 / 500).
- Master curriculum corrected: 59 + Module 0 / 600 (was 60 / 610).

*Priority shifts:*
- Module 7.3 Simile vs Metaphor: P0 → P1 (Break-250-level students already know this).
- Module 7.9 Tone Shift in Poetry: P2 → P0 (higher-leverage, better thesis fit, connects to Module 4).
- Module 5.5 Structure Reveals Argument: P2 → P1 (bridges to Module 6).

*Module 0 quiz simplification:*
- Quiz #7: "→ Poetry / Structure" → "→ Figurative Language & Poetry" (single-tool).
- Quiz #10: "Mixed: ... → Evidence + Inference" → single-tool Evidence example.

*New content:*
- §4.1 tighter MVP option (~210 quizzes). Lists 4 demotion candidates; 5 more pending reviewer call.
- §5.0 student-facing name note ("The 8 Reading Tools" candidate; UI decision later).
- §9 added Q13 (Module 0 rename) and Q14 (Mood vs Tone — reviewers disagree).
- Appendix A change log entry for v2.2.

*Final priority counts:* P0=30, P1=20, P2=9. Sub-concept total: 59. With Module 0: 60 items.

**Decisions captured:**
- All GPT high-priority fixes applied as recommended.
- 7.3↔7.9 swap matches GPT pedagogical reasoning, not just count reconciliation.
- Module 0 single-tool quiz format is now consistent.
- Tighter MVP option surfaced explicitly; not yet adopted.

**What slipped:** none new; `project_plan.md` / `progress_tracking.md` remain stale.

**Open / blocked on:**
- Q12 (Launch v1 size: 310 vs 210).
- Q13 (Module 0 student-facing name).
- Q14 (Mood vs Tone priority — reviewers disagree).
- 11 other questions from earlier rounds.

**Next action:** user/reviewer call on Q12; then lock curriculum; then rewrite plan + tracker.

---

---

## 2026-05-27 — Q12 locked + plan/tracker rewrite

**Phase:** Entering Phase 0.

**What happened:**
- User locked **Q12: Launch v1 = 310 quizzes** (30 P0 sub-concepts + Module 0). Tighter MVP option (~210) considered and not adopted.
- Curriculum doc bumped to **v2.3** to record the lock. Master remains 600; Full v1 (post-launch) remains 490.
- **Curriculum is now substantially locked for engineering purposes.** Remaining open questions (Q1–Q11, Q13, Q14) are non-blocking and can be applied as later revisions.
- Rewrote `project_plan.md` from the old 6-phase Supabase plan to the new 6-phase mywordbank-pattern plan. No more DB, RLS, admin CMS, diagnostic, parent dashboard. Static-leaning CSV-driven web app with localStorage progress.
- Rewrote `progress_tracking.md` from 51 atomic components (old) to ~37 (new: 7+6+5+5+4+2+6 engineering + 31 content tracker rows).
- Added an explicit **content release ladder** (Wave 1: Module 0 + 8 P0 sub-concepts ≈ 90 quizzes; Wave 2: +10 ≈ +100; Wave 3: +12 ≈ +120).
- Named **Tone 4.3 "Neutral vs Skeptical"** as the worked sample for Phase 0 (P0-4 + C-4.3).

**Decisions captured:**
- Launch v1 size: 310 quizzes. Locked.
- Stack lock deferred until Phase 0 worked sample (P0-4) validates schemas.
- File structure: `content/lessons/{module}/{NN-slug}.csv` + `content/quizzes/{module}/{NN-slug}.csv`.
- Content authoring ships in 3 waves, not all-at-once.
- Module 0 atomic in the plan: own phase (Phase 4), separate UX, completion-only status.

**What slipped:** none — this was an alignment / replanning pass, not feature work.

**Open / blocked on:**
- P0-1 + P0-2: lock CSV schemas as a small ADR + validator.
- Then P0-4 worked sample.
- Then P0-5 stack lock.

**Next action:** start P0-1 (lesson CSV schema doc + validator).

---

---

## 2026-05-27 (later) — P0-1, P0-2, P0-3 complete

**Phase:** Phase 0 — Foundations.

**What shipped:**
- **P0-1 + P0-2:** locked CSV schemas. `docs/csv_schemas.md` v1.0. 26 columns for lesson, 14 columns for quiz. Includes RFC-4180-style quoting rules, N/A convention for unused optional fields, example-sequencing rule (no gaps), and an illustrative TypeScript+Zod reference implementation.
- **P0-3:** content directory structure created (`content/lessons/m0..m7/`, `content/quizzes/m0..m7/`); `content/STATUS.md` tracks the 31 content packs across 3 release waves (Wave 1 = 9 packs / ~90 quizzes; Wave 2 = 10 / ~100; Wave 3 = 12 / ~120).

**Decisions captured:**
- File naming: `{NN}-{slug}.csv` under per-module folders (`m0`..`m7`).
- Module 0 reuses the same schemas; `mini_lesson` carries the entire orientation as markdown; examples and common_trap fields are `N/A`.
- `mini_lesson` lives inline in the CSV cell for now; escape hatch to a sibling `.md` file if multi-line editing becomes painful.
- 3 low-risk open schema questions noted in `csv_schemas.md` §"Open schema questions" — non-blocking.

**What slipped:** nothing.

**Open / blocked on:**
- P0-4 worked sample (Tone 4.3 "Neutral vs Skeptical") — content drafting, validates the schemas in practice.
- P0-5 stack lock — held until P0-4 lands.

**Next action:** draft P0-4. Content authoring task — produce the canonical example pack that other content writers will reference.

---

---

## 2026-05-27 (later) — P0-4 worked sample drafted

**Phase:** Phase 0 — Foundations.

**What shipped:**
- **P0-4 worked sample:** Tone 4.3 "Neutral vs Skeptical."
  - `content/lessons/m4/03-neutral-vs-skeptical.csv` — 26-column lesson with ~500-word mini-lesson, quick_ref (160 chars), 4 worked examples (5th is N/A as schema allows), 3 common traps.
  - `content/quizzes/m4/03-neutral-vs-skeptical.csv` — 10 trap-revealing quizzes with per-choice feedback on every row.
- Both CSVs validate cleanly against the v1.0 schemas (verified via Python csv module): correct column counts, sequencing, all required fields filled, quiz_ids unique, question_numbers 1–10 with no gaps.

**Quality status:**
- **Schema conformance:** PASS.
- **Pedagogical review:** PENDING. SME must read and approve before this becomes the canonical template.
- **Known issue:** correct-answer position is B-heavy (7 of 10 correct = B). Authoring bias. Flagged in `content/STATUS.md` as a content-style rule to avoid going forward; needs rebalancing in this sample before it ships as the template.
- **Genre balance:** all nonfiction in this sample. Future content should mix in fiction/poetry/opinion per curriculum §9 Q8 (~50/30/10/10).

**Decisions captured:**
- Mini-lesson markdown rendering happens at display time; the CSV cell holds raw markdown.
- "How to use this tool" mini-section inside the mini_lesson is a useful pattern — make it part of the style guide.
- Quiz mix matched curriculum §7 default (2 concept-ID + 2 sentence + 4 passage + 1 trap-focus + 1 evidence).

**What slipped:** none.

**Open / blocked on:**
- SME review of worked sample.
- Then P0-5 (stack lock) — held until quality bar is set by approved sample.

**Next action:** SME review. After approval (or with revisions): proceed to P0-5 stack lock.

---

---

## 2026-05-27 (late) — v2.4 redesign: Module 8 + `why_250.md`

**Phase:** Phase 0 (paused engineering for curriculum redesign).

**Trigger:** User shared specific MAP-data analysis for a target student showing Vocabulary at 233–245 vs overall Reading at 246. Analysis identifies vocabulary nuance as the #1 unlocking factor for breaking 250. User requested:
1. A file explaining "Part 2: MAP 250+ is about author-thinking comprehension."
2. A new curriculum module for vocabulary, explicitly framed as not flashcard memorization.

**What shipped:**

*New doc:*
- **`docs/why_250.md`** — public-facing manifesto. Sections: The plateau; What MAP 250+ tests; The shift to author-thinking; Four MAP sub-areas; Priorities 1–3 (Vocabulary, Literary inference, Informational analysis); How Break 250 Reading addresses these; What this means for a student stuck at 240–249. Drafted from user's analysis, generalized for any plateaued advanced reader.

*Curriculum changes (v2.3 → v2.4):*
- Added **Module 8: Vocabulary in Context** with 6 sub-concepts (4 P0, 2 P1):
  - 8.1 Context Meaning, 8.2 Connotation from Context, 8.3 Academic Verbs, 8.4 Tone Vocabulary (all P0)
  - 8.5 Word Precision, 8.6 Figurative Word Meaning (P1)
- §4 module list updated from 8 modules to 9 (added row 8).
- §4.1 Launch v1 totals: 30 + Module 0 / 310 → **34 + Module 0 / 350**.
- §5.0 Module 0 updated: previews 9 tools (not 8); phrasing changed to "the core reading tools" for count-flexibility.
- §6 added two new overlap rows: Module 4 ↔ Module 8, and Module 7 ↔ Module 8.6.
- §7 volume rollup table updated.
- §9 added Q15 (Module 8 sub-concept count), Q16 (Module 4 ↔ Module 8 boundary), Q17 (vocabulary passage source).
- Appendix A v2.4 changelog entry.
- Final priority counts: P0=34, P1=22, P2=9 (total 65 + Module 0).

*Content / engineering updates:*
- `content/lessons/m8/` and `content/quizzes/m8/` directories created.
- `content/STATUS.md` updated: 31 → 35 content packs; Wave 1 expanded to include Module 8 P0 (4 sub-concepts) → 130 quizzes in Wave 1.
- `project_plan.md` updated: 30 → 34 P0 sub-concepts; release ladder updated; Module 8 explicitly noted as Wave-1 priority for the unlocking-vocabulary reason.
- `progress_tracking.md` content workstream extended with C-8.1, C-8.2, C-8.3, C-8.4.

**Decisions captured:**
- Module 8 is its own module, not a sub-section of Module 4. Different angle (decoding/lexicon-building vs reading-the-text).
- Module 8 P0 sub-concepts ship in Wave 1, not Wave 3, because vocabulary is the highest-leverage path to breaking 250 per the user's MAP-data evidence.
- Module 0 references 9 tools and uses count-flexible phrasing in case the curriculum grows further.
- The worked sample (Tone 4.3) and schema lock (v1.0) are unaffected by v2.4 — same schemas, same file structure, same per-choice feedback engine.

**What slipped:**
- P0-4 SME review delayed by the redesign pass; resumes after v2.4 curriculum is approved.

**Open / blocked on:**
- SME review of P0-4 worked sample (Tone 4.3).
- Reviewer review of v2.4 curriculum additions + `docs/why_250.md`.
- Then stack lock (P0-5).

**Next action:** await SME + reviewer pass on v2.4. After approval: rebalance P0-4 answer positions, then P0-5 stack lock, then begin Wave 1 content authoring.

---

---

## 2026-05-27 (later) — v3.0 structural redesign

**Phase:** Phase 0.

**Trigger:** User direction — "let's redesign from scratch to match the 3 categories (mark are given to categories right?)" — restructure curriculum to mirror the 3 MAP scoring sub-areas: Literary Text, Informational Text, Vocabulary.

**What shipped:**

*Curriculum (v2.4 → v3.0):*
- Replaced 8 skill-organized modules with **3 MAP-aligned categories**: A Literary (5 modules), B Informational (6 modules), C Vocabulary (1 module) — 12 modules + Module 0.
- Renumbered all sub-concept IDs with category prefix (A1.1, B4.1, C1.3, etc.).
- Tone split into A4 (fiction signals) and B4 (nonfiction signals — neutral vs skeptical, hedging verbs).
- Inference moved to Category A; Evidence stays in Category B. Cross-overlap documented.
- Vocabulary elevated from sub-module to top-level Category C.
- New §6 cross-category overlap section (intentional, not bugs).
- New §8 carrier table mapping v2.4 modules to v3.0 categories.
- §9 open questions replaced with v3.0-relevant questions (10 of them).
- Final priority counts: P0=37, P1=16, P2=9 (total 62).

*Volume tiers:*
- Launch v1: 380 quizzes (37 P0 + Module 0) — up from v2.4's 350.
- Full v1: 540 quizzes.
- Master: 630 quizzes.

*Content directories restructured:*
- New: `a1..a5/, b1..b6/, c1/` under `content/lessons/` and `content/quizzes/`.
- Old `m1..m8` folders removed (Module 0's `m0/` kept).
- Worked sample (Tone 4.3) moved from `m4/03-neutral-vs-skeptical.csv` to `b4/01-neutral-vs-skeptical.csv`.
- Updated `module_id` (m4 → b4), `sub_concept_id` (4.3 → B4.1), `quiz_id` (`tone_4-3_q*` → `b4-1_q*`), `trap_type` (`4.3-neutral-vs-skeptical` → `b4.1-neutral-vs-skeptical`).
- Re-validated against schemas — PASS.

*Other docs updated:*
- `docs/csv_schemas.md` file-layout section updated for v3.0 paths and ID conventions.
- `docs/why_250.md` module map updated to v3.0 (3 categories × their modules).
- `content/STATUS.md` rewritten: 38 content packs in 3 waves, Wave 1 hits all 3 categories from day one.
- `status.md` rewritten for v3.0.

*Not yet updated:* `project_plan.md` and `progress_tracking.md` mostly carry forward — phases are unchanged, only content-workstream IDs need refresh.

**Decisions captured:**
- Top-level structure = 3 categories matching MAP scoring sub-areas.
- Tone is bifurcated (A4 + B4); each module teaches the signals appropriate to its text type.
- Wave 1 ships across all 3 categories so pilot users see the full structure.
- Worked sample's content unchanged; only IDs/path change.
- Module 0 stays as the single orientation entry, now previewing 3 categories instead of 8/9 tools.

**What slipped:**
- P0-4 SME review delayed by the v3.0 redesign pass; resumes once structure is approved.

**Open / blocked on:**
- SME validation of 3-category structure (§9 Q1 in curriculum doc).
- SME pedagogical review of P0-4 worked sample (now B4.1).
- Then P0-5 stack lock.

**Next action:** await SME pass on v3.0 + worked sample. After approval: rebalance answer positions in B4.1, then P0-5.

---

---

## 2026-05-27 (latest) — v3.1: vocab expanded, B-inference added, MVP tier explicit

**Phase:** Phase 0.

**Trigger:** External reviewer feedback flagged: (1) `csv_schemas.md` Zod enum was stale (still `m0..m7`); (2) Vocabulary was underweighted (40 quizzes vs Literary 140 / Informational 190) — contradicts the MAP-data thesis that vocabulary is the bottleneck; (3) No explicit informational inference; (4) Launch v1 of 380 too large for first quality launch — recommend a tighter MVP 210–250 quizzes.

**What shipped:**

*Curriculum (v3.0 → v3.1):*
- **Category C expanded 1 → 3 modules:**
  - C1 Context Meaning (C1.1, C1.2, C1.3 — all P0)
  - C2 Word Nuance & Precision (C2.1 P0, C2.2 P1)
  - C3 Academic & Tone Lexicon (C3.1, C3.2 — both P0)
- **B2 expanded** from "Evidence" (4 sub-concepts) to "Evidence & Inference (Informational)" (6 sub-concepts). Added B2.5 Inference from Nonfiction Cues (P0) and B2.6 Avoiding Over-Conclusion (P1).
- **Promotions:** C1.3 Figurative Word Meaning P1→P0; C2.1 Word Precision P1→P0.
- **Explicit MVP tier added** to §4.1: 22 sub-concepts + Module 0 = 230 quizzes. Vocab-first. Within reviewer's recommended 210–250 range.
- §6 cross-category overlap rows updated for new C module IDs (C3.2 for Tone Vocabulary, C2.2 for Hedge vs Strong).
- §8 carrier table updated for v3.1 changes.
- §9 Q10 (vocab split) marked RESOLVED; added Q11 (MVP composition).
- Appendix A v3.1 changelog.

*Final priority counts:* P0=40, P1=16, P2=9 (total 65 + Module 0).

*Volume tiers:*
| Tier | Sub-concepts | Quizzes |
|---|---:|---:|
| MVP | 22 + Module 0 | 230 |
| Launch v1 | 40 + Module 0 | 410 |
| Full v1 | 56 + Module 0 | 570 |
| Master | 65 + Module 0 | 660 |

*Doc fixes:*
- `docs/csv_schemas.md`: Zod ModuleId enum updated to `m0, a1..a5, b1..b6, c1..c3`. File-layout example updated. Example rows abbreviated (full content in worked sample). `sub_concept_id` format documented (`A1.1`, `B4.1`, `C1.3`).
- `docs/why_250.md`: Category C module map updated from 1 module to 3 modules. Note added explaining the 3-module weight reflects vocabulary being the bottleneck.

*Content directories:* added `content/lessons/c2/`, `content/lessons/c3/`, `content/quizzes/c2/`, `content/quizzes/c3/`. Total module dirs: 15 (m0 + a1..a5 + b1..b6 + c1..c3).

*Wave structure rewritten:* `content/STATUS.md` now organized as **MVP (22 packs + Module 0)** → **Post-MVP P0 (18 more packs)** → P1/P2. MVP composition: all 6 vocab P0 + 9 literary P0 + 7 informational P0 (including Module 0 and worked sample B4.1).

*Project plan:* `project_plan.md` updated to reference both MVP (230 quizzes) and Launch v1 (410 quizzes) targets.

**Decisions captured:**
- Vocabulary gets the structural weight of 3 modules to match the bottleneck importance.
- B2 covers informational inference explicitly; A2 covers literary inference.
- MVP and Launch v1 are distinct ship targets — MVP is what pilot users see; Launch v1 is the full P0 set within ~6 months.

**What slipped:**
- P0-4 SME review delayed; resumes after v3.1 structural sign-off.

**Open / blocked on:**
- SME validation of v3.1 structure (especially C split + B2 expansion).
- SME pedagogical review of P0-4 worked sample.
- MVP composition review (`content/STATUS.md`).

**Next action:** SME pass on v3.1 + worked sample. After approval: rebalance B4.1, P0-5 stack lock, MVP content drafting starts with Category C P0 sub-concepts.

---

---

## 2026-05-27 (cleanup) — v3.1.1: GPT review 2 stale-reference fixes

**Phase:** Phase 0.

**Trigger:** GPT review 2 (`docs/gpt_review2.md`) confirmed v3.1 direction is strong but flagged 9 documentation-consistency issues — stale v3.0/v2.x references that hadn't been swept after the structural rewrites.

**What shipped (no structural changes; doc hygiene only):**

*`docs/csv_schemas.md`:*
- Lesson schema "Columns (25)" → "Columns (26)"; self-correction paragraph removed.
- `module_id` allowed values updated from "`m0`–`m7`" to "`m0`, `a1`–`a5`, `b1`–`b6`, `c1`–`c3`."
- `sub_concept_id` example updated from "`4.3`" to "`B4.1`, `A2.3`, `C1.3`."
- `quiz_id` example updated from "`tone_4-3_q01`" to "`b4-1_q01`."
- `trap_type` example updated from "`4.3-neutral-vs-skeptical`" to "`b4.1-neutral-vs-skeptical`."
- Module 0 description changed from "8-tools preview list" to "3-MAP-categories preview, the core tools inside each category."

*`docs/why_250.md`:*
- B2 module label updated from "Evidence" to "Evidence & Inference (Informational)" with new tagline.

*`docs/curriculum_design.md`:*
- §1: "v3.0 is a structural redesign" → "v3.x is a structural redesign... v3.1 (this draft) expanded..."
- §2 + §7: "Modules A1–C1" → "Modules A1–C3."
- §9 Q2 (Should B have its own inference module?) marked RESOLVED in v3.1.
- §11: "vote on the 10 open questions" → "vote on the 9 open questions" (matches actual count after Q2 + Q10 resolved).
- Appendix B: "v3.0 (this doc) is canonical" → "v3.1 (this doc) is canonical."
- New Appendix A entry: v3.1.1 (cleanup pass).

**No structural / priority changes.** P0=40, P1=16, P2=9 unchanged. Volume tiers unchanged. MVP composition unchanged.

**Decisions captured:** none new — pure hygiene pass.

**What slipped:** nothing.

**Open / blocked on:** unchanged — SME structural validation of v3.1 (now without the docs-quality concerns).

**Next action:** SME pedagogical review of v3.1 + P0-4 worked sample (now that the supporting docs are consistent).

---

---

## 2026-05-27 (final cleanup) — v3.1.2: GPT review 3 fixes

**Phase:** Phase 0.

**Trigger:** GPT review 3 confirmed v3.1 is solid; flagged 4 remaining doc-consistency issues — three in `csv_schemas.md` and one in `curriculum_design.md` §9.

**What shipped (cleanup only):**

*`docs/csv_schemas.md`:*
- File layout examples now include `c2/01-word-precision.csv` and `c3/01-academic-verbs.csv` in both lessons and quizzes sections.
- Rules line: `c1` → `c1..c3`.
- module_id set: added `c2` and `c3`.
- Validation rule: "must equal `m0…m7`" → "must equal one of `m0`, `a1`–`a5`, `b1`–`b6`, `c1`–`c3`."

*`docs/curriculum_design.md` §9:*
- Renamed "Open in v3.0" → "Open in v3.1."
- Lifted Q2 (inference split) and Q10 (C split) out of the numbered list into a "Resolved in v3.1" subsection.
- Renumbered remaining open items 1–9 (was 1, 3, 4, 5, 7, 8, 9, 11 with strikethroughs interleaved).
- Added new Q9 — possible B3.2 (Finer Purposes) P0 → P1 demotion (GPT review 2 suggestion).
- Appendix A: v3.1.2 changelog entry.

**No structural / priority changes.** P0=40, P1=16, P2=9 unchanged.

**Decisions captured:** none new — final cleanup pass.

**What slipped:** nothing.

**Open / blocked on:** unchanged — SME validation of v3.1 structure + P0-4 worked sample.

**Next action:** SME review. Docs are now consistent and ready to be treated as locked from a documentation-quality standpoint.

---

---

## 2026-05-27 (final, final cleanup) — v3.1.3: Module 0 schema exception

**Phase:** Phase 0.

**Trigger:** GPT review 4 caught 4 remaining items:
1. csv_schemas.md headings still said "updated for v3.0."
2. curriculum_design.md §8 header still said "v2.4 → v3.0 mapping."
3. curriculum_design.md §9 had a stale Launch v1 size note that didn't account for v3.1's Vocabulary expansion and B2 inference addition.
4. **Real schema issue:** csv_schemas.md said `common_trap_1` and `example_1_*` are required, but Module 0 lessons set those fields to N/A. Either the schema was wrong or Module 0 lessons would fail validation.

**What shipped:**

*Doc-hygiene fixes (1, 2, 3):*
- `csv_schemas.md` headings: "updated for v3.0 curriculum" → "v3.x curriculum"; "Column-value rules updated for v3.0" → "(v3.x)."
- `curriculum_design.md` §8: header "v2.4 → v3.0 mapping" → "v2.4 → v3.x mapping."
- `curriculum_design.md` §9: stale Launch v1 size resolution rewritten to capture v3.0 → v3.1 evolution: 350 → 380 → 410 full P0; MVP tier = 230.

*Schema fix (4) — the real one:*
- `csv_schemas.md` column-rule table: `common_trap_1` and `example_1_*` marked "yes (except Module 0 — see below)."
- New "Module 0 exception" line in the validation rules section.
- Module 0 specifics section: added explicit "Schema exception" callout.
- Reference Zod validator updated: `common_trap_1` field type changed from `NonEmpty` to `OptionalField`; added a new `.refine()` that returns `true` for `module_id === "m0"` and otherwise requires `common_trap_1 !== "N/A"` AND `example_1_*` filled.

*Re-validation:*
- B4.1 worked sample re-validated. Has non-N/A `common_trap_1` and `example_1_*` (it's not Module 0), so it passes both the old strict rule and the new conditional rule.
- Module 0 sample (when authored) will now validate without forced workarounds.

**No structural / priority changes.** P0=40, P1=16, P2=9 unchanged.

**Decisions captured:** Module 0 is the only module exempt from the trap-led required-field rules. Future modules adding to Categories A/B/C still must have non-N/A `common_trap_1` and `example_1_*`.

**Open / blocked on:** SME structural validation + P0-4 worked sample pedagogical review remain the only outstanding items.

**Next action:** SME review. Docs are now fully consistent AND the Module 0 schema validation hole is closed.

---

---

## 2026-05-27 (final-final) — csv_schemas v1.1: real Module 0 validator bug fixed

**Phase:** Phase 0.

**Trigger:** GPT review 5 caught a real implementation bug: the Module 0 exception was documented and applied in the FIRST Zod `.refine()` (required-field check) but the SECOND refine (example-sequencing) still rejected Module 0 because it required `example_1` to be filled before checking sequencing.

**What shipped:**

*`docs/csv_schemas.md`:*
- Second `.refine()` (example sequencing) now short-circuits with `if (lesson.module_id === "m0") return true;` at the top of the callback. Module 0 lessons will no longer be rejected by the sequencing check.
- Error message updated: "Module 0 exempt" appended.
- **Schema bumped to v1.1** to reflect the materially-evolved content from the v1.0 initial lock.
- New v1.1 changelog entry documenting the Module 0 exception across both refinements + the c2/c3 enum expansion that was added between v1.0 and v1.1.

*Cross-doc references updated:*
- `content/STATUS.md`: "Schemas locked: v1.0" → "v1.1."
- `status.md`: "Schemas: LOCKED v1.0" → "LOCKED v1.1" + note about the Module 0 exception being correctly enforced.
- Historical references in earlier `progress.md` entries left as-is (they accurately log the state at the time they were written).

**No structural / priority changes.** P0=40, P1=16, P2=9 unchanged.

**Decisions captured:**
- Schema version semantic: bump minor (v1.0 → v1.1) when content changes materially without breaking the API. The original v1.0 schema is fully backward-compatible with v1.1 readers; new Module 0 lessons just won't crash the validator anymore.

**Open / blocked on:** SME validation + worked-sample pedagogical review. Same as before.

**Next action:** SME pass. The Module 0 schema hole is now fully closed: both refinements respect the exception, the docs match the code, and the schema version reflects reality.

---

---

## 2026-05-27 (reviewer pass + B4.1 rebalance) — Phase 0 close-out

**Phase:** Phase 0 — Foundations.

**Trigger:** GPT returned verdicts on all three review-packet items (`docs/answer_gpt.md`).

**What shipped:**

*Reviewer outcomes:*
- **Item 1 (v3.1 structural validation):** APPROVED with minor changes. 3-category structure, C split, A4/B4 tone split, B2 informational inference — all confirmed correct.
- **Item 2 (B4.1 worked sample pedagogy):** APPROVED with required fixes. Answer-position rebalance required + light ambiguity pass.
- **Item 3 (MVP composition):** APPROVED. Vocab-first weighting confirmed; 22 + Module 0 = 230 quizzes confirmed.

*B4.1 answer rebalance applied:*
- Old distribution: A=1, B=7, C=2, D=0.
- New distribution: **A=3, B=3, C=2, D=2.**
- Approach: rewrote 4 quizzes (Q4, Q6, Q9, Q10) by swapping choice content + corresponding per-choice feedback so the correct choice landed at a different letter. Content unchanged; only position changed.
- New `correct_choice` sequence: C, C, B, D, B, A, B, A, D, A.
- Validated: all correct-choice feedback fields still contain "Correct."; all quizzes still parse against the schema.

*Ambiguity pass result:*
- Reviewed quizzes Q3 (mayor "declared") and Q7 (company "assured") — both already pair the verb with contextual signals (temporal hedge, outcome contrast) and the per-choice feedback explicitly attributes skepticism to BOTH verb AND context. Judged pedagogically sound; no rewrite needed.
- Clean neutral examples (Q4 library closes, Q6 school board vote) preserved as unambiguous discriminators.

*Open product decisions surfaced (non-blocking, defaults in place):*
- B3.2 Finer Purposes priority — stays P0 unless product owner demotes.
- B3.1 Three Core Purposes potential MVP swap — stays out of MVP unless product owner adds.

*Tracking updates:*
- `docs/review_packet.md` — all 3 Verdict blocks filled in with GPT's approvals + applied changes.
- `status.md` — Phase 0 marked closing; P0-5 (stack lock) is the unblocked next action.

**Decisions captured:**
- Curriculum locked at v3.1.3 — no further structural changes pending.
- B4.1 locked as the canonical content template after rebalance.
- MVP composition locked at 22 sub-concepts + Module 0.

**What slipped:** nothing — this is the close-out of the review loop.

**Open / blocked on:** Two pending product decisions (B3.2 priority; B3.1 swap). Both have defaults; neither blocks engineering.

**Next action:** P0-5 stack lock. Then P0-6 (CI), P0-7 (dev docs), then Phase 1 (core lesson/quiz flow).

---

---

## 2026-05-27 (Phase 0 closed, Phase 1 P1-1 + P1-2 done)

**Phase:** Phase 0 → Phase 1.

**What shipped:**

*Phase 0 close-out (P0-5, P0-6, P0-7):*
- **Stack locked: v0 pure static.** HTML + vanilla JS ESM + Tailwind CDN + CSV fetch + localStorage. Records in `context.md`. v1 rewrite against mywordbank.net's stack planned for post-MVP validation.
- **CI scaffold:** `.github/workflows/ci.yml` runs `scripts/validate-content.py` on every push/PR. Validator covers schemas v1.1 including the Module 0 exception.
- **Dev docs:** `README.md` with stack overview, run instructions (`python3 -m http.server`), validator usage, repo layout, doc reading order.
- **Scaffold files:** `index.html` (static shell with Tailwind CDN + ESM entry), `.gitignore`.

*Phase 1 start (P1-1, P1-2):*
- **P1-1 CSV loader (`src/loader.js`).** RFC-4180 parser handling quoted multi-line cells. Validators mirror `csv_schemas.md` v1.1 exactly (column-set match, module_id allowed values, Module 0 exception for `common_trap_1` / `example_1_*`, quiz row count + question_number sequencing + correct_choice enum + difficulty enum). Returns shape-friendly Lesson and Quiz[] objects (camelCase keys, nested `choices` and `feedback` objects).
- **P1-2 mini-lesson page (`src/views/lesson.js`).** Renders title + subtitle + sub-concept ID + quick_ref callout (amber) + markdown mini-lesson (paragraphs, bullet lists, **bold**) + worked examples (boxed) + common traps. Route `#/learn/{moduleId}/{fileBasename}` wired into `main.js`.
- B4.1 worked sample renders end-to-end. Verified: home → click B4.1 link → see rendered lesson with all 4 worked examples and 3 traps.

*Smoke tests passed:*
- All 4 static file types serve 200 (HTML, JS modules, CSV)
- `validate-content.py` reports 1 lesson + 1 quiz valid

**Decisions captured:**
- Stack v0 is intentionally a throwaway — proves the content schema and UX before committing to a real framework.
- Markdown rendering kept minimal (paragraphs, bullets, bold only) — enough for the worked sample's mini_lesson content; we don't need a full markdown library for v0.
- `module_id` regex in router accepts lowercase letter + digits (`[a-z][a-z0-9]+`) — fits `m0`, `a1`..`a5`, `b1`..`b6`, `c1`..`c3`.

**What slipped:** nothing — Phase 0 closed on schedule.

**Open / blocked on:** nothing blocking. Phase 1 quiz flow (P1-3, P1-4, P1-5, P1-6) is the next active workstream.

**Next action:** Build the quiz flow:
- P1-3 MCQ component
- P1-4 Feedback panel (the teaching engine — per-choice trap-revealing feedback shown after submit)
- P1-5 Quiz flow state machine (1 of 10 → 10 of 10, MCQ + feedback per question, end-of-quiz score)
- P1-6 Score band display (9–10 Mastered / 7–8 Good / 5–6 Review / 0–4 Needs Practice)

Once those land, B4.1 is playable end-to-end and Phase 1 closes.

---

---

## 2026-05-27 (content sprint) — Category C complete + Module 0 drafted

**Phase:** Content authoring.

**What shipped:**

*7 new content packs drafted, validated, rebalanced:*
- **Module 0 (orientation)** — `m0/abstract.csv` lesson + 10 recognition quizzes. Mini-lesson ~460 words covering the 3 MAP categories + basic-vs-advanced reader table + the core tools inside each category. Recognition quizzes ("identify the tool") cover all major tools across the 3 categories.
- **C1.1 Context Meaning** — decoding unfamiliar words from text. Lesson covers 4 context signals (definition, contrast, example, cause/effect). 10 quizzes with diverse vocabulary words (deteriorated, reticent, ephemera, sediment, candor, meticulous, prolonged, sanguine, lavish).
- **C1.2 Connotation from Context** — figuring out positive/negative/neutral feeling from neighbors. Lesson covers 3 context signals + connotation-flipping. 10 quizzes pairing the same word in opposite contexts (stubborn, frugal, ambitious, unique).
- **C1.3 Figurative Word Meaning** — familiar words used non-literally (undermine, evoke, mirror, eclipse, anchor, fuel, ignite, paint). Lesson explains the borrow-from-literal shape. 10 quizzes incl. one that tests literal-vs-figurative discrimination (weathered).
- **C2.1 Word Precision** — near-synonym discrimination (suggests vs proves, reluctant vs unwilling, ambiguous vs unclear, concede vs admit, contributes vs causes, substantial vs significant, requires vs needs, implies vs states). Lesson lists the discriminations explicitly. 10 quizzes test each.
- **C3.1 Academic Verbs** — high-frequency lexicon (assert, imply, concede, scrutinize, undermine, refute, emphasize, contrast, dismiss, acknowledge, illustrate, clarify). Lesson explains what each verb signals. 10 quizzes target the highest-leverage discriminations.
- **C3.2 Tone Vocabulary** — building the lexicon to name tone (admiring, approving, skeptical, dismissive, scornful, urgent, nostalgic, reflective, wry, alarmed, bitter, hopeful, despairing, cautious). Lesson groups by category (positive / negative / emotional / reflective). 10 quizzes ask for precise tone naming, including a "negative is too broad" trap.

*Process improvements:*
- **Three CSV-quoting bugs caught and fixed.** Manual CSV authoring kept producing rows where embedded commas weren't quoted. Pivoted to Python csv.writer via one-shot generator scripts. Delete scripts after use.
- **Three answer-position rebalances** (C2.1, C3.1, C3.2). Even pre-distributing didn't fully work — authoring still drifts toward B. A second rebalance pass with a swap-table script fixed all three to A=3 B=3 C=2 D=2.

*State:*
- 8 packs / 80 quizzes / 8 mini-lessons drafted (Module 0, B4.1, all 6 Vocabulary).
- All validate against schemas v1.1.
- All have even answer distributions.
- All have trap-revealing per-choice feedback.

**Decisions captured:**
- **Authoring discipline rule:** use Python csv.writer for any multi-cell content. Manual CSV writing produces predictable quoting bugs.
- **Authoring discipline rule:** pre-distribute correct-answer letters before writing quizzes; spot-check after with a one-line counter.
- **Authoring discipline rule:** generic feedback like "this isn't right" fails the teaching engine. Every wrong-answer feedback must name the trap AND the rule.

**What slipped:** nothing — Vocabulary path finished ahead of estimate.

**Open / blocked on:** nothing blocking content authoring. SME pedagogical review is still nice-to-have but not required to continue drafting.

**Next action:** Category A — Literary Text. 9 sub-concepts: A1.1, A1.2, A2.1, A2.2, A2.3, A2.4, A4.1, A4.3, A5.1. Will use the same one-shot Python generator approach.

---

---

## 2026-05-28 (content sprint, Category A) — 9 literary packs drafted

**Phase:** Content authoring.

**What shipped:**

Nine new content packs (lessons + 10 quizzes each) for Category A — Literary Text:

- **A1.1 Theme Is a Message, Not a Topic** — topic/theme distinction; theme as full claim, not single word.
- **A1.2 Theme Is Supported by Multiple Details** — defensibility test for theme; pattern across multiple events.
- **A2.1 Inference = Clue + Reasoning** — the formula; what makes an inference vs a guess.
- **A2.2 Inference from Character Action** — actions reveal feelings; repeated, avoided, mismatched actions as clues.
- **A2.3 Inference vs Stated Fact** — distinguishing inferences from directly-stated facts; question-wording cues.
- **A2.4 Avoiding Over-Inference** — staying inside the text; outside-knowledge and extrapolation traps.
- **A4.1 Tone vs Topic in Fiction** — author's attitude vs story subject; tone words vs topic words.
- **A4.3 Mood vs Tone** — tone (author-side) vs mood (reader-side); the most-confused literary distinction.
- **A5.1 Imagery Creates Meaning** — sensory detail as meaning-making, not decoration.

*Process:*
- All 9 generated via one-shot Python script with strict csv.writer quoting.
- Pre-distributed correct-answer letters; 7 of 9 needed a rebalance pass after the initial generate.
- One file needed a single-letter tweak afterwards.
- After 2 rebalance passes: all 9 land 3-3-2-2.

*State:*
- 17 of 23 MVP packs drafted (74%).
- 170 quizzes total. All schema-valid. All 3-3-2-2. All trap-led feedback.

**Decisions captured:**
- Authoring discipline now standardized: one-shot Python generator + validate + rebalance + delete script.
- Category A uses literary passages (narrative, fiction, fragments of poetry). No reuse of nonfiction examples.
- A4.3 Mood vs Tone treated explicitly as the most-confused distinction; quizzes explicitly include divergent-tone-and-mood cases.

**What slipped:** nothing.

**Open / blocked on:** Category B (6 packs, ~60 quizzes) is the only remaining MVP content. Engineering Phase 1 quiz flow (P1-3 through P1-6) is parallel and unblocked.

**Next action:** Category B — Informational Text (6 remaining packs).

---

---

## 2026-05-28 (content sprint, Category B) — **MVP CONTENT COMPLETE**

**Phase:** Content authoring.

**What shipped:**

Six new Category B packs (lessons + 10 quizzes each):

- **B1.1 Topic vs Main Idea (Informational)** — single-sentence test for main idea vs topic.
- **B1.2 Main Idea vs Supporting Detail** — coverage test; main idea covers the whole, detail covers a piece.
- **B2.1 Evidence Must Be Traceable** — traceability discipline; quote or locate.
- **B2.3 Proof vs Related Information** — THE #1 advanced-reader trap; related ≠ proven.
- **B2.5 Inference from Nonfiction Cues** — distinct from literary inference; uses data, structure, word choice.
- **B5.3 Paragraph Function** — each paragraph has a job; name it.

Plus fixes:
- B5.3 quick_ref shortened from 216 → 171 chars (under the 200 limit).
- 5 of 6 distributions rebalanced to 3-3-2-2.
- One alignment bug fixed in b1/01-topic-vs-main-idea (Q9 had correct content at choice_a but `correct_choice="B"`; swapped choice contents to restore alignment).

**Final MVP state — 23 of 23 packs complete.**

| Category | Packs | Quizzes |
|---|---:|---:|
| Module 0 | 1 | 10 |
| Category A (Literary) | 9 | 90 |
| Category B (Informational) | 7 | 70 |
| Category C (Vocabulary) | 6 | 60 |
| **MVP TOTAL** | **23** | **230** |

Every pack: schema-valid, 3-3-2-2 distribution, trap-led per-choice feedback, genre-appropriate. Content is architect-drafted — pedagogical SME review still open across all 23 packs.

**Decisions captured:**
- Authoring discipline (Python generator + rebalance + delete) successfully shipped 23 packs across 4 batches in 2 days with zero CSV-quoting failures.
- Final MVP corpus is internally consistent and ready for engineering Phase 1.

**What slipped:** nothing. MVP content done.

**Open / blocked on:**
- Engineering Phase 1: quiz flow (P1-3, P1-4, P1-5, P1-6). The only thing between the corpus and a playable v0.
- Pedagogical SME review across all 23 packs (nice-to-have but not blocking).

**Next action:** build the quiz flow (P1-3 through P1-6). After that, v0 is playable end-to-end and an SME can actually USE the content for review instead of just reading CSVs.

---

---

## 2026-05-28 (engineering sprint) — Phase 1 complete, v0 is playable

**Phase:** Phase 1 — closed.

**What shipped:**

*P1-3 MCQ component:* Inline in `src/views/quiz.js`. Four choices as buttons. State machine: idle → answered (selection highlighted) → submitted (correct/incorrect coloring, buttons disabled). Color-coded: selected = slate; submitted-correct = emerald; submitted-selected-wrong = rose; submitted-other = slate-50.

*P1-4 Feedback panel:* Renders after submit inside `src/views/quiz.js`. Shows "Why [letter] is right/wrong" using the per-choice feedback from the CSV. When the student gets it wrong, also shows "Why [correct] is right" with the correct choice's feedback. This is the teaching engine made visible.

*P1-5 Quiz flow state machine:* `renderQuizPage(target, moduleId, fileBasename)` in `src/views/quiz.js`. In-memory session: `{answers: ["A"|"B"|...|null], submitted: [bool], currentIndex: number}`. Progress bar (`(currentIndex+1)/10`). Submit and Next buttons. Route `#/quiz/{module}/{slug}` added to `src/main.js`. Refresh resets session — Phase 3 will add localStorage persistence.

*P1-6 Score + status band:* `statusBand(score)` pure function in `src/views/quiz.js`. Bands per curriculum doc: 9-10 Mastered (emerald), 7-8 Good (blue), 5-6 Review (amber), 0-4 Needs Practice (rose). Each band has its own blurb explaining what the student should do next. **Module 0 special-cased:** end screen shows "Orientation Complete" with explicit "intentionally not scored" message — per curriculum design.

*Routing + home page:*
- `src/main.js` updated with `#/quiz/{module}/{slug}` route.
- Home page expanded from "1 sub-concept link" to **all 23 sub-concepts grouped by category** (Orientation / A · Literary / B · Informational / C · Vocabulary). Hardcoded `CATALOG` array; a content manifest could derive this in Phase 5.

*Lesson page integration:*
- `src/views/lesson.js` "Start 10 quizzes" button — formerly disabled placeholder — now links to `#/quiz/{module}/{basename}`.

*Smoke tests:*
- All static file types serve 200 (HTML, JS modules, all CSV variants tested).
- File structure unchanged from Phase 0 layout. No new dependencies (still pure HTML + vanilla JS + Tailwind via CDN).

**Decisions captured:**
- In-memory quiz session for v0; localStorage persistence is Phase 3 work.
- Module 0 end screen explicitly skips the score display ("not scored") — UI respects the curriculum design rule.
- `CATALOG` is hardcoded in main.js for v0. A content manifest (`content/manifest.json` or similar) is appropriate for Phase 5 once we want auto-discovery.
- Per-choice feedback display: shows the picked choice's feedback always; additionally shows the correct choice's feedback only when student got it wrong. Reduces visual clutter when correct.

**What slipped:** nothing. Phase 1 closed on schedule.

**Open / blocked on:**
- Pedagogical SME review of all 23 content packs.
- User in-browser test of the v0 flow.
- Phase 3 progress persistence (localStorage).

**Next action:** owner tests v0 in a browser. After that, Phase 3 (progress tracking) or Phase 5 (Quick Reference page) or pedagogical review are all unblocked.

---

---

## 2026-05-28 (engineering sprint cont.) — Phase 3 complete: progress persists

**Phase:** Phase 3 — closed.

**What shipped:**

*P3-1 localStorage schema:* New file `src/progress.js`. Root key `break250.progress.v1`. Schema: `{ version: 1, subConcepts: Record<key, {lastScore, bestScore, attempts, lastAttemptedAt}> }`. Keys are `{module}/{basename}` strings.

*P3-2 Progress write/read:* `recordAttempt()` called automatically inside `renderEndScreen()` of `src/views/quiz.js` when a student finishes all 10 questions. `getProgress()` reads on the end screen so retakes show best + attempt count. Storage failures (private mode, quota full) fail silently — v0 doesn't surface them.

*P3-3 Status band per sub-concept:* `statusFromScore()` and `statusBadge()` in `src/progress.js`. Bands match the curriculum doc:
- 9–10: Mastered (emerald)
- 7–8: Good (blue)
- 5–6: Review (amber)
- 0–4: Needs Practice (rose)
- Not attempted: Not Started (slate)
- Module 0 special: "Orientation Complete" if attempted (never scored)

*P3-4 Module-level roll-up:* `renderRollup()` in `src/main.js` aggregates sub-concept statuses for each category and shows a one-line summary: "5/9 attempted · 2 Mastered · 1 Good · 2 Review". Each category section in the home page gets its own roll-up.

*P3-5 Dashboard:*
- Home page enhanced: each sub-concept link now displays a colored status badge inline (right-aligned).
- Per-category roll-up line below each category heading.
- "Reset progress" button at the bottom of home with a confirm dialog.
- End-of-quiz screen now shows "Best: X/10 · Attempts: N" when the student retakes a sub-concept.

**Smoke tests passed:**
- All static files serve 200 (HTML, 5 JS modules, sample CSVs).
- `progress.js` exports the expected 5 functions: `recordAttempt`, `getProgress`, `resetAll`, `statusFromScore`, `statusBadge`.

**Decisions captured:**
- Storage version field (`version: 1`) included from the start so future schema changes can migrate.
- Module 0 status is "Orientation Complete" (emerald, no number) — UI respects curriculum design rule that Module 0 is never scored.
- Reset confirms via browser `confirm()` for v0; a custom modal can come in Phase 6 polish.
- No sync, no accounts — pure browser-local progress. Aligns with "no PII, no auth" v0 scope.
- localStorage failures fail silently. Phase 6 hardening could surface them.

**What slipped:** nothing.

**Open / blocked on:**
- Pedagogical SME review of all 23 content packs (long-standing).
- Phase 5 Quick Reference page (placeholder route exists).
- Phase 6 polish (mobile, a11y, perf, error monitoring).
- Stack v1 rewrite — held until mywordbank.net pattern is known.

**Next action:** owner tests the persisted-progress flow in a browser. After that, Phase 5 (Quick Reference) is the most useful next item — it pulls together all the `quick_ref` columns into the pre-read checklist.

---

---

## 2026-05-28 (later) — Phase 5 complete + C1.2 content bug fix

**Phase:** Phase 5 — closed.

**What shipped:**

*P5-1 Quick Reference page (`src/views/reference.js`):*
- Loads all 23 lessons in parallel (Promise.all).
- Groups by category (Orientation / A · Literary / B · Informational / C · Vocabulary).
- Each line is a clickable link: sub-concept ID + title + the `quick_ref` text. Click opens the full mini-lesson.
- Header explains the use: "read top to bottom in under a minute."
- Footer has a "Print this page" button (`window.print()`).
- Error-tolerant: if one lesson fails to load, the rest still render with a per-line error message.

*P5-2 Always-on nav link:* The top nav in `index.html` already includes "Quick Reference" — it's been pointing at the `/reference` route since Phase 0. Now that route is functional.

*Router wiring (`src/main.js`):* `renderReference()` now delegates to `renderReferencePage(app, CATALOG)`. Catalog is passed so reference can reuse the same metadata as the home page.

*Content-bug fix:* C1.2 lesson had a subtitle with unquoted commas: *"Figuring out whether a word's feeling is positive, negative, or neutral..."*. The unquoted commas split the row into extra columns — making the CSV parser read `quick_ref` as `" negative"` and `mini_lesson` as `" or neutral when the word is new to you."`. Both broken. Regenerated the file via `csv.writer(quoting=QUOTE_MINIMAL)` and re-validated. Health check across all 23 lessons confirms only C1.2 had this bug.

*Validator hardened:* Added sanity checks in `scripts/validate-content.py`:
- `quick_ref` must be at least 30 chars (catches truncated cells from column shifts).
- `quick_ref` must not start with whitespace or punctuation (catches mid-cell starts).
- `mini_lesson` must be at least 100 chars (catches truncated bodies).

These are content health checks, not strict schema rules — they exist to surface bugs the schema alone can't catch.

*Smoke tests passed:*
- All static files serve 200 (home, all 6 JS modules, sample CSVs).
- `validate-content.py` reports all 23 lessons + 23 quizzes valid against the hardened schema.

**Decisions captured:**
- Quick Reference loads all lessons in parallel and tolerates per-file errors — Promise.all with try/catch wrapping. The page renders even if one CSV is broken.
- Print button included because the reference is genuinely intended as a one-page checklist a student might print.
- Validator now catches the column-shift class of bugs that the original validator missed. Future content authoring should generate via csv.writer (the established discipline), but the validator also fails loudly if a manually-edited file slips through.

**What slipped:** nothing.

**Open / blocked on:**
- Pedagogical SME review (long-standing).
- Phase 6 polish (mobile, a11y, perf, error monitoring).

**Next action:** Phase 6 hardening, OR pause for SME pedagogical review, OR pause for in-browser dogfooding. All non-blocking.

---

---

## 2026-05-28 (later) — Phase 6 polish round: keyboard + a11y + privacy

**Phase:** Phase 6 — partial.

**What shipped:**

*Keyboard navigation in quiz (`src/views/quiz.js`):*
- Global `keydown` handler attached when each question renders.
- `1` / `2` / `3` / `4` keys select answer choices A/B/C/D.
- `Enter` key submits when a choice is selected, or advances when feedback is showing.
- Handler is removed on end-screen render to prevent stale shortcuts.
- Visible "Keyboard: 1-4 to select · Enter to submit/advance" hint at the bottom of each question.
- All buttons get `focus:outline-none focus:ring-2 focus:ring-slate-400` for keyboard visibility.

*A11y attributes added (no scan yet, but coverage):*
- `aria-live="polite"` on the post-submit feedback panel so screen readers announce per-choice feedback.
- `role="status"` on the feedback panel, the score card, and the Module 0 completion message.
- `role="radiogroup"` with `aria-label="Answer choices"` on the choice cluster.
- `aria-pressed` on each choice button before submit (reflects selection state).
- `role="progressbar"` with `aria-valuenow/min/max` on the question progress bar.
- Programmatic focus moves to the question's prompt block on advance (`tabindex="-1"` + `.focus()`); skipped on initial mount.
- Skip-to-content link in the page header (visible only when focused).

*Privacy disclosure in footer (`index.html`):*
- Explicit statement: localStorage stores quiz scores + attempts only; no data leaves the device; no tracking; no third-party scripts beyond Tailwind CDN; Reset Progress wipes everything.
- Footer is visible on every page.

*Print stylesheet (`index.html` inline `<style>`):*
- `@media print` hides header, footer, and the print button itself.
- Links print without underlines/colors so the Quick Reference prints cleanly as a 1-page checklist.

*Smoke tests passed:*
- All file types serve 200.
- Homepage HTML contains both "Privacy:" disclosure text and "Skip to content" link.
- Validator still reports all 23 lessons + 23 quizzes valid.

**Decisions captured:**
- Keyboard shortcuts implemented as document-level keydown handler scoped to the quiz view; cleaned up on end-screen render.
- Privacy disclosure is in-app footer text, not a separate modal. For v0 this is sufficient; pilot deployment may want a more formal consent flow per the curriculum's privacy notes.
- A11y attributes added defensively; full axe-core/Playwright scan deferred until a browser-test environment exists.

**What slipped:** nothing.

**Open / blocked on:**
- Pedagogical SME review (long-standing).
- Browser-test environment for full a11y/perf scans.
- Pilot consent doc (separate from in-app disclosure).
- Stack v1 rewrite.

**Next action:** v0 is now polished enough for pilot dogfooding. Suggested: pause for actual in-browser testing + SME content review before further engineering.

---

---

## 2026-05-28 (Reading Lab v1) — public-domain texts with color-coded markup

**Phase:** Reading Lab v1 — shipped (per spec at `docs/superpowers/specs/2026-05-28-reading-lab-design.md`).

**Trigger:** Brainstorming pass — user asked about adding free novels/articles (e.g., Shakespeare) and a marked-up HTML pattern that demonstrates the reader-as-marker habit. Decomposed into Path B first → Path D later. Path B approved.

**What shipped:**

*Spec doc (`docs/superpowers/specs/2026-05-28-reading-lab-design.md`):*
- Records the design: 6 starter texts, 5-color system, JSON format, UI pattern, file layout, scope, path to v2.

*Six public-domain text files in `content/lab/`:*
- 001 Sonnet 18 — Shakespeare 1609 — Poetry — 7 annotations, 4 prompts
- 002 Gettysburg Address — Lincoln 1863 — Informational — 8 annotations, 5 prompts
- 003 "I went to the woods" (Walden) — Thoreau 1854 — Opinion essay — 8 annotations, 4 prompts
- 004 Huck Finn opening — Twain 1884 — Literary — 7 annotations, 4 prompts
- 005 Gift of the Magi opening — O. Henry 1905 — Literary — 8 annotations, 4 prompts
- 006 Boy Who Cried Wolf — Aesop 1867 — Fable — 7 annotations, 4 prompts

All clearly US public-domain (pre-1929). 45 annotations + 25 prompts total. Each annotation has character offsets (start, end), a category (tone/evidence/theme/inference/structure), and a teaching note.

*Loader extension (`src/loader.js`):*
- New `loadLabText(basename)` function that fetches `content/lab/{basename}.json`, validates structure + annotation offsets + category enum, shapes to camelCase for UI.
- New runtime validators: `validateLabText()` checks required fields, passage length, annotation offsets within passage, category enum, note length.

*New view (`src/views/lab.js`):*
- Renders a text detail page with:
  - Sticky color legend (5 colored dots + labels) at top
  - **Show markup / Hide markup** toggle (defaults to ON)
  - Passage rendered with `whitespace: pre-wrap`; annotated ranges become colored buttons
  - Click any annotated range → annotation note appears in a panel below
  - Discussion prompts at the bottom
  - Source link (opens external in new tab)
- `buildSegments()` helper splits the passage at every annotation boundary; handles overlapping annotations by stacking colors at the first match.
- Color classes: amber (tone), emerald (evidence), sky (theme), violet (inference), orange (structure).
- A11y: focusable buttons for annotation ranges, `aria-label` naming the categories, `aria-live` on the note panel.

*Router + home page (`src/main.js`):*
- New `#/lab/{basename}` route.
- New `LAB_CATALOG` constant listing the 6 texts with metadata.
- New `renderLabSection()` function rendering the lab catalog as cards.
- Reading Lab section added to the home page after Category C.

*Validator extension (`scripts/validate-content.py`):*
- New `validate_lab(path)` function called for every JSON in `content/lab/`.
- Checks: JSON parses, required fields present, category in {Literary, Informational, Poetry, Fable}, passage ≥ 50 chars, annotations is list, each annotation has int start/end within passage bounds, category in {tone, evidence, theme, inference, structure}, note ≥ 10 chars, discussion_prompts is non-empty list.
- Summary line now reads "Validated N lesson · M quiz · L lab file(s)."

*Smoke tests:*
- All static files serve 200.
- All 6 JSON files parse cleanly with valid annotation offsets.
- Validator reports all 52 content files valid.

**Decisions captured:**
- JSON (not CSV) chosen for lab texts. Passages are bigger than CSV easily handles; annotations are nested structures. CSV stays canonical for lessons/quizzes.
- 5 colors, not 9. Matches the visual-clarity sweet spot. Figurative Language doesn't get its own color in v1 (overlaps Tone/Theme).
- Toggle defaults to "markup ON" so users see the demonstration first. Toggle off to read clean.
- Annotation offsets are character indices — hand-counted in v1. Any future passage edits require recomputing offsets. Flagged as a known limitation.
- Source URLs link to Project Gutenberg / Library of Congress for the full original text.

**What slipped:** nothing.

**Open / blocked on:**
- SME pedagogical review of the 6 lab annotations (the markup IS the teaching, so this is especially valuable).
- Path D (embed annotated micro-passages in existing sub-concept lessons) — deferred until v1 is dogfooded.

**Next action:** browser dogfooding of Reading Lab + SME review of the annotations.

---

## Template for future entries

```
## YYYY-MM-DD — [phase] [component IDs touched]

**Phase:** Phase N — Name

**What shipped:**
- P{N}-X — short summary, link to PR

**What slipped:**
- P{N}-Y — reason, new target

**Decisions:**
- ...

**Tests:**
- new tests added: ...
- coverage delta: ...

**Review findings:** (link to feedback.md sections)

**Next action:** (link to status.md)
```
