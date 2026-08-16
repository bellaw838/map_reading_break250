# MAP Reading Break 250 — 51-Flag Fix Specification

**Source checked:** the live `main` branch and deployed quiz content on 2026-08-15  
**Audience:** developer/content editor  
**Voice target:** direct, natural English for strong readers ages 10–14; do not rewrite the site into academic or AI-sounding prose.

## Count reconciliation

The requested counts add up once the lesson-level problems are separated from the question-level problems:

| Level | Action | Count |
|---|---:|---:|
| Lesson rules/examples | Global fix | 4 |
| Quiz questions | Replace completely | 2 |
| Quiz questions | Revise materially | 24 |
| Quiz questions | Minor edit | 21 |
| **Total flags** |  | **51** |

The **47 question-level changes** below were also checked for answer-length clues:

- Maximum choice-length spread after the proposed edits: **4 words**
- Correct answer uniquely longest: **0 of 47**
- “Always choose a longest option” expected accuracy across these 47 items: **25%**

## Implementation rules

1. Keep the existing `quiz_id`, `question_number`, `trap_type`, and `difficulty` unless this document explicitly changes them.
2. For each item, fields not listed under **Apply these changes** remain unchanged.
3. Keep the runtime answer shuffle. Store correctness by the stable choice/key, not by a displayed letter.
4. When a keyed interpretation is only *possible*, either add a clue that makes it best supported or soften the answer. Do not defend ambiguity with longer feedback.
5. Preserve Bella’s voice: prefer “best supported,” “seems uneasy,” and “look at the clues” over formal phrases such as “analytical-answer selection.”
6. After editing, run `python3 scripts/validate-content.py`, then complete the QA checks at the end of this document.

---

# A. Four lesson-level fixes

These should be applied before or at the same time as the question changes, so lesson rules and quiz feedback do not contradict one another.

## G1 — Theme: remove the fixed three-moment rule and automatic symbol/change rules

**File:** `content/lessons/a1/02-theme-multiple-details.csv`

The live lesson is already improved in several places, but three old absolutes remain.

### 1. Replace the “list 3 specific moments” paragraph in `mini_lesson`

**Find the paragraph beginning:**

> After writing a theme as a sentence, list 3 specific moments...

**Replace it with:**

> After writing a theme as a sentence, point to a meaningful pattern across the text. That pattern might be two or more central moments, a repeated contrast, a character’s change across several scenes, or an ending that brings earlier details together. Do not use a fixed number as proof. The real question is whether the theme explains the text as a whole rather than one isolated moment.

### 2. Replace the recurring-object example fields

```text
example_3_answer = "Signal to investigate — recurrence shows importance, not automatically theme."
example_3_explanation = "When an object returns, ask what changes around it and what the object comes to mean. It may support theme, character, mood, or plot. Repetition alone does not decide which."
```

### 3. Replace the character-change example fields

```text
example_4_answer = "Strong theme clue — the change can help reveal the theme."
example_4_explanation = "The change is evidence, not usually the complete theme. Ask what the change suggests about people, choices, or life."
```

---

## G2 — Inference: allow ordinary background knowledge, reject unsupported story details

**Files:**

- `content/lessons/a2/01-inference-clue-reasoning.csv`
- `content/lessons/a2/04-avoiding-over-inference.csv`

### A2.1 changes

Replace the final mini-lesson section beginning **“Use what you know, but don’t invent story details.”** with:

> **Use what you know to connect the clues, but keep the answer anchored in this text.**  
> Ordinary knowledge helps you understand that repeated clock-checking may show impatience or worry. The mistake is using a stereotype, genre expectation, or invented backstory when this passage gives no supporting clue.

Replace:

```text
common_trap_2 = "Using a general expectation without checking whether this text supports it."
```

### A2.4 changes

Replace:

```text
subtitle = "Infer only as far as the text supports — do not add motives, causes, history, or future events the passage never gives you."
common_trap_1 = "Adding unsupported story details and calling them inference."
example_1_answer = "Over-inference — unsupported extra detail."
example_1_explanation = "Loving to read does not establish Mia’s grades. The reader added a story fact that the text never supports."
```

In `mini_lesson`, replace the sentence:

> If you find yourself thinking “well, in real life this would mean...”, pull back...

with:

> Real-life knowledge may suggest a possibility. Before choosing it, check whether this passage gives a clue for that specific conclusion. If not, it is speculation.

Replace the final rule:

> Stay one step beyond the text. Not two. Not three.

with:

> Go beyond what is stated only as far as the clues can carry you. Choose the strongest supported conclusion—not the biggest one and not the vaguest one.

---

## G3 — Nonfiction inference: remove unsupported motive and causation examples

**File:** `content/lessons/b2/05-inference-from-nonfiction.csv`

### 1. Policy/complaints example

The lesson currently treats the authors’ refusal to comment as evidence that they may be unwilling to defend the policy. That assigns a motive.

Replace the example’s inference and explanation with:

```text
example_1_answer = "The rise in complaints raises questions about whether the policy is working as intended; the article gives no explanation from the policy’s authors."
example_1_explanation = "The complaint trend supports concern about the result. The lack of comment tells us only that no explanation is provided here; it does not prove why the authors stayed silent."
```

Make the same change in the worked example inside `mini_lesson`: remove “the authors may be unwilling to defend the policy publicly.”

### 2. Music/silence example

Replace the study text, answer, and explanation with:

```text
example_3_text = "A study randomly assigned 200 students to two otherwise identical study sessions. Group A studied with music. Group B studied in silence. Group B scored higher on the same test."
example_3_answer = "For this task, studying in silence may have helped performance."
example_3_explanation = "Random assignment and otherwise identical sessions make silence a reasonable possible explanation. The hedge “may” matters, and one study does not prove that silence is best for every student or task."
```

---

## G4 — Skeptical tone: make context—not individual reporting verbs—the deciding factor

**File:** `content/lessons/b4/01-neutral-vs-skeptical.csv`

Most of this lesson is already corrected. Two example explanations still overstate individual verbs.

Replace the explanation for the eco-friendly bottle example with:

```text
example_1_explanation = "The skepticism comes mainly from the contrast between the eco-friendly claim and the nearly unchanged plastic use. “Claimed” can be neutral by itself; the surrounding contradiction creates the doubtful framing."
```

Replace the explanation for the supporters/traffic example with:

```text
example_3_explanation = "The skepticism comes from “however” plus the early data that challenges the supporters’ prediction. “Argue” attributes their position; it does not automatically signal doubt."
```

**Do not re-edit the C3.1 academic-verbs lesson.** The live version now correctly distinguishes `refute` from `challenge`, `dispute`, and `rebut`.

---

# B. Replace two questions completely

For these two items, changing one answer or one feedback line is not enough. Replace all listed content fields.


## P1 — `a1-1_q10` — Theme: replace the ambiguous “signal words” item

**File:** `content/quizzes/a1/01-theme-message-not-topic.csv`  
**Why replace:** Both “is about” and “about courage” can signal that the draft names a topic instead of making a theme claim.

### Replace the row’s content fields with

```text
prompt = "What is missing from this draft theme? \"The story is about courage.\""
choice_a = "A claim about what the story says about courage."
choice_b = "The title and names of the main characters."
choice_c = "A summary of the story’s single most dramatic scene."
choice_d = "A quotation in which a character mentions courage."
correct_choice = "A"
feedback_a = "Correct. A theme does more than name courage as the topic. It makes a claim about what the story suggests about courage."
feedback_b = "Tempting because titles and characters identify the story. But they do not turn a topic into a message about life or people."
feedback_c = "Tempting because a dramatic scene may support the theme. But a summary tells what happens; it does not state the larger message."
feedback_d = "Tempting because a quotation can provide evidence. But evidence supports a theme after the theme has been stated; it is not the missing theme claim."
```


## P2 — `c3-2_q04` — Tone vocabulary: replace the nostalgic/wistful/reflective overlap

**File:** `content/quizzes/c3/02-tone-vocabulary.csv`  
**Why replace:** The current sentence can reasonably be called nostalgic, wistful, or reflective, so it does not have one clearly best answer.

### Replace the row’s content fields with

```text
prompt = "Read: \"Every autumn, he takes out the unused train ticket and imagines the journey he never made.\" The tone is:"
choice_a = "Wistful"
choice_b = "Jubilant"
choice_c = "Detached"
choice_d = "Accusing"
correct_choice = "A"
feedback_a = "Correct. The unused ticket and the journey he never made create gentle longing mixed with regret, which is wistful."
feedback_b = "Jubilant means openly joyful or triumphant. This sentence looks back at a missed chance, not a victory."
feedback_c = "Detached means emotionally uninvolved. Taking out the ticket every year shows that the missed journey still matters to him."
feedback_d = "Accusing tone blames someone. The sentence expresses longing and regret without blaming another person."
```


---

# C. Revise 24 questions materially

These items can keep their IDs and lesson placement, but they need a real content change—not only punctuation or softer feedback.


## R01 — `a1-2_q06` — Recurring object: make recurrence a clue, not automatic proof of theme

**File:** `content/quizzes/a1/02-theme-multiple-details.csv`  
**Problem:** A recurring object may be symbolic, thematic, personal, or plot-important. Recurrence proves emphasis, not one particular function.

### Apply these changes

```text
prompt = "Across a story, the same worn photograph appears in three different scenes. What does this most safely signal?"
choice_a = "The object is important and may carry meaning beyond itself."
choice_b = "The object only makes the setting feel more realistic."
choice_c = "The object must reveal one character’s personal history."
choice_d = "The object must later become important to the main plot."
correct_choice = "A"
feedback_a = "Correct. Repetition signals importance. Check the surrounding scenes before deciding whether the photograph works as a symbol, a theme clue, a plot clue, or more than one of these."
feedback_b = "Tempting because concrete objects can make a setting believable. But “only” is too narrow when the author deliberately returns to the object."
feedback_c = "Tempting because a worn photograph may connect to someone’s past. But recurrence alone does not prove whose history it reveals."
feedback_d = "Tempting because repeated objects often matter to the plot. But “must” goes too far; the repetition may mainly build meaning or emotion."
```


## R02 — `a1-2_q09` — Teaching pattern: add an outcome that supports the intended theme

**File:** `content/quizzes/a1/02-theme-multiple-details.csv`  
**Problem:** The current passage shows the sister returning, but it does not show that her return makes learning possible. The distractor about skills taking different amounts of time is directly supported.

### Apply these changes

```text
prompt = "Read: An older sister teaches her younger brother to ride a bike, do a card trick, and tie a knot. He struggles and fails several times. Each week she returns and practices with him again. By the end of the month, he can do all three. Which theme is best supported by the whole pattern?"
choice_a = "Good teachers never become frustrated with struggling learners."
choice_b = "Some skills are naturally easier to learn than others."
choice_c = "Patient support can help someone keep going through failure."
choice_d = "One hard skill makes every later skill easier."
correct_choice = "C"
feedback_a = "Tempting because the sister stays patient. But “never” is too absolute, and the passage does not describe every feeling she has."
feedback_b = "True in the passage, but incomplete. Different difficulty is part of the setup; the repeated support and eventual success carry the larger message."
feedback_c = "Correct. The brother fails more than once, the sister keeps returning, and he eventually learns. The whole pattern supports patient support through failure."
feedback_d = "Tempting because the tasks happen in order. But the passage never shows that learning one skill makes the next one easier."
```


## R03 — `a2-2_q04` — Maya and the phone: add evidence that her laugh hurt her friend

**File:** `content/quizzes/a2/02-inference-from-character-action.csv`  
**Problem:** Offering to pay can show concern, but the current passage does not prove that Maya recognized hurt or felt guilty.

### Apply these changes

```text
prompt = "Read: Maya laughed when her friend described the broken phone. Her friend looked down and stopped speaking. Maya’s smile disappeared, and she offered to help pay for the repair. What is the BEST inference?"
choice_a = "Maya is confused about how the phone was broken."
choice_b = "Maya realizes her laugh was hurtful and feels sorry."
choice_c = "Maya thinks paying will make the phone work again."
choice_d = "Maya wants her friend to forget the whole problem."
correct_choice = "B"
feedback_a = "Tempting because a sudden pause can show confusion. But the friend’s reaction and Maya’s changed expression point to social awareness, not puzzlement."
feedback_b = "Correct. The friend looks down and goes quiet; Maya stops smiling and tries to help. Those clues support regret about her first reaction."
feedback_c = "Tempting because she offers money for the repair. But she is offering help, not claiming that money alone will fix everything."
feedback_d = "Tempting because people sometimes use money to end an awkward moment. Nothing here shows that she wants to dismiss or forget the problem."
```


## R04 — `a2-2_q09` — Coach’s reaction: add a clue that separates acceptance from disappointment

**File:** `content/quizzes/a2/02-inference-from-character-action.csv`  
**Problem:** A hand on the shoulder, silence, and a nod can communicate approval, disappointment, reassurance, forgiveness, or mixed feelings.

### Apply these changes

```text
prompt = "Read: After Marco admitted that he had hidden the broken window, Coach’s expression softened. He put a hand on Marco’s shoulder, nodded once, and said, “We’ll deal with the window tomorrow.” What is BEST supported?"
choice_a = "Coach has decided the broken window no longer matters."
choice_b = "Coach is too angry to speak clearly to Marco."
choice_c = "Coach appreciates the honesty, although the damage still matters."
choice_d = "Coach does not understand what Marco has admitted."
correct_choice = "C"
feedback_a = "Tempting because Coach responds calmly. But “we’ll deal with the window tomorrow” shows that the damage still has consequences."
feedback_b = "Tempting because silence can signal anger. Here, however, his expression softens and he responds calmly."
feedback_c = "Correct. The softened expression and touch acknowledge Marco’s honesty, while the final sentence shows that the damage is not being ignored."
feedback_d = "Tempting because Coach pauses. But his direct response about the window shows that he understands the confession."
```


## R05 — `a2-4_q02` — Over-inference test: replace “smallest conclusion” with “unsupported details”

**File:** `content/quizzes/a2/04-avoiding-over-inference.csv`  
**Problem:** The smallest conclusion can be vague or incomplete. The right answer is the strongest exact conclusion the evidence supports.

### Apply these changes

```text
choice_b = "Whether the conclusion adds details the clue cannot support."
feedback_b = "Correct. An inference overreaches when it adds a motive, cause, history, or future event that the clue cannot support. The goal is the strongest supported conclusion, not automatically the smallest one."
choice_d = "Whether it is the most dramatic reading among the choices."
```


## R06 — `a2-4_q07` — “We’ll see”: distinguish useful background knowledge from an unchecked stereotype

**File:** `content/quizzes/a2/04-avoiding-over-inference.csv`  
**Problem:** Readers may use ordinary language knowledge to notice that “we’ll see” can be evasive. The error is treating that usual meaning as certain without checking this scene.

### Apply these changes

```text
choice_b = "The student assumes the usual meaning without checking this scene."
feedback_b = "Correct. Real-life language knowledge can suggest a possibility, but this story’s tone, actions, and later events must support the conclusion. “Usually” is not enough by itself."
choice_d = "The phrase is too common to carry meaning in this scene."
```


## R07 — `a5-1_q06` — Empty-chair imagery: ask what noticing it first reveals

**File:** `content/quizzes/a5/01-imagery-creates-meaning.csv`  
**Problem:** The current correct answer is vaguer than the distractor saying that an important person is missing.

### Apply these changes

```text
prompt = "Read: “He noticed the empty chair at the head of the table before he noticed anything else.” What does noticing the chair first reveal about him?"
choice_a = "He is strongly affected by the person’s absence."
choice_b = "He expects the family to begin dinner soon."
choice_c = "He is counting the furniture around the room."
choice_d = "He thinks the dining room is too large."
correct_choice = "A"
feedback_a = "Correct. The chair catches his attention before everything else, showing that the missing person’s absence matters strongly to him."
feedback_b = "Tempting because the setting suggests a meal. But the sentence emphasizes his attention to one empty place, not the dinner schedule."
feedback_c = "Tempting because he notices a piece of furniture. But nothing suggests that he is counting or inspecting the room."
feedback_d = "Tempting because an empty chair creates unused space. The sentence connects the chair to a missing person, not to the room’s size."
```


## R08 — `b2-1_q10` — Evidence traceability: allow precise paraphrase

**File:** `content/quizzes/b2/01-evidence-traceable.csv`  
**Problem:** A precise paraphrase of a locatable detail can be valid evidence. Quotation marks are not the definition of evidence.

### Apply these changes

```text
prompt = "Why does evidence need to be traceable on a reading test?"
choice_a = "Precise wording sounds more academic and careful to a grader."
choice_b = "Quoted evidence is always stronger than paraphrased evidence."
choice_c = "Another reader can find and check the supporting detail."
choice_d = "Students must memorize the passage before answering."
correct_choice = "C"
feedback_a = "Tempting because precise writing helps. But traceability is about whether the support can be checked, not whether the answer sounds academic."
feedback_b = "Tempting because a quotation is easy to locate. A precise paraphrase can also be strong evidence when another reader can trace it to the passage."
feedback_c = "Correct. Evidence is traceable when another reader can locate the quoted or paraphrased detail and judge whether it supports the answer."
feedback_d = "Tempting because memory can save time. But students can look back; the skill is finding and using the right detail."
```


## R09 — `b2-5_q04` — Music study: add design information before allowing a causal possibility

**File:** `content/quizzes/b2/05-inference-from-nonfiction.csv`  
**Problem:** Two pre-existing groups scoring differently do not show that music or silence caused the difference.

### Apply these changes

```text
prompt = "Read: “A study randomly assigned 200 students to two otherwise identical study sessions. Group A studied with music. Group B studied in silence. Group B scored higher on the same test.” Which is the BEST inference?"
choice_a = "For this task, silence may have helped students perform better."
choice_b = "Music always reduces how much students actually learn."
choice_c = "Group A students did not take the study seriously."
choice_d = "Silence is the best study method for every kind of student."
correct_choice = "A"
feedback_a = "Correct. Random assignment and otherwise identical sessions make silence a reasonable possible explanation, while “may” keeps the claim appropriately cautious."
feedback_b = "Tempting because Group A scored lower. But “always” and “how much students learn” go beyond one task and one study."
feedback_c = "Tempting because effort could affect scores. The passage gives no evidence that the groups differed in seriousness."
feedback_d = "Tempting because Group B did better here. One study cannot establish the best method for every student or every kind of task."
```


## R10 — `b2-5_q09` — Five-percent improvement: describe qualified praise, not unjustified praise

**File:** `content/quizzes/b2/05-inference-from-nonfiction.csv`  
**Problem:** A five-percent gain can reasonably be called encouraging. The comparison makes the praise qualified, not necessarily excessive.

### Apply these changes

```text
choice_b = "The author praises the gain but presents it as comparatively modest."
feedback_b = "Correct. “Encouraging” gives the five-percent gain credit, while the twelve-percent comparison presents it as modest beside the larger result."
```


## R11 — `b2-5_q10` — Data conclusion: replace “smallest” with “strongest fully supported”

**File:** `content/quizzes/b2/05-inference-from-nonfiction.csv`  
**Problem:** The smallest claim may be too weak to answer the question. The aim is calibrated strength.

### Apply these changes

```text
choice_d = "The strongest claim the data fully supports without extra assumptions."
feedback_d = "Correct. A conclusion should say as much as the data justifies, but no more. Avoid both dramatic overreach and answers so vague that they miss the pattern."
choice_c = "A claim that extends the data to many similar situations."
```


## R12 — `b5-3_q02` — Paragraph role: remove the overlapping purpose choice

**File:** `content/quizzes/b5/03-paragraph-function.csv`  
**Problem:** How a paragraph connects to the author’s purpose can be a valid description of the paragraph’s function.

### Apply these changes

```text
choice_d = "The facts and examples that paragraph 3 mentions."
feedback_d = "Tempting because these details tell you what the paragraph contains. But a role question asks what those details do in the argument."
```


## R13 — `b5-3_q09` — Multiple paragraph jobs: make placement the final check, not an absolute rule

**File:** `content/quizzes/b5/03-paragraph-function.csv`  
**Problem:** Counting the dominant kind of sentence and asking why the paragraph appears there are both useful strategies. The current stem makes them compete as universal rules.

### Apply these changes

```text
prompt = "When a paragraph seems to do more than one job, what is the BEST final check?"
feedback_a = "Tempting because the dominant kind of sentence is a useful clue. But sentence count alone can miss the paragraph’s larger job in the argument."
feedback_b = "Correct. After noticing examples, contrasts, or counterarguments, ask which job best explains why the paragraph appears at that point in the argument."
```


## R14 — `c2-1_q04` — Reluctant versus unwilling: use “refused” as the clear stronger contrast

**File:** `content/quizzes/c2/01-word-precision.csv`  
**Problem:** “Unwilling” can overlap with “reluctant”; it does not always mean a final refusal.

### Apply these changes

```text
prompt = "Read: “She was reluctant to leave, but she eventually agreed.” Could “reluctant to leave” be replaced with “refused to leave” without changing the meaning?"
choice_a = "Yes, because both show she preferred to stay."
choice_b = "Yes, because both phrases carry a negative feeling."
choice_c = "No, because reluctant allows hesitation before agreeing."
choice_d = "No, because refused is much more formal."
correct_choice = "C"
feedback_a = "Tempting because both phrases show resistance. But preferring to stay is not the same as refusing to leave."
feedback_b = "Tempting because both are negative. Shared connotation does not make two phrases equal in strength or outcome."
feedback_c = "Correct. Reluctant means hesitant or resistant, but still persuadable. Refused means she did not agree to do it."
feedback_d = "Tempting because “refused” sounds stronger. The important difference is meaning, not formality."
```


## R15 — `c2-1_q09` — Substantial versus significant: test the technical statistical meaning

**File:** `content/quizzes/c2/01-word-precision.csv`  
**Problem:** The current rule “substantial = size, significant = importance” is too rigid; the words overlap, and “significant” also has a technical statistical meaning.

### Apply these changes

```text
prompt = "Which sentence uses “significant” in a way that “substantial” may not match exactly?"
choice_a = "The storm caused significant damage across the coast."
choice_b = "The study found a statistically significant difference between groups."
choice_c = "The company reported a significant increase in yearly sales."
choice_d = "The renovation required a significant amount of new material."
correct_choice = "B"
feedback_a = "Tempting because “significant” works here. “Substantial damage” could also describe a large amount of damage with little change in meaning."
feedback_b = "Correct. “Statistically significant” is a technical research term. “Statistically substantial” is not the same expression."
feedback_c = "Tempting because the increase may be important. “Substantial increase” could also describe a large increase in this context."
feedback_d = "Tempting because the amount may matter. “A substantial amount” is a natural replacement when the focus is quantity."
```


## R16 — `c3-1_q08` — Academic verbs: give a paragraph and test its argumentative move

**File:** `content/quizzes/c3/01-academic-verbs.csv`  
**Problem:** All four current choices describe something an author can do in a paragraph, so the item tests the writer’s preferred wording rather than a unique concept.

### Apply these changes

```text
prompt = "Paragraph 2 begins by presenting the critics’ objection, then uses two studies to answer it. What does the author do in the paragraph?"
choice_a = "Lists the critics and the studies in the paragraph."
choice_b = "Acknowledges a counterargument and rebuts it with evidence."
choice_c = "Uses formal vocabulary to make the paragraph sound academic."
choice_d = "Summarizes the article’s topic without taking a position."
correct_choice = "B"
feedback_a = "Tempting because it names the content. But it does not explain the relationship between the objection and the studies."
feedback_b = "Correct. The author first acknowledges the opposing view, then answers it with evidence. Those verbs name the paragraph’s argumentative work."
feedback_c = "Tempting because academic passages often use formal words. The prompt describes an argument move, not a vocabulary choice."
feedback_d = "Tempting because the paragraph discusses the article’s topic. But it takes a clear position by answering the critics."
```


## R17 — `a2-2_q01` — Character action: remove the false rule that every action has a feeling behind it

**File:** `content/quizzes/a2/02-inference-from-character-action.csv`  
**Problem:** Actions can be habitual, practical, accidental, or driven by several motives. Context is needed.

### Apply these changes

```text
choice_a = "What feeling or motive best fits this action in context?"
choice_b = "What feeling does the character directly name in the dialogue?"
choice_c = "What would I feel in the same situation?"
choice_d = "What feeling usually follows this action in stories?"
correct_choice = "A"
feedback_a = "Correct. Treat the action as a clue, then use the surrounding context to decide which feeling or motive best explains it."
feedback_b = "Tempting because dialogue can help. But a directly named feeling is stated information, and characters may hide or misunderstand their emotions."
feedback_c = "Tempting because imagining yourself there builds empathy. Your reaction is only a possibility; this character’s words and actions must decide."
feedback_d = "Tempting because familiar story patterns can suggest possibilities. A genre pattern cannot replace evidence from this scene."
```


## R18 — `a2-2_q05` — Bill inference: keep the supported emotion and remove the private motive

**File:** `content/quizzes/a2/02-inference-from-character-action.csv`  
**Problem:** Rereading and silence support unease, but they do not prove that Dad is “not ready to talk” or deliberately keeping the news to himself.

### Apply these changes

```text
choice_c = "Dad seems worried or unsettled by the bill."
feedback_c = "Correct. Opening it twice and then going silent support worry or unease. The passage does not tell us exactly what he plans to say or why he stays quiet."
```


## R19 — `a2-2_q06` — Letter inference: soften “afraid” to the level the behavior supports

**File:** `content/quizzes/a2/02-inference-from-character-action.csv`  
**Problem:** Avoiding the letter supports uneasiness or reluctance; it does not prove fear or a private plan to face the news alone.

### Apply these changes

```text
choice_a = "Tara feels uneasy about opening the letter."
feedback_a = "Correct. She keeps the letter in view but delays opening it all day, which supports uneasiness. The text does not reveal exactly what she expects it to say."
```


## R20 — `a2-4_q08` — “Staying inside the text”: allow ordinary reasoning, reject invented details

**File:** `content/quizzes/a2/04-avoiding-over-inference.csv`  
**Problem:** Readers use ordinary knowledge to connect clues. The boundary is whether the final claim is anchored in this text.

### Apply these changes

```text
choice_c = "Use the text’s clues without adding unsupported story details."
feedback_c = "Correct. Use ordinary reasoning to connect the clues, but make sure the conclusion is anchored in this passage and does not invent story facts."
choice_b = "Quoting the passage exactly in every part of your answer."
```


## R21 — `b2-1_q02` — Valid evidence: include precise paraphrase and make the wrong summary clearly vague

**File:** `content/quizzes/b2/01-evidence-traceable.csv`  
**Problem:** The current item wrongly excludes a precise paraphrase from valid evidence.

### Apply these changes

```text
choice_b = "A direct quote or a precise, locatable detail from the passage."
choice_c = "A broad summary that gives no specific supporting detail."
feedback_b = "Correct. Evidence may quote the text or precisely paraphrase a detail, as long as another reader can locate and check it."
feedback_c = "Tempting because a broad summary may be accurate. But without a specific detail, it cannot show exactly what supports the answer."
choice_a = "A statement that matches your overall impression of the whole passage."
```


## R22 — `b4-1_q01` — Skeptical tone signal: remove “claimed” from the automatic-signal pair

**File:** `content/quizzes/b4/01-neutral-vs-skeptical.csv`  
**Problem:** “Supposedly” often creates distance, while “claimed” can be neutral attribution depending on context.

### Apply these changes

```text
choice_c = "Distancing words such as “supposedly” or “so-called”"
feedback_c = "Correct. These words often hold a statement at a distance and can signal doubt. Still check the surrounding contrast and framing; no single word decides tone automatically."
```


## R23 — `c1-2_q06` — Ambitious plan: ask about the sentence’s framing, not the word’s fixed connotation

**File:** `content/quizzes/c1/02-connotation-from-context.csv`  
**Problem:** “Ambitious” itself is often positive or neutral. The criticism comes from the whole sentence, especially “but ignored how they would be paid for.”

### Apply these changes

```text
prompt = "Read: “The candidate’s ambitious plan promised major reforms but ignored how they would be paid for.” How does the whole sentence frame the plan?"
choice_a = "As bold, practical, and fully convincing to voters"
choice_b = "As ambitious in scale but unrealistic about cost"
choice_c = "As neutral, detailed, and purely factual in tone"
choice_d = "As hopeful, affordable, and likely to succeed"
correct_choice = "B"
feedback_a = "Tempting because “ambitious” and “major reforms” sound positive. The clause after “but” removes the sense that the plan is practical."
feedback_b = "Correct. The plan is large in scope, but the author criticizes it for ignoring how the reforms would be funded."
feedback_c = "Tempting because the sentence reports a plan and a funding gap. “Ignored” is judgmental, so the framing is not purely neutral."
feedback_d = "Tempting because the plan promises reform. Nothing in the sentence supports “affordable” or “likely to succeed.”"
```


## R24 — `c3-1_q03` — Assert: separate the verb’s meaning from the sentence’s evidence clause

**File:** `content/quizzes/c3/01-academic-verbs.csv`  
**Problem:** “Assert” means state confidently. It does not itself mean “without proof”; the following clause supplies that information.

### Apply these changes

```text
prompt = "Read: “The author asserts that small classes improve learning, but cites no studies to support the claim.” What does “asserts” itself tell the reader?"
choice_b = "The author states the claim confidently."
feedback_b = "Correct. “Asserts” means states confidently. The separate clause “cites no studies” tells us that this sentence provides no supporting evidence."
```


---

# D. Make 21 minor edits

These items have a defensible key, but a small wording, scope, or feedback change will make the teaching more accurate and reduce avoidable disagreement.


## M01 — `a1-1_q06` — Make the distractor a topic phrase rather than another theme-shaped claim

**File:** `content/quizzes/a1/01-theme-message-not-topic.csv`  
**Reason:** Choice B is also a complete general claim, so it has legitimate theme shape even if it is vague.

### Apply these changes

```text
choice_b = "The role of school in children’s lives."
feedback_b = "Tempting because it names an important subject. But it is a topic phrase; it does not make a claim about what school does to growing children."
```


## M02 — `a1-2_q07` — Remove a distractor that is actually a sensible next step

**File:** `content/quizzes/a1/02-theme-multiple-details.csv`  
**Reason:** Looking for a second scene is reasonable, even if “mentioned” is weaker than “supported.”

### Apply these changes

```text
choice_d = "Add more impressive wording without checking the rest of the story."
feedback_d = "Tempting because stronger wording can make an answer sound better. But style cannot replace evidence from more than one part of the story."
```


## M03 — `a2-1_q06` — Soften an absolute claim about genuinely certain people

**File:** `content/quizzes/a2/01-inference-clue-reasoning.csv`  
**Reason:** A person can be confident and still check the door repeatedly.

### Apply these changes

```text
feedback_a = "Correct. The repeated glances suggest that Dad’s behavior is less confident than his words. The contrast supports uncertainty without proving exactly what he feels."
```


## M04 — `a2-1_q10` — Align the stem with what the keyed clue actually proves

**File:** `content/quizzes/a2/01-inference-clue-reasoning.csv`  
**Reason:** Several clues show a reaction; choice D most specifically shows that he is not finished with the letter.

### Apply these changes

```text
prompt = "Read: “He read the letter, then read it again. He didn’t say anything. After a long moment, he put the letter in his pocket instead of back on the table.” Which clue best shows that he is not finished thinking about the letter?"
choice_b = "\"After a long moment,\" he finally moved the letter"
```


## M05 — `a4-1_q01` — Define tone without limiting it to the narrator’s feelings

**File:** `content/quizzes/a4/01-tone-vs-topic-fiction.csv`  
**Reason:** Tone can be the attitude shown by an author, narrator, or speaker; it is not always a narrator’s private feeling.

### Apply these changes

```text
choice_a = "Topic is what the text is about; tone is the attitude shown toward it."
feedback_a = "Correct. Topic is the subject—the WHAT. Tone is the attitude the language shows toward that subject. The same topic can be treated warmly, bitterly, humorously, or calmly."
choice_b = "Topic is how the narrator feels; tone is what the whole story is about."
```


## M06 — `a4-1_q04` — Remove the near-overlapping “admiring” distractor

**File:** `content/quizzes/a4/01-tone-vs-topic-fiction.csv`  
**Reason:** “Each word landed with care” can sound admiring, making B and C closer than intended.

### Apply these changes

```text
choice_c = "Careless"
feedback_c = "Tempting only if “evenly” is mistaken for lack of interest. “With care” shows control and attention, which is the opposite of careless."
```


## M07 — `a4-3_q05` — Use a precise tone–mood pair without forcing “wistful”

**File:** `content/quizzes/a4/03-mood-vs-tone.csv`  
**Reason:** The sentence is warm and nostalgic; it does not clearly contain the longing or sadness usually carried by “wistful.”

### Apply these changes

```text
choice_c = "Tone is nostalgic; mood is warm and comforting."
feedback_c = "Correct. “That summer” looks back fondly, while the bread smell creates a warm, comforting feeling for the reader. Tone and mood can align without using the same word."
feedback_d = "Tempting because the memory is pleasant. But “amused” requires humor, and the sentence creates warmth rather than a joke."
```


## M08 — `a5-1_q02` — Acknowledge that imagery also helps readers picture the scene

**File:** `content/quizzes/a5/01-imagery-creates-meaning.csv`  
**Reason:** Choice C is true. The intended distinction is between basic visualization and deeper literary work.

### Apply these changes

```text
prompt = "Beyond helping the reader picture a scene, imagery often does which of these jobs?"
feedback_c = "Tempting because imagery does help readers picture a scene. The word “beyond” asks for its deeper work: building mood, tone, character, or theme."
```


## M09 — `b2-5_q07` — State the correlation rule precisely

**File:** `content/quizzes/b2/05-inference-from-nonfiction.csv`  
**Reason:** Correlation is not merely a “smaller claim”; it is an observed association that does not establish cause.

### Apply these changes

```text
choice_d = "Report the association without claiming that one thing caused the other."
feedback_d = "Correct. Correlation supports an association between two variables. A causal claim needs additional evidence, such as random assignment or a strong research design."
```


## M10 — `b4-1_q09` — Broaden the explanation of skepticism beyond hedging

**File:** `content/quizzes/b4/01-neutral-vs-skeptical.csv`  
**Reason:** Skepticism can also come from contrast, irony, loaded wording, selective detail, or framing.

### Apply these changes

```text
choice_d = "Technical words show subject matter, not attitude; check wording and framing."
feedback_d = "Correct. Words such as “compounding” and “mitigation” identify the subject. Skepticism comes from how claims are framed—through distancing, contrast, irony, or other attitude signals."
```


## M11 — `c1-1_q04` — Define “ephemera” with the temporary-use idea

**File:** `content/quizzes/c1/01-context-meaning.csv`  
**Reason:** “Everyday paper goods” is too broad and misses the defining idea that ephemera were made for short-term use or interest.

### Apply these changes

```text
choice_a = "rare antiques that collectors consider highly valuable"
choice_b = "printed items made for brief use or interest"
choice_c = "old handwritten letters saved by their original owners"
choice_d = "equipment used to produce plays on a stage"
feedback_a = "Tempting because old paper items can become collectible. But the examples were originally ordinary, short-lived printed pieces rather than valuable antiques."
feedback_b = "Correct. The examples are printed items originally made for brief use or interest, even though people may later collect them."
feedback_c = "Tempting because postcards can be personal keepsakes. But the list includes tickets and programs, not specifically handwritten correspondence."
feedback_d = "Tempting because one example comes from plays. The shared feature is temporary printed material, not stage equipment."
```


## M12 — `m0_q03` — Match “speaker” in the stem with “speaker or narrator” in the answer

**File:** `content/quizzes/m0/abstract.csv`  
**Reason:** A speaker is not automatically the author.

### Apply these changes

```text
choice_b = "Tone: the speaker or narrator’s attitude"
feedback_b = "Correct. Attitude points to tone. In a poem it may be the speaker’s attitude; in a story it may be the narrator’s."
```


## M13 — `m0-1_q10` — Do not say background knowledge itself causes over-inference

**File:** `content/quizzes/m0/01-five-questions.csv`  
**Reason:** Background knowledge helps comprehension; the problem is answering from it instead of checking the text.

### Apply these changes

```text
feedback_c = "Tempting because what you know can help you understand the passage. But first identify what the question asks, then check your idea against the text’s clues."
choice_c = "Recall everything you already know about the topic."
```


## M14 — `a1-2_q02` — Limit the one-moment warning to texts that actually contain a larger pattern

**File:** `content/quizzes/a1/02-theme-multiple-details.csv`  
**Reason:** A very short text or poem may support a theme through one decisive turn or ending. The current rule is too absolute.

### Apply these changes

```text
prompt = "If a story gives you several important moments, but your theme fits only ONE of them, what is the most likely problem?"
feedback_a = "Tempting because short stories have less room. But this stem says the story contains several important moments, so the theme should account for more than one of them."
feedback_b = "Correct. When a theme fits only one scene while the rest of the story builds something else, you have probably mistaken that scene’s lesson for the whole text’s message."
```


## M15 — `a2-1_q07` — Name the real error: an unchecked genre expectation

**File:** `content/quizzes/a2/01-inference-clue-reasoning.csv`  
**Reason:** Knowledge of common story patterns can suggest a hypothesis; it becomes weak reasoning when the student never checks this passage.

### Apply these changes

```text
choice_b = "The student uses a genre expectation without checking this text’s clues."
feedback_b = "Correct. Familiar story patterns can suggest “scared” as a possibility, but the student must point to this character’s words, actions, or setting before accepting it."
```


## M16 — `a2-4_q01` — Describe over-inference as adding unsupported details, not importing knowledge

**File:** `content/quizzes/a2/04-avoiding-over-inference.csv`  
**Reason:** Ordinary knowledge is part of inference; invented or unanchored story details are the problem.

### Apply these changes

```text
feedback_a = "Correct. Over-inference stretches a clue past what it can support, often by adding a motive, cause, history, or future event that the text never establishes."
choice_b = "Drawing any conclusion the text does not directly state."
```


## M17 — `a2-4_q06` — Correct the explanation for the unsupported-parent distractor

**File:** `content/quizzes/a2/04-avoiding-over-inference.csv`  
**Reason:** The problem is not that the idea comes from “outside knowledge”; it is that the parents never appear and no clue supports the claim.

### Apply these changes

```text
feedback_c = "Tempting because repeated absences are sometimes linked to family attitudes. But Tom’s parents are never mentioned, so this adds an unsupported explanation."
```


## M18 — `m0-1_q05` — Keep narrator and author separate in the five-question label

**File:** `content/quizzes/m0/01-five-questions.csv`  
**Reason:** The stem asks about the narrator, while the keyed choice asks how the author feels.

### Apply these changes

```text
choice_c = "How does the speaker or narrator feel about it?"
feedback_c = "Correct. “Attitude” points to tone: how the speaker or narrator regards the subject. That voice is not automatically the real author."
choice_a = "How do I prove the answer from the text?"
```


## M19 — `m0_q01` — Use “support” rather than treating all textual evidence as proof

**File:** `content/quizzes/m0/abstract.csv`  
**Reason:** Evidence can strongly support an interpretation without proving it with mathematical certainty.

### Apply these changes

```text
choice_b = "Evidence: the support in the text"
feedback_b = "Correct. “Best supports” asks for the words or details that most strongly back up the answer."
feedback_c = "Trap: theme is the deeper message of a story. This asks which sentence supports a point, not what the story means."
choice_a = "Tone: the attitude shown"
choice_c = "Theme: the story’s deeper message"
choice_d = "Inference: a conclusion not directly stated"
feedback_a = "Trap: tone is the attitude shown toward a subject. This question asks what backs up an answer, not what attitude the language creates."
feedback_d = "Trap: inference is a conclusion that is not directly stated; evidence is the stated detail used to support that conclusion."
```


## M20 — `c3-2_q05` — Use a natural and precise tone label

**File:** `content/quizzes/c3/02-tone-vocabulary.csv`  
**Reason:** “Urgent and warning” is understandable but not idiomatic; “urgent and cautionary” is the standard adjective pair.

### Apply these changes

```text
choice_a = "Urgent and cautionary"
feedback_a = "Correct. “This month” creates time pressure, while “may be irreversible” warns of harm if no action is taken."
```


## M21 — `c3-2_q08` — Do not teach “although” or attribution alone as automatic skepticism

**File:** `content/quizzes/c3/02-tone-vocabulary.csv`  
**Reason:** “Supposedly” often signals doubt, but “in their words” may be neutral attribution and “although” is simply a contrast marker.

### Apply these changes

```text
prompt = "A passage uses “supposedly” and “in their words,” then follows the claim with contrary evidence. The tone is most likely:"
feedback_a = "Trap: admiration uses approving language. Here the writer distances the claim and then presents evidence against it."
feedback_b = "Correct. “Supposedly” creates doubt, and the contrary evidence strengthens the skeptical framing. “In their words” and contrast alone would not automatically decide the tone."
feedback_c = "Trap: attribution can be objective, but “supposedly” plus contrary evidence adds clear doubt."
```


---

# E. Post-edit QA and acceptance criteria

## Automated checks

Run:

```bash
python3 scripts/validate-content.py
```

Add or run checks confirming:

1. Exactly 24 quiz files and 240 unique `quiz_id` values remain.
2. Every file contains exactly 10 questions.
3. Every `correct_choice` is one of `A`, `B`, `C`, or `D`.
4. All four choices and all four feedback fields are non-empty.
5. Shuffling keeps each choice attached to its own feedback and recalculates the displayed correct letter.
6. For the 47 edited questions:
   - maximum choice-length spread is no more than 4 words;
   - no correct answer is uniquely the longest;
   - a longest-choice guessing strategy averages 25%.

## Editorial checks

Have a reviewer answer the **47 edited questions without seeing the key**. For every item, require:

- one clearly best answer;
- a precise textual reason the key wins;
- a named misconception for each distractor;
- no feedback that claims more than the passage proves;
- no narrator/speaker/author mix-up;
- no automatic rule based on one word such as `claimed`, `although`, or `asserts`;
- no claim that background knowledge itself is invalid;
- no causal conclusion from a comparison unless the design supports it.

Then answer a random sample of **20 unchanged questions** to check that this audit was not too narrow.

## Release decision

The bank is ready for wider independent use when:

- all 51 flags above are resolved;
- the validator passes;
- the blind reviewer agrees with every edited key;
- any disagreement leads to a wording change rather than a longer defense of the existing key.

