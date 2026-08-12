#!/usr/bin/env python3
"""Add difficulty tags to existing lab texts + generate 6 new Easy/Medium ones.

Existing 9 are mostly Hard. Adds:
  - 4 Easy texts (2 more fables + 1 short poem + 1 children's classic opening)
  - 2 Medium texts (2 Frost poems)

Difficulty levels: Easy / Medium / Hard.

After running, JSON files are the artifact. Delete the script.
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LAB = BASE / "content/lab"


# ─── Step 1: Tag existing 9 with difficulty ───────────────────────────────────

EXISTING_DIFFICULTY = {
    "001-sonnet-18.json":                       "Hard",
    "002-gettysburg-address.json":              "Hard",
    "003-walden-i-went-to-the-woods.json":      "Hard",
    "004-huck-finn-opening.json":               "Medium",
    "005-gift-of-the-magi-opening.json":        "Medium",
    "006-boy-who-cried-wolf.json":              "Easy",
    "007-all-the-worlds-a-stage.json":          "Hard",
    "008-tomorrow-and-tomorrow.json":           "Hard",
    "009-tale-of-two-cities-opening.json":      "Hard",
}


def offsets_for(passage, phrase, occurrence=1):
    pos = -1
    for _ in range(occurrence):
        pos = passage.find(phrase, pos + 1)
        if pos == -1:
            raise ValueError(f"phrase not found: {phrase!r} (occurrence {occurrence})")
    return pos, pos + len(phrase)


def annotate(passage, anns):
    out = []
    for phrase, occ, cat, note in anns:
        start, end = offsets_for(passage, phrase, occ)
        out.append({"start": start, "end": end, "category": cat, "note": note})
    return out


# ─── 010 The Tortoise and the Hare (Aesop) — EASY ────────────────────────────

TORTOISE_PASSAGE = """The Hare was once boasting of his speed before the other animals. "I have never yet been beaten," said he, "when I put forth my full speed. I challenge anyone here to race with me."

The Tortoise said quietly, "I accept your challenge."

"That is a good joke," said the Hare. "I could dance round you all the way."

"Keep your boasting until you've beaten," answered the Tortoise. "Shall we race?"

So a course was set and a start was made. The Hare darted almost out of sight at once, but soon stopped and, to show his contempt for the Tortoise, lay down to have a nap. The Tortoise plodded on and plodded on, and when the Hare awoke from his nap, he saw the Tortoise just near the winning post and could not run up in time to save the race.

Then the Tortoise said: "Slow but steady wins the race." """.strip()

TORTOISE = {
    "id": "lab-010-tortoise-and-the-hare",
    "title": "The Tortoise and the Hare",
    "author": "Aesop (translated by George Fyler Townsend)",
    "year": 1867,
    "source_url": "https://www.gutenberg.org/files/19994/19994-h/19994-h.htm",
    "category": "Fable",
    "difficulty": "Easy",
    "length_words": 170,
    "intro": "A short fable. Notice the pattern: the Hare boasts, takes a shortcut (a nap), and loses. Aesop ends with the explicit moral. As you read, see how each action of the Hare reveals his character.",
    "passage": TORTOISE_PASSAGE,
    "annotations": annotate(TORTOISE_PASSAGE, [
        ("I have never yet been beaten", 1, "tone",
         "The Hare's tone: confident, almost arrogant. Word choice ('never yet been beaten') signals boasting before the race even starts."),
        ("said quietly", 1, "tone",
         "The Tortoise's tone contrasts with the Hare's. 'Quietly' is the giveaway — modest, calm. Tone is shown through HOW characters speak, not just what they say."),
        ("to show his contempt for the Tortoise, lay down to have a nap", 1, "inference",
         "Character action reveals motive. The Hare doesn't nap because he's tired — he naps to show off. We can INFER his pride from the choice."),
        ("plodded on and plodded on", 1, "structure",
         "Repetition mirrors what the Tortoise actually does. Aesop is using sentence rhythm to show the slow, steady action."),
        ("could not run up in time to save the race", 1, "structure",
         "The structural turn. The Hare's plan breaks down right here — when he wakes and realizes he can't catch up."),
        ("Slow but steady wins the race", 1, "theme",
         "The explicit theme. Fables always end with the moral stated outright. Notice the theme is a complete sentence (not just 'patience'), which makes it usable as a real reading-analysis answer."),
    ]),
    "discussion_prompts": [
        "Find one action the Hare takes that reveals his character WITHOUT the narrator telling you what kind of animal he is.",
        "The theme is stated at the end. Could you have figured it out from the story alone? Why does Aesop spell it out anyway?",
        "Compare the Hare's words ('I have never yet been beaten') with what he actually does. What's the gap?",
        "What single word in the Tortoise's first reply ('I accept your challenge') signals his confidence?",
    ],
}


# ─── 011 The Lion and the Mouse (Aesop) — EASY ───────────────────────────────

LION_PASSAGE = """A Lion was awakened from sleep by a Mouse running across his face. Rising up in anger, he caught him and was about to kill him, when the Mouse cried out: "If you would only spare my life, I would be sure to repay your kindness."

The Lion laughed and let him go.

It happened shortly after this that the Lion was caught by some hunters, who bound him by strong ropes to the ground. The Mouse, recognizing his roar, came and gnawed the rope with his teeth, and set him free.

"You laughed at the idea of my ever being able to help you," said the Mouse, "expecting no repayment for your favor. Now you know that even a Mouse can help a Lion." """.strip()

LION = {
    "id": "lab-011-lion-and-mouse",
    "title": "The Lion and the Mouse",
    "author": "Aesop (translated by George Fyler Townsend)",
    "year": 1867,
    "source_url": "https://www.gutenberg.org/files/19994/19994-h/19994-h.htm",
    "category": "Fable",
    "difficulty": "Easy",
    "length_words": 148,
    "intro": "Another fable, this time about a reversal. The mighty Lion needs help from the small Mouse he once spared. Watch how Aesop builds the setup, then breaks it with the hunters' arrival.",
    "passage": LION_PASSAGE,
    "annotations": annotate(LION_PASSAGE, [
        ("Rising up in anger", 1, "tone",
         "Tone signal for the Lion: anger, dominance. The action reveals attitude immediately."),
        ("If you would only spare my life, I would be sure to repay your kindness", 1, "evidence",
         "The Mouse's promise. This sentence is the setup that the rest of the story will fulfill. Notice the conditional ('If… I would') — a deal is being offered."),
        ("The Lion laughed and let him go", 1, "inference",
         "We infer the Lion thinks the Mouse's offer is absurd — too small a creature to ever help him. The LAUGH is the inference clue."),
        ("It happened shortly after this", 1, "structure",
         "The structural turn. 'Shortly after' signals the time shift — the second half of the story begins, and the situation will reverse."),
        ("gnawed the rope with his teeth, and set him free", 1, "evidence",
         "Direct action that proves the Mouse can help the Lion. This is the EVIDENCE that fulfills the earlier promise."),
        ("even a Mouse can help a Lion", 1, "theme",
         "Theme stated explicitly. The fable's moral is about the value of small creatures and kindness — not just 'be nice.' The theme is a complete sentence."),
    ]),
    "discussion_prompts": [
        "The Lion laughs at the Mouse's offer. Why does Aesop include this detail rather than just having the Lion release him?",
        "Find the structural turn — where the story shifts from setup to reversal. What words mark the shift?",
        "The Mouse's last speech repeats his earlier promise. Why does Aesop repeat it?",
        "What does this fable share with 'The Tortoise and the Hare'? What's the recurring pattern in Aesop?",
    ],
}


# ─── 012 "Who Has Seen the Wind?" (Rossetti) — EASY ──────────────────────────

WIND_PASSAGE = """Who has seen the wind?
Neither I nor you:
But when the leaves hang trembling,
The wind is passing through.

Who has seen the wind?
Neither you nor I:
But when the trees bow down their heads,
The wind is passing by."""

WIND = {
    "id": "lab-012-who-has-seen-the-wind",
    "title": "Who Has Seen the Wind?",
    "author": "Christina Rossetti",
    "year": 1872,
    "source_url": "https://www.gutenberg.org/cache/epub/19188/pg19188.txt",
    "category": "Poetry",
    "difficulty": "Easy",
    "length_words": 38,
    "intro": "Eight lines, two near-identical stanzas. Notice how Rossetti uses repetition with small changes to make the same point twice — and how she answers her own question without naming the wind directly.",
    "passage": WIND_PASSAGE,
    "annotations": [
        # Both stanzas open with the same question; use occurrence indexing.
        *annotate(WIND_PASSAGE, [
            ("Who has seen the wind?", 1, "structure",
             "Opening question. Sets up the pattern: ask, answer no, then describe how we know anyway."),
        ]),
        *annotate(WIND_PASSAGE, [
            ("Neither I nor you", 1, "evidence",
             "Direct answer to the question: nobody has seen the wind. But the next two lines will show how we know it's there anyway."),
        ]),
        *annotate(WIND_PASSAGE, [
            ("leaves hang trembling", 1, "inference",
             "We can't see the wind itself, but we CAN see its effect. This is exactly how inference works: the clue (trembling leaves) tells us about the unseen cause (wind)."),
        ]),
        *annotate(WIND_PASSAGE, [
            ("Who has seen the wind?", 2, "structure",
             "Second stanza opens identically. The repetition signals that the pattern is the point — Rossetti is teaching her young readers a way of thinking, not just telling them about wind."),
        ]),
        *annotate(WIND_PASSAGE, [
            ("trees bow down their heads", 1, "inference",
             "Personification (trees don't have heads to bow) AND another inference clue. Same move as stanza 1 — Rossetti shows the effect, not the cause."),
        ]),
        *annotate(WIND_PASSAGE, [
            ("The wind is passing by", 1, "theme",
             "Theme: we know things by their effects, even when we can't see them. The poem is teaching a way to think about anything unseen — not just wind."),
        ]),
    ],
    "discussion_prompts": [
        "Both stanzas have the same shape. What changes between them? Why might Rossetti make the change tiny?",
        "Find an example of personification in the second stanza. What does giving trees 'heads' add to the poem?",
        "The wind is never named, but the poem is ABOUT the wind. How do we know what the wind is doing?",
        "Could this poem be about anything besides wind? What else moves invisibly but leaves signs?",
    ],
}


# ─── 013 Opening of The Wind in the Willows (Grahame) — EASY ─────────────────

WILLOWS_PASSAGE = """The Mole had been working very hard all the morning, spring-cleaning his little home. First with brooms, then with dusters; then on ladders and steps and chairs, with a brush and a pail of whitewash; till he had dust in his throat and eyes, and splashes of whitewash all over his black fur, and an aching back and weary arms.

Spring was moving in the air above and in the earth below and around him, penetrating even his dark and lowly little house with its spirit of divine discontent and longing. It was small wonder, then, that he suddenly flung down his brush on the floor, said "Bother!" and "O blow!" and also "Hang spring-cleaning!" and bolted out of the house without even waiting to put on his coat."""

WILLOWS = {
    "id": "lab-013-wind-in-the-willows-opening",
    "title": "Opening of The Wind in the Willows",
    "author": "Kenneth Grahame",
    "year": 1908,
    "source_url": "https://www.gutenberg.org/files/289/289-h/289-h.htm",
    "category": "Literary",
    "difficulty": "Easy",
    "length_words": 152,
    "intro": "A children's classic. Watch how Grahame uses small specific details (the brush, the whitewash, the splashes of paint) to build a vivid scene — and how the second paragraph turns the day around with one big idea: spring.",
    "passage": WILLOWS_PASSAGE,
    "annotations": annotate(WILLOWS_PASSAGE, [
        ("working very hard all the morning, spring-cleaning his little home", 1, "structure",
         "Opening establishes character + activity. The first paragraph is all about Mole's effort and discomfort — needed setup for the turn that's coming."),
        ("dust in his throat and eyes, and splashes of whitewash all over his black fur", 1, "evidence",
         "Specific physical details that prove how hard Mole is working. Grahame doesn't say 'Mole was tired' — he shows it through the dust, the splashes, the aching."),
        ("an aching back and weary arms", 1, "inference",
         "We infer Mole is exhausted. The detail is small, but it's the bridge between the work (paragraph 1) and the explosion of frustration (paragraph 2)."),
        ("Spring was moving in the air above and in the earth below", 1, "tone",
         "Tone shifts here. The first paragraph was domestic and tired. Now spring is 'moving' — the writing feels suddenly alive. Word choice ('above,' 'below,' 'around') makes spring feel everywhere at once."),
        ("divine discontent and longing", 1, "theme",
         "The story's central theme appears in three words: spring stirs a 'divine discontent' — a holy restlessness that pulls Mole out of his routine. The whole novel is about this longing."),
        ("\"Bother!\" and \"O blow!\" and also \"Hang spring-cleaning!\"", 1, "tone",
         "Mole's voice. The three exclamations build to comic frustration. Grahame is showing us Mole's personality through what he says, not just what the narrator describes."),
        ("bolted out of the house without even waiting to put on his coat", 1, "structure",
         "The action turn. Mole has gone from working dutifully to bolting out the door without his coat — and the rest of the novel begins. One sentence reverses the whole opening situation."),
    ]),
    "discussion_prompts": [
        "The first paragraph is full of small physical details (dust, brushes, ladders). What do these details accomplish that 'Mole was cleaning' wouldn't?",
        "Find the sentence that turns the story. What single word or phrase signals the shift?",
        "Mole says three things in a row ('Bother!' 'O blow!' 'Hang spring-cleaning!'). Why three? What does the repetition do?",
        "The narrator calls Mole's feeling 'divine discontent.' What does putting 'divine' (a heavy word) next to 'discontent' (a small irritation) do to the tone?",
    ],
}


# ─── 014 "The Road Not Taken" (Frost) — MEDIUM ────────────────────────────────

ROAD_PASSAGE = """Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever come back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference."""

ROAD = {
    "id": "lab-014-road-not-taken",
    "title": "The Road Not Taken",
    "author": "Robert Frost",
    "year": 1916,
    "source_url": "https://www.gutenberg.org/files/29345/29345-h/29345-h.htm",
    "category": "Poetry",
    "difficulty": "Medium",
    "length_words": 144,
    "intro": "Frost's most famous poem. Almost everyone misreads it. Watch carefully — the poem says the two roads were ABOUT THE SAME, but the speaker imagines telling the story later as if his choice was meaningful. The poem is about how we make meaning out of choices, not about choosing the harder path.",
    "passage": ROAD_PASSAGE,
    "annotations": annotate(ROAD_PASSAGE, [
        ("Two roads diverged in a yellow wood", 1, "structure",
         "The opening image. Two roads = two choices. The whole poem will use this metaphor."),
        ("sorry I could not travel both", 1, "tone",
         "Speaker's tone: regret at having to choose. We've all felt this — wanting to keep both options open."),
        ("Had worn them really about the same", 1, "evidence",
         "Critical line. The speaker himself says the roads were ABOUT THE SAME. Most readers miss this. It's the evidence that contradicts the famous ending."),
        ("both that morning equally lay\nIn leaves no step had trodden black", 1, "evidence",
         "More evidence that the roads were equal — neither had been walked that morning. Frost is being very explicit."),
        ("I shall be telling this with a sigh", 1, "structure",
         "The structural turn. The speaker jumps from the present (standing at the fork) to imagining the future (telling the story later). 'Telling this with a sigh' signals the story will be DRAMATIZED."),
        ("I took the one less traveled by", 1, "tone",
         "The famous line. Notice the irony: the speaker just told us the roads were 'about the same,' but now claims he took 'the one less traveled.' He's telling a story that doesn't match what he saw."),
        ("And that has made all the difference", 1, "theme",
         "Theme: we make meaning out of choices by the stories we tell ourselves later. The choice itself may have been small or even arbitrary — but the storytelling makes it feel significant. This is what the poem is really about."),
    ]),
    "discussion_prompts": [
        "Find the line where the speaker says the two roads were about the same. Why do most readers miss this line when they remember the poem?",
        "'I shall be telling this with a sigh / Somewhere ages and ages hence.' What does it mean to predict your own future storytelling?",
        "Compare the description of the choice (stanzas 1–3) with the speaker's future story about the choice (final stanza). What's different?",
        "What's the difference between the road and the STORY about the road in this poem?",
    ],
}


# ─── 015 "Stopping by Woods on a Snowy Evening" (Frost) — MEDIUM ─────────────

WOODS_PASSAGE = """Whose woods these are I think I know.
His house is in the village though;
He will not see me stopping here
To watch his woods fill up with snow.

My little horse must think it queer
To stop without a farmhouse near
Between the woods and frozen lake
The darkest evening of the year.

He gives his harness bells a shake
To ask if there is some mistake.
The only other sound's the sweep
Of easy wind and downy flake.

The woods are lovely, dark and deep,
But I have promises to keep,
And miles to go before I sleep,
And miles to go before I sleep."""

WOODS = {
    "id": "lab-015-stopping-by-woods",
    "title": "Stopping by Woods on a Snowy Evening",
    "author": "Robert Frost",
    "year": 1923,
    "source_url": "https://www.gutenberg.org/files/19153/19153-h/19153-h.htm",
    "category": "Poetry",
    "difficulty": "Medium",
    "length_words": 108,
    "intro": "Sixteen lines. A man stops his horse on a snowy road to look at the woods. Watch how Frost builds the pull of the woods (lovely, dark, deep) and then turns away from them at the end. The repeated final line is one of the most famous in American poetry.",
    "passage": WOODS_PASSAGE,
    "annotations": annotate(WOODS_PASSAGE, [
        ("Whose woods these are I think I know", 1, "tone",
         "The speaker is uncertain ('I think I know'). The casual phrasing makes the opening feel like a passing thought, not a confident statement."),
        ("He will not see me stopping here", 1, "inference",
         "We INFER the speaker is alone and somewhat hidden. He's stopping where he's not supposed to — there's a quiet hint of trespass."),
        ("The darkest evening of the year", 1, "tone",
         "The darkest evening = winter solstice. The setting choice contributes to the heavy, quiet mood. Frost picks the date deliberately."),
        ("He gives his harness bells a shake\nTo ask if there is some mistake", 1, "inference",
         "Personification. The horse doesn't really 'ask' anything — Frost projects the speaker's own doubts onto the horse. The horse's confusion mirrors what the reader might feel: WHY is he stopping?"),
        ("The woods are lovely, dark and deep", 1, "theme",
         "The pivot line. Three adjectives — lovely, dark, deep — pile up. The woods are attractive AND dangerous AND mysterious. The pull is strong."),
        ("But I have promises to keep", 1, "structure",
         "The structural turn. 'But' marks the speaker's decision to leave the woods despite their pull. Duty wins over the call of the unknown."),
        ("And miles to go before I sleep,\nAnd miles to go before I sleep", 1, "theme",
         "Repetition with a difference. The first 'miles to go' is literal (the journey home). The second 'miles to go' suggests something larger — life itself, before final rest. The repeated line is the theme: there's always more to do before you can stop."),
    ]),
    "discussion_prompts": [
        "Why does Frost set the poem on 'the darkest evening of the year'? What does the choice of date add to the mood?",
        "The horse 'shakes his harness bells.' Whose doubt is this really — the horse's or the speaker's?",
        "The final two lines are identical. What's different about reading them the second time?",
        "Find the word 'But' in the final stanza. Why is this single word the turn of the whole poem?",
    ],
}


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Step 1: add difficulty to existing files
    print("Tagging existing files with difficulty:")
    for fname, diff in EXISTING_DIFFICULTY.items():
        path = LAB / fname
        data = json.loads(path.read_text(encoding="utf-8"))
        data["difficulty"] = diff
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  + {fname}: {diff}")

    print()
    print("Writing 6 new texts:")
    for data, name in [
        (TORTOISE, "010-tortoise-and-the-hare.json"),
        (LION,     "011-lion-and-mouse.json"),
        (WIND,     "012-who-has-seen-the-wind.json"),
        (WILLOWS,  "013-wind-in-the-willows-opening.json"),
        (ROAD,     "014-road-not-taken.json"),
        (WOODS,    "015-stopping-by-woods.json"),
    ]:
        path = LAB / name
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  + {name}: {data['difficulty']} · {data['category']} · {len(data['passage'])}c · {len(data['annotations'])} ann")


if __name__ == "__main__":
    main()
