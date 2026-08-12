#!/usr/bin/env python3
"""Parse The Moonstone into a Reading Library JSON.

Source: /tmp/moonstone-raw.txt (PG eBook #155)
Output: content/library/003-moonstone.json

The Moonstone uses a multi-narrator structure (eight narratives + prologue +
epilogue). The narrator-voice shifts ARE the teaching value. We preserve
the structure by tagging each chapter with the narrator name in the label.

Sparse annotations focus on narrator-voice shifts and the famous moments.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_DIR = REPO_ROOT / "content" / "library"
RAW_PATH = Path("/tmp/moonstone-raw.txt")

SMART_QUOTES = {
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u2013": "-",
}


def normalize(text: str) -> str:
    out = text
    for k, v in SMART_QUOTES.items():
        out = out.replace(k, v)
    return out


def find_substring(passage: str, sub: str, occurrence: int = 1) -> tuple[int, int]:
    pos = -1
    for _ in range(occurrence):
        pos = passage.find(sub, pos + 1)
        if pos == -1:
            raise ValueError(f"not found: {sub!r}")
    return pos, pos + len(sub)


# Each narrative gets a slug + display name. Some narratives are short
# enough that we keep them as a single section (no chapter split).
# The First Period is one long Betteredge narrative split by chapter.
NARRATIVES = [
    # (slug, display_name, group_header_in_raw, split_by_chapter)
    ("betteredge",  "Betteredge",            "FIRST PERIOD",        True),
    ("clack",       "Miss Clack",            "FIRST NARRATIVE",     True),
    ("bruff",       "Mr Bruff",              "SECOND NARRATIVE",    True),
    ("blake",       "Franklin Blake",        "THIRD NARRATIVE",     True),
    ("jennings",    "Ezra Jennings",         "FOURTH NARRATIVE",    True),
    ("blake-2",     "Franklin Blake",        "FIFTH NARRATIVE",     False),
    ("cuff",        "Sergeant Cuff",         "SIXTH NARRATIVE",     False),
    ("candy",       "Mr Candy",              "SEVENTH NARRATIVE",   False),
    ("betteredge-2","Betteredge",            "EIGHTH NARRATIVE",    False),
]


def find_nth(raw: str, needle: str, n: int = 2) -> int:
    """Return position of n-th occurrence (1-indexed). Used to skip the TOC."""
    pos = -1
    for _ in range(n):
        pos = raw.find(needle, pos + 1)
        if pos < 0:
            return -1
    return pos


def parse(raw: str) -> list[dict]:
    sections: list[dict] = []

    # ── Prologue (body — the SECOND occurrence; the first is the TOC) ─
    prologue_start = find_nth(raw, "PROLOGUE", 2)
    prologue_end   = find_nth(raw, "FIRST PERIOD", 2)
    if prologue_start < 0 or prologue_end < 0:
        raise RuntimeError("prologue boundaries not found")
    # advance past the literal "PROLOGUE\n" header
    nl = raw.find("\n", prologue_start)
    prologue_start = nl + 1
    prologue_text = raw[prologue_start:prologue_end].strip()
    prologue_text = re.sub(r"\n{3,}", "\n\n", prologue_text)
    sections.append({
        "id": "prologue",
        "label": "Prologue",
        "subtitle": "The Storming of Seringapatam (1799) — extracted from a family paper",
        "text": prologue_text,
    })

    # ── Narratives ────────────────────────────────────────────────────
    # Start the cursor BEFORE prologue_end so the first narrative ("FIRST
    # PERIOD") boundary matches the body header at prologue_end itself.
    boundaries = []
    cursor = prologue_start  # search forward from the prologue body
    for slug, name, header, split in NARRATIVES:
        idx_a = raw.find("\n" + header + "\n", cursor)
        idx_b = raw.find("\n" + header + ".\n", cursor)
        candidates = [i for i in (idx_a, idx_b) if i >= 0]
        if not candidates:
            raise RuntimeError(f"narrative header not found from cursor {cursor}: {header}")
        idx = min(candidates)
        boundaries.append((idx, slug, name, split))
        cursor = idx + 1

    epilogue_pos = raw.find("EPILOGUE.", cursor)
    if epilogue_pos < 0:
        epilogue_pos = raw.find("EPILOGUE", cursor)
    boundaries.append((epilogue_pos, None, None, None))

    chap_re = re.compile(r"^CHAPTER ([IVX]+)\.?$")

    for i in range(len(boundaries) - 1):
        start, slug, name, split = boundaries[i]
        end   = boundaries[i + 1][0]
        block = raw[start:end]

        # Skip past the header line itself.
        block = block.split("\n", 2)[2] if "\n" in block else block

        if not split:
            # Whole narrative as one section.
            txt = re.sub(r"\n{3,}", "\n\n", block).strip()
            sections.append({
                "id": slug,
                "label": f"{name} narrates",
                "subtitle": "",
                "text": txt,
            })
            continue

        # Split into chapters.
        lines = block.split("\n")
        cur_chap = None
        cur_buf: list[str] = []

        def flush():
            nonlocal cur_chap, cur_buf
            if cur_chap is None:
                return
            txt = re.sub(r"\n{3,}", "\n\n", "\n".join(cur_buf)).strip()
            if len(txt) < 20:
                cur_chap = None
                cur_buf = []
                return
            sections.append({
                "id": f"{slug}-ch-{cur_chap.lower()}",
                "label": f"{name} — Chapter {cur_chap}",
                "subtitle": "",
                "text": txt,
            })
            cur_chap = None
            cur_buf = []

        for line in lines:
            m = chap_re.match(line.strip())
            if m:
                flush()
                cur_chap = m.group(1)
                continue
            if cur_chap is not None:
                cur_buf.append(line)
        flush()

    # ── Epilogue ──────────────────────────────────────────────────────
    epilogue_text = raw[epilogue_pos:].split("\n", 1)[1]
    # Strip end-of-book marker.
    epilogue_text = re.split(r"\*\*\* END OF", epilogue_text)[0]
    epilogue_text = re.sub(r"\n{3,}", "\n\n", epilogue_text).strip()
    sections.append({
        "id": "epilogue",
        "label": "Epilogue",
        "subtitle": "The Finding of the Diamond",
        "text": epilogue_text,
    })

    return sections


# Sparse annotations on narrator-voice shifts + famous moments.
ANNOTATIONS_BY_SECTION: dict[str, list[dict]] = {

    "prologue": [
        {
            "sub": "I address these lines—written in India—to my relatives in England.",
            "category": "structure",
            "note": "STR: the Prologue opens with a letter from a soldier — explaining why he has CUT OFF his cousin John Herncastle. Collins sets the whole novel inside a moral indictment: Herncastle stole the diamond, and the family knows.",
        },
        {
            "sub": "THE STORMING OF SERINGAPATAM",
            "category": "structure",
            "note": "STR: the historical anchor. The diamond is taken during a real 1799 British siege of an Indian fortress. Collins ties the family-mystery to colonial violence — the diamond's curse is also a moral debt.",
        },
    ],

    "betteredge-ch-i": [
        {
            "sub": "Robinson Crusoe",
            "category": "tone",
            "note": "TO: Betteredge opens by quoting Robinson Crusoe — and treats Defoe's novel as a sacred oracle throughout. His voice (servant, faithful, mildly comic) is established in line one. Watch this voice change when the next narrator takes over.",
            "occurrence": 1,
        },
    ],

    "clack-ch-i": [
        {
            "sub": "I am indebted to my dear parents",
            "category": "structure",
            "note": "STR/narrator shift: Miss Clack's narrative begins. Compare her voice to Betteredge's. He was warm, plain, faithful. She is sanctimonious, judgmental, comic in her self-righteousness. Same diamond, totally different narrator — the novel's whole pedagogy.",
        },
    ],

    "bruff-ch-i": [
        {
            "sub": "My fair friend, Miss Clack, having laid down the pen",
            "category": "structure",
            "note": "STR/narrator shift: Mr Bruff (a lawyer) takes over from Miss Clack. The transition itself is the lesson — he REFERS to her by name as he picks up the story. The narrators are aware of each other.",
        },
    ],

    "blake-ch-i": [
        {
            "sub": "In the spring of the year eighteen hundred and forty-nine",
            "category": "structure",
            "note": "STR/narrator shift: Franklin Blake — protagonist + investigator + (it turns out) suspect. His narration opens with a date and a journey, the mark of a memoirist. More intimate than the previous narrators.",
        },
    ],

    "jennings-ch-i": [
        {
            "sub": "June 15th",
            "category": "structure",
            "note": "STR/narrator shift: Ezra Jennings — the outsider, the dying doctor's assistant. His narrative is a DIARY, dated by day. Collins gives the key insight (the opium hypothesis) to the character society would dismiss. Note the FORM change too — diary instead of memoir.",
            "occurrence": 1,
        },
    ],

    "betteredge-ch-iv": [
        {
            "sub": "Shivering Sand",
            "category": "structure",
            "note": "STR: the Shivering Sand — a literal quicksand near the house — becomes a recurring symbol. Whatever falls into it cannot be recovered. Collins plants this image early; it pays off later when a body and the secret it carries both go into the sand.",
        },
    ],

    "betteredge-ch-x": [
        {
            "sub": "_Robinson Crusoe_",
            "category": "tone",
            "note": "TO: Betteredge consults Robinson Crusoe again — his oracle. The recurring habit is a character marker: he treats Defoe's novel as a sacred text. Watch how often the book appears in his narrative; it's almost a verbal tic.",
        },
    ],

    "blake-ch-iv": [
        {
            "sub": "of having taken the Diamond",
            "category": "structure",
            "note": "STR: the great structural reveal. The investigator IS the thief. Collins designed this move 50 years before Christie used it in Roger Ackroyd — and it works for the same reason: the narrator we trust is the one we should suspect.",
        },
    ],

    "blake-ch-ix": [
        {
            "sub": "opium",
            "category": "evidence",
            "note": "E: opium is named as the key piece of evidence. The hypothesis is that Blake took the diamond under the influence of opium given by Dr Candy. The case requires this marginal knowledge — an unfashionable drug — to be solved.",
            "occurrence": 1,
        },
    ],

    "epilogue": [
        {
            "sub": "THE FINDING OF THE DIAMOND",
            "category": "theme",
            "note": "TH: the diamond is found — back in India, at the shrine. The Epilogue answers the Prologue: same place, same priests' line of duty. The novel is the loop between these two moments. Where it BEGAN is where it ENDS.",
        },
    ],
}


DISCUSSION = [
    {
        "prompt": "Collins gives the same story to multiple narrators (Betteredge, Miss Clack, Bruff, Blake, Jennings). Pick any two and describe how their voices differ. What does Collins gain by switching?",
        "answer": "Betteredge: warm, plain, comic, devoted. Miss Clack: sanctimonious, judgmental, hilariously blind to her own pettiness. Switching narrators forces the reader to weigh BIAS — every account is partial, and the truth assembles only when the accounts overlap. This is the novel's pedagogical move: trust no single perspective.",
    },
    {
        "prompt": "The Prologue (Seringapatam, 1799) and the Epilogue (the diamond returns to India) frame the whole book. What does Collins claim by structuring it this way?",
        "answer": "The diamond's place in India is not just a curse — it is its proper home. The English have been holding what was never theirs. The frame puts the entire English plot in moral parentheses: 'this is what happens when a stolen sacred object is dragged into a quiet country house.'",
    },
    {
        "prompt": "Miss Clack's narrative is comic on purpose. Find a moment where her self-righteousness reveals something she does NOT see about herself.",
        "answer": "Many candidates — most of her interactions with Rachel and Lady Verinder include her distributing religious tracts that no one wants. Miss Clack believes she is being charitable; the reader sees she is being a nuisance. Collins uses her blindness to teach the reader to read NARRATORS skeptically.",
    },
    {
        "prompt": "Ezra Jennings is dying, mixed-race, working-class, and ostracized. Why does Collins give him the breakthrough insight (the opium hypothesis)?",
        "answer": "Because the truth comes from the outside, not the center. The respectable English narrators (Bruff, Blake, even Betteredge) cannot solve the case. Jennings — who has nothing to lose and who reads detail without prejudice — can. Collins is making a quiet argument: the marginalised observer sees most clearly.",
    },
    {
        "prompt": "The Moonstone is often called 'the first detective novel.' What detective-genre moves does Collins invent that we still see today (in Christie, Holmes, etc.)?",
        "answer": "(1) Closed-circle suspect list. (2) The amateur sleuth + professional detective contrast (Sergeant Cuff). (3) Misdirection via narrator perspective. (4) The 'gather the suspects and reveal' set-piece. (5) Plot-twist where the protagonist himself is implicated. Every Christie and Conan Doyle is using furniture Collins built.",
    },
]


def main() -> int:
    if not RAW_PATH.exists():
        print(f"FAIL: {RAW_PATH} not found.")
        return 2

    raw = normalize(RAW_PATH.read_text(encoding="utf-8"))
    sections = parse(raw)
    print(f"Parsed {len(sections)} sections.")

    total_anns_attached = 0
    for sec in sections:
        sec_anns = ANNOTATIONS_BY_SECTION.get(sec["id"], [])
        out_anns = []
        for spec in sec_anns:
            try:
                start, end = find_substring(sec["text"], spec["sub"], spec.get("occurrence", 1))
            except ValueError as e:
                print(f"  ! {sec['id']}: annotation skip ({e})")
                continue
            out_anns.append({
                "start": start, "end": end,
                "category": spec["category"], "note": spec["note"],
            })
        sec["annotations"] = out_anns
        total_anns_attached += len(out_anns)

    annotated = sum(1 for s in sections if s["annotations"])
    print(f"Annotated {annotated}/{len(sections)} sections with {total_anns_attached} total annotations.")

    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    out = {
        "id": "library-003-moonstone",
        "type": "novel",
        "title": "The Moonstone",
        "author": "Wilkie Collins",
        "year": 1868,
        "source_url": "https://www.gutenberg.org/ebooks/155",
        "category": "Detective Fiction",
        "difficulty": "Hard",
        "length_words": sum(len(s["text"].split()) for s in sections),
        "intro": (
            "The first detective novel. A sacred Indian diamond is stolen at "
            "a country-house birthday party — and the story is told by EIGHT "
            "different narrators in turn (a faithful steward, a sanctimonious "
            "cousin, a lawyer, the suspect himself, an outcast doctor's assistant…). "
            "The narrator-voice shifts are the whole pedagogical point. Marking "
            "annotations are placed at each shift so you can compare voices. "
            "Read slowly — this is a long book."
        ),
        "sections": sections,
        "discussion_prompts": [d["prompt"] for d in DISCUSSION],
        "discussion_answers": [d["answer"] for d in DISCUSSION],
    }

    out_path = LIBRARY_DIR / "003-moonstone.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  ✓ {out_path.relative_to(REPO_ROOT)} ({out['length_words']:,} words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
