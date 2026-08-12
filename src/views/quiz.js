// src/views/quiz.js — quiz flow for one sub-concept.
//
// Implements Phase 1 components P1-3 (MCQ), P1-4 (feedback panel),
// P1-5 (quiz flow state machine), P1-6 (score + status band).
//
// Phase 6 additions: keyboard shortcuts (1-4 to select, Enter to submit/next),
// focus management, aria-live feedback announcements.

import { loadLesson, loadQuizzes } from "../loader.js";
import { recordAttempt, getProgress } from "../progress.js";

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

/**
 * Map a 0–10 score to a status band.
 * Per curriculum_design.md status bands: 9-10 Mastered / 7-8 Good / 5-6 Review / 0-4 Needs Practice.
 *
 * @param {number} score
 * @returns {{label: string, color: "emerald"|"blue"|"amber"|"rose", blurb: string}}
 */
function statusBand(score) {
  if (score >= 9) {
    return {
      label: "Mastered",
      color: "emerald",
      blurb: "Excellent — you can name and use this tool. Pick another sub-concept next.",
    };
  }
  if (score >= 7) {
    return {
      label: "Good",
      color: "blue",
      blurb: "Solid grasp. One more pass through this sub-concept will lock it in.",
    };
  }
  if (score >= 5) {
    return {
      label: "Review",
      color: "amber",
      blurb: "On the way. Reread the mini-lesson and try the quizzes again — pay extra attention to the per-choice feedback for each wrong answer.",
    };
  }
  return {
    label: "Needs Practice",
    color: "rose",
    blurb: "Worth working through the mini-lesson again before retrying. Read the per-choice feedback for every wrong answer — that's where the teaching happens.",
  };
}

const BAND_CLASSES = {
  emerald: "border-emerald-300 bg-emerald-50 text-emerald-900",
  blue:    "border-blue-300 bg-blue-50 text-blue-900",
  amber:   "border-amber-300 bg-amber-50 text-amber-900",
  rose:    "border-rose-300 bg-rose-50 text-rose-900",
};

/**
 * Render the quiz flow into a target element.
 *
 * @param {HTMLElement} target
 * @param {string} moduleId
 * @param {string} fileBasename
 */
export async function renderQuizPage(target, moduleId, fileBasename, next = null) {
  target.innerHTML = `<div class="text-slate-500 text-sm">Loading quizzes…</div>`;

  let lesson, quizzes;
  try {
    [lesson, quizzes] = await Promise.all([
      loadLesson(moduleId, fileBasename),
      loadQuizzes(moduleId, fileBasename),
    ]);
  } catch (err) {
    target.innerHTML = `
      <div class="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">
        Failed to load quiz: ${escapeHtml(err.message)}
      </div>
      <a href="#/" class="mt-4 inline-block text-sm text-slate-700 underline">← Back home</a>
    `;
    return;
  }

  const isModule0 = moduleId === "m0";

  // In-memory session state. Phase 3 persists final score; Phase 6 could add per-question save.
  const session = {
    answers:   new Array(quizzes.length).fill(null),   // "A"/"B"/"C"/"D"
    submitted: new Array(quizzes.length).fill(false),
    currentIndex: 0,
  };

  const LETTERS = ["A", "B", "C", "D"];
  let keyHandler = null;

  function renderQuestion() {
    const idx = session.currentIndex;
    const q = quizzes[idx];
    const selected = session.answers[idx];
    const submitted = session.submitted[idx];

    const choicesHtml = LETTERS.map((letter) => {
      const lower = letter.toLowerCase();
      const text = q.choices[lower];
      const isSelected = selected === letter;
      let cls = "block w-full text-left rounded-md border px-4 py-3 text-sm transition focus:outline-none focus:ring-2 focus:ring-slate-400";

      if (submitted) {
        const isCorrect = letter === q.correctChoice;
        if (isCorrect) {
          cls += " border-emerald-400 bg-emerald-50 text-emerald-900";
        } else if (isSelected) {
          cls += " border-rose-400 bg-rose-50 text-rose-900";
        } else {
          cls += " border-slate-200 bg-slate-50 text-slate-600";
        }
      } else if (isSelected) {
        cls += " border-slate-900 bg-slate-100 text-slate-900";
      } else {
        cls += " border-slate-200 bg-white hover:border-slate-400 cursor-pointer";
      }

      const ariaPressed = submitted ? "" : `aria-pressed="${isSelected}"`;

      return `
        <button class="${cls}" data-letter="${letter}" ${ariaPressed} ${submitted ? "disabled" : ""}>
          <span class="inline-block w-6 font-semibold">${letter}.</span>
          ${escapeHtml(text)}
        </button>
      `;
    }).join("");

    const trapLabel = q.trapType && q.trapType !== "N/A" ? `<span class="ml-2 text-slate-400">· ${escapeHtml(q.trapType)}</span>` : "";

    let feedbackHtml = "";
    if (submitted) {
      const isCorrect = selected === q.correctChoice;
      const selectedLower = selected.toLowerCase();
      const correctLower = q.correctChoice.toLowerCase();

      const headerCls = isCorrect ? "border-emerald-300 bg-emerald-50" : "border-amber-300 bg-amber-50";
      const headerTextCls = isCorrect ? "text-emerald-900" : "text-amber-900";
      const headerText = isCorrect ? "✓ Correct." : `Not quite — the correct answer is ${q.correctChoice}.`;

      feedbackHtml = `
        <div id="feedback-panel" class="rounded-lg border ${headerCls} p-4 space-y-3" role="status" aria-live="polite">
          <div class="text-sm font-semibold ${headerTextCls}">${headerText}</div>
          <div class="text-sm text-slate-700">
            <div class="text-xs uppercase tracking-wide text-slate-500 mb-1">Why ${selected} is ${isCorrect ? "right" : "wrong"}</div>
            ${escapeHtml(q.feedback[selectedLower])}
          </div>
          ${!isCorrect ? `
            <div class="text-sm text-slate-700">
              <div class="text-xs uppercase tracking-wide text-slate-500 mb-1">Why ${q.correctChoice} is right</div>
              ${escapeHtml(q.feedback[correctLower])}
            </div>
          ` : ""}
        </div>
      `;
    }

    const actionHtml = submitted ? `
      <button id="next-btn" class="rounded-md bg-slate-900 text-white px-4 py-2 text-sm font-medium hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-400">
        ${idx === quizzes.length - 1 ? "See results →" : "Next →"}
      </button>
    ` : `
      <button id="submit-btn"
        class="rounded-md bg-slate-900 text-white px-4 py-2 text-sm font-medium ${selected ? "hover:bg-slate-700" : "opacity-40 cursor-not-allowed"} focus:outline-none focus:ring-2 focus:ring-slate-400"
        ${selected ? "" : "disabled"}>
        Submit
      </button>
    `;

    target.innerHTML = `
      <article class="space-y-6">
        <header class="space-y-1">
          <div class="text-xs uppercase tracking-wide text-slate-500">
            ${escapeHtml(lesson.moduleId)} · ${escapeHtml(lesson.subConceptId)} — ${escapeHtml(lesson.title)}
          </div>
          <div class="flex items-center justify-between">
            <div class="text-sm text-slate-600">Question ${idx + 1} of ${quizzes.length}${trapLabel}</div>
            <div class="text-xs text-slate-400">${escapeHtml(q.difficulty)}</div>
          </div>
          <div class="h-1.5 bg-slate-100 rounded-full overflow-hidden mt-2" role="progressbar" aria-valuemin="0" aria-valuemax="${quizzes.length}" aria-valuenow="${idx + 1}">
            <div class="h-full bg-slate-700 transition-all" style="width: ${((idx + 1) / quizzes.length) * 100}%"></div>
          </div>
        </header>

        <div id="prompt-block" class="rounded-lg border border-slate-200 bg-white p-4" tabindex="-1">
          <p class="text-slate-800 whitespace-pre-line">${escapeHtml(q.prompt)}</p>
        </div>

        <div class="space-y-2" role="radiogroup" aria-label="Answer choices">
          ${choicesHtml}
        </div>

        ${feedbackHtml}

        <div class="flex justify-between items-center pt-2">
          <a href="#/learn/${escapeHtml(moduleId)}/${escapeHtml(fileBasename)}" class="text-sm text-slate-700 underline">← Back to lesson</a>
          ${actionHtml}
        </div>

        <div class="text-xs text-slate-400 text-center pt-2">
          Keyboard: <kbd class="font-mono">1</kbd>–<kbd class="font-mono">4</kbd> to select · <kbd class="font-mono">Enter</kbd> to ${submitted ? "advance" : "submit"}
        </div>
      </article>
    `;

    wireHandlers();
    // Focus the prompt block on new question for screen readers (programmatic focus
    // via tabindex="-1"). Skip on initial mount to avoid stealing focus from the URL bar.
    if (idx > 0 && !submitted) {
      const promptBlock = target.querySelector("#prompt-block");
      if (promptBlock) promptBlock.focus({ preventScroll: false });
    }
  }

  function wireHandlers() {
    const idx = session.currentIndex;
    const submitted = session.submitted[idx];

    // Remove previous global key handler (if any) before attaching new one
    if (keyHandler) document.removeEventListener("keydown", keyHandler);

    keyHandler = (e) => {
      // Ignore if user is typing in an input/textarea
      const tag = e.target?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;

      if (!submitted) {
        // 1-4 selects A-D
        if (e.key >= "1" && e.key <= "4") {
          const letter = LETTERS[Number(e.key) - 1];
          session.answers[idx] = letter;
          renderQuestion();
          e.preventDefault();
          return;
        }
        // Enter submits if a choice is selected
        if (e.key === "Enter" && session.answers[idx]) {
          session.submitted[idx] = true;
          renderQuestion();
          e.preventDefault();
          return;
        }
      } else {
        // Enter advances
        if (e.key === "Enter") {
          if (session.currentIndex < quizzes.length - 1) {
            session.currentIndex++;
            renderQuestion();
          } else {
            renderEndScreen();
          }
          e.preventDefault();
        }
      }
    };
    document.addEventListener("keydown", keyHandler);

    if (!submitted) {
      target.querySelectorAll("button[data-letter]").forEach((btn) => {
        btn.addEventListener("click", () => {
          session.answers[idx] = btn.dataset.letter;
          renderQuestion();
        });
      });
      const submitBtn = target.querySelector("#submit-btn");
      if (submitBtn) {
        submitBtn.addEventListener("click", () => {
          if (session.answers[idx]) {
            session.submitted[idx] = true;
            renderQuestion();
          }
        });
      }
    } else {
      const nextBtn = target.querySelector("#next-btn");
      if (nextBtn) {
        nextBtn.addEventListener("click", () => {
          if (session.currentIndex < quizzes.length - 1) {
            session.currentIndex++;
            renderQuestion();
          } else {
            renderEndScreen();
          }
        });
      }
    }
  }

  function renderEndScreen() {
    if (keyHandler) document.removeEventListener("keydown", keyHandler);

    const correctCount = session.answers.filter((ans, i) => ans === quizzes[i].correctChoice).length;
    // Persist the attempt before rendering — Phase 3 progress tracking.
    recordAttempt(moduleId, fileBasename, correctCount, quizzes.length);
    const prior = getProgress(moduleId, fileBasename);

    if (isModule0) {
      target.innerHTML = `
        <article class="space-y-6">
          <header>
            <div class="text-xs uppercase tracking-wide text-slate-500">${escapeHtml(lesson.moduleId)} — ${escapeHtml(lesson.title)}</div>
            <h1 class="text-2xl font-semibold tracking-tight mt-1">Orientation Complete</h1>
            <p class="mt-2 text-slate-600">
              You've completed Module 0. The recognition quizzes train you to identify which tool a question is testing —
              now you can dive into individual sub-concepts with the map in hand.
            </p>
          </header>

          <div class="rounded-lg border border-emerald-300 bg-emerald-50 p-4 text-sm text-emerald-900" role="status">
            ✓ All 10 recognition quizzes attempted. Module 0 is intentionally <strong>not scored</strong> — it's orientation, not mastery.
          </div>

          <div class="flex flex-wrap gap-2 pt-2">
            <a href="#/learn/${escapeHtml(moduleId)}/${escapeHtml(fileBasename)}" class="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium hover:border-slate-500">Reread orientation</a>
            <a href="#/" class="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium hover:border-slate-500">Home</a>
            ${next
              ? `<a href="#/learn/${escapeHtml(next.module)}/${escapeHtml(next.basename)}" class="ml-auto rounded-md bg-slate-900 text-white px-4 py-2 text-sm font-medium hover:bg-slate-700">Next: ${escapeHtml(next.title)} →</a>`
              : `<a href="#/" class="ml-auto rounded-md bg-slate-900 text-white px-4 py-2 text-sm font-medium hover:bg-slate-700">Done →</a>`}
          </div>
        </article>
      `;
      return;
    }

    const band = statusBand(correctCount);

    target.innerHTML = `
      <article class="space-y-6">
        <header>
          <div class="text-xs uppercase tracking-wide text-slate-500">${escapeHtml(lesson.moduleId)} · ${escapeHtml(lesson.subConceptId)} — ${escapeHtml(lesson.title)}</div>
          <h1 class="text-2xl font-semibold tracking-tight mt-1">Quiz Complete</h1>
        </header>

        <div class="rounded-lg border ${BAND_CLASSES[band.color]} p-6 text-center space-y-2" role="status">
          <div class="text-4xl font-bold">${correctCount} <span class="text-slate-400 text-2xl">/ ${quizzes.length}</span></div>
          <div class="text-lg font-medium">${band.label}</div>
          ${prior && prior.attempts > 1 ? `<div class="text-xs text-slate-600">Best: ${prior.bestScore}/${quizzes.length} · Attempts: ${prior.attempts}</div>` : ""}
        </div>

        <div class="text-sm text-slate-600">${band.blurb}</div>

        <div class="flex flex-wrap gap-2 pt-2">
          <a href="#/learn/${escapeHtml(moduleId)}/${escapeHtml(fileBasename)}" class="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium hover:border-slate-500">Back to lesson</a>
          <a href="#/" class="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium hover:border-slate-500">Home</a>
          ${next
            ? `<a href="#/learn/${escapeHtml(next.module)}/${escapeHtml(next.basename)}" class="ml-auto rounded-md bg-slate-900 text-white px-4 py-2 text-sm font-medium hover:bg-slate-700">Next: ${escapeHtml(next.title)} →</a>`
            : `<a href="#/" class="ml-auto rounded-md bg-slate-900 text-white px-4 py-2 text-sm font-medium hover:bg-slate-700">Done →</a>`}
        </div>
      </article>
    `;
  }

  renderQuestion();
}
