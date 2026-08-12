# feedback.md — Code & design review feedback

> Findings from architect reviews and code reviewer agents. Severity follows global standard: CRITICAL (block) · HIGH (warn) · MEDIUM (info) · LOW (note).

---

## 2026-05-26 — Architect pass on `design1.md`

The design doc is thorough but has gaps that need decisions before code lands. Findings below are on the **design**, not on code (none exists yet).

### CRITICAL

**C-1 — Wrong-answer-type taxonomy is not locked.**
Design §7.6 lists 11 mistake categories. Design §9.2 example uses `wrong_answer_type` values like `"tempting_because_factual_content"`, `"opposite_tone"`, `"unsupported"` — these do **not** map cleanly to the 11 categories. The product differentiator (wrong-answer diagnosis) depends on a stable taxonomy.

*Action:* before P1-2 (question schema migration), produce a canonical enum that reconciles §7.6 and §9.2. Enforce as a DB enum + Zod enum. Map ambiguous historical labels in a `wrong_answer_type_alias` table if needed.

### HIGH

**H-1 — Evidence selection model is underspecified.**
Design §9.1 shows `"required_evidence": ["claims", "supposedly"]` (literal strings) and elsewhere `"valid_evidence": ["p3_s2"]` (segment IDs). Two different shapes. Need to decide: do we score on text spans (offsets) or segment IDs (paragraph/sentence)? Probably both — paragraph/sentence ID for coarse, span offsets for fine — but P1-2 must define.

*Action:* author an "Evidence model" ADR in `docs/` before Phase 1.

**H-2 — Explanation scoring path is not honest.**
Design §10.3 ships a 0–4 rubric. §15.1 says "AI scoring can assist later." §10.4 then weighs explanation 20% in mastery. If MVP has no scorer, mastery math is fragile and recommendations will skew. Either drop explanation from MVP mastery (set weight to 0) or commit to manual scoring at pilot scale.

*Action:* recommend dropping explanation from the MVP mastery formula and re-weighting: `0.65·accuracy + 0.35·evidence`. Capture explanation text for content quality review, but don't score it in MVP. Document this in `context.md` invariants once confirmed.

**H-3 — "Highlight exact text" question type has no scoring spec.**
Design §6.6 lists "highlight exact text" as a question type. No rubric for partial-overlap, multiple-span, or fuzzy-match. Defer or specify.

*Action:* defer to post-MVP unless we want it. If we want it, write the spec in the Evidence ADR.

### MEDIUM

**M-1 — Mobile two-pass close reading is hard.**
Design §7.4 hand-waves "passage first, question panel below, sticky 'Show Passage' button." But the second-read flow requires the student to actively reread *while* looking at a focused question (e.g., "highlight tone words"). On a phone this is hard. Prototype mobile flow in Phase 2, not Phase 6.

**M-2 — Parent linkage and consent are vague.**
§3.2 mentions parents/teachers as secondary users. §22.2 lists parent controls but doesn't say how a parent gets linked to a student account. For minors, this likely needs parental consent before the student plays at all. Legal-flavored question; raise early.

**M-3 — Diagnostic question count math doesn't match.**
§7.2 says "20–30 questions" then lists `2 × 10 = 20`. Pick one. Suggest exactly 20 for MVP — 2/skill across the 10 listed groups in §7.2 (note: this list shows 10 categories, but module list §5.2 has 12 modules — Word Choice and one other are missing from the diagnostic mix; reconcile).

**M-4 — "Streak" gamification is mentioned but defined only as a UI element.**
Design §17.3 says light gamification (streaks, badges). But streaks reward speed/consistency, which conflicts with §17.3's own line "reward precision, not speed." Suggest dropping daily streak, keeping mastery-badge progression only.

### LOW

**L-1 — Tagline / branding is a list of options, not a choice.** Pick before Phase 5 admin UI shows brand chrome.

**L-2 — No mention of dark mode.** Per `~/.claude/rules/web/coding-style.md` we should not default to dark mode just because — but readers may want a night mode for long sessions. Decide explicitly, don't drift in.

**L-3 — "8–30 lines" poetry range is wide.** Tight upper bound (~20) keeps the lesson scope small.

---

---

## 2026-05-26 — Direction pivot supersedes earlier findings

Several earlier findings (C-1, H-1, H-2, M-2) are partially or fully **moot** under the mywordbank.net pattern simplification. Rather than delete them, mark status:

- **C-1 (wrong-answer-type taxonomy):** Still relevant, but simpler scope. Now lives as the `trap_type` column on quizzes CSV. Taxonomy is a per-quiz free tag pointing at a sub-concept (e.g., `5.3-neutral-vs-skeptical`). DB enum no longer applies (no DB). **Status: Active, simplified.**
- **H-1 (evidence model — spans vs segments):** **Moot for v1.** No evidence-selection UI in the mywordbank-pattern MVP. Evidence questions ask the student to pick which quoted line proves the answer — still MCQ. Revisit if we add highlighting later.
- **H-2 (explanation scoring):** **Moot for v1.** No short-answer explanation field in the mywordbank pattern. Score is `correct count / 10`. Mastery formula collapses to score-only banded thresholds. Revisit if explanation collection is added.
- **H-3 (highlight exact text):** **Moot for v1.** Dropped per "no complex interactions" rule.
- **M-1 (mobile two-pass close reading):** **Moot for v1.** No two-pass flow in the simplified design. Mobile is still important but for a much simpler page (mini-lesson + 10-quiz flow).
- **M-2 (parent linkage / consent):** **Still active.** Even with no auth in v1, if we collect any progress (localStorage), we need an age gate and a "for under-13 users get parent OK" disclaimer. Revisit before any deployment.
- **M-3 (diagnostic question count math):** **Moot for v1.** No diagnostic in the simplified design.
- **M-4 (streak gamification):** **Still active.** Reaffirmed by the new design (do not use speed-based rewards).
- **L-1, L-2, L-3:** Carry forward as-is.

### New finding from curriculum design pass

**H-4 — Mini-lesson granularity. RESOLVED 2026-05-26.**
Resolution: **one mini-lesson + 10 quizzes per sub-concept** for Modules 1–7. **Module 0 is a deliberate exception** — one orientation lesson covering all 8 tools + 10 recognition quizzes. Recorded in curriculum doc v2 §3.7, §3.8, §5.0.

Consequences:
- File structure nested: `content/lessons/{module}/{NN-slug}.csv` + `content/quizzes/{module}/{NN-slug}.csv`.
- Volume v2: ~59 sub-concepts + Module 0 = ~600 quizzes for v1.
- Progress tracking is per sub-concept; module-level mastery is a roll-up.
- Module 0 is scored separately and labeled "Orientation" in UI (not "Mastered") — see new finding M-5.
- Lesson CSV schema can be locked once reviewers approve curriculum v2.

### Findings from curriculum doc v2 pass

**M-5 (new) — Module 0 false-confidence risk.**
Module 0 quizzes are recognition-format ("identify the tool") and easy by design. 10/10 means a student can name the tools, not use them. The UI must label Module 0 as **Orientation** rather than **Mastered**, and the dashboard should visually separate Module 0 status from Modules 1–7 mastery rolls.

*Action:* called out in §5.0 UI watch-out and §9 Q11. UI design must respect this when we get there.

**M-6 (new) — Module 6 grouping deviates from common standards.**
Pairing "Compare Viewpoints" with Argument (rather than its own future Paired-Text module) is a pragmatic compromise. Defensible but unusual. Flagged for ELA reviewers via §9 Q12.

**M-7 — Content authoring volume. PARTIALLY RESOLVED in v2.1.**
Resolution: v2.1 introduced P0/P1/P2 priority labels. Launch v1 is now scoped to **P0 only ≈ 310 quizzes** (down from v2's 600). Architecture must still support incremental release; the master curriculum (~610 quizzes) remains the long-term ceiling.

*Action:* `project_plan.md` rewrite targets the 310-quiz launch, with P1 and P2 as post-launch expansion phases.

### Findings from curriculum doc v2.1 (reviewer round 2)

**M-5 — Module 0 false-confidence. RESOLVED in v2.1.**
Resolution: Module 0 is now **not scored** at all. UI shows "Orientation Complete" / "Not Started" only. Recorded in §5.0 scoring section and §3.8 design principle.

**L-4 (new, low) — 2.1 Evidence wording was too strict.**
v2 said "must be quoted, not paraphrased." Some real-test evidence questions only require *pointing to* the text, not literal quotation. Softened in v2.1 to "Evidence Must Be Traceable to the Text — you can explain in your own words, but you must be able to point to the exact words in the passage." Recorded in §5.2.

**L-5 (new, low) — §5.4 Tone language was overclaiming.**
v2 said "Tone is the single highest-leverage concept for the 240→250 jump." That's a strong empirical claim without data behind it. Softened in v2.1 to "Tone is likely one of the highest-leverage concepts for advanced reading plateaus."

**M-8 (new) — Module 7 was front-loaded with low-leverage basics.**
v2 led Module 7 with Simile vs Metaphor — a concept advanced readers mostly already know. Reordered in v2.1 so the high-leverage interpretive moves (Imagery, Symbolism, Speaker not Poet, Line Break) come first. Simile vs Metaphor demoted to P1.

**M-9 (new) — 6.5 "Basic Logical Moves" risked overshooting grade band.**
v2's Module 6.5 listed appeal-to-emotion, bandwagon, false binary — fallacy vocabulary that's borderline for Grade 5–6. Renamed in v2.1 to **"Emotional Appeal vs Logical Evidence"** with a tighter trap framing.

### Findings from curriculum doc v2.2 (GPT reviewer pass)

**C-2 (new, CRITICAL) — Rollup arithmetic off by one. RESOLVED in v2.2.**
v2.1 §4.1 said full v1 = 49 sub-concepts / 500 quizzes and master = 60 / 610. Actual was 48 / 490 and 59 / 600. Fixed.

**M-11 (new) — Module 7 narrative contradicted its own table.**
v2.1 §5.7 narrative said "Simile vs Metaphor is not P0" while the table marked it P0. **RESOLVED in v2.2:** demoted 7.3 to P1 and promoted 7.9 Tone Shift in Poetry to P0 (better pedagogical fit at this level). Module 7 P0 count stays at 5.

**M-12 (new) — Module 0 examples mixed tools.**
v2.1 Module 0 quiz #7 ("→ Poetry / Structure") and quiz #10 ("→ Evidence + Inference") tested multiple tools. Bad pedagogy for an orientation module that should teach **single-tool recognition first**. **RESOLVED in v2.2:** both rewritten as single-tool examples.

**L-6 (new, low) — "Reading-Analysis Abstract" is an internal-flavored name.**
Fine for architecture docs but unfriendly in product UI. Recorded as §9 Q13. Possible student-facing labels: "The 8 Reading Tools," "Reading Analysis Map," "Advanced Reading Orientation." Decision deferred to the UI/copy phase.

**M-13 (new) — Advanced-grade sub-concepts need content-authoring care.**
GPT flagged these as appropriate for Grade 7–8 but possibly tough for Grade 5 even with advanced readers:
- 1.9 Universal vs Text-Specific Theme
- 3.7 Reliable vs Unreliable Narrator
- 6.2 Assumption
- 6.5 Emotional Appeal vs Logical Evidence
- 7.9 Tone Shift in Poetry

*Action:* the eventual content authoring style guide must give these sub-concepts simpler passages, more familiar topics, and more careful example design. This is not a curriculum decision; it's a content-quality discipline applied during writing.

**M-14 (new) — Reviewer disagreement: Mood vs Tone (4.6) priority.**
Round-2 reviewer placed it at P0 ("very high-value"). GPT named it as an MVP demotion candidate ("useful but less essential than evidence, inference, central idea, tone, word choice, paragraph function"). Logged as §9 Q14. Architect recommendation pending more data — neither reviewer is obviously wrong.

---

**M-10 — Content release ladder needed.**
Per reviewer's strong recommendation: even within Launch v1 (P0), 310 quizzes is meaningful work. The app should be launchable with Module 0 + a single category's P0 sub-concepts; further P0 sub-concepts ship incrementally.

*Action:* `project_plan.md` rewrite must include this ladder explicitly. Suggested first ship: Module 0 + Module 1 P0 (3 sub-concepts) + Module 2 P0 (5 sub-concepts) = 90 quizzes — students can use the app from day one.

---

## How to use this file

- New review findings are appended with a date header.
- Each finding gets an ID (`C-N`, `H-N`, `M-N`, `L-N`) and stays referenceable from `progress.md` and code comments.
- Resolved findings are not deleted — they're marked **Resolved** with a date and a link to the commit/PR that closed them.
