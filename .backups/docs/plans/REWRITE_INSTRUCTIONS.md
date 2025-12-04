# INSTRUKSJONER FOR AUTOMATISK RENSKRIVNING AV MØTENOTATER

## KONTEKST

Dette prosjektet har 24 møter med rånotater som skal rensskrives til profesjonelle møtereferater.

**Prosjekt:** Hovfaret 13 - Transformasjon av kontorbygg fra 1989
**Utfordring:** Områdeplanen krever riving, men prosjektet argumenterer for rehabilitering
**Nøkkelargument:** 48% lavere CO₂ med transformasjon vs riving

## DATAKILDER

1. **`data/meetings.json`** - Metadata for alle 45 møter (deltakere, dato, etc.)
2. **`data/restructured_notes/`** - 24 rånotater som skal rensskrives
3. **`data/project.json`** - Full prosjekt-kontekst
4. **`data/stakeholders/organizations.json`** - Organisasjonsdata

## OPPGAVE

Renskrive ALLE 24 møtenotater ved å:

1. **Lese original notat** fra `data/restructured_notes/`
2. **Hente metadata** fra tilsvarende møte i `meetings.json`
3. **Bruke prosjekt-kontekst** fra `project.json`
4. **Renskrive notatet** til profesjonelt format
5. **Lagre** i `data/polished_notes/[DATO]_[ID]_POLISHED.md`

## OUTPUT-FORMAT

Hvert renskrevet notat skal ha:

```markdown
# [Beskrivende tittel basert på innhold]

**Dato:** [ISO format]
**Tid:** [Hvis nevnt]
**Sted:** [Lokasjon]
**Organisert av:** [Navn]

## Deltakere

- **[Navn]** - [Organisasjon] ([e-post])
- ...

## Sammendrag

[2-3 setninger som fanger essensen av møtet]

## Diskusjonstemaer

- [Tema 1]
- [Tema 2]
- ...

## Diskusjon

### [Tema 1]

[Detaljert beskrivelse...]

### [Tema 2]

[Detaljert beskrivelse...]

## Beslutninger

- [Beslutning 1]
- [Beslutning 2]

## Action Items

- **[Oppgave]** - Ansvarlig: [Navn] - Frist: [Dato]
- ...

## Viktige sitater

> "[Sitat hvis relevant]"

## Vedlegg / Referanser

- [Lenker/dokumenter nevnt]

---
*Renskrevet: 2025-11-22*
*Basert på: [original filnavn]*
```

## KVALITETSKRITERIER

✅ **Behold all faktisk informasjon** - ikke oppfinn
✅ **Bruk prosjekt-kontekst** - forklar begreper med kontekst
✅ **Ekstraher action items** - finn alle handlingspunkter (også implisitte)
✅ **Identifiser decisions** - finn alle beslutninger
✅ **Strukturer logisk** - organiser etter tema
✅ **Profesjonelt språk** - ryddig men naturlig norsk
✅ **Behold detaljer** - tall, navn, sitater er viktige
✅ **Marker usikkerhet** - bruk [?] hvis noe er uklart

## MATCHING LOGIC

For å finne riktig møte i meetings.json:
- Bruk filnavnet fra restructured_notes
- Match mot `report_link` feltet i meetings.json
- Hent all metadata derfra (deltakere, dato, etc.)

## PROSESSFLYT

1. Les alle filer i `data/restructured_notes/`
2. For hver fil:
   a. Finn tilsvarende møte i `meetings.json`
   b. Last prosjekt-kontekst fra `project.json`
   c. Renskrive notatet med full kontekst
   d. Lagre i `data/polished_notes/`
3. Generer rapport med:
   - Antall prosesserte
   - Gjennomsnittlig lengde før/etter
   - Liste over output-filer

## EKSEMPEL PÅ KONTEKST-BRUK

**Original:** "Vi diskuterte omsorg pluss"
**Renskrevet:** "Vi diskuterte Omsorg+-scenariet, som innebærer omgjøring av bygget til omsorgsboliger med 3 etasjer påbygg, rettet mot eldre i Ullern bydel."

**Original:** "Andreas sa noe om CO2"
**Renskrevet:** "Andreas fra Urbania fremhevet at rehabilitering gir 48% lavere CO₂-utslipp sammenlignet med riving og nybygg (456 vs 631 kg CO₂-ekv/m² BTA)."

## START PROCESSING

Når du er klar, start med å:
1. Lese `data/meetings.json` for full oversikt
2. Liste alle filer i `data/restructured_notes/`
3. Prosessere dem én for én
4. Lagre i `data/polished_notes/`
5. Generere samle-rapport

**MÅL:** Alle 24 møtenotater renskrevet med høy kvalitet og full kontekst.
