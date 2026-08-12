# content/STATUS.md — Content workstream tracker

**As of:** 2026-05-27
**Curriculum locked:** v3.1 (`docs/curriculum_design.md`) — Vocabulary expanded to 3 modules; B2 adds informational inference
**Schemas locked:** v1.1 (`docs/csv_schemas.md`) — Module 0 exception added; file layout aligned with v3.1 IDs
**Target Launch v1:** 40 P0 sub-concepts + Module 0 = **410 quizzes**
**First ship (MVP):** 22 P0 sub-concepts + 2 Module 0 orientation lessons = **240 quizzes** (vocab-first, hits all 3 MAP categories)

Status legend: `Not Started` · `Drafting` · `In Review` · `Approved` · `Shipped`

---

## MVP — first usable ship (22 packs + 2 Module 0 orientation lessons, ~240 quizzes)

Vocab-first composition. A pilot user gets meaningful content for every MAP sub-score from day one.

### Vocabulary (Category C) — all 6 P0 ship in MVP

| ID | Module | Slug | Lesson | Quizzes |
|---|---|---|---|---|
| C-C1.1 | c1 | context-meaning | **Drafted 2026-05-27** | **Drafted 2026-05-27** |
| C-C1.2 | c1 | connotation-from-context | **Drafted 2026-05-27** | **Drafted 2026-05-27** |
| C-C1.3 | c1 | figurative-word-meaning | **Drafted 2026-05-27** | **Drafted 2026-05-27** |
| C-C2.1 | c2 | word-precision | **Drafted 2026-05-27** | **Drafted 2026-05-27** |
| C-C3.1 | c3 | academic-verbs | **Drafted 2026-05-27** | **Drafted 2026-05-27** |
| C-C3.2 | c3 | tone-vocabulary | **Drafted 2026-05-27** | **Drafted 2026-05-27** |

### Literary (Category A) — 9 P0 ship in MVP

| ID | Module | Slug | Lesson | Quizzes |
|---|---|---|---|---|
| C-A1.1 | a1 | theme-message-not-topic | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-A1.2 | a1 | theme-multiple-details | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-A2.1 | a2 | inference-clue-reasoning | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-A2.2 | a2 | inference-from-character-action | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-A2.3 | a2 | inference-vs-stated-fact | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-A2.4 | a2 | avoiding-over-inference | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-A4.1 | a4 | tone-vs-topic-fiction | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-A4.3 | a4 | mood-vs-tone | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-A5.1 | a5 | imagery-creates-meaning | **Drafted 2026-05-28** | **Drafted 2026-05-28** |

### Informational (Category B) — 7 P0 ship in MVP

| ID | Module | Slug | Lesson | Quizzes |
|---|---|---|---|---|
| C-M0 | m0 | abstract | **Drafted 2026-05-27** | **Drafted 2026-05-27** (A=3/B=3/C=2/D=2; ~460 words) |
| C-B1.1 | b1 | topic-vs-main-idea | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-B1.2 | b1 | main-idea-vs-detail | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-B2.1 | b2 | evidence-traceable | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-B2.3 | b2 | proof-vs-related | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-B2.5 | b2 | inference-from-nonfiction | **Drafted 2026-05-28** | **Drafted 2026-05-28** |
| C-B4.1 | b4 | neutral-vs-skeptical | **Drafted + reviewed 2026-05-27** | **Drafted + reviewed 2026-05-27** |
| C-B5.3 | b5 | paragraph-function | **Drafted 2026-05-28** | **Drafted 2026-05-28** |

**MVP total: 22 graded sub-concepts + 2 Module 0 orientation lessons = 240 quizzes, 24 mini-lessons.**

---

## Post-MVP P0 (Launch v1 expansion — 18 more sub-concepts, ~180 quizzes)

| ID | Module | Slug |
|---|---|---|
| C-A2.5 | a2 | inference-from-word-choice-narrative |
| C-A3.1 | a3 | narrator-vs-author |
| C-A4.2 | a4 | tone-words-fiction |
| C-A5.2 | a5 | symbolism |
| C-A5.4 | a5 | speaker-not-poet |
| C-A5.5 | a5 | line-break |
| C-B2.2 | b2 | best-supported-answer |
| C-B3.1 | b3 | three-core-purposes |
| C-B3.2 | b3 | finer-purposes |
| C-B3.3 | b3 | purpose-vs-main-idea |
| C-B3.4 | b3 | purpose-from-word-choice |
| C-B4.2 | b4 | tone-words-nonfiction |
| C-B4.3 | b4 | word-choice-creates-tone |
| C-B5.1 | b5 | five-common-structures |
| C-B5.2 | b5 | signal-words |
| C-B5.4 | b5 | sequence-vs-cause-effect |
| C-B6.1 | b6 | claim-evidence-reasoning |
| C-B6.2 | b6 | assumption |
| C-B6.3 | b6 | counterclaim-rebuttal |

**Launch v1 grand total:** 40 P0 sub-concepts + Module 0 = **410 quizzes**, 41 mini-lessons.

---

## Content authoring style — based on worked sample (C-B4.1)

`content/lessons/b4/01-neutral-vs-skeptical.csv` + `content/quizzes/b4/01-neutral-vs-skeptical.csv` is the canonical style reference.

### Style rules surfaced from the worked sample

1. **Mini-lesson voice:** direct, second-person where appropriate, named "tools" the student can use. ~500 words.
2. **Quick ref:** ≤ 200 chars, action-oriented ("look for X").
3. **Examples:** real-sounding sentences in the appropriate genre. Pair a positive example with a negative one to build discrimination.
4. **Quiz mix per sub-concept:** 2 concept-ID + 2 sentence-level + 4 short-passage + 1 trap-focus + 1 evidence selection.
5. **Per-choice feedback:** every wrong choice's feedback names the trap (why it's tempting) and why it fails. Every correct choice's feedback explains the rule, not just "correct."
6. **Difficulty mix:** roughly 2–3 easy, 4–5 medium, 2–3 hard per sub-concept.

### Known authoring issues to fix in future content

- **C-B4.1 has answer-position bias** (7 of 10 correct = choice B). Distribute roughly even across A/B/C/D.
- **Genre matching:** Category A uses literary passages; Category B uses nonfiction; Category C can mix (vocabulary works in any genre).
- **Reading level:** kept deliberately accessible. Advanced sub-concepts (A1.4, A3.2, B6.2, B6.5) should not raise passage level — keep complexity in the *analytical move*.

## Post-launch (P1 — Full v1)

16 P1 sub-concepts; ~160 additional quizzes.

## Long-term (P2)

9 P2 sub-concepts; ~90 additional quizzes. Master curriculum total: **660 quizzes**.
