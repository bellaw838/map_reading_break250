# GPT Review 2 — v3.1 Curriculum and Docs

**Reviewed docs:**

- `docs/curriculum_design.md`
- `docs/why_250.md`
- `docs/csv_schemas.md`

**Review date:** 2026-05-27  
**Reviewer:** GPT

---

## Overall Assessment

The v3.1 curriculum direction is strong.

The latest update addresses the major concerns from the previous review:

- Vocabulary is no longer underweighted. It is now its own 3-module category: C1, C2, C3.
- Informational inference is now explicit in B2 instead of being assumed under Evidence.
- The curriculum now includes an MVP tier: 22 sub-concepts + Module 0 = 230 quizzes.
- The structure now maps cleanly to the three MAP Reading sub-areas: Literary Text, Informational Text, Vocabulary.

The main remaining issues are not strategic. They are documentation consistency problems, especially in `csv_schemas.md`.

Recommendation: approve the v3.1 curriculum direction, but clean up the stale references before treating the docs as locked.

---

## What Improved

### 1. Vocabulary Is Properly Elevated

The prior v3.0 design gave Vocabulary only one module and 40 launch quizzes. That was too light given the diagnosis that vocabulary nuance is likely the fastest path from 246 to 250+.

v3.1 fixes this by splitting Vocabulary into:

| Module | Focus |
|---|---|
| C1. Context Meaning | Decoding unfamiliar words from surrounding text |
| C2. Word Nuance & Precision | Distinguishing near-synonyms and certainty levels |
| C3. Academic & Tone Lexicon | Academic verbs and tone words |

This better matches the actual MAP bottleneck:

> vocabulary nuance + literary inference + advanced passage analysis

### 2. Informational Inference Is Now Explicit

The earlier v3.0 design put inference mainly in Category A and assumed informational inference would be covered by Evidence. v3.1 fixes that by expanding B2 into:

> B2. Evidence & Inference (Informational)

The added sub-concepts are useful:

- B2.5 Inference from Nonfiction Cues
- B2.6 Avoiding Over-Conclusion

This is the right call. MAP informational questions often ask students to draw conclusions from facts, claims, data, and paragraph-level cues. That is not identical to literary inference.

### 3. MVP Tier Is Now Realistic

The full P0 launch is now 410 quizzes, which is too large for a first content-quality pass.

The new MVP tier is much better:

| Tier | Scope | Quizzes |
|---|---:|---:|
| MVP | 22 sub-concepts + Module 0 | 230 |
| Launch v1 | 40 sub-concepts + Module 0 | 410 |
| Full v1 | 56 sub-concepts + Module 0 | 570 |
| Master curriculum | 65 sub-concepts + Module 0 | 660 |

The MVP composition is sensible because it includes:

- all 6 Vocabulary P0s,
- 9 Literary P0s,
- 7 Informational P0s.

That gives the first release enough coverage across all three MAP categories while still prioritizing the likely bottleneck.

---

## Remaining Issues To Fix

### 1. `csv_schemas.md` Is Still Internally Inconsistent

The schema doc partially reflects v3.1, but several old references remain.

Examples:

- The file layout rules say valid module folders are `m0`, `a1`..`a5`, `b1`..`b6`, `c1`, but v3.1 also has `c2` and `c3`.
- The lesson schema table still says `module_id` is `m0`-`m7`.
- The `sub_concept_id` example still uses `4.3`.
- The validation rules still say `module_id` must equal `m0`...`m7`.
- The quiz schema still uses examples like `tone_4-3_q01` and `4.3-neutral-vs-skeptical`.

These should be updated to the v3.1 ID system:

- `module_id`: `m0`, `a1`-`a5`, `b1`-`b6`, `c1`-`c3`
- `sub_concept_id`: `A1.1`, `B4.1`, `C2.1`, etc.
- `trap_type`: e.g. `b4.1-neutral-vs-skeptical`
- `quiz_id`: e.g. `b4-1_q03`

### 2. `csv_schemas.md` Should Not Contain a Self-Correction

The lesson schema section says:

> Columns (25)

Then later corrects itself to 26 columns.

Because this is a locked schema doc, it should be clean and authoritative:

- Change the heading to `Columns (26)`.
- Fix the `example_5_*` row to use columns `24-26`.
- Remove the correction paragraph entirely.

### 3. Module 0 Schema Notes Still Mention the Old 8-Tools Preview

`csv_schemas.md` still says Module 0 contains the "8-tools preview list."

That is stale. In v3.1, Module 0 orients around:

- 3 MAP categories,
- the core tools inside each category,
- completion-only status.

Update this wording to match `curriculum_design.md`.

### 4. `why_250.md` Has One Stale Module Label

The public-facing manifesto is mostly synced, but the module map still labels B2 as:

> B2. Evidence

It should match the v3.1 curriculum:

> B2. Evidence & Inference (Informational)

Suggested wording:

> The exact words that prove an answer, and the conclusions nonfiction facts support.

### 5. `curriculum_design.md` Has Stale v3.0 Language

The curriculum itself is good, but the document still has some v3.0 wording inside a v3.1 draft.

Fix these:

- Section 1 says "v3.0 is a structural redesign." It should say v3.1 builds on v3.0 by expanding Vocabulary, adding informational inference, and adding the MVP tier.
- Section 2 says user experience applies to "Modules A1-C1." It should say "Modules A1-C3."
- Section 7 says "Modules A1-C1." It should also say "A1-C3."
- Section 9 still asks whether B should have informational inference; this is resolved in v3.1.
- Section 9 still asks whether C should split into multiple modules; this is resolved in v3.1.
- Section 11 asks reviewers to vote on 10 open questions, but the list currently has 11.
- Appendix B says v3.0 is canonical. It should say v3.1 is canonical.

---

## Curriculum Judgment

The v3.1 curriculum is now much closer to the real student need.

The strongest design choices are:

- Splitting Vocabulary into 3 modules instead of leaving it as a small add-on.
- Keeping Literary and Informational Text separate because MAP reports them separately and the signals differ.
- Splitting tone into fiction and nonfiction contexts.
- Adding informational inference explicitly.
- Using an MVP tier so content quality is protected.

The main launch risk is still content volume. A 410-quiz full P0 launch is large. The MVP tier should be treated as the actual first ship target unless there is unusually strong content-authoring capacity.

---

## Possible Priority Adjustment

If the MVP needs to get even tighter, preserve all Vocabulary P0s first.

The first candidate to demote or defer would be:

- B3.2 Finer Purposes

Reason: it is useful, but less central than vocabulary nuance, inference, evidence, tone, and paragraph function for a student trying to move from 246 to 250.

Do not cut:

- C1.1 Context Meaning
- C1.2 Connotation from Context
- C1.3 Figurative Word Meaning
- C2.1 Word Precision
- C3.1 Academic Verbs
- C3.2 Tone Vocabulary

Those are the highest-leverage path to the score goal.

---

## Recommendation Before Locking

Before treating the docs as ready:

1. Clean up stale v3.0 and v2.x references in `curriculum_design.md`.
2. Fully update `csv_schemas.md` for `a1`-`a5`, `b1`-`b6`, and `c1`-`c3`.
3. Remove the self-correction from the lesson schema column count.
4. Update Module 0 schema wording from "8 tools" to "3 MAP categories."
5. Update `why_250.md` so B2 is labeled `Evidence & Inference (Informational)`.

After those fixes, the v3.1 curriculum and supporting docs are in good shape for content authoring and implementation planning.
