import { config } from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

config({ path: resolve(__dirname, '../.env') });

export const NOTION_TOKEN = process.env.NOTION_TOKEN;
export const NOTION_PAGE_ID = process.env.NOTION_PAGE_ID || '2c720392ef5b8084a580dcc6578a23fb';
export const DATA_DIR = resolve(__dirname, process.env.DATA_DIR || '../data');

export const RATE_LIMIT = 3;
export const BATCH_SIZE = 50;
export const RETRY_ATTEMPTS = 3;
export const RETRY_DELAY = 1000;

export const DATABASE_ORDER = [
  'organizations',
  'people',
  'meetings',
  'documents',
  'timeline',
  'deliverables',
  // Omsorg+ databases (order matters for relations)
  'omsorgPlusConcept',
  'omsorgPlusFloors',
  'omsorgPlusUnits',
  'omsorgPlusFacilities',
  'omsorgPlusCompliance',
  'sustainability'
];

export const DATABASE_NAMES = {
  organizations: 'Organizations',
  people: 'People',
  meetings: 'Meetings',
  documents: 'Documents',
  timeline: 'Timeline',
  deliverables: 'Deliverables',
  omsorgPlusConcept: 'Omsorg+ Concept',
  omsorgPlusFloors: 'Omsorg+ Floors',
  omsorgPlusUnits: 'Omsorg+ Units',
  omsorgPlusFacilities: 'Omsorg+ Facilities',
  omsorgPlusCompliance: 'Omsorg+ Compliance',
  sustainability: 'Sustainability Scenarios'
};
