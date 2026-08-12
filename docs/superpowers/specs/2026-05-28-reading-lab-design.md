# Reading Lab — Design Spec

**Status:** Approved (2026-05-28)
**Scope:** v1 — curated library of 6 public-domain texts with color-coded annotations.
**Path to v2 (later):** embed small annotated micro-passages inside each existing sub-concept lesson.

---

## Purpose

Demonstrate the **reader-as-marker habit**: an advanced reader doesn't just read a text — they actively mark up tone words, evidence, theme statements, inference clues, and structural moves. Reading Lab shows finished examples of that markup on real, classic public-domain texts.

The teaching move: *show the habit, then ask the student to copy it on a fresh text (in print, with a real marker).*

---

## Where it lives

- **New top-level section on the home page** after Category C, titled **"Reading Lab."**
- **Detail pages** at `#/lab/{id}`.
- **Sticky color legend** on each detail page so the markup is decoded at a glance.

---

## Starter set (6 texts)

| # | Title · Author · Year | Category | Length |
|---|---|---|---|
| 1 | **Sonnet 18** · Shakespeare · 1609 | Poetry | 14 lines |
| 2 | **The Gettysburg Address** · Lincoln · 1863 | Informational speech | 272 words |
| 3 | **"I went to the woods…"** (excerpt from *Walden*) · Thoreau · 1854 | Opinion essay | ~150 words |
| 4 | **Opening of *The Adventures of Huckleberry Finn*** · Twain · 1884 | Literary fiction | ~150 words |
| 5 | **Opening of "The Gift of the Magi"** · O. Henry · 1905 | Literary short story | ~300 words |
| 6 | **The Boy Who Cried Wolf** · Aesop (Townsend translation, pre-1900) | Fable | ~150 words |

All US public domain (pre-1929). Mix of literary, informational, poetry, fable.

---

## Color system (5 colors)

| Color | Tool category |
|---|---|
| 🟡 Amber | **Tone & Word Choice** |
| 🟢 Green | **Evidence** |
| 🔵 Blue | **Central Idea / Theme** |
| 🟣 Purple | **Inference Clues** |
| 🟠 Orange | **Structure / Paragraph Function** |

Five colors is the visual-clarity sweet spot. Figurative Language doesn't get its own color in v1 — it overlaps with Tone/Theme often.

---

## Content format — JSON

Existing CSV format doesn't handle long passages + structured range annotations. New content type uses one JSON file per text under `content/lab/`.

### Schema

```json
{
  "id": "lab-002-gettysburg",
  "title": "The Gettysburg Address",
  "author": "Abraham Lincoln",
  "year": 1863,
  "source_url": "https://www.loc.gov/...",
  "category": "Informational",
  "length_words": 272,
  "intro": "Two minutes long…",
  "passage": "Full text of the passage as a single string. Newlines preserved.",
  "annotations": [
    {
      "start": 0,
      "end": 105,
      "category": "structure",
      "note": "Opens in the past — anchors the argument in history."
    }
  ],
  "discussion_prompts": [
    "Find where Lincoln shifts from past to present. What's the structural job of that shift?",
    "Which words carry the speech's tone of solemnity?"
  ]
}
```

### Rules

- `id` matches filename (`lab-{NN}-{slug}.json`).
- `category` ∈ {`Literary`, `Informational`, `Poetry`, `Fable`}.
- `annotations[].start` and `end` are character offsets into `passage` (0-indexed, exclusive end).
- `annotations[].category` ∈ {`tone`, `evidence`, `theme`, `inference`, `structure`} — drives the color.
- `annotations[].note` is the teaching commentary shown when the range is selected.
- Annotations may overlap (the renderer handles overlap by stacking).
- 3–7 annotations per text — enough to demonstrate the habit, not so many it looks like graffiti.
- 2–5 discussion prompts per text — tied to the markup, encourage rereading.

---

## UI

### Reading Lab section on home (`#/`)

- Sits after Category C as a new section.
- Card grid: title · author · year · category · length · 1-line intro snippet.
- Each card links to `#/lab/{id}`.

### Text detail page (`#/lab/{id}`)

- Title, author, year, source link (opens external in new tab).
- Intro paragraph — what to watch for.
- **Color legend strip** at the top (sticky).
- **Toggle button:** "Show markup" / "Hide markup" — defaults to ON (markup visible by default; user can read it clean).
- **Passage** rendered as one block, preserving newlines. Annotated ranges show colored background. Clicking a range reveals the annotation note in a panel below the passage.
- **Discussion prompts** at the bottom.
- Back link to home.

### A11y

- Keyboard-navigable annotated ranges (focusable buttons within the passage).
- `aria-label` on each range explaining its category.
- Color legend doubles as semantic labels so colorblind users get text not just hue.

---

## File layout

```
content/lab/
  001-sonnet-18.json
  002-gettysburg-address.json
  003-walden-i-went-to-the-woods.json
  004-huck-finn-opening.json
  005-gift-of-the-magi-opening.json
  006-boy-who-cried-wolf.json

src/
  loader.js                — add loadLabText(id) + loadLabCatalog()
  views/
    lab.js                 — listing rendered inline on home
    lab-text.js            — single-text detail page
  main.js                  — add #/lab/{id} route; add Reading Lab section to home

scripts/
  validate-content.py      — extend to validate lab JSON files
```

---

## Path to v2 (deferred)

Add an embedded micro-passage to each existing sub-concept lesson page (50–100 words, 2–3 annotations) using the same color system + the same renderer. Reuses everything.

---

## Out of scope for v1

- Interactive student annotation (let student mark up their own ranges) — deferred to v3+.
- Annotation editing UI (admin tool) — content is hand-authored in JSON for v1.
- Audio narration — could be added later.
- Filter/search across the library — 6 texts don't need it; revisit at 30+ texts.

---

## Implementation order

1. Schema doc (this spec + extending `scripts/validate-content.py`).
2. JSON loader extension (`src/loader.js`).
3. Six hand-annotated content files.
4. Lab view + text detail view (`src/views/lab.js`, `src/views/lab-text.js`).
5. Home page section + router.
6. Smoke test against the running static server.

**Estimated total:** half a day of engineering + content authoring combined.
