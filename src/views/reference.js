// src/views/reference.js — the Quick Reference page.
//
// Pulls quick_ref from every available lesson and renders a one-page scannable
// pre-read checklist grouped by MAP category.

import { loadLesson } from "../loader.js";

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

/**
 * Render the Quick Reference page.
 *
 * @param {HTMLElement} target
 * @param {Array<{module: string, basename: string, title: string, category: string, subId: string}>} catalog
 */
export async function renderReferencePage(target, catalog) {
  target.innerHTML = `<div class="text-slate-500 text-sm">Loading reference…</div>`;

  // Load all lessons in parallel. If any fail, we still render the rest.
  const lessons = await Promise.all(
    catalog.map(async (item) => {
      try {
        const lesson = await loadLesson(item.module, item.basename);
        return { ...item, quickRef: lesson.quickRef, error: null };
      } catch (err) {
        return { ...item, quickRef: null, error: err.message };
      }
    }),
  );

  // Group by category, preserving catalog order.
  const groups = [];
  const seen = new Map();
  for (const l of lessons) {
    if (!seen.has(l.category)) {
      seen.set(l.category, groups.length);
      groups.push({ category: l.category, items: [] });
    }
    groups[seen.get(l.category)].items.push(l);
  }

  const sections = groups
    .map((g) => {
      const rows = g.items
        .map((it) => {
          if (it.error) {
            return `
              <li class="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">
                <span class="text-xs font-mono mr-2">${escapeHtml(it.subId)}</span>
                ${escapeHtml(it.title)} — failed to load
              </li>
            `;
          }
          return `
            <li class="rounded-md border border-slate-200 bg-white px-3 py-2 text-sm">
              <a class="block hover:bg-slate-50 -mx-3 -my-2 px-3 py-2 rounded-md transition"
                 href="#/learn/${escapeHtml(it.module)}/${escapeHtml(it.basename)}">
                <div class="flex items-baseline gap-2">
                  <span class="text-xs font-mono text-slate-500 shrink-0 w-12">${escapeHtml(it.subId)}</span>
                  <span class="font-medium text-slate-800">${escapeHtml(it.title)}</span>
                </div>
                <div class="text-slate-600 mt-1 ml-14 text-sm">${escapeHtml(it.quickRef)}</div>
              </a>
            </li>
          `;
        })
        .join("");

      return `
        <section class="space-y-2">
          <h2 class="text-xs uppercase tracking-wide text-slate-500">${escapeHtml(g.category)}</h2>
          <ul class="space-y-2">${rows}</ul>
        </section>
      `;
    })
    .join("\n");

  target.innerHTML = `
    <section class="space-y-6">
      <header>
        <h1 class="text-2xl font-semibold tracking-tight">Quick Reference</h1>
        <p class="mt-2 text-slate-600">
          One-minute pre-read checklist. Before you open a new passage, scan this page —
          remind yourself what to notice.
        </p>
      </header>

      <div class="rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900">
        <span class="font-semibold">How to use:</span> read top to bottom in under a minute.
        Click any line to open the full mini-lesson.
      </div>

      ${sections}

      <footer class="pt-4 border-t border-slate-200 flex items-center justify-between text-sm">
        <a href="#/" class="text-slate-700 underline">← Back home</a>
        <div class="flex items-center gap-4">
          <a href="#/marking" class="text-slate-700 underline">See the full Marking Guide →</a>
          <button id="print-btn" class="text-slate-700 underline">Print this page</button>
        </div>
      </footer>
    </section>
  `;

  const printBtn = document.getElementById("print-btn");
  if (printBtn) {
    printBtn.addEventListener("click", () => window.print());
  }
}
