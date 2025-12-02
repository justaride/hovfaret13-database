# Embedded Meeting Reports - User Guide

## Overview

Meeting reports are now embedded directly in meeting cards in the Meeting Browser. No need to open external files - all content is accessible with expandable sections.

## How to Use

### 1. Open Meeting Browser

```bash
cd dashboard
python3 -m http.server 8888
# Open http://localhost:8888/meetings.html
```

### 2. Find a Meeting

- Browse by month sections
- Use search bar to filter meetings
- Filter by type, organization, or participant
- Look for meetings with the green file icon (📄) - these have embedded reports

### 3. Expand a Meeting Card

Click on any meeting header to expand it. You'll see:
- Meeting details (date, location, organizer)
- Participants list with avatars
- Topics discussed
- **Embedded Report** (if available)

### 4. Navigate the Report

**Always Visible:**
- **Summary** - Green box with key takeaways from the meeting

**Expandable Sections** (click header to expand):
- **Diskusjon** (Discussion) - Detailed meeting notes with subsections
- **Beslutninger** (Decisions) - Key decisions made in green boxes
- **Action Items** - Tasks with responsible person and deadline (orange boxes)
- **Viktige sitater** (Quotes) - Important quotes from participants
- **Kontekst og betydning** (Context) - Meeting's significance in project

## Visual Guide

### Report Sections Color Coding

- 🟢 **Green** - Summary & Decisions (positive actions)
- 🟠 **Orange** - Action Items (tasks to do)
- 🔵 **Purple** - Quotes (participant insights)
- ℹ️ **Blue** - Context (background information)

### Icons Used

- 📄 `file-text` - Summary section
- 💬 `message-square` - Discussion section
- ✅ `clipboard-check` - Decisions section
- ☑️ `check-square` - Action Items section
- 💭 `quote` - Quotes section
- ℹ️ `info` - Context section
- 🔽 `chevron-down` - Expandable section (rotates when expanded)

## Statistics

As of 2025-11-22:
- **45 total meetings** in database
- **23 meetings** have embedded reports
  - 23 with summaries
  - 23 with discussion sections
  - 8 with decisions
  - 7 with action items
  - 7 with quotes
  - 7 with context

## Example Meeting

**m_2024-03-11_urbania_hovfaret_13_konseptskisse_1_0**
- **Date:** 2024-03-11
- **Title:** Urbania Hovfaret 13 - Konseptskisse 1.0
- **Complete Report:**
  - Summary: 493 characters
  - Discussion: 6 sections
  - Decisions: 3 items
  - Action Items: 4 items (with responsible & deadlines)
  - Quotes: 1 item
  - Context: 781 characters

## Tips

1. **Scan Summaries** - All summaries are visible by default for quick overview
2. **Expand Selectively** - Click only the sections you need to read
3. **Search Within** - Use browser search (Cmd/Ctrl+F) to find specific content
4. **Mobile Friendly** - All sections are responsive and work on mobile devices

## Technical Details

**Files:**
- `dashboard/lib/renderer.js` - Rendering logic
- `dashboard/styles/embedded-reports.css` - Styling
- `data/meetings.json` - Meeting data with embedded reports

**Data Structure:**
```json
{
  "report": {
    "summary": "string",
    "topics": ["array"],
    "discussion": [{"heading": "string", "content": "string"}],
    "decisions": ["array"],
    "action_items": [{"task": "string", "responsible": "string", "deadline": "string"}],
    "quotes": ["array"],
    "context": "string"
  }
}
```

## Future Enhancements

Planned features:
- Cross-meeting search across all embedded reports
- Export report to PDF
- Link to related documents
- Timeline integration showing meeting context
- Analytics across all action items

---

**Last Updated:** 2025-11-22
**Status:** ✅ Complete - All 23 embedded reports rendering inline
