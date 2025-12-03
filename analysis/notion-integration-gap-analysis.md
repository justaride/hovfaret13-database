# Gap-analyse: Notion Integrering

**Dato:** 2025-12-03
**Formål:** Identifisere manglende data og inkonsistenser etter Notion-integrering

---

## 1. MØTER - Gap-analyse

### Status før analyse
- **meetings.json:** 65 møter
- **notion-import/meetings-from-notion.json:** 4 møter

### Møter som MÅ merges inn i meetings.json

| Dato | Notion-møte | Eksisterer i meetings.json? | Handling |
|------|-------------|------------------------------|----------|
| 2025-09-05 | Strategimøte Hovfaret 13 | ❌ NEI | **LEGG TIL** |
| 2025-09-08 | NCE søknad oppfølging | ❌ NEI | **LEGG TIL** |
| 2025-09-19 | Tlf Thomas nabolagsmøte | ❌ NEI | **LEGG TIL** |
| 2025-10-14 | Nabolagsmøte (30 deltakere) | ⚠️ DELVIS - har "Befaring" | **LEGG TIL SOM SEPARAT** |

### Detaljer om 2025-10-14 konflikt
- **Eksisterende:** "Hovfaret 13 - Befaring og prosjektdiskusjon" (3 deltakere, Gabriel+Einar+ekstern)
- **Fra Notion:** "Nabolagsmøte Hovfaret 13" (30 deltakere, offentlig møte)
- **Konklusjon:** Dette er TO FORSKJELLIGE MØTER på samme dag - begge skal beholdes

### Prioritet: HØY
Disse 4 møtene inneholder kritisk strategisk informasjon:
- Sept 5: Beslutning om å gå direkte til Omsorg+ (strategisk skifte)
- Sept 8: Nordic Innovation søknadsstrategi
- Sept 19: Planlegging av nabolagsmøte
- Okt 14: Offentlig presentasjon med ~30 deltakere

---

## 2. STAKEHOLDERS - Gap-analyse

### Allerede oppdatert ✅
| Person | Status | Endring |
|--------|--------|---------|
| Linda Marie Aas | ✅ Utvidet | Fullstendig navn, bio, leveranser |
| Kamran Surizehi | ✅ NY | Komplett profil |
| Severin Døcker | ✅ Utvidet | Fullstendig navn |

### Mangler fortsatt
| Person | Nevnt i Notion | Handling |
|--------|----------------|----------|
| Thomas (R21) | Ja - Tlf 19. sept | Verifiser at Thomas Thorsen har oppdatert info |
| Ingrid Hopp | Ja - Nabolagsmøte | ✅ Finnes allerede |
| Wenche | Nevnt i leveranser | ❓ Hvem er Wenche? Undersøk |
| Emil Paaske | Invitert til nabolagsmøte | ❓ Legg til? |

### Organisasjoner - Allerede oppdatert ✅
| Organisasjon | Status |
|--------------|--------|
| Byggesaksrådgivning AS | ✅ NY |
| Parabol | ✅ NY |
| Nordic Circle Hotspot | ✅ NY |

---

## 3. TIMELINE - Gap-analyse

### Allerede oppdatert ✅
| ID | Dato | Hendelse | Status |
|----|------|----------|--------|
| o_023 | 2025-10-14 | Nabolagsmøte | ✅ Lagt til |
| o_024 | 2025-10-16 | Nabovarsel sendt | ✅ Lagt til |
| o_025 | 2025-10-29 | Bydelsutvalgsmøte | ✅ Lagt til |
| o_026 | 2025-11-07 | Bruksendringssøknad | ✅ Lagt til |
| o_027 | 2025-12-01 | Konseptskisse 2.0 | ✅ Lagt til |

### Mangler muligens
| Dato | Hendelse | Kilde | Prioritet |
|------|----------|-------|-----------|
| 2025-09-29 | Nettside lansering | Notion | Medium |
| 2025-10-16 | Bankmøte | Notion | Lav |
| 2025-09-05 | Strategisk skifte til Omsorg+ | Notion møte | HØY |

---

## 4. DOKUMENTER - Gap-analyse

### Nye dokumenter fra Notion som bør registreres
| Dokument | Type | Kilde | Prioritet |
|----------|------|-------|-----------|
| Invitasjon nabolagsmøte | Plakat/PDF | Notion leveranse | Medium |
| Presentasjon nabolagsmøte | Slides | Notion leveranse | HØY |
| Oppsummering nabolagsmøte | Rapport | Notion | HØY |
| Plansjer temastasjon | Plakater | Notion leveranse | Medium |
| hovfaret13.no nettside | Web | Parabol | Medium |

### Sjekk documents.json
- **Totalt:** 271 dokumenter
- **Siste dato i documents.json:** Må verifiseres
- **Mangler trolig:** Dokumenter fra sept-nov 2025

---

## 5. LEVERANSER (NY KATEGORI)

### Status
Notion-eksporten inneholder 75 leveranser som ikke har egen datafil i prosjektet.

### Anbefaling
Opprett `data/deliverables.json` basert på `notion-import/deliverables-from-notion.json`

### Struktur forslag
```json
{
  "metadata": {...},
  "deliverables": [
    {
      "id": "d_001",
      "title": "Nabolagsmøte",
      "status": "completed",
      "dates": {"start": "2025-10-06", "end": "2025-10-14"},
      "responsible": ["linda_marie_aas", "kamran_surizehi"],
      "category": "stakeholder_engagement"
    }
  ]
}
```

---

## 6. DASHBOARD-SIDER - Gap-analyse

### Sider som trenger oppdatering
| Side | Trenger oppdatering? | Handling |
|------|----------------------|----------|
| meetings.html | ⚠️ Ja | Nye møter vises ikke |
| stakeholders.html | ⚠️ Ja | Kamran, Linda ikke synlig |
| timeline.html | ✅ Automatisk | Leser fra timeline-enhanced.json |
| documents.html | ❓ Sjekk | Nye dokumenter? |

### Ny side forslag
- `deliverables.html` - Leveranse-oversikt fra Notion

---

## 7. HANDLINGSPLAN

### Fase 1: Kritisk (NÅ) ✅ FULLFØRT
1. [x] Merge 4 Notion-møter inn i meetings.json ✅
2. [x] Verifisere at stakeholder-endringer reflekteres i dashboard ✅

### Fase 2: Høy prioritet ✅ FULLFØRT
3. [x] Legge til strategisk skifte (5. sept) i timeline som strategic event ✅ (s_010)
4. [x] Legge til nabolagsmøte (14. okt) i timeline som strategic event ✅ (s_011)
5. [x] Opprette deliverables.json fra Notion-data ✅

### Fase 3: Medium prioritet
6. [ ] Undersøke hvem Wenche og Emil Paaske er
7. [ ] Verifisere documents.json dekker sept-nov 2025
8. [ ] Vurdere ny deliverables.html side
9. [ ] Registrere nabolagsmøte-dokumenter i documents.json

### Fase 4: Lav prioritet
10. [ ] Legge til nettside-lansering og bankmøte i timeline
11. [ ] Oppdatere project.json med nye milepæler

---

## 8. DATAKVALITET SCORE

| Kategori | Før | Etter | Mål | Status |
|----------|-----|-------|-----|--------|
| Møter | 65 | 69 | 70+ | ✅ Nær mål |
| Stakeholders | 22 | 24 | 25+ | ⚠️ Pågående |
| Organisasjoner | 13 | 16 | 16 | ✅ Oppnådd |
| Timeline events | 32 | 39 | 40+ | ✅ Nær mål |
| Dokumenter | 271 | 271 | 280+ | ⚠️ Trenger oppdatering |
| Leveranser | 0 | 75 | 75 | ✅ Oppnådd |

---

## Konklusjon

**Status: ✅ Kritiske handlinger FULLFØRT (2025-12-03)**

Alle kritiske og høy-prioritet oppgaver er nå fullført:
- ✅ 4 møter fra Notion merget inn i meetings.json (65→69 møter)
- ✅ 2 strategiske hendelser lagt til i timeline (s_010, s_011)
- ✅ deliverables.json opprettet med 75 strukturerte leveranser

Prosjektdatabasen har nå fullstendig dokumentasjon av den strategiske perioden september-oktober 2025, inkludert:
- Beslutning om å gå direkte til Omsorg+ (5. sept)
- Nordic Innovation søknadsstrategi (8. sept)
- Nabolagsmøte planlegging og gjennomføring (19. sept - 14. okt)

**Gjenværende oppgaver (medium/lav prioritet):**
- Undersøke ukjente stakeholders (Wenche, Emil Paaske)
- Oppdatere documents.json med sept-nov 2025 dokumenter
- Vurdere ny deliverables.html dashboard-side
