# Break 250 Reading — Apple App Design (v1)

**Date:** 2026-08-14
**Status:** Design approved; implementation plan not yet written.
**Scope:** Native iOS/iPadOS app for the Lessons + Quizzes surface, plus a Review queue.

---

## 1. Purpose

Bring the website's core surface — 24 mini-lessons and 240 trap-revealing quizzes — to iPhone and iPad as a native app, and add the one habit mechanism the website lacks: a review queue of questions the student got wrong.

The 24 lessons are 22 graded sub-concepts plus 2 Module 0 orientation lessons (0.1 "The 5 Reading Questions" and 0.2 "The Reading Areas & Tools"). All 24 have 10 quizzes each; the Module 0 quizzes are recognition-format and reported as completion, not score.

The website (`https://bellaw838.github.io/map_reading_break250/`) remains the full product, including Reading Lab and Reading Library. The app v1 is deliberately the Core surface only.

### Non-goals for v1

- Reading Lab and Reading Library (planned for later versions).
- Accounts, sync, or any server component.
- Localization. The target user reads at MAP 240+, so the app is English-only.
- Theme switching. One academic theme.
- Spaced repetition scheduling, streaks, or XP.
- Search and onboarding flows. Module 0 is the orientation; 24 sub-concepts fit on one screen.

---

## 2. Reference: the wordbank app

`../wordbank/app/Apple/` is the pattern being followed:

- Native SwiftUI, chosen over a WKWebView wrapper for offline use, native feel, and App Store review.
- A logic package (`WordbankKit`) and a UI package (`WordbankUI`) with a thin app target.
- Bundled-content option documented in `APPLE_APP_PLAN.md` as the zero-hosting starting point.

Deliberately **not** carried over: the two-theme system (`playful` / `scholarly`), `Localization.swift` and `Loc()`, `RewardConfetti`, and `SoundPlayer`. Dropping these removes a large amount of surface area.

---

## 3. Architecture

Three layers.

### 3.1 `Break250Kit` — logic, no UI, fully unit-testable

| Component | Responsibility |
|---|---|
| `CSVParser` | RFC-4180 parsing with quoted multi-line cells. Adapted from `WordbankKit/CSV.swift`. Required: the `mini_lesson` column contains embedded newlines and commas. |
| `Lesson`, `Quiz`, `Choice`, `Category`, `SubConcept` | Models mirroring the locked schemas in `docs/csv_schemas.md` v1.1. |
| `ContentRepository` (protocol) | Content access boundary. v1 implementation: `BundledContentRepository`. A `RemoteContentRepository` can be added later without touching views. |
| `Catalog` | The 24 entries (2 Orientation + 22 graded) grouped into Orientation / A · Literary / B · Informational / C · Vocabulary. Defined explicitly in Swift, ported from `CATALOG` in `src/main.js`, so ordering is intentional rather than filesystem-derived. Each entry carries `module`, `basename`, `title`, `category`, `subId` — the same fields as the web catalog. |
| `ProgressStore` | Per-sub-concept `lastScore`, `bestScore`, `attempts`, `lastAttemptedAt`, `contentHash`; plus missed-question records. Versioned JSON in Application Support. |
| `QuizSession` | State machine for one 10-question run: select → submit → reveal feedback → next → score. |
| `ReviewQueue` | Missed questions across all sub-concepts. Deduped by `quiz_id`; an entry is removed when the student later answers it correctly. |
| `StatusBand` | 9–10 Mastered / 7–8 Good / 5–6 Review / 0–4 Needs Practice, plus the Module 0 "Orientation Complete" case. |

### 3.2 `Break250UI` — presentation only

- A single `Theme` (academic): `ColorPalette`, `TypographyScale`, `SpacingScale`, `CornerRadiusScale`. Same file layout as `WordbankUI/Theme/` for familiarity, minus the theme-variant machinery.
- No emoji, no sound. Haptics retained — a light tap on submit is useful feedback on a phone.
- Components: `ChoiceButton`, `FeedbackPanel`, `StatusChip`, `QuizProgressBar`, `CategoryHeader`, `LoadingState`, `ErrorState`.

### 3.3 `Break250` app target

`AppModel` (load state, injected repository and stores) plus SwiftUI views. Thin by design.

### 3.4 Project layout and toolchain

The Apple app lives in this repository under `app/Apple/`, matching wordbank's layout:

```
app/Apple/
  Break250Kit/          Swift package (logic + UI packages as two targets)
  Break250/             Xcode app project
  Break250/Content/     synced copy of content/lessons + content/quizzes
```

Minimum deployment target **iOS 17** — it gives current SwiftUI navigation and `@Observable` without excluding devices this audience plausibly uses. Universal iPhone + iPad, portrait and landscape. Swift package targets build and test from the command line (`swift test`), which is what keeps the logic tests fast and CI-friendly; the Xcode project is needed only for building and shipping the app itself.

---

## 4. Screens

`NavigationSplitView` shell: a persistent sidebar on iPad, collapsing to a navigation stack on iPhone. Five sidebar sections — **Learn**, **Review**, **Quick Reference**, **Progress**, **About**. Lesson, Quiz, and Score are pushed destinations rather than sidebar entries.

**Learn (home).** Four category sections listing their sub-concepts, each with a status chip. Per-category roll-up line ("5/9 attempted · 2 Mastered"). The website's home page, natively.

**Lesson.** Pushed from a sub-concept. The `mini_lesson` markdown rendered natively: paragraphs, bold, italic, blockquotes, bullet lists, definition lists, and **tables** (Module 0 requires tables — this was a real bug on the web side). Quick-reference card at top, worked-example cards, numbered trap callouts. Primary action: **Start 10 quizzes**.

**Quiz.** One question per screen. Prompt, four `ChoiceButton`s, Submit. On submit: correct/incorrect coloring, then the per-choice feedback panel — the picked choice's feedback always, plus the correct choice's feedback when wrong. Progress bar ("3 of 10"). Next advances.

**Score.** Band and blurb; best score and attempt count on retakes; missed questions surfaced as "3 questions added to Review". Module 0 shows "Orientation Complete" and never a score.

**Review.** Every missed question, grouped by category, with a "Practice N questions" button that runs them through the same quiz screen. Answering correctly removes the entry. Empty state: "Nothing to review — miss a question and it lands here."

Module 0 questions **do** enter the review queue when missed. Module 0 is exempt from *scoring*, not from practice, and its recognition questions ("which tool does this question test?") are worth re-answering. A review session mixing Module 0 and graded questions reports only how many were answered correctly out of how many attempted — it never assigns a status band, because a review session is not an attempt at any one sub-concept and must not overwrite `lastScore`.

**Quick Reference.** All 24 `quick_ref` lines grouped by category, each tappable through to its lesson.

**Progress.** Per-category counts and a list of what is not yet mastered. Deliberately modest.

**About.** The text from `about.md`, plus version and a link to the website.

---

## 5. Data flow

**Startup.** `AppModel.load()` → `BundledContentRepository` reads the catalog; individual lessons and quiz packs are parsed on first open and memoized. The catalog is Swift code, so Learn renders with no cold-start loading state.

**Content in the bundle.** The app's `Content/` directory is a verbatim copy of the website's `content/lessons/` and `content/quizzes/` — same CSV files, same paths, no transformation. A sync script (`scripts/sync_app_content.py`) copies them and writes `content_version.json` containing a version string and a per-sub-concept content hash.

Keeping CSV as the on-device format means one content source of truth across web and app. The alternative (converting to JSON at build time) was considered and rejected: it inserts a build step between content and app, creating drift risk if it is not re-run.

**Progress persistence.** Versioned JSON (`{ version: 1, subConcepts: [...], missed: [...] }`) in Application Support, written after each completed quiz. Schema shape mirrors the website's localStorage so a future export/import between surfaces remains possible. No iCloud sync in v1: no account, no PII, and an App Store privacy label of "no data collected".

---

## 6. Content updates after SME review

The website's quizzes will be revised following SME review. Because v1 bundles content, revisions reach app users through App Store releases while web users get them on push. The design must ensure updates never corrupt progress.

**Rules:**

1. **`quiz_id` is the stable contract.** Already true in the CSVs (`b4-1_q01`). Made explicit as a content-authoring rule: revising a question's wording, choices, or feedback keeps its ID; a deleted question's ID is retired permanently and never reused. Progress and review records key off `quiz_id`, never off position or index.

2. **Loading tolerates drift.** The review queue filters stored IDs against the corpus actually present at read time. Dangling IDs are skipped silently. A revised question simply appears with its new text. Ordinary content edits therefore need no migration.

3. **Scores are kept and flagged, never reset.** Each progress record stores the content hash of the quiz pack it was earned against — the hash covers that sub-concept's quiz CSV only, so editing a lesson's prose does not flag its score. When the current hash differs, the UI shows the score with a quiet "content updated since your last attempt" note. A 9/10 earned against superseded questions is preserved but not silently presented as current mastery.

4. **New sub-concepts** added in later content waves (B3, B6, A3, B5) appear in the catalog as Not Started.

**Upgrade path.** If revisions prove frequent enough that App Store releases become a bottleneck, the fix is a `RemoteContentRepository` fetching a manifest from the existing GitHub Pages site with the bundled content as fallback. `ContentRepository` is a protocol from day one specifically to make this a drop-in change.

---

## 7. Error handling

Three real failure modes, all local:

| Failure | Behavior |
|---|---|
| A CSV fails to parse | Contained to the affected sub-concept: an `ErrorState` view on that screen. The rest of the app keeps working. Mirrors the Quick Reference page's per-lesson error tolerance on the web. |
| A file is missing from the bundle | Same as above; the sub-concept shows as unavailable rather than crashing. |
| Progress JSON is corrupt | Backed up aside and reset, rather than crashing on launch. |

Content integrity is enforced in **tests, not at runtime** — a bad content sync must fail CI, not reach a student.

---

## 8. Testing

`Break250Kit` unit tests, no simulator required:

- CSV parsing: quoted multi-line cells, embedded commas, and the column-shift class of bug that broke C1.2 on the web.
- `StatusBand` at every boundary (0, 4, 5, 6, 7, 8, 9, 10) plus the Module 0 exception.
- `QuizSession` state transitions, including submit-before-select and advancing past the last question.
- `ReviewQueue`: add, dedupe by `quiz_id`, removal on later correct answer, and filtering of dangling IDs.
- `ProgressStore`: round-trip, version handling, corrupt-file recovery, content-hash staleness flagging.

**Corpus test** (the app-side equivalent of `scripts/validate-content.py`): every bundled lesson and quiz parses; `quiz_id`s are unique; question numbers run 1–10 with no gaps; every `correct_choice` has non-empty feedback; every lesson has a non-empty `quick_ref` and `mini_lesson`.

UI tests are limited to a smoke test of the primary flow (Learn → Lesson → Quiz → Score) on both size classes.

---

## 9. Open questions

None blocking. Two decisions deferred by design:

- **Reading Lab in v2.** The annotation renderer (tap a highlight, see the note) is the natural next surface and suits touch well.
- **Remote content loading.** Deferred until update frequency justifies it (see §6).
