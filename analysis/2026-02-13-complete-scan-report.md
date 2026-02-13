# Complete Project Scan Report

Date: 2026-02-13  
Scope: full repo audit (`dashboard/`, `data/`, `scripts/`, `notion-sync/`, key docs)  
Method: static checks + browser smoke + schema contract validation

## Coverage Summary

- JSON validation: `30/30` files parsed successfully under `data/`.
- Dashboard runtime pages scanned: `52` pages (all `44` configured routes + `7` orphan pages + `index`).
- HTTP status scan: `52/52` pages returned `200`.
- Data-route existence scan for explicit `fetch("*.json")` callsites: no missing files.
- Navigation integrity:
  - Configured page targets in `dashboard/lib/page-config.js` all exist.
  - Orphan HTML pages not reachable from `page-config`: `7` files.

## Source-of-Truth Metrics (from data files)

- Meetings: `62` (`data/meetings.json`)
- Documents: `278` (`data/documents.json`)
- Deliverables: `37` (`data/deliverables.json`)
- People: `27` (`data/stakeholders/people.json`)
- Organizations: `19` (`data/stakeholders/organizations.json`)

These match `data/config.json:32`-`data/config.json:38`.

## Findings (Severity Ordered)

### 1) High: Overview dashboard renders `undefined` for Organizations

- Evidence:
  - `dashboard/overview.html:693` initializes `organizations` as `data.organizations || []`.
  - `dashboard/overview.html:808` renders `${organizations.length}`.
  - `data.organizations` is an object map, not an array.
  - Browser validation on `overview.html` rendered stat values including `\"undefined\"` for label `\"Organisasjoner\"`.
- Impact:
  - End users see incorrect KPI output on core overview page.
  - Undermines trust in dashboard metrics.
- Root cause:
  - Data-shape mismatch (object map consumed as array).
- Fix plan:
  1. Normalize `data.organizations` to array before render (`DataLoader.getOrganizationsArray(...)` or `Object.values(...)`).
  2. Add defensive fallback for non-array/non-object values.
  3. Add smoke assertion that `#stats-grid` contains numeric value for `Organisasjoner`.

### 2) High: Deliverables page fails person lookup and falls back to raw IDs

- Evidence:
  - `dashboard/deliverables.html:1208` uses `(peopleData.people || []).forEach(...)`.
  - `peopleData.people` is an object map in `data/stakeholders/people.json`, so `.forEach` is invalid.
  - Exception is swallowed and logged at `dashboard/deliverables.html:1212` as `Could not load people data`.
  - UI then falls back to raw ID via `dashboard/deliverables.html:1028`.
  - Browser validation showed chip text like `thomas_thorsen` instead of formatted person name.
- Impact:
  - Responsible-person display quality is degraded.
  - People enrichment data is effectively unused on this page.
- Root cause:
  - Same object-vs-array schema mismatch as above.
- Fix plan:
  1. Convert to array before iterating: `Object.values(peopleData.people || {})`.
  2. Keep console warning only for real fetch/parse failures, not schema mismatch.
  3. Add regression check: first deliverable responsible chip resolves to human-readable name.

### 3) High: Solstudie page CSP blocks inline boot script, removing global header injection

- Evidence:
  - CSP in `dashboard/solstudie.html:7` allows `script-src 'self'` only.
  - Inline script at `dashboard/solstudie.html:31` calls `ContentHeader.inject(\"solstudie\")`.
  - Browser console reports CSP violation on this script.
  - Runtime validation confirms `.tab-header` is absent on `solstudie.html`.
- Impact:
  - Navigation/header consistency is broken on this page.
  - UX parity with rest of dashboard is lost.
- Root cause:
  - CSP policy disallows the page's own inline initializer.
- Fix plan:
  1. Move inline initializer to external JS file, or
  2. Introduce nonce/hash CSP strategy and apply it consistently.
  3. Add runtime check that `.tab-header` exists on `solstudie.html`.

### 4) Medium: Widespread metrics drift between docs/UI copy and actual data

- Evidence:
  - Truth: `62` meetings, `278` documents, `27` people, `19` orgs (`data/config.json:32`-`data/config.json:38`).
  - Stale values in docs/UI:
    - `README.md:17`-`README.md:21` (61/271/23/16)
    - `QUICKSTART.md:48`-`QUICKSTART.md:52` (60/271/23/16)
    - `dashboard/lib/page-config.js:22`, `dashboard/lib/page-config.js:28`, `dashboard/lib/page-config.js:73`
    - `dashboard/index.html:479`, `dashboard/index.html:483`, `dashboard/index.html:582`, `dashboard/index.html:600`, `dashboard/index.html:601`
- Impact:
  - Core navigation and onboarding docs present contradictory project facts.
  - Creates avoidable confusion during stakeholder communication.
- Root cause:
  - Manual hardcoded counts not linked to data source.
- Fix plan:
  1. Replace hardcoded headline counts with values loaded from `data/config.json`.
  2. If some pages are historical snapshots, label them explicitly with “as of <date>”.
  3. Add consistency check script comparing docs/UI key counts vs `data/config.json`.

### 5) Medium: DataLoader public contract is inconsistent for stakeholder shapes

- Evidence:
  - `DataLoader.loadAllData()` returns `people: people.people` and `organizations: organizations.organizations` (`dashboard/lib/data-loader.js:236`-`dashboard/lib/data-loader.js:237`), i.e. object maps.
  - Same module also has many methods that require arrays (`filterPeople`, `groupPeopleByCategory`, `getPersonCategories`, etc.) and one search path directly calling `data.people.forEach` (`dashboard/lib/data-loader.js:370`).
  - Some pages explicitly normalize, some do not.
- Impact:
  - Easy to introduce silent defects when new pages consume `loadAllData()` directly.
- Root cause:
  - Unclear/unstable shape contract at DataLoader boundary.
- Fix plan:
  1. Define canonical return types for `loadAllData()` and enforce them (prefer arrays at UI boundary).
  2. Keep raw object maps only in explicit low-level loaders if needed.
  3. Add type-guard utilities and schema tests for `people`/`organizations`.

### 6) Low: Documentation path/version drift and navigation discoverability gaps

- Evidence:
  - Local start path in docs is stale for current workspace:
    - `README.md:28`
    - `QUICKSTART.md:8`
  - Version metadata mismatch:
    - `README.md:1` shows `v2.94`
    - `QUICKSTART.md:1` shows `v2.86` and footer `2.49` at `QUICKSTART.md:103`.
  - Orphan pages not linked from `page-config`:
    - `dialogmote-2-rapport.html`
    - `dialogmote-2026-01-29.html`
    - `moete-2025-12-19.html`
    - `status-december-2025-light.html`
    - `status-december-2025-minimal.html`
    - `sustainability-report-full.html`
    - `sustainability.html`
- Impact:
  - New contributors may run wrong startup path and miss available pages.
- Fix plan:
  1. Update docs paths and version tags in one sweep.
  2. Decide which orphan pages should be linked vs archived.
  3. Add doc freshness check in release workflow.

## Exclusions / Non-Issues

- `dashboard/nabomerknader.html` throws `access denied` without token (`dashboard/nabomerknader.html:1237`): treated as intentional access-control behavior, not a defect.

## Recommended Regression Checks (after fixes)

1. `overview.html` shows numeric organization count (not `undefined`).
2. `deliverables.html` logs no `Could not load people data` warning and renders person names from `people.json`.
3. `solstudie.html` loads with no CSP script error and displays `.tab-header`.
4. Key counts in docs/navigation match `data/config.json`.
5. Full browser smoke over all configured pages remains free of unhandled errors.
