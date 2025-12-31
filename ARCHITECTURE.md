# Hovfaret 13 Prosjektdatabase - Arkitektur

**Sist oppdatert:** 2025-12-12
**Versjon:** 2.83

---

## Hurtigoversikt

```
Hovfaret 13 Prosjektdatabase
├── 59 møter dokumentert
├── 271 dokumenter kategorisert
├── 37 leveranser sporet
├── 23 personer + 16 organisasjoner
├── 37 aktive dashboards
└── Konseptskisse 2.0 (123 sider)
```

---

## 1. Mappestruktur

```
/2.0-Hovfaret13-NewStructureSimplified/
│
├── 📄 Hovedfiler
│   ├── README.md              # Prosjektoversikt
│   ├── STATUS.md              # Gjeldende status (Phase 62)
│   ├── CHANGELOG.md           # Endringshistorikk
│   ├── ARCHITECTURE.md        # Denne filen
│   ├── CLAUDE.md              # AI-instruksjoner
│   ├── QUICKSTART.md          # Kom i gang
│   └── QUICK_ACCESS.md        # Dashboard-lenker
│
├── 📊 dashboard/              # HTML-dashboards (37 aktive)
│   ├── index.html             # Hovednavigasjon
│   ├── lib/                   # JavaScript-bibliotek
│   └── assets/                # Bilder, rapporter
│
├── 💾 data/                   # JSON-datafiler
│   ├── project.json           # Masterprosjekt
│   ├── meetings.json          # 59 møter
│   ├── documents.json         # 271 dokumenter
│   ├── config.json            # Sentralkonfigurasjon
│   ├── stakeholders/          # Personer + organisasjoner
│   └── themes/                # Bærekraft, Omsorg+, etc.
│
├── 📈 analysis/               # Aktive analyser
│   ├── konseptskisse-2.0-analyse.md
│   ├── barekraftsrapport-2.0-analyse.md
│   └── project-integrity-analysis.md
│
├── 🔧 scripts/                # Automatisering (Python/JS)
│
├── 📁 source/                 # Kildemateriale
│   ├── extraction-cache/      # 458 ekstraherte filer
│   └── original-documents/    # Google Drive symlink
│
└── 🗄️ .backups/               # Arkiverte filer
    ├── data/                  # Gamle JSON-backups
    ├── dashboard/             # Gamle HTML-versjoner
    ├── analysis/              # Prosess-output
    └── docs/                  # Gamle dokumenter
```

---

## 2. Datamodell

### Hovedfiler

| Fil | Innhold | Antall | Oppdateres av |
|-----|---------|--------|---------------|
| `project.json` | Bygning, faser, scenarier | - | Manuelt |
| `meetings.json` | Møter med notater | 70 | Scripts + manuelt |
| `documents.json` | Dokumentregister | 271 | Scripts |
| `config.json` | Nøkkeltall | - | Manuelt |
| `deliverables.json` | Leveranser | 75 | Manuelt |

### Stakeholders

| Fil | Innhold | Antall |
|-----|---------|--------|
| `stakeholders/people.json` | Nøkkelpersoner | 22 |
| `stakeholders/organizations.json` | Organisasjoner | 13 |

### Tematiske filer

| Fil | Beskrivelse |
|-----|-------------|
| `themes/sustainability.json` | Energi, klima, CO₂ |
| `themes/omsorg-plus.json` | Eldreboliger (73 enheter) |
| `themes/regulatory.json` | Søknader, regulering |
| `themes/konseptskisse.json` | Presentasjonsinnhold |
| `themes/konseptskisse-2.0-tillegg.json` | Del 5: Progresjon |

---

## 3. Dashboard-oversikt

### Primære dashboards (daglig bruk)

| Dashboard | URL | Beskrivelse |
|-----------|-----|-------------|
| **Hjemmeside** | `/index.html` | Navigasjon til alle dashboards |
| **Oversikt** | `/overview.html` | Prosjekthelse, KPIer |
| **Møter** | `/meetings.html` | 70 møter med notater |
| **Tidslinje** | `/timeline.html` | Kronologisk oversikt |
| **Dokumenter** | `/documents.html` | 271 dokumenter |

### Interessent og analyse

| Dashboard | URL | Beskrivelse |
|-----------|-----|-------------|
| **Interessenter** | `/stakeholders.html` | Personer og organisasjoner |
| **Scenarier** | `/scenarios.html` | 3 utviklingsscenarier |
| **Bærekraft** | `/sustainability.html` | Miljø og klima |
| **Leveranser** | `/deliverables.html` | 75 leveranser |

### Presentasjoner

| Dashboard | URL | Beskrivelse |
|-----------|-----|-------------|
| **Konseptskisse** | `/konseptskisse.html` | Original (99 sider) |
| **Konseptskisse 2.0** | `/konseptskisse-2.html` | + Del 5 (side 100-119) |
| **Prosjekthistorie** | `/project-story.html` | Narrativ fremstilling |
| **Interessentreise** | `/stakeholder-journey.html` | Presentasjonsmodus |

### Rapporter

| Dashboard | URL | Beskrivelse |
|-----------|-----|-------------|
| **Bærekraftsrapport** | `/sustainability-report.html` | 83 sider |
| **Bærekraftsrapport 2.0** | `/barekraftsrapport-2.html` | Arbeidsrom |
| **Regulatorisk** | `/regulatory-status.html` | Søknadsstatus |

---

## 4. Dataflyt

```
┌─────────────────────────────────────────────────────────────┐
│                     KILDER                                   │
├─────────────────────────────────────────────────────────────┤
│  Google Drive  │  Notion  │  Møter  │  Rapporter  │  E-post │
└───────┬────────┴────┬─────┴────┬────┴──────┬──────┴────┬────┘
        │             │          │           │           │
        ▼             ▼          ▼           ▼           ▼
┌─────────────────────────────────────────────────────────────┐
│                   SCRIPTS (scripts/)                         │
│  • parse-meeting-notes.py                                    │
│  • enrich-meetings-with-reports.py                          │
│  • build-enhanced-timeline.js                                │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATA (data/)                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │meetings.json│  │documents.json│  │themes/*.json        │  │
│  │  (70 møter) │  │(271 docs)    │  │(bærekraft, omsorg+) │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          ▼                ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│               JAVASCRIPT LIB (dashboard/lib/)                │
│  ┌───────────────┐  ┌────────────┐  ┌──────────────────┐    │
│  │data-loader.js │→ │renderer.js │→ │*-helpers.js      │    │
│  │(laster JSON)  │  │(HTML)      │  │(transformasjon)  │    │
│  └───────────────┘  └────────────┘  └──────────────────┘    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               DASHBOARDS (dashboard/*.html)                  │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐ ┌──────────────┐  │
│  │index.html│ │meetings  │ │stakeholders│ │konseptskisse │  │
│  │          │ │.html     │ │.html       │ │-2.html       │  │
│  └──────────┘ └──────────┘ └────────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Nøkkeltall (config.json)

| Metrikk | Verdi |
|---------|-------|
| Møter totalt | 70 |
| Dokumenter | 271 |
| Leveranser | 75 |
| Personer | 22 |
| Organisasjoner | 13 |
| Timeline events | 32 |

### Bærekraft

| Metrikk | Verdi |
|---------|-------|
| CO₂-besparelse | 48% |
| Materialbesparelse | 80% |
| Energiforbedring | F → C |

### Omsorg+

| Metrikk | Verdi |
|---------|-------|
| Enheter planlagt | 73 |
| Bydelsbehov | 150-200 |
| Husbanken compliance | 12/12 |

---

## 6. Konseptskisse 2.0 Struktur

```
Konseptskisse 2.0 (123 sider totalt)
│
├── Del 1: Bakgrunn (s. 1-27)
├── Del 2: Stedsutvikling (s. 28-53)
├── Del 3: Konseptskisse 1.0 (s. 54-91)
├── Del 4: Utviklingsstrategi (s. 92-99)
│
└── Del 5: Progresjon (s. 100-123) ← NYE SIDER
    ├── 100: Del 5 Divider
    ├── 101-104: Faglige leveranser
    ├── 105: Interessentdialog
    ├── 106-108: Konsept og analyse
    ├── 109-110: Neste steg + Oppsummering
    ├── 111-114: Natural State metodikk
    ├── 115-119: Prosesser fra møter
    └── 120-123: Benchmark-implementering (nettside, marked, økonomi, medvirkning)
```

---

## 7. Kom i gang

### Vis dashboards lokalt

```bash
cd /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard
python3 -m http.server 8888
# Åpne http://localhost:8888/
```

### Viktige filer å lese først

1. `STATUS.md` - Gjeldende status
2. `QUICK_ACCESS.md` - Dashboard-lenker
3. `data/config.json` - Nøkkeltall

### Oppdatere data

1. Rediger relevant JSON-fil i `data/`
2. Oppdater `config.json` hvis nøkkeltall endres
3. Logg endringen i `CHANGELOG.md`
4. Oppdater `STATUS.md` ved større endringer

---

## 8. Arkivstruktur

Gamle filer flyttes til `.backups/`:

```
.backups/
├── data/           # Gamle meetings.backup.json
├── dashboard/      # Gamle HTML-versjoner
├── analysis/       # Prosess-output
│   └── process-output/  # Store JSON-filer
└── docs/
    ├── sessions/   # SESSION_SUMMARY_*.md
    └── plans/      # Gamle plan-dokumenter
```

---

*Dokumentert: 2025-12-03 | Phase 37*
