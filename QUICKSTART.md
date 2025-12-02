# Quick Start Guide - Hovfaret 13 Dashboard

## View the Dashboard

### Option 1: Local Server (Recommended)

```bash
# Navigate to dashboard directory
cd /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard

# Start simple HTTP server
python3 -m http.server 8888

# Open homepage in browser
open http://localhost:8888/index.html
```

**Dashboard is now running at:**
- **Homepage:** http://localhost:8888/index.html
- **Timeline:** http://localhost:8888/timeline-v2.html

### Option 2: Direct File Open

Due to CORS restrictions with JSON loading, this won't work. Use Option 1.

---

## Homepage Features

### 🏠 Dashboard Hub

**URL:** http://localhost:8888/index.html

The homepage provides:

**Hero Section:**
- Elegant glassmorphic box with backdrop blur
- "Hovfaret 13" title in Space Grotesk font (modern geometric)
- "videre bruk" handwritten tagline in Caveat font
- Blue accent border with hover glow effect
- Fullscreen building background (8% opacity)

**Project Overview:**
- Location: Hovfaret 13, Skøyen, Oslo
- Built: 1989
- Area: 6,100 m² BTA
- CO₂ savings: 48% lower vs demolition
- Owner: Urbania Eiendom AS
- Status: Under planlegging

**Dashboard Cards:**
1. ✅ **Project Timeline** (available) - Click to view
2. 🔜 Document Explorer (coming soon)
3. 🔜 Stakeholder Network (coming soon)
4. 🔜 Scenario Comparison (coming soon)
5. 🔜 Meeting Browser (coming soon)
6. 🔜 Sustainability Report (coming soon)

### 🧭 Navigation

All pages have a sticky navigation bar:
- **🏗️ Hovfaret 13** (left) - Click to return to homepage
- **→ Current Page** (right) - Shows where you are

---

## Timeline Features

### 🎯 Timeline Views

**Strategic Overview (10 events)**
- Major milestones only
- Executive summary format
- Perfect for presentations

**Operational Timeline (22 events)**
- All project activities
- Complete audit trail
- Project management view

**All Events (32 events)**
- Combined chronological view
- Full project history

### 🔍 Search & Filter

**Search bar:**
- Search across events, meetings, people, documents
- Real-time results
- Multi-category display

**Filters:**
- **All** - Show everything
- **Critical** - Only critical importance events
- **Has Meetings** - Events with linked meetings

### 📋 Event Cards

**Collapsed state:**
- Date, title, description
- Indicators: meeting count, documents, importance

**Expanded state (click to expand):**
- Executive summary (3 bullet points)
- Related meetings with participant counts
- Related documents
- Tags and metadata

**Click on meeting → View meeting details** (side panel coming soon)

### 🎨 Technical Skin

- Dark theme optimized for readability
- Data-dense layout
- Progressive disclosure (click to expand)
- Responsive design (mobile + desktop)
- Importance-based color coding:
  - 🔴 Critical = Red border
  - 🟠 High = Orange border
  - 🟡 Medium = Yellow border

---

## Project Structure

```
dashboard/
├── index.html                # Homepage (dashboard hub)
├── timeline-v2.html          # Timeline view (Technical Skin)
├── timeline.html             # v1 reference (basic 3-view)
├── lib/
│   ├── navigation.js         # Reusable navigation component
│   ├── data-loader.js        # Data loading + search + filters
│   └── renderer.js           # Event cards + rendering
├── skins/
│   └── technical.css         # Dark theme styling (includes nav)
├── assets/
│   └── building-elevation.png # Building image (add your own)
└── data/ → ../data           # Symlink to data files

data/
├── timeline-enhanced.json    # Timeline with meeting links + exec summaries
├── meetings.json             # 37 meetings
├── documents.json            # 271 documents
├── project.json              # Building info + scenarios
├── stakeholders/
│   ├── people.json           # 22 people
│   └── organizations.json    # 13 orgs
└── themes/
    ├── sustainability.json
    ├── regulatory.json
    └── omsorg-plus.json
```

---

## Key Statistics

**Timeline Coverage:**
- Strategic events: 10
- Operational events: 22
- Total events: 32
- Date range: 1989 → Q4 2025

**Data Integration:**
- Events with exec summaries: 10/10 (100%)
- Strategic events with meetings: 4/10 (40%)
- Operational events with meetings: 10/22 (45%)
- Total meetings: 37
- Total documents: 271
- Total people: 22

**Phase Coverage:**
- Phase 1 (1989-2010): Historical context
- Phase 2 (2023-09): Demolition requirement
- Phase 3 (2024-03 to 2024-05): Project start
- Phase 4 (2024-10 to 2024-12): Scenario development
- Phase 5 (2025-01 to 2025-05): Core deliverables
- Phase 6 (2025-07 to 2025-Q4): Application preparation

---

## Keyboard Shortcuts

- **Click event card** → Expand/collapse
- **Click meeting link** → View meeting details
- **Type in search** → Real-time search (2+ chars)
- **Click result** → Jump to event

---

## Development

### Rebuild Enhanced Timeline

If you update meetings or want to regenerate the enhanced timeline:

```bash
cd /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified

# Analyze current matching
node scripts/match-timeline-meetings.js

# Rebuild enhanced timeline
node scripts/build-enhanced-timeline.js
```

This will regenerate `data/timeline-enhanced.json` with updated meeting links.

### Add New Executive Summary

Edit `scripts/build-enhanced-timeline.js`:

```javascript
const execSummaries = {
  "s_XXX": {
    "exec_summary": [
      "Bullet point 1",
      "Bullet point 2",
      "Bullet point 3"
    ],
    "related_documents": ["doc_id_1", "doc_id_2"]
  }
};
```

Then rebuild:
```bash
node scripts/build-enhanced-timeline.js
```

---

## Next Steps (Phase 3)

Planned components:

1. **Document Explorer** - Searchable index of 271 documents
2. **Stakeholder Network** - Interactive visualization of 22 people, 13 orgs
3. **Scenario Comparison** - Visual comparison of 6 scenarios with CO₂/cost data
4. **Meeting Browser** - Dedicated view for 37 meetings with full content

---

## Adding Building Image

To display the architectural elevation as fullscreen background:

1. **Get your image:**
   - Should be an architectural elevation/facade drawing
   - PNG format with transparent background works best
   - Any size works (will scale to cover screen)
   - White/light lines on dark/transparent background ideal

2. **Save from Claude chat or copy to assets:**
   ```bash
   # Option 1: Right-click image in Claude chat → Save Image As
   # Navigate to: dashboard/assets/
   # Name it: building-elevation.png

   # Option 2: Copy from another location
   cp /path/to/your/building-drawing.png \
      dashboard/assets/building-elevation.png
   ```

3. **Refresh homepage:**
   - Reload http://localhost:8888/index.html
   - Building will appear as fullscreen background (8% opacity)
   - Subtle, elegant presence behind all content

**How it appears:**
- Fixed position - follows as you scroll
- Covers entire viewport
- 8% opacity (subtle but visible)
- Centers and scales automatically
- Adds depth without overwhelming

**Adjust opacity (optional):**
Edit `index.html` line ~23:
```css
opacity: 0.08;  /* Change 0.06-0.12 for more/less visible */
```

---

## Troubleshooting

**Problem:** Files not loading (404 errors)

**Solution:**
1. Make sure you're using `python3 -m http.server` from the `dashboard/` directory
2. Check that `data` symlink exists: `ls -la dashboard/data`
3. If symlink missing: `cd dashboard && ln -sf ../data data`

**Problem:** Search not working

**Solution:**
- Make sure you're typing at least 2 characters
- Check browser console for errors (F12 → Console tab)

**Problem:** Events not expanding

**Solution:**
- Click on the event card itself, not just the title
- Check browser console for JavaScript errors

---

## File Locations

- **Dashboard:** `/Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard/timeline-v2.html`
- **Data:** `/Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/data/`
- **Source docs:** `/Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/source/`

---

**Version:** 2.8.0 (Refined Homepage Design)
**Last Updated:** 2025-11-21
**Status:** ✅ Phase 2++ Complete

**Main Entry Point:** http://localhost:8888/index.html

**Latest Design:**
- Glassmorphic hero box
- Space Grotesk + Caveat typography
- Fullscreen building background
- "videre bruk" handwritten tagline
