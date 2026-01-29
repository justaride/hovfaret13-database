# Plan: Innhenting og Integrering av Miljødokumentasjon H13

## Overview
Dette er en plan for å innhente og integrere de 8 manglende dokumentene identifisert i `environmental-arguments.json`. Målet er å tette kunnskapshullene før rammesøknad og sikre at argumentasjonen mot riving er basert på eiendomsspesifikke fakta.

## Current State Analysis
- **Filreferanse**: `data/themes/environmental-arguments.json` definerer ønsket status.
- **Mangler**: 8 spesifikke rapporter (Biologi, Geoteknikk, Klimarisiko, Overvann, Trafikk, Kulturminne).
- **Åpne Spørsmål**: Det er usikkert om utkast eksisterer i eksterne kanaler (Google Drive/E-post) som ikke er synket til dette depotet.

## Implementation Approach
Vi vil følge en 3-faset tilnærming:
1. **Intern Verifisering**: Sjekke med nøkkelpersoner om utkast eksisterer.
2. **Ekstern Oppfølging**: Kontakte rådgivere (Vill Energi, R21, Naturforvalter).
3. **Integrering**: Oppdatere dashboard og argumentasjonsbase med nye data.

## Phase 1: Verifisering og Lokalisering
### Overview
Bekrefte om noe av dokumentasjonen allerede er produsert, men ikke arkivert korrekt.
### Changes Required:
#### 1. Prosjektledelse / Gabriel Bøen
**Handling**: Sjekke Google Drive-mappe "H13 Backup Process Nov 25" og "Natural State Files" for følgende:
- Geoteknisk rapport (Norconsult/Multiconsult?)
- Biologisk kartlegging (Eiriks notater)
- Overvannsberegninger (VA-notater)

#### 2. data/themes/environmental-arguments.json
**Changes**: Oppdatere `status` feltet i `missing_documents` dersom filer lokaliseres.

### Success Criteria:
#### Manual:
- [ ] Bekreftelse på om Eirik har et utkast til biologisk kartlegging.
- [ ] Avklaring på om det er utført grunnundersøkelser på tomta i 2024/2025.

## Phase 2: Bestilling og Oppfølging
### Overview
Bestille manglende analyser fra eksterne rådgivere.
### Actions:
#### 1. Vill Energi
**Handling**: Be om formell "Klimarisikovurdering H13" basert på kravene i e-post datert 2025-02-11.
#### 2. VA-Rådgiver
**Handling**: Innhente tilbud på spesifikk overvannsberegning for transformasjonsscenariet (Scenario 2/3).
#### 3. Byantikvaren
**Handling**: Sende forespørsel om antikvarisk vurdering.
#### 4. Bydel Ullern / Oslobygg KF
**Status**: ✅ **ANSKAFFET**
**Dokument**: Rammetillatelse, Ferdigattest og Tegninger for Skøyen Terrasse 1 (Sak 202453701).
**Funn**: Bekrefter setningsskader, skjevstilling og omfattende stålforsterkning i 2024/2025.

#### 5. Plan- og bygningsetaten (Saksinnsyn)
**Status**: ✅ **DELVIS ANSKAFFET**
- **Hoffsveien 17**: Miljøteknisk grunnundersøkelse (Multiconsult 2016) er analysert. Bekrefter forurensning og leire.
- **Gjenstår**: "GEOTEKNISK RAPPORT Nedre Skøyen vei 2" & "610419A OSLO RIDEHUS AS".

## Phase 3: Teknisk Integrering
### Overview
Når dokumenter mottas, skal de gjøres tilgjengelige i dashboardet.
### Changes Required:
#### 1. data/documents.json
**Changes**: Legge til nye PDF-referanser med korrekt metadata.
#### 2. data/themes/environmental-arguments.json
**Changes**: Flytte dokumenter fra `missing_documents` til `source_documents`.
**Changes**: Oppdatere styrkegraden på berørte argumenter (f.eks. fra `medium` til `strong` når proxy-data erstattes med fakta).

### Success Criteria:
#### Automated:
- [ ] `grep "missing_" data/themes/environmental-arguments.json | wc -l` (Expect 0 after phase 3)
- [ ] `node scripts/analyze-meeting-reports.py` (Verify no broken references)
#### Manual:
- [ ] Åpne `dashboard/miljo-argumenter.html` i browser.
- [ ] Bla ned til "Dokumenter som bør innhentes".
- [ ] Bekreft at seksjonen er tom eller viser "Alle dokumenter er nå på plass".
- [ ] Klikk på et argument (f.eks. "Klimafordel") og bekreft at kildereferansen peker på en gyldig lokal PDF.
