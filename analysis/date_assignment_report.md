# DATO-TILDELING RAPPORT

**Generert:** 2025-11-22
**Skript:** `scripts/assign-meeting-dates.py`

---

## 📊 SAMMENDRAG

- **8 nye møter** ble opprettet fra umatchede notater
- **7 møter** manglet datoer
- **7 datoer tildelt** automatisk fra filnavn og innhold
- **1 møte** hadde allerede korrekt dato

---

## ✅ TILDELTE DATOER

### 1. Møte om James Lorentzen
- **ID:** `m_2025_06_24_med_james_lorentzen`
- **Dato:** 2025-06-24 ✅ (allerede korrekt)
- **Kilde:** Filnavn: "MØTE 24.06 2025 - avklaringer før møte med james .md"
- **Tillit:** Høy (eksplisitt dato i filnavn)

### 2. Rapport fra åpent møte: Bydel Ullern 2035
- **ID:** `m_unknown_date_rapport_fra_pent_mte_bydel_ullern`
- **Dato:** 2025-05-13 ✅
- **Kilde:** Innhold: "Tirsdag 13. mai 2025"
- **Tillit:** Høy (eksplisitt dato i innholdet)

### 3. Umiddelbare oppgaver (denne uken)
- **ID:** `m_unknown_date_umiddelbare_oppgaver_denne_uken`
- **Dato:** 2025-05-22 ⚠️
- **Kilde:** Filnavn: "MØTE  22 MAI   notater.md"
- **Tillit:** Medium (år estimert - kan være 2024)

### 4. Rapport: Bydelsledernes Uttalelser - Møte om Omsorg Pluss
- **ID:** `m_unknown_date_rapport_bydelsledernes_uttalelser_mte_om_omsorg`
- **Dato:** 2025-05-22 ⚠️
- **Kilde:** Filnavn: "MØTE  22 MAI  .md"
- **Tillit:** Medium (år estimert - kan være 2024)

### 5. Rapport: Møte om utviklingsprosjekt på Skøyen
- **ID:** `m_unknown_date_rapport_mte_om_utviklingsprosjekt_p_skyen`
- **Dato:** 2025-05-05 ⚠️
- **Kilde:** Filnavn: "MØTE  5 MAI  .md" + innhold nevner "2025"
- **Tillit:** Høy (innhold refererer til "pågående prosjekt i 2025")

### 6. Notat: Hva skal vi måles mot?
- **ID:** `m_unknown_date_notat_hva_skal_vi_mles_mot`
- **Dato:** 2025-04-03 ⚠️
- **Kilde:** Filnavn: "MØTE  3  April  .md"
- **Tillit:** Medium (år estimert)

### 7. Detaljert sammendrag av samtalen om skolebygget
- **ID:** `m_unknown_date_detaljert_sammendrag_av_samtalen_om_skolebygget`
- **Dato:** 2025-03-07 ⚠️
- **Kilde:** Filnavn: "MØTE  7 MARS   skoletomten.md"
- **Tillit:** Medium (år estimert - kan være 2024)

### 8. Nabolagsfabrikken møte
- **ID:** `m_unknown_date_det_er_jo_det`
- **Tittel:** "Det er jo det."
- **Dato:** 2025-03-07 ⚠️
- **Kilde:** Filnavn: "MØTE  7 MARS   Nabolagsfabrikken .md"
- **Tillit:** Medium (år estimert - kan være 2024)

---

## 🔍 DATOER SOM TRENGER VERIFISERING

### Prioritet 1: To møter på 22. mai - er de samme dag?
- **Umiddelbare oppgaver** (2025-05-22)
- **Bydelsledernes Uttalelser** (2025-05-22)

**Aksjon:** Sjekk om disse er fra samme møte eller to separate møter.

### Prioritet 2: To møter på 7. mars - er de samme dag?
- **Samtalen om skolebygget** (2025-03-07)
- **Nabolagsfabrikken møte** (2025-03-07)

**Aksjon:** Sjekk om disse er fra samme møte eller to separate møter.

### Prioritet 3: Bekreft år (2024 vs 2025)
Følgende datoer bruker estimert år basert på måned:
- Mars-møtene: 2025-03-07 (kan være 2024-03-07)
- April-møtet: 2025-04-03 (kan være 2024-04-03)
- Mai-møtene: 2025-05-05, 2025-05-22 (kan være 2024-05-xx)

**Aksjon:** Sjekk Google Calendar / Outlook for eksakte datoer.

---

## 📋 NESTE STEG

### 1. Dato-verifisering (høyest prioritet)
- [ ] Søk i Google Calendar etter møter i mars-juni 2024/2025
- [ ] Søk i e-post etter møteinnkallinger
- [ ] Kryss-sjekk med andre møter i meetings.json

### 2. Møte-disambiguering
- [ ] Bekreft om 22. mai-møtene er samme møte
- [ ] Bekreft om 7. mars-møtene er samme møte
- [ ] Vurder å slå sammen hvis samme møte

### 3. Metadata-oppdatering
- [ ] Legg til deltakere fra møtenotater
- [ ] Oppdater titler (spesielt "Det er jo det.")
- [ ] Fjern `data_quality_note` når verifisert

### 4. Action Items-ekstraksjon
- [ ] Les gjennom alle 8 notater
- [ ] Ekstraher handlingspunkter manuelt
- [ ] Oppdater `action_items` array

---

## 📁 FILER OPPDATERT

- ✅ `data/meetings.json` - 7 møter oppdatert med datoer
- ✅ `scripts/assign-meeting-dates.py` - Nytt skript for dato-tildeling
- ✅ `analysis/date_assignment_report.md` - Denne rapporten

---

## 🎯 STATUS: TRINN 2.1 FULLFØRT

**Fullført:**
- ✅ Identifisert alle 8 nye møter
- ✅ Tildelt datoer til 7 møter
- ✅ Dokumentert tillitsnivå for hver dato

**Gjenstår i Trinn 2:**
- ⏳ Verifiser datoer med kalender/e-post
- ⏳ Utfyll deltakerlister
- ⏳ Gjennomgå notater for action items
- ⏳ Oppdater titler og metadata

**Estimert tid gjenstående:** 5-7 timer

---

*Rapport generert automatisk - 2025-11-22*
