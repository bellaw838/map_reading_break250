# GPT Answers — Review Packet

**Reviewed packet:** `docs/review_packet.md`  
**Reviewer:** GPT  
**Date:** 2026-05-27

---

## Item 1 — Structural validation of the v3.1 curriculum

**Verdict (Item 1): Approve with minor changes.**

The 3-category structure is the right top-level shape:

- Category A — Literary Text
- Category B — Informational Text
- Category C — Vocabulary

This maps cleanly to MAP Reading reporting and makes the product easier to explain to parents, teachers, and students. It also gives a student with a weak sub-score a direct route through the app.

Specific answers:

1. **Are the 3 categories right?**  
   Yes. Keep them.

2. **Is anything misfiled?**  
   Mostly no. The big correction was already made: B2 now includes informational inference explicitly. That should stay.

3. **Is the C split too granular?**  
   No. Keep C1/C2/C3. Vocabulary is the likely bottleneck, so it deserves more than one module.

4. **Is the Tone split right?**  
   Yes. Keep A4 fiction tone and B4 nonfiction tone separate. Tone is transferable, but the signals differ enough by genre to justify two modules.

5. **Are high-leverage MAP skills missing?**  
   No obvious major gap. The main high-leverage skills are covered: vocabulary nuance, inference, evidence, tone, structure, author purpose, argument, and figurative language.

6. **Are sub-concepts well-grouped?**  
   Mostly yes. The grouping is coherent and teachable.

7. **Are any traps weak?**  
   None are clearly invented at the curriculum level. Trap quality should be checked again during content authoring because a good sub-concept can still produce weak quiz traps.

Specific changes requested:

- Keep `B2 Evidence & Inference (Informational)` as written.
- Keep `C1/C2/C3` as separate Vocabulary modules.
- Keep the `A4/B4` tone split.
- Consider whether `B3.2 Finer Purposes` should remain P0 or move to P1.

---

## Item 2 — B4.1 worked sample pedagogical review

**Verdict (Item 2): Approve with required fixes.**

The B4.1 "Neutral vs Skeptical" sample is pedagogically strong enough to serve as the content template after cleanup.

The mini-lesson is clear, the examples are plausible, and the per-choice feedback usually names the textual signal rather than giving generic feedback. The sub-concept is also high leverage: advanced readers often confuse factual-sounding skeptical writing with neutral reporting.

Specific answers:

1. **Mini-lesson voice and reading level**  
   Good for advanced Grade 5-8 readers. Terms like "hedging verb" and "distancing phrase" are acceptable because the lesson explains them through examples.

2. **Worked examples**  
   Mostly clean. The examples give enough contrast between neutral and skeptical reporting.

3. **Quiz traps**  
   Mostly real. The traps match plausible student mistakes: defaulting to neutral because the sentence sounds factual, overreading difficult vocabulary as tone, and missing hedging words.

4. **Per-choice feedback**  
   Strong overall. The feedback usually names the trap and points to the textual signal.

5. **Difficulty spread**  
   Reasonable. The easy/medium/hard tags broadly match expected difficulty.

6. **Anything missing**  
   No major missing piece. Do not overcomplicate this template with irony or passive voice yet. Keep the first canonical sample focused.

Required fixes before this can be the template:

- Rebalance answer positions. Current correct answers are heavily biased toward `B`, and `D` is never correct.
- Do a light ambiguity pass on examples using words like `declared`, `assured`, and `claimed`. These can signal skepticism in context, but they are not always skeptical by themselves.
- Keep at least one very clean neutral example so students do not learn to over-detect skepticism everywhere.

---

## Item 3 — MVP composition validation

**Verdict (Item 3): Approve with one recommended swap discussion.**

The 22-sub-concept MVP is a good first ship target. It is large enough to cover all three MAP categories, but small enough to author and QA carefully.

The vocab-first weighting is correct. If the target student is near 250 and Vocabulary is the likely bottleneck, all 6 Vocabulary P0 sub-concepts should stay in MVP.

Specific answers:

1. **Vocab-first weighting**  
   Correct. Keep all 6 Vocabulary P0s in MVP.

2. **Gap in Purpose and Argument**  
   Acceptable for MVP, but worth discussing. The biggest concern is zero B3 Author's Purpose coverage. Argument can wait longer than purpose.

3. **Would I swap any of the 22 picks?**  
   Possibly. If reviewers want at least one Author's Purpose skill in MVP, swap in `B3.1 Three Core Purposes`.

   Possible swap candidates:

   - `A4.3 Mood vs Tone`
   - `A5.1 Imagery Creates Meaning`

   I would not cut any Vocabulary item.

4. **MVP size**  
   Keep 22 sub-concepts + Module 0. Do not expand to 30. Do not shrink below 20 unless content capacity becomes a serious constraint.

Swaps and adjustments:

- Recommended discussion: add `B3.1 Three Core Purposes` to MVP if the SME believes purpose questions are common enough for day-one coverage.
- If adding `B3.1`, remove either `A4.3 Mood vs Tone` or `A5.1 Imagery Creates Meaning`.
- Preserve all 6 Category C Vocabulary sub-concepts.

---

## Final Recommendation

Proceed with the v3.1 structure and the 22-sub-concept MVP after:

1. Rebalancing B4.1 answer positions.
2. Doing a light ambiguity pass on the B4.1 skeptical examples.
3. Deciding whether `B3.1 Three Core Purposes` should enter MVP.

Do not expand the MVP beyond 230 quizzes for first ship.
