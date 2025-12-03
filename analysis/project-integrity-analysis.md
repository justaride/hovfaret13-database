# Prosjekt Integritetsanalyse
## Hovfaret 13 Prosjektdatabase v2.38

**Analysedato:** 2025-12-03
**Analysert av:** Claude Code

---

## 1. IDENTIFISERTE FEIL OG INKONSISTENSER

### 1.1 Kritiske Faktafeil

#### A) CO₂-besparelse Inkonsistens
| Lokasjon | Verdi | Status |
|----------|-------|--------|
| `project.json` linje 66 | "28% lower CO₂" | ❌ FEIL |
| Alle andre kilder | "48% lower CO₂" | ✅ Riktig |

**Problem:** `project.json` sier "28% lower CO₂ emissions vs demolition/rebuild" mens alle andre filer (klimagassrapport, dashboard, konseptskisse) sier 48%.

**Kilde:** Klimagassberegninger Hovfaret 13 v2 (22.04.2025) bekrefter 48%.

#### B) Møtetall Inkonsistens
| Fil | Verdi | Kommentar |
|-----|-------|-----------|
| `project.json` | 47 meetings | ❌ Utdatert |
| `meetings.json` | 69 meetings | ✅ Faktisk |
| `timeline-enhanced.json` metadata | 12 strategic, 22 operational | Operasjonell er 27 faktisk |
| `timeline.json` metadata | 10 strategic events | ❌ Utdatert (er 12) |

#### C) Omsorg+ Enheter Inkonsistens
| Kilde | Antall |
|-------|--------|
| Nabolagsmøte-notat | "ca. 70 enheter" |
| Konseptskisse | "73 enheter" |
| Omsorg-plus.json | "70-100 enheter", "48+25 enheter" |

**Anbefaling:** Standardiser til 73 enheter (fra R21 tegninger).

### 1.2 Utdaterte Metadata

| Fil | Felt | Nåværende | Burde være |
|-----|------|-----------|------------|
| `project.json` | last_updated | 2025-11-21 | 2025-12-03 |
| `project.json` | meetings_tracked | 47 | 69 |
| `project.json` | extracted_documents_count | 307 | 271 (documents.json) |
| `timeline-enhanced.json` | last_updated | 2025-11-21 | 2025-12-03 |
| `timeline-enhanced.json` | operational event_count | 22 | 27 |
| `deliverables.json` | total_deliverables | 75 | Verifiser |
| `people.json` | last_meeting dates | 2025-09-04 | 2025-10-14 |

### 1.3 Manglende Koblinger (Orphaned Data)

1. **Nabolagsmøte 14/10/2025** - Ikke koblet til alle relevante filer
2. **Strategimøte 5/9/2025** - Mangler i timeline-enhanced.json som strategisk event
3. **Nabovarsel 16/10/2025** - Ny hendelse, trenger kobling

---

## 2. DATA-AVHENGIGHETER (DEPENDENCIES)

### 2.1 Sentraliserte Tall som MÅ Synkroniseres

```
┌─────────────────────────────────────────────────────────────┐
│                    MASTER DATA POINTS                        │
├─────────────────────────────────────────────────────────────┤
│  Møter: 69          → project.json, timeline-enhanced.json, │
│                        konseptskisse-2.html, index.html      │
│                                                              │
│  CO₂-besparelse: 48% → project.json, sustainability.html,   │
│                        konseptskisse-2.html, alle dashboards │
│                                                              │
│  Omsorg+ enheter: 73 → omsorg-plus.json, konseptskisse.json,│
│                        scenarios.html, index.html            │
│                                                              │
│  Dokumenter: 271     → project.json, documents.html          │
│                                                              │
│  Leveranser: 75      → deliverables.json, overview.html     │
│                                                              │
│  Strategiske events: 12 → timeline-enhanced.json            │
│  Operasjonelle events: 27 → timeline-enhanced.json          │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Fil-til-Fil Avhengigheter

```
project.json (MASTER)
    ├── phases → timeline-enhanced.json
    ├── scenarios → scenarios.html, sustainability.html
    ├── key_dates → timeline-enhanced.json, konseptskisse.json
    └── data_sources.meetings_tracked → meetings.json (COUNT)

meetings.json (69 møter)
    ├── → timeline-enhanced.json (linked_meetings)
    ├── → deliverables.json (linked_meetings)
    ├── → stakeholders/people.json (total_meetings per person)
    └── → stakeholders/organizations.json (total_meetings)

timeline-enhanced.json
    ├── strategic events → timeline.html, project-story.html
    ├── operational events → timeline.html
    └── linked_meetings → meetings.json

deliverables.json (75 leveranser)
    ├── → konseptskisse-2.html (tall)
    ├── → overview.html
    └── linked_timeline_events → timeline-enhanced.json

stakeholders/people.json
    ├── → stakeholders.html
    ├── total_meetings → UTDATERT (ikke synkronisert med meetings.json)
    └── last_meeting → UTDATERT

sustainability-journey.json (17 events)
    ├── → sustainability.html sidebar
    └── linked_meetings → meetings.json
```

### 2.3 Dashboard-til-Data Koblinger

| Dashboard | Bruker data fra |
|-----------|-----------------|
| index.html | project.json, meetings.json (count), inline stats |
| meetings.html | meetings.json |
| timeline.html | timeline-enhanced.json |
| sustainability.html | inline data, sustainability-journey.json |
| stakeholders.html | stakeholders/*.json |
| documents.html | documents.json |
| scenarios.html | project.json scenarios |
| konseptskisse-2.html | konseptskisse-2.0-tillegg.json (delvis inline) |
| overview.html | Aggregert fra flere kilder |

---

## 3. ANBEFALTE STRUKTURELLE FORBEDRINGER

### 3.1 Opprett Sentral Konfigurasjon

**Ny fil:** `data/config.json`
```json
{
  "metrics": {
    "meetings_total": 69,
    "documents_total": 271,
    "deliverables_total": 75,
    "strategic_events": 12,
    "operational_events": 27,
    "co2_savings_percent": 48,
    "material_savings_percent": 80,
    "omsorg_plus_units": 73,
    "building_area_m2": 6100
  },
  "dates": {
    "project_start": "2024-03-11",
    "energy_report": "2025-04-11",
    "climate_report": "2025-04-22",
    "sustainability_report": "2025-07-04",
    "strategic_shift": "2025-09-05",
    "neighborhood_meeting": "2025-10-14",
    "neighbor_notice": "2025-10-16"
  },
  "status": {
    "nabovarsel": "completed",
    "bruksendringssoknad": "in_progress",
    "rammesoknad": "not_started"
  },
  "last_updated": "2025-12-03"
}
```

### 3.2 Manglende Data-Elementer

| Element | Status | Prioritet |
|---------|--------|-----------|
| Bydelsutvalgsmøte 29/10/2025 | Ikke i meetings.json | Høy |
| NCE søknad status | Fragmentert | Medium |
| Bank/finansiering status | Ikke strukturert | Medium |
| Arkitekttegninger referanser | Delvis | Lav |

### 3.3 Dashboards som Mangler

1. **Deliverables Dashboard** - `deliverables.html`
   - Viser 75 leveranser med status
   - Gantt-lignende tidslinje
   - Filtrering per kategori

2. **Regulatory Status Dashboard** - `regulatory.html`
   - Søknadsstatus med tidslinje
   - PBE-prosess visualisering
   - Neste steg-oversikt

3. **Financial Overview** - Ikke planlagt, men relevant

---

## 4. PRIORITERT HANDLINGSPLAN

### Fase 1: Kritiske Fikser (Umiddelbart)

- [ ] Fiks CO₂ "28%" → "48%" i project.json
- [ ] Oppdater meetings_tracked: 47 → 69 i project.json
- [ ] Oppdater timeline-enhanced.json event_count metadata
- [ ] Synkroniser people.json total_meetings med faktiske tall

### Fase 2: Data-Synkronisering (Kort sikt)

- [ ] Opprett `data/config.json` som sentral sannhetskilde
- [ ] Oppdater dashboards til å lese fra config.json
- [ ] Legg til manglende møter (bydelsutvalgsmøte etc.)
- [ ] Oppdater stakeholder engagement-tall

### Fase 3: Strukturelle Forbedringer (Medium sikt)

- [ ] Opprett deliverables.html dashboard
- [ ] Forbedre cross-referencing mellom JSON-filer
- [ ] Automatisert validering av data-integritet
- [ ] Dokumenter alle data-dependencies

---

## 5. DATAKVALITET SCORE

| Kategori | Score | Kommentar |
|----------|-------|-----------|
| Møtedata | 8/10 | Komplett, men metadata utdatert |
| Timeline | 7/10 | Mangler noen nyere events |
| Stakeholders | 6/10 | Engagement-tall utdatert |
| Deliverables | 8/10 | God struktur, trenger dashboard |
| Bærekraft | 9/10 | Godt dokumentert |
| Regulatorisk | 7/10 | Mangler dedikert oversikt |
| Cross-referencing | 5/10 | Fragmentert, mange orphans |

**Total Score: 7.1/10**

---

## 6. KONKLUSJON

Prosjektdatabasen har god grunnstruktur, men lider av:
1. **Fragmenterte oppdateringer** - Tall oppdateres ikke konsistent på tvers av filer
2. **Manglende sentral konfigurasjon** - Ingen "single source of truth" for nøkkeltall
3. **Utdaterte metadata** - Flere filer har feil metadata/counts
4. **Manglende dashboards** - Deliverables og regulatory status trenger visualisering

Hovedanbefaling: Opprett `config.json` og systematisk oppdater alle filer til å referere til denne.
