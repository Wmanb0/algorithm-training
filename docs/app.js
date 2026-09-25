"use strict";

const state = {
  problems: [],
  topics: new Map(),
  topicChildren: new Map(),
  selectedProblem: null,
  ratingPlatform: "",
  charts: new Map(),
};

const elements = {};

function byId(id) {
  return document.getElementById(id);
}

function platformLabel(value) {
  return { codeforces: "Codeforces", leetcode: "LeetCode", atcoder: "AtCoder" }[value]
    || value.split("-").map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join(" ");
}

function problemLevel(problem) {
  return problem.level_label || problem.difficulty_label || "—";
}

function problemRating(problem) {
  if (problem.rating != null) return Number(problem.rating);
  const meta = problem.platform_meta || {};
  const value = problem.platform === "atcoder" ? meta.difficulty_rating : meta.rating;
  return value == null ? null : Number(value);
}

function ratingSystem(problem) {
  if (problem.rating_system) return problem.rating_system;
  if (problem.platform === "codeforces") return "codeforces";
  if (problem.platform === "atcoder") return "atcoder-problems";
  return null;
}

function ratingDisplay(problem) {
  const rating = problemRating(problem);
  if (rating == null) return "—";
  if (ratingSystem(problem) === "codeforces") return `CF ${rating}`;
  if (ratingSystem(problem) === "atcoder-problems") return `AtCoder ≈${rating}`;
  return String(rating);
}

function ratingSourceLabel(problem) {
  const source = problem.rating_source || problem.platform_meta?.rating_source;
  if (problem.platform === "codeforces") {
    return source === "manual" ? "Manually specified Codeforces rating" : "Official Codeforces rating";
  }
  if (problem.platform === "atcoder") {
    return source === "manual"
      ? "Manually specified AtCoder difficulty estimate"
      : "Difficulty estimated by AtCoder Problems";
  }
  return "Platform-specific rating";
}

function latestAttempt(problem) {
  return [...(problem.attempts || [])].sort((a, b) => b.date.localeCompare(a.date))[0] || null;
}

function toLocalISO(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function shiftDate(iso, amount) {
  const [year, month, day] = iso.split("-").map(Number);
  const value = new Date(year, month - 1, day);
  value.setDate(value.getDate() + amount);
  return toLocalISO(value);
}

function streaks(problems) {
  const dates = [...new Set(problems.flatMap((problem) => (problem.attempts || []).map((item) => item.date)))].sort();
  if (!dates.length) return { current: 0, longest: 0, days: 0 };
  let longest = 1;
  let run = 1;
  for (let index = 1; index < dates.length; index += 1) {
    run = dates[index] === shiftDate(dates[index - 1], 1) ? run + 1 : 1;
    longest = Math.max(longest, run);
  }
  const today = toLocalISO(new Date());
  const mostRecent = dates[dates.length - 1];
  let current = 0;
  if (mostRecent === today || mostRecent === shiftDate(today, -1)) {
    current = 1;
    for (let index = dates.length - 1; index > 0; index -= 1) {
      if (dates[index - 1] !== shiftDate(dates[index], -1)) break;
      current += 1;
    }
  }
  return { current, longest, days: dates.length };
}

function countBy(values) {
  const counts = new Map();
  values.forEach((value) => counts.set(value, (counts.get(value) || 0) + 1));
  return counts;
}

const chartColors = [
  "#2563eb", "#14b8a6", "#8b5cf6", "#f59e0b", "#ec4899",
  "#22c55e", "#06b6d4", "#f97316", "#6366f1", "#84cc16",
];

function sortedCounts(values, limit = Number.POSITIVE_INFINITY) {
  return [...countBy(values).entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0])))
    .slice(0, limit);
}

function matchingAttempts(problems) {
  const from = elements.dateFrom.value;
  const to = elements.dateTo.value;
  return problems.flatMap((problem) => (problem.attempts || []).filter((attempt) => (
    (!from || attempt.date >= from) && (!to || attempt.date <= to)
  )));
}

function chartOptions(extra = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    interaction: { intersect: false, mode: "nearest" },
    plugins: {
      legend: {
        position: "bottom",
        labels: { color: "#475569", boxWidth: 11, boxHeight: 11, padding: 14, usePointStyle: true },
      },
      tooltip: {
        backgroundColor: "#172033",
        titleColor: "#ffffff",
        bodyColor: "#ffffff",
        padding: 10,
        cornerRadius: 7,
      },
    },
    ...extra,
  };
}

function drawChart(name, config, hasData) {
  const canvas = elements[`${name}Chart`];
  const empty = elements[`${name}ChartEmpty`];
  const previous = state.charts.get(name);
  if (previous) previous.destroy();
  state.charts.delete(name);
  canvas.hidden = !hasData;
  empty.hidden = hasData;
  if (!hasData || !window.Chart) {
    if (!window.Chart && hasData) {
      canvas.hidden = true;
      empty.hidden = false;
      empty.textContent = "Chart library could not be loaded";
    }
    return;
  }
  empty.textContent = `No matching ${name} data`;
  state.charts.set(name, new window.Chart(canvas, config));
}

function renderAnalytics(problems) {
  const attempts = matchingAttempts(problems);

  const activity = [...countBy(attempts.map((attempt) => attempt.date)).entries()]
    .sort((a, b) => a[0].localeCompare(b[0]));
  drawChart("activity", {
    type: "line",
    data: {
      labels: activity.map(([date]) => date),
      datasets: [{
        label: "Attempts",
        data: activity.map(([, count]) => count),
        borderColor: "#2563eb",
        backgroundColor: "rgba(37, 99, 235, 0.12)",
        borderWidth: 2,
        pointBackgroundColor: "#2563eb",
        pointRadius: 3,
        pointHoverRadius: 5,
        tension: 0.28,
        fill: true,
      }],
    },
    options: chartOptions({
      plugins: { ...chartOptions().plugins, legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#64748b", maxRotation: 0, autoSkip: true, maxTicksLimit: 12 } },
        y: { beginAtZero: true, grid: { color: "#edf2f7" }, ticks: { color: "#64748b", precision: 0 } },
      },
    }),
  }, activity.length > 0);

  const platforms = sortedCounts(problems.map((problem) => problem.platform));
  drawChart("platform", {
    type: "doughnut",
    data: {
      labels: platforms.map(([platform]) => platformLabel(platform)),
      datasets: [{
        data: platforms.map(([, count]) => count),
        backgroundColor: chartColors.slice(0, platforms.length),
        borderColor: "#ffffff",
        borderWidth: 3,
        hoverOffset: 5,
      }],
    },
    options: chartOptions({ cutout: "64%" }),
  }, platforms.length > 0);

  const languages = sortedCounts(attempts.map((attempt) => attempt.language || "Unknown"));
  drawChart("language", {
    type: "doughnut",
    data: {
      labels: languages.map(([language]) => language),
      datasets: [{
        data: languages.map(([, count]) => count),
        backgroundColor: chartColors.slice(0, languages.length),
        borderColor: "#ffffff",
        borderWidth: 3,
        hoverOffset: 5,
      }],
    },
    options: chartOptions({ cutout: "64%" }),
  }, languages.length > 0);

  const topics = sortedCounts(
    problems.map((problem) => problem.primary_topic || problem.topics?.[0]).filter(Boolean),
    10,
  );
  drawChart("topic", {
    type: "bar",
    data: {
      labels: topics.map(([topic]) => state.topics.get(topic)?.name || topic),
      datasets: [{
        label: "Problems",
        data: topics.map(([, count]) => count),
        backgroundColor: topics.map((_, index) => `${chartColors[index % chartColors.length]}cc`),
        borderColor: topics.map((_, index) => chartColors[index % chartColors.length]),
        borderWidth: 1,
        borderRadius: 5,
      }],
    },
    options: chartOptions({
      indexAxis: "y",
      plugins: { ...chartOptions().plugins, legend: { display: false } },
      scales: {
        x: { beginAtZero: true, grid: { color: "#edf2f7" }, ticks: { color: "#64748b", precision: 0 } },
        y: { grid: { display: false }, ticks: { color: "#475569" } },
      },
    }),
  }, topics.length > 0);
}

function option(select, value, label) {
  const item = document.createElement("option");
  item.value = value;
  item.textContent = label;
  select.append(item);
}

function fillSelect(select, values, labeler = (value) => value) {
  const first = select.firstElementChild;
  select.replaceChildren(first);
  [...values].sort((a, b) => labeler(a).localeCompare(labeler(b))).forEach((value) => {
    option(select, value, labeler(value));
  });
}

function topicDepth(topic) {
  return Math.max(0, (topic.path || []).length - 1);
}

function populateFilters() {
  fillSelect(elements.platformFilter, new Set(state.problems.map((item) => item.platform)), platformLabel);

  const usedTopics = new Set();
  state.problems.forEach((problem) => {
    Object.values(problem.topic_paths || {}).forEach((path) => path.forEach((id) => usedTopics.add(id)));
  });
  const selectable = [...state.topics.values()].filter((topic) => usedTopics.has(topic.id));
  const first = elements.topicFilter.firstElementChild;
  elements.topicFilter.replaceChildren(first);
  selectable
    .sort((a, b) => a.path.join("/").localeCompare(b.path.join("/")))
    .forEach((topic) => option(elements.topicFilter, topic.id, `${"· ".repeat(topicDepth(topic))}${topic.name}`));

  const divisions = new Set(
    state.problems.filter((item) => item.platform === "codeforces")
      .flatMap((item) => item.platform_meta?.divisions || []),
  );
  fillSelect(elements.divisionFilter, divisions, (value) => value.replace("div", "Div."));
  refreshDifficultyOptions();
}

function refreshDifficultyOptions() {
  const selected = elements.platformFilter.value;
  const ratingSupported = selected === "codeforces" || selected === "atcoder";
  if (state.ratingPlatform !== selected) {
    elements.ratingMin.value = "";
    elements.ratingMax.value = "";
    if (elements.sortSelect.value.startsWith("rating-")) elements.sortSelect.value = "recent";
    state.ratingPlatform = selected;
  }
  const values = new Set(
    state.problems
      .filter((problem) => !selected || problem.platform === selected)
      .map(problemLevel)
      .filter((value) => value && value !== "—"),
  );
  const previous = elements.difficultyFilter.value;
  fillSelect(elements.difficultyFilter, values);
  if (values.has(previous)) elements.difficultyFilter.value = previous;
  const isCodeforces = selected === "codeforces";
  elements.codeforcesFilters.hidden = !isCodeforces;
  if (!isCodeforces) elements.divisionFilter.value = "";
  elements.ratingFilters.hidden = !ratingSupported;
  [elements.ratingSortAsc, elements.ratingSortDesc].forEach((item) => {
    item.hidden = !ratingSupported;
    item.disabled = !ratingSupported;
  });
  if (selected === "codeforces") {
    elements.ratingMinLabel.textContent = "Min Codeforces rating";
    elements.ratingMaxLabel.textContent = "Max Codeforces rating";
    elements.ratingMin.placeholder = "800";
    elements.ratingMax.placeholder = "3500";
  } else if (selected === "atcoder") {
    elements.ratingMinLabel.textContent = "Min AtCoder estimate";
    elements.ratingMaxLabel.textContent = "Max AtCoder estimate";
    elements.ratingMin.placeholder = "0";
    elements.ratingMax.placeholder = "4000";
  }
}

function renderStats() {
  const attempts = state.problems.reduce((total, problem) => total + (problem.attempts || []).length, 0);
  const streak = streaks(state.problems);
  elements.problemCount.textContent = String(state.problems.length);
  elements.attemptCount.textContent = String(attempts);
  elements.dayCount.textContent = String(streak.days);
  elements.currentStreak.textContent = String(streak.current);
  elements.longestStreak.textContent = String(streak.longest);

  const platforms = countBy(state.problems.map((problem) => problem.platform));
  elements.platformTotal.textContent = String(platforms.size);
  renderCountList(elements.platformCounts, platforms, platformLabel, (value) => {
    elements.platformFilter.value = value;
    refreshDifficultyOptions();
    renderProblems();
  });

  const topics = countBy(state.problems.flatMap((problem) => [...new Set(problem.topics || [])]));
  elements.topicTotal.textContent = String(topics.size);
  renderCountList(
    elements.topicCounts,
    new Map([...topics].sort((a, b) => b[1] - a[1])),
    (value) => state.topics.get(value)?.name || value,
    (value) => {
      elements.topicFilter.value = value;
      renderProblems();
    },
  );
}

function renderCountList(container, counts, labeler, onSelect) {
  container.replaceChildren();
  [...counts.entries()].sort((a, b) => b[1] - a[1] || labeler(a[0]).localeCompare(labeler(b[0]))).forEach(([value, count]) => {
    const row = document.createElement("div");
    row.className = "count-row";
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = labeler(value);
    button.addEventListener("click", () => onSelect(value));
    const number = document.createElement("strong");
    number.textContent = String(count);
    row.append(button, number);
    container.append(row);
  });
  if (!counts.size) container.textContent = "No data";
}

function searchableText(problem) {
  const topicNames = (problem.topics || []).map((id) => state.topics.get(id)?.name || id);
  const notes = (problem.attempts || []).map((attempt) => attempt.note || "");
  return [
    problem.title, problem.problem_id, problem.platform, problemLevel(problem),
    ratingDisplay(problem), ...topicNames, ...notes,
  ].join(" ").toLowerCase();
}

function matchesTopic(problem, selected) {
  if (!selected) return true;
  if ((problem.topics || []).includes(selected)) return true;
  return Object.values(problem.topic_paths || {}).some((path) => path.includes(selected));
}

function filteredProblems() {
  const query = elements.searchInput.value.trim().toLowerCase();
  const platform = elements.platformFilter.value;
  const topic = elements.topicFilter.value;
  const difficulty = elements.difficultyFilter.value;
  const division = elements.divisionFilter.value;
  const min = Number(elements.ratingMin.value || 0);
  const max = Number(elements.ratingMax.value || Number.POSITIVE_INFINITY);
  const ratingSupported = platform === "codeforces" || platform === "atcoder";
  const hasRatingFilter = ratingSupported && Boolean(elements.ratingMin.value || elements.ratingMax.value);
  const from = elements.dateFrom.value;
  const to = elements.dateTo.value;

  const result = state.problems.filter((problem) => {
    const attemptDates = (problem.attempts || []).map((attempt) => attempt.date);
    const inDateRange = attemptDates.some((date) => (!from || date >= from) && (!to || date <= to));
    const meta = problem.platform_meta || {};
    const rating = problemRating(problem);
    return (!query || searchableText(problem).includes(query))
      && (!platform || problem.platform === platform)
      && matchesTopic(problem, topic)
      && (!difficulty || problemLevel(problem) === difficulty)
      && (!division || (meta.divisions || []).includes(division))
      && (!hasRatingFilter || (rating != null && rating >= min && rating <= max))
      && (!from && !to || inDateRange);
  });

  const sort = elements.sortSelect.value;
  return result.sort((a, b) => {
    if (sort === "oldest") return (latestAttempt(a)?.date || "").localeCompare(latestAttempt(b)?.date || "");
    if (sort === "title") return a.title.localeCompare(b.title);
    if (sort === "platform") return a.platform.localeCompare(b.platform) || a.title.localeCompare(b.title);
    if (sort === "rating-asc" || sort === "rating-desc") {
      const aRating = problemRating(a);
      const bRating = problemRating(b);
      if (aRating == null && bRating == null) return a.title.localeCompare(b.title);
      if (aRating == null) return 1;
      if (bRating == null) return -1;
      return sort === "rating-asc" ? aRating - bRating : bRating - aRating;
    }
    return (latestAttempt(b)?.date || "").localeCompare(latestAttempt(a)?.date || "");
  });
}

function makePills(problem) {
  const list = document.createElement("div");
  list.className = "pill-list";
  (problem.topics || []).forEach((topicId) => {
    const pill = document.createElement("span");
    pill.className = `pill${topicId === problem.primary_topic ? " primary" : ""}`;
    pill.textContent = state.topics.get(topicId)?.name || topicId;
    list.append(pill);
  });
  return list;
}

function renderProblems() {
  const problems = filteredProblems();
  elements.resultCount.textContent = String(problems.length);
  elements.problemRows.replaceChildren();
  elements.emptyState.hidden = problems.length > 0;
  renderAnalytics(problems);

  problems.forEach((problem) => {
    const row = document.createElement("tr");
    const titleCell = document.createElement("td");
    titleCell.className = "problem-cell";
    const link = document.createElement("a");
    link.href = problem.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = problem.title;
    const id = document.createElement("span");
    id.className = "problem-id";
    id.textContent = problem.problem_id;
    titleCell.append(link, id);

    const platform = document.createElement("td");
    platform.textContent = platformLabel(problem.platform);
    const level = document.createElement("td");
    level.textContent = problemLevel(problem);
    const rating = document.createElement("td");
    const ratingValue = problemRating(problem);
    rating.textContent = ratingDisplay(problem);
    if (ratingValue != null) rating.title = ratingSourceLabel(problem);
    const topics = document.createElement("td");
    topics.append(makePills(problem));
    const trained = document.createElement("td");
    trained.textContent = latestAttempt(problem)?.date || "—";
    const action = document.createElement("td");
    const button = document.createElement("button");
    button.className = "details-button";
    button.type = "button";
    button.textContent = "View";
    button.addEventListener("click", () => openProblem(problem));
    action.append(button);
    row.append(titleCell, platform, level, rating, topics, trained, action);
    elements.problemRows.append(row);
  });
}

function renderAttempt(problem, index) {
  const attempts = [...(problem.attempts || [])].sort((a, b) => b.date.localeCompare(a.date));
  const attempt = attempts[index];
  elements.dialogNote.textContent = attempt?.note || "No notes for this attempt.";
  elements.dialogCode.removeAttribute("data-highlighted");
  const languageClass = {
    "C": "c",
    "C++": "cpp",
    "Python": "python",
    "Java": "java",
    "Kotlin": "kotlin",
    "Rust": "rust",
    "Go": "go",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
  }[attempt?.language] || "plaintext";
  elements.dialogCode.className = `language-${languageClass}`;
  elements.dialogCode.textContent = attempt?.code || "Source file not available in the generated data.";
  elements.codeLanguage.textContent = attempt?.language || "";
  if (window.hljs) window.hljs.highlightElement(elements.dialogCode);
}

function openProblem(problem) {
  state.selectedProblem = problem;
  elements.dialogPlatform.textContent = platformLabel(problem.platform);
  elements.dialogTitle.textContent = problem.title;
  elements.dialogProblemLink.href = problem.url;
  elements.dialogMeta.replaceChildren();

  const level = problemLevel(problem);
  if (level !== "—") {
    const pill = document.createElement("span");
    pill.className = "pill";
    pill.textContent = level;
    elements.dialogMeta.append(pill);
  }
  const rating = problemRating(problem);
  if (rating != null) {
    const pill = document.createElement("span");
    pill.className = "pill rating";
    pill.textContent = ratingDisplay(problem);
    pill.title = ratingSourceLabel(problem);
    elements.dialogMeta.append(pill);
  }
  (problem.topics || []).forEach((topicId) => {
    const pill = document.createElement("span");
    pill.className = `pill${topicId === problem.primary_topic ? " primary" : ""}`;
    pill.textContent = state.topics.get(topicId)?.name || topicId;
    elements.dialogMeta.append(pill);
  });

  const attempts = [...(problem.attempts || [])].sort((a, b) => b.date.localeCompare(a.date));
  elements.attemptSelect.replaceChildren();
  attempts.forEach((attempt, index) => option(elements.attemptSelect, String(index), `${attempt.date} · ${attempt.language}`));
  renderAttempt(problem, 0);
  elements.problemDialog.showModal();
}

function resetFilters() {
  [elements.searchInput, elements.dateFrom, elements.dateTo, elements.ratingMin, elements.ratingMax].forEach((input) => { input.value = ""; });
  [elements.platformFilter, elements.topicFilter, elements.difficultyFilter, elements.divisionFilter].forEach((select) => { select.value = ""; });
  elements.sortSelect.value = "recent";
  refreshDifficultyOptions();
  renderProblems();
}

function bindEvents() {
  [
    elements.searchInput, elements.topicFilter, elements.difficultyFilter, elements.dateFrom,
    elements.dateTo, elements.divisionFilter, elements.ratingMin, elements.ratingMax, elements.sortSelect,
  ].forEach((control) => control.addEventListener("input", renderProblems));
  elements.platformFilter.addEventListener("change", () => {
    refreshDifficultyOptions();
    renderProblems();
  });
  elements.resetFilters.addEventListener("click", resetFilters);
  elements.closeDialog.addEventListener("click", () => elements.problemDialog.close());
  elements.problemDialog.addEventListener("click", (event) => {
    if (event.target === elements.problemDialog) elements.problemDialog.close();
  });
  elements.attemptSelect.addEventListener("change", () => renderAttempt(state.selectedProblem, Number(elements.attemptSelect.value)));
  elements.copyCode.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(elements.dialogCode.textContent);
      elements.copyCode.textContent = "Copied";
      window.setTimeout(() => { elements.copyCode.textContent = "Copy code"; }, 1200);
    } catch {
      elements.copyCode.textContent = "Copy failed";
    }
  });
}

async function initialize() {
  [
    "problemCount", "attemptCount", "dayCount", "currentStreak", "longestStreak",
    "platformFilter", "topicFilter", "difficultyFilter", "dateFrom", "dateTo",
    "divisionFilter", "ratingMin", "ratingMax", "codeforcesFilters", "ratingFilters",
    "ratingMinLabel", "ratingMaxLabel", "ratingSortAsc", "ratingSortDesc", "searchInput",
    "resetFilters", "sortSelect", "resultCount", "problemRows", "emptyState",
    "platformCounts", "topicCounts", "platformTotal", "topicTotal", "problemDialog",
    "dialogPlatform", "dialogTitle", "dialogMeta", "dialogProblemLink", "attemptSelect",
    "dialogNote", "dialogCode", "codeLanguage", "closeDialog", "copyCode", "loadError",
    "activityChart", "activityChartEmpty", "platformChart", "platformChartEmpty",
    "languageChart", "languageChartEmpty", "topicChart", "topicChartEmpty",
  ].forEach((id) => { elements[id] = byId(id); });

  bindEvents();
  try {
    const [problemResponse, taxonomyResponse] = await Promise.all([
      fetch("./data/problems.json", { cache: "no-store" }),
      fetch("./data/taxonomy.json", { cache: "no-store" }),
    ]);
    if (!problemResponse.ok || !taxonomyResponse.ok) throw new Error("Data request failed");
    const problemData = await problemResponse.json();
    const taxonomyData = await taxonomyResponse.json();
    state.problems = problemData.problems || [];
    (taxonomyData.topics || []).forEach((topic) => state.topics.set(topic.id, topic));
    populateFilters();
    renderStats();
    renderProblems();
  } catch (error) {
    console.error(error);
    elements.loadError.hidden = false;
  }
}

document.addEventListener("DOMContentLoaded", initialize);
