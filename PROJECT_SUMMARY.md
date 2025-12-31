# Hovfaret 13 Project Summary

**Version:** 2.86 | **Phase:** 65 | **Updated:** 2025-12-31

## Quick Reference

```yaml
Auth: h13-skøyen-2025 (24h session)
Config: data/config.json (single source of truth)
Dashboard: 38 pages, all auth-protected
Live: https://justaride.github.io/hovfaret13-database/
```

## Metrics

| Data | Count |
|------|-------|
| Meetings | 60 |
| Documents | 271 |
| People | 23 |
| Organizations | 16 |
| Deliverables | 37 |
| Timeline events | 32 |

## Building

- **Address:** Hovfaret 13, Skøyen, Oslo
- **Built:** 1989
- **Floors:** 5 current (+3 extension = 8 total)
- **Area:** 6,100 m² BTA

## Sustainability

- 48% CO₂ savings vs demolition
- 80% material savings
- 2,549 tonnes CO₂ saved

## Omsorg+ (Elderly Housing)

- 73 planned units
- Covers 46% of district need (160 units)
- Unit sizes: 42-67 m²

## Regulatory

| Process | Status |
|---------|--------|
| Nabovarsel | Complete (2025-10-16) |
| Bruksendring | In progress |
| Rammesøknad | Q1 2026 |

## Key Files

```
data/config.json           # Central config
data/meetings.json         # 60 meetings
data/documents.json        # 271 documents
dashboard/lib/utils.js     # Shared utilities
dashboard/lib/data-loader.js  # Data loading with caching
dashboard/css/variables.css   # CSS design tokens
```

## Recent Changes (Phase 62)

1. Meeting data quality cleanup (70→59 meetings)
2. Removed 6 non-meetings (notes, reports, task lists)
3. Merged 5 duplicate meetings
4. Added meeting types to all 59 meetings (100%)
5. Fixed all corrupt data (locations, titles)
6. Notion sync: 538 records
