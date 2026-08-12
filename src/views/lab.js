// src/views/lab.js — Reading Lab text detail page.
//
// Renders a public-domain passage with color-coded annotation ranges.
// Click any annotated range to see its note. Toggle markup on/off.

import { loadLabText } from "../loader.js";
import { COLOR_TO_CODE, MARKING_ITEMS } from "./marking-guide.js";

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

const CATEGORY_LABEL = {
  tone:      "How it feels: Tone & Word Choice",
  evidence:  "How to prove it: Evidence",
  theme:     "What it says: Theme / Central Idea",
  inference: "What it suggests: Inference Clues",
  structure: "How it's built: Structure / Function",
};

// Tailwind class strings per category. Background + a darker text on hover/active.
const CATEGORY_CLASS = {
  tone:      "bg-amber-200 hover:bg-amber-300 text-amber-950",
  evidence:  "bg-emerald-200 hover:bg-emerald-300 text-emerald-950",
  theme:     "bg-sky-200 hover:bg-sky-300 text-sky-950",
  inference: "bg-violet-200 hover:bg-violet-300 text-violet-950",
  structure: "bg-orange-200 hover:bg-orange-300 text-orange-950",
};

const CATEGORY_DOT = {
  tone:      "bg-amber-400",
  evidence:  "bg-emerald-400",
  theme:     "bg-sky-400",
  inference: "bg-violet-400",
  structure: "bg-orange-400",
};

const DIFFICULTY_CLASS = {
  Easy:   "bg-emerald-100 text-emerald-800 border-emerald-200",
  Medium: "bg-amber-100 text-amber-800 border-amber-200",
  Hard:   "bg-rose-100 text-rose-800 border-rose-200",
};

/**
 * Split a passage into segments by every annotation start/end boundary.
 * Each segment is either un-annotated or has one+ annotation indices applicable.
 *
 * @param {string} passage
 * @param {Array} annotations
 * @returns {Array<{text: string, annIndices: number[]}>}
 */
function buildSegments(passage, annotations) {
  if (annotations.length === 0) {
    return [{ text: passage, annIndices: [] }];
  }
  const points = new Set([0, passage.length]);
  for (const ann of annotations) {
    points.add(ann.start);
    points.add(ann.end);
  }
  const sorted = [...points].sort((a, b) => a - b);
  const segments = [];
  for (let i = 0; i < sorted.length - 1; i++) {
    const start = sorted[i];
    const end = sorted[i + 1];
    if (start === end) continue;
    const text = passage.substring(start, end);
    const annIndices = [];
    annotations.forEach((ann, idx) => {
      if (ann.start <= start && ann.end >= end) annIndices.push(idx);
    });
    segments.push({ text, annIndices });
  }
  return segments;
}

/**
 * Render the Reading Lab text detail page.
 *
 * @param {HTMLElement} target
 * @param {string} basename
 */
export async function renderLabPage(target, basename) {
  target.innerHTML = `<div class="text-slate-500 text-sm">Loading…</div>`;

  let lab;
  try {
    lab = await loadLabText(basename);
  } catch (err) {
    target.innerHTML = `
      <div class="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">
        Failed to load text: ${escapeHtml(err.message)}
      </div>
      <a href="#/" class="mt-4 inline-block text-sm text-slate-700 underline">← Back home</a>
    `;
    return;
  }

  // UI state — markup visibility toggle.
  let showMarkup = true;
  let selectedAnnIdx = null;

  function render() {
    const segments = buildSegments(lab.passage, lab.annotations);
    const passageHtml = segments
      .map((seg, segIdx) => {
        // Preserve newlines via CSS (whitespace: pre-wrap on parent).
        const safe = escapeHtml(seg.text);
        if (!showMarkup || seg.annIndices.length === 0) {
          return safe;
        }
        // Use the first annotation's category for the visual color when multiple overlap.
        const primary = lab.annotations[seg.annIndices[0]];
        const cls = CATEGORY_CLASS[primary.category];
        const labels = seg.annIndices.map((i) => CATEGORY_LABEL[lab.annotations[i].category]).join(", ");
        const isSelected = selectedAnnIdx === seg.annIndices[0];
        const ring = isSelected ? "ring-2 ring-slate-600" : "";
        // Inline span (not <button>) so highlights flow with the text and wrap per line —
        // critical for verse, where a multi-line annotation must break across lines cleanly.
        return `<span role="button" tabindex="0" data-ann-idx="${seg.annIndices[0]}" class="${cls} ${ring} rounded cursor-pointer transition focus:outline-none focus:ring-2 focus:ring-slate-600" aria-label="${escapeHtml(labels)}">${safe}</span>`;
      })
      .join("");

    const legend = Object.entries(CATEGORY_LABEL)
      .map(
        ([key, label]) => `
        <span class="inline-flex items-center gap-1.5 text-xs">
          <span class="inline-block w-3 h-3 rounded-sm ${CATEGORY_DOT[key]}"></span>
          ${escapeHtml(label)}
          <span class="font-mono text-[10px] text-slate-500">(${escapeHtml(COLOR_TO_CODE[key] || "?")})</span>
        </span>
      `,
      )
      .join("");

    const notesPanel = (() => {
      if (selectedAnnIdx === null) {
        return `
          <div class="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-500 text-center">
            Click any highlighted phrase above to see why it's marked.
          </div>
        `;
      }
      const ann = lab.annotations[selectedAnnIdx];
      const dot = CATEGORY_DOT[ann.category];
      const code = COLOR_TO_CODE[ann.category] || "?";
      const codeItem = MARKING_ITEMS.find((it) => it.code === code);
      const codeBadge = `
        <a href="#/marking" class="inline-flex items-center gap-1 ml-2 font-mono text-xs font-semibold bg-slate-100 border border-slate-200 rounded px-2 py-0.5 text-slate-700 hover:bg-slate-200 transition" title="${escapeHtml(codeItem ? codeItem.name + " — see Marking Guide" : "see Marking Guide")}">${escapeHtml(code)}</a>
      `;
      return `
        <div class="rounded-lg border border-slate-200 bg-white p-4 space-y-2" role="status" aria-live="polite">
          <div class="flex items-center gap-2 text-xs uppercase tracking-wide">
            <span class="inline-block w-3 h-3 rounded-sm ${dot}"></span>
            <span class="text-slate-600">${escapeHtml(CATEGORY_LABEL[ann.category])}</span>
            ${codeBadge}
          </div>
          <div class="text-sm text-slate-700">${escapeHtml(ann.note)}</div>
        </div>
      `;
    })();

    const promptsHtml = lab.discussionPrompts.length
      ? `
        <section class="space-y-2">
          <div class="flex items-baseline justify-between">
            <h2 class="text-sm uppercase tracking-wide text-slate-500">Discussion prompts</h2>
            ${lab.discussionAnswers.length === lab.discussionPrompts.length
              ? `<span class="text-xs text-slate-500">Click any prompt to reveal a sample answer.</span>`
              : ""}
          </div>
          <ol class="list-decimal list-outside ml-5 space-y-2 text-sm text-slate-700">
            ${lab.discussionPrompts.map((p, i) => {
              const ans = lab.discussionAnswers[i];
              if (!ans) {
                return `<li>${escapeHtml(p)}</li>`;
              }
              return `
                <li>
                  <details class="group">
                    <summary class="cursor-pointer list-none -ml-1 pl-1 rounded hover:bg-slate-50 transition">
                      <span class="inline-flex items-baseline gap-1">
                        <span>${escapeHtml(p)}</span>
                        <span class="text-xs text-slate-400 group-open:hidden">▾ answer</span>
                        <span class="text-xs text-slate-400 hidden group-open:inline">▴ hide</span>
                      </span>
                    </summary>
                    <div class="mt-1.5 ml-1 pl-3 border-l-2 border-slate-200 text-slate-600 text-sm">
                      ${escapeHtml(ans)}
                    </div>
                  </details>
                </li>
              `;
            }).join("")}
          </ol>
        </section>
      `
      : "";

    const sourceLink = lab.sourceUrl
      ? `<a href="${escapeHtml(lab.sourceUrl)}" target="_blank" rel="noopener noreferrer" class="text-xs text-slate-500 underline hover:text-slate-700">source</a>`
      : "";

    target.innerHTML = `
      <article class="space-y-6">
        <header class="space-y-1">
          <div class="flex items-center gap-2 text-xs uppercase tracking-wide text-slate-500">
            <span>Reading Lab · ${escapeHtml(lab.category)}</span>
            ${lab.difficulty ? `<span class="inline-block border rounded-full px-1.5 py-0.5 text-[10px] normal-case tracking-normal ${DIFFICULTY_CLASS[lab.difficulty] || ""}">${escapeHtml(lab.difficulty)}</span>` : ""}
          </div>
          <h1 class="text-2xl font-semibold tracking-tight">${escapeHtml(lab.title)}</h1>
          <div class="text-sm text-slate-600">
            ${escapeHtml(lab.author)} · ${escapeHtml(String(lab.year))} · ${lab.lengthWords ? `${lab.lengthWords} words` : ""}
            ${sourceLink ? `· ${sourceLink}` : ""}
          </div>
        </header>

        <div class="rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900">
          ${escapeHtml(lab.intro)}
        </div>

        <div class="sticky top-0 z-10 -mx-4 px-4 py-3 bg-slate-50 border-y border-slate-200">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div class="flex flex-wrap items-center gap-3">${legend}</div>
            <button id="toggle-markup" class="text-xs rounded border border-slate-300 px-3 py-1 hover:border-slate-500 bg-white">
              ${showMarkup ? "Hide markup" : "Show markup"}
            </button>
          </div>
        </div>

        <div class="rounded-lg border border-slate-200 bg-white p-5 leading-relaxed whitespace-pre-wrap text-slate-800 font-serif text-base"
          >${passageHtml}</div>

        ${notesPanel}

        ${promptsHtml}

        <footer class="pt-4 border-t border-slate-200 text-sm">
          <a href="#/" class="text-slate-700 underline">← Back home</a>
        </footer>
      </article>
    `;

    // Wire up annotation handlers (spans with role=button → click + keyboard).
    target.querySelectorAll("[data-ann-idx]").forEach((el) => {
      const activate = () => {
        selectedAnnIdx = Number(el.dataset.annIdx);
        render();
      };
      el.addEventListener("click", activate);
      el.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          activate();
        }
      });
    });

    // Toggle button
    const toggle = target.querySelector("#toggle-markup");
    if (toggle) {
      toggle.addEventListener("click", () => {
        showMarkup = !showMarkup;
        selectedAnnIdx = null;
        render();
      });
    }
  }

  render();
}
