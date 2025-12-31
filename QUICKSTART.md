# Hurtigstart - Hovfaret 13 Dashboard v2.86

**Live på GitHub Pages:** https://justaride.github.io/hovfaret13-database/

## Start dashboardet lokalt

```bash
cd /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard
python3 -m http.server 8888
open http://localhost:8888/index.html
```

## Hovedsider

| Side | URL | Beskrivelse |
|------|-----|-------------|
| Hjemmeside | http://localhost:8888/index.html | Hovednavigasjon |
| Oversikt | http://localhost:8888/overview.html | Prosjekthelse, KPIer |
| Møter | http://localhost:8888/meetings.html | 60 møter med notater |
| Tidslinje | http://localhost:8888/timeline.html | Kronologisk oversikt |
| Dokumenter | http://localhost:8888/documents.html | 271 dokumenter |
| Interessenter | http://localhost:8888/stakeholders.html | 23 personer, 16 org |
| Scenarier | http://localhost:8888/scenarios.html | CO₂-analyse |
| Bærekraft | http://localhost:8888/sustainability.html | Miljødata |

## Presentasjoner

| Side | URL | Beskrivelse |
|------|-----|-------------|
| Konseptskisse | http://localhost:8888/konseptskisse.html | Original (99 s.) |
| Konseptskisse 2.0 | http://localhost:8888/konseptskisse-2.html | + Del 5 (s. 100-123) |
| Prosjekthistorie | http://localhost:8888/project-story.html | Narrativ |
| Interessentreise | http://localhost:8888/stakeholder-journey.html | Presentasjon |

## Rapporter

| Side | URL | Beskrivelse |
|------|-----|-------------|
| Bærekraftsrapport | http://localhost:8888/sustainability-report.html | 83 sider |
| Bærekraftsrapport 2.0 | http://localhost:8888/barekraftsrapport-2.html | Arbeidsrom |
| Regulatorisk | http://localhost:8888/regulatory-status.html | Søknadsstatus |
| Leveranser | http://localhost:8888/deliverables.html | 37 leveranser |

## Nøkkeltall

| Metrikk | Verdi |
|---------|-------|
| Møter | 60 |
| Dokumenter | 271 |
| Leveranser | 37 |
| Personer | 23 |
| Organisasjoner | 16 |
| CO₂-besparelse | 48% |
| Omsorg+ enheter | 73 |
| Bydelsbehov | 150-200 |

## Tema-velger

Alle dashboards har tema-bytte i navigasjonen:
- **Technical Dark** - Mørkest
- **Technical Dusk** - Standard (anbefalt)
- **Technical Twilight** - Lysere
- **Technical Day** - Lysest

## Mappestruktur

```
/2.0-Hovfaret13-NewStructureSimplified/
├── dashboard/         # 36 HTML-dashboards
├── data/              # JSON-datafiler
│   ├── meetings.json
│   ├── documents.json
│   ├── stakeholders/
│   └── themes/
├── analysis/          # Analyser
├── scripts/           # Automatisering
└── .backups/          # Arkiverte filer
```

## Viktige filer

| Fil | Formål |
|-----|--------|
| `STATUS.md` | Gjeldende status |
| `ARCHITECTURE.md` | Prosjektarkitektur |
| `data/config.json` | Nøkkeltall |

## Feilsøking

**Problem:** Filer laster ikke (404)
```bash
# Sjekk at du er i dashboard-mappen
cd dashboard
python3 -m http.server 8888
```

**Problem:** Gammel versjon vises
- Mac: `Cmd + Shift + R` (hard refresh)
- Windows: `Ctrl + Shift + F5`

---

**Versjon:** 2.49
**Oppdatert:** 2025-12-03
