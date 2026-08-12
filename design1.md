
# Design Document: Break 250 Reading Lab

## Close-Reading Concept Trainer for Advanced Middle-School Readers

## 1. Product Summary

**Break 250 Reading Lab** is a focused reading-analysis learning app for strong middle-school readers who already read a lot but are stuck around high MAP Reading scores, especially around **240–249**, and want to break into **250+**.

The app is **not** a general reading app. It is not mainly about reading more books or increasing Lexile level. It is a **close-reading concept trainer**.

The app teaches students how to use advanced reading tools:

* evidence
* inference
* tone
* author’s purpose
* text structure
* word choice
* figurative language
* theme
* argument
* poetry
* paired-text analysis

The app’s core method:

> **Concept → micro-example → short text → first read → second read → MAP-style questions → prove with text → wrong-answer diagnosis → targeted next practice**

---

# 2. Product Vision

## 2.1 Core Problem

Many strong students read a lot but still plateau in advanced reading assessments.

They may already:

* read hundreds of books per year
* have strong vocabulary
* understand plot and basic comprehension
* perform well in school reading

But they may still struggle with:

* choosing the best-supported answer
* proving answers with exact text
* identifying subtle tone
* understanding paragraph function
* recognizing author’s purpose
* analyzing arguments and assumptions
* interpreting poetry and figurative language
* explaining why wrong answers are tempting but incorrect

The issue is not reading volume. The issue is **analytical reading precision**.

## 2.2 Product Thesis

Students often learn terms like “tone,” “author’s purpose,” and “text structure” in school, but they may not know how to use them as tools.

This app turns ELA terms into usable reading tools.

## 2.3 Product Positioning

### Not this:

> “Read more nonfiction.”

### Instead:

> “Learn how advanced readers analyze texts.”

### Tagline options

* **Read like a 250+ reader.**
* **Turn ELA terms into reading tools.**
* **You already read well. Now learn how to analyze.**
* **Close reading practice for advanced readers.**

---

# 3. Target Users

## 3.1 Primary User

Advanced Grade 5–8 readers who:

* read independently
* have high reading volume
* are scoring high but plateauing
* want to improve MAP Reading or advanced reading analysis
* can handle short nonfiction, fiction, poetry, and argument texts

Typical score range:

* MAP Reading 230–249
* Especially useful for 240–249

## 3.2 Secondary Users

Parents who want structured enrichment beyond “read more books.”

Teachers/tutors who want targeted lessons on reading-analysis concepts.

Bilingual or international-school students who read fluently but need explicit analytical frameworks.

---

# 4. Product Goals

## 4.1 Learning Goals

The student should be able to:

1. Identify the concept being tested by a question.
2. Explain key reading-analysis concepts in simple language.
3. Use exact text evidence to prove answers.
4. Identify why a wrong answer is tempting but incorrect.
5. Analyze tone, structure, purpose, inference, and argument.
6. Transfer these skills to A3000, CommonLit, MAP-style passages, and school reading.

## 4.2 Product Goals

The app should:

1. Teach concepts clearly.
2. Provide short, high-quality practice texts.
3. Support two-pass reading.
4. Require evidence-based answers.
5. Diagnose wrong-answer types.
6. Track skill-level progress.
7. Recommend targeted next lessons.
8. Avoid becoming a generic reading platform.

---

# 5. MVP Scope

## 5.1 MVP Version

The MVP should include:

* 12 concept modules
* 3 lessons per module
* 36 total lessons
* diagnostic quiz
* student dashboard
* lesson player
* question engine
* answer explanation system
* wrong-answer diagnosis
* progress tracking
* parent/admin view

## 5.2 MVP Module List

| Module ID | Module Name                  |
| --------- | ---------------------------- |
| M01       | Main Idea vs Detail vs Theme |
| M02       | Evidence                     |
| M03       | Inference                    |
| M04       | Author’s Purpose             |
| M05       | Text Structure               |
| M06       | Tone                         |
| M07       | Word Choice                  |
| M08       | Figurative Language          |
| M09       | Theme                        |
| M10       | Argument                     |
| M11       | Poetry                       |
| M12       | Paired Texts                 |

Each module has 3 lessons:

* Lesson A: basic concept
* Lesson B: applied practice
* Lesson C: challenge / mixed question practice

---

# 6. Core Learning Flow

## 6.1 Standard Lesson Flow

Each lesson follows the same structure.

### Step 1: Concept Introduction

Short explanation of one concept.

Example:

> Tone means the author’s or speaker’s attitude. Tone is not the topic. Tone is not how you feel. Tone is the attitude shown through word choice.

### Step 2: Micro-Examples

Use very short examples before the main passage.

Example:

Sentence:

> The plan was bold and inspiring.

Question:

> What is the tone?

Answer:

> Approving / admiring.

Proof:

> “bold” and “inspiring.”

### Step 3: Short Text

Student reads a short passage.

Passage length:

* Easy: 200–350 words
* Medium: 350–600 words
* Challenge: 600–900 words
* Poetry: 8–30 lines
* Paired texts: two passages of 250–500 words each

### Step 4: First Read — Understand

Questions focus on basic comprehension:

* What is the text mostly about?
* Who is speaking?
* What happened?
* What is the central idea?
* What confused you?

### Step 5: Second Read — Analyze

Student rereads with one focus.

Examples:

* Highlight tone words.
* Mark evidence.
* Label paragraph function.
* Identify claim and evidence.
* Find a metaphor and explain it.
* Identify a shift in a poem.

### Step 6: MAP-Style Questions

Each lesson has 5–8 questions.

Question types:

* multiple choice
* select evidence
* drag sentence into function label
* short explanation
* choose best proof
* identify wrong-answer type
* highlight exact text

### Step 7: Evidence Requirement

For higher-level questions, student must select or type the exact evidence.

Core prompt:

> Which exact words in the text prove your answer?

### Step 8: Feedback

Feedback includes:

* correct answer
* explanation
* exact text proof
* why wrong answers are tempting
* concept reminder

### Step 9: Reflection

Student answers:

* What concept did I practice?
* What mistake did I avoid?
* What should I watch for next time?

---

# 7. Screen Design

## 7.1 Student Home Dashboard

### Purpose

Show progress and next recommended action.

### Elements

* Welcome message
* Current level / path
* Streak
* Skill progress map
* Recommended next lesson
* Recent mistake patterns
* Continue button

### Example

```
Welcome back, Bella.

Your strongest skill:
Evidence

Your current focus:
Tone and Word Choice

Recommended next lesson:
Tone Lesson 2 — Skeptical vs Neutral

Recent mistake pattern:
Related but not proven answers
```

### Key CTAs

* Continue Lesson
* Take Diagnostic
* Review Mistakes
* Practice Weak Skill
* View Progress

---

## 7.2 Diagnostic Screen

### Purpose

Determine weak skills.

### Structure

20–30 questions across all modules.

Question mix:

* 2 evidence
* 2 inference
* 2 author purpose
* 2 structure
* 2 tone
* 2 figurative language
* 2 argument
* 2 poetry
* 2 main idea/theme
* 2 paired-text

### Output

Diagnostic report:

| Skill     | Status         |
| --------- | -------------- |
| Evidence  | Strong         |
| Tone      | Needs practice |
| Structure | Needs practice |
| Argument  | Developing     |
| Poetry    | Needs practice |

### Recommendation

The app suggests a learning path.

Example:

> Start with Tone → Text Structure → Argument.

---

## 7.3 Lesson List Screen

### Purpose

Allow student to browse modules and lessons.

### Elements

Each module card includes:

* title
* skill icon
* short description
* number of lessons
* progress status
* mastery score

Example:

```
Tone
Learn how to detect the author’s attitude from word choice.
Progress: 1 / 3 lessons
Mastery: 68%
```

---

## 7.4 Lesson Player Screen

### Layout

The lesson player should have a clean, distraction-free layout.

Desktop:

* left: passage
* right: questions / notes / highlights

Mobile:

* passage first
* question panel below
* sticky “Show Passage” button

### Features

* text highlighting
* note-taking
* evidence selection
* paragraph numbering
* vocabulary popups
* concept reminder card
* progress bar

### Highlight colors

No need to overcomplicate, but suggested categories:

| Highlight Type      | Meaning             |
| ------------------- | ------------------- |
| Evidence            | Proof               |
| Tone Word           | Attitude            |
| Structure Signal    | Organization        |
| Figurative Language | Non-literal meaning |
| Claim               | Argument main point |

---

## 7.5 Question Screen

### Question Structure

Each question should display:

* question stem
* answer choices
* optional hint
* evidence selection
* submit button

Example:

```
Question:
Which word best describes the author’s tone in paragraph 3?

A. Neutral
B. Skeptical
C. Excited
D. Playful

Before submitting, select the word or phrase that proves your answer.
```

### After Submit

Feedback panel:

```
Correct answer: B. Skeptical.

Why:
The words “supposedly” and “claims” show doubt.

Why A is tempting:
The paragraph includes facts, so it may seem neutral. But the word choice shows the author’s attitude is not fully neutral.

Skill:
Tone + Word Choice
```

---

## 7.6 Mistake Review Screen

### Purpose

The most important learning screen.

Shows all recent wrong answers grouped by mistake type.

### Mistake Categories

| Error Type                  | Explanation                                |
| --------------------------- | ------------------------------------------ |
| Too Broad                   | Answer says more than text proves          |
| Too Narrow                  | Answer focuses on one small detail         |
| Related but Not Proven      | Answer sounds connected but lacks evidence |
| Opposite Tone               | Answer misses author attitude              |
| Literal Only                | Answer misses implied meaning              |
| Outside Knowledge           | Answer uses knowledge not in passage       |
| True but Not the Question   | Answer is true but does not answer stem    |
| Detail Instead of Main Idea | Confuses support with central point        |
| Weak Evidence               | Evidence does not fully support answer     |
| Misread Structure           | Misunderstands paragraph function          |
| Missed Shift                | Misses change in tone/idea                 |

### Example Display

```
Mistake Type:
Related but Not Proven

Your answer:
B

Correct answer:
D

Why B was tempting:
It mentions the same topic.

Why D is better:
D is directly supported by paragraph 4.

Proof:
“...”
```

### CTA

* Retry Similar Question
* Review Concept
* Add to Mistake Notebook

---

## 7.7 Skill Progress Screen

### Purpose

Track mastery by concept.

### Metrics

For each skill:

* accuracy
* evidence accuracy
* explanation quality
* recent trend
* number of completed lessons
* common mistake type

Example:

| Skill     | Accuracy | Evidence Score | Status         |
| --------- | -------: | -------------: | -------------- |
| Evidence  |      88% |            92% | Strong         |
| Tone      |      64% |            58% | Needs practice |
| Structure |      71% |            65% | Developing     |
| Argument  |      59% |            54% | Needs practice |

---

## 7.8 Parent / Teacher Dashboard

### Purpose

Allow parent or tutor to see progress.

### Elements

* completed lessons
* time spent
* skill strengths
* weak skills
* common wrong-answer types
* recommended next focus
* sample student explanations

### Example Recommendation

```
Bella is strong in general comprehension and evidence questions.
Current weakness: distinguishing neutral tone from skeptical tone.
Suggested next focus: Tone Lesson 2 and Word Choice Lesson 1.
```

---

# 8. Content Design

## 8.1 Text Types

The app needs short texts across genres.

| Text Type          | Use Case                          |
| ------------------ | --------------------------------- |
| Short fiction      | tone, inference, theme, irony     |
| Nonfiction article | central idea, evidence, structure |
| Historical speech  | purpose, rhetoric, tone, argument |
| Poem               | imagery, line break, tone shift   |
| Classic excerpt    | word choice, syntax, theme        |
| Opinion essay      | claim, counterclaim, assumption   |
| Paired text        | compare viewpoint and purpose     |

## 8.2 Copyright Strategy

Important for development.

Use one of these:

1. Public domain texts
2. Original texts written for the app
3. Licensed texts
4. Short excerpts only if legally allowed
5. User-provided texts for personal use

For MVP, safest approach:

* Use original passages.
* Use public-domain texts where appropriate.
* Avoid copyrighted modern texts unless licensed.

## 8.3 Passage Metadata

Each passage should have structured metadata.

Example JSON:

```json
{
  "passage_id": "P_TONE_001",
  "title": "The New Rule",
  "author": "Original",
  "genre": "nonfiction_argument",
  "word_count": 420,
  "estimated_grade_band": "6-8",
  "estimated_lexile_band": "850-1050",
  "primary_skill": "tone",
  "secondary_skills": ["word_choice", "evidence"],
  "difficulty": "medium",
  "source_type": "original",
  "text": "...",
  "paragraphs": [
    {
      "paragraph_id": "p1",
      "text": "..."
    }
  ]
}
```

---

# 9. Question Design

## 9.1 Question Types

### Multiple Choice

Standard MAP-style question.

```json
{
  "type": "multiple_choice",
  "question": "Which word best describes the author's tone?",
  "choices": ["neutral", "skeptical", "excited", "playful"],
  "answer": "skeptical"
}
```

### Evidence Selection

Student selects sentence or phrase.

```json
{
  "type": "evidence_selection",
  "question": "Which sentence best supports the inference?",
  "valid_evidence": ["p3_s2"]
}
```

### Highlight Text

Student highlights exact words.

Useful for tone, word choice, figurative language.

### Short Explanation

Student writes 1–3 sentences.

Prompt:

> Explain why the correct answer is better than the tempting wrong answer.

### Paragraph Function

Student labels each paragraph.

Options:

* introduce problem
* give example
* provide evidence
* show contrast
* explain cause
* present counterargument
* conclude

### Wrong-Answer Diagnosis

Student must choose why a wrong answer is wrong.

Options:

* too broad
* too narrow
* related but not proven
* outside knowledge
* opposite tone

This is a key feature.

---

## 9.2 Question Metadata

Each question should be tagged carefully.

```json
{
  "question_id": "Q_TONE_001_03",
  "passage_id": "P_TONE_001",
  "skill": "tone",
  "subskill": "skeptical_vs_neutral",
  "difficulty": "medium",
  "question_type": "multiple_choice_with_evidence",
  "question_text": "Which word best describes the author's tone in paragraph 3?",
  "choices": [
    {
      "id": "A",
      "text": "neutral",
      "is_correct": false,
      "wrong_answer_type": "tempting_because_factual_content",
      "feedback": "This is tempting because the paragraph includes facts, but the word choice shows doubt."
    },
    {
      "id": "B",
      "text": "skeptical",
      "is_correct": true,
      "feedback": "Correct. Words like 'claims' and 'supposedly' show doubt."
    },
    {
      "id": "C",
      "text": "excited",
      "is_correct": false,
      "wrong_answer_type": "opposite_tone",
      "feedback": "The author does not show enthusiasm or excitement."
    },
    {
      "id": "D",
      "text": "playful",
      "is_correct": false,
      "wrong_answer_type": "unsupported",
      "feedback": "There is no humor or playful language."
    }
  ],
  "required_evidence": ["claims", "supposedly"],
  "explanation": "The tone is skeptical because the author uses words that suggest doubt."
}
```

---

# 10. Scoring System

## 10.1 Basic Accuracy

Track correct / incorrect per question.

## 10.2 Evidence Score

A student gets evidence credit if they select valid proof.

Suggested scoring:

| Evidence Selection       | Score |
| ------------------------ | ----: |
| Exact proof              |   1.0 |
| Partially relevant proof |   0.5 |
| Wrong proof              |     0 |
| No proof                 |     0 |

## 10.3 Explanation Score

For short explanations, score using a simple rubric.

| Score | Meaning                                                              |
| ----: | -------------------------------------------------------------------- |
|     0 | No explanation or irrelevant                                         |
|     1 | Restates answer only                                                 |
|     2 | Gives answer with weak evidence                                      |
|     3 | Gives answer with exact evidence                                     |
|     4 | Gives answer, exact evidence, and explains why wrong answer is wrong |

This can be human-scored first. Later AI scoring can assist.

## 10.4 Mastery Score

For each skill:

```
mastery_score = 
  0.5 * recent_accuracy
+ 0.3 * evidence_score
+ 0.2 * explanation_score
```

Use rolling recent performance, not lifetime only.

## 10.5 Skill Status

| Mastery Score | Status         |
| ------------: | -------------- |
|        85–100 | Strong         |
|         70–84 | Developing     |
|         50–69 | Needs Practice |
|          0–49 | Start Here     |

---

# 11. Recommendation Engine

## 11.1 Input Signals

The app should recommend lessons based on:

* weak skill
* recent accuracy
* evidence score
* common mistake type
* lesson completion
* difficulty history

## 11.2 Recommendation Examples

If student misses tone questions:

> Recommended: Tone Lesson 2 — Skeptical vs Neutral

If student selects answers without valid proof:

> Recommended: Evidence Lesson 1 — Prove It with Exact Words

If student confuses details with central ideas:

> Recommended: Main Idea Lesson 2 — Detail vs Central Idea

If student misses poetry tone shifts:

> Recommended: Poetry Lesson 3 — Finding the Shift

## 11.3 Simple MVP Algorithm

Pseudo logic:

```python
def recommend_next_lesson(user_skill_scores, completed_lessons):
    weak_skills = sorted(user_skill_scores, key=lambda s: s.mastery_score)
    
    for skill in weak_skills:
        next_lesson = find_next_uncompleted_lesson(skill)
        if next_lesson:
            return next_lesson
    
    return find_mixed_review_lesson()
```

---

# 12. Content Schema

## 12.1 Module

```json
{
  "module_id": "M06",
  "title": "Tone",
  "description": "Learn how to identify the author's or speaker's attitude through word choice.",
  "learning_goals": [
    "Define tone",
    "Identify tone words",
    "Use evidence to prove tone",
    "Distinguish neutral, skeptical, critical, and admiring tones"
  ],
  "lessons": ["L_TONE_001", "L_TONE_002", "L_TONE_003"]
}
```

## 12.2 Lesson

```json
{
  "lesson_id": "L_TONE_001",
  "module_id": "M06",
  "title": "What Is Tone?",
  "difficulty": "easy",
  "duration_minutes": 20,
  "primary_skill": "tone",
  "secondary_skills": ["word_choice", "evidence"],
  "concept_intro": "...",
  "micro_examples": ["ME_TONE_001", "ME_TONE_002"],
  "passage_id": "P_TONE_001",
  "questions": ["Q_TONE_001_01", "Q_TONE_001_02"],
  "reflection_prompt": "What words helped you identify tone today?"
}
```

## 12.3 Student Attempt

```json
{
  "attempt_id": "A_123",
  "user_id": "U_001",
  "lesson_id": "L_TONE_001",
  "started_at": "2026-05-26T10:00:00Z",
  "completed_at": "2026-05-26T10:23:00Z",
  "answers": [
    {
      "question_id": "Q_TONE_001_01",
      "selected_choice": "B",
      "is_correct": true,
      "selected_evidence": ["claims", "supposedly"],
      "evidence_score": 1.0,
      "explanation": "The author sounds skeptical because these words show doubt.",
      "explanation_score": 3
    }
  ],
  "skill_scores": {
    "tone": 0.82,
    "evidence": 0.91
  }
}
```

---

# 13. Database Model

Suggested entities:

## Tables / Collections

### users

* id
* name
* email
* role: student / parent / teacher / admin
* grade
* created_at

### modules

* id
* title
* description
* order_index

### lessons

* id
* module_id
* title
* difficulty
* estimated_time
* primary_skill
* secondary_skills
* passage_id
* order_index

### passages

* id
* title
* author
* source_type
* genre
* word_count
* text
* metadata

### passage_segments

* id
* passage_id
* paragraph_index
* sentence_index
* text

### questions

* id
* lesson_id
* passage_id
* type
* skill
* subskill
* question_text
* difficulty
* explanation

### answer_choices

* id
* question_id
* label
* text
* is_correct
* wrong_answer_type
* feedback

### evidence_keys

* id
* question_id
* segment_id
* exact_text
* score_weight

### attempts

* id
* user_id
* lesson_id
* started_at
* completed_at
* total_score

### responses

* id
* attempt_id
* question_id
* selected_choice
* selected_evidence
* explanation_text
* is_correct
* evidence_score
* explanation_score
* wrong_answer_type

### skill_progress

* user_id
* skill
* accuracy
* evidence_score
* explanation_score
* mastery_score
* updated_at

---

# 14. Admin / Content Management

## 14.1 Admin Features

Admin should be able to:

* create modules
* create lessons
* add/edit passages
* add questions
* add answer choices
* tag skills
* tag wrong-answer types
* add feedback
* preview lesson
* publish/unpublish lesson

## 14.2 Content Authoring Workflow

1. Create passage.
2. Tag passage metadata.
3. Create lesson intro.
4. Add micro-examples.
5. Add questions.
6. Add answer choices.
7. Add feedback for correct and wrong answers.
8. Add evidence keys.
9. Preview as student.
10. Publish.

## 14.3 Content Quality Checklist

Each lesson must have:

* one clear primary skill
* short concept explanation
* at least two micro-examples
* one passage
* at least five questions
* answer explanations
* wrong-answer feedback
* evidence requirement for at least three questions
* reflection prompt

---

# 15. AI Features

## 15.1 MVP AI Usage

For MVP, keep AI limited and controlled.

Possible safe AI features:

* generate draft explanations for admin review
* suggest wrong-answer categories
* rewrite explanation at easier level
* summarize student mistake patterns
* help score short explanations with human review

## 15.2 Avoid in MVP

Avoid fully AI-generated live content for students without review.

Reasons:

* accuracy risk
* age/safety concerns
* inconsistent quality
* copyright concerns
* hard to control pedagogy

## 15.3 Later AI Features

Later version can include:

* AI close-reading coach
* AI asks Socratic follow-up questions
* AI reviews student explanation
* AI generates similar practice questions
* AI adapts text difficulty
* AI recommends outside reading

Example AI coach prompt:

> You are a close-reading coach. Do not give the answer immediately. Ask the student to find exact words in the passage that prove their answer.

---

# 16. UX Principles

## 16.1 Keep It Focused

Do not overload each lesson.

One lesson = one main concept.

## 16.2 Avoid Killing Reading Joy

The app is for deliberate practice, not all reading.

Suggested message:

> Keep reading for fun. Use this lab to train the advanced tools.

## 16.3 Make Concepts Feel Useful

Avoid school-like definitions only.

Use phrasing like:

* “This tool helps you…”
* “Use this when the question asks…”
* “Watch out for this trap…”

## 16.4 Show Why Wrong Answers Are Tempting

This is critical.

High-level students often need to learn that wrong answers are not always silly. They are often partly true.

## 16.5 Evidence First

The app should repeatedly ask:

> What exact words prove it?

---

# 17. Design Style

## 17.1 Visual Style

Suggested:

* clean
* calm
* academic but friendly
* not childish
* suitable for Grade 5–8 advanced readers

## 17.2 UI Tone

Use direct, encouraging language.

Examples:

* “Good. Now prove it.”
* “This answer is related, but not proven.”
* “Look for the words that show attitude.”
* “The question is asking about structure, not topic.”

## 17.3 Gamification

Use light gamification only.

Good:

* streaks
* badges for skill mastery
* progress map
* “Proof Master” badge
* “Tone Detective” badge

Avoid:

* too many animations
* game mechanics that distract from reading
* speed-based rewards

This app should reward precision, not speed.

---

# 18. Lesson Examples

## 18.1 Evidence Lesson Example

### Concept

Evidence means the exact words that prove an answer.

### Micro-example

Text:

> Mia checked the clock for the third time and tapped her pencil against the desk.

Question:

> What can you infer about Mia?

A. She is bored.
B. She is nervous or impatient.
C. She is happy.
D. She forgot her pencil.

Correct:

B

Evidence:

> checked the clock for the third time
> tapped her pencil

Feedback:

> These actions suggest nervousness or impatience. “Bored” is possible, but less directly proven.

---

## 18.2 Tone Lesson Example

Text:

> The company claimed its new bottle was “eco-friendly,” although it used nearly the same amount of plastic as before.

Question:

> What is the author’s tone?

A. admiring
B. skeptical
C. playful
D. neutral

Correct:

B

Proof:

> claimed
> although
> nearly the same amount

Feedback:

> “Claimed” suggests doubt. “Although” introduces a contrast that weakens the company’s statement.

---

## 18.3 Structure Lesson Example

Question:

> Why does the author include paragraph 4?

Choices:

A. To introduce a new topic
B. To provide evidence for the claim
C. To summarize the whole article
D. To entertain the reader with a story

Feedback:

> Paragraph 4 gives data that supports the claim made in paragraph 2. Therefore, its function is evidence.

---

# 19. Analytics

## 19.1 Student-Level Analytics

Track:

* lessons completed
* time spent
* accuracy by skill
* evidence score
* explanation score
* wrong-answer types
* improvement trend
* retry success

## 19.2 Product Analytics

Track:

* lesson completion rate
* question difficulty
* most common wrong choices
* average time per lesson
* drop-off points
* repeated mistake types
* concept lessons that need improvement

## 19.3 Content Improvement Loop

If many students miss the same question:

* check if question is ambiguous
* improve explanation
* add micro-example
* adjust difficulty
* rewrite answer choices

---

# 20. Technical Recommendation

## 20.1 Suggested Stack

Depends on existing dev team, but a typical stack:

### Web App

* Frontend: React / Next.js
* Styling: Tailwind CSS
* Backend: Node.js / Next.js API / Python FastAPI
* Database: PostgreSQL or Supabase
* Auth: Supabase Auth / Firebase Auth / Clerk
* Hosting: Vercel + Supabase

### Mobile App

Given user already has an Apple app for MyWordBank, options:

1. Build responsive web first.
2. Later wrap as mobile app.
3. Or build React Native / Flutter if cross-platform is desired.
4. If iOS-first, SwiftUI is fine but content/admin iteration may be slower.

## 20.2 Recommended MVP Approach

Build responsive web first.

Reasons:

* faster content updates
* easier admin tools
* easier sharing with testers
* easier parent/student access
* lower App Store friction

Then build iOS app after validation.

---

# 21. API Design

## 21.1 Basic Endpoints

### Auth

* POST /auth/signup
* POST /auth/login
* POST /auth/logout

### Modules

* GET /modules
* GET /modules/:id

### Lessons

* GET /lessons/:id
* GET /modules/:id/lessons

### Attempts

* POST /attempts/start
* POST /attempts/:id/submit-answer
* POST /attempts/:id/complete
* GET /attempts/:id

### Progress

* GET /users/:id/progress
* GET /users/:id/mistakes
* GET /users/:id/recommendation

### Admin

* POST /admin/passages
* POST /admin/lessons
* POST /admin/questions
* PATCH /admin/questions/:id
* POST /admin/publish/:lesson_id

---

# 22. Privacy and Safety

Because this app is for children, privacy matters.

## 22.1 Data Minimization

Collect only:

* name or nickname
* grade
* progress data
* responses
* optional parent email

Avoid collecting unnecessary personal information.

## 22.2 Parent Controls

Parent should be able to:

* view progress
* delete account
* export data
* control AI coach access if added later

## 22.3 AI Safety

If AI chat is added later:

* no open-ended unsafe chat
* restrict to lesson context
* no personal advice
* no collection of sensitive info
* log and monitor AI responses
* provide parent control

---

# 23. MVP Development Milestones

## Milestone 1: Content + Data Foundation

Deliverables:

* database schema
* module/lesson schema
* passage schema
* question schema
* admin import script
* 3 sample lessons

## Milestone 2: Student Lesson Player

Deliverables:

* student login
* module list
* lesson page
* passage display
* question answering
* evidence selection
* feedback display

## Milestone 3: Scoring + Progress

Deliverables:

* accuracy tracking
* evidence score
* skill progress
* mistake classification
* review screen

## Milestone 4: Diagnostic + Recommendation

Deliverables:

* diagnostic quiz
* skill report
* recommended lesson engine

## Milestone 5: Parent/Admin Dashboard

Deliverables:

* parent progress view
* admin content editor
* lesson publishing workflow

## Milestone 6: Pilot Testing

Deliverables:

* test with 5–10 students
* collect usage data
* collect feedback
* improve lessons
* prepare public launch

---

# 24. MVP Success Criteria

## Learning Success

After 6–8 weeks, students should show improvement in:

* naming the skill being tested
* proving answers with text
* explaining tone with word choice
* explaining paragraph function
* identifying wrong-answer traps
* writing stronger short explanations

## Product Success

For pilot users:

| Metric                                   |               Target |
| ---------------------------------------- | -------------------: |
| Lesson completion rate                   |                 >70% |
| Average lesson time                      |            15–30 min |
| Students completing 8+ lessons           |                 >60% |
| Parent satisfaction                      |        >80% positive |
| Students can explain at least 5 concepts |                 >80% |
| Evidence-score improvement               | visible upward trend |

Do not claim MAP improvement until there is enough data.

---

# 25. Suggested Initial 12 Lessons

For first build, instead of all 36 lessons, start with 12.

| Lesson | Skill               | Text Type                     |
| ------ | ------------------- | ----------------------------- |
| 1      | Main Idea vs Detail | Nonfiction                    |
| 2      | Theme vs Topic      | Short fiction                 |
| 3      | Evidence            | Short fiction                 |
| 4      | Inference           | Narrative                     |
| 5      | Author’s Purpose    | Informational article         |
| 6      | Text Structure      | Science/history article       |
| 7      | Tone                | Opinion paragraph             |
| 8      | Word Choice         | Short nonfiction              |
| 9      | Figurative Language | Poem                          |
| 10     | Argument            | Opinion article               |
| 11     | Poetry Shift        | Poem                          |
| 12     | Paired Texts        | Two short views on same topic |

This is enough for a strong alpha version.

---

# 26. Suggested Lesson Template for Content Writers

Each lesson should be written in this format.

```markdown
# Lesson Title

## Skill
Tone

## Learning Goal
Students will identify tone using exact word choice.

## Concept Explanation
Tone means...

## Micro-Example 1
Text:
Question:
Answer:
Proof:
Explanation:

## Micro-Example 2
Text:
Question:
Answer:
Proof:
Explanation:

## Passage
Title:
Genre:
Text:

## First Read Questions
1.
2.

## Second Read Focus
Highlight three words that reveal tone.

## MAP-Style Questions
Question 1:
Choices:
Correct:
Evidence:
Feedback:
Wrong-answer explanations:

Question 2:
...

## Reflection
What words helped you identify tone?
```

---

# 27. Key Product Differentiators

The app is different from A3000/CommonLit/Khan because:

| Existing Tool | Main Strength               | Gap                                                    |
| ------------- | --------------------------- | ------------------------------------------------------ |
| A3000         | Adaptive nonfiction reading | Not focused enough on explicit concept-to-tool mastery |
| CommonLit     | Great texts/questions       | Less personalized wrong-answer diagnosis               |
| Khan          | Concept lessons             | Less deep close-reading workflow                       |
| ReadTheory    | Adaptive questions          | More quiz-like, less concept coaching                  |
| Newsela       | Nonfiction articles         | Not a close-reading concept trainer                    |

Break 250 Reading Lab differentiates by focusing on:

1. Advanced reader plateau
2. Concept mastery
3. Two-pass close reading
4. Evidence requirement
5. Wrong-answer diagnosis
6. MAP-style analytical reasoning
7. Targeted skill recommendation

---

# 28. Future Features

## 28.1 AI Close-Reading Coach

Student writes an answer. AI responds:

* “Which exact word proves that?”
* “Is this answer too broad?”
* “What is the paragraph doing here?”
* “Can you explain why the other answer is tempting?”

## 28.2 Student Text Upload

Student uploads A3000/CommonLit/school passage.

App asks concept-based questions.

Need copyright/privacy careful design.

## 28.3 Teacher Mode

Teacher assigns:

* module
* lesson
* skill focus
* class progress review

## 28.4 MAP-Style Practice Sets

Mixed sets:

* 20 questions
* adaptive difficulty
* skill breakdown
* improvement report

## 28.5 Reading Recommendation Engine

Based on weak skills:

* weak tone → short stories, speeches, memoirs
* weak argument → editorials, debate articles
* weak poetry → poems with guided analysis
* weak structure → science/history articles

---

# 29. Developer Notes

## 29.1 Must-Have MVP Features

The MVP must include:

* module/lesson structure
* lesson player
* passage display
* MCQ question support
* evidence selection
* feedback display
* wrong-answer feedback
* skill scoring
* progress dashboard

## 29.2 Nice-to-Have MVP Features

* highlighting system
* short explanation scoring
* AI feedback
* parent dashboard
* badges
* adaptive recommendation

## 29.3 Do Not Overbuild First

Avoid:

* huge passage library
* full AI tutor
* complex gamification
* too many question types
* mobile app before web validation
* focus on MAP score guarantees

The value comes from concept clarity and feedback quality.

---

# 30. Final Product Summary

**Break 250 Reading Lab** is a focused app for advanced readers who need to move from strong comprehension to precise analytical reading.

The app teaches 12 high-leverage concepts:

* main idea
* evidence
* inference
* purpose
* structure
* tone
* word choice
* figurative language
* theme
* argument
* poetry
* paired texts

The core user experience is:

> Learn one concept → see micro-examples → read a short text → reread with a focus → answer MAP-style questions → prove with exact text → understand wrong-answer traps → practice the next weak skill.

The most important feature is **not** the passage library.

The most important feature is:

> Helping students understand why the right answer is best supported and why the wrong answer is tempting but wrong.

This is the mechanism that can help strong readers break through a high-level plateau.

