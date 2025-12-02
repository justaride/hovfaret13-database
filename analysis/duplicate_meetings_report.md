# RAPPORT: DUPLIKATE MØTER

**Generert:** 2025-11-22
**Skript:** `scripts/identify-duplicate-meetings.py`

---

## 📊 SAMMENDRAG

Fant **5 datoer** med multiple møter:
- **3 klare duplikater** (bør slås sammen)
- **2 mulige duplikater** (trenger review)
- **Totalt 13 møter** på disse datoene

---

## 🔀 KLARE DUPLIKATER (Høy tillit - bør slås sammen)

### 1. 11. mars 2024 - Score: 40/100

**Møte A:**
- **ID:** `m_2024-03-11_urbania_hovfaret_13_konseptskisse_1_0`
- **Tittel:** "Urbania Hovfaret 13 - Konseptskisse 1.0"
- **Deltakere:** 3 (Andreas, Einar, Gabriel)
- **Rapport:** `/My Drive/H13 Backup Process Nov 25/MIRO ting. MØTE RAPPORTER VIKTIG ER HER /MØTE  11 MARS 2024.md`

**Møte B:**
- **ID:** `m_2024-03-11__11_mars_2024`
- **Tittel:** "MØTE  11 MARS 2024"
- **Deltakere:** 3 (Andreas Helness, Einar Sneve Martinussen, Gabriel Boenjamin)
- **Rapport:** `data/restructured_notes/2024-03-11_MØTE  11 MARS   2024.md`

**ANALYSE:**
- ✅ Samme dato
- ✅ Samme deltakere (3 personer)
- ✅ Begge har rapporter
- ⚠️ Forskjellige rapport-filer - kan være samme møte med to rapporter

**ANBEFALING:** Slå sammen til én post, behold beste tittel og kombiner rapporter.

---

### 2. 6. mai 2024 - Score: 40/100

**Møte A:**
- **ID:** `m_2024-05-06_hovfaret_13_med_r21`
- **Tittel:** "Hovfaret 13 med R21"
- **Deltakere:** 3
- **Rapport:** Ja

**Møte B:**
- **ID:** `m_2024-05-06__6_mai_2024`
- **Tittel:** "MØTE  6  MAI 2024"
- **Deltakere:** 3
- **Rapport:** `data/restructured_notes/2024-05-06_MØTE  6  MAI   2024.md`

**ANALYSE:**
- ✅ Samme dato
- ✅ Samme antall deltakere
- ✅ Begge har rapporter

**ANBEFALING:** Slå sammen, behold "Hovfaret 13 med R21" som tittel.

---

### 3. 17. januar 2025 - Score: 70/100 (HØYEST)

**Møte A:**
- **ID:** `m_2025-01-17_hovfaret_13_status_m_te_`
- **Tittel:** "Hovfaret 13 Status Møte"
- **Deltakere:** 6
- **Rapport:** `MØTE 17  Januar 25.md`

**Møte B:**
- **ID:** `m_2025-01-17_17_januar_25`
- **Tittel:** "MØTE 17  Januar 25"
- **Deltakere:** 6
- **Rapport:** `MØTE 17  Januar 25.md` (SAMME FIL!)

**ANALYSE:**
- ✅ Samme dato
- ✅ Samme deltakere (6 personer)
- ✅ SAMME rapport-fil
- 🔥 Dette er 100% samme møte

**ANBEFALING:** Slå sammen umiddelbart. Dette er åpenbart samme møte registrert to ganger.

---

## ⚠️ TRENGER REVIEW

### 4. 7. mars 2025 - 4 møter totalt

**Eksisterende møter (Score: 40/100):**

**Møte A:**
- **ID:** `m_2025-03-07_hovfaret_13_statusm_tet`
- **Tittel:** "Hovfaret 13 - Statusmøtet"
- **Deltakere:** 4
- **Rapport:** `MØTE 7  Mars 25.md`

**Møte B:**
- **ID:** `m_2025-03-07_7_mars_25`
- **Tittel:** "MØTE 7  Mars 25"
- **Deltakere:** 4
- **Rapport:** `data/restructured_notes/2025-03-07_MØTE 7  Mars  2025.md`

**Nye møter (ingen deltakere):**

**Møte C:**
- **ID:** `m_unknown_date_detaljert_sammendrag_av_samtalen_om_skolebygget`
- **Tittel:** "Detaljert sammendrag av samtalen om skolebygget"
- **Deltakere:** 0
- **Rapport:** `UKJENT_DATO_MØTE  7 MARS   skoletomten.md`

**Møte D:**
- **ID:** `m_unknown_date_det_er_jo_det`
- **Tittel:** "Det er jo det."
- **Deltakere:** 0
- **Rapport:** `UKJENT_DATO_MØTE  7 MARS   Nabolagsfabrikken .md`

**ANALYSE:**
- ✅ Møte A og B er trolig samme møte (score 40/100)
- ❓ Møte C og D har ingen deltakere, kan være:
  - Notater fra samme møte (A/B)
  - Separate møter samme dag
  - Transkripsjoner/detaljnotater fra hovedmøtet

**ANBEFALING:**
1. Slå sammen A og B
2. Les gjennom rapportene C og D for å avgjøre om de hører til hovedmøtet
3. Hvis C og D er del av hovedmøtet: Merge alt til ett møte
4. Hvis separate: Behold som egne møter med bedre titler

---

### 5. 22. mai 2025 - 3 møter

**Eksisterende møte:**

**Møte A:**
- **ID:** `m_2025-05-22_m_te_med_bydels_leder_p_hovfaret_13_vi_m`
- **Tittel:** "Møte med Bydels leder på Hovfaret 13 ( Vi møtes en 1 time før )"
- **Deltakere:** 3
- **Rapport:** `2025-08-06_06 August 2025.md` (⚠️ Feil dato i filnavn!)

**Nye møter:**

**Møte B:**
- **ID:** `m_unknown_date_umiddelbare_oppgaver_denne_uken`
- **Tittel:** "Umiddelbare oppgaver (denne uken):"
- **Deltakere:** 0
- **Rapport:** `UKJENT_DATO_MØTE  22 MAI   notater.md`

**Møte C:**
- **ID:** `m_unknown_date_rapport_bydelsledernes_uttalelser_mte_om_omsorg`
- **Tittel:** "Rapport: Bydelsledernes Uttalelser - Møte om Omsorg Pluss i Ullern Bydel"
- **Deltakere:** 0
- **Rapport:** `UKJENT_DATO_MØTE  22 MAI  .md`

**ANALYSE:**
- ⚠️ Møte A har rapport fra 6. august (mismatch!)
- ⚠️ Møte C nevner spesifikt "Bydelsledernes Uttalelser" - matcher tittelen på Møte A
- ❓ Møte B ser ut som en action items-liste, ikke et møte
- **Score:** Kun 13/100 (lav tillit)

**ANBEFALING:**
1. **Verifiser:** Er Møte A faktisk 22. mai eller 6. august?
2. **Les rapportene:** Sammenlign innholdet i de tre rapportene
3. **Sannsynlig scenario:**
   - Møte A og C er samme møte (om Omsorg Pluss med bydelsleder)
   - Møte B er en oppfølgings-/action items-liste fra samme møte
4. **Hvis samme møte:** Merge alle tre, behold beste data fra hver

---

## 📋 HANDLINGSPLAN

### Fase 1: Automatisk merge (høy tillit)
- [ ] Merge møte 17. januar 2025 (score 70/100) - samme fil!
- [ ] Merge møte 11. mars 2024 (score 40/100)
- [ ] Merge møte 6. mai 2024 (score 40/100)

### Fase 2: Manuell review
- [ ] Les rapportene for 7. mars 2025 (4 møter)
- [ ] Les rapportene for 22. mai 2025 (3 møter)
- [ ] Avgjør om de skal merges eller beholdes separate

### Fase 3: Opprydding
- [ ] Fjern dupliserte møte-IDer fra meetings.json
- [ ] Oppdater metadata (total_meetings count)
- [ ] Verifiser at alle lenker fungerer

---

## 💡 INNSIKTER

**Hvordan oppsto duplikatene?**

1. **Original meetings.json** hadde møter fra kalender/e-post
2. **Restructured notes** ble matchet til eksisterende møter OG opprettet nye
3. **Resultat:** Noen møter finnes både som original post og som ny post fra notater

**Løsning:**
- Merge ved å beholde beste metadata fra hver kilde
- Original post har ofte bedre deltakerinformasjon
- Notater har bedre action items / topics / decisions

---

## 🎯 FORVENTET RESULTAT

**Før:** 45 møter
**Etter merge:** ~39-41 møter (estimat)

- 3 klare duplikater fjernet (-3 møter)
- 4-6 møter fra mars/mai potensielt merged (-1 til -3 møter)

---

*Rapport generert automatisk - 2025-11-22*
