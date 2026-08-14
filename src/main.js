// src/main.js — entry point for Break 250 Reading (Stack v0 pure-static)
//
// Active routes:
//   #/                              home (sub-concept directory + Reading Lab)
//   #/learn/{module}/{slug}         mini-lesson view
//   #/quiz/{module}/{slug}          quiz flow + feedback + score
//   #/lab/{basename}                Reading Lab text detail
//   #/reference                     Quick Reference page

import { renderLessonPage } from "./views/lesson.js";
import { renderQuizPage } from "./views/quiz.js";
import { renderReferencePage } from "./views/reference.js";
import { renderLabPage } from "./views/lab.js";
import { renderMarkingGuide } from "./views/marking-guide.js";
import { renderLibraryIndex, renderLibraryWorkPage, renderLibrarySectionPage } from "./views/library.js";
import { statusBadge, resetAll } from "./progress.js";

const app = document.getElementById("app");

const CATALOG = [
  { module: "m0", basename: "01-five-questions",                 title: "The 5 Reading Questions",              category: "Orientation",     subId: "0.1" },
  { module: "m0", basename: "abstract",                          title: "The Reading Areas & Tools",            category: "Orientation",     subId: "0.2" },
  { module: "a1", basename: "01-theme-message-not-topic",        title: "Theme Is a Message, Not a Topic",      category: "A · Literary",    subId: "A1.1" },
  { module: "a1", basename: "02-theme-multiple-details",         title: "Theme Is Supported by Multiple Details", category: "A · Literary",  subId: "A1.2" },
  { module: "a2", basename: "01-inference-clue-reasoning",       title: "Inference = Clue + Reasoning",         category: "A · Literary",    subId: "A2.1" },
  { module: "a2", basename: "02-inference-from-character-action", title: "Inference from Character Action",     category: "A · Literary",    subId: "A2.2" },
  { module: "a2", basename: "03-inference-vs-stated-fact",       title: "Inference vs Stated Fact",             category: "A · Literary",    subId: "A2.3" },
  { module: "a2", basename: "04-avoiding-over-inference",        title: "Avoiding Over-Inference",              category: "A · Literary",    subId: "A2.4" },
  { module: "a4", basename: "01-tone-vs-topic-fiction",          title: "Tone vs Topic in Fiction",             category: "A · Literary",    subId: "A4.1" },
  { module: "a4", basename: "03-mood-vs-tone",                   title: "Mood vs Tone",                         category: "A · Literary",    subId: "A4.3" },
  { module: "a5", basename: "01-imagery-creates-meaning",        title: "Imagery Creates Meaning",              category: "A · Literary",    subId: "A5.1" },
  { module: "b1", basename: "01-topic-vs-main-idea",             title: "Topic vs Main Idea",                   category: "B · Informational", subId: "B1.1" },
  { module: "b1", basename: "02-main-idea-vs-detail",            title: "Main Idea vs Supporting Detail",       category: "B · Informational", subId: "B1.2" },
  { module: "b2", basename: "01-evidence-traceable",             title: "Evidence Must Be Traceable",           category: "B · Informational", subId: "B2.1" },
  { module: "b2", basename: "03-proof-vs-related",               title: "Proof vs Related Information",         category: "B · Informational", subId: "B2.3" },
  { module: "b2", basename: "05-inference-from-nonfiction",      title: "Inference from Nonfiction Cues",       category: "B · Informational", subId: "B2.5" },
  { module: "b4", basename: "01-neutral-vs-skeptical",           title: "Neutral vs Skeptical (Tone)",          category: "B · Informational", subId: "B4.1" },
  { module: "b5", basename: "03-paragraph-function",             title: "Paragraph Function",                   category: "B · Informational", subId: "B5.3" },
  { module: "c1", basename: "01-context-meaning",                title: "Context Meaning",                      category: "C · Vocabulary",  subId: "C1.1" },
  { module: "c1", basename: "02-connotation-from-context",       title: "Connotation from Context",             category: "C · Vocabulary",  subId: "C1.2" },
  { module: "c1", basename: "03-figurative-word-meaning",        title: "Figurative Word Meaning",              category: "C · Vocabulary",  subId: "C1.3" },
  { module: "c2", basename: "01-word-precision",                 title: "Word Precision",                       category: "C · Vocabulary",  subId: "C2.1" },
  { module: "c3", basename: "01-academic-verbs",                 title: "Academic Verbs",                       category: "C · Vocabulary",  subId: "C3.1" },
  { module: "c3", basename: "02-tone-vocabulary",                title: "Tone Vocabulary",                      category: "C · Vocabulary",  subId: "C3.2" },
];

// Hand-maintained catalog of Reading Lab texts. Phase 2 (path to D) will derive this from a manifest.
const LAB_CATALOG = [
  // Easy
  { basename: "006-boy-who-cried-wolf",               title: "The Boy Who Cried Wolf",                   author: "Aesop",               year: 1867, category: "Fable",         difficulty: "Easy",   length: "155 words" },
  { basename: "010-tortoise-and-hare",                title: "The Tortoise and the Hare",                author: "Aesop",               year: 1867, category: "Fable",         difficulty: "Easy",   length: "130 words" },
  { basename: "011-lion-and-mouse",                   title: "The Lion and the Mouse",                   author: "Aesop",               year: 1867, category: "Fable",         difficulty: "Easy",   length: "145 words" },
  { basename: "012-who-has-seen-the-wind",            title: "Who Has Seen the Wind?",                   author: "Christina Rossetti",  year: 1872, category: "Poetry",        difficulty: "Easy",   length: "8 lines" },
  { basename: "013-wind-in-the-willows-opening",      title: "Opening of The Wind in the Willows",       author: "Kenneth Grahame",     year: 1908, category: "Literary",      difficulty: "Easy",   length: "140 words" },
  // Medium
  { basename: "004-huck-finn-opening",                title: "Opening of Huckleberry Finn",              author: "Mark Twain",          year: 1884, category: "Literary",      difficulty: "Medium", length: "152 words" },
  { basename: "005-gift-of-the-magi-opening",         title: "Opening of \"The Gift of the Magi\"",      author: "O. Henry",            year: 1905, category: "Literary",      difficulty: "Medium", length: "305 words" },
  { basename: "014-the-road-not-taken",               title: "The Road Not Taken",                       author: "Robert Frost",        year: 1916, category: "Poetry",        difficulty: "Medium", length: "20 lines" },
  { basename: "015-stopping-by-woods",                title: "Stopping by Woods on a Snowy Evening",     author: "Robert Frost",        year: 1923, category: "Poetry",        difficulty: "Medium", length: "16 lines" },
  // Hard
  { basename: "001-sonnet-18",                        title: "Sonnet 18",                                author: "William Shakespeare", year: 1609, category: "Poetry",        difficulty: "Hard",   length: "14 lines" },
  { basename: "007-all-the-worlds-a-stage",           title: "All the world's a stage (As You Like It)", author: "William Shakespeare", year: 1599, category: "Poetry",        difficulty: "Hard",   length: "28 lines" },
  { basename: "008-tomorrow-and-tomorrow",            title: "Tomorrow, and tomorrow, and tomorrow (Macbeth)", author: "William Shakespeare", year: 1606, category: "Poetry",   difficulty: "Hard",   length: "10 lines" },
  { basename: "002-gettysburg-address",               title: "The Gettysburg Address",                   author: "Abraham Lincoln",     year: 1863, category: "Informational", difficulty: "Hard",   length: "272 words" },
  { basename: "003-walden-i-went-to-the-woods",       title: "\"I went to the woods…\" (Walden)",        author: "Henry David Thoreau", year: 1854, category: "Informational", difficulty: "Hard",   length: "156 words" },
  { basename: "009-tale-of-two-cities-opening",       title: "Opening of A Tale of Two Cities",          author: "Charles Dickens",     year: 1859, category: "Literary",      difficulty: "Hard",   length: "118 words" },
];

const LAB_DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"];

const LAB_DIFFICULTY_CLASS = {
  Easy:   "bg-emerald-100 text-emerald-800 border-emerald-200",
  Medium: "bg-amber-100 text-amber-800 border-amber-200",
  Hard:   "bg-rose-100 text-rose-800 border-rose-200",
};

const BADGE_CLASSES = {
  emerald: "bg-emerald-100 text-emerald-800 border-emerald-200",
  blue:    "bg-blue-100 text-blue-800 border-blue-200",
  amber:   "bg-amber-100 text-amber-800 border-amber-200",
  rose:    "bg-rose-100 text-rose-800 border-rose-200",
  slate:   "bg-slate-100 text-slate-600 border-slate-200",
};

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function groupByCategory(catalog) {
  const groups = new Map();
  for (const item of catalog) {
    if (!groups.has(item.category)) groups.set(item.category, []);
    groups.get(item.category).push(item);
  }
  return groups;
}

// Per-category accent (dot + text) — mirrors the lesson-page gradient themes.
const CATEGORY_ACCENT = {
  "Orientation":       { bar: "bg-slate-400",   text: "text-slate-700" },
  "A · Literary":      { bar: "bg-rose-400",    text: "text-rose-700" },
  "B · Informational": { bar: "bg-sky-400",     text: "text-sky-700" },
  "C · Vocabulary":    { bar: "bg-emerald-400", text: "text-emerald-700" },
};

// Compact list of Library works for the home preview (full data lives in views/library.js).
const LIBRARY_HOME = [
  { basename: "001-macbeth",                      title: "Macbeth",                            meta: "Shakespeare · 1606 · play · 28 scenes",       difficulty: "Hard" },
  { basename: "002-adventures-of-sherlock-holmes", title: "The Adventures of Sherlock Holmes", meta: "Conan Doyle · 1892 · 12 stories",             difficulty: "Medium" },
  { basename: "003-moonstone",                    title: "The Moonstone",                      meta: "Wilkie Collins · 1868 · novel · 8 narrators", difficulty: "Hard" },
];

// Priority pill — signals how much a surface matters for breaking 250.
const PRIORITY_PILL = {
  core:        "bg-indigo-600 text-white border-indigo-600",
  recommended: "bg-amber-100 text-amber-800 border-amber-300",
  optional:    "bg-slate-100 text-slate-600 border-slate-300",
};
function priorityPill(label, kind) {
  return `<span class="inline-block text-[10px] font-semibold uppercase tracking-wide border rounded-full px-2 py-0.5 ${PRIORITY_PILL[kind] || PRIORITY_PILL.optional}">${escapeHtml(label)}</span>`;
}

// Top-level surface header — bold, with a colored accent bar, a priority pill, and an underline.
function surfaceHeader(title, accentBar, badge = "", right = "") {
  return `
    <div class="flex items-center gap-2.5 border-b-2 border-slate-200 pb-2 flex-wrap">
      <span class="inline-block w-1.5 h-6 rounded-full ${accentBar}"></span>
      <h2 class="text-xl font-bold tracking-tight text-slate-900">${escapeHtml(title)}</h2>
      ${badge}
      ${right ? `<div class="ml-auto text-xs text-slate-500">${right}</div>` : ""}
    </div>`;
}

// Second-level category header — colored dot + medium bold title.
function categoryHeader(title, accent, right = "") {
  return `
    <div class="flex items-center gap-2">
      <span class="inline-block w-2.5 h-2.5 rounded-full ${accent.bar}"></span>
      <h3 class="text-base font-semibold ${accent.text}">${escapeHtml(title)}</h3>
      ${right ? `<div class="ml-auto text-xs text-slate-500">${right}</div>` : ""}
    </div>`;
}

function renderBadge(item) {
  const badge = statusBadge(item.module, item.basename);
  const cls = BADGE_CLASSES[badge.color];
  const scoreSuffix = badge.best !== undefined ? ` ${badge.best}/10` : "";
  return `<span class="inline-block text-xs border rounded-full px-2 py-0.5 ${cls}">${escapeHtml(badge.label)}${scoreSuffix}</span>`;
}

function renderRollup(items) {
  const counts = { Mastered: 0, Good: 0, Review: 0, "Needs Practice": 0, "Not Started": 0, "Orientation Complete": 0 };
  for (const it of items) {
    const badge = statusBadge(it.module, it.basename);
    counts[badge.label] = (counts[badge.label] ?? 0) + 1;
  }
  const total = items.length;
  const completed = total - (counts["Not Started"] ?? 0);
  if (completed === 0) {
    return `<span class="text-xs text-slate-400">${total} sub-concepts · 0 attempted</span>`;
  }
  const parts = [];
  for (const label of ["Mastered", "Good", "Review", "Needs Practice", "Orientation Complete"]) {
    if (counts[label] > 0) parts.push(`${counts[label]} ${label}`);
  }
  return `<span class="text-xs text-slate-500">${completed}/${total} attempted · ${parts.join(" · ")}</span>`;
}

function renderLabSection() {
  const renderCard = (t) => {
    const diffCls = LAB_DIFFICULTY_CLASS[t.difficulty] || "bg-slate-100 text-slate-700 border-slate-200";
    return `
      <li>
        <a class="block rounded-md border border-slate-200 bg-white px-3 py-2 text-sm hover:border-slate-400 transition"
           href="#/lab/${escapeHtml(t.basename)}">
          <div class="flex items-start justify-between gap-2">
            <div class="font-medium text-slate-800">${escapeHtml(t.title)}</div>
            <span class="shrink-0 inline-block text-[10px] border rounded-full px-1.5 py-0.5 ${diffCls}">${escapeHtml(t.difficulty)}</span>
          </div>
          <div class="text-xs text-slate-500 mt-1">
            ${escapeHtml(t.author)} · ${escapeHtml(String(t.year))} · ${escapeHtml(t.category)} · ${escapeHtml(t.length)}
          </div>
        </a>
      </li>
    `;
  };

  const groups = LAB_DIFFICULTY_ORDER
    .map((diff) => {
      const items = LAB_CATALOG.filter((t) => t.difficulty === diff);
      if (items.length === 0) return "";
      const hint = { Easy: "Start here", Medium: "Step up", Hard: "Challenge" }[diff] || "";
      return `
        <div class="space-y-2">
          <div class="flex items-baseline gap-2">
            <h3 class="text-xs font-semibold uppercase tracking-wide text-slate-600">${escapeHtml(diff)}</h3>
            <span class="text-[11px] text-slate-400">${escapeHtml(hint)} · ${items.length} texts</span>
          </div>
          <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">${items.map(renderCard).join("")}</ul>
        </div>
      `;
    })
    .join("");

  return `
    <section class="space-y-4">
      ${surfaceHeader("Reading Lab", "bg-amber-400", priorityPill("Recommended", "recommended"), `${LAB_CATALOG.length} short texts · dense markup`)}
      <p class="text-sm text-slate-600 -mt-1">See how an advanced reader marks up a text — every meaningful phrase highlighted. You don't need all ${LAB_CATALOG.length}: work through a few across the difficulty levels to learn the technique, then apply it in the Library.</p>
      ${groups}
    </section>
  `;
}

function renderLibrarySection() {
  const cards = LIBRARY_HOME.map((b) => {
    const diffCls = LAB_DIFFICULTY_CLASS[b.difficulty] || "bg-slate-100 text-slate-700 border-slate-200";
    return `
      <li>
        <a class="block rounded-md border border-slate-200 bg-white px-3 py-2 text-sm hover:border-slate-400 transition"
           href="#/library/${escapeHtml(b.basename)}">
          <div class="flex items-start justify-between gap-2">
            <div class="font-medium text-slate-800">${escapeHtml(b.title)}</div>
            <span class="shrink-0 inline-block text-[10px] border rounded-full px-1.5 py-0.5 ${diffCls}">${escapeHtml(b.difficulty)}</span>
          </div>
          <div class="text-xs text-slate-500 mt-1">${escapeHtml(b.meta)}</div>
        </a>
      </li>
    `;
  }).join("");

  return `
    <section class="space-y-4">
      ${surfaceHeader("Reading Library", "bg-violet-400", priorityPill("Optional · Experimental", "optional"), `<a href="#/library" class="underline hover:text-slate-900">Open Library →</a>`)}
      <p class="text-sm text-slate-600 -mt-1">Full-length works with sparse marking — only the famous moments. Where you apply the habit at length. Our newest surface; annotations are AI-drafted, so treat them as a model rather than gospel.</p>
      <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">${cards}</ul>
    </section>
  `;
}

function renderHome() {
  const groups = groupByCategory(CATALOG);
  const catSections = [];
  for (const [cat, items] of groups) {
    const accent = CATEGORY_ACCENT[cat] || { bar: "bg-slate-300", text: "text-slate-700" };
    const links = items.map((it) => `
      <li>
        <a class="flex items-center justify-between gap-2 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm hover:border-slate-400 hover:shadow-sm transition"
           href="#/learn/${escapeHtml(it.module)}/${escapeHtml(it.basename)}">
          <span>
            <span class="text-slate-400 text-xs font-mono mr-2">${escapeHtml(it.subId)}</span>
            ${escapeHtml(it.title)}
          </span>
          ${renderBadge(it)}
        </a>
      </li>
    `).join("");
    catSections.push(`
      <section class="space-y-2">
        ${categoryHeader(cat, accent, renderRollup(items))}
        <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">${links}</ul>
      </section>
    `);
  }

  app.innerHTML = `
    <div class="space-y-10">
      <header class="bg-gradient-to-b from-indigo-50 to-white -mx-4 px-4 pt-2 pb-6 border-b border-slate-200">
        <p class="text-xs font-semibold uppercase tracking-wide text-indigo-700">For advanced middle-school readers around RIT 230-249</p>
        <h1 class="mt-2 text-3xl font-bold tracking-tight text-slate-900">Train for MAP Reading 250+ Thinking</h1>
        <div class="mt-4 max-w-3xl space-y-3 text-sm leading-6 text-slate-600">
          <p>
            Many strong readers get stuck near <span class="font-medium text-slate-900">MAP Reading 250</span>,
            even after reading hundreds of books and millions of words a year.
          </p>
          <p>
            They can follow the passage, understand the plot, and identify the main idea. But 250+ questions
            often test something more precise: whether students can
            <span class="font-medium text-slate-900">understand the author’s purpose</span>,
            <span class="font-medium text-slate-900">avoid true-but-incomplete answers</span>, and
            <span class="font-medium text-slate-900">choose the answer best supported by exact evidence</span>.
          </p>
          <p>
            At this level, 250+ advanced readers ask:
          </p>
          <ul class="grid gap-1 text-slate-700 sm:grid-cols-2">
            <li><span class="font-semibold text-slate-900">Why did the author choose this word?</span></li>
            <li><span class="font-semibold text-slate-900">What evidence proves the answer?</span></li>
            <li><span class="font-semibold text-slate-900">What is implied, but not directly stated?</span></li>
            <li><span class="font-semibold text-slate-900">What tone is being created?</span></li>
            <li><span class="font-semibold text-slate-900">How is the passage structured?</span></li>
          </ul>
          <div class="-mb-1">
            <button id="pitch-toggle" type="button" class="text-xs font-semibold text-indigo-700 underline hover:text-indigo-900">Hide the example ▴</button>
          </div>
          <div id="pitch-more" class="space-y-3">
            <p>
              The common trap is choosing an answer that sounds correct, mature, or logically possible.
              MAP 250+ rewards the answer that is <span class="font-medium text-slate-900">best-supported by the text</span>:
              the one the exact evidence proves best.
            </p>
            <div class="rounded-xl border border-slate-200 bg-white/80 p-4">
              <h2 class="text-sm font-semibold text-slate-900">Worked example: a true answer vs. the best-supported answer</h2>
              <p class="mt-2 text-slate-600">
                In <span class="italic">Harry Potter and the Sorcerer’s Stone</span>, Harry discovers the Mirror of Erised.
                When he looks into it, he sees his parents and the family he lost as a baby, alive and smiling back at him.
                He returns to the mirror again, because the image gives him something he longs for. Dumbledore tells him not to return, and says:
              </p>
              <blockquote class="mt-3 border-l-4 border-indigo-200 pl-3 text-sm italic text-slate-700">
                “This mirror gives us neither knowledge or truth.”<br>
                “It does not do to dwell on dreams and forget to live.”
              </blockquote>

              <p class="mt-4 font-medium text-slate-900">Question</p>
              <p class="mt-1 text-slate-600">What deeper idea is the author showing here?</p>
              <ul class="mt-2 space-y-1.5">
                <li><button type="button" data-choice="A" class="ex-opt w-full text-left rounded-md border border-slate-200 bg-white px-2.5 py-1.5 text-slate-700 transition hover:border-indigo-300 hover:bg-indigo-50/60 focus:outline-none focus:ring-2 focus:ring-indigo-400"><span class="font-mono text-xs text-slate-400 mr-1">A.</span> Harry misses his parents and wishes he could see them again.</button></li>
                <li><button type="button" data-choice="B" class="ex-opt w-full text-left rounded-md border border-slate-200 bg-white px-2.5 py-1.5 text-slate-700 transition hover:border-indigo-300 hover:bg-indigo-50/60 focus:outline-none focus:ring-2 focus:ring-indigo-400"><span class="font-mono text-xs text-slate-400 mr-1">B.</span> The mirror is magical and shows whatever a person most wants.</button></li>
                <li><button type="button" data-choice="C" class="ex-opt w-full text-left rounded-md border border-slate-200 bg-white px-2.5 py-1.5 text-slate-700 transition hover:border-indigo-300 hover:bg-indigo-50/60 focus:outline-none focus:ring-2 focus:ring-indigo-400"><span class="font-mono text-xs text-slate-400 mr-1">C.</span> Dumbledore is wise and knows more about the mirror than Harry does.</button></li>
                <li><button type="button" data-choice="D" class="ex-opt w-full text-left rounded-md border border-slate-200 bg-white px-2.5 py-1.5 text-slate-700 transition hover:border-indigo-300 hover:bg-indigo-50/60 focus:outline-none focus:ring-2 focus:ring-indigo-400"><span class="font-mono text-xs text-slate-400 mr-1">D.</span> Dwelling on what you wish for can stop you from living your real life.</button></li>
              </ul>
              <p id="ex-hint" class="mt-3 text-xs italic text-slate-500">Pick an answer to see how a strong reader and a 250+ reader think it through.</p>

              <div id="ex-explain" class="hidden mt-3 border-t border-slate-100 pt-3">
                <p class="text-sm font-medium text-slate-900">
                  The difference: strong readers often find a true answer; 250+ readers find the answer the text proves best.
                </p>
                <div class="mt-3 grid gap-3 sm:grid-cols-2">
                  <div class="rounded-lg bg-slate-50 p-3">
                    <h3 class="text-xs font-semibold uppercase tracking-wide text-slate-500">Strong reader — understands the story</h3>
                    <ul class="mt-1 space-y-1.5 text-slate-700">
                      <li>
                        <span class="font-semibold text-slate-900">Understands the story:</span>
                        Harry misses his parents, and the mirror shows people what they most want.
                      </li>
                      <li>
                        <span class="font-semibold text-slate-900">Knows the main idea:</span>
                        he wants to see his parents, and Dumbledore warns him that the mirror will not help him.
                      </li>
                      <li>
                        <span class="font-semibold text-slate-900">Picks a true answer:</span>
                        often <span class="font-semibold">A, B, or C</span> — each is true, but none is the deeper idea.
                      </li>
                    </ul>
                  </div>
                  <div class="rounded-lg bg-indigo-50 p-3">
                    <h3 class="text-xs font-semibold uppercase tracking-wide text-indigo-700">250+ reader — finds what the author proves</h3>
                    <ul class="mt-1 space-y-1.5 text-slate-700">
                      <li>
                        <span class="font-semibold text-indigo-900">Finds the author’s idea:</span>
                        the scene is not really about the mirror’s magic or about Dumbledore’s wisdom — it is about the danger of
                        living inside a wish instead of a real life.
                      </li>
                      <li>
                        <span class="font-semibold text-indigo-900">Proves it with exact evidence:</span>
                        “It does not do to <span class="italic">dwell on dreams and forget to live</span>,” and the mirror gives
                        “neither knowledge or truth” — the words point straight at the idea.
                      </li>
                      <li>
                        <span class="font-semibold text-indigo-900">Separates inference from guessing:</span>
                        A, B, and C are all true in the story, but only <span class="font-semibold">D</span> is what the evidence
                        supports — so the 250+ reader chooses <span class="font-semibold">D</span>.
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <p>
            This app helps students build that habit quickly. Begin with short lessons and trap-focused
            quizzes. Then move into <span class="font-medium text-slate-900">Reading Lab</span> and
            <span class="font-medium text-slate-900">Library</span> to recognize the same reading moves in real passages.
          </p>
          <p class="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-amber-900">
            Honest promise: this is not an official MAP simulator or a score guarantee. It teaches the evidence,
            inference, tone, structure, and word-choice habits that strong readers need at higher levels. You still
            need to practice real reading with these methods until the moves become automatic.
          </p>
        </div>
      </header>

      <section class="space-y-5">
        ${surfaceHeader("Lessons & Quizzes", "bg-indigo-500", priorityPill("Core", "core"), `${CATALOG.length} lessons · ${CATALOG.length * 10} quizzes`)}
        ${catSections.join("\n")}
      </section>

      ${renderLabSection()}

      ${renderLibrarySection()}

      <div class="rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600 flex items-center justify-between gap-3">
        <div>
          <p class="font-medium text-slate-800 mb-1">Progress is saved in your browser</p>
          <p>${CATALOG.length} lessons · ${CATALOG.length * 10} quizzes · ${LAB_CATALOG.length} lab texts · ${LIBRARY_HOME.length} library books. Status badges update after each completed quiz.</p>
        </div>
        <button id="reset-btn" class="shrink-0 text-xs text-rose-600 hover:underline">Reset progress</button>
      </div>
    </div>
  `;

  const resetBtn = document.getElementById("reset-btn");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      if (confirm("Reset all progress? This will erase your quiz scores and attempts.")) {
        resetAll();
        renderHome();
      }
    });
  }

  wirePitchInteractions();
}

// Landing-pitch interactivity: hide/show the example, choose an answer to mark
// it right/wrong + reveal the comparison, and remember the answer across refreshes.
const PITCH_ANSWER_KEY = "break250.pitchAnswered";
const PITCH_CORRECT = "D";

function loadPitchAnswer() {
  try { return localStorage.getItem(PITCH_ANSWER_KEY); } catch { return null; }
}
function savePitchAnswer(choice) {
  try { localStorage.setItem(PITCH_ANSWER_KEY, choice); } catch {}
}

// Mark each option right (the correct one) or wrong (the chosen one), like a quiz.
function markPitchAnswer(chosen) {
  document.querySelectorAll(".ex-opt").forEach((b) => {
    b.classList.remove(
      "border-emerald-400", "bg-emerald-50", "border-rose-300", "bg-rose-50",
      "border-slate-200", "bg-white",
    );
    const oldTag = b.querySelector(".ex-tag");
    if (oldTag) oldTag.remove();
    const c = b.dataset.choice;
    if (c === PITCH_CORRECT) {
      b.classList.add("border-emerald-400", "bg-emerald-50");
      b.insertAdjacentHTML("beforeend", `<span class="ex-tag ml-2 whitespace-nowrap text-xs font-semibold text-emerald-700">✓ best-supported</span>`);
    } else if (c === chosen) {
      b.classList.add("border-rose-300", "bg-rose-50");
      b.insertAdjacentHTML("beforeend", `<span class="ex-tag ml-2 whitespace-nowrap text-xs font-semibold text-rose-600">✗ true, but not the best</span>`);
    } else {
      b.classList.add("border-slate-200", "bg-white");
    }
  });
}

function wirePitchInteractions() {
  const pitchToggle = document.getElementById("pitch-toggle");
  const pitchMore = document.getElementById("pitch-more");
  const exExplain = document.getElementById("ex-explain");
  const exHint = document.getElementById("ex-hint");

  function setCollapsed(collapsed) {
    if (!pitchMore || !pitchToggle) return;
    pitchMore.classList.toggle("hidden", collapsed);
    pitchToggle.textContent = collapsed ? "Show the example ▾" : "Hide the example ▴";
  }

  if (pitchToggle && pitchMore) {
    pitchToggle.addEventListener("click", () => setCollapsed(!pitchMore.classList.contains("hidden")));
  }

  function reveal(chosen) {
    markPitchAnswer(chosen);
    if (exHint) exHint.classList.add("hidden");
    if (exExplain) exExplain.classList.remove("hidden");
  }

  document.querySelectorAll(".ex-opt").forEach((btn) => {
    btn.addEventListener("click", () => {
      const chosen = btn.dataset.choice;
      reveal(chosen);
      savePitchAnswer(chosen);
    });
  });

  // Returning visitor: if they already answered, restore the marked state and
  // auto-collapse the example so they don't have to scroll past it again.
  const prior = loadPitchAnswer();
  if (prior) {
    reveal(prior);
    setCollapsed(true);
  }
}

function renderReference() {
  renderReferencePage(app, CATALOG);
}

function renderMarking() {
  renderMarkingGuide(app);
}

function renderNotFound(hash) {
  app.innerHTML = `
    <section class="space-y-4">
      <h1 class="text-2xl font-semibold tracking-tight">Not found</h1>
      <p class="text-slate-600">Route <code>${escapeHtml(hash)}</code> doesn't match a known view.</p>
      <a href="#/" class="inline-block text-sm text-slate-700 underline">← Back home</a>
    </section>
  `;
}

function router() {
  const hash = location.hash || "#/";

  if (hash === "#/" || hash === "#") {
    renderHome();
    return;
  }

  if (hash === "#/reference") {
    renderReference();
    return;
  }

  if (hash === "#/marking") {
    renderMarking();
    return;
  }

  const learnMatch = hash.match(/^#\/learn\/([a-z][a-z0-9]+)\/(.+)$/);
  if (learnMatch) {
    const [, moduleId, fileBasename] = learnMatch;
    renderLessonPage(app, moduleId, fileBasename);
    return;
  }

  const quizMatch = hash.match(/^#\/quiz\/([a-z][a-z0-9]+)\/(.+)$/);
  if (quizMatch) {
    const [, moduleId, fileBasename] = quizMatch;
    const idx = CATALOG.findIndex((c) => c.module === moduleId && c.basename === fileBasename);
    const next = idx >= 0 && idx + 1 < CATALOG.length ? CATALOG[idx + 1] : null;
    renderQuizPage(app, moduleId, fileBasename, next);
    return;
  }

  const labMatch = hash.match(/^#\/lab\/(.+)$/);
  if (labMatch) {
    const [, basename] = labMatch;
    renderLabPage(app, basename);
    return;
  }

  if (hash === "#/library") {
    renderLibraryIndex(app);
    return;
  }

  // Section route must be matched BEFORE the book-overview route.
  const librarySectionMatch = hash.match(/^#\/library\/([^/]+)\/(.+)$/);
  if (librarySectionMatch) {
    const [, basename, sectionId] = librarySectionMatch;
    renderLibrarySectionPage(app, basename, sectionId);
    return;
  }

  const libraryMatch = hash.match(/^#\/library\/([^/]+)$/);
  if (libraryMatch) {
    const [, basename] = libraryMatch;
    renderLibraryWorkPage(app, basename);
    return;
  }

  renderNotFound(hash);
}

window.addEventListener("hashchange", router);
window.addEventListener("DOMContentLoaded", router);
router();
