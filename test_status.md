# test_status.md — Test coverage and last run

**As of:** 2026-05-26
**Status:** No tests yet — no code yet.

## Test framework targets (planned)

| Layer | Framework | Notes |
|---|---|---|
| Unit (pure fns: scoring, recommend) | Vitest | Fast, TS-native |
| Component | Vitest + React Testing Library | |
| API integration | Vitest + Supertest against local Supabase | Use service-role key |
| RLS isolation | pgTAP **or** Vitest + Supabase role JWT | Must run in CI before Phase 2 |
| E2E | Playwright | Cross-browser: Chromium, Firefox, WebKit |
| A11y | axe-core via Playwright | Zero serious violations on lesson player, dashboard, diagnostic |
| Performance | Lighthouse CI | CWV targets from `~/.claude/rules/web/performance.md` |

## Coverage target

- 80% line coverage on `src/lib/**` (pure logic — scoring, recommendation, validators)
- 80% line coverage on `src/app/api/**` (route handlers)
- UI components covered primarily by component + E2E tests; line coverage is secondary signal

## Last run

n/a — no CI yet.

## Open test debts

(Empty — tracked here as phases progress.)

## Critical test gates by phase

| Gate | Required before starting |
|---|---|
| Schema migration idempotency tests pass | Phase 2 |
| RLS role-isolation tests pass | Phase 2 |
| `computeMastery()` golden-case tests pass | Phase 4 |
| `recommendNextLesson()` fallback test passes | Pilot |
| E2E full-lesson happy path passes on mobile viewport | Phase 6 |
| Axe-core zero serious violations | Pilot |
