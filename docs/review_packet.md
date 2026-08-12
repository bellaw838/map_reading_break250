# Review Packet — Break 250 Reading

**Date:** 2026-05-27
**For:** ELA subject-matter expert (teacher, reading specialist, curriculum designer) or product owner acting as proxy
**Purpose:** Three outstanding decisions that block engineering. Each is a content-judgment call — engineering cannot unblock them.

---

## How to use this doc

For each of the three items below:

1. Read the **What to read** section.
2. Answer the **Questions** posed.
3. Record verdict in the **Verdict** block — `Approve` / `Approve with changes (list them)` / `Reject (explain)`.
4. When all three are answered, the path opens to rebalancing the worked sample → locking the stack → drafting MVP content.

Estimated total review time: **60–90 minutes.**

---

## Item 1 — Structural validation of the v3.1 curriculum

### What it is

Confirm the curriculum's **shape** — the categories, modules, and sub-concept buckets — is sound before content authoring scales up. If the structure is wrong, every quiz we write is wrong.

### What to read

- `docs/curriculum_design.md`, especially §4 (module list), §4.1 (launch scope), §5 (modules and sub-concepts), §6 (cross-category overlaps), §8 (mapping from v2.4 → v3.x), and §9 (open questions).
- `docs/why_250.md` (positioning manifesto — gives the *why* behind the categories).

### Background you may not have

- The curriculum mirrors **MAP Reading's 3 scored sub-areas:** Literary Text (Category A), Informational Text (Category B), Vocabulary (Category C). Choice driven by the fact that MAP reports scores in these three areas, so a student who needs to lift a specific sub-score has a direct path through one category.
- **14 modules + Module 0.** 5 in A, 6 in B, 3 in C.
- **65 sub-concepts total.** Each sub-concept = one mini-lesson + 10 trap-revealing quizzes.
- **Trap-led design:** every sub-concept exists to disarm a specific wrong-answer trap that plateaued readers fall into. If a sub-concept can't credibly support 10 trap-revealing quizzes, it doesn't earn its slot.

### Questions to answer

1. **Are the 3 categories the right top-level buckets?** Or should we split / merge / rename?
2. **Is anything misfiled?** Examples: should "Inference" really live mostly in Category A, with informational inference as a B2 sub-section? Or should B have its own full Inference module?
3. **Is the C split into 3 modules (C1 Context Meaning / C2 Word Nuance & Precision / C3 Academic & Tone Lexicon) too granular?** Could it be one module? Or is it underdone — should there be a fourth (e.g., Etymology / Word Parts)?
4. **Is the Tone split (A4 fiction / B4 nonfiction) the right call?** Or is tone one transferable skill that should be taught once?
5. **Are any high-leverage MAP skills missing entirely?**
6. **Within each module, are the sub-concepts well-grouped?** Or do any feel like padding, duplicates, or out of scope?
7. **Is any sub-concept's "trap" invented or weak?** Trap quality is what makes content distinctive — flag any that don't ring true to how real students mis-answer.

### Verdict

```
Verdict (Item 1): APPROVED with minor changes (GPT review, 2026-05-27)

Specific changes requested:
- Keep B2 Evidence & Inference (Informational) as written.
- Keep C1/C2/C3 as separate Vocabulary modules.
- Keep A4/B4 tone split.
- OPEN: decide whether B3.2 Finer Purposes should remain P0 or move to P1 (deferred to product owner).

Reviewer: GPT (see docs/answer_gpt.md for full reasoning)
```

---

## Item 2 — P0-4 worked sample pedagogical review

### What it is

The worked sample for **B4.1 "Neutral vs Skeptical"** (Tone in nonfiction). This is the canonical example every other content writer will copy from. If it's pedagogically thin, every sub-concept after it inherits the flaw.

It already validates against the CSV schemas. What it needs now is a **teacher's eye** on the pedagogy.

### What to read

- `content/lessons/b4/01-neutral-vs-skeptical.csv` — one row containing: title, quick_ref, ~500-word mini-lesson, 3 common traps, 4 worked examples.
- `content/quizzes/b4/01-neutral-vs-skeptical.csv` — 10 quizzes, each with question + 4 choices + correct answer + per-choice feedback + difficulty.

Both files are short. CSV is hard to read by eye — easiest to open in a spreadsheet or run them through a CSV viewer.

### Known issue (already flagged, please confirm)

**Answer-position bias.** The correct answer lands on choice B for 7 of 10 quizzes. Real assessments distribute roughly evenly across A/B/C/D. Will be rebalanced after this review — please confirm the rebalance is needed.

### Questions to answer

1. **Mini-lesson voice and reading level.** Right for an advanced Grade 5–8 reader? Too dry? Too dense? Right amount of jargon (e.g., "hedging verb," "distancing phrase")?
2. **Worked examples.** Are the 4 examples (eco-friendly bottle, city council vote, traffic policy, new bridge) clean discriminators between neutral and skeptical? Or do any feel ambiguous?
3. **The 10 quiz traps — are they real?** I drafted them as architect, not teacher. The test for each trap: *would a real Break-250-level student actually pick this tempting wrong answer?* If you'd predict they wouldn't, the trap is invented and the quiz is weak.
4. **Per-choice feedback specificity.** Each wrong choice has an explanation. Are those explanations specific (names the trap, names the textual signal) or generic ("This isn't quite right")? The wrong-answer-trap feedback is the product's teaching engine — generic feedback would be a critical failure.
5. **Difficulty spread.** Quizzes are tagged easy/medium/hard. Does the labeling match what a real student would experience?
6. **Anything missing?** Should this sub-concept have an example for *irony as a hedging signal* or *passive voice as a distancing move*? Anything you'd add?

### Verdict

```
Verdict (Item 2): APPROVED with required fixes (GPT review, 2026-05-27)

Specific fixes required before this can be the template:
- DONE 2026-05-27: Rebalance answer positions. New distribution A=3, B=3, C=2, D=2.
- NOTED: Light ambiguity pass on examples using "declared," "assured," "claimed" — these can be neutral in context. Current quizzes already pair these verbs with contextual contrast signals (e.g., "after just two months," "however," outcome reversal), and the per-choice feedback explicitly attributes skepticism to both the verb AND the surrounding context. Reviewed and judged sufficient; no change required.
- DONE: Clean neutral examples preserved (Q4 "library closes" and Q6 "school board voted" remain unambiguous neutrals after rebalance).

Reviewer: GPT (see docs/answer_gpt.md for full reasoning)
```

---

## Item 3 — MVP composition validation

### What it is

The product launches in stages. The first usable ship — the **MVP** — is **22 sub-concepts + Module 0 = 230 quizzes**. The question is: are these the right 22? Pick wrong and the first pilot users won't move their scores; pick right and the early signal validates the whole product.

### What to read

- `content/STATUS.md` — the MVP composition is listed at the top, broken into Vocabulary (6), Literary (9), Informational (7) buckets.
- `docs/curriculum_design.md` §4.1 — explains the MVP tier rationale and per-category counts.

### The 22 sub-concepts currently picked for MVP

**Category C — Vocabulary (all 6 P0 ship in MVP)**
- C1.1 Context Meaning
- C1.2 Connotation from Context
- C1.3 Figurative Word Meaning
- C2.1 Word Precision
- C3.1 Academic Verbs
- C3.2 Tone Vocabulary

**Category A — Literary (9 P0 ship in MVP)**
- A1.1 Theme Is a Message, Not a Topic
- A1.2 Theme Is Supported by Multiple Details
- A2.1 Inference = Clue + Reasoning
- A2.2 Inference from Character Action
- A2.3 Inference vs Stated Fact
- A2.4 Avoiding Over-Inference
- A4.1 Tone vs Topic in Fiction
- A4.3 Mood vs Tone
- A5.1 Imagery Creates Meaning

**Category B — Informational (7 P0 ship in MVP)**
- B1.1 Topic vs Main Idea
- B1.2 Main Idea vs Supporting Detail
- B2.1 Evidence Must Be Traceable
- B2.3 Proof vs Related Information
- B2.5 Inference from Nonfiction Cues
- B4.1 Neutral vs Skeptical (= worked sample)
- B5.3 Paragraph Function

**Plus Module 0** (orientation, not scored).

### The reasoning behind this composition

- **Vocab-first weighting.** The MAP-data analysis identifies vocabulary as the #1 unlocking factor at this level. All 6 P0 vocab sub-concepts ship from day one.
- **Literary inference second.** Per the diagnosis: *"vocabulary nuance + literary inference + advanced passage analysis"* — so 4 of 9 literary slots are inference.
- **Informational as maintenance.** Currently strong for most plateaued readers, so MVP has fewer informational sub-concepts but includes the most-trapped (Neutral vs Skeptical) and the foundation (Evidence, Main Idea, Paragraph Function).

### Visible gaps

- **Zero from Module 3 (Author's Purpose & POV).** Is that OK for MVP? Or does a student need at least Three Core Purposes (B3.1) early?
- **Zero from Module 6 (Argument & Comparison).** Is that OK? Or is at least Claim/Evidence/Reasoning (B6.1) a day-one need?
- **Only 1 from Category A's Module 5 (Figurative Language & Poetry).** Imagery only. Is that enough literary figurative coverage?

### Possible adjustments (GPT review 2 suggested)

- **B3.2 Finer Purposes:** could demote from P0 to P1 if MVP needs to tighten.
- B3.1 Three Core Purposes (currently P0, not in MVP): could swap in for one of the demotable items.

### Questions to answer

1. **Vocab-first weighting:** correct? Or should literary inference get more of the slots?
2. **Is the gap in Modules 3 (Purpose) and 6 (Argument) acceptable for MVP?**
3. **Would you swap any of the 22 picks?** Specific swap recommendations welcome.
4. **MVP size:** 22 sub-concepts = 230 quizzes. Tighter (e.g., 15 = 160) or wider (e.g., 30 = 310) preferable?

### Verdict

```
Verdict (Item 3): APPROVED with one open swap discussion (GPT review, 2026-05-27)

Swaps and adjustments:
- Vocab-first weighting CONFIRMED. All 6 Category C sub-concepts stay in MVP.
- MVP size CONFIRMED at 22 + Module 0 = 230 quizzes. Do not expand to 30; do not shrink below 20.
- OPEN: Should B3.1 Three Core Purposes enter MVP? If yes, swap out either A4.3 Mood vs Tone OR A5.1 Imagery Creates Meaning. Deferred to product owner — needs judgment on whether day-one Author's Purpose coverage matters more than Mood-vs-Tone discrimination or Imagery interpretation.

Reviewer: GPT (see docs/answer_gpt.md for full reasoning)
```

---

## After review

Once all three verdicts are recorded:

1. I apply any changes requested.
2. Rebalance B4.1 answer positions (already known fix).
3. Lock the stack (P0-5) — held until this review pass.
4. Begin MVP content drafting, starting with Category C sub-concepts (vocab-first).
5. Engineering Phase 0 closes; Phase 1 (core lesson/quiz flow) opens.

---

## Quick reference — supporting docs

| Doc | Purpose |
|---|---|
| `docs/curriculum_design.md` | Full curriculum spec (v3.1.3) |
| `docs/why_250.md` | Public-facing manifesto on MAP 250+ and the 3 categories |
| `docs/csv_schemas.md` | Lesson + quiz CSV schemas (v1.1) — informational only for this review |
| `content/STATUS.md` | Content workstream tracker; MVP composition lives here |
| `project_plan.md` | Engineering phase plan |
| `progress_tracking.md` | Per-component status checklist |
| `progress.md` | Dated narrative log of every decision and change |

If anything in this packet contradicts those source docs, the source docs are canonical — flag the contradiction so I can fix it.
