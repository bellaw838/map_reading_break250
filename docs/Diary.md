# Diary.md — Break 250 Reading

> Development log. Newest entries at the bottom of each dated section. Records what changed and *why*, not just *what*.

---

## 2026-05-27 — Stack lock + worked sample

- Locked **Stack v0 = pure static** (HTML + vanilla JS ES modules + Tailwind CDN + CSV content + localStorage). Rationale: smallest surface to validate the content schema and UX end-to-end with no build pipeline. A v1 rewrite against a target stack is deferred until that stack is known.
- Authored the canonical worked sample (B4.1 "Neutral vs Skeptical") to prove the CSV schemas before committing to a framework.
- Locked CSV schemas (`docs/csv_schemas.md` v1.1): 26-col lesson, 14-col quiz, with a Module 0 exception (orientation lesson is not scored and may use N/A for trap/example fields).

## 2026-05-28 — Curriculum + core flow + 230 quizzes

- Restructured the curriculum around the 3 MAP scoring categories (Literary / Informational / Vocabulary) plus Module 0 orientation. Canonical spec: `docs/curriculum_design.md`.
- Built the core flow end-to-end: CSV loader (`loader.js`), lesson page, 10-quiz flow with per-choice feedback (the teaching engine), score + status bands, localStorage progress, home directory with badges, Quick Reference page.
- Authored all 23 MVP content packs (230 quizzes). Fixed recurring authoring hazards: CSV column-shift from unquoted commas (now always generated via Python `csv.writer`), and B-heavy correct-answer distributions (rebalanced to ~3-3-2-2).

---

## 2026-05-29 — Reading Lab, difficulty system, marking guide

- **Reading Lab built**: public-domain passages rendered with *dense* color-coded annotations (5 categories: tone/evidence/theme/inference/structure), click-to-reveal notes, markup toggle. Stored as JSON (better than CSV for long passages + structured annotation offsets). Why JSON: annotations need integer start/end offsets and per-annotation category+note; a flat CSV row can't express that cleanly.
- Seeded 9 texts (incl. Shakespeare sonnet/soliloquies, Gettysburg, Walden, Huck Finn, Gift of the Magi, Aesop, Dickens).
- **Difficulty system added**: every lab text tagged Easy/Medium/Hard; home page Lab section grouped by difficulty with "Start here / Step up / Challenge" hints. Added 6 new Easy/Medium texts (Aesop fables, Rossetti, Grahame, two Frost poems) to balance a Hard-heavy library → 15 texts total (Easy 5 · Medium 4 · Hard 6).
- **Marking guide wired in**: `docs/marking.md` (20-item, 5-family code system) surfaced as a `#/marking` page; Lab notes bridge the 5 colors to the precise codes.

### Annotation offset audit + fix
- Found the first batch of lab annotations had **hand-counted offsets that were wrong** (e.g. Sonnet 18's "But" volta highlighted "l summ"; Tomorrow soliloquy cropped mid-word). Root cause: offsets written by hand.
- Fix: `scripts/fix_lab_offsets.py` re-anchors every annotation by **substring lookup** instead of hand-counted integers. 57 offsets corrected across 9 files. New generators always compute offsets from substrings — verified visually in-browser later.

### Marking-guide consistency pass on poetry
- Applied `docs/article_marking_guide.md` suggestions: poetry notes now lead with the most direct move (FIG/personification before "theme"), and several mis-categorized annotations were re-labeled (e.g. "Neither you nor I" tone→structure; "horse must think it queer" structure→inference).

### Discussion answers
- Added `discussion_answers` (parallel array to `discussion_prompts`) to all 15 lab texts — teacher-style sample responses revealed via click-to-expand. Validator enforces equal-length arrays.

### Reading Library subsystem (3 works)
- Built a second long-form surface distinct from the Lab: full works with *sparse* marking only at famous moments. Sourced full texts from Project Gutenberg via one-shot parser scripts (`scripts/gen_library_{macbeth,sherlock,moonstone}.py`).
  - **Macbeth** (play, 28 scenes, 57 annotations)
  - **The Adventures of Sherlock Holmes** (story collection, 12 stories, 144 annotations)
  - **The Moonstone** (novel, 50 sections, 51 annotations) — chosen as the public-domain stand-in for Christie, whose work is not yet PD anywhere (Orient Express deferred to 2027-01-01).
- Why these three: Macbeth for structure/theme density, Sherlock for inference (clue→reasoning→conclusion), Moonstone for point-of-view / unreliable narration (its 8 narrator voices are the teaching point).

### Library UX rebuild (paginated)
- First version was one giant single-page render with broken in-page `#sec-` anchors and notes hidden at the bottom. Rebuilt into **per-section pages**: `#/library/{book}/{section}`. Each section page = two columns (prose + sticky margin-notes), footnote-style superscripts linking highlights to numbered notes, a prominent color legend, prev/next nav, and `localStorage` reading-position memory. The work-overview page got a grouped, collapsible TOC (auto-groups on `" — "` labels, so Moonstone's 50 sections fold into named narrator groups).

### Lesson page redesign
- Rebuilt `views/lesson.js` markdown renderer to handle `*italic*`, `> blockquotes`, and whole-paragraph `**Headings**` (previously rendered as raw asterisks / inline bold). Restructured the page: category-keyed gradient header, quick-reference card, "Why this matters" pullout (a field that previously rendered nowhere), worked-example cards, numbered trap callouts.

### Library annotation LLM-review + audit
- Passed all three Library works through an annotation rewrite that normalizes every note to start with **one** official marking code matching its category family (no mixed `TH/FIG`, `E/INF`, `STR/narrator shift` prefixes). `scripts/rewrite_library_annotations.py` applies the rewrites and audits prefix↔family consistency. Result: Macbeth 57/57, Moonstone 51/51, Sherlock previously done — all audit-clean.

### Browser QA pass (this session)
- Served the app and drove it headless (gstack `browse`). Screenshotted and visually verified: home, lesson (redesign confirmed — markdown, blockquote, pullout, example cards, trap callouts all render), quiz, Library index, Macbeth overview + section (margin notes + footnote highlights + prev/next confirmed), Moonstone grouped TOC (50→named groups confirmed), Lab Sonnet 18 (offset fixes visually confirmed — "But" correctly marks the volta).
- **Verdict:** no broken pages, no console errors (only the expected Tailwind-CDN production warning). One confirmed gap: the quiz page is functional but visually plainer than the redesigned lesson page (parity work outstanding).
- Updated the mandated docs to match reality (this file, `STRUCTURE.md`, `context.md`, `README.md`) — they had drifted badly (context.md still claimed "pre-implementation").

### Reading Lab display fix (poetry)
- Browser QA of the Lab surface found poems rendering badly — Sonnet 18's lines staggered rightward, line 1 indented, multi-line highlights breaking alignment. Prose (Gettysburg, Tale of Two Cities) was fine.
- **Two root causes in `views/lab.js`:**
  1. The passage container used `white-space: pre-wrap`, which preserved the **template literal's own newline + indentation** (`\n          ` between `<div>` and `${passageHtml}`) as a leading blank line + indent. Fix: inline `${passageHtml}` directly against the tags so no template whitespace enters the rendered text.
  2. Highlights were `<button>` elements, which default to `display: inline-block` — they don't participate in normal inline line layout, so multi-line annotations rendered as tall boxes and broke verse alignment. Fix: switched to inline `<span role="button" tabindex="0">` (+ Enter/Space keyboard handler, + selected-state ring). Inline spans flow and wrap per-line, so a multi-line annotation now highlights each line cleanly like a real marker stroke.
- Verified in-browser: Sonnet 18 and "Who Has Seen the Wind?" now left-align cleanly with per-line highlights; Gettysburg prose unchanged (no regression); clicking a highlight rings it and shows the note. Annotation offsets untouched (the passage string is never trimmed — only template whitespace was removed).

---

## 2026-06-01 — Module 0 layout fix + new orientation lesson

### M0 page rendered tables as raw pipes
- The "Reading Areas & Tools" lesson uses a markdown comparison table (`| Basic reader asks | Advanced reader asks |`), but `views/lesson.js`'s markdown renderer had no table support — it dumped the raw `| … |` pipes as a run-on paragraph. That was why Module 0 still looked unfinished next to the redesigned A1.1 page.
- Fix: added GitHub-flavored table support to the renderer (buffer pipe-lines → parse cells → skip the `--- | ---` separator row → emit a styled `<table>` with bold header + zebra rows). Verified the M0 comparison table now renders cleanly.

### New Module 0 orientation lesson + reorder
- Decision (the user asked which order): teach the **5-category lens first**, the tools second. The five questions are the most fundamental frame, every question is one of them, and they are literally the 5 highlight colors used in the Lab/Library — so learning them first makes the marking colors legible everywhere else. `docs/marking.md` is ordered the same way.
- Added **0.1 "The 5 Reading Questions"** (`content/lessons/m0/01-five-questions.csv`): the five big questions (saying / proving / suggested / feeling / built), a 3-column table mapping each to what the test actually asks and to its mark color, and the "first move on every question" habit. Orientation lesson — no quiz, schema-exempt.
- Renumbered the existing tools lesson to **0.2 "The Reading Areas & Tools"** (was titled inconsistently — home said "The 8 Reading Tools," the CSV said "The 3 Reading Areas"; unified both). Updated `CATALOG` in `main.js` to list 0.1 before 0.2.
- Home footer count made unambiguous/dynamic: `${CATALOG.length} lessons · 230 quizzes · {lab} lab texts · {library} library books`.
- Validator green: **24 lesson · 23 quiz · 15 lab · 3 library**. Browser-verified: home shows 0.1 then 0.2 under Orientation; the new 0.1 page renders with the design-language header, the table, the blockquote, and the "Why this matters" pullout.

### Regression caught + fixed: blank front page
- The home-footer count edit referenced `${LIBRARY_CATALOG.length}`, but `LIBRARY_CATALOG` is defined in `views/library.js`, **not** in `main.js`. `renderHome()` threw `ReferenceError: LIBRARY_CATALOG is not defined` before painting, leaving the page stuck on the "Loading…" placeholder (the earlier passing screenshot predated this edit, so it slipped through).
- Lesson: the content validator does **not** catch JS runtime errors — only a browser load does. A blank `#app` (innerHTML ~75 chars = just the loader) is the tell. Fix: replaced the undefined reference with the literal `3 library books` (main.js doesn't own the library catalog). Re-verified in a fresh browser: full render, no console errors.

### Module 0 polish: definition-list rendering + quizzes surfaced
- **Display:** 0.1/0.2 looked flatter than A/B/C because their bold-lead `**Term** — description` bullet lists rendered as a monochrome bullet wall (0.2 had three stacked). Added definition-list rendering to the lesson markdown renderer: a list where *every* item is `**Term** — desc` (em/en dash, hyphen, or colon) renders as a styled term/description grid (bordered rows, term column) instead of bullets. Conservative trigger — A/B/C's `*italic* →` bullets don't match, so they're untouched. Verified: 0.2's three tool sections are now clean definition lists; 0.1's "Why these five" too.
- **Quizzes:** both M0 lessons have valid 10-question *recognition* quizzes (`content/quizzes/m0/{01-five-questions,abstract}.csv`), but `lesson.js` deliberately hid the quiz button for `m0` (the old "orientation = no quiz" design), so they were unreachable. Unhid the button (labelled "Try 10 recognition quizzes →" for m0).
- **Scoring decision (user):** keep the **orientation framing** — quizzes run with full per-choice feedback, but the end screen stays "Orientation Complete" and the home badge shows that, not a score. `quiz.js`/`progress.js` already implement this, so no scoring code changed. Browser-verified the full flow: pick → Submit → per-choice feedback ("✓ Correct. WHY A IS RIGHT…") → Next → … → Orientation Complete.
- Validator: **24 lesson · 24 quiz · 15 lab · 3 library**, all valid.

### Front page redesign — visual hierarchy
- Complaint: section names were all `text-xs uppercase text-slate-500` (tiny, identical, gray) — impossible to tell they were section headers, and all six sat at one flat level with no grouping.
- Rebuilt `renderHome` with a **two-level hierarchy**: bold accent-barred **surface headers** (`surfaceHeader()` — colored bar + `text-xl font-bold` + underline) for the three surfaces (Lessons & Quizzes / Reading Lab / Reading Library), and color-dotted **category headers** (`categoryHeader()`) for the four lesson categories (Orientation=slate, A=rose, B=sky, C=emerald — mirroring the lesson-page gradient themes). Added a gradient hero, grouped the 4 lesson categories under the "Lessons & Quizzes" surface, and made the Library preview show all 3 books (was Macbeth only) via a small `LIBRARY_HOME` list.
- Bug caught in review: passed `"Lessons &amp; Quizzes"` to `surfaceHeader`, which escapes again → rendered literal `&amp;`. Fixed to plain `&`.
- Browser-verified: clean render, no console errors, headers clearly distinguishable at both levels.

### Surface priority pills
- Added priority signals to the three surface headers so a student knows where to spend limited time (matches the leverage hierarchy from the "is it enough for 250" assessment): **Lessons & Quizzes → Core** (solid indigo), **Reading Lab → Recommended** (amber), **Reading Library → Optional · Experimental** (slate).
- Design note: the user originally proposed "Optional/Experimental **with AI**" for the Library. Dropped "with AI" from the label because (a) *all* surfaces have AI-authored content, so it's not a Library-specific distinguisher, and (b) "with AI" reads like an AI *feature* rather than AI-*authored*. Instead the Library blurb now carries an honest maturity note: "Our newest surface; annotations are AI-drafted, so treat them as a model rather than gospel." Lab blurb updated too: "You don't need all 15 — work through a few across the difficulty levels."
- Implemented as a reusable `priorityPill(label, kind)` + `surfaceHeader(title, accentBar, badge, right)`. Browser-verified.

### Landing pitch — Harry Potter worked example rewrite
- The home hero gained a landing pitch (Strong Reader vs 250+ Reader). Rewrote only the "Example" block (scope: don't touch other parts) into a proper worked example:
  - Fuller Mirror of Erised story (discovers it → sees the family he never knew → returns because the image gives him what he wants → Dumbledore's warning + quotes).
  - A/B/C/D question with **D** as the best-supported answer ("…it does not do to dwell on dreams and forget to live"); A/B/C are true-but-not-best distractors.
  - Folded the Strong-reader → 250+-reader comparison *into the answer*: strong reader knows the main idea and picks a true detail (A/B/C); 250+ reader **finds the author's idea** (danger of living inside a wish instead of a real life), **proves it with exact evidence** ("dwell on dreams and forget to live"; "neither knowledge or truth"), and **separates inference from guessing** to choose D.
- Browser-verified; validator green (24 · 24 · 15 · 3). Note: user/linter also revised many Lab JSON intros + annotation notes this session — all still validate.
