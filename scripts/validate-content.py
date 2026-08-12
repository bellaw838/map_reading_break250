#!/usr/bin/env python3
"""Validate every CSV under content/ against the locked schema.

Schema reference: docs/csv_schemas.md v1.1.
Curriculum reference: docs/curriculum_design.md v3.1.3.

Run from repo root:
    python3 scripts/validate-content.py

Exit code 0 = all CSVs valid; non-zero = at least one failure (CI gate).
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"

VALID_MODULE_IDS = {
    "m0",
    "a1", "a2", "a3", "a4", "a5",
    "b1", "b2", "b3", "b4", "b5", "b6",
    "c1", "c2", "c3",
}

LESSON_COLUMNS = [
    "module_id", "sub_concept_id", "slug", "title", "subtitle",
    "quick_ref", "mini_lesson", "why_it_matters",
    "common_trap_1", "common_trap_2", "common_trap_3",
    "example_1_text", "example_1_answer", "example_1_explanation",
    "example_2_text", "example_2_answer", "example_2_explanation",
    "example_3_text", "example_3_answer", "example_3_explanation",
    "example_4_text", "example_4_answer", "example_4_explanation",
    "example_5_text", "example_5_answer", "example_5_explanation",
]

QUIZ_COLUMNS = [
    "quiz_id", "question_number", "prompt",
    "choice_a", "choice_b", "choice_c", "choice_d",
    "correct_choice",
    "feedback_a", "feedback_b", "feedback_c", "feedback_d",
    "trap_type", "difficulty",
]

VALID_DIFFICULTIES = {"easy", "medium", "hard"}
VALID_CHOICES = {"A", "B", "C", "D"}
SLUG_FROM_FILENAME = re.compile(r"^\d+-(.+)\.csv$|^([a-z][a-z0-9-]+)\.csv$")

VALID_LAB_CATEGORIES = {"Literary", "Informational", "Poetry", "Fable"}
VALID_LAB_ANN_CATEGORIES = {"tone", "evidence", "theme", "inference", "structure"}
VALID_LAB_DIFFICULTIES = {"Easy", "Medium", "Hard"}
VALID_LIBRARY_TYPES = {"play", "novel", "story-collection"}
MARKING_CODE_FAMILIES = {
    "theme": {"T", "MI", "TH", "CL"},
    "evidence": {"E", "RSN", "TRAP"},
    "inference": {"INF", "POV", "SPK"},
    "tone": {"TO", "M", "WC", "CON", "P"},
    "structure": {"STR", "PF", "SHIFT", "FIG", "CTR"},
}
MARKING_CODE_TO_FAMILY = {
    code: family
    for family, codes in MARKING_CODE_FAMILIES.items()
    for code in codes
}
LEADING_MARKING_CODE = re.compile(r"^([A-Z]+)(?:\s*(?:/|->|→)\s*([A-Z]+))*:")


class ValidationError(Exception):
    def __init__(self, path: Path, message: str):
        super().__init__(f"{path.relative_to(REPO_ROOT)}: {message}")


def validate_lesson(path: Path) -> None:
    module_id = path.parent.name
    if module_id not in VALID_MODULE_IDS:
        raise ValidationError(path, f"module folder '{module_id}' is not a valid module id")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != LESSON_COLUMNS:
            raise ValidationError(
                path,
                f"lesson columns mismatch.\n  expected: {LESSON_COLUMNS}\n  got:      {reader.fieldnames}",
            )
        rows = list(reader)

    if len(rows) != 1:
        raise ValidationError(path, f"lesson CSV must have exactly 1 data row, got {len(rows)}")

    row = rows[0]

    if row["module_id"] != module_id:
        raise ValidationError(
            path,
            f"module_id column ({row['module_id']!r}) must match parent folder ({module_id!r})",
        )

    m = SLUG_FROM_FILENAME.match(path.name)
    if not m:
        raise ValidationError(path, f"filename '{path.name}' does not match expected pattern")
    filename_slug = m.group(1) or m.group(2)
    if row["slug"] != filename_slug:
        raise ValidationError(
            path,
            f"slug column ({row['slug']!r}) must match filename slug ({filename_slug!r})",
        )

    for col in ("title", "quick_ref", "mini_lesson"):
        if not row[col] or row[col] == "N/A":
            raise ValidationError(path, f"required field '{col}' is empty or N/A")

    if len(row["quick_ref"]) > 200:
        raise ValidationError(path, f"quick_ref exceeds 200 chars ({len(row['quick_ref'])})")

    # Sanity checks that catch column-shift bugs (unquoted commas splitting cells).
    # These are content health checks, not strict schema rules.
    if len(row["quick_ref"]) < 30:
        raise ValidationError(
            path,
            f"quick_ref suspiciously short ({len(row['quick_ref'])} chars: {row['quick_ref']!r}) "
            "— possible CSV column-shift from unquoted commas in an earlier cell",
        )
    if row["quick_ref"].startswith(" ") or row["quick_ref"].startswith(","):
        raise ValidationError(
            path,
            f"quick_ref starts with whitespace/punctuation ({row['quick_ref'][:30]!r}) "
            "— possible CSV column-shift",
        )
    if len(row["mini_lesson"]) < 100:
        raise ValidationError(
            path,
            f"mini_lesson suspiciously short ({len(row['mini_lesson'])} chars) "
            "— possible CSV column-shift",
        )

    # Module 0 exception: common_trap_1 and example_1_* may be N/A for m0.
    if module_id != "m0":
        if not row["common_trap_1"] or row["common_trap_1"] == "N/A":
            raise ValidationError(path, "common_trap_1 is required for non-Module-0 lessons")
        for col in ("example_1_text", "example_1_answer", "example_1_explanation"):
            if not row[col] or row[col] == "N/A":
                raise ValidationError(path, f"{col} is required for non-Module-0 lessons")

        # Example sequencing: no gaps once a filled example is followed by N/A.
        filled_flags = []
        for i in range(1, 6):
            t = row[f"example_{i}_text"]
            a = row[f"example_{i}_answer"]
            e = row[f"example_{i}_explanation"]
            filled_flags.append(all(v and v != "N/A" for v in (t, a, e)))
        saw_gap = False
        for i, flag in enumerate(filled_flags, start=1):
            if saw_gap and flag:
                raise ValidationError(
                    path,
                    f"example sequencing violated: example_{i} is filled after a gap",
                )
            if not flag:
                saw_gap = True


def validate_quiz(path: Path) -> None:
    module_id = path.parent.name
    if module_id not in VALID_MODULE_IDS:
        raise ValidationError(path, f"module folder '{module_id}' is not a valid module id")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != QUIZ_COLUMNS:
            raise ValidationError(
                path,
                f"quiz columns mismatch.\n  expected: {QUIZ_COLUMNS}\n  got:      {reader.fieldnames}",
            )
        rows = list(reader)

    if len(rows) != 10:
        raise ValidationError(path, f"quiz CSV must have exactly 10 data rows, got {len(rows)}")

    seen_ids: set[str] = set()
    for idx, row in enumerate(rows, start=1):
        try:
            qnum = int(row["question_number"])
        except ValueError:
            raise ValidationError(path, f"row {idx}: question_number must be an integer") from None
        if qnum != idx:
            raise ValidationError(
                path,
                f"row {idx}: question_number ({qnum}) must equal row position ({idx})",
            )
        if row["quiz_id"] in seen_ids:
            raise ValidationError(path, f"duplicate quiz_id: {row['quiz_id']}")
        seen_ids.add(row["quiz_id"])
        if row["correct_choice"] not in VALID_CHOICES:
            raise ValidationError(
                path, f"row {idx}: correct_choice must be A/B/C/D, got {row['correct_choice']!r}"
            )
        if row["difficulty"] not in VALID_DIFFICULTIES:
            raise ValidationError(
                path, f"row {idx}: difficulty must be easy/medium/hard, got {row['difficulty']!r}"
            )
        for col in ("prompt", "choice_a", "choice_b", "choice_c", "choice_d",
                    "feedback_a", "feedback_b", "feedback_c", "feedback_d"):
            if not row[col] or row[col] == "N/A":
                raise ValidationError(path, f"row {idx}: required field '{col}' is empty or N/A")


def validate_lab(path: Path) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValidationError(path, f"invalid JSON: {e}") from None

    required = ["id", "title", "author", "year", "category", "difficulty", "passage", "annotations", "intro", "discussion_prompts"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValidationError(path, f"missing fields: {missing}")

    if data["category"] not in VALID_LAB_CATEGORIES:
        raise ValidationError(path, f"category {data['category']!r} not in {sorted(VALID_LAB_CATEGORIES)}")

    if data["difficulty"] not in VALID_LAB_DIFFICULTIES:
        raise ValidationError(path, f"difficulty {data['difficulty']!r} not in {sorted(VALID_LAB_DIFFICULTIES)}")

    passage = data["passage"]
    if not isinstance(passage, str) or len(passage) < 50:
        raise ValidationError(path, "passage too short (must be at least 50 chars)")

    if not isinstance(data["annotations"], list):
        raise ValidationError(path, "annotations must be a list")

    passage_len = len(passage)
    annotations = data["annotations"]
    for i, ann in enumerate(annotations, start=1):
        for k in ("start", "end", "category", "note"):
            if k not in ann:
                raise ValidationError(path, f"annotation #{i} missing field {k!r}")
        if not (isinstance(ann["start"], int) and isinstance(ann["end"], int)):
            raise ValidationError(path, f"annotation #{i} start/end must be ints")
        if ann["start"] < 0 or ann["end"] > passage_len or ann["start"] >= ann["end"]:
            raise ValidationError(
                path,
                f"annotation #{i} has invalid offsets [{ann['start']}, {ann['end']}] (passage length {passage_len})",
            )
        if ann["category"] not in VALID_LAB_ANN_CATEGORIES:
            raise ValidationError(
                path,
                f"annotation #{i} category {ann['category']!r} not in {sorted(VALID_LAB_ANN_CATEGORIES)}",
            )
        if not isinstance(ann["note"], str) or len(ann["note"]) < 10:
            raise ValidationError(path, f"annotation #{i} note too short")
        prefix = LEADING_MARKING_CODE.match(ann["note"])
        if not prefix:
            raise ValidationError(
                path,
                f"annotation #{i} note must start with an official Marking Guide code prefix",
            )
        first_code = prefix.group(1)
        if first_code not in MARKING_CODE_TO_FAMILY:
            raise ValidationError(path, f"annotation #{i} note starts with unknown code {first_code!r}")
        expected_family = MARKING_CODE_TO_FAMILY[first_code]
        if expected_family != ann["category"]:
            raise ValidationError(
                path,
                f"annotation #{i} category {ann['category']!r} does not match leading code {first_code!r} "
                f"(family {expected_family!r})",
            )

    # Reading Lab renderer exposes only the first overlapping annotation on a
    # segment. Keep Lab annotations non-overlapping so no note is hidden.
    for i, left in enumerate(annotations, start=1):
        for j, right in enumerate(annotations[i:], start=i + 1):
            if max(left["start"], right["start"]) < min(left["end"], right["end"]):
                raise ValidationError(path, f"annotations #{i} and #{j} overlap")

    if not isinstance(data["discussion_prompts"], list) or len(data["discussion_prompts"]) < 1:
        raise ValidationError(path, "discussion_prompts must be a non-empty list")

    if "discussion_answers" in data:
        if not isinstance(data["discussion_answers"], list):
            raise ValidationError(path, "discussion_answers must be a list")
        if len(data["discussion_answers"]) != len(data["discussion_prompts"]):
            raise ValidationError(
                path,
                f"discussion_answers length ({len(data['discussion_answers'])}) "
                f"must match discussion_prompts length ({len(data['discussion_prompts'])})",
            )
        for i, ans in enumerate(data["discussion_answers"], start=1):
            if not isinstance(ans, str) or len(ans) < 20:
                raise ValidationError(path, f"discussion_answers #{i} too short or not a string")


def validate_library(path: Path) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValidationError(path, f"invalid JSON: {e}") from None

    required = ["id", "type", "title", "author", "year", "category", "difficulty", "intro", "sections"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValidationError(path, f"missing fields: {missing}")

    if data["type"] not in VALID_LIBRARY_TYPES:
        raise ValidationError(path, f"type {data['type']!r} not in {sorted(VALID_LIBRARY_TYPES)}")
    if data["difficulty"] not in VALID_LAB_DIFFICULTIES:
        raise ValidationError(path, f"difficulty {data['difficulty']!r} not in {sorted(VALID_LAB_DIFFICULTIES)}")

    sections = data["sections"]
    if not isinstance(sections, list) or len(sections) == 0:
        raise ValidationError(path, "sections must be a non-empty list")

    seen_ids: set[str] = set()
    for i, sec in enumerate(sections, start=1):
        for k in ("id", "label", "text"):
            if k not in sec:
                raise ValidationError(path, f"section #{i} missing field {k!r}")
        if sec["id"] in seen_ids:
            raise ValidationError(path, f"section #{i}: duplicate id {sec['id']!r}")
        seen_ids.add(sec["id"])
        text = sec["text"]
        if not isinstance(text, str) or len(text) < 20:
            raise ValidationError(path, f"section #{i} ({sec['id']}) text too short")
        anns = sec.get("annotations", [])
        if not isinstance(anns, list):
            raise ValidationError(path, f"section #{i} annotations must be a list")
        for j, ann in enumerate(anns, start=1):
            for k in ("start", "end", "category", "note"):
                if k not in ann:
                    raise ValidationError(path, f"section {sec['id']} ann #{j} missing field {k!r}")
            if ann["start"] < 0 or ann["end"] > len(text) or ann["start"] >= ann["end"]:
                raise ValidationError(
                    path,
                    f"section {sec['id']} ann #{j} invalid offsets [{ann['start']}, {ann['end']}] (text length {len(text)})",
                )
            if ann["category"] not in VALID_LAB_ANN_CATEGORIES:
                raise ValidationError(
                    path,
                    f"section {sec['id']} ann #{j} category {ann['category']!r} not in {sorted(VALID_LAB_ANN_CATEGORIES)}",
                )
            if not isinstance(ann["note"], str) or len(ann["note"]) < 10:
                raise ValidationError(path, f"section {sec['id']} ann #{j} note too short")

    # Optional discussion answers symmetry.
    if "discussion_answers" in data:
        if len(data["discussion_answers"]) != len(data.get("discussion_prompts", [])):
            raise ValidationError(
                path,
                f"discussion_answers length ({len(data['discussion_answers'])}) "
                f"must match discussion_prompts length ({len(data.get('discussion_prompts', []))})",
            )


def main() -> int:
    if not CONTENT_DIR.exists():
        print(f"FAIL: content directory not found at {CONTENT_DIR}")
        return 2

    errors: list[ValidationError] = []
    lesson_count = 0
    quiz_count = 0
    lab_count = 0
    library_count = 0

    for csv_path in sorted((CONTENT_DIR / "lessons").rglob("*.csv")):
        try:
            validate_lesson(csv_path)
            lesson_count += 1
        except ValidationError as e:
            errors.append(e)

    for csv_path in sorted((CONTENT_DIR / "quizzes").rglob("*.csv")):
        try:
            validate_quiz(csv_path)
            quiz_count += 1
        except ValidationError as e:
            errors.append(e)

    lab_dir = CONTENT_DIR / "lab"
    if lab_dir.exists():
        for json_path in sorted(lab_dir.glob("*.json")):
            try:
                validate_lab(json_path)
                lab_count += 1
            except ValidationError as e:
                errors.append(e)

    library_dir = CONTENT_DIR / "library"
    if library_dir.exists():
        for json_path in sorted(library_dir.glob("*.json")):
            try:
                validate_library(json_path)
                library_count += 1
            except ValidationError as e:
                errors.append(e)

    print(f"Validated {lesson_count} lesson · {quiz_count} quiz · {lab_count} lab · {library_count} library file(s).")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for err in errors:
            print(f"  ✗ {err}")
        return 1
    print("All content valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
