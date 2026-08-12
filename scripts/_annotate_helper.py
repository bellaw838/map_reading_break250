#!/usr/bin/env python3
"""Helper to find offsets and patch library annotations. Annotation content is LLM-authored."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LIB = REPO / "content/library/002-adventures-of-sherlock-holmes.json"


def find_span(text: str, snippet: str, start_from: int = 0) -> tuple[int, int]:
    idx = text.find(snippet, start_from)
    if idx == -1:
        raise ValueError(f"Snippet not found: {snippet[:80]!r}...")
    return idx, idx + len(snippet)


def make_ann(text: str, snippet: str, category: str, note: str, start_from: int = 0) -> dict:
    start, end = find_span(text, snippet, start_from)
    return {"start": start, "end": end, "category": category, "note": note}


def patch_section(section_id: str, annotations: list[dict]) -> None:
    data = json.loads(LIB.read_text(encoding="utf-8"))
    for sec in data["sections"]:
        if sec["id"] == section_id:
            # verify sorted
            for a in annotations:
                assert a["start"] < a["end"]
            annotations.sort(key=lambda x: x["start"])
            sec["annotations"] = annotations
            LIB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Patched {section_id}: {len(annotations)} annotations")
            return
    raise KeyError(section_id)


if __name__ == "__main__":
    print("Import and use patch_section()")
