# CSV Schemas — Break 250 Reading

**Status:** Locked v1.1 (2026-05-27)
**Owners:** Architect; content writers must conform; stack-specific validators must implement this spec exactly.

---

## Purpose

Defines the on-disk format for all curriculum content. Every lesson and quiz in `content/` must conform. A loader implementation (in whatever stack we pick) is responsible for parsing, validating against this spec, and surfacing useful errors.

**Stack-neutral.** This doc commits to no framework. A reference TypeScript+Zod implementation is included at the bottom as illustration, but the schemas are equally implementable in Python/dataclasses, Rust/serde, Go/structs, etc.

---

## File layout (updated 2026-05-27 for v3.x curriculum)

```
content/
  lessons/
    m0/abstract.csv                          # Module 0 — orientation lesson
    a1/01-theme-message-not-topic.csv        # Category A — Literary Text
    a2/01-inference-clue-reasoning.csv
    a3/01-narrator-vs-author.csv
    a4/01-tone-vs-topic-fiction.csv
    a5/01-imagery-creates-meaning.csv
    b1/01-topic-vs-main-idea.csv             # Category B — Informational Text
    b2/01-evidence-traceable.csv
    b3/01-three-core-purposes.csv
    b4/01-neutral-vs-skeptical.csv           # worked sample (was m4/03 in v2.x)
    b5/01-five-common-structures.csv
    b6/01-claim-evidence-reasoning.csv
    c1/01-context-meaning.csv                # Category C — Vocabulary
    c2/01-word-precision.csv
    c3/01-academic-verbs.csv
  quizzes/
    m0/abstract.csv                          # 10 recognition quizzes
    a1/01-theme-message-not-topic.csv        # 10 rows each
    ...
    b4/01-neutral-vs-skeptical.csv           # 10 rows
    ...
    c1/01-context-meaning.csv
    c2/01-word-precision.csv
    c3/01-academic-verbs.csv
```

**Rules:**
- Top-level folder per module: `m0`, `a1`..`a5`, `b1`..`b6`, `c1`..`c3`. Module-ID prefix encodes the MAP category (`a` = Literary, `b` = Informational, `c` = Vocabulary).
- One CSV per sub-concept. **Filename is the canonical sub-concept slug.**
- File naming: `{NN}-{kebab-slug}.csv` where `NN` is a zero-padded ordinal within the module (e.g., `01-…`, `02-…`).
- Module 0 has exactly one lesson file: `m0/abstract.csv`. Same for the quiz file.
- Lesson and quiz files **must have matching filenames** (the loader pairs them by name).

### Column-value rules (v3.x)

- `module_id` ∈ {`m0`, `a1`, `a2`, `a3`, `a4`, `a5`, `b1`, `b2`, `b3`, `b4`, `b5`, `b6`, `c1`, `c2`, `c3`}.
- `sub_concept_id` uses uppercase prefix matching the curriculum doc: `A1.1`, `A2.3`, `B4.1`, `C1.3`, etc. For Module 0: `0`.
- `quiz_id` format: `{module_lower}-{N}_q{NN}` — e.g., `b4-1_q03` for B4.1 quiz #3. Module 0 quizzes use `m0_q{NN}`.

---

## Schema 1 — Lesson CSV (one row per file)

A lesson CSV contains **exactly one data row** (plus the header). It describes a complete mini-lesson for one sub-concept.

### Columns (26)

| # | Column | Type | Required | Notes |
|---|---|---|:-:|---|
| 1 | `module_id` | string | yes | `m0`, `a1`–`a5`, `b1`–`b6`, `c1`–`c3`. Must match the file's parent directory. |
| 2 | `sub_concept_id` | string | yes | E.g., `B4.1`, `A2.3`, `C1.3`. Matches curriculum doc IDs. For Module 0: `0`. |
| 3 | `slug` | string | yes | E.g., `neutral-vs-skeptical`. Must match the filename slug (without the `NN-` prefix and `.csv`). |
| 4 | `title` | string | yes | Student-facing title. E.g., `Neutral vs Skeptical`. |
| 5 | `subtitle` | string | optional | One-line subtitle. `N/A` if unused. |
| 6 | `quick_ref` | string | yes | The 1-sentence pre-read reminder used by the `/reference` page. ≤ 200 chars. |
| 7 | `mini_lesson` | string (multi-line) | yes | The full mini-lesson body. Markdown allowed. Aim 300–600 words (500–800 for Module 0). |
| 8 | `why_it_matters` | string | optional | Short paragraph. `N/A` if folded into `mini_lesson`. |
| 9 | `common_trap_1` | string | yes (except Module 0 — see below) | The primary trap this sub-concept disarms. Must match curriculum doc's trap statement. |
| 10 | `common_trap_2` | string | optional | `N/A` if unused. |
| 11 | `common_trap_3` | string | optional | `N/A` if unused. |
| 12–14 | `example_1_text`, `example_1_answer`, `example_1_explanation` | string × 3 | yes (all three or none — except Module 0 — see below) | First worked example. |
| 15–17 | `example_2_text`, `example_2_answer`, `example_2_explanation` | string × 3 | optional (all three or none — `N/A` for unused) | |
| 18–20 | `example_3_text`, `example_3_answer`, `example_3_explanation` | string × 3 | optional | |
| 21–23 | `example_4_text`, `example_4_answer`, `example_4_explanation` | string × 3 | optional | |
| 24–26 | `example_5_text`, `example_5_answer`, `example_5_explanation` | string × 3 | optional (all three or none — `N/A` for unused) | |

Total: **11 non-example columns (1–11) + 15 example columns (12–26) = 26 columns.**

### Validation rules

- `module_id` must equal the file's parent directory name (one of: `m0`, `a1`–`a5`, `b1`–`b6`, `c1`–`c3`).
- **Module 0 exception:** when `module_id == "m0"`, the otherwise-required fields `common_trap_1` and `example_1_*` MAY be `N/A`. Module 0 is an orientation lesson that does not follow the trap-led sub-concept format. All trap and example fields default to `N/A` for Module 0.
- `slug` must equal the filename without its `NN-` prefix and `.csv` suffix.
- Examples must be **filled in sequence**. If `example_3_*` has content, `example_1_*` and `example_2_*` must also have content.
- Unused example slots must use the literal string `N/A` in all three fields (text, answer, explanation).
- `mini_lesson` field can span multiple lines inside a quoted CSV cell. Newlines, commas, and double quotes must follow standard CSV escaping (RFC 4180: wrap in double quotes; escape inner double quotes by doubling).
- `quick_ref` ≤ 200 chars (loader warns; doesn't reject).

### Example row (B4.1 Neutral vs Skeptical — abbreviated)

```
module_id,sub_concept_id,slug,title,...
b4,B4.1,neutral-vs-skeptical,Neutral vs Skeptical,...
```

Full worked sample: `content/lessons/b4/01-neutral-vs-skeptical.csv`.

---

## Schema 2 — Quiz CSV (10 rows per file)

A quiz CSV contains **exactly 10 data rows** (plus the header). Each row is one quiz.

### Columns (14)

| # | Column | Type | Required | Notes |
|---|---|---|:-:|---|
| 1 | `quiz_id` | string | yes | E.g., `b4-1_q01`. Format `{module_lower}-{N}_q{NN}`. Globally unique. |
| 2 | `question_number` | integer 1–10 | yes | No gaps, no duplicates within a file. |
| 3 | `prompt` | string (multi-line) | yes | The question. Can contain a short embedded passage (use newlines inside quoted cell). |
| 4 | `choice_a` | string | yes | |
| 5 | `choice_b` | string | yes | |
| 6 | `choice_c` | string | yes | |
| 7 | `choice_d` | string | yes | |
| 8 | `correct_choice` | enum `A`/`B`/`C`/`D` | yes | Case-sensitive. |
| 9 | `feedback_a` | string | yes | Per-choice feedback. **Required for all 4 choices** — non-negotiable. |
| 10 | `feedback_b` | string | yes | |
| 11 | `feedback_c` | string | yes | |
| 12 | `feedback_d` | string | yes | |
| 13 | `trap_type` | string | optional | Tag like `b4.1-neutral-vs-skeptical`. Usually matches parent sub-concept ID. `N/A` for Module 0. |
| 14 | `difficulty` | enum `easy`/`medium`/`hard` | yes | |

### Validation rules

- Exactly **10 data rows** per file. Loader **fails loudly** with fewer or more.
- `question_number` values must be `1, 2, 3, …, 10` — no gaps, no duplicates, no out-of-range.
- `correct_choice` must be exactly one of `A`, `B`, `C`, `D`.
- All four `feedback_*` fields required for every row. **Blank is a hard error** — the per-choice feedback is the teaching engine. The feedback for the `correct_choice` letter should explain why it's right; the other three should explain why their respective wrong choice is tempting and why it's still wrong.
- `quiz_id` must be unique across the entire `content/quizzes/` tree (loader can build a uniqueness index).
- `difficulty` ∈ `{easy, medium, hard}`.

### Example row (B4.1 quiz #3 — abbreviated)

```
quiz_id,question_number,prompt,...,correct_choice,feedback_a,...,trap_type,difficulty
b4-1_q03,3,"Read: ...",B,...,b4.1-neutral-vs-skeptical,medium
```

Full worked sample: `content/quizzes/b4/01-neutral-vs-skeptical.csv`.

---

## Module 0 specifics

Module 0 uses **the same two schemas**, with these conventions and exemptions:

- `m0/abstract.csv` (lesson) has `module_id=m0`, `sub_concept_id=0`, `slug=abstract`.
- `mini_lesson` carries the full Module 0 mini-lesson (500–800 words) including the 3-MAP-categories preview, the core tools inside each category, and the basic-vs-advanced reader contrast table as embedded markdown.
- **Schema exception:** `common_trap_1` and `example_1_*` are exempt from the usual required-field rule when `module_id == "m0"`. All trap and example fields default to `N/A` because Module 0 is orientation, not trap-led.
- `m0/abstract.csv` (quiz) has 10 rows, all recognition-format. `trap_type=N/A`. `difficulty=easy`.

The loader recognizes `module_id=m0` and routes to the Module 0 special page.

The reference Zod validator at the bottom of this doc should include a `.refine()` that allows `N/A` in `common_trap_1` and `example_1_*` when `module_id === "m0"`, but rejects `N/A` in those fields for any other module.

---

## CSV format requirements (RFC 4180-ish)

- UTF-8, no BOM.
- Header row required, column names exactly as specified above.
- Standard CSV quoting: wrap any field containing commas, newlines, or double quotes in double quotes; escape inner double quotes by doubling (`""`).
- Empty/null is **never valid** in required fields. Use `N/A` for "explicitly empty optional."
- Unix line endings (`\n`) preferred. Loader should tolerate `\r\n`.

---

## Reference validator (illustrative — TypeScript + Zod)

This is a sketch of how the schemas might be enforced in a TypeScript+Zod stack. Other stacks must implement equivalent validation.

```typescript
import { z } from "zod";

const ModuleId = z.enum([
  "m0",
  "a1", "a2", "a3", "a4", "a5",
  "b1", "b2", "b3", "b4", "b5", "b6",
  "c1", "c2", "c3",
]);
const Difficulty = z.enum(["easy", "medium", "hard"]);
const Choice = z.enum(["A", "B", "C", "D"]);

const NonEmpty = z.string().min(1);
const NA = z.literal("N/A");
const OptionalField = z.union([NA, NonEmpty]);

const ExampleTriple = z.object({
  text: OptionalField,
  answer: OptionalField,
  explanation: OptionalField,
});

export const LessonSchema = z.object({
  module_id: ModuleId,
  sub_concept_id: NonEmpty,
  slug: NonEmpty,
  title: NonEmpty,
  subtitle: OptionalField,
  quick_ref: NonEmpty.max(200),
  mini_lesson: NonEmpty,
  why_it_matters: OptionalField,
  // common_trap_1 + example_1_* are normally required.
  // Module 0 is exempt — see the refinement below.
  common_trap_1: OptionalField,
  common_trap_2: OptionalField,
  common_trap_3: OptionalField,
  example_1: ExampleTriple,
  example_2: ExampleTriple,
  example_3: ExampleTriple,
  example_4: ExampleTriple,
  example_5: ExampleTriple,
}).refine(
  // Module 0 exception: when module_id === "m0", common_trap_1 and example_1_*
  // may all be N/A. For every other module, common_trap_1 must be non-empty
  // and example_1_* must be filled (not N/A).
  (lesson) => {
    if (lesson.module_id === "m0") return true;
    const filled = (e: typeof lesson.example_1) =>
      e.text !== "N/A" && e.answer !== "N/A" && e.explanation !== "N/A";
    return lesson.common_trap_1 !== "N/A" && filled(lesson.example_1);
  },
  { message: "common_trap_1 and example_1 are required for all modules except m0" },
).refine(
  // example sequencing: if example_N is filled, example_{N-1} must be filled.
  // Module 0 is exempt — Module 0 lessons may have all example_* set to N/A.
  (lesson) => {
    if (lesson.module_id === "m0") return true;
    const filled = (e: typeof lesson.example_1) =>
      e.text !== "N/A" && e.answer !== "N/A" && e.explanation !== "N/A";
    const flags = [
      filled(lesson.example_1),
      filled(lesson.example_2),
      filled(lesson.example_3),
      filled(lesson.example_4),
      filled(lesson.example_5),
    ];
    // example_1 must be filled (for non-m0 modules)
    if (!flags[0]) return false;
    // no gaps: once we hit an unfilled, all subsequent must be unfilled
    let sawUnfilled = false;
    for (const f of flags) {
      if (sawUnfilled && f) return false;
      if (!f) sawUnfilled = true;
    }
    return true;
  },
  { message: "Examples must be filled in sequence with no gaps; example_1 is required (Module 0 exempt)" },
);

export const QuizSchema = z.object({
  quiz_id: NonEmpty,
  question_number: z.number().int().min(1).max(10),
  prompt: NonEmpty,
  choice_a: NonEmpty,
  choice_b: NonEmpty,
  choice_c: NonEmpty,
  choice_d: NonEmpty,
  correct_choice: Choice,
  feedback_a: NonEmpty,
  feedback_b: NonEmpty,
  feedback_c: NonEmpty,
  feedback_d: NonEmpty,
  trap_type: OptionalField,
  difficulty: Difficulty,
});

export const QuizFileSchema = z.array(QuizSchema)
  .length(10)
  .refine(
    (rows) => {
      const nums = rows.map((r) => r.question_number).sort((a, b) => a - b);
      return nums.every((n, i) => n === i + 1);
    },
    { message: "question_number must be 1..10 with no gaps or duplicates" },
  )
  .refine(
    (rows) => new Set(rows.map((r) => r.quiz_id)).size === rows.length,
    { message: "quiz_id must be unique within a file" },
  );
```

Notes:
- CSV → object marshalling (turning the flat `example_1_text`/`example_1_answer`/`example_1_explanation` columns into the nested `example_1: ExampleTriple`) happens in the loader, not the validator.
- A Python/dataclasses or Rust/serde implementation should enforce the same rules.

---

## Open schema questions (low-risk)

1. **Allow markdown in `quick_ref`?** Currently the spec says plain string. If formatting helps the `/reference` page (e.g., bold a key trap word), markdown would help — but it also expands the validation surface. Default: plain text; revisit if `/reference` design needs it.
2. **`trap_type` enum vs free string?** Currently free string. Enforcing as enum (one value per sub-concept) prevents typos but requires regenerating the enum every time curriculum changes. Default: free string with a CI lint that warns on unrecognized values.
3. **CSV vs JSON for cells with significant structure?** The lesson `mini_lesson` field carrying multi-paragraph markdown is awkward in CSV. If editing becomes painful, the escape hatch is to move `mini_lesson` to a sibling `.md` file (referenced by filename) without changing the rest of the schema.

These are non-blocking for the worked sample and can be revisited if pain materializes.

---

## Change log

| Version | Date | Changes |
|---|---|---|
| v1.0 | 2026-05-27 | Initial lock. 26-column lesson schema; 14-column quiz schema. RFC 4180 quoting; N/A for empty optional. Module 0 reuses the same schemas. |
| **v1.1** | **2026-05-27** | **Module 0 schema exception** added: when `module_id == "m0"`, `common_trap_1` and `example_1_*` may be `N/A`. Column-rule table updated; new "Module 0 exception" line in validation rules; Module 0 specifics section spells it out; reference Zod validator updated in **both refinements** (the required-field refinement AND the example-sequencing refinement) to short-circuit when `module_id === "m0"`. Also: `module_id` enum expanded to include `c2` and `c3`; file layout examples include c2/c3 rows. Status bumped to v1.1. |
