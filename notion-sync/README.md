# Hovfaret 13 → Notion Sync

Syncs project data from JSON files to Notion databases.

## Quick Start

```bash
cd notion-sync
npm run sync
```

## Configuration

### Environment Variables (`.env`)

```bash
NOTION_TOKEN=ntn_xxx                    # Notion integration token
NOTION_PAGE_ID=2c720392ef5b80d3...      # Target Notion page ID
DATA_DIR=/path/to/data                  # Source data directory
```

### Getting a Notion Token

1. Go to https://www.notion.so/my-integrations
2. Create new integration (Internal)
3. Copy the token
4. Add target page to integration's "Content Capabilities"

## Commands

```bash
npm run sync              # Full sync (all databases)
npm run sync:dry          # Dry run (no changes)
npm run sync -- --db=meetings    # Sync specific database
npm run sync -- --force   # Force recreate all records
```

## Databases Synced

| Database | Records | Source File |
|----------|---------|-------------|
| Organizations | 16 | `stakeholders/organizations.json` |
| People | 23 | `stakeholders/people.json` |
| Meetings | 70 | `meetings.json` |
| Documents | 271 | `documents.json` |
| Timeline | 32 | `timeline.json` |
| Deliverables | 37 | `deliverables.json` |
| **Omsorg+ Concept** | 1 | `themes/omsorg-plus.json` |
| **Omsorg+ Floors** | 7 | `themes/omsorg-plus.json` |
| **Omsorg+ Units** | 73 | `themes/omsorg-plus.json` |
| **Omsorg+ Facilities** | 11 | `themes/omsorg-plus.json` |
| **Omsorg+ Compliance** | 5 | `themes/omsorg-plus.json` |
| Sustainability | 3 | `themes/sustainability.json` |

**Total: 549 records across 12 databases**

## Project Structure

```
notion-sync/
├── package.json
├── .env                    # Config (not in git)
├── .env.example            # Template
├── scripts/                # Data enrichment scripts
│   ├── enrich-meetings.js
│   ├── enrich-timeline.js
│   └── enrich-deliverables.js
├── src/
│   ├── index.js           # Main entry point
│   ├── config.js          # Environment config
│   ├── notion-client.js   # Notion API client
│   ├── rate-limiter.js    # API rate limiting
│   ├── id-mapper.js       # Local↔Notion ID mapping
│   └── transformers/      # JSON → Notion transformers
│       ├── index.js
│       ├── organizations.js
│       ├── people.js
│       ├── meetings.js
│       ├── documents.js
│       ├── deliverables.js
│       ├── timeline.js
│       ├── sustainability.js
│       └── omsorg-plus/   # Expanded Omsorg+ transformers
│           ├── index.js
│           ├── concept.js
│           ├── floors.js
│           ├── units.js
│           ├── facilities.js
│           └── compliance.js
└── cache/
    └── id-map.json        # Persistent ID mappings
```

## How It Works

### Sync Process

1. **Phase 1: Create Databases** - Creates Notion databases under target page
2. **Phase 2: Sync Records** - Creates/updates pages in each database
3. **Phase 3: Link Relations** - Connects People → Organizations

### ID Mapping

- Local IDs (from JSON) are mapped to Notion page IDs
- Stored in `cache/id-map.json`
- Enables re-running sync to update existing records

### Rate Limiting

- 3 requests/second (Notion API limit)
- Automatic retry with exponential backoff
- Max 3 retry attempts

## Omsorg+ Database Structure

The Omsorg+ data is split into 5 related databases:

### Omsorg+ Concept (1 record)
Central metadata: purpose, target group, financing, market position.

### Omsorg+ Floors (7 records)
Floor-by-floor breakdown: U2, U1, Ground, 2-4, 5, 6-8, Roof.

### Omsorg+ Units (73 records)
Individual housing units with room features:
- 66 single rooms (42.1 m²)
- 7 double rooms (66.5 m²)
- Full room feature lists (living, bedroom, bathroom, entrance, balcony)

### Omsorg+ Facilities (11 records)
Common facilities: activity rooms, café, healthcare services, elevators.

### Omsorg+ Compliance (5 records)
Husbanken requirements: location, construction, installations, energy, security.

## Data Enrichment Scripts

Run these to improve source data quality:

```bash
# Add outcomes to meetings without them
node scripts/enrich-meetings.js

# Add descriptions and Norwegian titles to timeline
node scripts/enrich-timeline.js

# Assign responsible persons and Norwegian titles to deliverables
node scripts/enrich-deliverables.js
```

## Notion Property Types

| JSON Type | Notion Type | Example |
|-----------|-------------|---------|
| String | `title` | `{ title: [{ text: { content: 'Name' } }] }` |
| String | `rich_text` | `{ rich_text: [{ text: { content: 'Text' } }] }` |
| String | `select` | `{ select: { name: 'Option' } }` |
| Array | `multi_select` | `{ multi_select: [{ name: 'Tag1' }, { name: 'Tag2' }] }` |
| Date | `date` | `{ date: { start: '2025-01-01' } }` |
| Number | `number` | `{ number: 42 }` |
| Boolean | `checkbox` | `{ checkbox: true }` |
| String | `url` | `{ url: 'https://...' }` |
| String | `email` | `{ email: 'x@y.com' }` |
| ID | `relation` | `{ relation: [{ id: 'notion-page-id' }] }` |

## Troubleshooting

### "Page not found" Error

- Ensure page is shared with integration
- Go to integration settings → Add page

### "Can't create databases parented by a database"

- Target must be a **page**, not a database
- Check that NOTION_PAGE_ID points to a page

### Multi-select Comma Error

- Notion doesn't allow commas in multi-select options
- Transformer replaces `,` with `;`

### Rate Limiting

- Script handles automatically with retry
- If persistent, increase delay in `rate-limiter.js`

## Notion URLs

- **Target Page**: https://www.notion.so/Hovfaret-13-2c720392ef5b80d3baa1cb77261199d3
- **Integration Settings**: https://www.notion.so/my-integrations

## Current Database IDs

```json
{
  "organizations": "2c720392-ef5b-81ea-9f00-e966eb6b9a91",
  "people": "2c720392-ef5b-8153-b989-dc6ea3ed9e15",
  "meetings": "2c720392-ef5b-81bf-a2ce-f9712f077041",
  "documents": "2c720392-ef5b-8175-9e8f-d3cae6deb0c1",
  "timeline": "2c720392-ef5b-81bf-8f2b-cbaf5a0bea27",
  "deliverables": "2c720392-ef5b-8169-9cec-f05e6351c10a",
  "omsorgPlusConcept": "2c720392-ef5b-8161-a42f-ca77d2935211",
  "omsorgPlusFloors": "2c720392-ef5b-8166-ba9b-c08246111743",
  "omsorgPlusUnits": "2c720392-ef5b-8181-94b9-c9481e7699fa",
  "omsorgPlusFacilities": "2c720392-ef5b-8122-be31-c8817eef06a3",
  "omsorgPlusCompliance": "2c720392-ef5b-81ac-b15e-d12582a5ee1f",
  "sustainability": "2c720392-ef5b-81ad-9552-d5a92e233bb6"
}
```

## Data Quality (as of 2025-12-12)

| Data | Status | Coverage |
|------|--------|----------|
| Meetings with outcomes | ✅ | 100% (70/70) |
| Timeline with descriptions | ✅ | 100% (32/32) |
| Deliverables with responsible | ✅ | 100% (37/37) |
| People with email | ⚠️ | 74% (17/23) |
| Omsorg+ data coverage | ✅ | 100% |

## Future Improvements

- [ ] Add Participants relation (Meetings → People)
- [ ] Add Responsible relation (Deliverables → People)
- [ ] Two-way sync (Notion → JSON)
- [ ] Webhook for real-time updates
- [ ] Add missing emails for 6 government stakeholders

---

Created: 2025-12-12
Last Sync: 549 records (12 databases)
Version: 2.0
