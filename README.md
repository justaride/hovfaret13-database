# Hovfaret 13 Prosjektdatabase v2.94

Komplett prosjektdatabase med interaktivt dashboard for Hovfaret 13 transformasjonsprosjektet.

**Live:** https://justaride.github.io/hovfaret13-database/

## Prosjektoversikt

**Hovfaret 13** er et eiendomstransformasjonsprosjekt på Skøyen i Oslo. Bygningen (bygget 1989) er planlagt for riving under gjeldende områderegulering, men prosjektteamet demonstrerer at rehabilitering/transformasjon er den overlegne tilnærmingen.

**Nøkkelargument:** Bygningen ble strukturelt designet med reservekapasitet for 3 nye etasjer. Transformasjon sparer 48% CO₂-utslipp sammenlignet med riving.

## Nøkkeltall

| Metrikk | Verdi |
|---------|-------|
| Møter | 63 |
| Dokumenter | 327 |
| Leveranser | 37 |
| Personer | 27 |
| Organisasjoner | 19 |
| CO₂-besparelse | 48% |
| Omsorg+ enheter | 73 |

## Kom i gang

```bash
cd /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard
python3 -m http.server 8888
open http://localhost:8888/index.html
```

## Kvalitetssjekk før push

Kjør metrikk-konsistenskontroll før commit/push:

```bash
node scripts/check-metrics-consistency.js
```

Sjekken validerer at nøkkeltall i:
- `README.md`
- `QUICKSTART.md`
- `dashboard/lib/page-config.js`
- `dashboard/index.html`

matcher `data/config.json` og faktiske datafiler.

CI/Deploy:
- Workflow `Metrics Consistency` kjører på PR/push mot `main`.
- `Deploy to GitHub Pages` stopper hvis sjekken feiler.

## Dashboards

| Dashboard | Fil | Beskrivelse |
|-----------|-----|-------------|
| Hjemmeside | `index.html` | Navigasjon til alle dashboards |
| Oversikt | `overview.html` | Prosjekthelse og KPIer |
| Møter | `meetings.html` | 63 møter med notater |
| Tidslinje | `timeline.html` | Kronologisk oversikt |
| Dokumenter | `documents.html` | 327 dokumenter |
| Interessenter | `stakeholders.html` | 27 personer, 19 organisasjoner |
| Scenarier | `scenarios.html` | 3 utviklingsscenarier |
| Bærekraft | `sustainability.html` | Miljø og klima |
| Konseptskisse 2.0 | `konseptskisse-2.html` | 123 sider presentasjon |

## Datastruktur

```
data/
├── project.json              # Masterprosjekt
├── meetings.json             # 63 møter
├── documents.json            # 327 dokumenter
├── config.json               # Sentralkonfigurasjon
├── deliverables.json         # 37 leveranser
├── timeline.json             # Tidslinje
├── stakeholders/
│   ├── organizations.json    # 19 organisasjoner
│   └── people.json           # 27 personer
└── themes/
    ├── sustainability.json   # Energi, klima, sirkulært
    ├── regulatory.json       # Søknader, regulering
    ├── omsorg-plus.json      # Eldreboliger (73 enheter)
    └── konseptskisse-2.0-tillegg.json  # Del 5: Progresjon
```

## Dokumentasjon

| Fil | Beskrivelse |
|-----|-------------|
| `README.md` | Denne filen |
| `STATUS.md` | Gjeldende status (Phase 65) |
| `CHANGELOG.md` | Endringshistorikk |
| `ARCHITECTURE.md` | Komplett prosjektarkitektur |
| `QUICKSTART.md` | Hurtigstart-guide |
| `QUICK_ACCESS.md` | Dashboard-lenker |

## Hovedinteressenter

### Prosjektteam
- **Urbania Eiendom AS** - Eier (Andreas Thorsnes)
- **Natural State AS** - Prosjektkoordinering, bærekraft (Gabriel Bøen, Einar Holthe)
- **R21 Arkitekter** - Arkitektur (Thomas Thorsen)

### Konsulenter
- **Vill Energi** - Energi/klimaanalyse (Trym Osborg)
- **Byggesaksrådgivning AS** - Ansvarlig søker

### Myndigheter
- **Oslo Kommune** - Reguleringsmyndighet
- **Bydel Ullern** - Omsorg+ partner (150-200 enheter behov)

## Konseptskisse 2.0

```
Konseptskisse 2.0 (123 sider)
├── Del 1: Bakgrunn (s. 1-27)
├── Del 2: Stedsutvikling (s. 28-53)
├── Del 3: Konseptskisse 1.0 (s. 54-91)
├── Del 4: Utviklingsstrategi (s. 92-99)
└── Del 5: Progresjon (s. 100-123) ← 24 NYE SIDER
    ├── 100-119: Leveranser, metodikk, prosesser
    ├── 120: Nettside & Digital (hovfaret13.no)
    ├── 121: Markedsinnsikt (Bydel Ullern)
    ├── 122: Stedsøkonomi (arealregnskap)
    └── 123: Medvirkningsdokumentasjon
```

---

*Opprettet: 2025-11-21*
*Sist oppdatert: 2026-01-26 (v2.94 - Phase 72: Analyse av Lokale Bevis)*
