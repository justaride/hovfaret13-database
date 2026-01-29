# Research: Kartlegging av Dokumentasjonsstatus Hovfaret 13

**Dato**: 2026-01-26

## 1. Executive Summary
Denne rapporten dokumenterer nåværende status for miljø- og klimadokumentasjon for Hovfaret 13, basert på sammenligning mellom ønsket dokumentliste i `data/themes/environmental-arguments.json` og tilgjengelige filer i prosjektmappen.

## 2. Dokumentasjonsstatus (As-Is)

### Geoteknikk & Grunnforhold
- **Krav**: `missing_03` (Grunnundersøkelse H13) og `missing_04` (Kvikkleirekartlegging).
- **Eksisterende**:
    - `Hovfaret 13.../18_Omraadestabilitet.pdf`: Omhandler Nedre Skøyen vei 24–26 (nabotomt). Fastslår tilfredsstillende områdestabilitet for *det* prosjektet, men påviser kvikkleire i to borepunkter ved Hoffselva.
    - `Hovfaret 13.../56454645rte.md`: Oppsummering som slår fast at Hovfaret 13 ligger i samme marine avsetningssone og vil trenge egne geotekniske undersøkelser (L68).
- **Status**: Spesifikk geoteknisk rapport for Hovfaret 13 er ikke funnet i systemet.

### Biologi & Naturmiljø
- **Krav**: `missing_01` (Biologisk kartlegging) og `missing_02` (Sjøørret-bestandsvurdering).
- **Eksisterende**:
    - `Hovfaret 13.../13_Naturmiljoe.pdf`: Naturmiljøutredning for Hoff-prosjektet (TY1). Dokumenterer at Hoffselva er anadrom (sjøørret/laks).
    - `data/meetings.json`: Møte `m_2023-06-27` (L45) viser at Eirik (naturforvalter) fikk i oppgave å "Dokumentere biologisk mangfold på tomten".
- **Status**: Ferdigstilt eiendomsspesifikk rapport for biologisk mangfold på H13 er ikke funnet.

### Klima & Klimarisiko
- **Krav**: `missing_05` (Klimarisikovurdering H13 spesifikk).
- **Eksisterende**:
    - `Hovfaret 13.../Natural State AS Mail - Fwd_ Vurdering av klimarisiko Hovfaret 13.pdf`: E-post fra Vill Energi (2025-02-11) som lister opp nødvendig input for en klimarisikovurdering (temperatur, vind, vann, grunnforhold).
    - `data/themes/environmental-arguments.json`: Inneholder referanser til Vill Energi AS (2025) klimagassberegninger (arg_004).
- **Status**: Fullstendig stedsspesifikk klimarisikoanalyse (som etterspurt i e-post) er ikke funnet.

### Overvann & VA
- **Krav**: `missing_06` (Overvannsberegning for H13).
- **Eksisterende**:
    - `Hovfaret 13.../11_Vurdering_av_haandtering_av_overvann.pdf`: Vurdering for naboområdet.
    - `data/meetings.json`: Møte `m_2024-12-11` (L1800) viser befaring med Petter (Vill Energi) for energikartlegging mm.
- **Status**: Spesifikk overvannsberegning for transformasjonsscenariet mangler.

### Trafikk & Mobilitet
- **Krav**: `missing_08` (Trafikkanalyse for H13).
- **Eksisterende**:
    - `Hovfaret 13.../10_Notat_groenn_mobilitet_og_trafikk.pdf`: Generelt notat for Hoff-området.
    - `Hovfaret 13.../Trafikk, Skøyen _ Her flommer det over...pdf`: Nyhetsartikkel om flomutfordringer i trafikkbildet.
- **Status**: Eiendomsspesifikk trafikkanalyse for endret bruk (Omsorg+) er ikke funnet.

### Dagsenter & Setningsskader
- **Mangler**: `missing_09` (Tilstandsrapport/Setningsskader Dagsenter).
- **Eksisterende data**:
    - `data/meetings.json`: Møte `m_2025-05-22` (Bydelsledere Ullern) refererer til at "Eksisterende omsorg+-boliger (15-16 leiligheter) i nedre del av området må rives pga setningsskader".
    - `scripts/add_new_meetings_fase12.py`: Nevner "Eldreomsorgen lenger oppe i gata har setningsskader fra utgravning".
- **Status**: Ingen teknisk rapport eller tilstandsvurdering for dette bygget er funnet i depotet. Dette er et kritisk bevis for risikoen ved grunnarbeider i området.

### Nabotomt (Hoff Skole) - Ytterligere Data
- **Status**: Vi har gode oppsummeringer og enkelte rapporter (`18_Omraadestabilitet.pdf`, `08_ROS-analyse.pdf`), men bør verifisere om vi har *alle* vedlegg, spesielt de som omhandler detaljerte grunnboringer som danner grunnlaget for konklusjonene om kvikkleire.
- Er det utført boreprøver på tomta som ikke er arkivert i denne strukturen?
- Har Eirik (naturforvalter) produsert et utkast til biologisk kartlegging som ligger i en annen kanal (f.eks. Google Drive)?
- Hvilken VA-rådgiver er tenkt brukt for overvannsberegninger?
