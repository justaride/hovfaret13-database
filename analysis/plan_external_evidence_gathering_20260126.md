# Plan: Kartlegging av Ekstern Dokumentasjon & Naboforhold

## Overview
Dette er en strategi for å flytte fokuset fra "hva H13 må dokumentere" til "hva som allerede er dokumentert rundt oss". Målet er å finne **presedens**, **risikobevis** og **områdedata** fra naboeiendommer som kan styrke saken for bevaring og transformasjon. Vi skal gjennomføre "nabo-detektivarbeid" for å finne byggesaker, geotekniske rapporter og dispensasjoner i nærområdet.

## Current State Analysis
- **Internt fokus**: Vi har god kontroll på H13s egne behov og mangler.
- **Eksternt fokus**: Vi har identifisert Skøyen Terrasse 1 (setningsskader) og Hoff Skole (ROS-analyse), men mangler en systematisk gjennomgang av andre naboer.
- **Mulighet**: Offentlige saksarkiver (Saksinnsyn) og dokumenter fra store utbyggere (Møller, Storebrand, Bane NOR) inneholder sannsynligvis detaljerte grunnundersøkelser for hele området.

## Implementation Approach
1.  **Geografisk Kartlegging**: Definere "interessesonen" rundt H13.
2.  **Saks-Identifisering**: Finne saksnumre og adresser på relevante byggesaker.
3.  **Dokumentsøk**: Søke etter spesifikke dokumenttyper (geoteknikk, flom, dispensasjon).
4.  **Syntese**: Koble funnene til H13s argumentasjon.

## Phase 1: Geografisk Målsøk (Radius 500m)
### Overview
Identifisere nøkkeladresser og aktører som har gjennomført tunge prosesser nylig.
### Targets:
1.  **Harbitz Torg** (Møller Eiendom) - Stor transformasjon, sannsynligvis tunge miljø/grunnrapporter.
2.  **Hoffsveien 30** - Høyblokk, relevant for høyde/skygge/grunn.
3.  **Nedre Skøyen vei 26** (Amalies Hage) - Boligprosjekt, relevant for støy/grunn.
4.  **Skøyen Stasjon** (Bane NOR) - Områdeplanarbeid, tunge tekniske rapporter.
5.  **Verkstedveien** - Transformasjonsprosjekter.

### Success Criteria:
#### Manual:
- [ ] Liste over 5-10 konkrete adresser/Gnr/Bnr å søke på.

## Phase 2: Dypdykk i Saksdokumenter (Google/Saksinnsyn Proxy)
### Overview
Bruke Google Search-operatorer for å finne PDF-er og saksdokumenter som ligger åpent.
### Queries:
- `site:oslo.kommune.no "geoteknisk" "Skøyen" filetype:pdf`
- `site:oslo.kommune.no "dispensasjon" "Hoffsveien" filetype:pdf`
- `"grunnundersøkelse" "Harbitz Torg"`
- `"flomvei" "Hoffselva" kart`

### Success Criteria:
#### Manual:
- [ ] Identifisert minst 3 relevante eksterne rapporter (geoteknikk, flom, eller støy) fra naboer.
- [ ] Funnet eksempler på gitte dispensasjoner i området.

## Phase 3: Presedens-Analyse (Omsorg+ & Høyder)
### Overview
Finne bevis på at kommunen har godkjent lignende konsepter eller avvik i nærheten.
### Actions:
- Søke etter godkjente påbygg i området.
- Søke etter andre Omsorg+ etableringer i eksisterende bygg (presedens for konsept).

## Phase 4: Rapportering & Integrering
### Overview
Sammenstille funnene i en ny "Ekstern Bevis"-rapport og oppdatere argumentasjonsbasen.
### Changes Required:
#### 1. analysis/external_evidence_report_20260126.md
**Changes**: Opprette rapport med funn.
#### 2. data/themes/environmental-arguments.json
**Changes**: Legge til nye "Supporting Documents" fra naboer som styrker våre poenger.

### Success Criteria:
#### Manual:
- [ ] Rapport opprettet.
- [ ] Nye "ammunisjon"-punkter lagt til i dashboardet.
