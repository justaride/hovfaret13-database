import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../config.js';

// Color mapping for select options
const typeColors = {
  'Consultant': 'blue',
  'Government': 'purple',
  'Owner': 'green',
  'Contractor': 'orange',
  'Architect': 'pink',
  'Engineering': 'gray',
  'Legal': 'brown',
  'Financial': 'yellow'
};

const categoryColors = {
  'Technical': 'blue',
  'Regulatory': 'orange',
  'Strategic': 'red',
  'Financial': 'yellow',
  'Legal': 'brown',
  'Environmental': 'green'
};

const engagementColors = {
  'High': 'green',
  'Medium': 'yellow',
  'Low': 'gray'
};

const expertiseColors = {
  'Sustainability': 'green',
  'Bærekraft': 'green',
  'Architecture': 'pink',
  'Arkitektur': 'pink',
  'Engineering': 'blue',
  'Ingeniør': 'blue',
  'Regulatory': 'orange',
  'Regulatorisk': 'orange',
  'Energy': 'yellow',
  'Energi': 'yellow',
  'Legal': 'brown',
  'Juridisk': 'brown',
  'Financial': 'purple',
  'Finans': 'purple'
};

function getExpertiseColor(expertise) {
  for (const [key, color] of Object.entries(expertiseColors)) {
    if (expertise.toLowerCase().includes(key.toLowerCase())) {
      return color;
    }
  }
  return 'default';
}

export function loadOrganizations() {
  const filePath = resolve(DATA_DIR, 'stakeholders/organizations.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));
  return Object.values(data.organizations || data);
}

export const organizationsSchema = {
  'Name': { title: {} },
  'ID': { rich_text: {} },
  'Type': { select: {} },
  'Category': { select: {} },
  'Description': { rich_text: {} },
  'Role in Project': { rich_text: {} },
  'Website': { url: {} },
  'Expertise': { multi_select: {} },
  'Key Deliverables': { multi_select: {} },
  'Engagement Level': { select: {} },
  'First Involvement': { date: {} },
  'Total Meetings': { number: {} }
};

export function transformOrganization(org) {
  // Note: Colors for select options can only be set in Notion UI
  // API cannot change existing option colors
  return {
    'Name': { title: [{ text: { content: org.name || '' } }] },
    'ID': { rich_text: [{ text: { content: org.id || '' } }] },
    'Type': org.type ? { select: { name: org.type } } : undefined,
    'Category': org.category ? { select: { name: org.category } } : undefined,
    'Description': { rich_text: [{ text: { content: (org.description || '').slice(0, 2000) } }] },
    'Role in Project': { rich_text: [{ text: { content: (org.role_in_project || '').slice(0, 2000) } }] },
    'Website': org.website ? { url: org.website } : undefined,
    'Expertise': { multi_select: (org.expertise || []).slice(0, 100).map(e => ({ name: e.slice(0, 100) })) },
    'Key Deliverables': { multi_select: (org.key_deliverables || []).slice(0, 100).map(d => ({ name: d.slice(0, 100) })) },
    'Engagement Level': org.engagement_level ? { select: { name: org.engagement_level } } : undefined,
    'First Involvement': org.first_involvement ? { date: { start: org.first_involvement } } : undefined,
    'Total Meetings': { number: org.total_meetings || 0 }
  };
}
