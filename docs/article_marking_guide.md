# Article Marking Guide — Suggestions

**Purpose:** Align Reading Lab and future article/poetry markup with the existing Marking Guide, without changing the current app/content yet.

Canonical references:

- `docs/marking.md`
- `docs/marker_checklist.md`
- `src/views/marking-guide.js`

---

## Guiding Principle

Follow the Marking Guide first.

The app currently has 5 Reading Lab color categories:

| Lab category | Marking Guide code | Meaning |
|---|---|---|
| `tone` | `TO` / `WC` | Tone and word choice |
| `evidence` | `E` | Exact proof |
| `theme` | `TH` / `MI` | Theme, main idea, central claim |
| `inference` | `INF` | Clues that suggest something unstated |
| `structure` | `STR` / `PF` | Text structure, paragraph function, shifts |

Do not force every insight into these 5 labels if the better Marking Guide label is more specific. In prose notes, name the exact move: `FIG`, `WC`, `CON`, `SHIFT`, `SPK`, `POV`, `CL`, or `RSN` when useful.

For now, Reading Lab can keep the 5 colors, but the annotation note should say the more precise marking move.

Example:

```text
category: theme
note: "This is really a FIG move first: the master metaphor world = stage supports the larger theme that human life follows roles and stages."
```

---

## Suggested Labeling Rules

### 1. Mark Figurative Language as Figurative First

If a line is a metaphor, simile, personification, symbol, image, hyperbole, or understatement, the note should explicitly call it `FIG`, even if the app color remains `theme`, `tone`, or `inference`.

Use:

- `FIG → TH` when figurative language carries the theme.
- `FIG → TO` when figurative language shapes tone.
- `FIG → INF` when figurative language lets us infer feeling or meaning.

Avoid saying a metaphor is simply "theme" unless the note explains how the metaphor supports the theme.

### 2. Use Tone Only for Attitude

Mark `tone` only when the words reveal the author's or speaker's attitude.

Good tone evidence:

- emotionally loaded diction,
- hedging or distancing words,
- mocking, admiring, bitter, nostalgic, skeptical, urgent, reflective language,
- tone shifts.

Do not mark something as tone just because it is beautiful, figurative, or important.

### 3. Use Structure for Shape, Repetition, Turns, and Function

Mark `structure` when the text is doing something with form:

- repeated pattern,
- stanza shift,
- volta / turn,
- final couplet,
- paragraph function,
- sequence of examples,
- contrast setup,
- repeated line with changed meaning.

In poetry, repeated lines and stanza mirroring are usually structure first.

### 4. Use Evidence for Proof, Not Just Important Lines

Mark `evidence` when the highlighted words prove a specific claim.

Evidence notes should answer:

> What claim does this prove?

If the line is important but does not prove a stated claim, it may be better as `theme`, `structure`, `tone`, or `inference`.

### 5. Use Inference for Clues

Mark `inference` when the text gives a clue and the reader must conclude something unstated.

Common inference clues:

- character action,
- a reaction by another character,
- what is not said,
- setting details,
- repeated behavior,
- contradiction between what someone says and what happens.

### 6. Use Theme / Central Idea for the Point

Mark `theme` when the text states or strongly develops the message, central claim, or deeper point.

For literary texts, theme should usually be expressible as a full sentence.

For informational texts, this may be central idea or claim.

---

## Poetry-Specific Suggestions

Poetry needs special care because one line often does several jobs at once.

When marking poetry, use this order of thought:

1. Is this line figurative language or imagery?
2. Does it create tone?
3. Does it support theme?
4. Does it mark a structural turn or pattern?
5. Does it give a clue for an inference?

The note can mention multiple layers, but the first sentence should name the most direct move.

Example:

```text
This is a FIG move first: "Life's but a walking shadow" is a metaphor. It supports the theme that life feels insubstantial and meaningless to Macbeth.
```

---

## Suggestions For Current Poetry Lab Files

These are suggestions only. No content has been changed.

### `content/lab/001-sonnet-18.json`

- `Thou art more lovely and more temperate` is currently marked as `theme`. Better note: this is the poem's **central claim** more than the full theme.
- Lines 3-8 are marked as `evidence` for summer's flaws. Check the character range to make sure the highlighted span actually covers all the flaws named in the note.
- `eternal lines` is marked as `tone`. This is defensible, but the note should also name the `FIG/WC` move: the phrase turns poetry itself into the instrument of immortality.

### `content/lab/007-all-the-worlds-a-stage.json`

- `All the world's a stage` is currently marked as `theme`. It should be explained as **FIG first**: a master metaphor that supports the central idea.
- `bubble reputation` is marked as `theme`. Better note: this is **FIG/WC** supporting the theme that reputation is fragile and temporary.
- The seven ages structure is strong. Keep the `structure` label for the announced seven-part organization.

### `content/lab/008-tomorrow-and-tomorrow.json`

- `Life's but a walking shadow, a poor player` is currently marked as `theme`. Better note: **FIG first**, theme second. The metaphors support Macbeth's belief that life is insubstantial and meaningless.
- `That struts and frets his hour upon the stage` is currently marked as `structure`. It is more directly **FIG/WC/Tone** because it extends the actor metaphor and uses dismissive verbs.
- `Tomorrow, and tomorrow, and tomorrow` as `structure` is good: repetition/anaphora creates the sense of dragging time.

### `content/lab/012-who-has-seen-the-wind.json`

- `Neither you nor I` is currently marked as `tone`. Better as `structure`: it mirrors and slightly varies `Neither I nor you`.
- `But when the trees bow down their heads` is currently marked as `tone`. Better note: **FIG/personification** plus inference. The trees' movement lets us infer the wind's presence.
- `The wind is passing through` is marked as `theme`. Better as inference/evidence unless the note clearly connects it to the larger theme: invisible forces are known by visible effects.

### `content/lab/014-the-road-not-taken.json`

This is mostly strong.

- `yellow wood` as a sign of autumn/endings is plausible, but phrase it as an interpretive possibility rather than certainty.
- The `evidence` markings around the roads being equal are good and pedagogically useful because they correct a common misreading.
- The final famous line as `inference` is strong: students must infer that the future speaker may be reshaping the story.

### `content/lab/015-stopping-by-woods.json`

- `My little horse must think it queer...` is currently marked as `structure`. Better as `inference`: the horse's reaction shows the stop is unusual.
- `His house is in the village though` currently supports an inference that the speaker is relieved. Soften this: we infer he is aware of ownership and of not being seen; "relieved" may be too strong.
- First `And miles to go before I sleep` is marked as `evidence`. Better as `structure` or theme setup: the repetition changes the meaning on the second occurrence.
- Second `And miles to go before I sleep` as `theme` is strong.

---

## Recommended Annotation Note Pattern

Use this pattern for future notes:

```text
[Primary marking code]: [what the words are doing]. This supports [larger reading move] because [specific reason].
```

Examples:

```text
FIG: "All the world's a stage" is a master metaphor. It supports the central idea that human life follows roles and stages.
```

```text
STR: The repeated question begins the second stanza. The repetition creates a pattern, and the tiny changes underneath make the reader compare the two stanzas.
```

```text
INF: The horse thinks the stop is strange, so we infer the speaker is doing something unusual by pausing here.
```

---

## Recommendation

Do not change the app colors immediately.

Instead:

1. Keep the current 5 Reading Lab categories for visual simplicity.
2. Update annotation notes over time so they explicitly use the richer Marking Guide codes.
3. If poetry markup keeps feeling forced, add a sixth visual category later: `figurative` / `FIG`.

This preserves the simple color system while making the pedagogy more accurate.
