# CLAUDE.md - Project Instructions for Claude Code

## Project: Hovfaret 13 Data Consolidation v2.90

Real estate transformation project database. Version 2.90, Phase 68.

**Auth:** Password `h13-skøyen-2025` (24h localStorage session)

## Key Files

| Priority | File               | Purpose                                  |
| -------- | ------------------ | ---------------------------------------- |
| 1        | `data/config.json` | Single source of truth for all metrics   |
| 2        | `STATUS.md`        | Current progress, blockers, next actions |
| 3        | `CHANGELOG.md`     | Session history                          |

## Current Metrics (from config.json)

| Data             | Count                              |
| ---------------- | ---------------------------------- |
| Meetings         | 60                                 |
| Documents        | 271                                |
| People           | 23                                 |
| Organizations    | 16                                 |
| Deliverables     | 37 (verifisert)                    |
| Timeline events  | 32 (10 strategic + 22 operational) |
| Dashboard pages  | 39 (all auth-protected)            |
| Project duration | 21 months                          |
| Notion databases | 12                                 |
| Notion records   | 538                                |

## Project Structure

```
data/
├── config.json           # Central config - single source of truth
├── project.json          # Building, phases, scenarios
├── timeline.json         # Multi-layer timeline (strategic/operational)
├── meetings.json         # 60 meetings with summaries/outcomes
├── documents.json        # 271 documents categorized
├── stakeholders/
│   ├── organizations.json (16 orgs)
│   └── people.json       (23 people)
└── themes/
    ├── sustainability.json
    ├── regulatory.json
    ├── omsorg-plus.json
    └── utleie.json

dashboard/
├── auth.js               # Reusable auth module
├── index.html            # Main entry point
└── *.html                # 38 pages total
```

## Working Principles

1. **Data-first** - All content lives in JSON files, dashboard consumes them
2. **Single source of truth** - Don't duplicate data across files
3. **Iterative dashboard** - Build one component at a time, verify before next
4. **Norwegian context** - Project is in Oslo, many terms are Norwegian

## Data Boundary Rules

**Project Data** vs **Deliverable Content** are strictly separated:

| Type                    | Files                                                                                                           | Rule                                                              |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Project Data**        | meetings.json, timeline.json, stakeholders/, deliverables.json, config.json                                     | Immutable project history - never modified by deliverable updates |
| **Deliverable Content** | themes/konseptskisse\*.json, themes/barekraftsrapport.json, themes/sustainability.json, themes/omsorg-plus.json | Extracted content from presentations/reports                      |
| **Process Data**        | themes/sustainability-journey.json, themes/regulatory.json                                                      | Project process records (flagged as project_data)                 |

### Content Classification

All theme files have `metadata.content_classification`:

```json
"content_classification": {
  "type": "deliverable_content",  // or "project_data"
  "deliverable_id": "d_025",       // null for project_data
  "deliverable_version": "2.0",
  "source_document": "Document name",
  "is_primary_source": false
}
```

### Rules for New Deliverables

When creating content for a new deliverable (e.g., Konseptskisse 3.0):

1. **Create new theme file** - `themes/konseptskisse-3.0.json`
2. **Add content_classification** - type: `deliverable_content`, link to deliverable ID
3. **Update deliverables.json** - add `theme_content_files` reference
4. **Never modify project data** - meetings, timeline, stakeholders stay unchanged
5. **Update config.json reference** - point `konseptskisse_ref.current_version` to new version

## Notion Sync

```bash
cd notion-sync
npm run sync        # Full sync to Notion
npm run sync:dry    # Preview changes
```

12 databases synced:

- Organizations (16), People (23), Meetings (60), Documents (271)
- Timeline (32), Deliverables (37), Sustainability (3)
- Omsorg+ Concept (1), Floors (7), Units (73), Facilities (11), Compliance (5)

## Source Data Locations

- **Extraction cache**: `source/extraction-cache/` (458 extracted docs)
- **Original documents**: `source/original-documents/` (Google Drive)
- **Previous database**: `/Users/gabrielboen/h13-project-database/`

## When Updating Data

1. Update the relevant JSON file
2. Log the change in CHANGELOG.md
3. Update STATUS.md if it affects current tasks

## Key Context

- **Building**: Hovfaret 13, Skøyen, Oslo - built 1989, 5 floors (+3 extension capacity = 8)
- **Area**: 6,100 m² BTA / 5,800 m² BRA
- **Challenge**: Area plan requires demolition, project argues for transformation
- **Main argument**: 48% CO₂ savings, 80% material savings with rehabilitation
- **Preferred scenario**: Omsorg+ (73 elderly housing units) with 3-floor extension
- **District need**: 160 Omsorg+ units by 2040 (H13 covers 46%)

## Regulatory Status

| Process             | Status         | Date           |
| ------------------- | -------------- | -------------- |
| Nabovarsel          | ✅ Complete    | 2025-10-16     |
| Bruksendringssøknad | 🔄 In progress | Target Q4 2025 |
| Rammesøknad         | ⏳ Not started | Target Q1 2026 |

## Quality Checklist

- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Norwegian names preserved (ø, æ, å)
- [ ] Sources referenced
- [ ] Cross-references use consistent IDs
- [ ] Metrics match config.json
