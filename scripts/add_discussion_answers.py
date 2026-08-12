#!/usr/bin/env python3
"""Add `discussion_answers` (parallel array to `discussion_prompts`) to every lab JSON.

Each answer is a short teacher-style suggested response (1-4 sentences) —
not a definitive answer, just enough to seed a discussion.

Run from repo root:
    python3 scripts/add_discussion_answers.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LAB_DIR = REPO_ROOT / "content" / "lab"


ANSWERS: dict[str, list[str]] = {

    # ─── 001 Sonnet 18 ─────────────────────────────────────────────
    "001-sonnet-18.json": [
        # 1. Why is 'But' the most important structural move?
        "It is the volta — the turn. Everything before it (lines 1-8) builds a problem: summer is a flawed comparison. 'But' announces that the rest of the poem will give the answer. One three-letter word splits the sonnet into 'setup' and 'payoff.'",
        # 2. Purpose of listing summer's flaws BEFORE praising the beloved?
        "Shakespeare is preparing the reader to dismiss the obvious comparison. By the time line 9 arrives, we already agree summer is unreliable — so when he claims the beloved is BETTER than summer, the claim feels earned, not flattering.",
        # 3. What does the final couplet's promise of immortality suggest about tone?
        "Confident, almost boastful. Shakespeare is claiming his own poem will preserve the beloved across time. The tone shifts from praise to a quiet announcement of his own power as a poet — the poem itself is the gift.",
        # 4. Tone shift from lines 1-8 to lines 9-14?
        "Lines 1-8 are exploratory and slightly anxious — summer keeps failing as a comparison. Lines 9-14 are decisive and triumphant — once Shakespeare turns, he commits. The shift is from questioning to declaring.",
    ],

    # ─── 002 Gettysburg ────────────────────────────────────────────
    "002-gettysburg-address.json": [
        # 1. Where do past/present/future begin? Why this order?
        "PAST begins 'Four score and seven years ago…' (paragraph 1). PRESENT begins 'Now we are engaged…' (paragraph 2). FUTURE begins 'It is for us the living…' (last paragraph). The order moves listeners from founding ideal → current crisis → call to action. You can't make the call before grounding the principle.",
        # 2. Purpose of 'we can not dedicate / consecrate / hallow'?
        "Three things at once: rhythm makes the line memorable; the religious vocabulary (consecrate, hallow) raises the stakes; the triple denial signals that ordinary words aren't powerful enough — only the dead can consecrate this ground.",
        # 3. Why does the dead's sacrifice matter (final long sentence)?
        "Lincoln says: because they died, WE must take 'increased devotion' to the cause they died for — so that the government 'of the people, by the people, for the people' will not perish. The sacrifice has meaning only if democracy survives.",
        # 4. Tone shift between paragraphs 2 and 3?
        "Paragraph 2 is solemn and quiet — we have come, we are met, it is fitting and proper. Paragraph 3 becomes urgent and forward-looking — 'it is for us the living, rather, to be dedicated…' Language of duty replaces language of mourning.",
        # 5. Why end with 'of the people, by the people, for the people'?
        "The three repetitions give the phrase weight and rhythm — it sounds inevitable. Each preposition is doing a different job: government BELONGING to citizens (of), RUN BY citizens (by), SERVING citizens (for). A simpler phrase couldn't carry all three claims.",
    ],

    # ─── 003 Walden ────────────────────────────────────────────────
    "003-walden-i-went-to-the-woods.json": [
        # 1. What does the accumulation of intensity-words tell you about attitude?
        "Thoreau treats his project as serious work, not vacation. The accumulation of 'deliberately,' 'essential,' 'sturdily,' 'Spartan-like' tells you he is going to the woods to LIVE harder, not easier — to engage with life, not retreat from it.",
        # 2. Why distinguish his goal from 'resignation'?
        "Because someone might assume retreating to the woods means giving up on regular life. Thoreau rejects that reading explicitly. His goal is the opposite — to engage with life so completely that nothing essential is missed.",
        # 3. Why commit to publishing the truth either way?
        "Because for Thoreau the goal is KNOWING, not finding a particular result. If life turns out to be mean (small, ugly), that truth is worth reporting too. He values honesty over comfort.",
        # 4. Most important word — defend the choice.
        "Strong candidates: 'deliberately,' 'essential,' 'know.' Best argument for 'deliberately': it carries the whole project's attitude in one word — chosen, careful, intentional. Strong argument for 'know': it names the final goal, which is understanding rather than experience.",
    ],

    # ─── 004 Huck Finn ─────────────────────────────────────────────
    "004-huck-finn-opening.json": [
        # 1. What do ungrammatical phrases tell you?
        "Huck is uneducated, working-class, speaks in dialect. He sounds like a real boy, not a literary narrator. But — and this is the trick — the same boy is also careful and observant. The grammar tells us about his class; what he NOTICES tells us about his mind.",
        # 2. What does 'mainly' do?
        "It quietly undermines the claim. 'He told the truth, mainly' = he told the truth most of the time but not always. Huck is implying Twain is partly a liar — which is funny, because Huck is the character Twain invented to say so.",
        # 3. A place Huck reveals his character indirectly?
        "Many options: 'or maybe Mary' (hesitation = careful weighing); 'laughed at them for their pains' (the boy noticed the cruelty); 'I never seen anybody but lied' (cynical worldview for a child). Any of these shows Huck's mind without him describing himself.",
        # 4. Why does Huck repeat 'a true book, with some stretchers'?
        "Real people repeat themselves when they speak. Twain is mimicking spoken storytelling, not polished prose — so the circling back is part of the voice. It also reinforces the book's central tension: truth vs. stretching.",
    ],

    # ─── 005 Gift of the Magi ──────────────────────────────────────
    "005-gift-of-the-magi-opening.json": [
        # 1. Why is the five-word opening strong?
        "Specific and small. Five words = scarcity in form, not just content. The exact amount ('eighty-seven cents,' not 'a little money') makes the reader feel the precision of poverty. And it raises a question: what does someone with $1.87 DO?",
        # 2. Show poverty without saying 'poor'?
        "Examples: 'sixty cents of it was in pennies' (savings in the smallest possible coin); 'bulldozing the grocer and the vegetable man and the butcher' (haggling daily, with shame); 'furnished flat at $8 per week' (cheap rent, weekly, not monthly). Each detail PROVES poverty by showing its behavior.",
        # 3. Is 'life is made up of sobs, sniffles, and smiles' theme or joke?
        "Both. It is funny because it is so confidently generalizing from one woman's bad afternoon. It is also a real claim — O. Henry believes life leans toward small sadnesses. The narrator can mock and mean it at the same time.",
        # 4. Tone change paragraphs 1-3?
        "Paragraph 1: precise, matter-of-fact (Della counting). Paragraph 3: dry, almost legalistic ('mendicancy squad'). What stays the same: warmth — O. Henry never mocks Della herself, only the situation. The narrator is on her side throughout.",
    ],

    # ─── 006 Boy Who Cried Wolf ────────────────────────────────────
    "006-boy-who-cried-wolf.json": [
        # 1. Structural turn — what word marks it?
        "'However.' It signals a contradiction is coming: the pattern (false alarms, neighbors come) is about to break. The word 'however' tells the reader 'this time is different' before the sentence finishes.",
        # 2. Why no explanation of why neighbors don't come?
        "Because the cause is obvious — the prior lies. Aesop trusts the reader to infer it. Spelling out 'the neighbors had stopped believing him' would be condescending and would slow the fable.",
        # 3. Why is 'at his leisure' bleak?
        "It means the wolf isn't even in a hurry. No tension, no struggle — the boy's crisis is just the wolf's quiet meal. The phrase makes the boy's mistake feel total: the consequences happen calmly, like the universe doesn't care.",
        # 4. Why 'no believing a liar' instead of 'don't lie'?
        "'Don't lie' aims at the liar. Aesop aims somewhere subtler: at the LISTENERS. Once a liar speaks, no one will believe them — even when they are telling the truth. The moral is about credibility, which lasts beyond the lie itself.",
    ],

    # ─── 007 All the world's a stage ───────────────────────────────
    "007-all-the-worlds-a-stage.json": [
        # 1. Master metaphor in your own words?
        "The world is a theatre; people are actors playing fixed roles. The metaphor works for 28 lines because it can absorb every kind of human life — infant, schoolboy, lover, soldier, judge, old man, dying — and treat each as a 'part' in the same play.",
        # 2. Where does tone shift from comic to serious?
        "Around the sixth age (the lean, slippered old man). Up through the justice, Shakespeare is gently mocking. The decline of the body — clothes too big, voice turning childish — is the first stage that isn't funny. The seventh age ('mere oblivion') seals it.",
        # 3. Why end with 'sans teeth, sans eyes, sans taste, sans everything'?
        "The repetition (anaphora) lands the loss rhythmically. The specificity (teeth, eyes, taste) makes the absence physical, not abstract. An abstract statement like 'and then we die' would be forgettable; this catalogs the EMPTYING of a person.",
        # 4. Most vivid age?
        "Common winners: the lover ('sighing like furnace, with a woeful ballad / Made to his mistress' eyebrow') — the absurd specific image makes it work. Or the soldier ('seeking the bubble reputation / Even in the cannon's mouth') — the bubble metaphor is unforgettable. Defend your pick by naming the specific words.",
    ],

    # ─── 008 Tomorrow ──────────────────────────────────────────────
    "008-tomorrow-and-tomorrow.json": [
        # 1. Four images for life — what does each add?
        "Candle: brief and easily blown out. Walking shadow: insubstantial, going through motions without weight. Poor player: performing badly for a fixed time then exiting. Tale told by an idiot: noise without sense. Each shrinks life further: from brief → empty → bad performance → meaningless noise.",
        # 2. Difference from Jaques' 'All the world's a stage'?
        "Jaques uses the stage metaphor with detached amusement — life as comic theatre with stages. Macbeth uses the same metaphor with despair — life as a bad performance that ends in silence. Same image, opposite emotional weight.",
        # 3. Why end on 'signifying nothing'?
        "'Nothing' is the bleakest noun available. Ending on it deflates everything before it — the sound and fury build energy, the last word releases it into emptiness. The smallness of the final word IS the point: life ends in zero.",
        # 4. Why is 'full of sound and fury' so often quoted?
        "It captures a feeling many people have — that life is loud and emotionally intense yet ultimately pointless. Two nouns, monosyllables, hard consonants. The phrase sounds like the experience it names: big, energetic, going nowhere.",
    ],

    # ─── 009 Tale of Two Cities ────────────────────────────────────
    "009-tale-of-two-cities-opening.json": [
        # 1. What does the repetition accomplish?
        "The contradictions pile up rather than cancel out. Each pair adds to a growing sense that the era was EVERYTHING at once. A varied sentence ('It was an era of contradiction') would be a claim ABOUT the period; the repetition makes you FEEL the contradiction.",
        # 2. What does 'in short' do?
        "It signals a summary is coming — and undercuts the grand language of the first half with a casual phrase. The tone steps down from biblical (epoch, incredulity) to conversational. Dickens is winking.",
        # 3. What's Dickens claiming about his own time (1859)?
        "That 1859 (when he is writing) is just as full of contradiction and superlative rhetoric as 1789 (the French Revolution). The historical novel is also a quiet warning about the present — read about France to understand England.",
        # 4. Why one sentence?
        "Because the era can't be split into pieces — the contradictions exist simultaneously. Breaking it into ten sentences would suggest the eras alternated; one sentence forces them to coexist. The sentence's FORM is the argument.",
    ],

    # ─── 010 Tortoise and Hare ─────────────────────────────────────
    "010-tortoise-and-hare.json": [
        # 1. The two strategies?
        "Hare: rely on natural speed; race in bursts. Tortoise: keep moving without stopping, regardless of pace. The Hare bets on talent; the Tortoise bets on consistency.",
        # 2. Hare's character shown without telling?
        "'Ridiculed' (the Hare mocks the Tortoise's body); 'believing her assertion to be simply impossible' (instant overconfidence); 'lying down by the wayside, fell fast asleep' (treats the race as too easy to bother). Every action proves arrogance without the word being used.",
        # 3. Why 'slow but steady' instead of 'don't be lazy'?
        "'Don't be lazy' attacks one habit. 'Slow but steady' makes a positive claim about HOW to win — consistency beats bursts. Aesop's version is more useful: it tells you what to DO, not just what to avoid.",
        # 4. Where does the outcome become inevitable?
        "'The Hare, lying down by the wayside, fell fast asleep.' Once he sleeps, the race is decided — even if he wakes early, he can't be sure how far ahead the Tortoise has gone. The single sentence is the structural turn.",
    ],

    # ─── 011 Lion and Mouse ────────────────────────────────────────
    "011-lion-and-mouse.json": [
        # 1. What changes when the Mouse delivers the moral?
        "It feels EARNED instead of preached. A narrator declaring a moral keeps the lesson outside the story; the Mouse saying it makes the lesson part of the action. The character who proved the claim gets to make the claim.",
        # 2. Why include the Lion's laughter?
        "The laughter establishes the SCALE of the lesson. If the Lion had been polite or neutral, the reversal would feel small. The laughter makes him wrong in a specific way — proud — which the rescue then humbles. Without the laugh, the moral has no target.",
        # 3. Parallel between scenes?
        "Scene 1: Mouse is helpless, Lion has the power to spare or kill. Scene 2: Lion is helpless, Mouse has the power to free or leave. The roles invert exactly. The structural symmetry IS the moral — power changes hands.",
        # 4. Moral delivery vs Boy Who Cried Wolf?
        "Boy Who Cried Wolf states the moral as a separate sentence ('There is no believing a liar…'). Lion and Mouse puts the moral inside the Mouse's dialogue. Same genre, two different placements — one narrator-led, one character-led.",
    ],

    # ─── 012 Who Has Seen the Wind? ────────────────────────────────
    "012-who-has-seen-the-wind.json": [
        # 1. Tiny differences between stanzas?
        "Differences: (a) 'I nor you' → 'you nor I' (pronouns swap); (b) 'leaves hang trembling' → 'trees bow down their heads' (smaller plants → bigger plants; smaller motion → bigger motion); (c) 'passing through' → 'passing by' (direction changes). Each variation makes the wind feel bigger and the world more affected.",
        # 2. Why not name the wind directly?
        "Because the poem's argument is that we don't see the wind — we see its effects. Naming the wind in the noun position would defeat the poem. The trembling and bowing ARE the wind, in the only way we can know it.",
        # 3. What's the poem really about?
        "Plausible deeper readings: God (an invisible force known only through visible effects); time; emotion; any unseen power. The poem teaches a reading habit — look for what something DOES, not just what it IS. That habit applies far beyond wind.",
        # 4. Sample new stanza?
        "Example: 'Who has seen the cold? / Neither you nor me: / But when the windows fog up white, / The cold is keeping company.' The exercise reveals how strict Rossetti's form is — question + denial + 'But when…' + visible-effect line.",
    ],

    # ─── 013 Wind in the Willows ───────────────────────────────────
    "013-wind-in-the-willows-opening.json": [
        # 1. What does the Mole's exclamations reveal?
        "Mild, polite, slightly old-fashioned — even his swears are tame. The Mole is house-proud, careful, the kind of creature whose worst word is 'Bother!' That tells you what kind of book this will be: comic, warm, never violent.",
        # 2. Shift from chores to outside world — what word marks it?
        "The sentence 'Spring was moving in the air above and in the earth below and around him…' The word 'Spring' (capitalized in some editions) shifts the focus. Before that sentence we're indoors; after it we're inside a force much bigger than the room.",
        # 3. 'Divine discontent and longing' — meaning + word choice?
        "A holy restlessness. 'Divine' suggests the urge comes from somewhere larger than the Mole himself; 'discontent' names the restlessness; 'longing' adds direction (toward something, not just away from something). Together the phrase makes spring feel like a calling.",
        # 4. Why is leaving without his coat the most important detail?
        "Because it proves the strength of the urge without naming it. A careful, indoor creature LEAVES HIS COAT BEHIND. Grahame never writes 'he was overwhelmed' — the abandoned coat tells you exactly that.",
    ],

    # ─── 014 Road Not Taken ────────────────────────────────────────
    "014-the-road-not-taken.json": [
        # 1. How different were the roads?
        "Barely at all. Stanza 2: the second road is 'just as fair' and 'the passing there / Had worn them really about the same.' Stanza 3: 'both that morning equally lay / In leaves no step had trodden black.' Frost says clearly: the roads were EQUAL in the moment of choice.",
        # 2. What does 'I shall be telling this with a sigh' do?
        "It puts the famous line in the future tense — meaning the heroic 'less traveled' speech is something the speaker PREDICTS he will say, not what he believes now. The future tense quietly distances the speaker from the story he'll tell.",
        # 3. Why is the famous line so often misread?
        "Quoted out of context, it sounds like advice to take the bold path. But the line is what the FUTURE speaker says — and the poem just told us the present speaker thought the roads were equal. Readers skip the qualifier ('with a sigh,' 'ages and ages hence') and treat the line as Frost's claim, not a character's predicted self-mythologizing.",
        # 4. What single word would change to make it 'take the brave path'?
        "If 'sigh' were 'smile,' the future story would be triumphant instead of complicated. Or if 'doubted' (in stanza 3) were 'knew,' the speaker would be certain instead of uncertain. Frost picks ambiguity at every choice point — that's the poem's argument.",
    ],

    # ─── 015 Stopping by Woods ─────────────────────────────────────
    "015-stopping-by-woods.json": [
        # 1. Why repeat the final line?
        "First time: literal — miles before bedtime. Second time: metaphorical — 'sleep' starts to mean death, and 'miles' become the rest of life. The repetition forces the second reading. The same words mean two different things, depending on which one we just heard.",
        # 2. What does the trio 'lovely, dark and deep' do?
        "Two opposing pulls in one phrase. 'Lovely' invites; 'dark and deep' warns. Three adjectives create a small list, which feels more considered than 'beautiful but dangerous.' The line packs the whole poem's tension into five words.",
        # 3. The horse's role?
        "A non-human stand-in for the speaker's own awareness. The speaker projects his uncertainty onto the horse ('must think it queer'), and reads the horse's bell-shake as a question. The horse is the speaker's own caution, externalized.",
        # 4. Rhyme scheme change in the last stanza?
        "Stanzas 1-3 follow AABA — the third line introduces a new sound that becomes the next stanza's main rhyme. The last stanza is AAAA — no escape sound, no link to a next stanza. The rhyme tells you the poem is ENDING and the speaker isn't moving forward to anything new.",
    ],
}


def main() -> int:
    for filename, answers in ANSWERS.items():
        path = LAB_DIR / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        prompts = data.get("discussion_prompts", [])
        if len(answers) != len(prompts):
            print(f"  ✗ {filename}: {len(answers)} answers vs {len(prompts)} prompts — MISMATCH")
            continue
        data["discussion_answers"] = answers
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  ✓ {filename}: added {len(answers)} answers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
