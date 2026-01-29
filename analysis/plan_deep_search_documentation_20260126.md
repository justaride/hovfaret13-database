# Plan: Dyp Research & Dokumentsøk - Geoteknikk & Miljø

## Overview
En målrettet forskningsplan for å lokalisere kritisk manglende dokumentasjon knyttet til setningsskader på nabobygg ("dagsenteret") og andre miljødata. Planen kombinerer interne tekstsøk i depotet med målrettede eksterne søk (via Google Search-verktøyet) for å finne offentlige saksdokumenter.

## Current State Analysis
- **Kritisk mangel**: Dokumentasjon på setningsskader ved dagsenteret (nevnt i møter) mangler.
- **Ukjent adresse**: Vi vet ikke nøyaktig hvilket bygg "dagsenteret" refererer til (muligens Hoffsveien 30, Nedre Skøyen vei 26, eller lignende).
- **Nabodata**: Vi har ROS-analyse for Hoff skole, men mangler potensielt vedleggene med detaljerte boreprøver.

## Implementation Approach
Vi jobber i trakter:
1.  **Identifisering**: Finne adressen til dagsenteret gjennom interne søk.
2.  **Eksternt Søk**: Bruke adressen til å finne saksnumre og rapporter online (Saksinnsyn, Google).
3.  **Lokalt Dypdykk**: Søke i PDF-innhold (hvis mulig) og notater etter spesifikke nøkkelord.
4.  **Syntese**: Sammenstille funnene i en ny rapport.

## Phase 1: Identifisering av Objekt (Dagsenteret)
### Overview
Finne nøyaktig adresse/navn på bygget med setningsskader.
### Actions:
#### 1. Lokalt Søk
**Handling**: Kjøre `search_file_content` med utvidede termer for å finne referanser til adresser eller navn.
**Søkeord**: "dagsenter", "omsorgsbolig", "eldreomsorg", "Hoffsveien", "Nedre Skøyen vei", "setning", "skade".

### Success Criteria:
#### Manual:
- [ ] Identifisert adressen til dagsenteret (f.eks. "Hoffsveien 30").

## Phase 2: Eksternt Dypdykk (Google Web Search)
### Overview
Finne offentlige dokumenter basert på identifisert adresse.
### Actions:
#### 1. Google Søk
**Handling**: Bruke `google_web_search` for å finne saksdokumenter.
**Queries**:
- "setningsskader [adresse] saksinnsyn"
- "tilstandsrapport [adresse] Skøyen"
- "geoteknisk vurdering [adresse] Oslo"
- "Hoff skole geoteknisk rapport vedlegg"

### Success Criteria:
#### Manual:
- [ ] Funnet referanse til saksnummer eller tittel på rapporter.

## Phase 3: Lokalt PDF-Søk & Verifisering
### Overview
Sjekke om vi faktisk har disse dokumentene "skjult" i store PDF-er eller feilnavnede filer.
### Actions:
#### 1. List & Glob
**Handling**: Liste alle PDF-filer i `Hovfaret 13 - Klima...` og undermapper.
#### 2. Innholdssøk (hvis mulig)
**Handling**: Manuelt sjekke innholdsfortegnelser i store samlerapporter (f.eks. "Komplettvurdering").

## Phase 4: Rapportering & Oppdatering
### Overview
Dokumentere funnene og oppdatere argumentasjonsbasen.
### Changes Required:
#### 1. analysis/deep_search_results_20260126.md
**Changes**: Opprette rapport med funn (adresser, saksnumre, utdrag).
#### 2. data/themes/environmental-arguments.json
**Changes**: Oppdatere `missing_09` med konkret adresse og eventuelle lenker/referanser funnet.

### Success Criteria:
#### Manual:
- [ ] `deep_search_results_20260126.md` eksisterer med konkrete funn.
- [ ] `environmental-arguments.json` er oppdatert med presis info.
