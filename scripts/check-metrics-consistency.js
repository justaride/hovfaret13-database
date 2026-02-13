#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");

function readFile(relPath) {
  return fs.readFileSync(path.join(root, relPath), "utf8");
}

function readJson(relPath) {
  return JSON.parse(readFile(relPath));
}

function toInt(value) {
  const n = Number.parseInt(value, 10);
  return Number.isFinite(n) ? n : null;
}

function firstNumberMatch(text, regex) {
  const match = text.match(regex);
  if (!match) return null;
  return toInt(match[1]);
}

function multiNumberMatch(text, regex) {
  const match = text.match(regex);
  if (!match) return null;
  return match.slice(1).map(toInt);
}

const issues = [];

function pushMismatch(file, label, expected, actual) {
  if (expected !== actual) {
    issues.push({
      type: "mismatch",
      file,
      label,
      expected,
      actual,
    });
  }
}

function pushMissing(file, label) {
  issues.push({
    type: "missing_pattern",
    file,
    label,
  });
}

function checkSingle(text, file, label, regex, expected) {
  const actual = firstNumberMatch(text, regex);
  if (actual === null) {
    pushMissing(file, label);
    return;
  }
  pushMismatch(file, label, expected, actual);
}

function checkMulti(text, file, label, regex, expected) {
  const actual = multiNumberMatch(text, regex);
  if (!actual || actual.some((v) => v === null)) {
    pushMissing(file, label);
    return;
  }
  if (expected.length !== actual.length) {
    issues.push({
      type: "length_mismatch",
      file,
      label,
      expected,
      actual,
    });
    return;
  }
  for (let i = 0; i < expected.length; i += 1) {
    pushMismatch(file, `${label} [${i}]`, expected[i], actual[i]);
  }
}

function loadExpectedMetrics() {
  const config = readJson("data/config.json");
  const metrics = config.metrics || {};
  const stakeholders = metrics.stakeholders || {};
  return {
    meetings: toInt(metrics.meetings_total),
    documents: toInt(metrics.documents_total),
    deliverables: toInt(metrics.deliverables_total),
    people: toInt(stakeholders.people),
    organizations: toInt(stakeholders.organizations),
  };
}

function loadActualMetrics() {
  const meetings = readJson("data/meetings.json");
  const documents = readJson("data/documents.json");
  const deliverables = readJson("data/deliverables.json");
  const people = readJson("data/stakeholders/people.json");
  const organizations = readJson("data/stakeholders/organizations.json");

  return {
    meetings: Array.isArray(meetings.meetings) ? meetings.meetings.length : null,
    documents: Array.isArray(documents.documents)
      ? documents.documents.length
      : null,
    deliverables: Array.isArray(deliverables.deliverables)
      ? deliverables.deliverables.length
      : null,
    people:
      people.people && typeof people.people === "object"
        ? Object.keys(people.people).length
        : null,
    organizations:
      organizations.organizations && typeof organizations.organizations === "object"
        ? Object.keys(organizations.organizations).length
        : null,
  };
}

function run() {
  const expected = loadExpectedMetrics();
  const actual = loadActualMetrics();

  // Validate config metrics against data files first.
  pushMismatch(
    "data/config.json",
    "metrics.meetings_total",
    actual.meetings,
    expected.meetings,
  );
  pushMismatch(
    "data/config.json",
    "metrics.documents_total",
    actual.documents,
    expected.documents,
  );
  pushMismatch(
    "data/config.json",
    "metrics.deliverables_total",
    actual.deliverables,
    expected.deliverables,
  );
  pushMismatch(
    "data/config.json",
    "metrics.stakeholders.people",
    actual.people,
    expected.people,
  );
  pushMismatch(
    "data/config.json",
    "metrics.stakeholders.organizations",
    actual.organizations,
    expected.organizations,
  );

  const readme = readFile("README.md");
  checkSingle(
    readme,
    "README.md",
    "Nøkkeltall Møter",
    /\|\s*Møter\s*\|\s*(\d+)\s*\|/i,
    expected.meetings,
  );
  checkSingle(
    readme,
    "README.md",
    "Nøkkeltall Dokumenter",
    /\|\s*Dokumenter\s*\|\s*(\d+)\s*\|/i,
    expected.documents,
  );
  checkSingle(
    readme,
    "README.md",
    "Nøkkeltall Leveranser",
    /\|\s*Leveranser\s*\|\s*(\d+)\s*\|/i,
    expected.deliverables,
  );
  checkSingle(
    readme,
    "README.md",
    "Nøkkeltall Personer",
    /\|\s*Personer\s*\|\s*(\d+)\s*\|/i,
    expected.people,
  );
  checkSingle(
    readme,
    "README.md",
    "Nøkkeltall Organisasjoner",
    /\|\s*Organisasjoner\s*\|\s*(\d+)\s*\|/i,
    expected.organizations,
  );

  const quickstart = readFile("QUICKSTART.md");
  checkSingle(
    quickstart,
    "QUICKSTART.md",
    "Nøkkeltall Møter",
    /\|\s*Møter\s*\|\s*(\d+)\s*\|/i,
    expected.meetings,
  );
  checkSingle(
    quickstart,
    "QUICKSTART.md",
    "Nøkkeltall Dokumenter",
    /\|\s*Dokumenter\s*\|\s*(\d+)\s*\|/i,
    expected.documents,
  );
  checkSingle(
    quickstart,
    "QUICKSTART.md",
    "Nøkkeltall Leveranser",
    /\|\s*Leveranser\s*\|\s*(\d+)\s*\|/i,
    expected.deliverables,
  );
  checkSingle(
    quickstart,
    "QUICKSTART.md",
    "Nøkkeltall Personer",
    /\|\s*Personer\s*\|\s*(\d+)\s*\|/i,
    expected.people,
  );
  checkSingle(
    quickstart,
    "QUICKSTART.md",
    "Nøkkeltall Organisasjoner",
    /\|\s*Organisasjoner\s*\|\s*(\d+)\s*\|/i,
    expected.organizations,
  );

  const pageConfig = readFile("dashboard/lib/page-config.js");
  checkSingle(
    pageConfig,
    "dashboard/lib/page-config.js",
    "meetings desc",
    /id:\s*"meetings"[\s\S]*?desc:\s*"(\d+)\s+møter/i,
    expected.meetings,
  );
  checkSingle(
    pageConfig,
    "dashboard/lib/page-config.js",
    "documents desc",
    /id:\s*"documents"[\s\S]*?desc:\s*"(\d+)\s+dokumenter/i,
    expected.documents,
  );
  checkMulti(
    pageConfig,
    "dashboard/lib/page-config.js",
    "stakeholders desc",
    /id:\s*"stakeholders"[\s\S]*?desc:\s*"(\d+)\s+personer,\s*(\d+)\s+org/i,
    [expected.people, expected.organizations],
  );

  const indexHtml = readFile("dashboard/index.html");
  checkSingle(
    indexHtml,
    "dashboard/index.html",
    "tab header meetings",
    /<span class="tab-stat-value">(\d+)<\/span>\s*<span class="tab-stat-label">Møter<\/span>/i,
    expected.meetings,
  );
  checkSingle(
    indexHtml,
    "dashboard/index.html",
    "tab header documents",
    /<span class="tab-stat-value">(\d+)<\/span>\s*<span class="tab-stat-label">Dokumenter<\/span>/i,
    expected.documents,
  );
  checkMulti(
    indexHtml,
    "dashboard/index.html",
    "moduleData meetings stats",
    /meetings:\s*{[\s\S]*?stats:\s*\[[\s\S]*?\{ value: "(\d+)", label: "Møter" \}[\s\S]*?\{ value: "(\d+)", label: "Deltakere" \}[\s\S]*?\{ value: "(\d+)", label: "Org" \}/m,
    [expected.meetings, expected.people, expected.organizations],
  );
  checkMulti(
    indexHtml,
    "dashboard/index.html",
    "moduleData stakeholders stats",
    /stakeholders:\s*{[\s\S]*?stats:\s*\[[\s\S]*?\{ value: "(\d+)", label: "Personer" \}[\s\S]*?\{ value: "(\d+)", label: "Org" \}/m,
    [expected.people, expected.organizations],
  );

  if (issues.length === 0) {
    console.log("Metrics consistency check passed.");
    console.log(
      `Expected/actual: meetings=${expected.meetings}, documents=${expected.documents}, deliverables=${expected.deliverables}, people=${expected.people}, organizations=${expected.organizations}`,
    );
    return;
  }

  console.error(`Metrics consistency check failed with ${issues.length} issue(s):`);
  for (const issue of issues) {
    if (issue.type === "missing_pattern") {
      console.error(`- [MISSING] ${issue.file} :: ${issue.label}`);
      continue;
    }
    if (issue.type === "length_mismatch") {
      console.error(
        `- [LENGTH] ${issue.file} :: ${issue.label} expected=${JSON.stringify(issue.expected)} actual=${JSON.stringify(issue.actual)}`,
      );
      continue;
    }
    console.error(
      `- [MISMATCH] ${issue.file} :: ${issue.label} expected=${issue.expected} actual=${issue.actual}`,
    );
  }
  process.exitCode = 1;
}

run();
