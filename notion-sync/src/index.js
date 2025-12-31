import { notion, testConnection } from './notion-client.js';
import { withRetry } from './rate-limiter.js';
import { idMapper } from './id-mapper.js';
import { NOTION_PAGE_ID, DATABASE_ORDER, DATABASE_NAMES } from './config.js';
import { getRecordIcon, getDatabaseIcon } from './visual-config.js';

import {
  loadOrganizations, organizationsSchema, transformOrganization,
  loadPeople, peopleSchema, transformPerson, getOrganizationId,
  loadMeetings, meetingsSchema, transformMeeting, getMeetingContent,
  loadDocuments, documentsSchema, transformDocument,
  loadDeliverables, deliverablesSchema, transformDeliverable,
  loadTimeline, timelineSchema, transformTimelineEvent,
  loadSustainabilityScenarios, sustainabilitySchema, transformSustainabilityScenario
} from './transformers/index.js';

// Omsorg+ expanded transformers
import {
  loadOmsorgPlusConcept, omsorgPlusConceptSchema, transformOmsorgPlusConcept,
  loadOmsorgPlusFloors, omsorgPlusFloorsSchema, transformOmsorgPlusFloor,
  loadOmsorgPlusUnits, omsorgPlusUnitsSchema, transformOmsorgPlusUnit,
  loadOmsorgPlusFacilities, omsorgPlusFacilitiesSchema, transformOmsorgPlusFacility,
  loadOmsorgPlusCompliance, omsorgPlusComplianceSchema, transformOmsorgPlusCompliance
} from './transformers/omsorg-plus/index.js';

const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');
const FORCE = args.includes('--force');
const SPECIFIC_DB = args.find(a => a.startsWith('--db='))?.split('=')[1];

const loaders = {
  organizations: loadOrganizations,
  people: loadPeople,
  meetings: loadMeetings,
  documents: loadDocuments,
  deliverables: loadDeliverables,
  timeline: loadTimeline,
  // Omsorg+ expanded databases
  omsorgPlusConcept: loadOmsorgPlusConcept,
  omsorgPlusFloors: loadOmsorgPlusFloors,
  omsorgPlusUnits: loadOmsorgPlusUnits,
  omsorgPlusFacilities: loadOmsorgPlusFacilities,
  omsorgPlusCompliance: loadOmsorgPlusCompliance,
  sustainability: loadSustainabilityScenarios
};

const schemas = {
  organizations: organizationsSchema,
  people: peopleSchema,
  meetings: meetingsSchema,
  documents: documentsSchema,
  deliverables: deliverablesSchema,
  timeline: timelineSchema,
  // Omsorg+ expanded databases
  omsorgPlusConcept: omsorgPlusConceptSchema,
  omsorgPlusFloors: omsorgPlusFloorsSchema,
  omsorgPlusUnits: omsorgPlusUnitsSchema,
  omsorgPlusFacilities: omsorgPlusFacilitiesSchema,
  omsorgPlusCompliance: omsorgPlusComplianceSchema,
  sustainability: sustainabilitySchema
};

const transformers = {
  organizations: transformOrganization,
  people: transformPerson,
  meetings: transformMeeting,
  documents: transformDocument,
  deliverables: transformDeliverable,
  timeline: transformTimelineEvent,
  // Omsorg+ expanded databases
  omsorgPlusConcept: transformOmsorgPlusConcept,
  omsorgPlusFloors: transformOmsorgPlusFloor,
  omsorgPlusUnits: transformOmsorgPlusUnit,
  omsorgPlusFacilities: transformOmsorgPlusFacility,
  omsorgPlusCompliance: transformOmsorgPlusCompliance,
  sustainability: transformSustainabilityScenario
};

function getRecordId(record, dbName) {
  if (record.id) return record.id;
  if (record.unit_id) return record.unit_id;
  if (record.file_name) return `doc_${record.file_name.replace(/[^a-zA-Z0-9]/g, '_')}`;
  return `${dbName}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function cleanProperties(props) {
  const cleaned = {};
  for (const [key, value] of Object.entries(props)) {
    if (value !== undefined && value !== null) {
      cleaned[key] = value;
    }
  }
  return cleaned;
}

async function createDatabase(dbName) {
  const existingId = idMapper.getNotionDatabaseId(dbName);
  if (existingId && !FORCE) {
    console.log(`  Database "${DATABASE_NAMES[dbName]}" already exists: ${existingId}`);
    return existingId;
  }

  const schema = schemas[dbName];
  const cleanedSchema = {};
  for (const [key, value] of Object.entries(schema)) {
    if (!value.relation || value.relation.database_id !== 'PLACEHOLDER') {
      cleanedSchema[key] = value;
    }
  }

  if (DRY_RUN) {
    console.log(`  [DRY RUN] Would create database: ${DATABASE_NAMES[dbName]}`);
    return 'dry-run-id';
  }

  const response = await withRetry(() => notion.databases.create({
    parent: { page_id: NOTION_PAGE_ID },
    title: [{ type: 'text', text: { content: DATABASE_NAMES[dbName] } }],
    properties: cleanedSchema
  }), `create ${dbName}`);

  idMapper.setNotionDatabaseId(dbName, response.id);
  console.log(`  Created database: ${DATABASE_NAMES[dbName]} (${response.id})`);
  return response.id;
}

async function syncRecords(dbName, dbId) {
  const loader = loaders[dbName];
  const transformer = transformers[dbName];

  let records;
  try {
    records = loader();
  } catch (error) {
    console.error(`  Failed to load ${dbName}: ${error.message}`);
    return { created: 0, updated: 0, errors: 1 };
  }

  console.log(`  Syncing ${records.length} ${dbName} records...`);

  let created = 0, updated = 0, errors = 0;

  for (const record of records) {
    const localId = getRecordId(record, dbName);
    const existingPageId = idMapper.getNotionPageId(localId, dbName);

    try {
      const properties = cleanProperties(transformer(record));

      if (DRY_RUN) {
        console.log(`    [DRY RUN] Would ${existingPageId ? 'update' : 'create'}: ${localId}`);
        existingPageId ? updated++ : created++;
        continue;
      }

      // Get icon for this record
      const icon = getRecordIcon(dbName, record);

      if (existingPageId && !FORCE) {
        await withRetry(() => notion.pages.update({
          page_id: existingPageId,
          properties,
          icon: { type: 'emoji', emoji: icon.emoji }
        }), `update ${localId}`);
        updated++;
      } else {
        const response = await withRetry(() => notion.pages.create({
          parent: { database_id: dbId },
          properties,
          icon: { type: 'emoji', emoji: icon.emoji }
        }), `create ${localId}`);
        idMapper.setNotionPageId(localId, response.id, dbName);
        created++;

        if (dbName === 'meetings') {
          const content = getMeetingContent(record);
          if (content.length > 0) {
            await withRetry(() => notion.blocks.children.append({
              block_id: response.id,
              children: content
            }), `add content ${localId}`);
          }
        }
      }
    } catch (error) {
      console.error(`    Error syncing ${localId}: ${error.message}`);
      errors++;
    }
  }

  return { created, updated, errors };
}

async function linkPeopleToOrganizations() {
  console.log('\nLinking People → Organizations...');

  const people = loadPeople();
  const orgDbId = idMapper.getNotionDatabaseId('organizations');

  if (!orgDbId) {
    console.log('  Skipping: Organizations database not found');
    return;
  }

  let linked = 0;
  for (const person of people) {
    const orgId = getOrganizationId(person);
    if (!orgId) continue;

    const personNotionId = idMapper.getNotionPageId(person.id, 'people');
    const orgNotionId = idMapper.getNotionPageId(orgId, 'organizations');

    if (!personNotionId || !orgNotionId) continue;

    if (DRY_RUN) {
      console.log(`  [DRY RUN] Would link ${person.name} → ${orgId}`);
      linked++;
      continue;
    }

    try {
      await withRetry(() => notion.pages.update({
        page_id: personNotionId,
        properties: {
          'Organization': { relation: [{ id: orgNotionId }] }
        }
      }), `link ${person.id} → ${orgId}`);
      linked++;
    } catch (error) {
      console.error(`  Error linking ${person.id}: ${error.message}`);
    }
  }

  console.log(`  Linked ${linked} people to organizations`);
}

async function main() {
  console.log('='.repeat(60));
  console.log('Hovfaret 13 → Notion Sync');
  console.log('='.repeat(60));

  if (DRY_RUN) console.log('\n*** DRY RUN MODE - No changes will be made ***\n');
  if (FORCE) console.log('\n*** FORCE MODE - Recreating all records ***\n');

  if (!DRY_RUN) {
    const connected = await testConnection();
    if (!connected) {
      console.error('\nFailed to connect to Notion. Check your NOTION_TOKEN.');
      process.exit(1);
    }
  }

  console.log(`\nTarget page: ${NOTION_PAGE_ID}`);

  const databasesToSync = SPECIFIC_DB
    ? [SPECIFIC_DB]
    : DATABASE_ORDER;

  console.log('\n--- Phase 1: Creating Databases ---\n');

  for (const dbName of databasesToSync) {
    if (!loaders[dbName]) {
      console.error(`Unknown database: ${dbName}`);
      continue;
    }
    await createDatabase(dbName);
  }

  console.log('\n--- Phase 2: Syncing Records ---\n');

  const stats = {};
  for (const dbName of databasesToSync) {
    const dbId = idMapper.getNotionDatabaseId(dbName);
    if (!dbId || dbId === 'dry-run-id') continue;

    console.log(`\n[${DATABASE_NAMES[dbName]}]`);
    stats[dbName] = await syncRecords(dbName, dbId);
  }

  console.log('\n--- Phase 3: Linking Relations ---\n');

  if (databasesToSync.includes('people') && databasesToSync.includes('organizations')) {
    await linkPeopleToOrganizations();
  }

  console.log('\n--- Summary ---\n');

  let totalCreated = 0, totalUpdated = 0, totalErrors = 0;
  for (const [dbName, s] of Object.entries(stats)) {
    console.log(`${DATABASE_NAMES[dbName]}: ${s.created} created, ${s.updated} updated, ${s.errors} errors`);
    totalCreated += s.created;
    totalUpdated += s.updated;
    totalErrors += s.errors;
  }

  console.log(`\nTotal: ${totalCreated} created, ${totalUpdated} updated, ${totalErrors} errors`);
  console.log('\n' + '='.repeat(60));
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
