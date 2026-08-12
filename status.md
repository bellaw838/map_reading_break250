# status.md — Current focus

**As of:** 2026-05-28
**Phase:** Reading Lab v1 shipped (Path B per the brainstorming session)
**Curriculum:** LOCKED v3.1.3
**Schemas:** LOCKED v1.1 + Reading Lab JSON schema (informal v1)
**Stack:** LOCKED v0 (pure static)

## What just shipped — Reading Lab

A new top-level section on the home page: **6 public-domain texts with color-coded annotations** demonstrating how an advanced reader marks up a passage.

| # | Title | Author | Year | Category | Length |
|---|---|---|---|---|---|
| 1 | Sonnet 18 | Shakespeare | 1609 | Poetry | 14 lines |
| 2 | The Gettysburg Address | Lincoln | 1863 | Informational speech | 272 words |
| 3 | "I went to the woods…" (Walden) | Thoreau | 1854 | Opinion essay | 156 words |
| 4 | Opening of Huckleberry Finn | Twain | 1884 | Literary | 152 words |
| 5 | Opening of "The Gift of the Magi" | O. Henry | 1905 | Literary short story | 305 words |
| 6 | The Boy Who Cried Wolf | Aesop | 1867 | Fable | 155 words |

All US public domain (pre-1929). Total: **45 annotations + 25 discussion prompts** across the 6 texts.

## Color system

| Color | Tool category |
|---|---|
| 🟡 Amber | Tone & Word Choice |
| 🟢 Green | Evidence |
| 🔵 Blue | Theme / Central Idea |
| 🟣 Purple | Inference Clues |
| 🟠 Orange | Structure / Function |

## UX

- Sticky color legend at top of each text page
- **Show markup / Hide markup** toggle (defaults to ON)
- Click any colored span → annotation note appears below the passage
- Discussion prompts at the bottom — tied to the markup
- Source link to Project Gutenberg / Library of Congress for the original full text

## How to run

```bash
python3 -m http.server 8000
# visit http://localhost:8000/
# scroll down to the "Reading Lab" section
# click any of the 6 texts
```

## Files added/changed this round

```
docs/superpowers/specs/2026-05-28-reading-lab-design.md   [NEW]  Design spec
content/lab/001-sonnet-18.json                            [NEW]  Sonnet 18
content/lab/002-gettysburg-address.json                   [NEW]  Gettysburg Address
content/lab/003-walden-i-went-to-the-woods.json           [NEW]  Walden excerpt
content/lab/004-huck-finn-opening.json                    [NEW]  Huck Finn opening
content/lab/005-gift-of-the-magi-opening.json             [NEW]  Gift of the Magi opening
content/lab/006-boy-who-cried-wolf.json                   [NEW]  Boy Who Cried Wolf
src/loader.js                                             [extended] + loadLabText() + validation
src/views/lab.js                                          [NEW]  Reading Lab detail page
src/main.js                                               [updated] + Reading Lab section on home + #/lab/{id} route
scripts/validate-content.py                               [extended] + lab JSON validation
```

## Validator summary

```
$ python3 scripts/validate-content.py
Validated 23 lesson · 23 quiz · 6 lab file(s).
All content valid.
```

## Path to D (later)

Once Reading Lab v1 is dogfooded, add small annotated micro-passages (50–100 words, 2–3 annotations) inside each existing sub-concept lesson. Same color system, same JSON shape, same renderer.

## Phase status

| Phase | Status |
|---|---|
| Phase 0 — Foundations | ✅ |
| Phase 1 — Lesson + Quiz flow | ✅ |
| Phase 3 — Progress tracking + dashboard | ✅ |
| Phase 4 — Module 0 special handling | ✅ |
| Phase 5 — Quick Reference page | ✅ |
| Phase 6 — Polish, a11y, privacy | Partial |
| **Reading Lab v1 (new)** | ✅ **shipped this round** |

## What's still open

- **Pedagogical SME review** of 23 content packs + 6 Reading Lab annotations.
- **Full Playwright + axe-core scan** — needs browser-test environment.
- **Mobile testing** on real devices.
- **Lighthouse CWV** measurement.
- **Pilot parent-consent doc**.
- **Reading Lab v2 (Path D)** — embed micro-passages in sub-concept lessons.
- **Stack v1 rewrite** when target stack is known.

## Watch-outs

- Reading Lab annotations are architect-authored. SME review especially valuable here because the markup IS the teaching.
- Annotation character offsets are hand-counted. Any future passage edits require recomputing offsets — flagged in `docs/superpowers/specs/2026-05-28-reading-lab-design.md`.
- v0 stack is throwaway. Reading Lab JSON files migrate to v1 stack as-is.
