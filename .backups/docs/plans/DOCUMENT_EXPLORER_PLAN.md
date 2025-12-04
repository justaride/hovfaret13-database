# Document Explorer - Detaljert Plan

**Opprettet:** 2025-11-21
**Status:** Planning
**Mål:** Interaktivt søkbart dokumentbibliotek for Hovfaret 13-prosjektet

---

## 1. Oversikt

### Formål
Document Explorer skal gi brukere en strukturert oversikt over alle 271 prosjektdokumenter, med kraftig søk, filtrering og cross-referencing til andre deler av dashboardet.

### Datagrunnlag
- **Kilde:** `data/documents.json`
- **Antall:** 271 dokumenter
- **Kategorier:** 10 (sustainability, omsorg_plus, meetings, presentations, etc.)
- **Filtyper:** PDF, Google Docs, Excel, Word, Markdown

---

## 2. UI Mockup - Desktop

### A. Hovedvisning (Standard Layout)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🏗️ Hovfaret 13 → Document Explorer                           [HOME]    │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  📚 Document Explorer                                                   │
│                                                                         │
│  271 documents across 10 categories                                     │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  🔍 Search: [_________________________________]  🔄 Clear  📊 Stats     │
│                                                                         │
│  Filter by:                                                             │
│  Category: [All ▾] Type: [All ▾] Source: [All ▾] Sort: [Newest ▾]     │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  CATEGORIES (Click to expand/collapse)                                  │
│                                                                         │
│  ▼ 📊 Sustainability (8 documents)                    🔗 View all      │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ 📄 20250411 Energikartlegging Hovfaret 13.pdf                     │ │
│  │    PDF • 2025-04-11 • Klimagass og energi beregninger             │ │
│  │    🔗 View • 📎 Linked to: s_007 (Climate Calculations)           │ │
│  ├───────────────────────────────────────────────────────────────────┤ │
│  │ 📄 Klimagassberegninger Hovfaret 13 v2.pdf                        │ │
│  │    PDF • 2025-04-22 • Klimagass og energi beregninger             │ │
│  │    🔗 View • 📎 Linked to: s_007, s_008                           │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ▶ 🏥 Omsorg+ (25 documents)                          🔗 View all      │
│                                                                         │
│  ▼ 📑 Presentations (61 documents)                    🔗 View all      │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ 📄 06.03.25 Hovfaret 13 - Konseptskisse 1.6.pdf                   │ │
│  │    PDF • 2025-03-06 • MIRO ting. MØTE RAPPORTER                   │ │
│  │    🔗 View • 📎 No links                                          │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ▶ 📝 Meetings (51 documents)                         🔗 View all      │
│  ▶ 🏗️ Architecture (9 documents)                     🔗 View all      │
│  ▶ ⚖️ Regulatory (5 documents)                       🔗 View all      │
│  ▶ 👥 Stakeholder Engagement (5 documents)           🔗 View all      │
│  ▶ 📋 Analysis Notes (94 documents)                  🔗 View all      │
│  ▶ 📢 Communications (2 documents)                   🔗 View all      │
│  ▶ 📦 Other (11 documents)                           🔗 View all      │
└─────────────────────────────────────────────────────────────────────────┘
```

### B. Expanded Document Card (Click to expand)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📄 Klimagassberegninger Hovfaret 13 v2.pdf                      [✕]    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  📂 Category: Sustainability                                            │
│  📁 Source: Klimagass og energi beregninger                             │
│  📅 Date: 2025-04-22                                                    │
│  🗂️ Type: PDF Document                                                  │
│  🆔 ID: doc_klimagassberegninger_v2                                     │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  📝 DESCRIPTION                                                         │
│  Climate gas calculations comparing demolition vs rehabilitation.       │
│  Key findings: 48% lower CO₂ with rehabilitation (456 vs 631 kg/m²)    │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  🔗 RELATED TIMELINE EVENTS (2)                                         │
│  • s_007 - Climate Calculations Complete (2025-04-22)                  │
│  • s_008 - Sustainability Report Delivered (2025-07-04)                │
│                                                                         │
│  🔗 RELATED MEETINGS (1)                                                │
│  • m_2025-04-22 - Climate Review with Vill Energi                      │
│                                                                         │
│  👥 KEY PEOPLE                                                          │
│  • Trym Osborg (Vill Energi) - Lead author                             │
│  • Andreas Thorsnes (Urbania) - Reviewer                               │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  [📥 Download] [👁️ View Source] [🔗 Copy Link] [📋 Add to Report]     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### C. Search Results View

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🔍 Search results for "klimagass"                         [Clear ✕]    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Found 12 documents matching "klimagass"                                │
│                                                                         │
│  📊 SUSTAINABILITY (3)                                                  │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ 📄 Klimagassberegninger Hovfaret 13 v2.pdf                        │ │
│  │    ...calculations comparing demolition vs rehabilitation with    │ │
│  │    klimagass emissions. Key findings: 48% lower CO₂...            │ │
│  ├───────────────────────────────────────────────────────────────────┤ │
│  │ 📄 20250411 Energikartlegging Hovfaret 13.pdf                     │ │
│  │    ...energy mapping including klimagass footprint analysis...    │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  📑 PRESENTATIONS (5)                                                   │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ 📄 Hovfaret 13 - Klimastrategi presentasjon.pdf                   │ │
│  │    ...overview of climate strategy and klimagass reduction...     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  📝 MEETINGS (4)                                                        │
│  [Show more results...]                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### D. Stats Panel (Click 📊 Stats button)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 Document Statistics                                          [✕]    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TOTAL DOCUMENTS: 271                                                   │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────────│
│  BY CATEGORY                                                            │
│  ████████████████████████████████████  Analysis Notes (94)  34.7%      │
│  ██████████████████████  Presentations (61)  22.5%                      │
│  ███████████████  Meetings (51)  18.8%                                  │
│  ████  Omsorg+ (25)  9.2%                                               │
│  ██  Other (11)  4.1%                                                   │
│  █  Architecture (9)  3.3%                                              │
│  █  Sustainability (8)  3.0%                                            │
│  █  Stakeholder Engagement (5)  1.8%                                    │
│  █  Regulatory (5)  1.8%                                                │
│  █  Communications (2)  0.7%                                            │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────────│
│  BY FILE TYPE                                                           │
│  ████████████████████  Google Docs (102)  37.6%                         │
│  ████████████████  PDF (98)  36.2%                                      │
│  ████████  Markdown (47)  17.3%                                         │
│  ███  Excel (15)  5.5%                                                  │
│  █  Word (9)  3.3%                                                      │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────────│
│  TIMELINE                                                               │
│  Latest: 2025-11-20                                                     │
│  Oldest: 2023-02-01                                                     │
│  Peak activity: Q2 2025 (87 documents)                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. UI Mockup - Mobile

```
┌─────────────────────────┐
│ 🏗️ H13 → Documents  ☰  │
└─────────────────────────┘
│                         │
│  📚 Documents           │
│  271 docs • 10 cats     │
│                         │
│ [🔍 Search...]          │
│                         │
│ [Filter ▾] [Sort ▾]     │
│                         │
│ ▼ 📊 Sustainability (8) │
│ ┌─────────────────────┐ │
│ │ 📄 Energikart...    │ │
│ │ PDF • 2025-04-11    │ │
│ │ [View] [⋮]          │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ 📄 Klimagass...     │ │
│ │ PDF • 2025-04-22    │ │
│ │ [View] [⋮]          │ │
│ └─────────────────────┘ │
│                         │
│ ▶ 🏥 Omsorg+ (25)       │
│ ▶ 📑 Presentations (61) │
│                         │
└─────────────────────────┘
```

---

## 4. Functional Requirements

### A. Core Features (MVP)

1. **Category Browse**
   - Collapsible category sections
   - Document count badges
   - "View all" link per category
   - Default: All categories collapsed except first

2. **Document Cards**
   - Compact view (default): Title, type, date, source
   - Expanded view (on click): Full metadata + relationships
   - File type icons (PDF, GDoc, Excel, etc.)
   - Date formatting (Norwegian style: 22. april 2025)

3. **Search**
   - Real-time search across:
     - File names
     - Categories
     - Source folders
     - Document IDs
   - Highlight matching text in results
   - Debounced (300ms) for performance
   - Show result count

4. **Filtering**
   - **Category filter:** Dropdown with all 10 categories
   - **File type filter:** All / PDF / Google Docs / Excel / Word / Markdown
   - **Source folder filter:** Dropdown of unique source folders
   - Multiple filters can be active simultaneously
   - "Clear all filters" button

5. **Sorting**
   - Newest first (extraction_date DESC) - default
   - Oldest first (extraction_date ASC)
   - A-Z by filename
   - Z-A by filename
   - By category

### B. Enhanced Features (Phase 2)

6. **Statistics Panel**
   - Document count by category (bar chart)
   - Document count by file type (bar chart)
   - Timeline visualization (documents over time)
   - Most active source folders
   - Toggle open/close

7. **Cross-referencing** (requires data enhancement)
   - Link documents to timeline events
   - Link documents to meetings
   - Link documents to people (authors/reviewers)
   - Bidirectional navigation

8. **Document Actions**
   - View source (if available)
   - Download (if file accessible)
   - Copy document ID
   - Add to report/export list
   - Share link

9. **Bulk Operations**
   - Select multiple documents
   - Export metadata as CSV
   - Generate document list for report
   - Tag documents

### C. Future Features (Phase 3+)

10. **Full-text Search**
    - Search within extracted document content
    - Preview matching snippets

11. **Document Preview**
    - PDF preview in modal/side panel
    - Image preview for architectural drawings
    - Google Docs iframe embed

12. **Tagging System**
    - User-defined tags
    - Tag management
    - Filter by tags

13. **Version Control**
    - Track document versions (v1, v2, etc.)
    - Compare versions
    - Show update history

---

## 5. Data Structure

### A. Current Structure (documents.json)

```json
{
  "id": "doc_unique_id",
  "file_name": "filename.pdf",
  "file_type": "pdf_document",
  "document_type": "unknown",
  "category": "sustainability",
  "source_folder": "Folder name",
  "extraction_date": "2025-11-20T16:04:26.974526",
  "has_error": false
}
```

### B. Proposed Enhancements (Future)

Add these fields to each document:

```json
{
  "id": "doc_unique_id",
  "file_name": "filename.pdf",
  "file_type": "pdf_document",
  "document_type": "report",
  "category": "sustainability",
  "source_folder": "Folder name",
  "extraction_date": "2025-11-20T16:04:26.974526",
  "has_error": false,

  // NEW FIELDS (Phase 2)
  "description": "Brief description of document content",
  "date": "2025-04-22",  // Document date (not extraction date)
  "authors": ["trym_osborg"],  // Person IDs
  "reviewers": ["andreas_thorsnes"],
  "related_events": ["s_007", "s_008"],  // Timeline event IDs
  "related_meetings": ["m_2025-04-22"],  // Meeting IDs
  "tags": ["climate", "co2", "calculations"],
  "version": "v2",
  "file_path": "path/to/file.pdf",  // If accessible
  "file_size_bytes": 2458624,
  "page_count": 42,
  "language": "no"
}
```

### C. Cross-reference Mapping File (Optional)

Create `data/document-relationships.json`:

```json
{
  "version": "1.0",
  "last_updated": "2025-11-21",
  "relationships": [
    {
      "document_id": "doc_klimagassberegninger_v2",
      "timeline_events": ["s_007", "s_008"],
      "meetings": ["m_2025-04-22"],
      "authors": ["trym_osborg"],
      "reviewers": ["andreas_thorsnes"]
    }
  ]
}
```

---

## 6. Technical Implementation

### A. File Structure

```
dashboard/
├─ documents.html              # Main document explorer page
├─ lib/
│   ├─ data-loader.js          # Already exists - extend with document methods
│   ├─ renderer.js             # Already exists - add document rendering
│   └─ document-helpers.js     # NEW - Document-specific utilities
├─ skins/
│   └─ technical.css           # Extend with document explorer styles
└─ assets/
    └─ file-icons/             # SVG icons for file types
```

### B. Key Functions (document-helpers.js)

```javascript
// Group documents by category
function groupByCategory(documents) { ... }

// Filter documents
function filterDocuments(documents, { category, fileType, source, search }) { ... }

// Sort documents
function sortDocuments(documents, sortBy) { ... }

// Get unique file types
function getFileTypes(documents) { ... }

// Get unique source folders
function getSourceFolders(documents) { ... }

// Generate statistics
function calculateStats(documents) { ... }

// Format file size
function formatFileSize(bytes) { ... }

// Get file icon
function getFileIcon(fileType) { ... }
```

### C. Rendering Functions (renderer.js extension)

```javascript
// Render document card (compact)
function renderDocumentCard(doc, isExpanded = false) { ... }

// Render category section
function renderCategorySection(category, documents, isExpanded = false) { ... }

// Render search results
function renderSearchResults(documents, query) { ... }

// Render statistics panel
function renderStatsPanel(stats) { ... }

// Render filter controls
function renderFilters(activeFilters) { ... }
```

### D. Data Loading (data-loader.js extension)

```javascript
// Already exists, extend with:

// Search documents
function searchDocuments(query) {
  const docs = data.documents.documents;
  return docs.filter(doc =>
    doc.file_name.toLowerCase().includes(query.toLowerCase()) ||
    doc.category.toLowerCase().includes(query.toLowerCase()) ||
    doc.source_folder.toLowerCase().includes(query.toLowerCase())
  );
}

// Get documents by category
function getDocumentsByCategory(category) {
  return data.documents.documents.filter(d => d.category === category);
}

// Get document by ID
function getDocumentById(docId) {
  return data.documents.documents.find(d => d.id === docId);
}
```

### E. State Management

```javascript
// Document Explorer state
const docExplorerState = {
  search: '',
  filters: {
    category: 'all',
    fileType: 'all',
    source: 'all'
  },
  sort: 'newest',
  expandedCategories: new Set(),
  expandedDocuments: new Set(),
  showStats: false
};

// Update and re-render
function updateState(updates) {
  Object.assign(docExplorerState, updates);
  renderDocumentExplorer();
}
```

---

## 7. User Interactions

### A. Click Behaviors

| Element | Action | Result |
|---------|--------|--------|
| Category header | Toggle | Expand/collapse document list |
| Document card | Toggle | Expand/collapse full details |
| "View all" link | Navigate | Show category in expanded mode with all docs |
| Search input | Type | Real-time filter + highlight |
| Filter dropdown | Select | Apply filter + re-render |
| Sort dropdown | Select | Re-sort list |
| Stats button | Toggle | Show/hide statistics panel |
| File type icon | Click | Filter by that file type |
| Document link | Click | Open document (if available) or show detail modal |

### B. Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `/` | Focus search |
| `Esc` | Clear search / Close expanded card |
| `↓` | Next document |
| `↑` | Previous document |
| `Enter` | Expand/collapse selected document |
| `Ctrl+F` | Focus search (browser default) |

---

## 8. Performance Considerations

### A. Optimization Strategies

1. **Virtual Scrolling**
   - Only render visible documents (+ buffer)
   - Lazy load as user scrolls
   - Critical for Analysis Notes (94 docs)

2. **Debounced Search**
   - 300ms delay before search execution
   - Cancel previous search if new input

3. **Collapsed by Default**
   - Categories start collapsed
   - Reduce initial DOM size (271 cards → 10 headers)

4. **Progressive Enhancement**
   - Load basic list first
   - Add statistics/charts later

5. **Caching**
   - Cache filter results
   - Cache search results
   - Only re-render changed sections

### B. Load Time Targets

- Initial render: < 200ms
- Search response: < 100ms
- Filter application: < 50ms
- Category expand: < 50ms

---

## 9. Styling (Technical Skin)

### Color Scheme (Dark Theme)

```css
/* Categories */
--category-sustainability: #10B981;
--category-omsorg: #8B5CF6;
--category-meetings: #3B82F6;
--category-presentations: #F59E0B;
--category-architecture: #EF4444;
--category-regulatory: #EC4899;
--category-stakeholder: #06B6D4;
--category-analysis: #6B7280;
--category-communications: #14B8A6;
--category-other: #9CA3AF;

/* File types */
--file-pdf: #EF4444;
--file-gdoc: #3B82F6;
--file-excel: #10B981;
--file-word: #3B82F6;
--file-markdown: #F59E0B;
```

### Document Card States

```css
.document-card {
  /* Default: Subtle */
  background: rgba(20, 25, 31, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.document-card:hover {
  /* Hover: Lift */
  border-color: rgba(88, 166, 255, 0.4);
  transform: translateY(-2px);
}

.document-card.expanded {
  /* Expanded: Prominent */
  background: rgba(20, 25, 31, 0.9);
  border-color: rgba(88, 166, 255, 0.6);
}
```

---

## 10. Success Metrics

### Phase 1 (MVP) Complete When:

- [ ] All 271 documents displayed
- [ ] 10 categories rendered with correct counts
- [ ] Search works across filename, category, source
- [ ] Filter by category, file type, source works
- [ ] Sort by date, name works
- [ ] Categories expand/collapse
- [ ] Document cards expand/collapse
- [ ] Mobile responsive
- [ ] Navigation integrated
- [ ] Loads in < 500ms

### Phase 2 Complete When:

- [ ] Statistics panel functional
- [ ] Cross-references to timeline events
- [ ] Cross-references to meetings
- [ ] Author/reviewer links to people
- [ ] Document actions (view, download, copy)
- [ ] Bulk operations (export CSV)

---

## 11. Implementation Phases

### Phase 1: MVP (Estimated: 3-4 hours)

**Step 1: Data & Infrastructure** (30 min)
- Extend `data-loader.js` with document functions
- Create `document-helpers.js` with utilities
- Test data loading

**Step 2: Basic Rendering** (1 hour)
- Create `documents.html` structure
- Implement category sections
- Implement compact document cards
- Add navigation

**Step 3: Interaction** (1 hour)
- Category expand/collapse
- Document expand/collapse
- Basic state management

**Step 4: Search & Filter** (1 hour)
- Search input + real-time filtering
- Category dropdown filter
- File type dropdown filter
- Source dropdown filter
- Sort dropdown

**Step 5: Styling** (30-45 min)
- Apply technical skin
- File type icons
- Category colors
- Responsive mobile layout

**Step 6: Testing & Polish** (30 min)
- Test with all 271 documents
- Performance optimization
- Edge cases (empty categories, long filenames)

### Phase 2: Enhanced Features (Future)

- Statistics panel (1-2 hours)
- Cross-referencing (requires data enhancement first)
- Document actions
- Bulk operations

---

## 12. Design Decisions ✅ CONFIRMED

### User Decisions (2025-11-21):

1. **Default category state:** ✅ **All collapsed**
   - Cleaner initial view, faster load
   - User expands categories on demand

2. **File type icons:** ✅ **SVG icons**
   - More professional appearance
   - **Note:** Plan for holistic design system update across entire dashboard
   - Replace emojis throughout with consistent icon set

3. **Document links:** ✅ **Expand in place**
   - Click document card → expands to show full details
   - No modals or side panels for MVP

4. **Search scope:** ✅ **Filename/category/source for MVP**
   - Full-text content search added in Phase 2

5. **Source folder display:** ✅ **Truncate long names**
   - Compact view: Truncate with ellipsis (max 40 chars)
   - Expanded view: Show full name
   - Tooltip on hover shows full name

### Design System Note:

User plans to implement holistic design system with consistent iconography across dashboard. Current implementation should:
- Use SVG icons where possible
- Keep icon usage modular/replaceable
- Document all icon usage for easy bulk replacement
- Prepare for future design system integration

---

## 13. Next Steps

**After approval:**

1. Confirm UI design decisions (questions above)
2. Start Phase 1 implementation
3. Create `documents.html`
4. Extend `data-loader.js` and `renderer.js`
5. Test with real data
6. Deploy to dashboard

**Estimated total time for MVP:** 3-4 hours of focused work

---

## Appendix A: File Type Mapping

```javascript
const FILE_TYPE_MAP = {
  'pdf_document': { icon: '📄', label: 'PDF', color: '#EF4444' },
  'google_doc_link': { icon: '📝', label: 'Google Doc', color: '#3B82F6' },
  'generic_excel': { icon: '📊', label: 'Excel', color: '#10B981' },
  'word_document': { icon: '📝', label: 'Word', color: '#3B82F6' },
  'markdown_document': { icon: '📋', label: 'Markdown', color: '#F59E0B' },
  'unknown': { icon: '📎', label: 'File', color: '#9CA3AF' }
};
```

## Appendix B: Category Metadata

```javascript
const CATEGORY_META = {
  'sustainability': {
    icon: '📊',
    label: 'Sustainability',
    description: 'Energy reports, climate calculations, environmental assessments',
    color: '#10B981'
  },
  'omsorg_plus': {
    icon: '🏥',
    label: 'Omsorg+',
    description: 'Omsorg+ concept documents and references',
    color: '#8B5CF6'
  },
  // ... etc for all 10 categories
};
```

---

*End of Document Explorer Plan*
