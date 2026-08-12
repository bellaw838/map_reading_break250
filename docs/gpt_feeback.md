# GPT Feedback on `curriculum_design.md`

**Reviewed document:** `docs/curriculum_design.md`  
**Review date:** 2026-05-26  
**Reviewer:** GPT

---

## Overall Assessment

The curriculum design is strong and reviewable. It has a clear product thesis, a focused audience, and a coherent instructional model built around sub-concepts, traps, mini-lessons, and targeted quizzes.

The strongest parts are:

- The product scope is disciplined: no AI tutor, no adaptive engine, no passage library in v1.
- The sub-concept model is clear enough for engineering, curriculum reviewers, and content writers.
- The P0/P1/P2 priority system is the right response to the original quiz-volume concern.
- The trap-led framing is useful because it forces each sub-concept to justify itself through teachable wrong-answer patterns.
- Module 0 is a good orientation layer, especially because it is completion-only rather than scored.

The document is close to ready for reviewer circulation, but a few inconsistencies should be fixed first.

---

## High-Priority Fixes

### 1. Fix the Curriculum Counts

The current rollups appear to overcount by one sub-concept.

Based on the module totals in section 5:

| Module | P0 | P1 | P2 | Total |
|---|---:|---:|---:|---:|
| 1. Central Idea / Theme | 3 | 3 | 3 | 9 |
| 2. Evidence & Inference | 5 | 5 | 0 | 10 |
| 3. Author's Purpose & POV | 4 | 2 | 2 | 8 |
| 4. Tone & Word Choice | 6 | 5 | 0 | 11 |
| 5. Text Structure & Development | 4 | 0 | 2 | 6 |
| 6. Argument & Comparison | 3 | 2 | 1 | 6 |
| 7. Figurative Language & Poetry | 5 | 1 | 3 | 9 |
| **Total** | **30** | **18** | **11** | **59** |

That means:

| Bucket | Current Doc Says | Corrected Count |
|---|---:|---:|
| Launch v1 | 30 + Module 0 / 310 quizzes | Correct |
| Full v1 | 49 + Module 0 / 500 quizzes | 48 + Module 0 / 490 quizzes |
| Master curriculum | 60 + Module 0 / 610 quizzes | 59 + Module 0 / 600 quizzes |

Recommendation: update sections 4.1, 7, and Appendix A so the counts agree with the actual module tables.

### 2. Resolve the Module 7 P0 Contradiction

Section 5.7 says:

> Simile vs Metaphor is included for completeness but is not P0

But the table marks **7.3 Simile vs Metaphor** as P0, and the P0 summary below the table includes it.

This needs one clear decision.

Recommendation: demote **7.3 Simile vs Metaphor** to P1 and promote **7.9 Tone Shift in Poetry** to P0.

Reasoning:

- Students at the Break 250 level likely already know simile vs metaphor at a recognition level.
- Tone shift is a more advanced reading move and better aligned with the app's thesis.
- Tone shift also connects strongly to Module 4, making the cross-module design more coherent.

If the curriculum team wants to keep Simile vs Metaphor as P0, then the explanatory prose should be changed so it no longer says it is "not P0."

---

## Medium-Priority Recommendations

### 3. Consider Tightening Launch v1 Further

The P0 launch is currently 310 quizzes. This is much better than the original ~600-quiz scope, but it may still be large for a quality-first launch.

The highest risk is not engineering. The highest risk is content quality: writing 300+ good quiz items with credible wrong-answer traps, per-choice feedback, and consistent reading level is a major authoring task.

Recommendation: seriously consider the reviewer's tighter MVP target of about 210 quizzes:

- Module 0: 10 recognition quizzes
- 20 P0 sub-concepts
- 200 targeted quizzes

This would make the first launch easier to author, QA, and improve from real usage data.

A possible approach:

- Keep the current 30 P0 list as "Launch v1 candidate P0."
- Mark 20 of those as "MVP P0."
- Treat the remaining 10 as "Launch expansion" rather than full P1.

### 4. Make Module 0 Quiz Answers Single-Tool Only

Module 0 is described as a recognition module where students identify which tool a question is testing. However, the examples include blended answers:

- "Poetry / Structure"
- "Evidence + Inference"

Those blended examples are pedagogically real, but they may make the orientation less clean.

Recommendation: keep Module 0 answers single-tool only. Save blended-tool questions for later modules, where students have more context.

### 5. Reconsider the Name "Reading-Analysis Abstract"

"Reading-Analysis Abstract" is accurate from an architecture standpoint, but it may sound unnatural to students, parents, and teachers.

Possible alternatives:

- Reading Analysis Map
- Reading Analysis Toolkit
- How Advanced Readers Think
- The 8 Reading Tools
- Advanced Reading Orientation

Recommendation: use a more student-facing name in the product and reserve "Module 0" / "orientation" as internal language.

### 6. Review Module 5's Priority Shape

Module 5 has 4 P0, 0 P1, and 2 P2 sub-concepts. That is not wrong, but it is unusual.

If P1 is meant to represent the natural post-launch expansion layer, consider whether one of these should be P1:

- 5.5 Structure Reveals Argument
- 5.6 Openers and Closers

Recommendation: promote **5.5 Structure Reveals Argument** to P1, because it connects directly to Module 6 and supports higher-level analysis.

---

## Pedagogical Notes

### Strong Choices

- Merging main idea and theme is sensible because students often fail both in the same way: they name a topic instead of a message.
- Merging evidence and inference is also strong because inference without evidence becomes guessing.
- Pairing tone and word choice is one of the best curriculum decisions in the doc.
- Treating wrong-answer traps as the "teaching engine" is a useful authoring discipline.
- Making Module 0 completion-only avoids false confidence.

### Potentially Advanced Concepts

The following concepts may be hard for Grade 5 students but appropriate for Grade 7-8 or advanced Grade 6 readers:

- 1.9 Universal vs Text-Specific Theme
- 3.7 Reliable vs Unreliable Narrator
- 6.2 Assumption
- 6.5 Emotional Appeal vs Logical Evidence
- 7.9 Tone Shift in Poetry

This does not mean they should be removed. It means the content style guide should give extra care to passage complexity and example design for these concepts.

---

## Suggested Priority Adjustments

If keeping a 30-sub-concept Launch v1:

| Sub-concept | Current | Suggested | Reason |
|---|---:|---:|---|
| 7.3 Simile vs Metaphor | P0 | P1 | Likely already known by target students. |
| 7.9 Tone Shift in Poetry | P2 | P0 | More advanced, higher leverage, better fit for Break 250. |
| 5.5 Structure Reveals Argument | P2 | P1 | Useful bridge into Module 6. |

If reducing to a 20-sub-concept MVP, the best candidates to demote from P0 are probably:

- 3.2 Finer Purposes
- 4.6 Mood vs Tone
- 5.4 Sequence vs Cause/Effect
- 6.3 Counterclaim and Rebuttal
- 7.3 Simile vs Metaphor

These are useful, but less essential than evidence, inference, central idea, tone, word choice, and paragraph function.

---

## Recommendation Before Reviewer Circulation

Before sending the doc to external reviewers:

1. Correct the sub-concept and quiz rollup counts.
2. Resolve the Module 7 Simile vs Metaphor contradiction.
3. Decide whether Launch v1 means 310 quizzes or whether there should be a smaller MVP tier.
4. Rename Module 0 if the title will be student-facing.
5. Simplify Module 0 quiz examples so they test one tool at a time.

After those fixes, the document is in good shape for curriculum review.
