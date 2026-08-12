# STRUCTURE.md — Break 250 Reading

> Architectural overview. Read after `context.md` to understand how the pieces fit and where to make changes. Last updated 2026-05-29.

---

## 1. What it is, in one paragraph

A static, build-free web app that teaches reading analysis to advanced middle-school readers. Three learning surfaces share one 5-category marking vocabulary (Tone, Evidence, Theme, Inference, Structure):

1. **Lessons + Quizzes** — a mini-lesson plus 10 trap-revealing quizzes per sub-concept, organized by the 3 MAP Reading categories (Literary / Informational / Vocabulary).
2. **Reading Lab** — short public-domain passages with *dense* color-coded annotations (every meaningful phrase marked). Where you *learn* the marking moves.
3. **Reading Library** — full-length public-domain works (a play, a story collection, a novel) with *sparse* annotations on the famous moments. Where you *apply* the marking moves at length.

No backend. No build step. Content is CSV (lessons/quizzes) and JSON (lab/library), fetched at runtime. Progress lives in `localStorage`.

---

## 2. Architecture at a glance

```
                          index.html
                  (Tailwind CDN, top nav, #app mount)
                               │
                               ▼
                      src/main.js  (hash router)
        ┌──────────────┬─────────────┬──────────────┬─────────────┐
        ▼              ▼             ▼              ▼             ▼
   views/lesson   views/quiz    views/lab     views/library  views/reference
        │              │             │              │         views/marking-guide
        └──────────────┴──────┬──────┴──────────────┘
                              ▼
                        src/loader.js
              (fetch + parse + validate, per content type)
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   content/lessons/*    content/lab/*.json    content/library/*.json
   content/quizzes/*       (dense anns)        (sparse anns, sections)
       (CSV)
                              │
                              ▼
                       src/progress.js
                  (localStorage: scores, bands;
                   library reading position)
```

Verification spine: **`scripts/validate-content.py`** re-checks every CSV and JSON file against the same rules the runtime loader enforces. It is the CI gate and the single source of "is the content valid?" Current green state: **24 lesson · 24 quiz · 15 lab · 3 library — all valid.**

---

## 3. Routes

All routing is hash-based (`src/main.js`), so the app works from any static host with no server rewrites.

| Route | View | Purpose |
|---|---|---|
| `#/` | `renderHome` (main.js) | Sub-concept directory by category + Lab (grouped by difficulty) + Library card |
| `#/learn/{module}/{slug}` | `views/lesson.js` | Mini-lesson page |
| `#/quiz/{module}/{slug}` | `views/quiz.js` | 10-quiz flow + per-choice feedback + score |
| `#/reference` | `views/reference.js` | Quick Reference — 1-minute pre-read checklist (all lessons' `quick_ref`) |
| `#/marking` | `views/marking-guide.js` | The 20-item marking guide with priority badges |
| `#/lab/{basename}` | `views/lab.js` | Reading Lab passage with dense annotations |
| `#/library` | `views/library.js` → `renderLibraryIndex` | Library catalog |
| `#/library/{basename}` | `views/library.js` → `renderLibraryWorkPage` | Book overview: intro, legend, grouped TOC, discussion prompts |
| `#/library/{basename}/{sectionId}` | `views/library.js` → `renderLibrarySectionPage` | One scene/chapter: prose + footnote highlights + margin notes + prev/next |

The section route is matched **before** the book-overview route in the router (more specific first).

---

## 4. Module-by-module reference

### `index.html`
Entry point. Loads Tailwind via CDN, defines the top nav (Home · Marking Guide · Quick Reference · Library), the `#app` mount point, the privacy footer, and print CSS. No app logic.

### `src/main.js`
Hash router + home page. Owns two hand-maintained catalogs: `CATALOG` (24 lesson entries) and `LIBRARY_CATALOG` (3 works). Renders the home directory grouped by MAP category with status badges, the Lab section grouped by difficulty (Easy/Medium/Hard), and a Library entry card. Delegates everything else to a view module.

### `src/loader.js`
Fetch + parse + validate for all three content types. Contains a minimal RFC-4180 CSV parser (handles quoted cells, embedded commas/newlines, doubled quotes), the lesson/quiz column schemas, and JSON validators for lab texts and library works. Every loader mirrors `scripts/validate-content.py` so the browser and CI agree. Exposes `loadLesson`, `loadQuizzes`, `loadLabText`, `loadLibraryWork`.

### `src/progress.js`
localStorage persistence. Root key `break250.progress.v1`. Stores per-sub-concept `{ lastScore, bestScore, attempts, lastAttemptedAt }` and computes status bands. Library reading position is stored separately by `views/library.js` under `library:progress:{basename}`.

### `src/views/lesson.js`
Mini-lesson renderer. Includes a lightweight markdown renderer (paragraphs, bullets, `> blockquotes`, `**bold**`/`*italic*`, whole-paragraph `**Heading.**` → subheading). Category-keyed gradient header, quick-reference card, "Why this matters" pullout, worked-example cards, numbered "common traps" callouts.

### `src/views/quiz.js`
The teaching engine. 10-question flow with idle→answered→submitted state, per-choice feedback (why each wrong answer is tempting), keyboard shortcuts (1–4 select, Enter submit/advance), a11y roles, score persistence, and status-band end screen. Module 0 is special-cased (no score; "Orientation Complete").

### `src/views/lab.js`
Reading Lab detail. Renders a passage as segments split on annotation boundaries; dense color-coded highlights; click-to-reveal note panel; markup on/off toggle; difficulty badge; bridges the 5-color system to the 20-label marking codes via `marking-guide.js` exports.

### `src/views/library.js`
Three views (index, work overview, section page). The section page is the richest UI: two-column layout (prose + sticky margin-notes column), footnote-style superscripts linking highlights to numbered notes, cross-highlight on click, prev/next nav, IntersectionObserver-free pagination (one section per page), and `localStorage` reading-position memory. The work-overview TOC auto-groups sections on a `" — "` label convention (so Moonstone's 50 sections collapse into named narrator groups).

### `src/views/reference.js` / `src/views/marking-guide.js`
Quick Reference (all lessons' one-line `quick_ref`, printable) and the canonical 20-item Marking Guide (exports `COLOR_TO_CODE` and `MARKING_ITEMS`, consumed by the Lab view).

---

## 5. The 5-category marking system

One vocabulary spans Lab and Library. Colors are consistent everywhere.

| Category | Color | Code family (per `docs/marking.md`) |
|---|---|---|
| `tone` | amber | TO · M · WC · CON · P |
| `evidence` | emerald | E · RSN · TRAP |
| `theme` | sky | TH · T · MI · CL |
| `inference` | violet | INF · POV · SPK |
| `structure` | orange | STR · SHIFT · PF · FIG · CTR |

**Annotation-note rule (enforced):** every Lab/Library note begins with a single official code, and that code's family must match the annotation's category. No mixed prefixes (`TH/FIG`, `E/INF`, etc.). `scripts/rewrite_library_annotations.py` audits this for the Library works.

---

## 6. Content inventory (2026-05-29)

### Lessons + Quizzes — 24 lessons (22 graded sub-concepts + 2 orientation), 240 quizzes
- **Module 0** — orientation, 2 lessons (schema-exempt: no quizzes/traps required): **0.1 The 5 Reading Questions** (the 5-category lens / marking colors), **0.2 The Reading Areas & Tools** (the 3 MAP areas + toolbox)
- **Category A · Literary** — a1–a5 (theme, inference, tone, imagery)
- **Category B · Informational** — b1–b6 (main idea, evidence, tone, paragraph function)
- **Category C · Vocabulary** — c1–c3 (context meaning, connotation, precision, academic verbs)
- Status bands: 9–10 Mastered · 7–8 Good · 5–6 Review · 0–4 Needs Practice. Module 0 → "Orientation Complete" (never scored).

### Reading Lab — 15 texts, 127 annotations
- Difficulty: **Easy 5 · Medium 4 · Hard 6**
- Category: Poetry 6 · Literary 4 · Fable 3 · Informational 2
- Each text: passage + dense annotations (start/end offsets, category, note) + intro + discussion prompts + answers.

### Reading Library — 3 works, 252 annotations
| Work | Type | Sections | Annotations | Words |
|---|---|---|---|---|
| Macbeth (Shakespeare) | play | 28 scenes | 57 | 20,704 |
| The Adventures of Sherlock Holmes (Doyle) | story-collection | 12 stories | 144 | 104,350 |
| The Moonstone (Collins) | novel | 50 sections | 51 | 180,070 |

All public-domain in every major jurisdiction. Murder on the Orient Express is intentionally deferred until it enters PD in life+50 countries on 2027-01-01.

---

## 7. Primary execution flows

**Take a quiz:** `#/quiz/a1/01-…` → `renderQuizPage` → `loadQuizzes` (fetch CSV → parse → validate 10 rows) → in-memory session state → per-question feedback → `recordAttempt()` writes score to localStorage → status band on end screen → home badges update.

**Read a Library section:** `#/library/001-macbeth/act-i-scene-vii` → router matches section route first → `renderLibrarySectionPage` → `loadLibraryWork` (fetch JSON → validate sections + annotation offsets) → `saveProgress(basename, sectionId)` → render prose split on annotation boundaries with footnote markers + sticky margin-notes column + prev/next.

**Author content:** write/generate CSV or JSON → `python3 scripts/validate-content.py` (must print "All content valid") → load in browser to eyeball. Generators (`scripts/gen_library_*.py`) resolve annotation offsets from substrings (never hand-counted) to avoid off-by-N drift.

---

## 8. Build / run / verify

```bash
# Run (any static server)
python3 -m http.server 8000        # then open http://localhost:8000/

# Validate all content (CI gate)
python3 scripts/validate-content.py
```

No bundler, no package.json runtime deps. Tailwind is the only third-party script (CDN). Python 3 is used only for the offline validator and one-shot content generators.

---

## 9. Status: implemented vs planned

**Implemented & browser-verified (2026-05-29):**
- ✅ Home directory with status badges + per-category roll-ups
- ✅ Lesson pages (restyled) + 10-quiz flow + per-choice feedback + score persistence
- ✅ Quick Reference + Marking Guide pages
- ✅ Reading Lab (15 texts, dense annotations, difficulty grouping)
- ✅ Reading Library (3 works, paginated sections, margin notes, grouped TOC, reading-position memory)
- ✅ Content validator (CI) green across all 4 content types

**Planned / not yet done:**
- ⏳ Quiz page visual parity with the restyled lesson page (currently plainer)
- ⏳ Deeper Moonstone annotation coverage (~1/section today)
- ⏳ Orient Express marking companion (commentary-only; unlocks 2027)
- ⏳ Mobile/a11y/Lighthouse audits (partial)
- ⏳ Stack v1 rewrite against target stack (deferred until known)
