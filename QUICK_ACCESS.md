# 🚀 Quick Access Guide - Hovfaret 13 Dashboard

## Dashboard URLs

Assuming local server is running on port 8888:

```bash
cd dashboard
python3 -m http.server 8888
```

### Main Dashboards

| Dashboard | URL | Beskrivelse |
|-----------|-----|-------------|
| 🏠 **Homepage** | http://localhost:8888/index.html | Hovedside med alle dashboard-kort |
| 📊 **Prosjektoversikt** | http://localhost:8888/overview.html | Health indicators, beslutninger, actions |
| 📅 **Timeline** | http://localhost:8888/timeline-v2.html | Strategiske og operasjonelle hendelser |
| 📄 **Documents** | http://localhost:8888/documents.html | 271 dokumenter, søkbar |
| 👥 **Stakeholders** | http://localhost:8888/stakeholders.html | 22 personer, 13 organisasjoner |
| 📋 **Meetings** | http://localhost:8888/meetings.html | 45 møter med embedded notater |
| ♻️ **Scenarios** | http://localhost:8888/scenarios.html | 3 scenarier, CO₂-analyse |
| 🌱 **Sustainability** | http://localhost:8888/sustainability.html | ESRS-rapport, klimapåvirkning |

### Testing & Debug

| Tool | URL | Formål |
|------|-----|---------|
| 🧪 **Function Test** | http://localhost:8888/test-functions.html | Test DataLoader funksjoner |

## Quick Commands

### Start Server
```bash
cd /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard
python3 -m http.server 8888 &
```

### Open Homepage
```bash
open http://localhost:8888/index.html
```

### Open Prosjektoversikt
```bash
open http://localhost:8888/overview.html
```

### Hard Refresh (clear cache)
- **Mac:** `Cmd + Shift + R`
- **Windows:** `Ctrl + Shift + F5`

## Key Features Per Dashboard

### 📊 Prosjektoversikt
- 4 health indicator cards
- 8 key statistics
- Recent activity timeline (15 items)
- Decision tracker (all meetings)
- Action items tracker (with status)
- Stakeholder engagement (top 12)

### 📋 Meetings
- 45 meetings total
- 23 with embedded reports (51%)
- Expandable sections per meeting
- Color-coded: Green (summary/decisions), Orange (actions), Purple (quotes)
- Search and filter by type, org, participant

### 📅 Timeline
- 32 events (10 strategic, 22 operational)
- 3-layer views
- Meeting integration (14 events linked)
- Executive summaries
- Real-time search and filters

### 📄 Documents
- 271 documents
- 10 categories
- Search by filename, category, source
- Filter by type, category, source
- 5 sort modes

### 👥 Stakeholders
- 22 people with detailed profiles
- 13 organizations
- Meeting participation tracking
- Contact information
- Expertise areas

### ♻️ Scenarios
- 3 development scenarios
- CO₂ impact analysis
- Material emissions comparison
- Energy consumption
- Visual charts

## Data Files Location

```
/Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/
├── data/
│   ├── project.json
│   ├── timeline.json
│   ├── timeline-enhanced.json
│   ├── meetings.json (45 meetings, 23 with reports)
│   ├── documents.json (271 docs)
│   ├── stakeholders/
│   │   ├── people.json
│   │   └── organizations.json
│   └── themes/
│       ├── sustainability.json
│       ├── regulatory.json
│       └── omsorg-plus.json
└── dashboard/
    ├── index.html
    ├── overview.html (NEW)
    ├── timeline-v2.html
    ├── documents.html
    ├── stakeholders.html
    ├── meetings.html
    └── scenarios.html
```

## Latest Updates

**Version:** 2.22.0
**Date:** 2025-11-22
**Latest Features:**
- ✅ **Technical Theme Family** - 4 variasjoner av samme designspråk
- ✅ **Technical Dusk** - Standard tema (20% lysere enn original) ⭐
- ✅ Persistent theme valg på tvers av sider
- ✅ Real-time theme bytte uten page reload
- ✅ Bærekraftsrapport Dashboard (ESRS-compliant)
- ✅ CO₂ impact visualizations (-48% besparelse)
- ✅ Circular economy metrics (85% avfallsreduksjon)
- ✅ Energy performance tracking (F → C/B)
- ✅ Environmental benefits (Hoffselva protection)
- ✅ Fullstendig norsk oversettelse av alle dashboards
- ✅ ~165 tekststrenger oversatt til norsk
- ✅ Prosjektoversikt dashboard
- ✅ 8 new data extraction functions

## Theme Switcher - Technical Family

**Hvordan bruke:**
1. Åpne hvilket som helst dashboard
2. Se dropdown i navigasjonsbaren (øverst til høyre)
3. Velg lyshetsnivå: 🌙 Dark | 🌆 Dusk | 🌇 Twilight | 🌄 Day
4. Valget lagres automatisk og gjelder alle sider

**Standard tema:** Technical Dusk (🌆) - Subtilt lysere, optimal balanse

**Technical Theme Family:**
- **Technical Dark** 🌙 - Original mørkt (mørkest)
- **Technical Dusk** 🌆 - 20% lysere (standard) ⭐
- **Technical Twilight** 🌇 - 40% lysere (merkbar lysning)
- **Technical Day** 🌄 - 60% lysere (betydelig lysere)

**Design:** Alle temaer beholder samme visuell hierarki, typografi og accent-farger. Kun bakgrunnslysheten endres.

## Support

**Issues?**
1. Hard refresh browser (Cmd+Shift+R)
2. Check browser console (F12)
3. Verify server is running
4. Check STATUS.md for latest updates
5. Read CHANGELOG.md for version history

**Documentation:**
- `README.md` - Project overview
- `STATUS.md` - Current status
- `CHANGELOG.md` - Version history
- `SESSION_SUMMARY_2025-11-22.md` - Today's work
- `QUICK_ACCESS.md` - This file
