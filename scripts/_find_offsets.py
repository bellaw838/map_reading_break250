#!/usr/bin/env python3
"""Helper to find exact character offsets in library section text."""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LIB = REPO / "content/library/002-adventures-of-sherlock-holmes.json"


def find(section_id: str, needle: str, occurrence: int = 0) -> tuple[int, int]:
    data = json.loads(LIB.read_text(encoding="utf-8"))
    sec = next(s for s in data["sections"] if s["id"] == section_id)
    text = sec["text"]
    start = 0
    for _ in range(occurrence + 1):
        idx = text.find(needle, start)
        if idx == -1:
            raise ValueError(f"Not found (occ={occurrence}): {needle[:80]!r}")
        start = idx + 1
    return idx, idx + len(needle)


if __name__ == "__main__":
    sid, quote = sys.argv[1], sys.argv[2]
    occ = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    s, e = find(sid, quote, occ)
    print(f"{s}:{e}")
