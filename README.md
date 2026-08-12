# Break 250 Reading

A focused reading-analysis trainer for advanced middle-school readers (Grade 5–8, MAP Reading ~230–249) trying to break 250+.

**Status:** MVP built on Stack v0 and browser-verified (2026-05-29). Three learning surfaces live.

---

## What this is

Not a general reading app. Not a passage library. Not a quiz mill.

Three surfaces sharing one 5-category marking vocabulary (Tone · Evidence · Theme · Inference · Structure):

**1. Lessons + Quizzes** — a **mini-lesson + 10 trap-revealing quizzes per sub-concept**, organized by the three MAP Reading scoring categories:
- **Category A — Literary Text** (fiction, narrative, poetry)
- **Category B — Informational Text** (nonfiction, articles, argument)
- **Category C — Vocabulary** (context meaning, nuance, lexicon)
- Plus **Module 0** — a one-lesson orientation that maps all the tools.

**2. Reading Lab** — short public-domain passages with *dense* color-coded annotations (every meaningful phrase marked). Where you **learn** the marking moves. 15 texts, grouped Easy / Medium / Hard.

**3. Reading Library** — full-length public-domain works with *sparse* annotations on the famous moments. Where you **apply** the moves at length. Macbeth, The Adventures of Sherlock Holmes, The Moonstone.

Supporting pages: **Marking Guide** (`#/marking`) and **Quick Reference** (`#/reference`).

See `docs/why_250.md` for the product manifesto, `docs/curriculum_design.md` for the curriculum, and `docs/STRUCTURE.md` for the architecture.

---

## Stack

**Stack v0 (this version): Pure static.**

- HTML + vanilla JavaScript (ES modules)
- Tailwind CSS via CDN (no build step)
- Content as CSV files in `content/`, fetched at runtime
- Progress persisted in `localStorage`
- No backend, no database, no auth

Chosen so the first end-to-end test can ship without a build pipeline. A future v1 will rewrite against a target stack (likely matching mywordbank.net's stack).

---

## Run locally

No build step required. Any static HTTP server works:

```bash
# Option 1: Python
python3 -m http.server 8000

# Option 2: Node (if installed)
npx serve .
```

Then visit `http://localhost:8000/` in a browser.

---

## Validate content

Validates every CSV in `content/` against the locked schema (`docs/csv_schemas.md` v1.1):

```bash
python3 scripts/validate-content.py
```

CI runs this on every push.

---

## Repository layout

```
reading_app/
├── index.html              # entry point (Tailwind CDN, top nav, #app)
├── src/
│   ├── main.js             # hash router + home page + catalogs
│   ├── loader.js           # fetch+parse+validate (CSV + JSON)
│   ├── progress.js         # localStorage scores + status bands
│   └── views/              # lesson · quiz · lab · library · reference · marking-guide
├── content/
│   ├── lessons/{m0,a1–a5,b1–b6,c1–c3}/   # 23 mini-lessons (CSV)
│   ├── quizzes/{…}/                       # 24 × 10 = 240 quizzes (CSV)
│   ├── lab/*.json                         # 15 dense-annotation Lab texts
│   └── library/*.json                     # 3 long-form Library works
├── scripts/
│   ├── validate-content.py                # schema validator (CI gate)
│   ├── gen_library_*.py                   # one-shot Gutenberg parsers
│   └── fix_lab_offsets.py · rewrite_library_annotations.py
├── docs/
│   ├── STRUCTURE.md                       # architecture overview
│   ├── Diary.md                           # dated development log
│   ├── curriculum_design.md               # curriculum spec (v3.1.3)
│   ├── csv_schemas.md                     # locked CSV schemas (v1.1)
│   ├── marking.md · article_marking_guide.md  # marking codes + conventions
│   ├── why_250.md · review_packet.md      # manifesto · reviewer doc
│   └── …
├── .github/workflows/ci.yml               # validate content
├── status.md · progress.md · project_plan.md · progress_tracking.md
└── design1.md · context.md · feedback.md · review.md · test_status.md
```

---

## Documentation order (for new contributors)

1. `docs/why_250.md` — what we're trying to do and why
2. `docs/curriculum_design.md` — the 3 categories, modules, and sub-concepts
3. `context.md` — current architectural state
4. `status.md` — what's happening right now
5. `docs/csv_schemas.md` — content authoring format
6. `project_plan.md` and `progress_tracking.md` — engineering phases and components

---

## Worked sample

The canonical content example lives at:

- `content/lessons/b4/01-neutral-vs-skeptical.csv`
- `content/quizzes/b4/01-neutral-vs-skeptical.csv`

This is **B4.1 "Neutral vs Skeptical"** — the highest-leverage Tone sub-concept. New content writers should read these two files before drafting their own sub-concepts.

---

## License

TBD.
