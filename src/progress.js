// src/progress.js — localStorage progress tracker.
//
// Stores per-sub-concept best score, last score, attempts, last attempted timestamp.
// Single root key `break250.progress.v1` holds a map keyed by `{module}/{basename}`.
//
// Status bands (per docs/curriculum_design.md):
//   Module 0: "Orientation Complete" or "Not Started" — never a score.
//   Modules 1+: 9-10 Strong on this set · 7-8 Getting there · 5-6 Review this one · 0-4 Needs practice.
//   Deliberately not "Mastered": these are fixed 10-question sets, so a high
//   score shows strength on THIS set, not proven transfer to an unseen passage.

const STORAGE_KEY = "break250.progress.v1";

/**
 * @typedef {object} SubConceptProgress
 * @property {number} lastScore
 * @property {number} bestScore
 * @property {number} attempts
 * @property {string} lastAttemptedAt  ISO 8601
 *
 * @typedef {object} ProgressRoot
 * @property {number} version
 * @property {Record<string, SubConceptProgress>} subConcepts
 */

/** @returns {ProgressRoot} */
function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { version: 1, subConcepts: {} };
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed === "object" && parsed.version === 1 && parsed.subConcepts) {
      return parsed;
    }
  } catch {
    // fall through to default
  }
  return { version: 1, subConcepts: {} };
}

/** @param {ProgressRoot} root */
function save(root) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(root));
  } catch {
    // storage may be disabled (private mode, full quota). Fail silently for v0.
  }
}

function key(moduleId, fileBasename) {
  return `${moduleId}/${fileBasename}`;
}

/**
 * Record a completed quiz attempt.
 *
 * @param {string} moduleId
 * @param {string} fileBasename
 * @param {number} score        0..10
 * @param {number} total        usually 10 (Module 0 also 10)
 */
export function recordAttempt(moduleId, fileBasename, score, total) {
  const root = load();
  const k = key(moduleId, fileBasename);
  const prior = root.subConcepts[k];
  const bestScore = Math.max(score, prior?.bestScore ?? 0);
  root.subConcepts[k] = {
    lastScore: score,
    bestScore,
    attempts: (prior?.attempts ?? 0) + 1,
    lastAttemptedAt: new Date().toISOString(),
  };
  save(root);
}

/**
 * Get progress for one sub-concept, or null if never attempted.
 *
 * @param {string} moduleId
 * @param {string} fileBasename
 * @returns {SubConceptProgress | null}
 */
export function getProgress(moduleId, fileBasename) {
  const root = load();
  return root.subConcepts[key(moduleId, fileBasename)] ?? null;
}

/**
 * Erase all progress. For "Reset" button.
 */
export function resetAll() {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // ignore
  }
}

/**
 * Compute the status band for a non-Module-0 sub-concept from a score.
 *
 * @param {number} score
 * @returns {{label: string, color: "emerald"|"blue"|"amber"|"rose"}}
 */
export function statusFromScore(score) {
  if (score >= 9) return { label: "Strong on this set", color: "emerald" };
  if (score >= 7) return { label: "Getting there", color: "blue" };
  if (score >= 5) return { label: "Review this one", color: "amber" };
  return { label: "Needs practice", color: "rose" };
}

/**
 * Compute a status badge for a sub-concept link on the home page.
 *
 * @param {string} moduleId
 * @param {string} fileBasename
 * @returns {{label: string, color: "emerald"|"blue"|"amber"|"rose"|"slate", best?: number, attempts?: number}}
 */
export function statusBadge(moduleId, fileBasename) {
  const p = getProgress(moduleId, fileBasename);
  if (!p) {
    return { label: "Not Started", color: "slate" };
  }
  if (moduleId === "m0") {
    // Module 0 is completion-only — never scored.
    return { label: "Orientation Complete", color: "emerald", attempts: p.attempts };
  }
  const status = statusFromScore(p.bestScore);
  return { ...status, best: p.bestScore, attempts: p.attempts };
}
