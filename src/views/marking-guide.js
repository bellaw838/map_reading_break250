// src/views/marking-guide.js — render the 20-item marking guide.
//
// Canonical source: docs/marking.md (this view mirrors that content for in-app access).
// Also exports the items array so other views (Reading Lab) can show short codes.

export const MARKING_ITEMS = [
  { code: "T",     name: "Topic",                  desc: "What the text is about in 1–3 words. Example: friendship, climate change, school rules." },
  { code: "MI",    name: "Main Idea / Central Idea", desc: "What the author says about the topic. Usually a full sentence." },
  { code: "TH",    name: "Theme",                  desc: "The deeper message in a story or poem. A full sentence, not one word." },
  { code: "E",     name: "Evidence",               desc: "The exact words or details that prove an answer." },
  { code: "INF",   name: "Inference",              desc: "What the text suggests but does not directly say. Formula: clue + reasoning." },
  { code: "TO",    name: "Tone",                   desc: "The author's or speaker's attitude. Examples: skeptical, admiring, frustrated, neutral." },
  { code: "M",     name: "Mood",                   desc: "The feeling created in the reader. Examples: tense, peaceful, gloomy, hopeful." },
  { code: "WC",    name: "Word Choice / Diction",  desc: "Important words the author chose and what they imply." },
  { code: "CON",   name: "Connotation",            desc: "Positive, negative, or neutral feeling of a word." },
  { code: "P",     name: "Author's Purpose",       desc: "Why the author wrote it: inform, persuade, entertain, explain, warn, criticize, celebrate." },
  { code: "POV",   name: "Point of View / Narrator", desc: "Who is speaking? Can we trust them? What do they know or not know?" },
  { code: "STR",   name: "Text Structure",         desc: "How the text is built: cause/effect, compare/contrast, sequence, problem/solution, description." },
  { code: "PF",    name: "Paragraph Function",     desc: "What job a paragraph does: introduce, explain, give evidence, contrast, conclude." },
  { code: "CL",    name: "Claim",                  desc: "What the author is trying to prove." },
  { code: "RSN",   name: "Reasoning",              desc: "How the evidence supports the claim." },
  { code: "CTR",   name: "Counterclaim / Rebuttal", desc: "Opposing view + how the author answers it." },
  { code: "FIG",   name: "Figurative Language",    desc: "Metaphor, simile, personification, imagery, symbolism, hyperbole." },
  { code: "SPK",   name: "Speaker vs Author / Poet", desc: "Especially in poems: the \"I\" in the poem is not always the poet." },
  { code: "SHIFT", name: "Shift",                  desc: "A change in tone, idea, argument, or direction." },
  { code: "TRAP",  name: "Trap Answer",            desc: "Why a wrong answer is tempting but not proven." },
];

// The 5-color Reading Lab → short-code mapping. One canonical code per color.
export const COLOR_TO_CODE = {
  tone:      "TO",
  evidence:  "E",
  theme:     "TH",
  inference: "INF",
  structure: "STR",
};

const MAP_250_PRIORITIES = ["WC", "E", "INF", "TO", "MI", "P", "STR"];

const BIG_QUESTIONS = [
  { question: "What is this text really saying?", codes: ["T", "MI", "TH", "CL"] },
  { question: "How do I prove it?", codes: ["E", "RSN", "TRAP"] },
  { question: "What is suggested but not directly said?", codes: ["INF", "POV", "SPK"] },
  { question: "How does the author feel or make me feel?", codes: ["TO", "M", "WC", "CON", "P"] },
  { question: "How is the text built?", codes: ["STR", "PF", "SHIFT", "FIG", "CTR"] },
];

const MARKING_FAMILIES = [
  {
    title: "Family 1 — What Is The Text Really Saying?",
    intro: "These marks are about the point of the text.",
    codes: ["T", "MI", "TH", "CL"],
    confusions: [
      ["Topic vs Main Idea", "Topic = subject. Main idea = what the author says about that subject."],
      ["Main Idea vs Theme", "Main idea is usually informational. Theme is usually literary. Both answer what the text is really saying."],
      ["Main Idea vs Claim", "In argument writing, the main idea is often the author's claim."],
    ],
  },
  {
    title: "Family 2 — How Do I Prove It?",
    intro: "These marks are about proof.",
    codes: ["E", "RSN", "TRAP"],
    confusions: [
      ["Evidence vs Inference", "Evidence = what the text says. Inference = what you conclude from evidence."],
      ["Evidence vs Reasoning", "Evidence is the proof. Reasoning explains how the proof supports the answer."],
      ["True Detail vs Best Evidence", "A detail can be true but still not be the strongest proof for the question."],
    ],
  },
  {
    title: "Family 3 — What Is Suggested But Not Said?",
    intro: "These marks are about clues, voice, and point of view.",
    codes: ["INF", "POV", "SPK"],
    confusions: [
      ["Inference vs Guess", "An inference must be supported by a clue in the text. A guess is not proven."],
      ["Author vs Narrator / Speaker", "Author = real writer. Narrator or speaker = voice inside the story or poem."],
      ["Stated Fact vs Inference", "If the text directly says it, it is not an inference."],
    ],
  },
  {
    title: "Family 4 — How Does The Text Feel?",
    intro: "These marks are about attitude, emotion, and word choice.",
    codes: ["TO", "M", "WC", "CON", "P"],
    confusions: [
      ["Tone vs Mood", "Tone = author or speaker's attitude. Mood = feeling created in the reader."],
      ["Word Choice vs Connotation", "Word choice is the selected word. Connotation is the feeling that word carries."],
      ["Word Choice vs Tone", "Word choice is often the evidence for tone."],
      ["Purpose vs Main Idea", "Purpose = why the author wrote it. Main idea = what the author says."],
    ],
  },
  {
    title: "Family 5 — How Is The Text Built?",
    intro: "These marks are about structure, function, and literary technique.",
    codes: ["STR", "PF", "SHIFT", "FIG", "CTR"],
    confusions: [
      ["Structure vs Paragraph Function", "Structure = whole-text pattern. Paragraph function = one paragraph's job."],
      ["Structure vs Shift", "Structure is the overall design. Shift is the moment the design changes direction."],
      ["Figurative Language vs Theme", "In poems and stories, metaphors and images often carry the theme, but they are figurative language first."],
      ["Claim vs Counterclaim", "Claim = author's position. Counterclaim = opposing position."],
    ],
  },
];

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

export function renderMarkingGuide(target) {
  const itemByCode = new Map(MARKING_ITEMS.map((it) => [it.code, it]));

  const codeBadge = (code) =>
    `<span class="inline-block font-mono text-xs font-semibold bg-slate-100 border border-slate-200 rounded px-2 py-1 text-slate-700">${escapeHtml(code)}</span>`;

  const familySections = MARKING_FAMILIES.map((family) => {
    const itemRows = family.codes.map((code) => {
      const it = itemByCode.get(code);
      const isPriority = MAP_250_PRIORITIES.includes(code);
      const priorityBadge = isPriority
        ? `<span class="ml-2 text-[10px] uppercase tracking-wide text-emerald-700 bg-emerald-100 border border-emerald-200 rounded px-1.5 py-0.5">MAP 250+</span>`
        : "";
      return `
        <li class="rounded-md border border-slate-200 bg-white p-3 flex items-baseline gap-3">
          ${codeBadge(code)}
          <div class="flex-1">
            <div class="text-sm font-medium text-slate-800">${escapeHtml(it.name)}${priorityBadge}</div>
            <div class="text-sm text-slate-600 mt-0.5">${escapeHtml(it.desc)}</div>
          </div>
        </li>
      `;
    }).join("");

    const confusionRows = family.confusions.map(([pair, difference]) => `
      <li>
        <span class="font-medium text-slate-800">${escapeHtml(pair)}:</span>
        <span class="text-slate-600">${escapeHtml(difference)}</span>
      </li>
    `).join("");

    return `
      <section class="space-y-3">
        <header>
          <h2 class="text-sm font-semibold text-slate-900">${escapeHtml(family.title)}</h2>
          <p class="text-sm text-slate-600 mt-1">${escapeHtml(family.intro)}</p>
        </header>
        <ul class="space-y-2">${itemRows}</ul>
        <div class="rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm">
          <div class="text-xs uppercase tracking-wide text-slate-500 mb-2">Easy confusion</div>
          <ul class="space-y-1.5">${confusionRows}</ul>
        </div>
      </section>
    `;
  }).join("");

  const codeRows = MARKING_ITEMS.map((it) => {
    const isPriority = MAP_250_PRIORITIES.includes(it.code);
    const priorityBadge = isPriority
      ? `<span class="ml-2 text-[10px] uppercase tracking-wide text-emerald-700 bg-emerald-100 border border-emerald-200 rounded px-1.5 py-0.5">MAP 250+</span>`
      : "";
    return `
      <tr class="border-t border-slate-100">
        <td class="py-2 pr-3 align-top">${codeBadge(it.code)}</td>
        <td class="py-2 align-top">
          <div class="text-sm font-medium text-slate-800">${escapeHtml(it.name)}${priorityBadge}</div>
        </td>
      </tr>
    `;
  }).join("");

  const priorityList = MAP_250_PRIORITIES.map((code) => {
    const it = itemByCode.get(code);
    return `<li><span class="font-mono font-semibold mr-2">${escapeHtml(code)}</span>${escapeHtml(it.name)}</li>`;
  }).join("");

  const bigQuestionRows = BIG_QUESTIONS.map((row) => `
    <tr class="border-t border-slate-100">
      <td class="py-2 pr-3 text-sm font-medium text-slate-800 align-top">${escapeHtml(row.question)}</td>
      <td class="py-2 align-top flex flex-wrap gap-1.5">${row.codes.map(codeBadge).join("")}</td>
    </tr>
  `).join("");

  target.innerHTML = `
    <article class="space-y-6">
      <header>
        <h1 class="text-2xl font-semibold tracking-tight">Marking Guide</h1>
        <p class="mt-2 text-slate-600">
          A map of the reading moves an advanced reader makes. The goal is not to memorize terms —
          it is to know what question each mark helps you answer.
        </p>
      </header>

      <section class="rounded-lg border border-slate-200 bg-white p-4">
        <h2 class="text-sm font-semibold text-slate-900 mb-2">The big picture</h2>
        <p class="text-sm text-slate-600 mb-3">Almost every reading-analysis question asks one of five things.</p>
        <table class="w-full text-left">
          <tbody>${bigQuestionRows}</tbody>
        </table>
      </section>

      <div class="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm">
        <div class="font-semibold text-emerald-900 mb-2">Most important for MAP 250+</div>
        <ul class="space-y-1 text-emerald-900">${priorityList}</ul>
        <p class="text-xs text-emerald-800 mt-3 italic">The key habit: do not choose the answer that sounds smart. Choose the answer the text proves best.</p>
      </div>

      <section class="space-y-6">
        <h2 class="text-xs uppercase tracking-wide text-slate-500">The five families of reading moves</h2>
        ${familySections}
      </section>

      <section class="rounded-lg border border-slate-200 bg-white p-4">
        <h2 class="text-sm font-semibold text-slate-900 mb-2">Short-code legend</h2>
        <table class="w-full text-left">
          <tbody>${codeRows}</tbody>
        </table>
      </section>

      <div class="rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
        <p class="font-medium text-slate-900 mb-1">How to use this with a real article</p>
        <ol class="list-decimal list-inside space-y-1">
          <li>Read once for understanding — no marks.</li>
          <li>Read again and ask the five big questions.</li>
          <li>Mark only the words that help answer those questions.</li>
          <li>Write three sentences: <strong>main idea</strong>, <strong>author's tone</strong> (specific word), <strong>strongest evidence</strong>.</li>
          <li>Compare with a friend or teacher. The disagreements are where the learning is.</li>
        </ol>
      </div>

      <footer class="pt-4 border-t border-slate-200 flex items-center justify-between text-sm">
        <a href="#/" class="text-slate-700 underline">← Back home</a>
        <a href="#/reference" class="text-slate-700 underline">Quick Reference →</a>
      </footer>
    </article>
  `;
}
