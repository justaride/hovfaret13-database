# CLAUDE.md - Project Instructions for Claude Code

## Project: Hovfaret 13 Data Consolidation v2.80

Real estate transformation project database. Version 2.80, Phase 58.

**Auth:** Password `h13-skøyen-2025` (24h localStorage session)

## Key Files

| Priority | File | Purpose |
|----------|------|---------|
| 1 | `data/config.json` | Single source of truth for all metrics |
| 2 | `STATUS.md` | Current progress, blockers, next actions |
| 3 | `CHANGELOG.md` | Session history |

## Current Metrics (from config.json)

| Data | Count |
|------|-------|
| Meetings | 70 |
| Documents | 271 |
| People | 23 |
| Organizations | 16 |
| Deliverables | 37 |
| Timeline events | 39 (12 strategic + 27 operational) |
| Dashboard pages | 37 (all auth-protected) |
| Project duration | 21 months |

## Project Structure

```
data/
├── config.json           # Central config - single source of truth
├── project.json          # Building, phases, scenarios
├── timeline.json         # Multi-layer timeline (strategic/operational)
├── meetings.json         # 70 meetings with summaries/outcomes
├── documents.json        # 271 documents categorized
├── stakeholders/
│   ├── organizations.json (16 orgs)
│   └── people.json       (23 people)
└── themes/
    ├── sustainability.json
    ├── regulatory.json
    └── omsorg-plus.json

dashboard/
├── auth.js               # Reusable auth module
├── index.html            # Main entry point
└── *.html                # 37 pages total
```

## Working Principles

1. **Data-first** - All content lives in JSON files, dashboard consumes them
2. **Single source of truth** - Don't duplicate data across files
3. **Iterative dashboard** - Build one component at a time, verify before next
4. **Norwegian context** - Project is in Oslo, many terms are Norwegian

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

| Process | Status | Date |
|---------|--------|------|
| Nabovarsel | ✅ Complete | 2025-10-16 |
| Bruksendringssøknad | 🔄 In progress | Target Q4 2025 |
| Rammesøknad | ⏳ Not started | Target Q1 2026 |

## Quality Checklist

- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Norwegian names preserved (ø, æ, å)
- [ ] Sources referenced
- [ ] Cross-references use consistent IDs
- [ ] Metrics match config.json
