#!/usr/bin/env python3
"""LLM-review pass for Macbeth + Moonstone annotation notes.

Every rewritten note:
  - Starts with a single official code from the marking guide.
  - Code's family matches the annotation's category:
      structure → STR | SHIFT | PF | FIG | CTR
      evidence  → E   | RSN   | TRAP
      theme     → TH  | T     | MI   | CL
      inference → INF | POV   | SPK
      tone      → TO  | M     | WC   | CON | P
  - Tighter, pedagogical phrasing (1-2 sentences focused on the marking move).

No mixed-family prefixes (TH/FIG, FIG/TO, E/INF, STR/narrator shift, …).

Run from repo root:
    python3 scripts/rewrite_library_annotations.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_DIR = REPO_ROOT / "content" / "library"


# Category-family validators (used by the audit step at the end).
FAMILY_CODES = {
    "structure": {"STR", "SHIFT", "PF", "FIG", "CTR"},
    "evidence":  {"E", "RSN", "TRAP"},
    "theme":     {"TH", "T", "MI", "CL"},
    "inference": {"INF", "POV", "SPK"},
    "tone":      {"TO", "M", "WC", "CON", "P"},
}


# Macbeth — keyed by (section_id, ordinal-zero-indexed).
MACBETH_REWRITES: dict[tuple[str, int], str] = {

    ("act-i-scene-i", 0): "STR: the very first words of the play. The witches open with a question about a future meeting, planting the engine of the whole tragedy in line 1.",
    ("act-i-scene-i", 1): "TH: the play's central theme arrives in line 11 as chiasmus — moral inversion, things becoming their opposites. Watch this phrase echo in Macbeth's first line ('So foul and fair a day').",

    ("act-i-scene-ii", 0): "TO: the Captain calls Macbeth 'brave' — the title he 'deserves.' This is the only moment in the play Macbeth is unambiguously a hero; the tragedy is the fall from this praise.",

    ("act-i-scene-iii", 0): "STR: Macbeth's first line picks up the witches' 'fair is foul' from Scene 1. He has stepped into their moral language before he meets them.",
    ("act-i-scene-iii", 1): "STR: the three hailings (Glamis, Cawdor, King) build a structural ladder. Each rung will be climbed in order across the play.",
    ("act-i-scene-iii", 2): "INF: Macbeth tells himself he could wait for chance to crown him. The reader infers he is already considering the alternative — and rejecting it.",

    ("act-i-scene-iv", 0): "STR: Duncan names Malcolm 'Prince of Cumberland' — a structural block against Macbeth's prophecy. Macbeth's next soliloquy resolves to remove the block.",

    ("act-i-scene-v", 0): "E: Lady Macbeth has just read the prophecy letter. She treats two of three predictions as fulfilled and the third as inevitable; her certainty is the evidence of her decisiveness.",
    ("act-i-scene-v", 1): "TO: the famous opening of Lady Macbeth's invocation. Even the raven (already a bird of bad omen) is hoarse — the tone is gothic, deliberate, terrible.",
    ("act-i-scene-v", 2): "TH: Lady Macbeth asks to be stripped of womanhood so she can do the deed. The play tests whether gender constrains violence; she answers no.",
    ("act-i-scene-v", 3): "STR: Lady Macbeth summons darkness to hide the murder from heaven. Pairs with Macbeth's 'Stars, hide your fires' (1.4) — both Macbeths want the world dimmed.",

    ("act-i-scene-vi", 0): "INF: Banquo praises peaceful birds nesting at Macbeth's castle. The reader infers dramatic irony — the gentle setting is a murder house in waiting.",

    ("act-i-scene-vii", 0): "TH: opening of Macbeth's great soliloquy of doubt. He wishes the murder could be a single, contained act; the rest of the speech shows he knows it won't be.",
    ("act-i-scene-vii", 1): "E: in this same speech Macbeth lists every reason NOT to kill Duncan (kinsman, guest, king, virtuous). The absence of any honest reason TO kill him is the evidence pushing him toward refusal.",
    ("act-i-scene-vii", 2): "TO: ambition imagined as a rider who leaps too hard and falls off the far side. The tone is honest, almost rueful — Macbeth knows the danger and names it.",

    ("act-ii-scene-i", 0): "TH: the dagger soliloquy. An imagined dagger floats before Macbeth on his way to murder. The hallucination IS the theme — guilt arrives BEFORE the act.",
    ("act-ii-scene-i", 1): "INF: Macbeth chooses to follow a vision he knows may not be real ('A dagger of the mind'). The reader infers he wants the vision to be true.",
    ("act-ii-scene-i", 2): "TO: the language turns shadowy and feverish — witchcraft, wolves, ghosts. Tone has shifted from 1.7's doubt to ritualized resolution.",

    ("act-ii-scene-ii", 0): "STR: the offstage murder is announced in five words. Shakespeare doesn't show the killing — the deed exists only in language. The whole scene is the IMMEDIATE AFTER.",
    ("act-ii-scene-ii", 1): "TH: an unseen voice names the murder — sleep itself is what's been killed. The line predicts Macbeth's punishment will be sleeplessness, which the play delivers.",
    ("act-ii-scene-ii", 2): "TO: hyperbole — not even the ocean can wash this blood. The tone is horror at what cannot be undone. This image returns inverted in Act 5 with Lady Macbeth's 'Out, damned spot.'",
    ("act-ii-scene-ii", 3): "STR: Lady Macbeth's casual dismissal will be answered by her own sleepwalking later. Shakespeare plants a structural reversal — her calm becomes Macbeth's; his horror becomes hers.",
    ("act-ii-scene-ii", 4): "TO: Macbeth's despairing closing line. The offstage knocking has begun — a constant, hammering reminder of the dead man inside. The tone is anguished: 'I wish you could wake him.'",

    ("act-ii-scene-iii", 0): "TO: the Porter scene opens with drunk-comedy moments after the murder. The tonal whiplash is intentional — the macabre joke makes the killing MORE terrible by contrast.",

    ("act-ii-scene-iv", 0): "TO: after Duncan's murder, daylight itself feels strangled. The tone shifts to disorder — nature mirrors the moral disorder inside Macbeth's castle.",
    ("act-ii-scene-iv", 1): "TH: Macduff worries the new political order will fit worse than the old. Clothing imagery carries the theme — bad kings wear ill-fitting kingship.",

    ("act-iii-scene-i", 0): "TH: Macbeth's new soliloquy. Becoming king isn't enough — he needs to STAY king. The crown brings new fear, not relief. The play's argument about ambition is doing its work.",

    ("act-iii-scene-ii", 0): "TH: Lady Macbeth names the cost of ambition: getting what you wanted has not brought peace.",
    ("act-iii-scene-ii", 1): "TO: Macbeth's mind is now poisonous and restless. The image shows guilt turning into paranoia — the tone has darkened from horror to dread.",
    ("act-iii-scene-ii", 2): "STR: power shifts inside the marriage. Macbeth now hides the murder plan from Lady Macbeth, reversing the dynamic of Act 1.",

    ("act-iii-scene-iii", 0): "STR: Banquo dies, but Fleance escapes. The prophecy line survives — Macbeth's attempt to control fate fails at the structural level.",
    ("act-iii-scene-iii", 1): "E: the murderers themselves name the failed half of the plan. The line is direct evidence that Fleance's escape will haunt every later scene.",

    ("act-iii-scene-iv", 0): "STR: Macbeth hosts the banquet, pretending normality. The next moment, Banquo's ghost arrives — the structural turn from ritual order to public collapse.",

    ("act-iii-scene-v", 0): "STR: Hecate reframes the witches' role. They are not just predicting events; they are managing riddles whose surface meaning misleads the hearer.",
    ("act-iii-scene-v", 1): "TH: the scene names Macbeth's next trap. It will be false confidence, not fear, that destroys him.",

    ("act-iii-scene-vi", 0): "TO: Lennox speaks in bitter irony. The tone teaches readers to listen for what speakers DO NOT mean — the reverse of the surface words.",
    ("act-iii-scene-vi", 1): "STR: the resistance plot begins. Macduff's absence from Macbeth's feast becomes the political danger that will end the play.",

    ("act-iv-scene-i", 0): "STR: the witches' chant returns. Anaphora + rhyme + repetition signal ritual space — Macbeth has come back to the source of his prophecies, looking for more.",
    ("act-iv-scene-i", 1): "E: the second prophecy. Macbeth treats this as proof of invincibility — but the line is a trap (Macduff 'was from his mother's womb / Untimely ripped'). 'Evidence' technically true, practically false.",

    ("act-iv-scene-ii", 0): "TH: Lady Macduff names the cruel logic of Macbeth's Scotland — fear itself can be treated as guilt.",
    ("act-iv-scene-ii", 1): "TO: the bird image makes Lady Macduff's anger maternal and vulnerable. Tone: even the smallest creature defends its young.",
    ("act-iv-scene-ii", 2): "INF: the messenger cannot give full evidence, but his warning lets the reader infer Macbeth's coming violence against innocents.",

    ("act-iv-scene-iii", 0): "TO: Malcolm's language shows Macbeth has become morally poisonous — even saying his name hurts.",
    ("act-iv-scene-iii", 1): "STR: Malcolm's self-accusations were a loyalty test. The scene turns when his false confession reveals true intent.",
    ("act-iv-scene-iii", 2): "TH: Macduff rejects the idea that manhood means hiding grief. The play contrasts this with Macbeth's earlier suppression of feeling.",

    ("act-v-scene-i", 0): "TH: Lady Macbeth sleepwalking. The 'spot' is imagined blood that cannot be washed away — answering her own line in 2.2 ('A little water clears us of this deed'). The play has rotated 180°.",
    ("act-v-scene-i", 1): "TO: hyperbole + futility. The tone is haunted, almost childlike. Lady Macbeth, who held the plan together in Acts 1-2, has been emptied by guilt.",

    ("act-v-scene-ii", 0): "STR: Malcolm's army assembles near Birnam Wood — the place named in the second prophecy. The 'impossible' condition is about to be fulfilled by soldiers carrying branches.",

    ("act-v-scene-iii", 0): "TO: Macbeth describes his own old age — withered, autumnal. He admits aloud what the play has shown: ambition led to premature decline.",

    ("act-v-scene-iv", 0): "STR: Malcolm gives the order that fulfills the prophecy. Each soldier carries a tree branch — and so Birnam Wood literally moves to Dunsinane.",

    ("act-v-scene-v", 0): "TO: Macbeth's first reaction to Lady Macbeth's death. The line is famously flat — neither grief nor surprise. The play has worn him down beyond emotion.",
    ("act-v-scene-v", 1): "TH: the great soliloquy of despair. See the Reading Lab entry 'Tomorrow, and tomorrow, and tomorrow' for full marking analysis.",

    ("act-v-scene-vi", 0): "STR: Birnam Wood has 'moved' because the soldiers drop their branches. The prophecy is fulfilled through a literal-minded trick.",

    ("act-v-scene-vii", 0): "TO: Macbeth imagines himself as a trapped bear. The once-ambitious hero is reduced to cornered survival — tone matches Act 5's other shrinking images.",
    ("act-v-scene-vii", 1): "TH: Macduff's revenge is not ambition; it is grief demanding justice. The play separates him sharply from Macbeth here.",

    ("act-v-scene-viii", 0): "STR: the trap snaps shut. The 'none of woman born' prophecy is fulfilled by a technicality — Macduff was born by caesarean. The play's logic of 'true but misleading' completes itself.",
    ("act-v-scene-viii", 1): "TO: Macbeth's last words. Defiant in the face of certain death. Whatever else he became, he ends as the soldier the play opened with — fighting.",
}


# Moonstone — keyed by (section_id, ordinal-zero-indexed).
MOONSTONE_REWRITES: dict[tuple[str, int], str] = {

    ("prologue", 0): "STR: the historical anchor. The diamond is taken during a real 1799 British siege of an Indian fortress. Collins ties the family-mystery to colonial violence — the curse is also a moral debt.",
    ("prologue", 1): "STR: the Prologue opens with a letter from a soldier explaining why he has cut off his cousin John Herncastle. The whole novel sits inside a moral indictment from the first page.",

    ("betteredge-ch-i", 0): "TO: Betteredge opens by quoting Robinson Crusoe and treats Defoe's novel as a sacred oracle. His voice (servant, faithful, mildly comic) is fingerprinted in line one.",

    ("betteredge-ch-ii", 0): "STR: Betteredge moves backward into family history before the theft. The chapter teaches the reader that detective stories collect ordinary household detail before crime arrives.",

    ("betteredge-ch-iii", 0): "STR: Betteredge explains his narration method — dates, a diary, memory. The book is teaching the reader how to read it: trust the timestamps, watch for the gaps.",

    ("betteredge-ch-iv", 0): "STR: the Shivering Sand — a literal quicksand near the house — becomes a recurring symbol. Whatever falls into it cannot be recovered. Collins plants the image early; it pays off later.",

    ("betteredge-ch-v", 0): "TO: Betteredge studies Franklin as both old servant and narrator. His personal disappointment colors the report — useful warmth, but also potential bias.",

    ("betteredge-ch-vi", 0): "STR: the diamond's backstory enters through reported speech. Collins layers testimony inside testimony — the form mirrors the legal evidence that will matter later.",

    ("betteredge-ch-vii", 0): "TO: Penelope's curiosity and Betteredge's evasions make the household comic. The light tone hides a building tension — the reader feels it before the steward names it.",

    ("betteredge-ch-viii", 0): "STR: Betteredge openly controls the pacing, skipping quiet days until the Moonstone becomes everyone's business. Narrator-as-editor is part of the marking lesson.",

    ("betteredge-ch-ix", 0): "STR: the birthday chapter starts as domestic routine. That calm setup matters: the diamond's arrival will overturn it sentence by sentence.",

    ("betteredge-ch-x", 0): "TO: Betteredge consults Robinson Crusoe again — his oracle. The recurring habit is a character marker; Defoe stands in for stable belief in a destabilizing case.",

    ("betteredge-ch-xi", 0): "E: the chapter opens with the practical question of WHERE Rachel will put the diamond. Placement is evidence — a detective novel treats spatial detail as proof.",

    ("betteredge-ch-xii", 0): "E: Betteredge presents news as 'items,' like entries in a case file. Each reported movement is a piece of evidence the reader should track separately.",

    ("betteredge-ch-xiii", 0): "INF: Lady Verinder's recoil from Sergeant Cuff is emotional evidence. The reader infers that the investigation will divide the household, not just identify a thief.",

    ("betteredge-ch-xiv", 0): "E: the shrubbery path is introduced as spatial evidence. In a detective novel, routes and favorite walks are clues — track them like physical objects.",

    ("betteredge-ch-xv", 0): "STR: the chapter turns domestic movements into a sequence. Detective structure builds from order of events; the steward becomes a chronicler.",

    ("betteredge-ch-xvi", 0): "INF: Betteredge's narration keeps mixing loyalty with suspicion. The reader infers what he cannot confess — that someone he loves may have done it.",

    ("betteredge-ch-xvii", 0): "E: Cuff's investigation runs on concrete particulars rather than impressions. Track the physical evidence he gathers; it returns later in another narrator's hands.",

    ("betteredge-ch-xviii", 0): "TO: Betteredge's loyal voice makes painful discoveries feel personal. The emotional tone is part of the evidence — readers should weigh it alongside the facts.",

    ("betteredge-ch-xix", 0): "STR: the case widens beyond the stolen jewel. Detective structure often expands the scene before it narrows — Collins lets the household grow before the investigation tightens.",

    ("betteredge-ch-xx", 0): "INF: when characters withhold, avoid, or redirect, silence becomes a clue. Read what is NOT said as evidence, not as absence.",

    ("betteredge-ch-xxi", 0): "STR: the first narrative approaches its break point. Collins uses chapter sequence to move from house-events to a structural handoff between narrators.",

    ("betteredge-ch-xxii", 0): "TO: Betteredge's attachment to the family shapes what he emphasizes. His warmth is useful, but it is also a filter — note what he glosses over.",

    ("betteredge-ch-xxiii", 0): "STR: the closing chapter of Betteredge's main narrative hands the case forward. The structure reminds the reader: the next voice will see different things.",

    ("clack-ch-i", 0): "STR: Miss Clack's narrative begins. Same diamond, totally different narrator. Compare her voice (sanctimonious, judgmental) to Betteredge's (warm, plain, faithful). This SHIFT is the novel's whole pedagogy.",

    ("clack-ch-ii", 0): "TO: Miss Clack's moral certainty produces comedy and distortion. Her tone is itself evidence of bias — readers should treat the voice as a separate clue.",

    ("clack-ch-iii", 0): "INF: Clack interprets other people through her religious agenda. Readers must infer the actual scene by subtracting her commentary from her descriptions.",

    ("clack-ch-iv", 0): "TO: the chapter keeps Clack's self-satisfied voice in front. Her confidence does not guarantee reliability — the louder the voice, the more skeptical the reader should be.",

    ("clack-ch-v", 0): "STR: Clack's section reframes the mystery through letters, visits, and social pressure rather than direct detection. The PoV shift changes which evidence even appears.",

    ("clack-ch-vi", 0): "INF: notice the gap between what Clack thinks she is doing and what the scene shows. The irony is the inference — and the reader's reward.",

    ("clack-ch-vii", 0): "TO: Clack's pious language often makes serious moments absurd. Collins uses voice to make the narrative itself a comic argument about bias.",

    ("clack-ch-viii", 0): "STR: Clack's final chapter closes one biased testimony and prepares the need for a cooler legal voice. Structural handoff signals: voice changes are about to change what the reader knows.",

    ("bruff-ch-i", 0): "STR: Mr Bruff (a lawyer) takes over from Miss Clack. The handoff is the lesson — he refers to her by name. The narrators are aware of each other; the novel knows itself.",

    ("bruff-ch-ii", 0): "E: Bruff's legal narration treats documents, motives, and timelines as evidence. This chapter should be read like a case file — fact by fact, source by source.",

    ("bruff-ch-iii", 0): "STR: Bruff's section shifts the case from family feeling to legal and financial motive, widening the field of suspects without changing the facts.",

    ("blake-ch-i", 0): "STR: Franklin Blake takes over — protagonist, investigator, and (it turns out) suspect. His narration opens with a date and a journey; the form is memoir, the most intimate voice so far.",

    ("blake-ch-ii", 0): "TO: Franklin's narration is anxious and self-involved. His emotional state matters because he is now both lead investigator and (the great twist) the unknowing thief.",

    ("blake-ch-iii", 0): "STR: Franklin's chapter turns the search into a journey toward a document. The detective plot is now about reconstructing a written record, not interviewing witnesses.",

    ("blake-ch-iv", 0): "STR: the great structural reveal. The investigator IS the thief. Collins built this move 50 years before Christie used it in Roger Ackroyd — and it works for the same reason.",

    ("blake-ch-v", 0): "INF: Franklin starts planning what evidence he needs and whom he must confront. His reasoning chain is now visible to the reader — and unreliable, because he distrusts himself.",

    ("blake-ch-vi", 0): "E: the letter and nightgown become portable evidence. Franklin carries physical objects that can be tested against his memory — a detective story tactic Collins basically invents here.",

    ("blake-ch-vii", 0): "TO: Rachel and Franklin's silent confrontation is emotionally charged before it is explanatory. Feeling carries information here — read the silences for evidence.",

    ("blake-ch-viii", 0): "STR: Bruff's visit marks the cost of discovery. The case is no longer 'what happened?' but what the answer will MEAN — a structural pivot from puzzle to consequence.",

    ("blake-ch-ix", 0): "E: opium is named as the key piece of evidence. The hypothesis is that Blake took the diamond under the influence of opium given by Dr Candy. The case turns on this single physical fact.",

    ("blake-ch-x", 0): "TO: Franklin's suspense is physical and mental. The narration makes waiting feel like pressure — the tone IS the reader's anxiety.",

    ("blake-2", 0): "STR: Franklin resumes after Ezra Jennings's journal, summarizing results rather than re-narrating events. The structure has compressed; the case is moving toward its end.",

    ("cuff", 0): "E: Cuff's contribution is explicitly a REPORT. The form promises answers through inference, sequence, and confirmed facts — a detective's testimony, distinct from the family voices.",

    ("candy", 0): "TO: Candy's letter turns the investigation into aftermath. The tone is elegiac — a reminder that the case has cost more than a diamond.",

    ("betteredge-2", 0): "STR: Betteredge returns to close the family story rather than the diamond story. The structure shifts from puzzle resolution to social repair — the household closes ranks.",

    ("epilogue", 0): "TH: the diamond is found — back in India, at the shrine. The Epilogue answers the Prologue: same place, same priests. The whole novel is the loop between these two moments.",
}


def apply_rewrites(filename: str, rewrites: dict[tuple[str, int], str], label: str) -> int:
    path = LIBRARY_DIR / filename
    data = json.loads(path.read_text(encoding="utf-8"))

    changed = 0
    mismatches: list[str] = []
    audit_pass = 0

    for sec in data["sections"]:
        for i, ann in enumerate(sec.get("annotations", [])):
            key = (sec["id"], i)
            if key in rewrites:
                ann["note"] = rewrites[key]
                changed += 1

            # Audit: verify prefix matches family
            note = ann["note"]
            prefix = note.split(":", 1)[0].strip() if ":" in note[:20] else None
            family_codes = FAMILY_CODES.get(ann["category"], set())
            if prefix in family_codes:
                audit_pass += 1
            else:
                mismatches.append(
                    f"  ✗ [{sec['id']}#{i + 1}] cat={ann['category']} prefix={prefix!r} → not in {sorted(family_codes)}"
                )

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(len(s.get("annotations", [])) for s in data["sections"])
    print(f"{label}: rewrote {changed} / {total} annotations. Audit pass: {audit_pass}/{total}.")
    for m in mismatches:
        print(m)
    return len(mismatches)


def main() -> int:
    fails = 0
    fails += apply_rewrites("001-macbeth.json", MACBETH_REWRITES, "Macbeth")
    fails += apply_rewrites("003-moonstone.json", MOONSTONE_REWRITES, "Moonstone")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
