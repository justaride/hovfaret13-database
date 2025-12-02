# Analyse: Norskifisering av Hovfaret 13 Dashboard

**Dato:** 2025-11-22
**Status:** Planlegging
**Mål:** All tekst på dashboardet skal være på norsk

---

## 📊 Oversikt

### Scope
Alle brukervendte dashboards skal være 100% på norsk:
- Overskrifter og titler
- Knapper og labels
- Feilmeldinger
- Beskrivelser
- Statuser og badges
- Navigation
- Tooltips og help-tekst

### Unntaker
Følgende skal forbli på engelsk:
- JavaScript variabelnavn
- CSS class names
- Teknisk kode
- Kommentarer i kode (valgfritt)
- Git commit messages (valgfritt)

---

## 🔍 Detaljert Analyse per Dashboard

### 1. index.html (Homepage)

**Engelske elementer:**

| Element | Nåværende (engelsk) | Ny (norsk) |
|---------|-------------------|-----------|
| Title | "Hovfaret 13 Dashboard" | "Hovfaret 13 Dashboard" (OK) |
| Badge | "Available" | "Tilgjengelig" |
| Badge | "Coming Soon" | "Kommer snart" |
| Card title | "Project Timeline" | "Prosjekttidslinje" |
| Card stat | "Events" | "Hendelser" |
| Card stat | "Meetings" | "Møter" |
| Card title | "Document Explorer" | "Dokumentutforsker" |
| Card stat | "Documents" | "Dokumenter" |
| Card stat | "Categories" | "Kategorier" |
| Card title | "Stakeholder Network" | "Interessentnettwerk" |
| Card stat | "People" | "Personer" |
| Card stat | "Organizations" | "Organisasjoner" |
| Card title | "Meeting Browser" | "Møteoversikt" |
| Card stat | "Participants" | "Deltakere" |
| Card title | "Scenario Comparison" | "Scenariosammenligning" |
| Card stat | "Scenarios" | "Scenarier" |
| Card title | "Sustainability Report" | "Bærekraftsrapport" |
| Info label | "Status:" | "Status:" (OK) |
| Info value | "Under planlegging" | "Under planlegging" (OK) |

**Estimat:** 15-20 tekststrenger

---

### 2. overview.html (Prosjektoversikt)

**Engelske elementer:**

| Element | Nåværende (engelsk) | Ny (norsk) |
|---------|-------------------|-----------|
| Title | "Project Overview - Hovfaret 13" | "Prosjektoversikt - Hovfaret 13" (delvis OK) |
| Section | "Recent Activity" | "Siste aktivitet" |
| Section | "Decision Tracker" | "Beslutningstracker" |
| Section | "Action Items Tracker" | "Handlingspunkttracker" |
| Section | "Stakeholder Engagement" | "Interessentengasjement" |
| Tab | "Decisions" | "Beslutninger" (delvis brukt) |
| Tab | "Action Items" | "Handlingspunkter" |
| Status badge | "pending" | "venter" |
| Status badge | "overdue" | "forfalt" |
| Status badge | "due-today" | "frist i dag" |
| Label | "meetings per month" | "møter per måned" |
| Label | "Total meetings" | "Totalt møter" |
| Label | "Past meetings" | "Avholdte møter" |
| Label | "Upcoming meetings" | "Kommende møter" |
| Label | "Total decisions" | "Totalt beslutninger" |
| Label | "Total action items" | "Totalt handlingspunkter" |
| Label | "Documents" | "Dokumenter" |
| Label | "Stakeholders" | "Interessenter" |
| Error msg | "Error loading data" | "Feil ved lasting av data" |
| Error msg | "No activity found" | "Ingen aktivitet funnet" |
| Error msg | "No decisions found" | "Ingen beslutninger funnet" |
| Error msg | "No action items found" | "Ingen handlingspunkter funnet" |
| Error msg | "No stakeholders found" | "Ingen interessenter funnet" |
| Label | "meetings" | "møter" (små bokstaver i stats) |
| Label | "Last meeting" | "Siste møte" |

**Estimat:** 30-40 tekststrenger

---

### 3. timeline-v2.html (Timeline)

**Engelske elementer:**

| Element | Nåværende (engelsk) | Ny (norsk) |
|---------|-------------------|-----------|
| Title | "Project Timeline - Hovfaret 13" | "Prosjekttidslinje - Hovfaret 13" |
| View button | "Strategic Events" | "Strategiske hendelser" |
| View button | "Operational Events" | "Operasjonelle hendelser" |
| View button | "All Events" | "Alle hendelser" |
| Filter | "Filter by Importance" | "Filtrer etter viktighet" |
| Filter option | "All" | "Alle" |
| Filter option | "Critical" | "Kritisk" |
| Filter option | "High" | "Høy" |
| Filter option | "Medium" | "Medium" (OK) |
| Filter | "Has Meeting" | "Har møte" |
| Search | "Search events..." | "Søk hendelser..." |
| Sort | "Sort by" | "Sorter etter" |
| Sort option | "Date (newest)" | "Dato (nyeste)" |
| Sort option | "Date (oldest)" | "Dato (eldste)" |
| Sort option | "Importance" | "Viktighet" |
| Label | "events found" | "hendelser funnet" |
| Section | "Executive Summary" | "Ledersammendrag" |
| Section | "Related Meetings" | "Relaterte møter" |
| Label | "participants" | "deltakere" |
| Section | "Related Documents" | "Relaterte dokumenter" |
| Indicator | "CRITICAL" | "KRITISK" |

**Estimat:** 25-35 tekststrenger

---

### 4. documents.html (Dokumentutforsker)

**Engelske elementer:**

| Element | Nåværende (engelsk) | Ny (norsk) |
|---------|-------------------|-----------|
| Title | "Document Explorer - Hovfaret 13" | "Dokumentutforsker - Hovfaret 13" |
| Heading | "Document Explorer" | "Dokumentutforsker" |
| Search | "Search documents..." | "Søk dokumenter..." |
| Filter | "Category" | "Kategori" |
| Filter | "File Type" | "Filtype" |
| Filter | "Source Folder" | "Kildemappe" |
| Filter option | "All Categories" | "Alle kategorier" |
| Filter option | "All Types" | "Alle typer" |
| Filter option | "All Sources" | "Alle kilder" |
| Sort | "Sort by" | "Sorter etter" |
| Sort option | "Newest" | "Nyeste" |
| Sort option | "Oldest" | "Eldste" |
| Sort option | "Name A-Z" | "Navn A-Å" |
| Sort option | "Name Z-A" | "Navn Å-A" |
| Sort option | "Category" | "Kategori" |
| Label | "documents found" | "dokumenter funnet" |
| Button | "Expand All" | "Utvid alle" |
| Button | "Collapse All" | "Skjul alle" |
| Section | "File Details" | "Fildetaljer" |
| Label | "Type:" | "Type:" (OK) |
| Label | "Size:" | "Størrelse:" |
| Label | "Category:" | "Kategori:" (OK) |
| Label | "Source:" | "Kilde:" |
| Label | "Date:" | "Dato:" (OK) |
| Empty state | "No documents found" | "Ingen dokumenter funnet" |

**Estimat:** 25-30 tekststrenger

---

### 5. stakeholders.html (Interessentnettwerk)

**Engelske elementer:**

| Element | Nåværende (engelsk) | Ny (norsk) |
|---------|-------------------|-----------|
| Title | "Stakeholder Network - Hovfaret 13" | "Interessentnettwerk - Hovfaret 13" |
| Heading | "Stakeholder Network" | "Interessentnettwerk" |
| Tab | "People" | "Personer" |
| Tab | "Organizations" | "Organisasjoner" |
| Search | "Search stakeholders..." | "Søk interessenter..." |
| Filter | "Category" | "Kategori" |
| Filter | "Organization Type" | "Organisasjonstype" |
| Filter option | "All" | "Alle" |
| Sort | "Sort by" | "Sorter etter" |
| Sort option | "Name A-Z" | "Navn A-Å" |
| Sort option | "Name Z-A" | "Navn Å-A" |
| Sort option | "Most Active" | "Mest aktive" |
| Label | "people found" | "personer funnet" |
| Label | "organizations found" | "organisasjoner funnet" |
| Section | "Contact" | "Kontakt" |
| Label | "Email:" | "E-post:" |
| Label | "Phone:" | "Telefon:" |
| Label | "Website:" | "Nettside:" |
| Label | "Role:" | "Rolle:" |
| Label | "Expertise:" | "Ekspertise:" |
| Label | "Bio:" | "Biografi:" |
| Label | "Team Members" | "Teammedlemmer" |
| Label | "Engagement:" | "Engasjement:" |
| Empty state | "No stakeholders found" | "Ingen interessenter funnet" |

**Estimat:** 25-30 tekststrenger

---

### 6. meetings.html (Møteoversikt)

**Engelske elementer:**

| Element | Nåværende (engelsk) | Ny (norsk) |
|---------|-------------------|-----------|
| Title | "Meeting Browser - Hovfaret 13" | "Møteoversikt - Hovfaret 13" |
| Heading | "Meeting Browser" | "Møteoversikt" |
| Tab | "All" | "Alle" |
| Tab | "Past" | "Tidligere" |
| Tab | "Upcoming" | "Kommende" |
| Search | "Search meetings..." | "Søk møter..." |
| Filter | "Meeting Type" | "Møtetype" |
| Filter | "Organization" | "Organisasjon" |
| Filter | "Participant" | "Deltaker" |
| Filter option | "All Types" | "Alle typer" |
| Filter option | "All Organizations" | "Alle organisasjoner" |
| Filter option | "All Participants" | "Alle deltakere" |
| Sort | "Sort by" | "Sorter etter" |
| Sort option | "Date (newest)" | "Dato (nyeste)" |
| Sort option | "Date (oldest)" | "Dato (eldste)" |
| Sort option | "Participant Count" | "Antall deltakere" |
| Label | "meetings found" | "møter funnet" |
| Section | "Participants" | "Deltakere" |
| Section | "Summary" | "Sammendrag" (delvis brukt) |
| Section | "Discussion" | "Diskusjon" (delvis brukt) |
| Section | "Decisions" | "Beslutninger" (delvis brukt) |
| Section | "Action Items" | "Handlingspunkter" (delvis brukt) |
| Section | "Important Quotes" | "Viktige sitater" (delvis brukt) |
| Section | "Context and Significance" | "Kontekst og betydning" (delvis brukt) |
| Label | "Data Quality:" | "Datakvalitet:" |
| Badge | "Reconstructed" | "Rekonstruert" |
| Empty state | "No meetings found" | "Ingen møter funnet" |

**Estimat:** 25-35 tekststrenger

---

### 7. scenarios.html (Scenariosammenligning)

**Engelske elementer:**

| Element | Nåværende (engelsk) | Ny (norsk) |
|---------|-------------------|-----------|
| Title | "Scenario Comparison - Hovfaret 13" | "Scenariosammenligning - Hovfaret 13" |
| Heading | "Scenario Comparison" | "Scenariosammenligning" |
| Section | "CO₂ per m²" | "CO₂ per m²" (OK) |
| Section | "Material Emissions" | "Materialutslipp" |
| Section | "Total CO₂" | "Totalt CO₂" (OK) |
| Section | "Energy Consumption" | "Energiforbruk" |
| Label | "vs Demolition" | "vs Riving" |
| Status | "Not recommended" | "Ikke anbefalt" |
| Status | "Recommended" | "Anbefalt" |
| Status | "Preferred" | "Foretrukket" |
| Label | "Best climate performance" | "Beste klimayting" |
| Label | "Best social benefit" | "Beste samfunnsnytte" |

**Estimat:** 15-20 tekststrenger

---

## 🗂️ JavaScript-filer som krever oversettelse

### lib/data-loader.js
**User-facing strings:**
- "Failed to load" → "Kunne ikke laste"
- "Error loading" → "Feil ved lasting"
- Få eller ingen brukervendte strenger

### lib/renderer.js
**User-facing strings:**
- "TBD" → "Ikke bestemt"
- "participants" → "deltakere"
- "No meetings found" → "Ingen møter funnet"
- Diverse labels i rendering

### lib/meeting-helpers.js
**Meeting type names:**
- "Core Team" → "Kjernegruppe"
- "Project Group" → "Prosjektgruppe"
- "External" → "Eksterne"
- "Government" → "Offentlig"
- "Tenant" → "Leietaker"
- "Site Visit" → "Befaring"
- "Workshop" → "Workshop" (OK)
- "Status" → "Status" (OK)
- "Other" → "Andre"

**Estimat:** 20-30 tekststrenger

---

## 📋 Oppsummering

### Total antall tekststrenger å oversette:

| Dashboard/Fil | Antall strenger | Prioritet |
|---------------|----------------|-----------|
| index.html | 15-20 | Høy |
| overview.html | 30-40 | Kritisk |
| timeline-v2.html | 25-35 | Høy |
| documents.html | 25-30 | Høy |
| stakeholders.html | 25-30 | Høy |
| meetings.html | 25-35 | Høy |
| scenarios.html | 15-20 | Medium |
| JavaScript files | 20-30 | Høy |
| **TOTALT** | **180-240** | - |

---

## 🎯 Implementeringsplan

### Fase 1: Kritiske dashboards (Prioritet 1)
**Estimert tid:** 2-3 timer

1. **overview.html** (30-40 strenger)
   - Health indicator labels
   - Status badges
   - Error messages
   - Tab names

2. **index.html** (15-20 strenger)
   - Card titles
   - Badge texts
   - Stats labels

### Fase 2: Hoveddashboards (Prioritet 2)
**Estimert tid:** 3-4 timer

3. **meetings.html** (25-35 strenger)
   - Search/filter labels
   - Section headers
   - Meeting type names

4. **timeline-v2.html** (25-35 strenger)
   - View buttons
   - Filter labels
   - Sort options

5. **documents.html** (25-30 strenger)
   - Category names
   - File type labels
   - Sort options

6. **stakeholders.html** (25-30 strenger)
   - Tab names
   - Contact labels
   - Filter options

### Fase 3: Sekundære dashboards (Prioritet 3)
**Estimert tid:** 1-2 timer

7. **scenarios.html** (15-20 strenger)
   - Chart labels
   - Status indicators
   - Section headers

### Fase 4: JavaScript-filer (Prioritet 4)
**Estimert tid:** 2-3 timer

8. **lib/renderer.js**
   - User-facing messages
   - Labels and tooltips

9. **lib/meeting-helpers.js**
   - Meeting type translations
   - Helper text

10. **lib/data-loader.js**
    - Error messages
    - Status messages

---

## 🛠️ Teknisk Tilnærming

### Metode 1: Direct Translation (Anbefalt for mindre filer)
Direkte søk-og-erstatt i HTML/JS filer.

**Fordeler:**
- Rask implementering
- Full kontroll
- Ingen nye dependencies

**Ulemper:**
- Kan bli rotete i store filer
- Må oppdatere på flere steder

### Metode 2: i18n Object (Anbefalt for JavaScript)
Opprett oversettelser-objekt:

```javascript
const translations = {
  en: {
    'loading': 'Loading...',
    'error': 'Error',
    'noData': 'No data found'
  },
  no: {
    'loading': 'Laster...',
    'error': 'Feil',
    'noData': 'Ingen data funnet'
  }
};

function t(key) {
  return translations['no'][key] || key;
}
```

**Fordeler:**
- Organisert
- Lett å vedlikeholde
- Kan enkelt bytte språk

**Ulemper:**
- Krever refactoring av eksisterende kode

### Metode 3: Hybrid (Anbefalt)
- **HTML-filer**: Direct translation
- **JavaScript-filer**: i18n object for brukervendte meldinger

---

## 📝 Oversettelsesguide

### Viktige oversettelser:

| Engelsk | Norsk | Kontekst |
|---------|-------|----------|
| Available | Tilgjengelig | Badge status |
| Coming Soon | Kommer snart | Badge status |
| Error loading data | Feil ved lasting av data | Error message |
| No data found | Ingen data funnet | Empty state |
| Search | Søk | Button/placeholder |
| Filter by | Filtrer etter | Label |
| Sort by | Sorter etter | Label |
| Expand | Utvid | Button |
| Collapse | Skjul | Button |
| Show more | Vis mer | Link |
| Show less | Vis mindre | Link |
| Loading... | Laster... | Status |
| Pending | Venter | Status |
| Overdue | Forfalt | Status |
| Completed | Fullført | Status |
| Critical | Kritisk | Priority |
| High | Høy | Priority |
| Medium | Medium | Priority |
| Low | Lav | Priority |
| Total | Totalt | Aggregation |
| Average | Gjennomsnitt | Calculation |
| Summary | Sammendrag | Section |
| Details | Detaljer | Section |
| All | Alle | Filter option |
| None | Ingen | Empty value |

---

## ✅ Testing Plan

### Pre-translation Testing
1. Dokumenter nåværende funksjonalitet
2. Ta screenshots av alle dashboards
3. Note ned edge cases

### Post-translation Testing
1. **Visual Testing**
   - Alle dashboards åpnes
   - Sjekk at tekst ikke bryter layout
   - Verifiser at norske tegn (æ, ø, å) vises korrekt

2. **Functional Testing**
   - Alle søk-funksjoner
   - Alle filter-funksjoner
   - Alle sorteringsfunksjoner
   - Alle interaktive elementer

3. **Cross-browser Testing**
   - Chrome
   - Firefox
   - Safari
   - Edge (hvis relevant)

4. **Responsive Testing**
   - Desktop (1920px)
   - Tablet (768px)
   - Mobile (375px)

### Akseptansekriterier
- ✅ Ingen engelsk tekst synlig for brukere
- ✅ All funksjonalitet fungerer som før
- ✅ Ingen layout-problemer
- ✅ Norske tegn vises korrekt
- ✅ Konsistent terminologi

---

## 📊 Risiko og Mitigering

### Risiko 1: Layout-problemer
**Beskrivelse:** Norske ord kan være lengre enn engelske, kan bryte design.

**Mitigering:**
- Test alle oversettelser i faktisk UI
- Juster CSS width/padding hvis nødvendig
- Bruk forkortelser der hensiktsmessig

### Risiko 2: Konsistens
**Beskrivelse:** Samme engelske ord oversettes forskjellig på ulike steder.

**Mitigering:**
- Opprett glossary/ordliste først
- Søk globalt for hvert ord før oversettelse
- Bruk søk-og-erstatt for konsistens

### Risiko 3: Kode-breaking
**Beskrivelse:** Oversettelse av strenger kan påvirke JavaScript-logikk.

**Mitigering:**
- Test grundig etter hver fil
- Ikke overset strenger brukt i kode-logikk
- Kun overset user-facing strings

---

## 🎯 Suksesskriterier

1. **100% norsk brukergrensesnitt**
   - Alle overskrifter, labels, knapper på norsk
   - Alle feilmeldinger på norsk
   - Alle statuser og badges på norsk

2. **Konsistent terminologi**
   - Samme norske ord for samme konsept overalt
   - Profesjonell språkbruk

3. **Bevart funksjonalitet**
   - Alle features fungerer som før
   - Ingen bugs introdusert

4. **God brukeropplevelse**
   - Naturlig norsk språk
   - Ikke direkte oversettelser som høres rart ut

---

## 📅 Estimert Tidsbruk

| Fase | Timer | Oppgaver |
|------|-------|----------|
| Analyse | ✅ 0.5 | Denne analysen |
| Fase 1 | 2-3 | Kritiske dashboards |
| Fase 2 | 3-4 | Hoveddashboards |
| Fase 3 | 1-2 | Sekundære dashboards |
| Fase 4 | 2-3 | JavaScript-filer |
| Testing | 1-2 | Omfattende testing |
| **TOTALT** | **9.5-14.5** | Full norskifisering |

---

## 🚀 Neste Steg

1. ✅ **Godkjenn analysen** - Les gjennom og godkjenn tilnærmingen
2. **Opprett glossary** - Standardiser oversettelser
3. **Start Fase 1** - Begynn med overview.html og index.html
4. **Iterativ implementering** - En fil om gangen
5. **Løpende testing** - Test etter hver fil
6. **Final review** - Gjennomgang av alt

---

*Analyse fullført: 2025-11-22*
*Neste: Venter på godkjenning og oppstart*
