# review.md — Architect notes for next reviewer

> If you are the next reviewer (or a GPT review pass via `gpt_review.md`), start here. These are the open architectural questions and the reasoning behind the current plan, written so a reviewer can challenge the plan rather than rederive it.

---

## 1. Stack choice — challenge me

**Proposed:** Next.js (App Router) + TypeScript + Tailwind + Supabase (Postgres + Auth + Storage) + Vercel.

**Why:**
- Design doc §20 already favors this lane.
- Single language (TS) end-to-end keeps the agent-context window small per task.
- Supabase removes ~80% of auth + DB boilerplate that would otherwise dominate Phase 0–1.
- RLS in Postgres aligns with the multi-role model (student/parent/teacher/admin).
- Vercel preview deploys give parents and pilot users a low-friction URL.

**Honest counter-arguments:**
- **Supabase lock-in.** RLS-heavy apps are hard to migrate off. If we expect ML-heavy scoring later, a more typical Postgres + custom API may be cleaner.
- **Next.js for an admin-heavy app is awkward.** Phase 5 admin CRUD could be better served by something like Refine or Retool, not bespoke React.
- **Mobile-first close reading might pressure us toward a native shell sooner than the design admits.** Design §20.2 says "build web first, wrap later"; but pilot UX on iOS Safari can be rough for long-form reading with highlighting gestures.

**Decision needed:** confirm stack, or propose alternative with one-line rationale. Recorded in `context.md` once locked.

---

## 2. Mastery score formula in MVP

**Design §10.4:** `0.5·accuracy + 0.3·evidence + 0.2·explanation`.

**Architect concern (see `feedback.md` H-2):** MVP has no explanation scorer. Either manual at pilot scale (expensive, slow feedback to student) or AI-assisted (out of scope for MVP per §15.2).

**Proposal:** for MVP, use `0.65·accuracy + 0.35·evidence`. Reweight to design §10.4 when explanation scoring lands.

**Risk:** mastery numbers will read differently in MVP vs post-MVP. Document the shift, do not retroactively rescore historical attempts.

**Decision needed:** confirm reweight or commit to manual explanation scoring with a named owner.

---

## 3. Content authoring is the long pole — who writes it?

12 lessons × ~8 questions × 4 choices × wrong-answer-type tag × evidence keys × feedback ≈ **300+ carefully written pieces of pedagogy**. Each needs to be MAP-style, age-appropriate, and use one of the locked wrong-answer-type values.

**Engineering can finish Phases 0–4 without all content** (3 sample lessons unblock the player; 12 are needed for diagnostic + recommend + pilot).

**Decision needed:** name the content owner. Without one, Phase 4+ will block.

---

## 4. Evidence model — text spans vs segment IDs

**See `feedback.md` H-1.** Design has both shapes. Options:

- **A. Segment-only (paragraph or sentence ID):** simpler UI, cheap scoring, lower fidelity ("the right paragraph but not the right phrase").
- **B. Text-span (character offsets):** higher fidelity, harder UI on mobile, more brittle (passage edits invalidate stored offsets).
- **C. Both (segment-required, span-optional bonus):** more code, but matches design's "exact words prove your answer" intent.

**Architect lean:** C — start with segment-required + collect span-optional. Score on segment in MVP; add span scoring once mobile UX is proven.

**Decision needed:** confirm C or pick A/B.

---

## 5. Diagnostic question count and coverage gap

Design §7.2 lists 10 skill categories × 2 questions = 20. But module list §5.2 has 12 modules. Missing from diagnostic mix: **Word Choice**, **Theme** (or similar — depends how you map). 

**Decision needed:** reconcile to either 12 modules × 2 = 24 (preferred) or accept that diagnostic samples 10 of 12 skills.

---

## 6. Privacy / parent consent flow

This is for minors. Several jurisdictions (COPPA in US, GDPR-K in EU, PIPEDA in Canada, PDPA variants in APAC) require parental consent **before** a child plays.

**Current design (§22):** vague. Says "optional parent email" — that's not how COPPA works for under-13.

**Decision needed:**
- Target user age range. Grade 5–8 spans 10–14 — about half is under 13.
- If we target sub-13 students at all: implement parental-consent-first flow (email verification gate before student account becomes active). If we restrict to 13+: explicit minimum-age gate at signup.

This is **not** an engineering judgment call — needs product/legal input.

---

## 7. Things explicitly left to a later review

- **Adaptive difficulty.** Out of scope for MVP per design §29.3. Don't build escape hatches for it in MVP schema beyond an integer `difficulty` field on questions.
- **AI close-reading coach.** Design §28.1. Schema should not preempt it; recommendation engine should not preempt it; do not add a `coach_session` table in MVP.
- **Teacher mode.** Design §28.3. P5-4 in tracker but flagged as may-defer.
- **Text upload feature.** Design §28.2. Privacy + copyright minefield. Post-MVP.

---

## Open questions for next reviewer (please answer or push back)

1. **Stack:** confirm Next.js + Supabase? Y / N / propose alternative.
2. **Mastery formula MVP:** drop explanation weight to 0? Y / N.
3. **Content owner:** who writes the 12 MVP lessons?
4. **Evidence model:** A / B / C (see §4)?
5. **Diagnostic coverage:** 24 questions covering all 12 modules? Y / N.
6. **Target age / consent flow:** what's the minimum age, and what's the parental-consent UX?
7. **Mobile UX risk:** is two-pass close reading on phones a Phase 2 must-prove, or can we ship desktop-first MVP?
8. **Streak gamification:** keep daily streak (rewards speed) or replace with mastery-only progression (rewards precision)?

A reviewer should write back into `gpt_review.md` (or a new `review_<reviewer>.md`) with answers and pushback. Architect will then update `context.md`, `feedback.md`, and `project_plan.md` accordingly before Phase 0 starts.
