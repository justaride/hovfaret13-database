import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../config.js';

export function loadPeople() {
  const filePath = resolve(DATA_DIR, 'stakeholders/people.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));
  return Object.values(data.people || data);
}

export const peopleSchema = {
  'Name': { title: {} },
  'ID': { rich_text: {} },
  'Email': { email: {} },
  'Phone': { phone_number: {} },
  'Organization': { relation: { database_id: 'PLACEHOLDER' } },
  'Title': { rich_text: {} },
  'Role in Project': { rich_text: {} },
  'Bio': { rich_text: {} },
  'Expertise': { multi_select: {} },
  'Category': { select: {} },
  'Total Meetings': { number: {} },
  'First Meeting': { date: {} },
  'Last Meeting': { date: {} }
};

export function transformPerson(person, orgDbId = null) {
  const props = {
    'Name': { title: [{ text: { content: person.name || '' } }] },
    'ID': { rich_text: [{ text: { content: person.id || '' } }] },
    'Email': person.email ? { email: person.email } : undefined,
    'Phone': person.phone ? { phone_number: person.phone } : undefined,
    'Title': { rich_text: [{ text: { content: person.title || '' } }] },
    'Role in Project': { rich_text: [{ text: { content: (person.role_in_project || '').slice(0, 2000) } }] },
    'Bio': { rich_text: [{ text: { content: (person.bio || '').slice(0, 2000) } }] },
    'Expertise': { multi_select: (person.expertise || []).slice(0, 100).map(e => ({ name: e.slice(0, 100) })) },
    'Category': person.category ? { select: { name: person.category } } : undefined,
    'Total Meetings': { number: person.engagement?.total_meetings || 0 },
    'First Meeting': person.engagement?.first_meeting ? { date: { start: person.engagement.first_meeting } } : undefined,
    'Last Meeting': person.engagement?.last_meeting ? { date: { start: person.engagement.last_meeting } } : undefined
  };

  return props;
}

export function getOrganizationId(person) {
  return person.organization_id;
}

export function getCollaboratorIds(person) {
  return person.key_collaborators || [];
}
