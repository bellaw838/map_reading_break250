// src/views/library.js — Reading Library (long-form works).
//
// Three views:
//   renderLibraryIndex       → catalog of all works (#/library)
//   renderLibraryWorkPage    → book overview: intro + TOC + prompts (#/library/:basename)
//   renderLibrarySectionPage → single section with marginalia (#/library/:basename/:sectionId)

import { loadLibraryWork } from "../loader.js";

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeProseWhitespace(s) {
  return String(s)
    .replace(/\r\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .replace(/([^\n])\n([^\n])/g, "$1 $2");
}

const CATEGORY_LABEL = {
  tone:      "How it feels: Tone & Word Choice",
  evidence:  "How to prove it: Evidence",
  theme:     "What it says: Theme / Central Idea",
  inference: "What it suggests: Inference Clues",
  structure: "How it's built: Structure / Function",
};

const CATEGORY_CLASS = {
  tone:      "bg-amber-200/70 hover:bg-amber-300 text-amber-950",
  evidence:  "bg-emerald-200/70 hover:bg-emerald-300 text-emerald-950",
  theme:     "bg-sky-200/70 hover:bg-sky-300 text-sky-950",
  inference: "bg-violet-200/70 hover:bg-violet-300 text-violet-950",
  structure: "bg-orange-200/70 hover:bg-orange-300 text-orange-950",
};

const CATEGORY_DOT = {
  tone:      "bg-amber-400",
  evidence:  "bg-emerald-400",
  theme:     "bg-sky-400",
  inference: "bg-violet-400",
  structure: "bg-orange-400",
};

const CATEGORY_BORDER = {
  tone:      "border-amber-300",
  evidence:  "border-emerald-300",
  theme:     "border-sky-300",
  inference: "border-violet-300",
  structure: "border-orange-300",
};

const DIFFICULTY_CLASS = {
  Easy:   "bg-emerald-100 text-emerald-800 border-emerald-200",
  Medium: "bg-amber-100 text-amber-800 border-amber-200",
  Hard:   "bg-rose-100 text-rose-800 border-rose-200",
};

// ───────────────────────────────────────────────────────────────────────────
// Progress (last-read section per book).

function progressKey(basename) { return `library:progress:${basename}`; }

function loadProgress(basename) {
  try {
    const raw = localStorage.getItem(progressKey(basename));
    return raw ? JSON.parse(raw) : { lastSectionId: null };
  } catch {
    return { lastSectionId: null };
  }
}

function saveProgress(basename, sectionId) {
  try {
    localStorage.setItem(progressKey(basename), JSON.stringify({ lastSectionId: sectionId, updatedAt: Date.now() }));
  } catch {}
}

// ───────────────────────────────────────────────────────────────────────────
// Legend (shared by all reading views).

function renderLegend() {
  const chips = Object.entries(CATEGORY_LABEL).map(([key, label]) => `
    <span class="inline-flex items-center gap-1.5 text-[11px]">
      <span class="inline-block w-3 h-3 rounded-sm ${CATEGORY_DOT[key]}"></span>
      ${escapeHtml(label)}
    </span>
  `).join("");
  return `
    <div class="rounded-lg border border-slate-200 bg-white px-3 py-2 flex flex-wrap items-center gap-x-4 gap-y-1.5">
      <span class="text-[10px] uppercase tracking-wide text-slate-500 font-semibold">Marks</span>
      ${chips}
    </div>
  `;
}

// ───────────────────────────────────────────────────────────────────────────
// Render text with footnote-style annotation markers.
// Each annotation in the section gets a 1-indexed footnote number; the in-text
// highlight ends with a small superscript number that matches an entry in the
// right-side margin notes column.

function buildSegments(text, annotations) {
  if (annotations.length === 0) {
    return [{ text, annIndices: [] }];
  }
  const points = new Set([0, text.length]);
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
    const segText = text.substring(start, end);
    const annIndices = [];
    annotations.forEach((ann, idx) => {
      if (ann.start <= start && ann.end >= end) annIndices.push(idx);
    });
    segments.push({ text: segText, annIndices });
  }
  return segments;
}

// ───────────────────────────────────────────────────────────────────────────
// 1. Library catalog index.

const LIBRARY_CATALOG = [
  {
    basename: "001-macbeth",
    title: "Macbeth",
    author: "William Shakespeare",
    year: 1606,
    category: "Drama",
    difficulty: "Hard",
    blurb: "Shakespeare's shortest tragedy. 5 acts, 28 scenes. A Scottish general is told he will be king — and then chooses to make it true.",
    teachingFocus: "Structure (5-act arc), theme (ambition, moral inversion), figurative language density.",
    status: "ready",
  },
  {
    basename: "002-adventures-of-sherlock-holmes",
    title: "The Adventures of Sherlock Holmes",
    author: "Arthur Conan Doyle",
    year: 1892,
    category: "Detective Fiction",
    difficulty: "Medium",
    blurb: "12 self-contained short stories. Each is a masterclass in observation and deduction.",
    teachingFocus: "Inference (clue → reasoning → conclusion), tone (Watson's voice).",
    status: "ready",
  },
  {
    basename: "003-moonstone",
    title: "The Moonstone",
    author: "Wilkie Collins",
    year: 1868,
    category: "Detective Fiction",
    difficulty: "Hard",
    blurb: "The first detective novel. Eight narrators tell pieces of one mystery.",
    teachingFocus: "Point of view, unreliable narration, structural genius. The PD substitute for Christie.",
    status: "ready",
  },
];

export function renderLibraryIndex(target) {
  const cards = LIBRARY_CATALOG.map((w) => {
    const diffCls = DIFFICULTY_CLASS[w.difficulty] || "";
    const isReady = w.status === "ready";
    return `
      <li>
        ${isReady ? `<a href="#/library/${escapeHtml(w.basename)}" class="block group">` : `<div class="block opacity-60">`}
          <div class="rounded-lg border border-slate-200 bg-white p-4 ${isReady ? "hover:border-slate-400 transition" : ""}">
            <div class="flex items-start justify-between gap-2">
              <div>
                <h3 class="font-semibold text-slate-800 ${isReady ? "group-hover:underline" : ""}">${escapeHtml(w.title)}</h3>
                <div class="text-xs text-slate-500 mt-0.5">${escapeHtml(w.author)} · ${escapeHtml(String(w.year))} · ${escapeHtml(w.category)}</div>
              </div>
              <div class="flex flex-col items-end gap-1 shrink-0">
                <span class="inline-block text-[10px] border rounded-full px-1.5 py-0.5 ${diffCls}">${escapeHtml(w.difficulty)}</span>
                ${isReady ? "" : `<span class="inline-block text-[10px] text-slate-500 border border-slate-200 rounded-full px-1.5 py-0.5">Planned</span>`}
              </div>
            </div>
            <p class="mt-2 text-sm text-slate-600">${escapeHtml(w.blurb)}</p>
            <p class="mt-1 text-xs text-slate-500 italic">${escapeHtml(w.teachingFocus)}</p>
          </div>
        ${isReady ? `</a>` : `</div>`}
      </li>
    `;
  }).join("");

  target.innerHTML = `
    <section class="space-y-6">
      <header>
        <h1 class="text-2xl font-semibold tracking-tight">Reading Library</h1>
        <p class="mt-2 text-slate-600">
          Full-length works with sparse marking annotations. Pick a book, read at your own pace,
          and use the highlighted passages to see how an experienced reader marks the page.
        </p>
      </header>

      <div class="rounded-lg border border-sky-200 bg-sky-50 p-3 text-sm text-sky-900">
        <span class="font-semibold">Library vs. Lab:</span> the Reading Lab has dense annotations on short passages
        — every line marked. The Library is the opposite: long reads with sparse marking only at the famous moments.
        Use the Lab to learn the moves; use the Library to apply them.
      </div>

      <ul class="grid grid-cols-1 gap-3">${cards}</ul>

      <div class="rounded-lg border border-slate-200 bg-white p-3 text-xs text-slate-500">
        <p><span class="font-semibold text-slate-700">Why these books:</span> all are public domain in every major jurisdiction (US, UK, Canada, Australia, Asia).
        Murder on the Orient Express enters PD in life+50 countries on Jan 1, 2027 — we'll add it then.</p>
      </div>

      <footer class="pt-4 border-t border-slate-200 text-sm">
        <a href="#/" class="text-slate-700 underline">← Back home</a>
      </footer>
    </section>
  `;
}

// ───────────────────────────────────────────────────────────────────────────
// 2. Book overview page — intro, TOC, discussion prompts. NO section bodies.

export async function renderLibraryWorkPage(target, basename) {
  target.innerHTML = `<div class="text-slate-500 text-sm">Loading…</div>`;

  let work;
  try {
    work = await loadLibraryWork(basename);
  } catch (err) {
    target.innerHTML = `
      <div class="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">
        Failed to load: ${escapeHtml(err.message)}
      </div>
      <a href="#/library" class="mt-4 inline-block text-sm text-slate-700 underline">← Back to Library</a>
    `;
    return;
  }

  const stored = loadProgress(basename);
  const continueLink = stored.lastSectionId
    ? `<a href="#/library/${escapeHtml(basename)}/${escapeHtml(stored.lastSectionId)}"
          class="inline-flex items-center gap-2 rounded-md bg-slate-900 text-white px-3 py-1.5 text-sm hover:bg-slate-700 transition">
        Continue where you left off →
      </a>`
    : "";
  const startLink = `<a href="#/library/${escapeHtml(basename)}/${escapeHtml(work.sections[0].id)}"
                       class="inline-flex items-center gap-2 rounded-md border border-slate-300 px-3 py-1.5 text-sm hover:border-slate-500 transition">
                       ${stored.lastSectionId ? "Start over from the beginning" : "Start reading →"}
                     </a>`;

  const diffCls = DIFFICULTY_CLASS[work.difficulty] || "";
  const sourceLink = work.sourceUrl
    ? `<a href="${escapeHtml(work.sourceUrl)}" target="_blank" rel="noopener noreferrer" class="text-xs text-slate-500 underline hover:text-slate-700">source (Project Gutenberg)</a>`
    : "";

  // Group sections by their narrator/period if they share a common prefix.
  // For Moonstone the section labels look like "Betteredge — Chapter I" etc.
  // We auto-group on " — " presence.
  const groups = [];
  let currentGroup = null;
  for (const sec of work.sections) {
    const m = sec.label.match(/^(.+?)\s+—\s+/);
    const groupName = m ? m[1] : "_ungrouped";
    if (!currentGroup || currentGroup.name !== groupName) {
      currentGroup = { name: groupName, items: [] };
      groups.push(currentGroup);
    }
    currentGroup.items.push(sec);
  }

  const tocHtml = groups.map((g) => {
    const isUngrouped = g.name === "_ungrouped";
    const items = g.items.map((sec) => {
      const hasAnn = (sec.annotations || []).length > 0;
      const isLast = sec.id === stored.lastSectionId;
      const annDot = hasAnn ? `<span class="inline-block w-1.5 h-1.5 rounded-full bg-sky-400" title="annotated"></span>` : `<span class="inline-block w-1.5 h-1.5"></span>`;
      const lastTag = isLast ? `<span class="ml-2 text-[10px] text-amber-700 bg-amber-100 border border-amber-200 rounded-full px-1.5 py-0.5">last read</span>` : "";
      const labelShort = isUngrouped ? sec.label : sec.label.replace(/^.+?\s+—\s+/, "");
      const sub = sec.subtitle ? `<div class="text-[11px] text-slate-500 italic">${escapeHtml(sec.subtitle)}</div>` : "";
      return `
        <li>
          <a href="#/library/${escapeHtml(basename)}/${escapeHtml(sec.id)}"
             class="flex items-baseline justify-between gap-2 rounded px-2 py-1.5 hover:bg-slate-50 transition">
            <div class="min-w-0">
              <div class="text-sm text-slate-800">
                <span class="inline-flex items-baseline gap-2">${annDot} ${escapeHtml(labelShort)}</span>
                ${lastTag}
              </div>
              ${sub}
            </div>
            <span class="text-[11px] text-slate-400 shrink-0">${(sec.annotations || []).length || ""}</span>
          </a>
        </li>
      `;
    }).join("");

    if (isUngrouped) {
      return `<ul class="space-y-0.5">${items}</ul>`;
    }
    return `
      <details ${groups.length <= 3 ? "open" : ""} class="group/g">
        <summary class="cursor-pointer list-none flex items-center justify-between gap-2 px-2 py-1.5 rounded hover:bg-slate-50">
          <span class="text-xs uppercase tracking-wide text-slate-600 font-semibold">${escapeHtml(g.name)}</span>
          <span class="text-[10px] text-slate-400">${g.items.length} sections</span>
        </summary>
        <ul class="space-y-0.5 pl-3 border-l border-slate-100 ml-2 mt-1">${items}</ul>
      </details>
    `;
  }).join("");

  const promptsHtml = work.discussionPrompts.length
    ? `
      <section class="space-y-2 mt-8">
        <h2 class="text-sm uppercase tracking-wide text-slate-500">Discussion prompts</h2>
        <ol class="list-decimal list-outside ml-5 space-y-2 text-sm text-slate-700">
          ${work.discussionPrompts.map((p, i) => {
            const ans = work.discussionAnswers[i];
            if (!ans) return `<li>${escapeHtml(p)}</li>`;
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
                  <div class="mt-1.5 ml-1 pl-3 border-l-2 border-slate-200 text-slate-600">${escapeHtml(ans)}</div>
                </details>
              </li>
            `;
          }).join("")}
        </ol>
      </section>
    `
    : "";

  target.innerHTML = `
    <article class="space-y-5">
      <header class="space-y-1">
        <div class="flex items-center gap-2 text-xs uppercase tracking-wide text-slate-500">
          <span>Reading Library · ${escapeHtml(work.category)}</span>
          ${work.difficulty ? `<span class="inline-block border rounded-full px-1.5 py-0.5 text-[10px] normal-case tracking-normal ${diffCls}">${escapeHtml(work.difficulty)}</span>` : ""}
        </div>
        <h1 class="text-2xl font-semibold tracking-tight">${escapeHtml(work.title)}</h1>
        <div class="text-sm text-slate-600">
          ${escapeHtml(work.author)} · ${escapeHtml(String(work.year))} · ${work.lengthWords ? `${work.lengthWords.toLocaleString()} words` : ""} · ${work.sections.length} sections
          ${sourceLink ? `· ${sourceLink}` : ""}
        </div>
      </header>

      <div class="rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900">${escapeHtml(work.intro)}</div>

      <div class="flex flex-wrap items-center gap-2">${continueLink} ${startLink}</div>

      ${renderLegend()}

      <section class="space-y-2 mt-2">
        <h2 class="text-sm uppercase tracking-wide text-slate-500">Contents</h2>
        <div class="rounded-lg border border-slate-200 bg-white p-2 space-y-1">${tocHtml}</div>
      </section>

      ${promptsHtml}

      <footer class="pt-4 border-t border-slate-200 text-sm">
        <a href="#/library" class="text-slate-700 underline">← Back to Library</a>
      </footer>
    </article>
  `;
}

// ───────────────────────────────────────────────────────────────────────────
// 3. Section page — single scene/chapter with marginalia.

export async function renderLibrarySectionPage(target, basename, sectionId) {
  target.innerHTML = `<div class="text-slate-500 text-sm">Loading…</div>`;

  let work;
  try {
    work = await loadLibraryWork(basename);
  } catch (err) {
    target.innerHTML = `
      <div class="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">
        Failed to load: ${escapeHtml(err.message)}
      </div>
      <a href="#/library" class="mt-4 inline-block text-sm text-slate-700 underline">← Back to Library</a>
    `;
    return;
  }

  const idx = work.sections.findIndex((s) => s.id === sectionId);
  if (idx < 0) {
    target.innerHTML = `
      <div class="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">
        Section <code>${escapeHtml(sectionId)}</code> not found in <em>${escapeHtml(work.title)}</em>.
      </div>
      <a href="#/library/${escapeHtml(basename)}" class="mt-4 inline-block text-sm text-slate-700 underline">← Back to ${escapeHtml(work.title)}</a>
    `;
    return;
  }

  // Save progress on visit.
  saveProgress(basename, sectionId);

  const sec = work.sections[idx];
  const prev = idx > 0 ? work.sections[idx - 1] : null;
  const next = idx < work.sections.length - 1 ? work.sections[idx + 1] : null;
  const anns = sec.annotations || [];

  let showMarkup = true;
  let highlightedAnnIdx = null;

  function renderTextHtml() {
    const segs = buildSegments(sec.text, anns);
    return segs
      .map((seg) => {
        const safe = escapeHtml(normalizeProseWhitespace(seg.text));
        if (!showMarkup || seg.annIndices.length === 0) return safe;
        const primary = anns[seg.annIndices[0]];
        const cls = CATEGORY_CLASS[primary.category];
        const isHighlighted = highlightedAnnIdx === seg.annIndices[0];
        const ring = isHighlighted ? "ring-2 ring-slate-700" : "";
        const labels = seg.annIndices.map((i) => CATEGORY_LABEL[anns[i].category]).join(", ");
        // First segment of this annotation gets the footnote marker
        const isFirstSeg = seg.annIndices.length > 0 && primary.start === (sec.text.indexOf(seg.text, primary.start) - 0 < 0 ? -1 : primary.start);
        // Simpler: only emit a footnote marker at the absolute start of an annotation
        // We track by checking if any annotation's start equals the segment's character position.
        const markerNum = seg.annIndices[0] + 1;
        const isAnnStart = primary.start === sec.text.indexOf(seg.text);
        return `<button data-ann-idx="${seg.annIndices[0]}"
                  class="${cls} ${ring} rounded px-0.5 cursor-pointer transition focus:outline-none focus:ring-2 focus:ring-slate-500"
                  aria-label="${escapeHtml(labels)}">${safe}<sup class="text-[10px] font-bold ml-0.5 not-italic">${markerNum}</sup></button>`;
      })
      .join("");
  }

  function renderMarginNotes() {
    if (anns.length === 0) {
      return `
        <div class="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-3 text-xs text-slate-500">
          No marking notes in this section. Keep reading — the next annotated passage may be a few sections away.
        </div>
      `;
    }
    return anns
      .map((ann, i) => {
        const dot = CATEGORY_DOT[ann.category];
        const border = CATEGORY_BORDER[ann.category];
        const isHighlighted = highlightedAnnIdx === i;
        const highlight = isHighlighted ? "ring-2 ring-slate-700" : "";
        const snippet = sec.text.substring(ann.start, ann.end);
        const snippetDisplay = snippet.length > 70 ? snippet.substring(0, 67) + "…" : snippet;
        return `
          <div data-note-idx="${i}"
               class="rounded-lg border-l-4 ${border} bg-white p-3 ${highlight} cursor-pointer hover:bg-slate-50 transition">
            <div class="flex items-center gap-2 text-[10px] uppercase tracking-wide">
              <span class="font-bold text-slate-600">${i + 1}</span>
              <span class="inline-block w-2.5 h-2.5 rounded-sm ${dot}"></span>
              <span class="text-slate-600">${escapeHtml(CATEGORY_LABEL[ann.category])}</span>
            </div>
            <div class="mt-1 text-[12px] text-slate-500 italic line-clamp-2">"${escapeHtml(snippetDisplay)}"</div>
            <div class="mt-1.5 text-xs text-slate-700 leading-snug">${escapeHtml(ann.note)}</div>
          </div>
        `;
      })
      .join("");
  }

  function renderNav(extraClass = "") {
    const prevLink = prev
      ? `<a href="#/library/${escapeHtml(basename)}/${escapeHtml(prev.id)}" class="inline-flex items-center gap-1 text-sm text-slate-700 hover:text-slate-900">← ${escapeHtml(prev.label)}</a>`
      : `<span class="text-sm text-slate-300">← (start of book)</span>`;
    const nextLink = next
      ? `<a href="#/library/${escapeHtml(basename)}/${escapeHtml(next.id)}" class="inline-flex items-center gap-1 text-sm text-slate-700 hover:text-slate-900">${escapeHtml(next.label)} →</a>`
      : `<span class="text-sm text-slate-300">(end of book) →</span>`;
    return `
      <nav class="flex items-center justify-between gap-3 ${extraClass}">
        ${prevLink}
        <span class="text-xs text-slate-500">Section ${idx + 1} of ${work.sections.length}</span>
        ${nextLink}
      </nav>
    `;
  }

  function render() {
    const diffCls = DIFFICULTY_CLASS[work.difficulty] || "";
    target.innerHTML = `
      <article class="space-y-4">
        <div class="flex items-center justify-between gap-2 text-xs">
          <a href="#/library/${escapeHtml(basename)}" class="text-slate-600 hover:text-slate-900 underline">← ${escapeHtml(work.title)}</a>
          <span class="text-slate-400">Reading Library</span>
        </div>

        <header class="space-y-1">
          <div class="flex items-center gap-2 text-xs uppercase tracking-wide text-slate-500">
            <span>${escapeHtml(work.title)}</span>
            ${work.difficulty ? `<span class="inline-block border rounded-full px-1.5 py-0.5 text-[10px] normal-case tracking-normal ${diffCls}">${escapeHtml(work.difficulty)}</span>` : ""}
          </div>
          <h1 class="text-2xl font-semibold tracking-tight">${escapeHtml(sec.label)}</h1>
          ${sec.subtitle ? `<div class="text-sm text-slate-600 italic">${escapeHtml(sec.subtitle)}</div>` : ""}
        </header>

        <div class="flex items-center justify-between gap-3 flex-wrap">
          <div class="flex-1 min-w-0">${renderLegend()}</div>
          <button id="toggle-markup" class="text-xs rounded border border-slate-300 px-3 py-1 hover:border-slate-500 bg-white">
            ${showMarkup ? "Hide marks" : "Show marks"}
          </button>
        </div>

        ${renderNav("border-y border-slate-200 py-2")}

        <div class="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-6">
          <div id="prose" class="whitespace-pre-wrap font-serif leading-8 text-slate-800 text-base lg:text-[17px] min-w-0">
            ${renderTextHtml()}
          </div>
          <aside class="lg:sticky lg:top-2 lg:self-start lg:max-h-[calc(100vh-3rem)] lg:overflow-y-auto space-y-2">
            <h2 class="text-xs uppercase tracking-wide text-slate-500 font-semibold">Margin notes (${anns.length})</h2>
            ${renderMarginNotes()}
          </aside>
        </div>

        ${renderNav("border-t border-slate-200 pt-4 mt-4")}
      </article>
    `;

    // Wire annotation click handlers — cross-highlight text ↔ note.
    target.querySelectorAll("button[data-ann-idx]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const i = Number(btn.dataset.annIdx);
        highlightedAnnIdx = highlightedAnnIdx === i ? null : i;
        render();
        if (highlightedAnnIdx !== null) {
          const noteEl = target.querySelector(`[data-note-idx="${highlightedAnnIdx}"]`);
          if (noteEl) noteEl.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      });
    });
    target.querySelectorAll("[data-note-idx]").forEach((el) => {
      el.addEventListener("click", () => {
        const i = Number(el.dataset.noteIdx);
        highlightedAnnIdx = highlightedAnnIdx === i ? null : i;
        render();
        if (highlightedAnnIdx !== null) {
          const ann = target.querySelector(`button[data-ann-idx="${highlightedAnnIdx}"]`);
          if (ann) ann.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      });
    });

    const toggle = target.querySelector("#toggle-markup");
    if (toggle) {
      toggle.addEventListener("click", () => {
        showMarkup = !showMarkup;
        highlightedAnnIdx = null;
        render();
      });
    }
  }

  render();
}
