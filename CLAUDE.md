# CLAUDE.md - Project Instructions for Claude Code

## Project: Hovfaret 13 Data Consolidation v2.0

This is a real estate transformation project database. When working on this project, always read `STATUS.md` first to understand current state.

## Key Files to Read on Session Start

1. **STATUS.md** - Current progress, blockers, next actions
2. **CHANGELOG.md** - What was done in previous sessions
3. **data/project.json** - Master project context

## Project Structure

```
data/
├── project.json          # Building, phases, scenarios
├── timeline.json         # Multi-layer timeline (strategic/operational)
├── meetings.json         # 37 meetings
├── documents.json        # 271 documents categorized
├── stakeholders/
│   ├── organizations.json
│   └── people.json
└── themes/
    ├── sustainability.json
    ├── regulatory.json
    └── omsorg-plus.json
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

- **Building**: Hovfaret 13, Skøyen, Oslo - built 1989, 5 floors (designed for 12)
- **Challenge**: Area plan requires demolition, project argues for transformation
- **Main argument**: 48% lower CO₂ with rehabilitation vs demolition
- **Preferred scenario**: Omsorg+ (elderly housing) with 3-floor extension

## Quality Checklist for Data

- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Norwegian names preserved correctly (ø, æ, å)
- [ ] Sources referenced where possible
- [ ] Cross-references use consistent IDs
