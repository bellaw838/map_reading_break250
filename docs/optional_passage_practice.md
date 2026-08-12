# Optional Passage-Anchored Practice

## Positioning

Passage-anchored practice should be an optional challenge layer, not part of the first mandatory path.

The mandatory path stays fast:

- Module 0 orientation.
- Three MAP-aligned sections.
- Short mini-lessons.
- Ten trap-focused quiz items per sub-concept.

Passage practice comes after that for students who want a more test-like transfer check. It should be labeled as deeper practice, not as a MAP score predictor.

## Why It Exists

The core app teaches reading moves one at a time. A real passage set asks the student to combine them:

- Read 300-600 words.
- Track main idea or theme.
- Notice tone and word choice.
- Choose evidence.
- Avoid over-inference.
- Explain paragraph function or structure.

This is closer to MAP-style work because several questions hang off the same text. It tests transfer: can the student use the right tool when the question does not name it?

## Optional Framing

Use student-facing language like:

> Optional Challenge: Apply several reading moves to one longer passage.

Avoid:

> MAP predictor
> 250 readiness score
> Official test simulation

If a readiness check is added later, label it honestly:

> This is a readiness signal from our practice content, not an official MAP-equated score.

## Passage Set Shape

Each set should contain:

- One passage, 300-600 words.
- Six scored questions.
- One short reflection prompt after scoring.
- Per-choice feedback for every answer.
- Difficulty and skill tags for each question.
- A short explanation of which reading move each item tested.

Recommended mix per set:

| Item | Primary move |
|---|---|
| 1 | Main idea / theme |
| 2 | Vocabulary in context or connotation |
| 3 | Evidence selection |
| 4 | Inference with limits |
| 5 | Tone / word choice |
| 6 | Structure / paragraph function / purpose |

## Suggested Schema

Store passage sets separately from the mandatory lesson/quiz CSVs so they do not blur the onboarding promise.

Proposed path:

```text
content/passages/
  literary/
    p001-title.json
  informational/
    p001-title.json
  vocabulary/
    p001-title.json
```

Proposed JSON shape:

```json
{
  "id": "literary-p001",
  "category": "literary",
  "title": "Passage title",
  "source": "Original / public domain / adapted",
  "difficulty_band": "230-240-transfer",
  "is_optional": true,
  "passage": "Full passage text...",
  "questions": [
    {
      "id": "literary-p001-q01",
      "skill": "theme",
      "marking_family": "theme",
      "difficulty": "medium",
      "prompt": "Question text",
      "choices": {
        "A": "Choice A",
        "B": "Choice B",
        "C": "Choice C",
        "D": "Choice D"
      },
      "correct_choice": "B",
      "feedback": {
        "A": "Trap feedback",
        "B": "Correct feedback",
        "C": "Trap feedback",
        "D": "Trap feedback"
      },
      "tested_move": "What the student had to notice"
    }
  ],
  "reflection_prompt": "Which question required the deepest rereading? What clue changed your answer?"
}
```

## Quality Bar

A passage set is not approved unless:

- Every question requires the passage.
- Every distractor is plausible for a strong reader.
- Every correct answer has one best textual reason.
- Feedback names both the trap and the textual signal.
- Difficulty comes from subtle evidence, not obscure vocabulary.
- The set includes at least one evidence item and one inference-limit item.
- The passage is short enough to complete without scaring away a busy student.

## Build Later

Do not add 8-12 passage sets until the mandatory path has been pilot-tested or a reviewer specifically asks for MAP-like transfer practice.

When built, start with 3 pilot sets:

- One literary passage.
- One informational passage.
- One mixed vocabulary-in-context passage.

Use those to test the UI, timing, scoring language, and student reaction before scaling to 8-12 sets.
