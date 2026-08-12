// src/views/lesson.js — render the mini-lesson page for one sub-concept.

import { loadLesson } from "../loader.js";

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// ───────────────────────────────────────────────────────────────────────────
// Lightweight markdown renderer.
//
// Supported:
//   - blank line → paragraph break
//   - `- item`  → bulleted list
//   - `> text`  → blockquote
//   - `**bold**`, `*italic*` (italics avoid matching inside bold)
//   - whole-paragraph `**Heading.**` → styled subheading
//   - GitHub-flavored tables (`| a | b |` with a `| --- | --- |` separator row)
//
// All other characters pass through escapeHtml.

function renderMarkdown(src) {
  const lines = src.split("\n");
  const blocks = [];
  let para = [];
  let list = [];
  let quote = [];
  let table = [];

  function inline(s) {
    // Order matters: bold (**...**) before italic (*...*).
    return escapeHtml(s)
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[^*])\*([^*\n][^*]*?)\*(?!\*)/g, "$1<em>$2</em>");
  }

  function flushPara() {
    if (!para.length) return;
    const joined = para.join(" ");
    // Whole-paragraph bold → heading
    const headingMatch = joined.match(/^\*\*(.+?)\*\*[.:]?$/);
    if (headingMatch) {
      blocks.push(`<h3 class="text-base font-semibold text-slate-800 mt-6 mb-2">${inline(headingMatch[1])}</h3>`);
    } else {
      blocks.push(`<p class="text-slate-700 leading-relaxed">${inline(joined)}</p>`);
    }
    para = [];
  }
  function flushList() {
    if (!list.length) return;
    // A "definition list" is one where every item is `**Term** — description`
    // (em/en dash, hyphen, or colon). Render those as a styled term/description
    // grid instead of flat bullets — gives orientation lessons real structure.
    const DEF = /^\*\*(.+?)\*\*\s*(?:[—–-]|:)\s*(.+)$/;
    if (list.length >= 2 && list.every((li) => DEF.test(li))) {
      const rows = list
        .map((li) => {
          const m = li.match(DEF);
          return `<div class="flex flex-col sm:flex-row sm:gap-4 px-3 py-2.5">
            <dt class="font-semibold text-slate-800 sm:w-48 sm:shrink-0">${inline(m[1])}</dt>
            <dd class="text-slate-600 leading-relaxed">${inline(m[2])}</dd>
          </div>`;
        })
        .join("");
      blocks.push(`<dl class="my-3 rounded-lg border border-slate-200 divide-y divide-slate-100 bg-white text-sm">${rows}</dl>`);
    } else {
      const items = list.map((li) => `<li class="leading-relaxed">${inline(li)}</li>`).join("");
      blocks.push(`<ul class="list-disc list-outside ml-5 text-slate-700 space-y-1.5">${items}</ul>`);
    }
    list = [];
  }
  function flushQuote() {
    if (!quote.length) return;
    const joined = quote.join(" ");
    blocks.push(`<blockquote class="border-l-4 border-sky-300 bg-sky-50 pl-4 pr-3 py-2 my-2 italic text-slate-700">${inline(joined)}</blockquote>`);
    quote = [];
  }
  function flushTable() {
    if (!table.length) return;
    const rows = table.map((ln) =>
      ln.replace(/^\s*\|/, "").replace(/\|\s*$/, "").split("|").map((c) => c.trim()),
    );
    const isSep = (r) => r.every((c) => /^:?-{2,}:?$/.test(c));
    const header = rows[0];
    const body = rows.slice(1).filter((r) => !isSep(r));
    const thead = `<thead><tr>${header
      .map((c) => `<th class="text-left font-semibold text-slate-700 px-3 py-2 border-b-2 border-slate-300">${inline(c)}</th>`)
      .join("")}</tr></thead>`;
    const tbody = `<tbody>${body
      .map((r, i) => `<tr class="${i % 2 ? "bg-slate-50" : "bg-white"}">${r
        .map((c) => `<td class="px-3 py-2 border-b border-slate-100 text-slate-700 align-top">${inline(c)}</td>`)
        .join("")}</tr>`)
      .join("")}</tbody>`;
    blocks.push(
      `<div class="overflow-x-auto my-4 rounded-lg border border-slate-200"><table class="w-full text-sm border-collapse">${thead}${tbody}</table></div>`,
    );
    table = [];
  }
  function flushAll() {
    flushPara();
    flushList();
    flushQuote();
    flushTable();
  }

  for (const raw of lines) {
    const line = raw.trim();
    if (line === "") {
      flushAll();
    } else if (line.startsWith("|")) {
      flushPara();
      flushList();
      flushQuote();
      table.push(line);
    } else if (line.startsWith("- ")) {
      flushPara();
      flushQuote();
      flushTable();
      list.push(line.slice(2));
    } else if (line.startsWith("> ")) {
      flushPara();
      flushList();
      flushTable();
      quote.push(line.slice(2));
    } else {
      flushList();
      flushQuote();
      flushTable();
      para.push(line);
    }
  }
  flushAll();
  return blocks.join("\n");
}

// ───────────────────────────────────────────────────────────────────────────
// Category accent (module → color band).

const CATEGORY_THEME = {
  m0: { name: "Orientation",                  band: "from-slate-100 to-white",      pill: "bg-slate-100 text-slate-700 border-slate-200" },
  a1: { name: "A · Literary",                 band: "from-rose-50 to-white",        pill: "bg-rose-100 text-rose-800 border-rose-200" },
  a2: { name: "A · Literary",                 band: "from-rose-50 to-white",        pill: "bg-rose-100 text-rose-800 border-rose-200" },
  a3: { name: "A · Literary",                 band: "from-rose-50 to-white",        pill: "bg-rose-100 text-rose-800 border-rose-200" },
  a4: { name: "A · Literary",                 band: "from-rose-50 to-white",        pill: "bg-rose-100 text-rose-800 border-rose-200" },
  a5: { name: "A · Literary",                 band: "from-rose-50 to-white",        pill: "bg-rose-100 text-rose-800 border-rose-200" },
  b1: { name: "B · Informational",            band: "from-sky-50 to-white",         pill: "bg-sky-100 text-sky-800 border-sky-200" },
  b2: { name: "B · Informational",            band: "from-sky-50 to-white",         pill: "bg-sky-100 text-sky-800 border-sky-200" },
  b3: { name: "B · Informational",            band: "from-sky-50 to-white",         pill: "bg-sky-100 text-sky-800 border-sky-200" },
  b4: { name: "B · Informational",            band: "from-sky-50 to-white",         pill: "bg-sky-100 text-sky-800 border-sky-200" },
  b5: { name: "B · Informational",            band: "from-sky-50 to-white",         pill: "bg-sky-100 text-sky-800 border-sky-200" },
  b6: { name: "B · Informational",            band: "from-sky-50 to-white",         pill: "bg-sky-100 text-sky-800 border-sky-200" },
  c1: { name: "C · Vocabulary",               band: "from-emerald-50 to-white",     pill: "bg-emerald-100 text-emerald-800 border-emerald-200" },
  c2: { name: "C · Vocabulary",               band: "from-emerald-50 to-white",     pill: "bg-emerald-100 text-emerald-800 border-emerald-200" },
  c3: { name: "C · Vocabulary",               band: "from-emerald-50 to-white",     pill: "bg-emerald-100 text-emerald-800 border-emerald-200" },
};

/**
 * Render the lesson page into a target element.
 *
 * @param {HTMLElement} target
 * @param {string} moduleId    e.g., "b4"
 * @param {string} fileBasename e.g., "01-neutral-vs-skeptical"
 */
export async function renderLessonPage(target, moduleId, fileBasename) {
  target.innerHTML = `<div class="text-slate-500 text-sm">Loading lesson…</div>`;
  let lesson;
  try {
    lesson = await loadLesson(moduleId, fileBasename);
  } catch (err) {
    target.innerHTML = `
      <div class="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">
        Failed to load lesson: ${escapeHtml(err.message)}
      </div>
      <a href="#/" class="mt-4 inline-block text-sm text-slate-700 underline">← Back home</a>
    `;
    return;
  }

  const theme = CATEGORY_THEME[moduleId] || CATEGORY_THEME.m0;

  const examplesHtml = lesson.examples.map((ex, i) => `
    <article class="rounded-lg border border-slate-200 bg-white overflow-hidden">
      <div class="bg-slate-50 border-b border-slate-200 px-4 py-2 flex items-baseline justify-between">
        <h3 class="text-xs uppercase tracking-wide text-slate-600 font-semibold">Example ${i + 1}</h3>
        <span class="text-[10px] text-slate-400 font-mono">EX${i + 1}</span>
      </div>
      <div class="p-4 space-y-3">
        <blockquote class="border-l-4 border-slate-300 pl-3 py-1 text-slate-700 italic font-serif">"${escapeHtml(ex.text)}"</blockquote>
        <div class="flex items-baseline gap-2">
          <span class="text-[10px] uppercase tracking-wide text-emerald-700 font-semibold bg-emerald-50 border border-emerald-200 rounded px-1.5 py-0.5">Answer</span>
          <span class="text-sm font-medium text-slate-800">${escapeHtml(ex.answer)}</span>
        </div>
        <p class="text-sm text-slate-600 leading-relaxed">${escapeHtml(ex.explanation)}</p>
      </div>
    </article>
  `).join("\n");

  const trapsHtml = lesson.commonTraps.length === 0 ? "" : `
    <section class="space-y-2">
      <h2 class="text-sm uppercase tracking-wide text-slate-500 font-semibold flex items-center gap-2">
        <span class="inline-block w-2 h-2 rounded-full bg-rose-400"></span> Common traps
      </h2>
      <ul class="space-y-2">
        ${lesson.commonTraps.map((t, i) => `
          <li class="rounded-lg border border-rose-200 bg-rose-50/50 p-3 text-sm text-slate-800 leading-relaxed">
            <span class="inline-flex items-center gap-2 mr-1.5">
              <span class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-rose-600 text-white text-[10px] font-bold">${i + 1}</span>
            </span>${escapeHtml(t)}
          </li>
        `).join("")}
      </ul>
    </section>
  `;

  const whyItMattersHtml = lesson.whyItMatters ? `
    <aside class="rounded-lg border-l-4 border-amber-400 bg-amber-50/70 px-4 py-3">
      <div class="text-[10px] uppercase tracking-wide text-amber-700 font-semibold mb-1">Why this matters</div>
      <p class="text-sm text-amber-950 leading-relaxed">${escapeHtml(lesson.whyItMatters)}</p>
    </aside>
  ` : "";

  const subtitleHtml = lesson.subtitle
    ? `<p class="text-slate-600 mt-1 leading-relaxed">${escapeHtml(lesson.subtitle)}</p>`
    : "";

  target.innerHTML = `
    <article class="max-w-3xl mx-auto space-y-8">
      <header class="bg-gradient-to-b ${theme.band} -mx-4 px-4 pt-6 pb-5 border-b border-slate-200">
        <div class="flex items-center gap-2 mb-2">
          <span class="inline-block text-[10px] uppercase tracking-wide border rounded-full px-1.5 py-0.5 ${theme.pill}">${escapeHtml(theme.name)}</span>
          <span class="text-xs text-slate-500 font-mono">${escapeHtml(lesson.subConceptId)}</span>
        </div>
        <h1 class="text-3xl font-semibold tracking-tight text-slate-900">${escapeHtml(lesson.title)}</h1>
        ${subtitleHtml}
      </header>

      <section class="rounded-lg border border-amber-200 bg-amber-50 p-4">
        <div class="text-[10px] uppercase tracking-wide text-amber-700 font-semibold mb-1.5">Quick reference</div>
        <p class="text-sm text-amber-950 leading-relaxed">${escapeHtml(lesson.quickRef)}</p>
      </section>

      <section class="prose-lesson space-y-3">
        ${renderMarkdown(lesson.miniLesson)}
      </section>

      ${whyItMattersHtml}

      ${lesson.examples.length > 0 ? `
        <section class="space-y-3">
          <h2 class="text-sm uppercase tracking-wide text-slate-500 font-semibold flex items-center gap-2">
            <span class="inline-block w-2 h-2 rounded-full bg-sky-400"></span> Worked examples
          </h2>
          <div class="space-y-3">${examplesHtml}</div>
        </section>
      ` : ""}

      ${trapsHtml}

      <footer class="pt-6 border-t border-slate-200 flex items-center justify-between gap-3 flex-wrap">
        <a href="#/" class="text-sm text-slate-600 hover:text-slate-900 underline">← Back home</a>
        <a href="#/quiz/${escapeHtml(moduleId)}/${escapeHtml(fileBasename)}"
           class="inline-flex items-center gap-2 rounded-md bg-slate-900 text-white px-4 py-2 text-sm font-medium hover:bg-slate-700 transition">
          ${lesson.moduleId === "m0" ? "Try 10 recognition quizzes →" : "Start 10 quizzes →"}
        </a>
      </footer>
    </article>
  `;
}
