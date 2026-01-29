# Hovfaret 13 Project Summary

**Version:** 2.96 | **Phase:** 74 | **Updated:** 2026-01-27

## Quick Reference

```yaml
Auth: h13-skøyen-2025 (24h session)
Config: data/config.json (single source of truth)
Dashboard: 42 pages, all auth-protected
Live: https://justaride.github.io/hovfaret13-database/
```

## Metrics

| Data | Count |
|------|-------|
| Meetings | 61 |
| Documents | 275 |
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
data/meetings.json         # 61 meetings
data/documents.json        # 275 documents
dashboard/lib/utils.js     # Shared utilities
dashboard/lib/data-loader.js  # Data loading with caching
dashboard/css/variables.css   # CSS design tokens
```

## Recent Changes (Phase 73)

1. La til solstudie‑viewer i dashboardet med playback, slider og grafikkjustering.
2. Ny pipeline for PDF → PNG‑frames + manifest (`scripts/build-solstudie-assets.py`).
3. Interpolerte videoer (MP4/WebM) med cinematic grading (`scripts/build-solstudie-video.py`).
4. Manifest oppdatert for auto‑load av video/frames (`dashboard/data/solstudie.json`).
5. Solstudie‑modul lagt til i hoveddashbordet (`dashboard/index.html`).

## Recent Changes (Phase 74)

1. Implementert ny forskningsmodul: **Ørret i Hoffselva** (`dashboard/orret.html`).
2. Strukturert datagrunnlag for ørret-kartlegging, inkludert innspill fra velforening og biologiske funn (`data/themes/orret.json`).
3. Utarbeidet vitenskapelig hypotese for skyggeeffekt på ørret med referanser til internasjonale kilder (USDA, KMAE).
4. Definert konkrete avbøtende tiltak (gytegrus, habitatforbedring) i dashbordet.
5. Lagt til nye sider for Miljøargumentasjon (Teknisk og Dokument) i produksjonsrommet.
