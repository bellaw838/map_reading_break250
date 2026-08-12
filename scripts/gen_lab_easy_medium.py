#!/usr/bin/env python3
"""Generate 6 Easy/Medium Reading Lab JSON files (010–015).

Each entry below pairs a passage with annotations specified as
substrings. The script resolves the substring to character offsets
via str.find(), so we never write raw offsets by hand.

Run from repo root:
    python3 scripts/gen_lab_easy_medium.py

Idempotent: safely overwrites existing 010–015 files.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LAB_DIR = REPO_ROOT / "content" / "lab"


def compute_offsets(passage: str, substring: str, occurrence: int = 1) -> tuple[int, int]:
    """Find the Nth occurrence (1-indexed) of substring; return (start, end)."""
    pos = -1
    for _ in range(occurrence):
        pos = passage.find(substring, pos + 1)
        if pos == -1:
            raise ValueError(f"substring not found: {substring!r} (occurrence {occurrence})")
    return pos, pos + len(substring)


def build_annotations(passage: str, specs: list[dict]) -> list[dict]:
    out = []
    for s in specs:
        start, end = compute_offsets(passage, s["substring"], s.get("occurrence", 1))
        out.append({
            "start": start,
            "end": end,
            "category": s["category"],
            "note": s["note"],
        })
    return out


# ─────────────────────────────────────────────────────────────────────
# 010 — The Tortoise and the Hare (Aesop, Easy, Fable)
# ─────────────────────────────────────────────────────────────────────
tortoise_passage = (
    'A HARE one day ridiculed the short feet and slow pace of the Tortoise, who replied, '
    'laughing: "Though you be swift as the wind, I will beat you in a race." The Hare, '
    'believing her assertion to be simply impossible, assented to the proposal; and they '
    'agreed that the Fox should choose the course and fix the goal. On the day appointed '
    'for the race the two started together. The Tortoise never for a moment stopped, but '
    'went on with a slow but steady pace straight to the end of the course. The Hare, '
    'lying down by the wayside, fell fast asleep. At last waking up, and moving as fast '
    'as he could, he saw the Tortoise had reached the goal, and was comfortably dozing '
    'after her fatigue.\n\nSlow but steady wins the race.'
)

tortoise = {
    "id": "lab-010-tortoise-and-hare",
    "title": "The Tortoise and the Hare",
    "author": "Aesop (translated by George Fyler Townsend)",
    "year": 1867,
    "source_url": "https://www.gutenberg.org/files/19994/19994-h/19994-h.htm",
    "category": "Fable",
    "difficulty": "Easy",
    "length_words": 130,
    "intro": (
        "A very short fable. The whole story is the setup for the one-line moral at the "
        "end. Watch how Aesop builds the contrast between the two animals — and notice "
        "what the Hare does (and doesn't do) versus the Tortoise."
    ),
    "passage": tortoise_passage,
    "annotations_spec": [
        {
            "substring": "A HARE one day ridiculed the short feet and slow pace of the Tortoise",
            "category": "structure",
            "note": "The opening sentence sets up the conflict in one breath: Hare mocks Tortoise. Fables don't waste words on background — the contrast IS the setup.",
        },
        {
            "substring": "ridiculed",
            "category": "tone",
            "note": "'Ridiculed' — not 'teased' or 'joked.' The word choice tells you the Hare is cruel, not playful. The whole moral hinges on this attitude.",
        },
        {
            "substring": '"Though you be swift as the wind, I will beat you in a race."',
            "category": "evidence",
            "note": "The Tortoise's quiet challenge. Notice she doesn't deny she's slow — she just claims she'll WIN anyway. That's the theme arriving in dialogue.",
        },
        {
            "substring": "believing her assertion to be simply impossible",
            "category": "inference",
            "note": "We infer the Hare's overconfidence here. He's so sure of winning he agrees to the race instantly. The reader sees the trap before he does.",
        },
        {
            "substring": "The Tortoise never for a moment stopped, but went on with a slow but steady pace",
            "category": "evidence",
            "note": "Direct evidence for the moral. The Tortoise's strategy is named explicitly: slow + steady + never stopping. Aesop is showing you the answer before stating it.",
        },
        {
            "substring": "The Hare, lying down by the wayside, fell fast asleep",
            "category": "structure",
            "note": "The turn. Until this sentence the Hare's victory seems guaranteed — then he naps. One sentence flips the whole race.",
        },
        {
            "substring": "comfortably dozing after her fatigue",
            "category": "tone",
            "note": "A small dignified detail: the Tortoise rests AFTER winning, not before. The contrast with the napping Hare is the whole point.",
        },
        {
            "substring": "Slow but steady wins the race.",
            "category": "theme",
            "note": "The explicit moral. Fables always end with the theme stated outright. Notice how every detail above has been preparing you for this one sentence.",
        },
    ],
    "discussion_prompts": [
        "The Hare and the Tortoise each take a strategy. Name each in your own words.",
        "Find a place where Aesop shows the Hare's character without telling you 'he was arrogant.' What's the detail?",
        "The moral could have been 'Don't be lazy' or 'Hard work wins.' Why does Aesop pick 'Slow but steady'? What's different?",
        "Where in the story does the outcome become inevitable? Mark the sentence.",
    ],
}

# ─────────────────────────────────────────────────────────────────────
# 011 — The Lion and the Mouse (Aesop, Easy, Fable)
# ─────────────────────────────────────────────────────────────────────
lion_passage = (
    "A LION was awakened from sleep by a Mouse running over his face. Rising up angrily, "
    "he caught him and was about to kill him, when the Mouse piteously entreated, saying: "
    '"If you would only spare my life, I would be sure to repay your kindness." The Lion '
    "laughed and let him go.\n\n"
    "It happened shortly after this that the Lion was caught by some hunters, who bound him "
    "by strong ropes to the ground. The Mouse, recognizing his roar, came and gnawed the "
    "rope with his teeth, and set him free, exclaiming:\n\n"
    '"You ridiculed the idea of my ever being able to help you, not expecting to receive '
    "from me any repayment of your favor; now you know that it is possible for even a Mouse "
    'to confer benefits on a Lion."'
)

lion = {
    "id": "lab-011-lion-and-mouse",
    "title": "The Lion and the Mouse",
    "author": "Aesop (translated by George Fyler Townsend)",
    "year": 1867,
    "source_url": "https://www.gutenberg.org/files/19994/19994-h/19994-h.htm",
    "category": "Fable",
    "difficulty": "Easy",
    "length_words": 145,
    "intro": (
        "Two scenes. In the first the Lion spares the Mouse; in the second the Mouse saves "
        "the Lion. Watch how Aesop sets up a debt in scene one and pays it off in scene "
        "two — and how the Mouse's last speech delivers the moral inside the story itself."
    ),
    "passage": lion_passage,
    "annotations_spec": [
        {
            "substring": "A LION was awakened from sleep by a Mouse running over his face",
            "category": "structure",
            "note": "The opening sets up the size mismatch in one sentence: Lion (big, sleeping) vs Mouse (small, scampering). Every fable starts with the contrast that will matter later.",
        },
        {
            "substring": "Rising up angrily",
            "category": "tone",
            "note": "The Lion's first reaction is rage. The story will test whether he can be more than his first instinct.",
        },
        {
            "substring": '"If you would only spare my life, I would be sure to repay your kindness."',
            "category": "evidence",
            "note": "The Mouse's promise. This is the seed. Everything in scene two pays off this single sentence.",
        },
        {
            "substring": "The Lion laughed and let him go.",
            "category": "inference",
            "note": "We infer the Lion thinks the Mouse's promise is absurd — he laughs. Aesop never says 'the Lion was condescending' — the laugh shows it.",
        },
        {
            "substring": "It happened shortly after this",
            "category": "structure",
            "note": "The structural pivot. Scene two begins. Notice how compressed the transition is — no time has passed for the reader, but the situation has reversed.",
        },
        {
            "substring": "caught by some hunters, who bound him by strong ropes",
            "category": "evidence",
            "note": "The Lion's reversal of fortune. Aesop is methodical: the powerful one is now helpless, exactly the condition the Mouse was in.",
        },
        {
            "substring": "came and gnawed the rope with his teeth, and set him free",
            "category": "evidence",
            "note": "The Mouse delivers on the promise. Concrete action — teeth, rope, free. The fable's logic is satisfied.",
        },
        {
            "substring": '"You ridiculed the idea of my ever being able to help you',
            "category": "theme",
            "note": "The Mouse's speech is the theme made explicit. He even names what the Lion did wrong — 'ridiculed.' Aesop lets the small character deliver the moral.",
        },
        {
            "substring": "it is possible for even a Mouse to confer benefits on a Lion",
            "category": "theme",
            "note": "The moral, in the Mouse's own words. Notice it's not 'be kind to small creatures' but 'small ones can help big ones' — the deeper claim.",
        },
    ],
    "discussion_prompts": [
        "Most fables end with a moral told by the narrator. Here the Mouse speaks the moral inside the story. What does this change?",
        "The Lion laughs at the Mouse's promise. Why does Aesop include this detail? What would be lost without it?",
        "Find the parallel between scene 1 and scene 2. Who is helpless in each? What does the structure tell you?",
        "Compare 'The Lion and the Mouse' to 'The Boy Who Cried Wolf.' Both are fables — how is the moral delivered differently?",
    ],
}

# ─────────────────────────────────────────────────────────────────────
# 012 — Who Has Seen the Wind? (Christina Rossetti, Easy, Poetry)
# ─────────────────────────────────────────────────────────────────────
wind_passage = (
    "Who has seen the wind?\n"
    "Neither I nor you:\n"
    "But when the leaves hang trembling,\n"
    "The wind is passing through.\n\n"
    "Who has seen the wind?\n"
    "Neither you nor I:\n"
    "But when the trees bow down their heads,\n"
    "The wind is passing by."
)

wind = {
    "id": "lab-012-who-has-seen-the-wind",
    "title": "Who Has Seen the Wind?",
    "author": "Christina Rossetti",
    "year": 1872,
    "source_url": "https://www.gutenberg.org/files/19188/19188-h/19188-h.htm",
    "category": "Poetry",
    "difficulty": "Easy",
    "length_words": 40,
    "intro": (
        "Two stanzas, eight lines. The poem is almost a riddle — it asks a question, "
        "admits the answer is 'no one,' and then tells you how to see what you can't see. "
        "Watch how the second stanza mirrors the first with tiny variations."
    ),
    "passage": wind_passage,
    "annotations_spec": [
        {
            "substring": "Who has seen the wind?",
            "category": "structure",
            "note": "The opening question is also the title. The poem will answer this question — but indirectly, by showing you the wind's EFFECTS rather than the wind itself.",
            "occurrence": 1,
        },
        {
            "substring": "Neither I nor you:",
            "category": "evidence",
            "note": "The honest answer: nobody has actually seen the wind. Rossetti is being precise — wind is invisible. The rest of the poem is about how to know something invisible.",
        },
        {
            "substring": "But when the leaves hang trembling",
            "category": "inference",
            "note": "The turn. We infer the wind's presence from what it DOES — trembling leaves. The poem's whole strategy: know the invisible by its visible effects.",
        },
        {
            "substring": "The wind is passing through.",
            "category": "theme",
            "note": "The pattern is named: we don't see the wind, but we know it by what it touches. Theme: invisible forces leave visible traces.",
        },
        {
            "substring": "Who has seen the wind?",
            "category": "structure",
            "note": "Second stanza repeats the question — same words, new context. The repetition isn't lazy; it's the poem's structural form. Watch what changes underneath.",
            "occurrence": 2,
        },
        {
            "substring": "Neither you nor I:",
            "category": "tone",
            "note": "Tiny but important variation: 'I nor you' became 'you nor I.' The pronouns swap. The poem keeps gently shifting under the repetition.",
        },
        {
            "substring": "the trees bow down their heads",
            "category": "tone",
            "note": "'Bow down their heads' — trees treated as if they have heads, as if they bow. The personification turns wind into a power that things RESPOND to.",
        },
        {
            "substring": "The wind is passing by.",
            "category": "structure",
            "note": "First stanza: 'passing through.' Second stanza: 'passing by.' One letter group changed. The wind moves; the poem's shape moves with it.",
        },
    ],
    "discussion_prompts": [
        "The poem repeats almost the same words in stanzas 1 and 2 — but not exactly. Find every tiny difference. Why each change?",
        "Why does Rossetti choose 'leaves trembling' and 'trees bowing' rather than naming the wind directly?",
        "What is this poem REALLY about? Just wind, or something bigger? Defend your answer.",
        "Try writing one more stanza in the same pattern — 'Who has seen X?' Pick something invisible.",
    ],
}

# ─────────────────────────────────────────────────────────────────────
# 013 — Opening of The Wind in the Willows (Kenneth Grahame, Easy, Literary)
# ─────────────────────────────────────────────────────────────────────
willows_passage = (
    "The Mole had been working very hard all the morning, spring-cleaning his little home. "
    "First with brooms, then with dusters; then on ladders and steps and chairs, with a "
    "brush and a pail of whitewash; till he had dust in his throat and eyes, and splashes "
    "of whitewash all over his black fur, and an aching back and weary arms. Spring was "
    "moving in the air above and in the earth below and around him, penetrating even his "
    "dark and lowly little house with its spirit of divine discontent and longing. It was "
    'small wonder, then, that he suddenly flung down his brush on the floor, said "Bother!" '
    'and "O blow!" and also "Hang spring-cleaning!" and bolted out of the house without '
    "even waiting to put on his coat."
)

willows = {
    "id": "lab-013-wind-in-the-willows-opening",
    "title": "Opening of The Wind in the Willows",
    "author": "Kenneth Grahame",
    "year": 1908,
    "source_url": "https://www.gutenberg.org/files/289/289-h/289-h.htm",
    "category": "Literary",
    "difficulty": "Easy",
    "length_words": 140,
    "intro": (
        "The novel opens mid-task — the Mole is spring-cleaning. Watch how Grahame uses "
        "specific, sensory details (brooms, dusters, dust in the throat) to set scene, "
        "then shifts the tone when 'spring' enters the air. The whole passage builds toward "
        "the Mole's decision to flee."
    ),
    "passage": willows_passage,
    "annotations_spec": [
        {
            "substring": "The Mole had been working very hard all the morning",
            "category": "structure",
            "note": "We meet the character mid-action. Grahame skips the introduction — no 'Once upon a time, there was a mole.' Just the work happening. This is a confident opening choice.",
        },
        {
            "substring": "First with brooms, then with dusters; then on ladders and steps and chairs, with a brush and a pail of whitewash",
            "category": "evidence",
            "note": "Concrete tools, listed in order. The detail makes the cleaning feel real — the reader can almost see him moving from one task to the next.",
        },
        {
            "substring": "till he had dust in his throat and eyes, and splashes of whitewash all over his black fur, and an aching back and weary arms",
            "category": "tone",
            "note": "Sensory exhaustion. Grahame piles up specific discomforts (throat, eyes, fur, back, arms). The tone is warm but not pitying — we feel the Mole's tiredness without being told 'he was tired.'",
        },
        {
            "substring": "Spring was moving in the air above and in the earth below and around him",
            "category": "structure",
            "note": "The pivot. The narrator zooms out from indoor work to outdoor weather. The whole world changes scale in one sentence.",
        },
        {
            "substring": "its spirit of divine discontent and longing",
            "category": "theme",
            "note": "The phrase that opens the book's real theme: 'divine discontent.' Spring isn't just weather — it's a feeling that pulls characters out of their normal lives. The whole novel will be about answering that pull.",
        },
        {
            "substring": "It was small wonder, then, that he suddenly flung down his brush",
            "category": "structure",
            "note": "'It was small wonder, then' — the narrator's voice. Grahame is telling us the action that follows is INEVITABLE given what came before. The cause-and-effect is doing the work.",
        },
        {
            "substring": '"Bother!" and "O blow!" and also "Hang spring-cleaning!"',
            "category": "tone",
            "note": "The Mole's three little exclamations are escalating. Notice they're mild, almost prim — Grahame writes the Mole as a polite small creature whose biggest swearwords are 'Bother!' and 'Hang!'",
        },
        {
            "substring": "bolted out of the house without even waiting to put on his coat",
            "category": "inference",
            "note": "We infer the strength of the spring-pull from this small detail. A careful, house-proud creature LEAVES HIS COAT BEHIND. That tells us how powerful the urge was without naming it.",
        },
    ],
    "discussion_prompts": [
        "The Mole's exclamations are 'Bother!' 'O blow!' 'Hang spring-cleaning!' What kind of character do these phrases reveal?",
        "Find the sentence where the focus shifts from the Mole's chores to the outside world. What word marks the shift?",
        "Grahame writes 'divine discontent and longing.' What does this phrase mean in context? Why these adjectives?",
        "The Mole leaves without his coat. Why is this small detail the most important in the passage?",
    ],
}

# ─────────────────────────────────────────────────────────────────────
# 014 — The Road Not Taken (Robert Frost, Medium, Poetry)
# ─────────────────────────────────────────────────────────────────────
frost_road_passage = (
    "Two roads diverged in a yellow wood,\n"
    "And sorry I could not travel both\n"
    "And be one traveler, long I stood\n"
    "And looked down one as far as I could\n"
    "To where it bent in the undergrowth;\n\n"
    "Then took the other, as just as fair,\n"
    "And having perhaps the better claim,\n"
    "Because it was grassy and wanted wear;\n"
    "Though as for that the passing there\n"
    "Had worn them really about the same,\n\n"
    "And both that morning equally lay\n"
    "In leaves no step had trodden black.\n"
    "Oh, I kept the first for another day!\n"
    "Yet knowing how way leads on to way,\n"
    "I doubted if I should ever come back.\n\n"
    "I shall be telling this with a sigh\n"
    "Somewhere ages and ages hence:\n"
    "Two roads diverged in a wood, and I—\n"
    "I took the one less traveled by,\n"
    "And that has made all the difference."
)

frost_road = {
    "id": "lab-014-the-road-not-taken",
    "title": "The Road Not Taken",
    "author": "Robert Frost",
    "year": 1916,
    "source_url": "https://www.gutenberg.org/files/59824/59824-h/59824-h.htm",
    "category": "Poetry",
    "difficulty": "Medium",
    "length_words": 144,
    "intro": (
        "Famously misread. The poem is usually quoted as a call to take the unusual path — "
        "but Frost is more careful than that. Watch what the speaker actually says about "
        "the two roads in stanzas 2 and 3, then look at the future tense in stanza 4. "
        "The tone shifts in important ways."
    ),
    "passage": frost_road_passage,
    "annotations_spec": [
        {
            "substring": "Two roads diverged in a yellow wood",
            "category": "structure",
            "note": "The setup, in one line. The choice is established before anything else. Notice the season — 'yellow' wood means autumn, a time of endings and decisions.",
            "occurrence": 1,
        },
        {
            "substring": "sorry I could not travel both",
            "category": "tone",
            "note": "The tone of regret arrives immediately. Before the speaker even picks, he's already mourning the path he can't take. This sets up the whole poem.",
        },
        {
            "substring": "long I stood",
            "category": "inference",
            "note": "We infer the difficulty of the choice from this small detail. The speaker doesn't rush — he STANDS, considering. This isn't a casual fork in the road.",
        },
        {
            "substring": "Then took the other, as just as fair",
            "category": "evidence",
            "note": "Critical line. The second road is 'just as fair' as the first. Frost is telling us the roads are EQUAL — the popular reading ('I took the bold path') is wrong here.",
        },
        {
            "substring": "Because it was grassy and wanted wear",
            "category": "evidence",
            "note": "The reason given for the choice: this road 'wanted wear' (needed walking). It seems like the less-traveled road. But read the next two lines carefully...",
        },
        {
            "substring": "Though as for that the passing there\nHad worn them really about the same",
            "category": "evidence",
            "note": "The quiet retraction. The speaker corrects himself: actually, the roads were worn 'really about the same.' This is the line readers usually skip.",
        },
        {
            "substring": "In leaves no step had trodden black",
            "category": "evidence",
            "note": "More evidence the roads were equally untouched. Fresh leaves on both. There's no 'less traveled' road in the actual moment of choice.",
        },
        {
            "substring": "I doubted if I should ever come back",
            "category": "theme",
            "note": "The theme arrives: choices are irreversible. Not because the road is rare, but because 'way leads on to way' — one decision opens new decisions that take you further from the original fork.",
        },
        {
            "substring": "I shall be telling this with a sigh",
            "category": "structure",
            "note": "The poem JUMPS in time. Stanzas 1–3 are present; stanza 4 is the future. The speaker is predicting how he'll talk about today, years from now.",
        },
        {
            "substring": "with a sigh",
            "category": "tone",
            "note": "'A sigh' is ambiguous — relief? regret? satisfaction? Frost picks the most uncertain word possible. The future story will have a complicated feeling.",
        },
        {
            "substring": "I took the one less traveled by",
            "category": "inference",
            "note": "The famous line. But look — the SPEAKER OF THE FUTURE says this. The speaker of the present (stanzas 2–3) just said the roads were equal. We infer he will REWRITE the story over time.",
        },
        {
            "substring": "And that has made all the difference.",
            "category": "theme",
            "note": "Read this with the rest of the poem in mind. The 'difference' is not that he took the rarer road — he didn't. The difference is that he chose at all. Or: the difference is the story he tells himself.",
        },
    ],
    "discussion_prompts": [
        "What do stanzas 2 and 3 say about how different the two roads actually were?",
        "Why does Frost have the speaker say 'I shall be telling this with a sigh' — what does the future tense do?",
        "The famous line 'I took the one less traveled by' is sometimes called the most misread line in American poetry. Why might that be?",
        "What single word would change if you wanted to make this poem clearly mean 'take the brave path'? What does Frost do instead?",
    ],
}

# ─────────────────────────────────────────────────────────────────────
# 015 — Stopping by Woods on a Snowy Evening (Robert Frost, Medium, Poetry)
# ─────────────────────────────────────────────────────────────────────
frost_woods_passage = (
    "Whose woods these are I think I know.\n"
    "His house is in the village though;\n"
    "He will not see me stopping here\n"
    "To watch his woods fill up with snow.\n\n"
    "My little horse must think it queer\n"
    "To stop without a farmhouse near\n"
    "Between the woods and frozen lake\n"
    "The darkest evening of the year.\n\n"
    "He gives his harness bells a shake\n"
    "To ask if there is some mistake.\n"
    "The only other sound's the sweep\n"
    "Of easy wind and downy flake.\n\n"
    "The woods are lovely, dark and deep,\n"
    "But I have promises to keep,\n"
    "And miles to go before I sleep,\n"
    "And miles to go before I sleep."
)

frost_woods = {
    "id": "lab-015-stopping-by-woods",
    "title": "Stopping by Woods on a Snowy Evening",
    "author": "Robert Frost",
    "year": 1923,
    "source_url": "https://www.gutenberg.org/cache/epub/70961/pg70961.txt",
    "category": "Poetry",
    "difficulty": "Medium",
    "length_words": 108,
    "intro": (
        "Four stanzas of four lines each. A man stops on a winter road to watch snow fall "
        "into woods. Nothing dramatic happens — but Frost packs the whole poem with "
        "tension. Watch the final two lines, where the same sentence is repeated. Why?"
    ),
    "passage": frost_woods_passage,
    "annotations_spec": [
        {
            "substring": "Whose woods these are I think I know.",
            "category": "structure",
            "note": "The poem opens with a thought, not a description. The speaker is already thinking about who OWNS these woods — a small worry hidden inside what looks like a peaceful scene.",
        },
        {
            "substring": "His house is in the village though",
            "category": "inference",
            "note": "We infer the speaker is RELIEVED the owner isn't here. He can stop without being seen. This is the first sign that stopping is not quite allowed.",
        },
        {
            "substring": "To watch his woods fill up with snow.",
            "category": "tone",
            "note": "The scene is quiet, almost still. Notice the verb 'fill up' — not 'cover' or 'blanket.' Frost picks a word that suggests slowness, accumulation, an ongoing process.",
        },
        {
            "substring": "My little horse must think it queer",
            "category": "structure",
            "note": "The horse appears. The speaker projects his own awareness onto the horse — meaning the horse is really a stand-in for the speaker's own sense that something is off.",
        },
        {
            "substring": "The darkest evening of the year.",
            "category": "tone",
            "note": "'The darkest evening of the year' — winter solstice. The line lands heavy because of its specific calendar weight. Tone shifts from quiet to somber.",
        },
        {
            "substring": "He gives his harness bells a shake\nTo ask if there is some mistake.",
            "category": "inference",
            "note": "The horse's shake is interpreted as a question. We infer the speaker has been still long enough that even the horse notices. He's been there A WHILE.",
        },
        {
            "substring": "The only other sound's the sweep\nOf easy wind and downy flake.",
            "category": "tone",
            "note": "The world has gone almost silent. 'Easy wind' and 'downy flake' are soft, gentle words. The whole stanza is the quietest part of the poem.",
        },
        {
            "substring": "The woods are lovely, dark and deep,",
            "category": "theme",
            "note": "Three adjectives. 'Lovely' is welcoming; 'dark and deep' is forbidding. The same woods are TWO things at once. The line is the poem's central tension in five words.",
        },
        {
            "substring": "But I have promises to keep,",
            "category": "structure",
            "note": "The 'But' is the turn. The speaker breaks his own spell. The lovely woods are not for him — there's work, duty, a life to return to.",
        },
        {
            "substring": "And miles to go before I sleep,",
            "category": "evidence",
            "note": "First time. On its surface: literal miles before bed. The line could end the poem here.",
        },
        {
            "substring": "And miles to go before I sleep.",
            "category": "theme",
            "note": "But Frost repeats the line. The repetition forces the second reading — 'sleep' starts to sound like something bigger than bedtime. The 'miles' become the whole rest of life.",
        },
    ],
    "discussion_prompts": [
        "Why does Frost end the poem by repeating the same line? What does the second 'And miles to go before I sleep' MEAN that the first one didn't?",
        "The woods are called 'lovely, dark and deep.' What does Frost do by piling three different adjectives together?",
        "Find the horse. What is the horse's role in the poem — what work does the animal do?",
        "Look at the rhyme scheme. The last stanza breaks the pattern of the first three. What does the change accomplish?",
    ],
}

# ─────────────────────────────────────────────────────────────────────
# Generate all files
# ─────────────────────────────────────────────────────────────────────
ENTRIES = [
    ("010-tortoise-and-hare.json",       tortoise),
    ("011-lion-and-mouse.json",          lion),
    ("012-who-has-seen-the-wind.json",   wind),
    ("013-wind-in-the-willows-opening.json", willows),
    ("014-the-road-not-taken.json",      frost_road),
    ("015-stopping-by-woods.json",       frost_woods),
]


def emit_one(filename: str, entry: dict) -> None:
    passage = entry["passage"]
    specs = entry.pop("annotations_spec")
    entry["annotations"] = build_annotations(passage, specs)

    # Reorder keys so output reads naturally.
    ordered = {
        "id": entry["id"],
        "title": entry["title"],
        "author": entry["author"],
        "year": entry["year"],
        "source_url": entry["source_url"],
        "category": entry["category"],
        "difficulty": entry["difficulty"],
        "length_words": entry["length_words"],
        "intro": entry["intro"],
        "passage": passage,
        "annotations": entry["annotations"],
        "discussion_prompts": entry["discussion_prompts"],
    }

    out_path = LAB_DIR / filename
    out_path.write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  ✓ {out_path.relative_to(REPO_ROOT)} ({len(passage)} chars, {len(entry['annotations'])} annotations)")


def main() -> int:
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating into {LAB_DIR.relative_to(REPO_ROOT)}/ …")
    for filename, entry in ENTRIES:
        emit_one(filename, entry)
    print(f"Done. Generated {len(ENTRIES)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
