// src/loader.js — CSV fetch + parse + validate.
// Stack v0: runs in the browser, no build step. Module 0 schema exception applied.

const VALID_MODULE_IDS = new Set([
  "m0",
  "a1", "a2", "a3", "a4", "a5",
  "b1", "b2", "b3", "b4", "b5", "b6",
  "c1", "c2", "c3",
]);

const VALID_DIFFICULTIES = new Set(["easy", "medium", "hard"]);
const VALID_CHOICES = new Set(["A", "B", "C", "D"]);

const LESSON_COLUMNS = [
  "module_id", "sub_concept_id", "slug", "title", "subtitle",
  "quick_ref", "mini_lesson", "why_it_matters",
  "common_trap_1", "common_trap_2", "common_trap_3",
  "example_1_text", "example_1_answer", "example_1_explanation",
  "example_2_text", "example_2_answer", "example_2_explanation",
  "example_3_text", "example_3_answer", "example_3_explanation",
  "example_4_text", "example_4_answer", "example_4_explanation",
  "example_5_text", "example_5_answer", "example_5_explanation",
];

const QUIZ_COLUMNS = [
  "quiz_id", "question_number", "prompt",
  "choice_a", "choice_b", "choice_c", "choice_d",
  "correct_choice",
  "feedback_a", "feedback_b", "feedback_c", "feedback_d",
  "trap_type", "difficulty",
];

/**
 * Minimal RFC-4180 CSV parser. Handles:
 *   - quoted cells (with embedded commas, newlines, and doubled "")
 *   - unquoted cells
 *   - CRLF or LF line endings
 * Returns array of arrays (rows of cells).
 */
function parseCSV(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];

    if (inQuotes) {
      if (ch === '"') {
        if (text[i + 1] === '"') {
          cell += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        cell += ch;
      }
    } else {
      if (ch === '"') {
        inQuotes = true;
      } else if (ch === ",") {
        row.push(cell);
        cell = "";
      } else if (ch === "\n") {
        row.push(cell);
        rows.push(row);
        row = [];
        cell = "";
      } else if (ch === "\r") {
        // skip; \n on next iter ends the row
      } else {
        cell += ch;
      }
    }
  }
  // tail
  if (cell.length > 0 || row.length > 0) {
    row.push(cell);
    rows.push(row);
  }
  // drop trailing empty row from a final newline
  if (rows.length > 0 && rows[rows.length - 1].every((c) => c === "")) {
    rows.pop();
  }
  return rows;
}

function rowsToObjects(rows, expectedColumns) {
  if (rows.length === 0) throw new Error("empty CSV");
  const header = rows[0];
  if (header.length !== expectedColumns.length || !expectedColumns.every((c, i) => c === header[i])) {
    throw new Error(
      `column mismatch.\n  expected: ${expectedColumns.join(",")}\n  got:      ${header.join(",")}`,
    );
  }
  return rows.slice(1).map((row) =>
    Object.fromEntries(expectedColumns.map((col, i) => [col, row[i] ?? ""])),
  );
}

function validateLesson(lesson, moduleId) {
  if (!VALID_MODULE_IDS.has(moduleId)) {
    throw new Error(`unknown module id: ${moduleId}`);
  }
  if (lesson.module_id !== moduleId) {
    throw new Error(`module_id mismatch: column=${lesson.module_id} path=${moduleId}`);
  }
  for (const col of ["title", "quick_ref", "mini_lesson"]) {
    if (!lesson[col] || lesson[col] === "N/A") {
      throw new Error(`required field '${col}' is empty or N/A`);
    }
  }
  if (lesson.quick_ref.length > 200) {
    throw new Error(`quick_ref exceeds 200 chars: ${lesson.quick_ref.length}`);
  }
  // Module 0 is exempt from common_trap_1 / example_1_* requirements
  if (moduleId !== "m0") {
    if (!lesson.common_trap_1 || lesson.common_trap_1 === "N/A") {
      throw new Error("common_trap_1 is required for non-Module-0 lessons");
    }
    for (const col of ["example_1_text", "example_1_answer", "example_1_explanation"]) {
      if (!lesson[col] || lesson[col] === "N/A") {
        throw new Error(`${col} is required for non-Module-0 lessons`);
      }
    }
  }
}

function validateQuizFile(rows) {
  if (rows.length !== 10) {
    throw new Error(`quiz CSV must have exactly 10 rows, got ${rows.length}`);
  }
  const seenIds = new Set();
  rows.forEach((row, idx) => {
    const qnum = Number(row.question_number);
    if (qnum !== idx + 1) {
      throw new Error(`row ${idx + 1}: question_number must equal row position`);
    }
    if (seenIds.has(row.quiz_id)) {
      throw new Error(`duplicate quiz_id: ${row.quiz_id}`);
    }
    seenIds.add(row.quiz_id);
    if (!VALID_CHOICES.has(row.correct_choice)) {
      throw new Error(`row ${idx + 1}: correct_choice must be A/B/C/D`);
    }
    if (!VALID_DIFFICULTIES.has(row.difficulty)) {
      throw new Error(`row ${idx + 1}: difficulty must be easy/medium/hard`);
    }
    for (const col of [
      "prompt", "choice_a", "choice_b", "choice_c", "choice_d",
      "feedback_a", "feedback_b", "feedback_c", "feedback_d",
    ]) {
      if (!row[col] || row[col] === "N/A") {
        throw new Error(`row ${idx + 1}: required field '${col}' is empty or N/A`);
      }
    }
  });
}

/**
 * Shape returned to UI consumers. Keeps the raw CSV row structure but
 * groups examples into convenient objects.
 *
 * @typedef {object} LessonExample
 * @property {string} text
 * @property {string} answer
 * @property {string} explanation
 *
 * @typedef {object} Lesson
 * @property {string} moduleId
 * @property {string} subConceptId
 * @property {string} slug
 * @property {string} title
 * @property {string} subtitle
 * @property {string} quickRef
 * @property {string} miniLesson
 * @property {string} whyItMatters
 * @property {string[]} commonTraps
 * @property {LessonExample[]} examples
 *
 * @typedef {object} Quiz
 * @property {string} quizId
 * @property {number} questionNumber
 * @property {string} prompt
 * @property {{a: string, b: string, c: string, d: string}} choices
 * @property {"A"|"B"|"C"|"D"} correctChoice
 * @property {{a: string, b: string, c: string, d: string}} feedback
 * @property {string} trapType
 * @property {"easy"|"medium"|"hard"} difficulty
 */

function shapeLesson(row) {
  const examples = [];
  for (let i = 1; i <= 5; i++) {
    const text = row[`example_${i}_text`];
    if (text && text !== "N/A") {
      examples.push({
        text,
        answer: row[`example_${i}_answer`],
        explanation: row[`example_${i}_explanation`],
      });
    }
  }
  const commonTraps = [row.common_trap_1, row.common_trap_2, row.common_trap_3]
    .filter((t) => t && t !== "N/A");
  return {
    moduleId: row.module_id,
    subConceptId: row.sub_concept_id,
    slug: row.slug,
    title: row.title,
    subtitle: row.subtitle === "N/A" ? "" : row.subtitle,
    quickRef: row.quick_ref,
    miniLesson: row.mini_lesson,
    whyItMatters: row.why_it_matters === "N/A" ? "" : row.why_it_matters,
    commonTraps,
    examples,
  };
}

const CHOICE_KEYS = ["a", "b", "c", "d"];

/**
 * Fisher-Yates shuffle on a copy.
 * @template T
 * @param {T[]} items
 * @returns {T[]}
 */
function shuffled(items) {
  const out = items.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

/**
 * Randomize which letter each choice appears under, carrying its feedback with
 * it. Authoring order leaked a strong positional pattern (Q1 was A in 19 of 24
 * packs) and a correct-answer-is-longest tell, so the displayed order is
 * shuffled per load. `correctChoice` is recomputed to the new letter.
 */
function randomizeChoices(row) {
  const sourceOrder = shuffled(CHOICE_KEYS);
  const choices = {};
  const feedback = {};
  let correctChoice = row.correct_choice;

  sourceOrder.forEach((from, i) => {
    const to = CHOICE_KEYS[i];
    choices[to] = row[`choice_${from}`];
    feedback[to] = row[`feedback_${from}`];
    if (from.toUpperCase() === row.correct_choice.toUpperCase()) {
      correctChoice = to.toUpperCase();
    }
  });

  return { choices, feedback, correctChoice };
}

function shapeQuiz(row) {
  const { choices, feedback, correctChoice } = randomizeChoices(row);
  return {
    quizId: row.quiz_id,
    questionNumber: Number(row.question_number),
    prompt: row.prompt,
    choices,
    correctChoice,
    feedback,
    trapType: row.trap_type === "N/A" ? "" : row.trap_type,
    difficulty: row.difficulty,
  };
}

/**
 * Fetch + parse + validate one lesson CSV.
 *
 * @param {string} moduleId  e.g., "b4"
 * @param {string} slug      filename without `NN-` prefix or `.csv`, e.g., "neutral-vs-skeptical"
 * @param {string} fileBasename  the actual filename basename, e.g., "01-neutral-vs-skeptical"
 * @returns {Promise<Lesson>}
 */
export async function loadLesson(moduleId, fileBasename) {
  const url = `content/lessons/${moduleId}/${fileBasename}.csv`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`failed to fetch ${url}: ${resp.status}`);
  const text = await resp.text();
  const rows = rowsToObjects(parseCSV(text), LESSON_COLUMNS);
  if (rows.length !== 1) {
    throw new Error(`${url}: lesson must have exactly 1 data row, got ${rows.length}`);
  }
  validateLesson(rows[0], moduleId);
  return shapeLesson(rows[0]);
}

/**
 * Fetch + parse + validate one quiz CSV (10 rows).
 *
 * @param {string} moduleId
 * @param {string} fileBasename
 * @returns {Promise<Quiz[]>}
 */
export async function loadQuizzes(moduleId, fileBasename) {
  const url = `content/quizzes/${moduleId}/${fileBasename}.csv`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`failed to fetch ${url}: ${resp.status}`);
  const text = await resp.text();
  const rows = rowsToObjects(parseCSV(text), QUIZ_COLUMNS);
  validateQuizFile(rows);
  return rows.map(shapeQuiz);
}

// ───────────────────────────────────────────────────────────────────────────
// Reading Lab — public-domain texts with color-coded annotations.

const LAB_CATEGORIES = new Set(["tone", "evidence", "theme", "inference", "structure"]);
const LAB_DIFFICULTIES = new Set(["Easy", "Medium", "Hard"]);

/**
 * @typedef {object} LabAnnotation
 * @property {number} start
 * @property {number} end
 * @property {"tone"|"evidence"|"theme"|"inference"|"structure"} category
 * @property {string} note
 *
 * @typedef {object} LabText
 * @property {string} id
 * @property {string} title
 * @property {string} author
 * @property {number} year
 * @property {string} sourceUrl
 * @property {"Literary"|"Informational"|"Poetry"|"Fable"} category
 * @property {number} lengthWords
 * @property {string} intro
 * @property {string} passage
 * @property {LabAnnotation[]} annotations
 * @property {string[]} discussionPrompts
 */

function validateLabText(data) {
  for (const f of ["id", "title", "author", "year", "category", "difficulty", "passage", "annotations", "intro", "discussion_prompts"]) {
    if (!(f in data)) throw new Error(`lab text missing required field: ${f}`);
  }
  if (!LAB_DIFFICULTIES.has(data.difficulty)) {
    throw new Error(`lab text difficulty must be Easy/Medium/Hard, got ${data.difficulty}`);
  }
  if (typeof data.passage !== "string" || data.passage.length < 50) {
    throw new Error(`lab text passage too short`);
  }
  if (!Array.isArray(data.annotations)) {
    throw new Error(`lab text annotations must be array`);
  }
  const passageLen = data.passage.length;
  data.annotations.forEach((ann, i) => {
    if (typeof ann.start !== "number" || typeof ann.end !== "number") {
      throw new Error(`annotation #${i + 1} missing start/end`);
    }
    if (ann.start < 0 || ann.end > passageLen || ann.start >= ann.end) {
      throw new Error(`annotation #${i + 1} has invalid offsets [${ann.start}, ${ann.end}] (passage length ${passageLen})`);
    }
    if (!LAB_CATEGORIES.has(ann.category)) {
      throw new Error(`annotation #${i + 1} has unknown category: ${ann.category}`);
    }
    if (typeof ann.note !== "string" || ann.note.length < 10) {
      throw new Error(`annotation #${i + 1} note too short`);
    }
  });
}

/**
 * Shape a raw lab JSON record to camelCase keys for UI consumers.
 */
function shapeLabText(raw) {
  return {
    id: raw.id,
    title: raw.title,
    author: raw.author,
    year: raw.year,
    sourceUrl: raw.source_url || "",
    category: raw.category,
    difficulty: raw.difficulty,
    lengthWords: raw.length_words || 0,
    intro: raw.intro,
    passage: raw.passage,
    annotations: raw.annotations.map((a) => ({
      start: a.start,
      end: a.end,
      category: a.category,
      note: a.note,
    })),
    discussionPrompts: raw.discussion_prompts || [],
    discussionAnswers: raw.discussion_answers || [],
  };
}

/**
 * Fetch + parse + validate one Reading Lab text.
 *
 * @param {string} basename  e.g., "002-gettysburg-address"
 * @returns {Promise<LabText>}
 */
export async function loadLabText(basename) {
  const url = `content/lab/${basename}.json`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`failed to fetch ${url}: ${resp.status}`);
  const data = await resp.json();
  validateLabText(data);
  return shapeLabText(data);
}

// ───────────────────────────────────────────────────────────────────────────
// Reading Library — long-form works (plays, novels, story collections) with
// sparse annotations on famous passages.

function validateLibraryWork(data) {
  for (const f of ["id", "type", "title", "author", "year", "category", "difficulty", "intro", "sections"]) {
    if (!(f in data)) throw new Error(`library work missing required field: ${f}`);
  }
  if (!LAB_DIFFICULTIES.has(data.difficulty)) {
    throw new Error(`library work difficulty must be Easy/Medium/Hard, got ${data.difficulty}`);
  }
  if (!Array.isArray(data.sections) || data.sections.length === 0) {
    throw new Error("library work sections must be a non-empty array");
  }
  data.sections.forEach((sec, i) => {
    for (const f of ["id", "label", "text"]) {
      if (!(f in sec)) throw new Error(`section #${i + 1} missing field: ${f}`);
    }
    if (typeof sec.text !== "string" || sec.text.length < 20) {
      throw new Error(`section #${i + 1} (${sec.id}) text too short`);
    }
    if (sec.annotations) {
      if (!Array.isArray(sec.annotations)) {
        throw new Error(`section #${i + 1} annotations must be array`);
      }
      const len = sec.text.length;
      sec.annotations.forEach((ann, j) => {
        if (ann.start < 0 || ann.end > len || ann.start >= ann.end) {
          throw new Error(`section ${sec.id} annotation #${j + 1} has invalid offsets [${ann.start}, ${ann.end}] (text length ${len})`);
        }
        if (!LAB_CATEGORIES.has(ann.category)) {
          throw new Error(`section ${sec.id} annotation #${j + 1} category ${ann.category} invalid`);
        }
      });
    }
  });
}

function shapeLibraryWork(raw) {
  return {
    id: raw.id,
    type: raw.type,
    title: raw.title,
    author: raw.author,
    year: raw.year,
    sourceUrl: raw.source_url || "",
    category: raw.category,
    difficulty: raw.difficulty,
    lengthWords: raw.length_words || 0,
    intro: raw.intro,
    sections: raw.sections.map((s) => ({
      id: s.id,
      label: s.label,
      subtitle: s.subtitle || "",
      text: s.text,
      annotations: (s.annotations || []).map((a) => ({
        start: a.start,
        end: a.end,
        category: a.category,
        note: a.note,
      })),
    })),
    discussionPrompts: raw.discussion_prompts || [],
    discussionAnswers: raw.discussion_answers || [],
  };
}

/**
 * Fetch + parse + validate one Reading Library work (long-form).
 *
 * @param {string} basename  e.g., "001-macbeth"
 * @returns {Promise<object>}
 */
export async function loadLibraryWork(basename) {
  const url = `content/library/${basename}.json`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`failed to fetch ${url}: ${resp.status}`);
  const data = await resp.json();
  validateLibraryWork(data);
  return shapeLibraryWork(data);
}
