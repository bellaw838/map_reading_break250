#!/usr/bin/env python3
"""Parse The Adventures of Sherlock Holmes into a Reading Library JSON.

Source: /tmp/sherlock-raw.txt (PG eBook #1661)
Output: content/library/002-adventures-of-sherlock-holmes.json

12 stories, each combining all of its inner sub-sections (I, II, III) into a
single section. Sparse annotations on Holmes's most famous deductions.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_DIR = REPO_ROOT / "content" / "library"
RAW_PATH = Path("/tmp/sherlock-raw.txt")

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


# Roman numeral story headers, in order.
STORY_HEADERS = [
    ("I. A SCANDAL IN BOHEMIA",                      "scandal-in-bohemia",         "A Scandal in Bohemia"),
    ("II. THE RED-HEADED LEAGUE",                    "red-headed-league",          "The Red-Headed League"),
    ("III. A CASE OF IDENTITY",                      "case-of-identity",           "A Case of Identity"),
    ("IV. THE BOSCOMBE VALLEY MYSTERY",              "boscombe-valley-mystery",    "The Boscombe Valley Mystery"),
    ("V. THE FIVE ORANGE PIPS",                      "five-orange-pips",           "The Five Orange Pips"),
    ("VI. THE MAN WITH THE TWISTED LIP",             "man-with-the-twisted-lip",   "The Man with the Twisted Lip"),
    ("VII. THE ADVENTURE OF THE BLUE CARBUNCLE",     "blue-carbuncle",             "The Adventure of the Blue Carbuncle"),
    ("VIII. THE ADVENTURE OF THE SPECKLED BAND",     "speckled-band",              "The Adventure of the Speckled Band"),
    ("IX. THE ADVENTURE OF THE ENGINEER'S THUMB",    "engineers-thumb",            "The Adventure of the Engineer's Thumb"),
    ("X. THE ADVENTURE OF THE NOBLE BACHELOR",       "noble-bachelor",             "The Adventure of the Noble Bachelor"),
    ("XI. THE ADVENTURE OF THE BERYL CORONET",       "beryl-coronet",              "The Adventure of the Beryl Coronet"),
    ("XII. THE ADVENTURE OF THE COPPER BEECHES",     "copper-beeches",             "The Adventure of the Copper Beeches"),
]

END_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK"


def split_stories(raw: str) -> list[dict]:
    """Locate each story's text by header. Use the SECOND occurrence of each
    header (the first occurrence is the TOC entry)."""
    sections: list[dict] = []
    # Find end of book.
    end_idx = raw.find(END_MARKER)
    if end_idx < 0:
        end_idx = len(raw)

    # Find each header occurrence (skip the TOC, which is the first occurrence).
    starts = []
    for header, slug, title in STORY_HEADERS:
        # The TOC and the story heading both have the same text. Find both
        # occurrences and take the second one (the body header).
        first = raw.find(header)
        if first < 0:
            raise RuntimeError(f"header not found: {header}")
        body = raw.find(header, first + 1)
        if body < 0:
            # Some stories may only appear once (no separate TOC). Use first.
            body = first
        starts.append((body, slug, title))

    # Add an end-of-book sentinel.
    starts.append((end_idx, None, None))

    for i in range(len(starts) - 1):
        body_start, slug, title = starts[i]
        body_end = starts[i + 1][0]
        # Skip past the header line itself
        header_end = raw.find("\n", body_start)
        text = raw[header_end + 1 : body_end]
        # Trim leading/trailing blanks; collapse 3+ blanks to 2.
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        sections.append({
            "id": slug,
            "label": title,
            "subtitle": f"Story {i + 1} of 12",
            "text": text,
        })
    return sections


# ─────────────────────────────────────────────────────────────────────
# Sparse annotations — only the most famous deductive moments.
# ─────────────────────────────────────────────────────────────────────
ANNOTATIONS_BY_STORY: dict[str, list[dict]] = {

    "scandal-in-bohemia": [
        {
            "sub": "To Sherlock Holmes she is always _the_ woman.",
            "category": "structure",
            "note": "STR: the first line of the first story. The collection opens by naming Irene Adler as the one person who matters to Holmes — before we ever meet her. Watson is framing what the case will mean.",
        },
        {
            "sub": "You see, but you do not observe.",
            "category": "theme",
            "note": "TH: Holmes's central teaching, stated explicitly. The whole series is built on the difference between SEEING and OBSERVING. Every deduction below is an example of this distinction.",
        },
        {
            "sub": "It is a capital mistake to theorise before one has",
            "category": "theme",
            "note": "TH: Holmes's method, stated as a rule — never form a theory before you have facts. Compare this to the Hat deduction in 'Blue Carbuncle' (where every conclusion has a physical anchor) — Doyle is teaching the rule and then demonstrating it.",
        },
        {
            "sub": "It is quite a pretty little problem,",
            "category": "tone",
            "note": "TO: Holmes's voice when an interesting case lands — 'pretty little problem.' He treats crimes as puzzles, not as moral horrors. The detached, almost cheerful tone runs across all twelve stories.",
        },
    ],

    "red-headed-league": [
        {
            "sub": "It is quite a three pipe problem,",
            "category": "tone",
            "note": "TO: Holmes measures problem difficulty in PIPES — a small, specific unit of his own. The detail establishes Holmes's interior life: when a case stumps him, he sits and smokes. The reader gets a glimpse of his working method.",
        },
        {
            "sub": "the smaller crimes",
            "category": "theme",
            "note": "TH: in this story Holmes notes that the LARGER crimes are often more transparent than the SMALL ones. Counter-intuitive — and a teaching move. The Red-Headed League is a giant, baroque setup that turns out to be cover for a tiny crime (a tunnel).",
        },
    ],

    "case-of-identity": [
        {
            "sub": "Perhaps I have trained myself to see what others overlook.",
            "category": "evidence",
            "note": "E: Holmes's claim about HOW his method works — observation is trainable. Doyle is telling readers that the deduction tricks are repeatable, not magical.",
        },
        {
            "sub": "I have every reason to believe\nthat I will succeed",
            "category": "inference",
            "note": "INF: Holmes's confident claim BEFORE he reveals his reasoning. The reader is left to infer what 'reason to believe' means — the answer is buried in clues Holmes has already collected but not yet named.",
        },
        {
            "sub": "rather elementary,",
            "category": "tone",
            "note": "TO: the famous 'elementary' line in its original form. Doyle does NOT have Holmes say 'elementary, my dear Watson' (a later catchphrase). Here it's a passing aside — Holmes dismissing his own genius. The understatement IS the character.",
        },
    ],

    "boscombe-valley-mystery": [
        {
            "sub": "There is nothing more deceptive than an obvious fact,",
            "category": "theme",
            "note": "TH: another of Holmes's named methods — a fact that looks obvious is often the most misleading. Trains the reader to be suspicious of easy conclusions.",
        },
    ],

    "five-orange-pips": [
        {
            "sub": "K. K. K.",
            "category": "evidence",
            "note": "E: the cryptic letters on the envelope. Holmes treats these three characters as concrete evidence — naming the Ku Klux Klan — long before the narrative spells it out. Demonstrates evidence-first reasoning.",
        },
        {
            "sub": "Hudson",
            "category": "inference",
            "note": "INF: the name 'Hudson' appears in the diary. The reader is invited to track recurring names across the story — names ARE clues in Holmes stories, treated as evidence. Doyle is training the habit of taking proper nouns seriously.",
            "occurrence": 1,
        },
    ],

    "blue-carbuncle": [
        {
            "sub": "On the contrary, Watson, you can see everything. You fail, however, to",
            "category": "theme",
            "note": "TH: the see-vs-observe lesson restated. Watson sees the same hat — but draws no conclusions from it. The pleasure is watching Holmes turn what Watson sees into what Watson MISSED.",
        },
    ],

    "blue-carbuncle": [
        {
            "sub": "He is a man who leads a sedentary life,\ngoes out little, is out of training entirely, is middle-aged",
            "category": "inference",
            "note": "INF: a famous deduction chain — from one battered hat Holmes infers lifestyle, age, grooming, even gas supply at home. Doyle is showing the reasoning, not just the conclusion. This is the most-cited example of the 'see vs. observe' method.",
        },
        {
            "sub": "These are the more patent facts which are\nto be deduced from his hat.",
            "category": "evidence",
            "note": "E: Holmes naming the hat itself as evidence. 'Patent facts' = facts visible to anyone — but only Holmes has collected them. The hat is treated like a witness.",
        },
    ],

    "speckled-band": [
        {
            "sub": "When a doctor does go wrong he is\nthe first of criminals.",
            "category": "tone",
            "note": "TO/inference: Holmes's general claim about Dr. Roylott. The tone is matter-of-fact, even admiring of the criminal's intelligence. Holmes never moralizes; he assesses.",
        },
        {
            "sub": "It is fear, Mr. Holmes. It is terror.",
            "category": "tone",
            "note": "TO: Helen Stoner naming her own emotional state. The whole story's atmosphere is built on this admission — fear comes before any of the evidence does.",
        },
        {
            "sub": "speckled band",
            "category": "evidence",
            "note": "E: the dying sister's last words. Holmes treats these two words as a literal physical clue — a band that is speckled. Most readers (and Watson) interpret 'band' as 'gang.' Doyle's whole story turns on the wrong reading vs the right one.",
            "occurrence": 1,
        },
    ],


    "copper-beeches": [
        {
            "sub": "Data! data!\ndata!",
            "category": "theme",
            "note": "TH: Holmes again on method — you cannot reason without data. The triple repetition makes the claim land. The story will demonstrate what happens when you reason in the absence of facts.",
        },
        {
            "sub": "I can't make bricks without clay.",
            "category": "tone",
            "note": "FIG/TO: the working metaphor. Holmes treats deduction as a craft requiring raw materials. The tone is practical, almost humble.",
        },
        {
            "sub": "Crime is common. Logic is rare.",
            "category": "theme",
            "note": "TH: Holmes contrasts the EVENT (crime, common) with the METHOD (logic, rare). He's claiming that what makes him valuable isn't access to crime but skill in reasoning. The story tests whether his logic can save a young woman from danger.",
        },
    ],
}


DISCUSSION = [
    {
        "prompt": "Holmes says 'You see, but you do not observe' in 'A Scandal in Bohemia.' Find a moment in any story where the difference between SEEING and OBSERVING is acted out. What does Holmes notice that Watson misses?",
        "answer": "Many candidates — the hat in 'Blue Carbuncle' is a classic example. Watson SEES a battered hat; Holmes OBSERVES greasiness (sedentary), inner band wear (decline), residue (specific habits). Any story works for this; the point is to identify a moment where physical detail becomes evidence.",
    },
    {
        "prompt": "Doyle invented the modern detective story formula: small detail → big inference → reveal. Pick one story and mark the three stages.",
        "answer": "Strong choice: 'Speckled Band.' Detail = the bell-pull that doesn't ring + ventilator that doesn't ventilate. Inference = something travels DOWN the bell-rope to the bed. Reveal = the snake. The structure is repeatable across all 12 stories.",
    },
    {
        "prompt": "Watson is the narrator, not Holmes. What does this do for the storytelling? What would change if Holmes told the stories himself?",
        "answer": "Watson lets the reader stay one step behind Holmes — we see the same evidence but don't draw the conclusion. If Holmes narrated, the reader would either see every connection instantly (no suspense) or be lectured at. Watson's mind sits between Holmes and the reader, as a buffer.",
    },
    {
        "prompt": "Holmes makes false starts and changes his mind. Find one. Why does Doyle include them?",
        "answer": "Examples: in 'Red-Headed League' Holmes doesn't immediately know the meaning of the league; in 'Boscombe Valley' he weighs multiple suspects. The false starts make Holmes feel real, not magical. They also model how good reasoning actually works — hypothesize, test, revise.",
    },
    {
        "prompt": "Compare the OPENING of any two stories. What stays the same in Doyle's formula? What varies?",
        "answer": "Constant: Watson at 221B, weather/atmosphere detail, client arrives with strange problem. Variable: client type (royal, working-class, woman in fear, businessman), Holmes's initial reaction (eager / lazy / bored / sharp). Doyle reuses the frame but recolors the people inside it.",
    },
]


def main() -> int:
    if not RAW_PATH.exists():
        print(f"FAIL: {RAW_PATH} not found.")
        return 2

    raw = normalize(RAW_PATH.read_text(encoding="utf-8"))
    sections = split_stories(raw)
    print(f"Parsed {len(sections)} stories.")
    for s in sections:
        print(f"  {s['label']:42} {len(s['text']):>6} chars / {len(s['text'].split()):>5} words")

    # Apply annotations.
    for sec in sections:
        sec_anns = ANNOTATIONS_BY_STORY.get(sec["id"], [])
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

    total_anns = sum(len(s["annotations"]) for s in sections)
    annotated = sum(1 for s in sections if s["annotations"])
    print(f"Annotated {annotated}/{len(sections)} stories with {total_anns} total annotations.")

    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    out = {
        "id": "library-002-sherlock",
        "type": "story-collection",
        "title": "The Adventures of Sherlock Holmes",
        "author": "Arthur Conan Doyle",
        "year": 1892,
        "source_url": "https://www.gutenberg.org/ebooks/1661",
        "category": "Detective Fiction",
        "difficulty": "Medium",
        "length_words": sum(len(s["text"].split()) for s in sections),
        "intro": (
            "Twelve self-contained short stories. Each is a small puzzle solved through "
            "observation. Watch how Doyle's formula works — small detail, large inference, "
            "the reveal — and how the same shape can produce a dozen different stories. "
            "Read one per sitting; you don't need to read in order."
        ),
        "sections": sections,
        "discussion_prompts": [d["prompt"] for d in DISCUSSION],
        "discussion_answers": [d["answer"] for d in DISCUSSION],
    }

    out_path = LIBRARY_DIR / "002-adventures-of-sherlock-holmes.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  ✓ {out_path.relative_to(REPO_ROOT)} ({out['length_words']:,} words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
