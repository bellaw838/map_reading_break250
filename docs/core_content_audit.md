# Core Content Audit — Mandatory Starter Path

## Scope

This audit covered the mandatory starter path:

- Two Module 0 orientation lessons.
- 22 MVP graded lesson/quiz packs.
- 24 mini-lessons total.
- 240 quiz items total.

Optional Reading Lab, Library, and future passage-anchored practice were not treated as mandatory launch blockers.

## Audit Standard

Each lesson/quiz pack was checked for:

- Correctness: one best answer, no misleading explanations.
- Difficulty fit: useful for strong RIT 230-240+ readers.
- Trap quality: wrong answers are plausible, not silly.
- Feedback specificity: every option explains the textual signal or trap.
- Alignment with the five reading families in `docs/marking.md`.
- Product fit: fast, focused, non-scary thinking-habit practice.

Quiz items were classified as:

- `keep`: correct, useful, and appropriately hard.
- `revise`: good idea, but wording, difficulty, distractors, or feedback needed cleanup.
- `replace`: too easy, ambiguous, under-supported, or not tied to the intended trap.

## Main Findings

The core content was mostly sound as draft material, but not ready enough to treat as a polished mandatory path.

The recurring problems were:

- Some `hard` labels were inflated; many were really medium.
- A few distractors were too obviously wrong for advanced readers.
- Some correct answers were too long or gave away the reasoning inside the option.
- A small number of items allowed ambiguity or over-inference.
- A few lesson statements were too deterministic and needed softer, context-aware wording.

## High-Priority Fixes Applied

- Module 0 quiz difficulty is now all `easy`, matching its orientation-only purpose.
- Module 0 vocabulary list now cleanly names the Category C tools.
- `A2.4 Avoiding Over-Inference` Q3 no longer rewards outside knowledge about fifth grade.
- `B2.1 Evidence Must Be Traceable` Q8 now uses quoted evidence for all choices.
- `C3.1 Academic Verbs` now defines `assert` as "state confidently" rather than "claim without proof" as a built-in meaning.
- `B4.1 Neutral vs Skeptical` now warns students to test skepticism signals in context instead of treating any hedge/contrast word as automatic skepticism.
- `B1.1 Topic vs Main Idea` removed a historically loaded Civil War example and uses a neutral urban-heat example instead.
- Multiple too-easy or ambiguous items were revised or replaced across Category A, B, and C.
- Answer distributions remain balanced; no mandatory quiz pack now has one answer letter more than four times.

## Verification

Fresh validation passes:

```bash
python3 scripts/validate-content.py
```

Result:

```text
Validated 24 lesson · 24 quiz · 15 lab · 3 library file(s).
All content valid.
```

An independent verification pass found one blocker after the first fix round (`C3.1` Q3 wrong-answer feedback began with "Correct."). That blocker was fixed and re-verified.

## Remaining Product Judgment

The mandatory starter is now stronger and cleaner, but this still should not be marketed as an official MAP simulator or score predictor.

The honest framing remains:

> In 3-5 hours, this app helps students learn the reading-thinking moves that matter most for advanced MAP Reading questions.

The next external step is SME review of `docs/sme_review_packet_mvp.md`.
