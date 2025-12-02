# Hovfaret 13 Project Database v2.28

Komplett prosjektdatabase med interaktivt dashboard for Hovfaret 13 transformasjonsprosjektet.

## Project Overview

**Hovfaret 13** er et eiendomstransformasjonsprosjekt på Skøyen i Oslo. Bygningen (bygget 1989) er planlagt for riving under gjeldende områdereguleringer, men prosjektteamet jobber for å demonstrere at rehabilitering/transformasjon er den overlegne tilnærmingen fra bærekraft, sosiale og økonomiske perspektiver.

**Nøkkelargument:** Bygningen ble strukturelt designet for 12 etasjer, men bare 5 ble bygget. Transformasjon sparer 48% CO₂-utslipp sammenlignet med riving.

## Dashboard

Start dashboardet:
```bash
cd dashboard
python3 -m http.server 8888
# Åpne http://localhost:8888/index.html
```

### Tilgjengelige sider
| Side | Beskrivelse |
|------|-------------|
| `index.html` | Hjemmeside med navigasjonskort |
| `meetings.html` | 65 møter med master-detail layout |
| `timeline.html` | Prosjekttidslinje |
| `stakeholders.html` | 22 personer, 13 organisasjoner |
| `documents.html` | 271 dokumenter |
| `scenarios.html` | 3 utviklingsscenarier |
| `sustainability.html` | Bærekraftsrapport |
| `analytics.html` | Prosjektanalyse |
| `overview.html` | Prosjektoversikt |

## Data Structure

```
data/
├── project.json              # Master project file (building, phases, scenarios)
├── timeline.json             # Multi-layer timeline (strategic/operational/detailed)
├── meetings.json             # 65 meetings with participants and reports
├── documents.json            # 271 document registry with categories
├── stakeholders/
│   ├── organizations.json    # 13 organizations (owner, consultants, government)
│   └── people.json           # 22 people with roles and engagement
└── themes/
    ├── sustainability.json   # Energy, climate, circular economy data
    ├── regulatory.json       # Planning status, permits, strategy
    └── omsorg-plus.json      # Elderly housing concept details
```

## Timeline Layers

1. **Strategic** (10 events) - For board/investor presentations
2. **Operational** (22 events) - For project management
3. **Detailed** - Links to meetings.json (65 meetings)

## Key Stakeholders

### Core Project Team
- **Urbania Eiendom AS** - Property owner (Andreas Thorsnes)
- **Natural State AS** - Project coordination, sustainability (Gabriel Bøen, Einar Holthe)
- **R21 Arkitekter** - Architecture (Thomas Thorsen)

### Key Consultants
- **Vill Energi** - Energy/climate analysis (Trym Osborg)
- **Byggekonsulent** - Technical building advice

### Government
- **Oslo Kommune** - Regulatory authority
- **Bydel Ullern** - Potential Omsorg+ partner

## Source Data

The `source/` folder contains symlinks to:
- `extraction-cache/` - 458 extracted document files from original processing
- `original-documents/` - Google Drive folder with 349 source files

## Usage

This data is designed to be:
1. **Read by Claude Code** for generating reports, analysis, updates
2. **Consumed by a future dashboard** (to be built iteratively)
3. **Version controlled in Git** as single source of truth

### Example Queries

```bash
# Get project status
cat data/project.json | jq '.project.status'

# List strategic timeline events
cat data/timeline.json | jq '.events.strategic[].title'

# Find meetings with Bydel Ullern
cat data/meetings.json | jq '.meetings[] | select(.title | contains("Bydel"))'

# Get all people from Natural State
cat data/stakeholders/people.json | jq '.people | to_entries[] | select(.value.organization == "Natural State AS") | .value.name'
```

## Migration from v1

This structure consolidates data from `/Users/gabrielboen/h13-project-database/` which had:
- Multiple overlapping JSON files
- Uncurated timeline with document-date noise
- 12+ dashboard pages (too fragmented)

v2.0 provides:
- Single source of truth per entity type
- Curated, multi-layer timeline
- Simplified structure for iterative dashboard development

---

*Opprettet: 2025-11-21*
*Sist oppdatert: 2025-12-02 (v2.28 - Dashboard Redesign)*
*Kilde: h13-project-database + Google Drive H13 Backup*
