# KVALITETSSIKRING SJEKKLISTE
## Møtenotater - Hovfaret 13 Prosjekt

**Generert:** 2025-11-22
**Formål:** Manuell gjennomgang av alle 45 møter før final oppdatering

---

## 📊 OVERSIKT

### Status:
- ✅ **Trinn 1 fullført:** Alle notater matchet og meetings.json oppdatert
- 🔄 **Trinn 2 pågår:** Manuell kvalitetssikring (automatisert del fullført)
- ⏳ **Trinn 3 venter:** Final verifisering

### Møter som trenger gjennomgang:
- **16 møter med notatdata** - behover verifisering
- **8 nye møter** ✅ **DATOER TILDELT** - må kvalitetssikres og utfylles
- **21 møter uten notater** - vurder om notater kan finnes

### NYE FUNN (fra automatisert analyse):
- 🔍 **5 datoer med duplikater** - 13 møter totalt
  - **3 klare duplikater** (score 40-70/100) - bør slås sammen
  - **2 mulige duplikater** - trenger manuell review
- 📅 **Alle 45 møter har nå dato** (7 nye tildelt automatisk)
- ⚠️ **5 møter** trenger dato-verifisering (år estimert)

---

## ✅ GJENNOMGANGSPROSESS

### For hvert møte med notater (16+8 = 24 møter):

#### 1. Verifiser grunnleggende metadata
- [ ] **Dato er korrekt** (stemmer med møtenotat og kalender)
- [ ] **Tittel er beskrivende** (ikke "MØTE DD MÅNED")
- [ ] **Deltakere er komplette** (navn, org, e-post)
- [ ] **Organisator er spesifisert**
- [ ] **Lokasjon er fylt ut** (hvis relevant)

#### 2. Sjekk notatinnhold
- [ ] **report_link peker til riktig fil** (test lenken)
- [ ] **Action items er meningsfulle** (ikke fragmenter som "hos statsforvalteren")
- [ ] **Topics discussed er relevante** (ikke meta-overskrifter)
- [ ] **Decisions er faktiske beslutninger** (ikke generell tekst)

#### 3. Berik med ekstra informasjon
- [ ] **Legg til manglende deltakere** (fra e-post, kalender)
- [ ] **Fyll ut action items** (les notatet, finn handlingspunkter)
- [ ] **Ekstraher decisions** (se etter "enighet om", "besluttet", "vedtatt")
- [ ] **Fjern data_quality_note** når verifisert

#### 4. Konsistenssjekk
- [ ] **participant_count matcher antall participants**
- [ ] **Ingen duplikater** i action_items, topics, decisions
- [ ] **Norsk tegnsetting er korrekt** (æ, ø, å)

---

## 🔍 SPESIELLE TILFELLER

### Nye møter (8 stk) - Ekstra oppmerksomhet:

Disse møtene ble auto-generert og har `data_quality_note`:

1. **m_unknown_date_umiddelbare_oppgaver_denne_uken**
   - ⚠️ Mangler dato - finn ut når dette møtet var
   - Notat: `MØTE  22 MAI   notater.md` (muligens 22. mai 2024/2025?)

2. **m_unknown_date_notat_hva_skal_vi_males_mot**
   - ⚠️ Mangler dato - fra filnavn "MØTE  3  April"
   - Mulig dato: 3. april 2024?

3. **m_unknown_date_rapport_bydelsledernes_uttalelser**
   - Innhold: "MØTE  22 MAI  .md"
   - Mulig dato: 22. mai 2024/2025?

4. **m_unknown_date_detaljert_sammendrag_av_samtalen**
   - Fra: "MØTE  7 MARS   skoletomten.md"
   - Mulig dato: 7. mars 2024/2025?

5. **m_unknown_date_det_er_jo_det**
   - Fra: "MØTE  7 MARS   Nabolagsfabrikken .md"
   - Mulig dato: 7. mars 2024/2025?

6. **m_unknown_date_med_james_lorentzen**
   - Fra: "MØTE 24.06 2025 - avklaringer før møte med james .md"
   - **Dato i filnavn: 24. juni 2025**

7. **m_unknown_date_rapport_mote_om_utviklingsprosjekt**
   - Fra: "MØTE  5 MAI  .md"
   - Mulig dato: 5. mai 2024/2025?

8. **m_unknown_date_rapport_fra_apent_mote**
   - Fra: "Rapport-fra-pent-mte-Bydel-UllernMØTE  13 MAI  -2035.md"
   - **Dato i filnavn: 13. mai 2035 (trolig feil - skal være 2025?)**

---

## 🤖 AUTOMATISERTE FUNN (22. november 2025)

### ✅ Fullført automatisk:

#### 1. Dato-tildeling (script: `assign-meeting-dates.py`)
- Analyserte 8 nye møter uten dato
- Tildelt datoer til alle 7 (1 hadde allerede dato)
- **Resultater:**
  - 2025-03-07: 2 møter ("Skoletomten" og "Nabolagsfabrikken")
  - 2025-04-03: 1 møte ("Hva skal vi måles mot")
  - 2025-05-05: 1 møte ("Utviklingsprosjekt på Skøyen")
  - 2025-05-13: 1 møte ("Bydel Ullern 2035")
  - 2025-05-22: 2 møter ("Umiddelbare oppgaver" og "Bydelsledernes uttalelser")
  - 2025-06-24: 1 møte ("James Lorentzen" - allerede korrekt)

**📄 Detaljer:** `analysis/date_assignment_report.md`

#### 2. Duplikat-identifikasjon (script: `identify-duplicate-meetings.py`)
- Analyserte alle 45 møter for duplikater
- Funnet 5 datoer med multiple møter (13 møter totalt)
- **Klare duplikater (bør merges):**
  1. **17. januar 2025** - 2 møter (score 70/100) - SAMME FIL!
  2. **11. mars 2024** - 2 møter (score 40/100)
  3. **6. mai 2024** - 2 møter (score 40/100)
- **Trenger review:**
  4. **7. mars 2025** - 4 møter (2 eksisterende + 2 nye)
  5. **22. mai 2025** - 3 møter (1 eksisterende + 2 nye)

**📄 Detaljer:** `analysis/duplicate_meetings_report.md`

### ⚠️ Krever manuell oppfølging:

1. **Merge de 3 klare duplikatene**
   - Estimert tid: 1-2 timer
   - Vil redusere møter fra 45 til 42

2. **Review 7. mars og 22. mai**
   - Les rapportene for å avgjøre om samme møte
   - Estimert tid: 2-3 timer

3. **Verifiser estimerte år**
   - 5 møter har estimert år (2024 vs 2025)
   - Sjekk kalender/e-post for bekreftelse

**📄 Full fremgangsrapport:** `analysis/TRINN_2_PROGRESS_REPORT.md`

---

## 📝 HANDLINGSPLAN

### Uke 1: Grunndata (Prioritet 1)
**Tidsbruk: ~2-3 timer**

1. ✅ Finn datoer for de 8 nye møtene
   - Sjekk Google Calendar / Outlook
   - Søk i e-post etter møteinnkallinger
   - Oppdater `date` felt i meetings.json

2. ✅ Verifiser og utfyll deltakere
   - Gå gjennom møteinnkallinger
   - Legg til e-postadresser
   - Sjekk organisasjonstilknytning

### Uke 2: Innholdsgjennomgang (Prioritet 2)
**Tidsbruk: ~4-5 timer**

3. ✅ Gjennomgå alle 24 notater
   - Les hvert notat grundig
   - Ekstraher action items manuelt
   - Identifiser decisions fra tekst
   - Oppdater topics_discussed

4. ✅ Kvalitetssikre high-confidence matcher
   - Verifiser at de 9 matchene er korrekte
   - Sjekk at riktig notat er koblet til riktig møte

### Uke 3: Finpuss (Prioritet 3)
**Tidsbruk: ~1-2 timer**

5. ✅ Fjern kvalitetsmerknader
   - Slett `data_quality_note` fra verifiserte møter
   - Oppdater `report_metadata` med review-status

6. ✅ Final konsistenssjekk
   - Verifiser at alle lenker fungerer
   - Sjekk at participant_count er riktig
   - Test at data kan lastes i dashboard

---

## 🎯 MÅLSETTING

### Suksesskriterier:
- ✅ Alle 45 møter har korrekt dato
- ✅ Minst 30 møter har komplette deltakerlister
- ✅ Alle 24 møter med notater har verifiserte action items
- ✅ Ingen `data_quality_note` gjenstår
- ✅ Alle `report_link` peker til eksisterende filer

### Akseptable hull:
- ❌ Noen møter kan mangle lokasjon (online møter)
- ❌ Noen møter kan ha få deltakere registrert (1-2 personer)
- ❌ Decisions kan være tomme hvis ingen beslutninger ble tatt

---

## 📂 ARBEIDSFILER

### Filer du trenger:
- `data/meetings.json` - Hovedfil som skal oppdateres
- `data/restructured_notes/` - Alle omstrukturerte notater
- `analysis/matching_applied_summary.json` - Oversikt over matcher

### Backup:
- `data/meetings.backup_20251122_102828.json` - Siste backup før matching

### Kommandoer:
```bash
# Åpne meetings.json for redigering
code data/meetings.json

# Se et omstrukturert notat
cat "data/restructured_notes/2024-03-11_MØTE  11 MARS   2024.md"

# Søk etter spesifikke møter
grep -i "james" data/meetings.json

# Telle møter
cat data/meetings.json | jq '.meetings | length'
```

---

## ✅ SJEKKLISTE PR. MØTE

Kopier denne for hvert møte du gjennomgår:

```markdown
### Møte: [TITTEL]
**ID:** [MEETING_ID]
**Dato:** [DATO]

- [ ] Dato verifisert
- [ ] Tittel oppdatert
- [ ] Deltakere komplette (minst navn)
- [ ] E-postadresser lagt til
- [ ] Organisator spesifisert
- [ ] Lokasjon fylt ut
- [ ] Action items verifisert (0-10 items)
- [ ] Topics discussed verifisert
- [ ] Decisions verifisert
- [ ] report_link testet
- [ ] data_quality_note fjernet
- [ ] participant_count riktig

**Notater:** [Eventuelle merknader]
```

---

## 🚀 KOMME I GANG

1. **Åpne meetings.json** i din favoritt-editor
2. **Søk etter "data_quality_note"** - dette er møtene som trenger review
3. **Start med de 8 nye møtene** - finn datoer først
4. **Deretter de 16 berikede møtene** - verifiser innhold
5. **Oppdater løpende** - lagre ofte!

**Estimert tid:** 7-10 timer totalt over 2-3 uker

---

*Lykke til med kvalitetssikringen! 🎯*
