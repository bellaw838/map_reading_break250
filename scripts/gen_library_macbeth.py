#!/usr/bin/env python3
"""Parse Project Gutenberg's Macbeth into a Reading Library JSON.

Source: /tmp/macbeth-raw.txt (PG eBook #1533)
Output: content/library/001-macbeth.json

Schema mirrors the Reading Lab JSON but adds:
  - type: "play" | "novel" | "story-collection"
  - sections: array of {id, label, subtitle, text, annotations}

Annotations are sparse (3-5 per famous scene only).
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_DIR = REPO_ROOT / "content" / "library"
RAW_PATH = Path("/tmp/macbeth-raw.txt")

# Smart-quote → ASCII normalization for stable substring lookup.
SMART_QUOTES = {
    "\u2018": "'", "\u2019": "'",  # left/right single quotes
    "\u201c": '"', "\u201d": '"',  # left/right double quotes
    "\u2014": "—",  # em dash kept as Unicode for visual fidelity
    "\u2013": "-",  # en dash → hyphen
    "\u2026": "…",  # ellipsis kept
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


def parse_scenes(raw: str) -> list[dict]:
    """Walk through raw text capturing ACT/SCENE boundaries."""
    lines = raw.splitlines()
    sections: list[dict] = []
    current_act = None
    current_scene_id = None
    current_scene_label = None
    current_subtitle = None
    current_text: list[str] = []

    act_re = re.compile(r"^ACT ([IVX]+)$")
    scene_re = re.compile(r"^SCENE ([IVX]+)\.\s*(.*)$")

    def flush():
        if current_scene_id is None:
            return
        text = "\n".join(current_text).strip()
        # collapse 3+ blank lines to 2
        text = re.sub(r"\n{3,}", "\n\n", text)
        sections.append({
            "id": current_scene_id,
            "label": current_scene_label,
            "subtitle": current_subtitle,
            "text": text,
        })

    for line in lines:
        am = act_re.match(line)
        if am:
            current_act = am.group(1)
            continue
        sm = scene_re.match(line)
        if sm and current_act:
            flush()
            scene_roman = sm.group(1)
            location = sm.group(2).strip()
            current_scene_id = f"act-{current_act}-scene-{scene_roman}".lower()
            current_scene_label = f"Act {current_act}, Scene {scene_roman}"
            current_subtitle = location
            current_text = []
            continue
        if current_scene_id is not None:
            current_text.append(line)

    flush()
    return sections


# ─────────────────────────────────────────────────────────────────────
# Sparse annotations on famous moments.
# Identified by (section_id, substring → category, note).
# ─────────────────────────────────────────────────────────────────────
ANNOTATIONS_BY_SCENE: dict[str, list[dict]] = {
    "act-i-scene-i": [
        {
            "sub": "When shall we three meet again?",
            "category": "structure",
            "note": "STR: the very first words of the play. Shakespeare opens with a question — the witches name a future meeting, planting the play's whole engine in line 1.",
        },
        {
            "sub": "Fair is foul, and foul is fair",
            "category": "theme",
            "note": "TH/FIG: chiasmus. The play's central theme arrives in line 11 — moral inversion, things being their opposites. Watch this phrase echo in Macbeth's own first line ('So foul and fair a day I have not seen').",
        },
    ],
    "act-i-scene-ii": [
        {
            "sub": "For brave Macbeth (well he deserves that name),",
            "category": "tone",
            "note": "TO: the Captain praises Macbeth in heroic terms — 'brave Macbeth,' the title he 'deserves.' This is the only moment in the play when Macbeth is unambiguously a HERO. The whole tragedy is the fall from this reputation.",
        },
    ],
    "act-i-scene-iv": [
        {
            "sub": "My plenteous joys,",
            "category": "structure",
            "note": "STR: Duncan announces Malcolm as his heir ('Prince of Cumberland') — a structural blockade against Macbeth's prophecy. Macbeth's next line is the soliloquy where he names the obstacle and decides to overstep it.",
        },
    ],
    "act-i-scene-v": [
        {
            "sub": "Glamis thou art, and Cawdor; and shalt be",
            "category": "evidence",
            "note": "E: Lady Macbeth has just read the prophecy letter. She immediately treats two of three prophecies as ACCOMPLISHED and the third as inevitable. She is faster than Macbeth at every step.",
        },
        {
            "sub": "The raven himself is hoarse",
            "category": "tone",
            "note": "FIG/TO: the famous opening of Lady Macbeth's invocation. The raven (already a bird of bad omen) is HOARSE — even the omens are exhausted. Tone: gothic, deliberate, terrible.",
        },
        {
            "sub": "That tend on mortal thoughts, unsex me here,",
            "category": "theme",
            "note": "TH: Lady Macbeth's 'unsex me' invocation. She asks the spirits to strip her of womanhood so she can do the deed. The play repeatedly asks whether gender constrains violence — and Lady Macbeth answers no.",
        },
        {
            "sub": "Come, thick night,",
            "category": "structure",
            "note": "STR: the second half of Lady Macbeth's invocation. She summons darkness to hide the murder from heaven. Compare to Macbeth's later 'Stars, hide your fires' (1.4) — both Macbeths want the world dimmed.",
        },
    ],
    "act-i-scene-vi": [
        {
            "sub": "The temple-haunting martlet, does approve,",
            "category": "inference",
            "note": "INF: Banquo praises the gentle birds nesting at Macbeth's castle. The reader infers DRAMATIC IRONY — the castle has been turned into a murder-house, but the visitors see only peaceful birds. Their inference is exactly wrong.",
        },
    ],
    "act-i-scene-iii": [
        {
            "sub": "So foul and fair a day I have not seen.",
            "category": "structure",
            "note": "STR/echo: Macbeth's first line in the play picks up the witches' 'fair is foul' from Scene 1. He doesn't know he's already inside their language.",
        },
        {
            "sub": "All hail, Macbeth! hail to thee, Thane of Glamis!",
            "category": "structure",
            "note": "STR: the prophecy begins. The three hailings (Glamis / Cawdor / King) set up a structural ladder the play will climb.",
        },
        {
            "sub": "If chance will have me king, why, chance may crown me\nWithout my stir.",
            "category": "inference",
            "note": "INF: the FIRST hint Macbeth might NOT act. He tells himself he could wait passively — which means he's already considering action. Inferred: ambition exists.",
        },
    ],
    "act-i-scene-vii": [
        {
            "sub": "If it were done when 'tis done, then 'twere well\nIt were done quickly.",
            "category": "theme",
            "note": "TH: opening of Macbeth's great soliloquy of doubt. He wishes the murder could be a single, contained act — but the rest of the speech shows he knows it won't be.",
        },
        {
            "sub": "Vaulting ambition, which o'erleaps itself\nAnd falls on th' other—",
            "category": "tone",
            "note": "FIG/TO: ambition imagined as a rider who leaps too hard and falls off the far side of the horse. Tone is honest, almost rueful — Macbeth knows the danger.",
        },
        {
            "sub": "I have no spur\nTo prick the sides of my intent, but only\nVaulting ambition",
            "category": "evidence",
            "note": "E: in this same speech Macbeth lists every REASON not to kill Duncan (kinsman, guest, king, virtuous). The lack of any honest reason TO kill him is the evidence that pushes him toward refusal — until Lady Macbeth changes his mind.",
        },
    ],
    "act-ii-scene-i": [
        {
            "sub": "Is this a dagger which I see before me,\nThe handle toward my hand?",
            "category": "theme",
            "note": "TH/FIG: the dagger soliloquy. Imagined dagger floats before Macbeth on his way to murder. The hallucination IS the theme — guilt has arrived BEFORE the act.",
        },
        {
            "sub": "Thou marshall'st me the way that I was going;",
            "category": "inference",
            "note": "INF: Macbeth chooses to follow the imagined dagger, which is leading him to Duncan's chamber. He KNOWS the vision may not be real ('A dagger of the mind') — but he goes anyway. Inferred: he wants the vision to be true.",
        },
        {
            "sub": "wicked dreams abuse\nThe curtain'd sleep",
            "category": "tone",
            "note": "TO: the language of the speech turns shadowy and feverish — witchcraft, wolves, ghosts. Tone has shifted from soliloquy of doubt (1.7) to ritual of resolution.",
        },
    ],
    "act-ii-scene-ii": [
        {
            "sub": "I have done the deed.",
            "category": "structure",
            "note": "STR: the offstage murder is announced in five words. Shakespeare doesn't show the killing — the deed lives only in language. The whole scene is the IMMEDIATE AFTER, where guilt arrives.",
        },
        {
            "sub": "Sleep no more!\nMacbeth does murder sleep,",
            "category": "theme",
            "note": "TH/FIG: the murder is named immediately by an unseen voice — sleep itself is what's been killed. The line tells us Macbeth's punishment will be SLEEPLESSNESS, which the play delivers.",
        },
        {
            "sub": "Will all great Neptune's ocean wash this blood\nClean from my hand?",
            "category": "tone",
            "note": "FIG/TO: hyperbole — not even the ocean is enough. Tone: horror at what cannot be undone. This image returns inverted in Act 5 with Lady Macbeth's 'Out, damned spot.'",
        },
        {
            "sub": "A little water clears us of this deed:",
            "category": "structure",
            "note": "STR: Lady Macbeth's casual dismissal here will be answered by her own sleepwalking later. Shakespeare plants a structural reversal — Macbeth's horror will become hers; her calm will become his.",
        },
        {
            "sub": "Wake Duncan with thy knocking!",
            "category": "tone",
            "note": "TO: Macbeth's despairing closing line. The offstage knocking that will summon the Porter has begun — a constant, hammering reminder of the dead man inside. The line is anguished: 'I wish you could wake him.'",
        },
    ],
    "act-ii-scene-iii": [
        {
            "sub": "Here's a knocking indeed!",
            "category": "tone",
            "note": "TO: the Porter scene begins. After Act 2 Scene 2's horror, Shakespeare drops us into drunk-comedy. The tonal whiplash is intentional — the Porter's macabre humor (gate-of-hell joke) makes the murder MORE terrible by contrast.",
        },
    ],
    "act-iii-scene-i": [
        {
            "sub": "To be thus is nothing,\nBut to be safely thus.",
            "category": "theme",
            "note": "TH: Macbeth's new soliloquy. Becoming king isn't enough — he needs to STAY king. The crown brings new fear, not relief. The play's argument about ambition is doing its work.",
        },
    ],
    "act-iii-scene-iv": [
        {
            "sub": "Now, good digestion wait on appetite,",
            "category": "structure",
            "note": "STR: Macbeth's hosting line at the banquet — pretending normality. The next moment, Banquo's ghost arrives. The structural turn: the banquet (state, order, ritual) is shattered by the murdered man's appearance.",
        },
    ],
    "act-iv-scene-i": [
        {
            "sub": "Double, double, toil and trouble;\nFire, burn; and cauldron, bubble.",
            "category": "structure",
            "note": "STR: the witches' chant returns. Anaphora + rhyme + repetition signal we're in ritual space — Macbeth has come back to the source of his prophecies, looking for more.",
        },
        {
            "sub": "for none of woman born\nShall harm Macbeth.",
            "category": "evidence",
            "note": "E: the second prophecy. Macbeth treats this as proof of invincibility — but the line is a trap (Macduff 'was from his mother's womb / Untimely ripped'). The 'evidence' is technically true while practically false.",
        },
    ],
    "act-v-scene-i": [
        {
            "sub": "Out, damned spot! out, I say!",
            "category": "theme",
            "note": "TH/FIG: Lady Macbeth sleepwalking. The 'spot' is imagined blood that cannot be washed away — answering her own line in 2.2 ('A little water clears us of this deed'). The play has rotated 180°.",
        },
        {
            "sub": "all the perfumes of Arabia will\nnot sweeten this little hand.",
            "category": "tone",
            "note": "TO: hyperbole + futility. Tone is haunted, almost childlike. Lady Macbeth, who held the plan together in Acts 1-2, has been emptied by guilt.",
        },
    ],
    "act-v-scene-iii": [
        {
            "sub": "Is fall'n into the sere, the yellow leaf;",
            "category": "tone",
            "note": "FIG/TO: Macbeth describing his own old age — withered, autumnal. He admits aloud what the play has shown: ambition led not to thriving but to premature decline.",
        },
    ],
    "act-v-scene-ii": [
        {
            "sub": "Near Birnam wood",
            "category": "structure",
            "note": "STR: Malcolm's army assembles near Birnam Wood — the place named in the second prophecy. The 'impossible' condition ('until Birnam Wood come to Dunsinane') is about to be fulfilled by soldiers carrying branches. The witches' words held.",
        },
    ],
    "act-v-scene-iv": [
        {
            "sub": "Let every soldier hew him down a bough",
            "category": "structure",
            "note": "STR: Malcolm gives the order that fulfills the prophecy. Each soldier carries a tree branch as cover — and so Birnam Wood literally moves to Dunsinane. A 'true but misleading' prophecy completed by a literal-minded trick.",
        },
    ],
    "act-v-scene-v": [
        {
            "sub": "She should have died hereafter.",
            "category": "tone",
            "note": "TO: Macbeth's first reaction to Lady Macbeth's death. The line is famously flat — neither grief nor surprise. The play has worn him down beyond emotion.",
        },
        {
            "sub": "Tomorrow, and tomorrow, and tomorrow,",
            "category": "theme",
            "note": "TH: the great soliloquy of despair. See the Reading Lab entry 'Tomorrow, and tomorrow, and tomorrow' for full marking analysis.",
        },
    ],
    "act-v-scene-viii": [
        {
            "sub": "Despair thy charm;\nAnd let the angel whom thou still hast serv'd\nTell thee, Macduff was from his mother's womb\nUntimely ripp'd.",
            "category": "structure",
            "note": "STR: the trap snaps shut. The 'none of woman born' prophecy is fulfilled by a technicality — Macduff was born by caesarean. The play's logic of 'words that look like truth but mean something else' completes itself.",
        },
        {
            "sub": "lay on, Macduff;\nAnd damn'd be him that first cries, \"Hold, enough!\"",
            "category": "tone",
            "note": "TO: Macbeth's last words. Defiant in the face of certain death. Whatever else he became, he ends as the soldier the play opened with — fighting.",
        },
    ],
}


# ─────────────────────────────────────────────────────────────────────
# Discussion prompts + sample answers for the work as a whole.
# ─────────────────────────────────────────────────────────────────────
DISCUSSION = [
    {
        "prompt": "The play opens with 'Fair is foul, and foul is fair.' Where does this phrase echo later, and what does the repetition tell you about Macbeth's world?",
        "answer": "Macbeth himself unknowingly picks it up in his first line ('So foul and fair a day I have not seen'). The echo signals that Macbeth has stepped into the witches' moral universe before he ever meets them. Throughout the play, things become their opposites — sleep becomes torture, the king becomes a corpse, the brave soldier becomes the tyrant.",
    },
    {
        "prompt": "Lady Macbeth says 'A little water clears us of this deed' (2.2) and later sleepwalks crying 'Out, damned spot!' (5.1). What does this reversal show?",
        "answer": "She wrong about the deed being washable. The structure of the play is built on her own line returning to mock her. Shakespeare lets characters predict their own destruction without realizing it. This is the play's deepest pattern.",
    },
    {
        "prompt": "Why does Macbeth's 'Tomorrow' soliloquy (5.5) feel different from his earlier soliloquies (1.7, 2.1)?",
        "answer": "1.7 is full of doubt and moral reasoning. 2.1 is feverish and hallucinatory. 5.5 is exhausted — emptied of all reasoning and all feeling. The progression maps the play's argument: ambition does not lead to power; it leads to numbness.",
    },
    {
        "prompt": "The witches' prophecies are technically TRUE but mislead Macbeth. Find two examples of this 'true but false' pattern.",
        "answer": "(1) 'None of woman born shall harm Macbeth' — Macduff was born by caesarean, so technically not 'born' in the usual way. (2) 'Until Great Birnam Wood to high Dunsinane Hill / Shall come' — soldiers cut branches from Birnam Wood as camouflage. Both prophecies sound impossible until they are fulfilled by a trick of language.",
    },
    {
        "prompt": "Pick any scene and mark it using the 5-color system. Where did you find each color?",
        "answer": "Open-ended. Strong choices: 1.3 (witches' prophecy — structure + tone + theme all dense), 2.2 (post-murder — tone + theme + figurative language), 5.1 (Lady Macbeth sleepwalking — every color is present). The point of this prompt is to apply the marking habit on a longer text.",
    },
]


def main() -> int:
    if not RAW_PATH.exists():
        print(f"FAIL: {RAW_PATH} not found. Fetch with curl first.")
        return 2

    raw = normalize(RAW_PATH.read_text(encoding="utf-8"))
    sections = parse_scenes(raw)
    print(f"Parsed {len(sections)} scenes.")

    # Attach annotations to scenes that have them defined.
    for sec in sections:
        sec_anns = ANNOTATIONS_BY_SCENE.get(sec["id"], [])
        out_anns = []
        for spec in sec_anns:
            try:
                start, end = find_substring(sec["text"], spec["sub"])
            except ValueError as e:
                print(f"  ! {sec['id']}: annotation skip ({e})")
                continue
            out_anns.append({
                "start": start,
                "end": end,
                "category": spec["category"],
                "note": spec["note"],
            })
        sec["annotations"] = out_anns

    annotated_scenes = sum(1 for s in sections if s["annotations"])
    total_anns = sum(len(s["annotations"]) for s in sections)
    print(f"Annotated {annotated_scenes} scenes with {total_anns} total annotations.")

    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

    out = {
        "id": "library-001-macbeth",
        "type": "play",
        "title": "Macbeth",
        "author": "William Shakespeare",
        "year": 1606,
        "source_url": "https://www.gutenberg.org/ebooks/1533",
        "category": "Drama",
        "difficulty": "Hard",
        "length_words": sum(len(s["text"].split()) for s in sections),
        "intro": (
            "Shakespeare's shortest tragedy. Five acts, 28 scenes. A Scottish "
            "general is told by three witches he will be king — and then chooses "
            "to make the prophecy come true. Watch how the play's central pattern "
            "(things becoming their opposites, words that look true but mislead) "
            "shows up in scene after scene. Sparse marking annotations on the "
            "famous moments — read the rest at your own pace."
        ),
        "sections": sections,
        "discussion_prompts": [d["prompt"] for d in DISCUSSION],
        "discussion_answers": [d["answer"] for d in DISCUSSION],
    }

    out_path = LIBRARY_DIR / "001-macbeth.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  ✓ {out_path.relative_to(REPO_ROOT)} ({out['length_words']:,} words, {len(sections)} scenes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
