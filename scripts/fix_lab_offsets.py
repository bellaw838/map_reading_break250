#!/usr/bin/env python3
"""Recompute annotation offsets for hand-counted lab files.

The first batch of lab JSON (001, 007, 008, etc.) was authored by counting
character offsets by hand. Several offsets are wrong:
  - Sonnet 18: 'But' volta marked as [366,372] = 'l summ' (wrong word entirely)
  - Sonnet 18: theme line [41,79] missing leading 'T' from 'Thou'
  - Tomorrow soliloquy: opening [0,33] cropped to 'Tomorrow, and tomorrow, and tomor'
  - Tomorrow soliloquy: theme [84,118] missing 'To ' prefix

For each annotation that has a wrong offset, we re-anchor it by intended
substring (the substring is encoded in the original note's quoted phrase or
named explicitly here). All other annotations are left alone.

Run from repo root:
    python3 scripts/fix_lab_offsets.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LAB_DIR = REPO_ROOT / "content" / "lab"


def find_substring(passage: str, sub: str, occurrence: int = 1) -> tuple[int, int]:
    pos = -1
    for _ in range(occurrence):
        pos = passage.find(sub, pos + 1)
        if pos == -1:
            raise ValueError(f"not found: {sub!r} (occurrence {occurrence})")
    return pos, pos + len(sub)


# Per-file corrections. Each entry is a list of (annotation_index, intended_substring, occurrence?)
# The intended_substring is what the note SAYS the annotation marks.
# annotation_index is 0-based; we identify the annotation to fix by its category + start offset
# combination, but for simplicity here we just replace by ordinal position in the array.
FIXES: dict[str, list[dict]] = {

    # ─── 001 Sonnet 18 ───────────────────────────────────────────────
    "001-sonnet-18.json": [
        # ann 0: opening question
        {"i": 0, "sub": "Shall I compare thee to a summer's day?"},
        # ann 1: the answer 'Thou art more lovely and more temperate' (the colon is part of the line)
        {"i": 1, "sub": "Thou art more lovely and more temperate:"},
        # ann 2: lines 3-8 — summer's flaws. Starts at "Rough winds" through "untrimm'd;"
        {"i": 2, "sub": "Rough winds do shake the darling buds of May,\nAnd summer's lease hath all too short a date:\nSometime too hot the eye of heaven shines,\nAnd often is his gold complexion dimm'd;\nAnd every fair from fair sometime declines,\nBy chance, or nature's changing course, untrimm'd;"},
        # ann 3: the volta — just the word 'But'
        {"i": 3, "sub": "But"},
        # ann 4: 'thy eternal summer shall not fade…' through 'thou grow'st'
        {"i": 4, "sub": "thy eternal summer shall not fade,\nNor lose possession of that fair thou ow'st;\nNor shall Death brag thou wander'st in his shade,\nWhen in eternal lines to time thou grow'st;"},
        # ann 5: the final couplet
        {"i": 5, "sub": "  So long as men can breathe, or eyes can see,\n  So long lives this, and this gives life to thee."},
        # ann 6: 'eternal lines' phrase
        {"i": 6, "sub": "eternal lines"},
    ],

    # ─── 008 Tomorrow, and tomorrow, and tomorrow ────────────────────
    "008-tomorrow-and-tomorrow.json": [
        # ann 0: opening anaphora — needs to include the full third 'tomorrow,'
        {"i": 0, "sub": "Tomorrow, and tomorrow, and tomorrow,"},
        # ann 1: 'Creeps in this petty pace from day to day,' — keep comma for full line
        {"i": 1, "sub": "Creeps in this petty pace from day to day,"},
        # ann 2: 'To the last syllable of recorded time' — needs 'To ' prefix
        {"i": 2, "sub": "To the last syllable of recorded time"},
        # ann 3: 'Out, out, brief candle!'
        {"i": 3, "sub": "Out, out, brief candle!"},
        # ann 4: extended metaphor begins
        {"i": 4, "sub": "Life's but a walking shadow, a poor player,"},
        # ann 5: 'That struts and frets his hour upon the stage,'
        {"i": 5, "sub": "That struts and frets his hour upon the stage,"},
        # ann 6: final image — 'a tale Told by an idiot, full of sound and fury, Signifying nothing.'
        {"i": 6, "sub": "It is a tale\nTold by an idiot, full of sound and fury,\nSignifying nothing."},
        # ann 7: 'full of sound and fury'
        {"i": 7, "sub": "full of sound and fury"},
    ],

    # ─── 007 All the world's a stage ─────────────────────────────────
    # These looked mostly correct but a few are slightly off. Re-anchor by exact phrase.
    "007-all-the-worlds-a-stage.json": [
        # ann 0: master metaphor
        {"i": 0, "sub": "All the world's a stage"},
        # ann 1: 'His acts being seven ages'
        {"i": 1, "sub": "His acts being seven ages"},
        # ann 2: infancy
        {"i": 2, "sub": "Mewling and puking in the nurse's arms"},
        # ann 3: schoolboy
        {"i": 3, "sub": "creeping like snail\nUnwillingly to school"},
        # ann 4: lover
        {"i": 4, "sub": "Sighing like furnace, with a woeful ballad"},
        # ann 5: bubble reputation
        {"i": 5, "sub": "Seeking the bubble reputation\nEven in the cannon's mouth"},
        # ann 6: justice
        {"i": 6, "sub": "In fair round belly with good capon lined"},
        # ann 7: old man — clothes that no longer fit
        {"i": 7, "sub": "a world too wide\nFor his shrunk shank"},
        # ann 8: sans, sans, sans, sans
        {"i": 8, "sub": "Sans teeth, sans eyes, sans taste, sans everything."},
    ],

    # ─── 002 Gettysburg Address (offsets looked fine; re-anchor to be safe) ───
    "002-gettysburg-address.json": [
        # ann 0: PAST — opening paragraph
        {"i": 0, "sub": "Four score and seven years ago our fathers brought forth, on this continent, a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal."},
        # ann 1: 'all men are created equal' — the founding proposition phrase
        {"i": 1, "sub": "dedicated to the proposition that all men are created equal."},
        # ann 2: PRESENT block — second paragraph
        {"i": 2, "sub": "Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived, and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives, that that nation might live. It is altogether fitting and proper that we should do this."},
        # ann 3: 'we can not dedicate — we can not consecrate — we can not hallow'
        {"i": 3, "sub": "we can not dedicate — we can not consecrate — we can not hallow — this ground."},
        # ann 4: 'The brave men…'
        {"i": 4, "sub": "The brave men, living and dead, who struggled here, have consecrated it far above our poor power to add or detract."},
        # ann 5: FUTURE — 'It is for us the living…'
        {"i": 5, "sub": "It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced."},
        # ann 6: closing theme — 'that government of the people…'
        {"i": 6, "sub": "that this nation, under God, shall have a new birth of freedom — and that government of the people, by the people, for the people, shall not perish from the earth."},
        # ann 7: 'of the people, by the people, for the people'
        {"i": 7, "sub": "of the people, by the people, for the people"},
    ],

    # ─── 003 Walden ──────────────────────────────────────────────────
    "003-walden-i-went-to-the-woods.json": [
        # ann 0: thesis sentence
        {"i": 0, "sub": "I went to the woods because I wished to live deliberately, to front only the essential facts of life, and see if I could not learn what it had to teach, and not, when I came to die, discover that I had not lived."},
        # ann 1: 'deliberately'
        {"i": 1, "sub": "deliberately"},
        # ann 2: 'the essential facts of life'
        {"i": 2, "sub": "the essential facts of life"},
        # ann 3: 'I did not wish to live what was not life…' (the resignation sentence)
        {"i": 3, "sub": "I did not wish to live what was not life, living is so dear; nor did I wish to practise resignation, unless it was quite necessary."},
        # ann 4: 'resignation'
        {"i": 4, "sub": "resignation"},
        # ann 5: stacked metaphors of intensity — long sentence about marrow
        {"i": 5, "sub": "I wanted to live deep and suck out all the marrow of life, to live so sturdily and Spartan-like as to put to rout all that was not life, to cut a broad swath and shave close, to drive life into a corner, and reduce it to its lowest terms,"},
        # ann 6: 'if it proved to be mean, why then to get the whole and genuine meanness of it…or if it were sublime, to know it by experience.'
        {"i": 6, "sub": "if it proved to be mean, why then to get the whole and genuine meanness of it, and publish its meanness to the world; or if it were sublime, to know it by experience."},
        # ann 7: same phrase (deeper claim — theme)
        {"i": 7, "sub": "if it proved to be mean, why then to get the whole and genuine meanness of it, and publish its meanness to the world; or if it were sublime, to know it by experience."},
    ],

    # ─── 004 Huck Finn opening ───────────────────────────────────────
    "004-huck-finn-opening.json": [
        {"i": 0, "sub": "You don't know about me without you have read a book by the name of The Adventures of Tom Sawyer; but that ain't no matter."},
        {"i": 1, "sub": "You don't know about me without you have read"},
        {"i": 2, "sub": "That book was made by Mr. Mark Twain, and he told the truth, mainly."},
        {"i": 3, "sub": "There was things which he stretched, but mainly he told the truth."},
        {"i": 4, "sub": "I never seen anybody but lied one time or another, without it was Aunt Polly, or the widow, or maybe Mary."},
        {"i": 5, "sub": "or maybe Mary"},
        {"i": 6, "sub": "which is mostly a true book, with some stretchers, as I said before."},
    ],

    # ─── 005 Gift of the Magi opening ────────────────────────────────
    "005-gift-of-the-magi-opening.json": [
        {"i": 0, "sub": "One dollar and eighty-seven cents. That was all. And sixty cents of it was in pennies."},
        {"i": 1, "sub": "Pennies saved one and two at a time by bulldozing the grocer and the vegetable man and the butcher until one's cheeks burned with the silent imputation of parsimony that such close dealing implied."},
        {"i": 2, "sub": "cheeks burned with the silent imputation of parsimony"},
        {"i": 3, "sub": "Three times Della counted it."},
        {"i": 4, "sub": "One dollar and eighty-seven cents. And the next day would be Christmas.", "occurrence": 1},
        {"i": 5, "sub": "There was clearly nothing left to do but flop down on the shabby little couch and howl."},
        {"i": 6, "sub": "life is made up of sobs, sniffles, and smiles, with sniffles predominating."},
        {"i": 7, "sub": "A furnished flat at $8 per week. It did not exactly beggar description, but it certainly had that word on the lookout for the mendicancy squad."},
    ],

    # ─── 006 Boy Who Cried Wolf ──────────────────────────────────────
    "006-boy-who-cried-wolf.json": [
        {"i": 0, "sub": "A SHEPHERD-BOY, who watched a flock of sheep near a village, brought out the villagers three or four times by crying out, \"Wolf! Wolf!\" and when his neighbors came to help him, laughed at them for their pains."},
        {"i": 1, "sub": "laughed at them for their pains"},
        {"i": 2, "sub": "The Wolf, however, did truly come at last."},
        {"i": 3, "sub": "The Shepherd-boy, now really alarmed, shouted in an agony of terror: \"Pray, do come and help me; the Wolf is killing the sheep\""},
        {"i": 4, "sub": "but no one paid any heed to his cries, nor rendered any assistance."},
        {"i": 5, "sub": "The Wolf, having no cause of fear, at his leisure lacerated or destroyed the whole flock."},
        {"i": 6, "sub": "There is no believing a liar, even when he speaks the truth."},
    ],

    # ─── 009 Tale of Two Cities ──────────────────────────────────────
    "009-tale-of-two-cities-opening.json": [
        {"i": 0, "sub": "It was the best of times, it was the worst of times,"},
        {"i": 1, "sub": "it was the age of wisdom, it was the age of foolishness,"},
        {"i": 2, "sub": "it was the epoch of belief, it was the epoch of incredulity,"},
        {"i": 3, "sub": "it was the season of Light, it was the season of Darkness,"},
        {"i": 4, "sub": "we had everything before us, we had nothing before us,"},
        {"i": 5, "sub": "we were all going direct to Heaven, we were all going direct the other way"},
        {"i": 6, "sub": "in short"},
        {"i": 7, "sub": "the period was so far like the present period"},
        {"i": 8, "sub": "noisiest authorities"},
    ],
}


def main() -> int:
    for filename, fixes in FIXES.items():
        path = LAB_DIR / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        passage = data["passage"]
        anns = data["annotations"]

        changes = 0
        for f in fixes:
            i = f["i"]
            sub = f["sub"]
            occ = f.get("occurrence", 1)
            if i >= len(anns):
                print(f"  ! {filename}: ann index {i} out of range ({len(anns)} anns)")
                continue
            try:
                start, end = find_substring(passage, sub, occ)
            except ValueError as e:
                print(f"  ✗ {filename} ann {i}: {e}")
                continue
            old = (anns[i]["start"], anns[i]["end"])
            new = (start, end)
            if old != new:
                changes += 1
                anns[i]["start"] = start
                anns[i]["end"] = end

        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  ✓ {filename}: {changes} offsets corrected")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
