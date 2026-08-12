# Curriculum Design — Break 250 Reading

**Status:** Draft v3.1 — Vocabulary expanded to 3 modules; B2 adds informational inference; explicit MVP tier (2026-05-27)
**Author:** Architect (Claude)
**Date:** 2026-05-27
**Audience:** ELA subject-matter experts, classroom teachers, reading specialists, and dev reviewers
**See also:** `docs/why_250.md` — public-facing manifesto on why MAP 250+ requires author-thinking comprehension.

---

## 1. Purpose of this document

Lock the curriculum — the **categories, modules, and sub-concepts** the app will teach, and **which of them ship in Launch v1** — before any lesson copy, quiz, or UI work begins.

**v3.x is a structural redesign** to mirror MAP Reading's three scored sub-areas: **Literary Text, Informational Text, Vocabulary**. The previous v2.x organized by skill (Tone, Evidence, Inference, etc.); v3.0 introduced the category structure; **v3.1** (this draft) expanded Vocabulary into 3 modules and added explicit informational inference to Category B, plus an MVP tier. A student who needs to lift their Literary Text score has a clear path through Category A; a student weak in Vocabulary has a clear path through Category C.

The trap-led sub-concept design, the per-choice feedback teaching engine, and the locked CSV schemas (v1.0) are unchanged.

---

## 2. Product context (one minute)

**Break 250 Reading** is a focused web app for advanced Grade 5–8 readers (MAP Reading ~230–249) who already read well but plateau in analytical reading questions. The product hypothesis: these students have heard ELA terms like *tone, evidence, inference* but don't use them as **tools**.

MAP Reading scores break down into three sub-areas:

- **Literary Text** — fiction, narrative, poetry. Inference, tone, character, theme, figurative language.
- **Informational Text** — nonfiction, articles, history. Argument, structure, evidence, purpose.
- **Vocabulary** — context-based meaning, connotation, word precision.

(MAP also reports a Lexile range, but that is a derived measure of overall text difficulty, not a separately taught category.)

Each MAP category has its own score, and a plateaued reader near 250 is usually uneven across them. **Break 250 mirrors the three categories so improvement maps directly to where a student is losing points.**

**The user experience for one sub-concept** (anywhere in Modules A1–C3):

1. Pick a sub-concept (e.g., A4 → "Neutral vs Skeptical").
2. Read a short mini-lesson (3–5 min).
3. Study 2–5 worked examples.
4. Take 10 quizzes (8–12 min) targeting that sub-concept.
5. See per-choice feedback explaining why the correct answer is right and why each wrong answer is tempting.

**Module 0 is intentionally different** — orientation only, not scored.

---

## 3. Design principles for the curriculum

1. **Category-aligned with MAP scoring.** The three top-level categories (A Literary, B Informational, C Vocabulary) match MAP's reported sub-areas so progress in the app maps directly to where students gain points.
2. **Concept-as-tool.** Every sub-concept must be something a student can *name* and *use* on a fresh passage.
3. **Trap-led.** Every sub-concept names the trap it disarms.
4. **Sub-concept count is reviewer-driven, not capped.** Each earns its slot by disarming a real trap that supports 10 trap-revealing quizzes.
5. **No vocabulary memorization, no fluency, no test-strategy fluff.** Vocabulary in Category C is decoding + lexicon-building, not flashcards.
6. **One pedagogically-honest layer.** Better to ship 30 strong sub-concepts than 60 mixed-quality ones.
7. **One sub-concept = one mini-lesson + 10 quizzes** (everywhere except Module 0).
8. **Module 0 is a deliberate exception** — orientation across all three categories, completion-only, not scored.
9. **Launch v1 ships a P0 subset.** The full curriculum is the master map; P0 is what ships first.

---

## 4. Module list (organized by category)

```
Module 0 — Reading-Analysis Abstract (orientation across all three categories)

Category A — Literary Text
  A1. Theme & Central Idea
  A2. Inference & Character
  A3. Point of View & Narrator
  A4. Tone & Mood
  A5. Figurative Language & Poetry

Category B — Informational Text
  B1. Main Idea & Central Idea
  B2. Evidence & Inference (Informational)
  B3. Author's Purpose
  B4. Tone & Word Choice (in nonfiction)
  B5. Text Structure & Development
  B6. Argument & Comparison

Category C — Vocabulary
  C1. Context Meaning
  C2. Word Nuance & Precision
  C3. Academic & Tone Lexicon
```

**Fourteen modules + Module 0.** Sub-concept IDs use the form `A1.1`, `A1.2`, `B3.2`, `C1.3`, etc. File paths: `content/lessons/a1/01-theme-vs-topic.csv` and similar.

---

## 4.1 Launch v1 scope

Priority labels:

| Label | Meaning |
|---|---|
| **P0** | Must-have for Launch v1. |
| **P1** | Important for full v1 expansion (post-launch). |
| **P2** | Good to add later. |

**Launch v1 totals (P0 + Module 0):**

| Category / Module | P0 sub-concepts | Quizzes |
|---|---:|---:|
| 0. Reading-Analysis Abstract | (1 lesson, not scored) | 10 |
| **Category A — Literary Text** | | |
| A1. Theme & Central Idea | 2 | 20 |
| A2. Inference & Character | 4 | 40 |
| A3. Point of View & Narrator | 1 | 10 |
| A4. Tone & Mood | 3 | 30 |
| A5. Figurative Language & Poetry | 4 | 40 |
| **Subtotal A** | **14** | **140** |
| **Category B — Informational Text** | | |
| B1. Main Idea & Central Idea | 2 | 20 |
| B2. Evidence & Inference (Informational) | 4 | 40 |
| B3. Author's Purpose | 4 | 40 |
| B4. Tone & Word Choice (nonfiction) | 3 | 30 |
| B5. Text Structure & Development | 4 | 40 |
| B6. Argument & Comparison | 3 | 30 |
| **Subtotal B** | **20** | **200** |
| **Category C — Vocabulary** | | |
| C1. Context Meaning | 3 | 30 |
| C2. Word Nuance & Precision | 1 | 10 |
| C3. Academic & Tone Lexicon | 2 | 20 |
| **Subtotal C** | **6** | **60** |
| **Launch v1 TOTAL** | **40 + Module 0** | **410** |

**Volume tiers:**

| Tier | Sub-concepts | Quizzes |
|---|---:|---:|
| **MVP (first ship, vocab-first subset of P0)** | **22 + 1** | **230** |
| Launch v1 (full P0 + Module 0) | 40 + 1 | 410 |
| Full v1 (P0 + P1 + Module 0) | 56 + 1 | 570 |
| Master curriculum (all + Module 0) | 65 + 1 | 660 |

*MVP composition (22 sub-concepts):* all 6 Category C P0 (vocabulary — the bottleneck), plus 9 Category A P0 (theme + inference + tone basics + imagery + speaker), plus 7 Category B P0 (main idea + evidence basics + paragraph function + neutral vs skeptical worked sample). Designed so a student weak in any of the 3 MAP categories has at least 5 sub-concepts of practice to lift their score immediately.

---

## 5. Modules and sub-concepts

For each module: short definition, why it matters, then the sub-concepts with priority labels. **Each sub-concept becomes its own mini-lesson + 10 quizzes** (except Module 0). Each sub-concept names the **trap** it disarms.

---

### 5.0 Module 0 — Reading-Analysis Abstract (special case)

> Give students the map of the three MAP categories and the tools inside each, so they recognize which tool a question is testing before they apply it.

**Priority:** P0 (always ships at launch).
**Student-facing name:** TBD by UI/copy phase. Candidates: *The 3 Reading Areas*, *Reading Analysis Map*, *The Reading Toolkit*.

#### Why Module 0 exists

Plateaued students have heard the terms (tone, evidence, inference, etc.) but don't see them as a *system* tied to *measurable categories*. Module 0 gives the system and explicitly maps each tool to a MAP-scoring category.

Serves three user types:
- **Lazy student** — only does Module 0. Still walks away understanding the 3 reading areas and that ELA terms are tools, not jargon.
- **Serious student** — uses Module 0 as a roadmap.
- **Parent / teacher** — reads Module 0 to understand the app's philosophy and how it maps to the score.

#### Mini-lesson contents (500–800 words)

1. What is reading analysis? (vs reading more)
2. The big questions advanced readers ask
3. The 3 MAP categories (Literary, Informational, Vocabulary) and the tools inside each
4. How test questions hide the tool
5. How to use the rest of this app

#### The 3 categories and their core tools (preview list inside the mini-lesson)

| Category | Core tools |
|---|---|
| **Literary Text** | Theme · Inference · Character · Point of View · Tone & Mood · Figurative Language · Poetry |
| **Informational Text** | Main Idea · Evidence · Author's Purpose · Tone & Word Choice · Text Structure · Argument |
| **Vocabulary** | Context Meaning · Connotation · Academic Verbs · Tone Words · Word Precision |

#### Basic reader vs Advanced reader (lifted into the mini-lesson)

| Basic reader asks | Advanced reader asks |
|---|---|
| What happened? | Why did the author write it this way? |
| What is the topic? | What is the central idea or theme? |
| What does this word mean? | What feeling or attitude does this word create? |
| What is the answer? | What exact evidence proves the answer? |
| What does the paragraph say? | What job does this paragraph do? |
| What is the claim? | What evidence and assumptions support it? |

#### Quiz format — recognition, not mastery

All 10 quizzes are **"identify the tool"** questions. Each sample question maps to a specific module across the three categories.

#### Scoring and UI handling

Module 0 is **not scored**. Status displayed is **"Orientation Complete"**, not a score. The dashboard separates Module 0 visually from the rest.

---

## Category A — Literary Text

Skills for reading fiction, narrative, and poetry. Maps directly to the MAP "Literary Text" sub-score.

---

### 5.A1 Module A1 — Theme & Central Idea (literary)

> What the narrative is really saying about life, people, or the world.

Plateaued readers name the **topic** ("friendship") and call it the theme. A real theme is a complete claim about the topic, supported by the whole text.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| A1.1 | **Theme Is a Message, Not a Topic** — theme is a complete sentence about life, not the subject word. | "The theme is friendship." (That's a topic.) | P0 |
| A1.2 | **Theme Is Supported by Multiple Details** — not just one event. | Drawing a theme from a single moment. | P0 |
| A1.3 | **Multiple Themes** — most stories carry several. | Assuming a single "right" theme. | P1 |
| A1.4 | **Universal vs Text-Specific Theme** — themes generalize beyond the story. | Writing a theme that's only about the specific characters. | P2 |

**Total: 4 sub-concepts (2 P0, 1 P1, 1 P2) → 40 quizzes (20 at launch).**

---

### 5.A2 Module A2 — Inference & Character

> Conclusions drawn from clues in narrative — character actions, dialogue, scene details — that aren't directly stated.

Plateaued readers in narrative texts either under-infer (read only literally) or over-infer (use outside knowledge).

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| A2.1 | **Inference = Clue + Reasoning** — must be grounded in the text. | Pure speculation. | P0 |
| A2.2 | **Inference from Character Action** — actions reveal feelings and motives. | Stating the action instead of what it implies. | P0 |
| A2.3 | **Inference vs Stated Fact** — if the text says it, it's not an inference. | Choosing a stated fact when an inference is asked. | P0 |
| A2.4 | **Avoiding Over-Inference** — only as far as the text supports. | Pulling in outside knowledge. | P0 |
| A2.5 | **Inference from Word Choice in Narrative** — connotation reveals tone. | Literal reading. | P1 |

**Total: 5 sub-concepts (4 P0, 1 P1) → 50 quizzes (40 at launch).**

---

### 5.A3 Module A3 — Point of View & Narrator

> Whose voice the reader hears, and how trustworthy that voice is.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| A3.1 | **Narrator vs Author** — narrator is *in* the story; author is outside it. | Confusing what the narrator believes with what the author believes. | P0 |
| A3.2 | **Reliable vs Unreliable Narrator** — narrators can mislead. | Trusting first-person narration uncritically. | P2 |

**Total: 2 sub-concepts (1 P0, 1 P2) → 20 quizzes (10 at launch).**

---

### 5.A4 Module A4 — Tone & Mood (in fiction)

> The author's or speaker's attitude in narrative writing, and the feeling the writing creates in the reader.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| A4.1 | **Tone vs Topic in Fiction** — what the story is ABOUT vs how the author FEELS about it. | Naming the topic. | P0 |
| A4.2 | **Identifying Tone Words in Fiction** — adjectives, verbs, qualifiers that reveal attitude. | Ignoring word choice. | P0 |
| A4.3 | **Mood vs Tone** — tone is author-side attitude; mood is reader-side feeling. | Conflating them. | P0 |
| A4.4 | **Tone Shifts in Narrative** — tone can change as a story moves. | Assigning one tone to the whole text. | P1 |
| A4.5 | **Irony and Sarcasm** — author means opposite of literal. | Literal reading. | P1 |

**Total: 5 sub-concepts (3 P0, 2 P1) → 50 quizzes (30 at launch).**

---

### 5.A5 Module A5 — Figurative Language & Poetry

> Language that means more than its literal words, plus poetry-specific tools.

Figurative moments often carry the central meaning. The high-value moves at this level are imagery, symbolism, speaker-vs-poet, line break, and tone shift in poetry.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| A5.1 | **Imagery Creates Meaning** — sensory detail shapes feeling and theme. | Treating imagery as decoration. | P0 |
| A5.2 | **Symbolism** — a concrete thing standing for an abstract idea. | Forcing symbols where none exist (or missing real ones). | P0 |
| A5.3 | **Simile vs Metaphor** — comparison with "like/as" vs direct equation. | Confusing them. | P1 |
| A5.4 | **Speaker (not the Poet)** — the speaker is a voice in the poem, not necessarily the author. | Reading every "I" as the poet. | P0 |
| A5.5 | **Line Break** — where the line ends shapes meaning and rhythm. | Ignoring line breaks. | P0 |
| A5.6 | **Personification** — non-human given human traits. | Missing the emotional implication. | P1 |
| A5.7 | **Hyperbole and Understatement** — deliberate exaggeration or downplay. | Literal reading. | P2 |
| A5.8 | **Repetition** — repeated words/phrases signal what matters. | Not noticing what's repeated. | P2 |
| A5.9 | **Tone Shift in Poetry** — poems often pivot at a specific line. | Assigning one tone to the whole poem. | P2 |

**Total: 9 sub-concepts (4 P0, 2 P1, 3 P2) → 90 quizzes (40 at launch).**

---

## Category B — Informational Text

Skills for reading nonfiction, articles, opinion pieces, and history. Maps directly to the MAP "Informational Text" sub-score.

---

### 5.B1 Module B1 — Main Idea & Central Idea (informational)

> What the article or essay is really saying about its topic.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| B1.1 | **Topic vs Main Idea** — topic is the subject; main idea is what the author says about it. | Students name the topic when asked for main idea. | P0 |
| B1.2 | **Main Idea vs Supporting Detail** — details prove the main idea but aren't IT. | Picking a true detail instead of the central point. | P0 |
| B1.3 | **Stated vs Implied Main Idea** — sometimes a thesis sentence, sometimes you synthesize. | Only looking for an explicit thesis. | P1 |
| B1.4 | **Paragraph-level vs Whole-text Main Idea** — each paragraph has its own; the text has an overall one. | Treating paragraph 2's main idea as the whole text's. | P2 |

**Total: 4 sub-concepts (2 P0, 1 P1, 1 P2) → 40 quizzes (20 at launch).**

---

### 5.B2 Module B2 — Evidence & Inference (Informational)

> The exact words from a nonfiction text that prove an answer, and the conclusions you can draw from informational cues.

The #1 advanced trap is **related-but-not-proven** — answers that sound connected but aren't actually supported. Informational inference (drawing conclusions from data, claims, and stated facts) is a distinct MAP-tested skill and lives here, not in Category A.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| B2.1 | **Evidence Must Be Traceable to the Text** — you can explain in your own words, but you must be able to point to the exact words. | Summarizing without being able to locate proof. | P0 |
| B2.2 | **Best-Supported Answer** — multiple choices may have some support; pick the strongest. | "Any evidence is enough" thinking. | P0 |
| B2.3 | **Proof vs Related Information** — the #1 advanced trap. | Choosing the answer that "sounds connected" without proof. | P0 |
| B2.4 | **Where to Find Evidence** — paragraph/sentence locality; scope of the question. | Searching the whole text when the question scopes to one paragraph. | P1 |
| B2.5 | **Inference from Nonfiction Cues** — drawing conclusions from data, claims, and stated facts in informational text. | Treating nonfiction inference as guesswork or as identical to literary inference. | P0 |
| B2.6 | **Avoiding Over-Conclusion** — only as far as the data and claims support. | Generalizing beyond what the facts prove. | P1 |

**Total: 6 sub-concepts (4 P0, 2 P1) → 60 quizzes (40 at launch).**

---

### 5.B3 Module B3 — Author's Purpose

> Why the author wrote this — inform, persuade, entertain, or finer.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| B3.1 | **Three Core Purposes** — inform, persuade, entertain. | Assuming nonfiction always = inform. | P0 |
| B3.2 | **Finer Purposes** — explain, warn, critique, celebrate, satirize. | Stopping at the broad three. | P0 |
| B3.3 | **Purpose vs Main Idea** — purpose = WHY; main idea = WHAT. | Blending them. | P0 |
| B3.4 | **Identifying Purpose from Word Choice** — loaded words reveal persuasive intent. | Missing rhetoric in seemingly informational text. | P0 |
| B3.5 | **Texts with Multiple Purposes** — inform + persuade is common in editorials. | Assuming one purpose. | P1 |
| B3.6 | **Bias and Slant** — even nonfiction texts have a perspective. | Treating any text as objectively neutral. | P2 |

**Total: 6 sub-concepts (4 P0, 1 P1, 1 P2) → 60 quizzes (40 at launch).**

---

### 5.B4 Module B4 — Tone & Word Choice (in nonfiction)

> The author's attitude in nonfiction, revealed through diction. The most-missed distinction here is **neutral vs skeptical**.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| B4.1 | **Neutral vs Skeptical** — the most-missed distinction at advanced levels. | Defaulting to "neutral" when subtle doubt is present. | P0 |
| B4.2 | **Identifying Tone Words in Nonfiction** — hedging verbs, contrast words, distancing phrases. | Ignoring word choice. | P0 |
| B4.3 | **Word Choice Creates Tone** — "claimed" ≠ "said." | Missing the substitution. | P0 |
| B4.4 | **Loaded Words / Charged Vocabulary** — emotionally weighted words in argumentative writing. | Not noticing the emotional pull. | P1 |
| B4.5 | **Formal vs Casual Diction** — register signals audience and purpose. | Ignoring register. | P1 |

**Total: 5 sub-concepts (3 P0, 2 P1) → 50 quizzes (30 at launch).**

*Note: this module is where the worked sample for P0-4 lives. The sample's content is unchanged from v2.x; only its location/ID changed (was `m4/4.3`; now `b4/B4.1`).*

---

### 5.B5 Module B5 — Text Structure & Development

> How a nonfiction text organizes its ideas.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| B5.1 | **Five Common Structures** — cause-effect, compare-contrast, sequence, problem-solution, description. | No vocabulary for structure. | P0 |
| B5.2 | **Signal Words** — because, however, first, although, in contrast. | Missing the signal. | P0 |
| B5.3 | **Paragraph Function** — introduce, provide example, give evidence, show contrast, conclude. | Thinking every paragraph "explains." | P0 |
| B5.4 | **Sequence vs Cause/Effect** — because one event comes after another doesn't mean it caused it. | Mistaking time order for causation. | P0 |
| B5.5 | **Structure Reveals Argument** — the structure mirrors the author's reasoning. | Reading structure as decoration. | P1 |
| B5.6 | **Openers and Closers** — opening sets up; closing seals. | Skimming the structural anchors. | P2 |

**Total: 6 sub-concepts (4 P0, 1 P1, 1 P2) → 60 quizzes (40 at launch).**

---

### 5.B6 Module B6 — Argument & Comparison

> Claims supported by evidence and reasoning, and how to compare claims across texts.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| B6.1 | **Claim, Evidence, Reasoning** — the three legs. | Conflating them. | P0 |
| B6.2 | **Assumption** — unstated belief connecting evidence to claim. | Missing it entirely. | P0 |
| B6.3 | **Counterclaim and Rebuttal** — strong arguments anticipate opposing views. | Missing the rebuttal move. | P0 |
| B6.4 | **Strong vs Weak Evidence** — relevance, specificity, source quality. | Counting evidence by quantity instead of quality. | P1 |
| B6.5 | **Emotional Appeal vs Logical Evidence** — language that moves feeling vs language that presents reasons. | Mistaking emotional language for strong evidence. | P1 |
| B6.6 | **Compare Viewpoints** — comparing claims across two short texts. | Treating two texts as making the same claim when they don't. | P2 |

**Total: 6 sub-concepts (3 P0, 2 P1, 1 P2) → 60 quizzes (30 at launch).**

---

## Category C — Vocabulary

Decoding unfamiliar words, identifying nuance, and building the lexicon advanced readers use. Distinctly **not** flashcard memorization. Maps directly to the MAP "Vocabulary" sub-score, which is often the single biggest unlocking factor for plateaued readers.

---

### 5.C1 Module C1 — Context Meaning

> Decoding unfamiliar words from the text around them. The foundational vocabulary skill: how to read a word you've never seen before.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| C1.1 | **Context Meaning** — use surrounding sentences to infer the meaning of an unfamiliar word. | Skipping unfamiliar words, or guessing from word-parts alone. | P0 |
| C1.2 | **Connotation from Context** — figure out positive/negative/neutral feeling when the word is new. | Treating connotation as a memorized property rather than something context reveals. | P0 |
| C1.3 | **Figurative Word Meaning** — when a familiar word is used non-literally (evoke a feeling; undermine an argument; mirror an idea). | Reading figuratively-used words literally. | P0 |

**Total: 3 sub-concepts (3 P0) → 30 quizzes (30 at launch).**

---

### 5.C2 Module C2 — Word Nuance & Precision

> Distinguishing words that look similar but signal different things. The trap-density module of Category C.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| C2.1 | **Word Precision** — distinguishing near-synonyms (suggests vs proves; reluctant vs unwilling; ambiguous vs unclear; concede vs admit). | Treating near-synonyms as interchangeable. | P0 |
| C2.2 | **Hedge vs Strong Claim** — "claimed" vs "showed"; "alleged" vs "demonstrated"; how verb choice signals certainty. | Missing the strength difference between superficially similar verbs. | P1 |

**Total: 2 sub-concepts (1 P0, 1 P1) → 20 quizzes (10 at launch).**

---

### 5.C3 Module C3 — Academic & Tone Lexicon

> Building the specific lexicon advanced readers need: the academic verbs and tone words that name what authors do and how they feel.

| # | Sub-concept | Trap it disarms | Priority |
|---|---|---|:-:|
| C3.1 | **Academic Verbs** — assert, imply, concede, scrutinize, undermine, refute, emphasize, contrast. | Glossing over the verbs that signal what the author is doing. | P0 |
| C3.2 | **Tone Vocabulary** — building a lexicon of tone words (skeptical, nostalgic, dismissive, reflective, urgent, cautious, admiring, critical). | Not having a wide enough vocabulary to name the tone correctly even after spotting it. | P0 |

**Total: 2 sub-concepts (2 P0) → 20 quizzes (20 at launch).**

---

**Category C total: 7 sub-concepts (6 P0, 1 P1) → 70 quizzes (60 at launch).**

*Note:* split from a single C1 module in v3.0 to three C1/C2/C3 modules in v3.1 per reviewer feedback. Vocabulary is the #1 unlocking factor per the MAP-data analysis; granting it the structural weight of 3 modules matches Categories A (5) and B (6) more proportionally and lets the launch lead with vocabulary content.

---

## 6. Cross-category overlaps (intentional, not bugs)

The 3-category structure mirrors MAP scoring; pedagogically, some skills span more than one category. Those overlaps are *features* — students see the same skill applied in different text types and recognize it as a transferable tool.

| Overlap | Why we keep both |
|---|---|
| **A2 Inference (literary) ↔ B2 Inference (informational)** | Inference is a transferable skill but signals differ. A2 teaches "clue + reasoning" from narrative cues (action, dialogue, scene). B2.5/B2.6 teach "claim + data + valid conclusion" from informational cues. Same underlying move; different surface. |
| **A4 Tone (fiction) ↔ B4 Tone (nonfiction)** | Tone exists in both, but the diction signals differ. Fiction tone shows in dialogue, narrative voice, sensory cues. Nonfiction tone shows in hedging verbs and contrast words. Two modules so students learn both signals. |
| **A4.2 Identifying Tone Words ↔ C3.2 Tone Vocabulary** | A4.2 = scanning text for tone-revealing diction. C3.2 = building the lexicon (skeptical, nostalgic, etc.) so you can NAME the tone correctly once you've spotted it. Different angle. |
| **B3 Author's Purpose ↔ B6 Argument** | When purpose = persuade, argument analysis kicks in. B6 lessons assume B3. |
| **B4.3 Word Choice Creates Tone ↔ C1.2 Connotation from Context** | B4.3 is in-text reading; C1.2 is decoding an unfamiliar word's feeling from context. Cross-references both ways. |
| **B4.4 Loaded Words ↔ C2.2 Hedge vs Strong Claim** | B4.4 catches loaded vocabulary in argumentative writing; C2.2 trains the discrimination at word-pair level. |
| **A5 Figurative Language ↔ A1 Theme** | Figurative moments often carry theme. A1 lessons can use a figurative passage; A5 lessons can lift theme as the interpretive payoff. |

Mini-lessons should *cross-reference* each other across these overlaps.

---

## 7. Quiz coverage strategy

**Modules A1–C3:** 10 quizzes per sub-concept. All 10 target the same sub-concept at varying formats and difficulties.

Each quiz row carries a `trap_type` tag (the parent sub-concept ID, e.g., `B4.1-neutral-vs-skeptical`).

**Recommended default mix (per sub-concept, 10 quizzes total):**

| Category | Count |
|---|---|
| Pure concept identification | 2 |
| Worked sentence-level example | 2 |
| Short-passage application | 4 |
| Wrong-answer-trap focus | 1 |
| Evidence selection | 1 |

**Module 0 is different:** all 10 quizzes are recognition-format. Not scored.

---

## 8. What was carried over from v2.4 and what changed

| v2.4 → v3.x mapping | Notes |
|---|---|
| Old Module 1 (Central Idea / Theme) → split into A1 (Theme, literary) and B1 (Main Idea, informational) | The merged module conflated two distinct testing contexts. |
| Old Module 2 (Evidence & Inference) → split into A2 (Inference & Character, literary) and B2 (Evidence, informational) | Inference is primarily a literary skill in MAP scoring; Evidence is primarily informational. |
| Old Module 3 (Purpose & POV) → split into A3 (POV, literary) and B3 (Purpose, informational) | POV is narrative-specific; Purpose is mostly informational. |
| Old Module 4 (Tone & Word Choice) → split into A4 (Tone & Mood, fiction) and B4 (Tone & Word Choice, nonfiction) | Tone signals differ markedly by text type. Worked sample for P0-4 moves to B4.1. |
| Old Module 5 (Text Structure) → B5 (Text Structure & Development) | Structure is primarily an informational skill. |
| Old Module 6 (Argument & Comparison) → B6 (Argument & Comparison) | Argument is informational. |
| Old Module 7 (Figurative Language & Poetry) → A5 (Figurative Language & Poetry) | Figurative and poetry are literary. |
| Old Module 8 (Vocabulary in Context) → C1 + C2 + C3 (split in v3.1) | Elevated to its own top-level category in v3.0; expanded to 3 modules in v3.1. |
| v3.0 B2 (Evidence only) → v3.1 B2 (Evidence & Inference, Informational) | Added B2.5 Inference from Nonfiction Cues and B2.6 Avoiding Over-Conclusion to capture informational inference explicitly. |
| Most P0/P1/P2 priorities preserved | Some promotions in v3.1: C1.3 Figurative Word Meaning P1 → P0; C2.1 Word Precision P1 → P0. |

---

## 9. Open questions for reviewers

Resolved from earlier rounds:
- **Granularity:** Path C hybrid (Module 0 special; per-sub-concept elsewhere). Settled.
- **Tone+Word Choice merge:** YES — now lives as two modules (A4 + B4) reflecting the category split.
- **Module 0 scoring:** Completion-only.
- **Launch v1 size (Q12):** P0 set ships. Count evolved: v3.0 increased it via the literary/nonfiction Tone split (350 → 380); v3.1 increased it further via Vocabulary expansion to 3 modules (C1+C2+C3) and Category B inference addition (B2.5, B2.6) — current full P0 = 410 quizzes. MVP tier = 230 quizzes is what ships first.

Resolved in v3.1:
- ~~Inference split (A2 vs B-Inference)~~ — B2 expanded to "Evidence & Inference (Informational)" with B2.5 + B2.6 added.
- ~~Module C1 split into C1 + C2 + C3~~ — split done: C1 Context Meaning, C2 Word Nuance & Precision, C3 Academic & Tone Lexicon.

Open in v3.1:

1. **Is the 3-category structure right?** Major restructure. Reviewers should validate before content authoring proceeds at scale.
2. **Tone split (A4 vs B4):** correct call? Or should there be one Tone module that uses both fiction and nonfiction passages?
3. **Module A4.5 (Irony and Sarcasm)** could double as A5 (Figurative Language) — same trap. Keep where?
4. **Priority labels:** are P0/P1/P2 assignments correct under the new structure?
5. **Module 0 quizzes** — should the 10 recognition quizzes split into ~3-4 per category (so students see questions from each category in orientation)?
6. **Worked sample (P0-4 = old Tone 4.3 = new B4.1):** unchanged content, new ID. Confirm renaming is fine.
7. **Coverage check:** what advanced reading move that *should* be in this curriculum is missing entirely?
8. **MVP tier (22 sub-concepts / 230 quizzes):** is the proposed composition right? Specifically, are these the right 22? Adjust if needed.
9. **Possible MVP demotion (per GPT review 2):** B3.2 Finer Purposes from P0 → P1 if MVP needs to tighten further. Currently kept at P0. Reviewers can vote.

---

## 10. What this doc deliberately does NOT decide

Downstream of curriculum approval:

- Tech stack
- UI / page layout
- Progress tracking (localStorage vs accounts)
- Content authoring style guide
- Sample passage sourcing and copyright
- Pilot recruitment, consent forms, age gating
- Student-facing names for categories and modules (TBD by UI/copy phase)

---

## 11. What I'm asking reviewers to do

Read §4 (module list), §4.1 (launch scope and MVP composition), §5 (modules and sub-concepts including Module 0), and §9 (open questions). Specifically:

- **Validate the 3-category structure.** This is the v3.x thesis — push back hard if categories are wrong or if a key skill is misfiled.
- Strike-through sub-concepts that don't earn their slot.
- Add sub-concepts that are missing.
- Flag any sub-concept whose trap is invented / weak.
- Push back on P0/P1/P2 labels — these determine launch composition.
- Validate the MVP 22-sub-concept composition.
- Vote on the 9 open questions in §9.

---

## Appendix A — Change log

| Version | Date | Changes |
|---|---|---|
| v1 | 2026-05-26 | Initial draft. 10 concepts. Trap-led. |
| v2 | 2026-05-26 | Added Module 0. 10 concepts → 8 modules. |
| v2.1 | 2026-05-26 | Priority labels (P0/P1/P2) added. Launch v1 scope. |
| v2.2 | 2026-05-26 | GPT reviewer fixes. Module 7 P0 swap. |
| v2.3 | 2026-05-27 | Q12 locked at 310 quizzes. |
| v2.4 | 2026-05-27 | Module 8 Vocabulary in Context added. `docs/why_250.md` created. |
| v3.0 | 2026-05-27 | Structural redesign: 3 MAP scoring categories. 8 modules → 12 + Module 0. Tone split (A4+B4). Vocabulary elevated. Worked sample moved to B4.1. |
| v3.1 | 2026-05-27 | Vocabulary expanded (1 module → 3 modules: C1 Context Meaning, C2 Word Nuance & Precision, C3 Academic & Tone Lexicon). B2 expanded to "Evidence & Inference (Informational)" with B2.5 + B2.6 added. Promotions: C1.3 P1→P0, C2.1 P1→P0. Explicit MVP tier (230 quizzes). Final counts: P0=40, P1=16, P2=9 (total 65). |
| v3.1.1 | 2026-05-27 | Cleanup pass per GPT review 2. Fixed stale v3.0/v2.x references across all 3 docs. |
| v3.1.2 | 2026-05-27 | Cleanup per GPT review 3. csv_schemas.md c2/c3 added across file layout, rules, module_id set, validation rule. §9 renamed and renumbered. |
| **v3.1.3** | **2026-05-27** | **Module 0 schema exception added** per GPT review 4: when `module_id == "m0"`, `common_trap_1` and `example_1_*` may be `N/A`. Updated csv_schemas.md (column-rule table notes, validation rules section, Module 0 specifics section, and Zod reference implementation with a `.refine()` enforcing the m0 exception). Also: csv_schemas.md "updated for v3.0" headings → "v3.x"; curriculum_design.md §8 "v2.4 → v3.0 mapping" → "v2.4 → v3.x mapping"; §9 stale Launch v1 size note rewritten to capture v3.0 → v3.1 evolution (350 → 380 → 410 quizzes; MVP = 230). B4.1 worked sample re-validated against the new semantics — still passes. |

---

## Appendix B — Cross-reference to `design1.md` and v2.x

`design1.md` is the original product spec (now superseded). v2.x was the 8-module skill-organized curriculum. **v3.1 (this doc) is canonical.**

For the mapping from v2.4 sub-concept IDs to v3.x IDs, see §8.
