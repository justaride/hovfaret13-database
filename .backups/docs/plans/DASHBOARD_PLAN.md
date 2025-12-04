# Dashboard Plan - Hovfaret 13

**Created:** 2025-11-21
**Status:** Phase 1 Complete, Phase 2 Ready to Start

---

## Vision

Multi-skin dashboard system with **depth-first** approach:
- **Technical Skin** (default): Full data access, all details, power-user features
- **Public Skin** (future): Storytelling for website, curated content
- **Executive Skin** (future): Presentation mode, high-level overview

**Core Principle:** Single source of truth (JSON data) → Multiple presentation layers

---

## Architecture Strategy: Multi-Skin System

```
Data Layer (JSON files)
    ↓
Business Logic Layer (data-loader.js, renderer.js)
    ↓
Presentation Layer (skins/)
    ├─ Technical Skin (dark, data-dense) ← PHASE 2
    ├─ Public Skin (brand, storytelling)
    └─ Executive Skin (light, high-level)
```

### Key Design Decisions:

1. **Depth-first**: Full detail available in technical skin, progressively simplified in other skins
2. **Component-based**: Reusable rendering functions
3. **CSS-scoped**: Each skin has own stylesheet
4. **Regenerate over real-time**: Export to new HTML for different contexts (not live skin-switching)

---

## Phase 1: Foundation ✅ COMPLETE

**Date:** 2025-11-21

### Completed:
- [x] Data structure verified and enriched
- [x] Timeline data verified (5 key dates confirmed)
- [x] People bios enriched (7 stakeholders)
- [x] Meetings cleaned (5 corrupted entries fixed)
- [x] Basic timeline.html created (strategic/operational/all views)

### Files Created:
- `dashboard/timeline.html` - Basic 3-view timeline
- `data/timeline.json` v2.1 - Verified
- `data/people.json` v2.1 - Enriched
- `data/meetings.json` v2.1 - Cleaned

---

## Phase 2: Technical Skin (Deep Timeline) 🎯 NEXT

**Goal:** Rebuild timeline with full depth, meeting integration, document links

### Architecture:

```
dashboard/
├─ data/                    # Symlink to ../data
├─ lib/
│   ├─ data-loader.js       # Load all JSON (meetings, timeline, docs, people)
│   ├─ renderer.js          # Core rendering logic
│   ├─ meeting-matcher.js   # Match timeline events to meetings
│   └─ skins.js             # Skin configuration registry
├─ skins/
│   ├─ technical.css        # Dark theme, full density
│   ├─ executive.css        # (future)
│   └─ public.css           # (future)
├─ timeline-v2.html         # New technical skin version
└─ timeline.html            # Keep v1 for reference
```

### Features to Build:

**A. Data Integration**
- [ ] Match timeline events to meetings by date
- [ ] Extract exec summaries from meeting notes
- [ ] Link related documents to events
- [ ] Show participants for each event

**B. Enhanced Timeline Events**

Each event card will show:
```
┌─────────────────────────────────────┐
│ 📅 2025-04-22                       │
│ Climate Calculations Complete       │
│ Klimaberegninger ferdigstilt        │
│ ✓ Verified                          │
├─────────────────────────────────────┤
│ EXECUTIVE SUMMARY:                  │
│ • 48% lower CO₂ vs demolition       │
│ • 456 vs 631 kg CO₂-ekv/m² BTA      │
│ • Core sustainability argument      │
├─────────────────────────────────────┤
│ 👥 PARTICIPANTS:                    │
│ Trym Osborg (Vill Energi)           │
│ Andreas Thorsnes (Urbania)          │
├─────────────────────────────────────┤
│ 📄 DOCUMENTS:                       │
│ → Klimagassberegninger v2.pdf       │
│ → Energy Report 2025-04-11          │
├─────────────────────────────────────┤
│ [Read Meeting Notes] [Expand All]  │
└─────────────────────────────────────┘
```

**C. Navigation & Filtering**
- [ ] Search across events, meetings, participants
- [ ] Filter by phase, importance, participant, theme
- [ ] Timeline scrubber for quick navigation
- [ ] "Show only events with meetings" toggle

**D. Progressive Disclosure**
- Default: Collapsed with 2-3 bullet exec summary
- Hover: Show participants
- Click: Expand full details
- "Read meeting notes" → Side panel with full content

**E. Meeting Integration**

For events with linked meetings:
```json
{
  "id": "s_007",
  "date": "2025-04-22",
  "title": "Climate Calculations Complete",
  "linked_meeting_id": "m_2025-04-22_klimaberegninger",
  "exec_summary": [
    "48% lower CO₂ vs demolition",
    "456 vs 631 kg CO₂-ekv/m² BTA",
    "Core sustainability argument established"
  ],
  "participants_from_meeting": ["trym_osborg", "andreas_thorsnes"],
  "related_documents": [
    "doc_klimagassberegninger_v2",
    "doc_energy_report_2025_04_11"
  ]
}
```

---

## Phase 3: Additional Components

**Priority order:**

1. **Document Explorer** - Searchable index of 271 documents
2. **Stakeholder Network** - Interactive visualization of 22 people, 13 orgs
3. **Scenario Comparison** - Visual comparison of 6 scenarios with CO₂/cost data
4. **Meeting Browser** - Dedicated view for 37 meetings with search

---

## Phase 4: Public & Executive Skins

Build alternative presentations using same data:

**Public Skin:**
- Storytelling mode with scrollytelling
- Curated timeline (not all 32 events)
- Brand colors and animations
- Accessible, responsive

**Executive Skin:**
- Only critical events (importance: critical)
- High-level metrics
- Print-optimized
- Slide export capability

---

## Data Requirements for Phase 2

### Need to Create:

**A. Enhanced timeline.json entries**
```json
"linked_meeting_id": "m_2025-04-22_...",
"exec_summary": ["bullet 1", "bullet 2", "bullet 3"],
"key_decisions": ["decision 1", "decision 2"],
"next_actions": ["action 1", "action 2"],
"related_documents": ["doc_id_1", "doc_id_2"]
```

**B. Meeting extraction summaries**
- Auto-extract or manually curate from `extraction-cache/`
- Store in meetings.json or separate `meeting-summaries.json`

**C. Document registry enhancements**
- Add `related_to_event_ids` array to documents.json
- Create reverse lookup capability

---

## Technical Considerations

### Performance:
- **Lazy loading**: Only render visible events initially
- **Virtual scrolling**: For full 32-event operational view
- **Debounced search**: Don't search on every keystroke

### Maintainability:
- **Single data source**: All skins read same JSON
- **Modular rendering**: Each component isolated
- **CSS scoping**: `.skin-technical`, `.skin-public`, etc.

### Export/Regeneration:
```javascript
// Generate standalone HTML for presentation
function exportToExecutiveSkin() {
  const events = filterCriticalEvents();
  const html = renderWithSkin(events, skins.executive);
  downloadAsHTML(html, 'hovfaret13-executive-timeline.html');
}
```

---

## Success Metrics

**Phase 2 Complete When:**
- [ ] All 10 strategic events have exec summaries
- [ ] Events with meetings show participant info
- [ ] Click event → see meeting details
- [ ] Search works across events/meetings/people
- [ ] Can filter by multiple criteria
- [ ] Related documents linkable
- [ ] Technical skin is fully functional

---

## Next Session Checklist

Before starting Phase 2 implementation:
1. ✅ Read this DASHBOARD_PLAN.md
2. ✅ Review CHANGELOG.md for current state
3. ✅ Check STATUS.md for any blockers
4. Start with data enhancement (match meetings to events)
5. Build data-loader.js infrastructure
6. Create timeline-v2.html with technical skin

---

## Open Questions

1. **Meeting summaries**: AI-extract or manual curation?
   - *Decision pending: Start with manual for critical events, automate later*

2. **Document storage**: Keep in documents.json or separate file?
   - *Decision pending: Discuss in Phase 2*

3. **Side panel vs modal**: For full meeting content?
   - *Leaning towards: Side panel (better UX for reference)*

