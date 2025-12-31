import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../../config.js';

export function loadOmsorgPlusFacilities() {
  const filePath = resolve(DATA_DIR, 'themes/omsorg-plus.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));

  const facilities = [];
  const commonFacilities = data.common_facilities || {};

  // Aktivitetssenter components
  if (commonFacilities.aktivitetssenter?.components) {
    for (const comp of commonFacilities.aktivitetssenter.components) {
      facilities.push({
        id: `facility_${comp.name.toLowerCase().replace(/[\s\/]/g, '_')}`,
        name: comp.name,
        category: 'aktivitetssenter',
        type: 'activity',
        capacity: String(comp.capacity_persons || ''),
        location: comp.location || '1. etasje'
      });
    }
  }

  // Cafe
  if (commonFacilities.cafe) {
    facilities.push({
      id: 'facility_cafe',
      name: 'Kafé/Restaurant',
      category: 'cafe',
      type: 'service',
      description: commonFacilities.cafe.service,
      components: commonFacilities.cafe.components || [],
      location: '1. etasje'
    });
  }

  // Servicedel
  if (commonFacilities.servicedel?.components) {
    for (const comp of commonFacilities.servicedel.components) {
      facilities.push({
        id: `facility_${comp.name.toLowerCase().replace(/[\s\/]/g, '_')}`,
        name: comp.name,
        category: 'servicedel',
        type: comp.type || 'service',
        capacity: comp.minimum_capacity ? `Min ${comp.minimum_capacity}` : '',
        location: '1. etasje'
      });
    }
  }

  // Social meeting places
  if (commonFacilities.social_meeting_places) {
    facilities.push({
      id: 'facility_social_meeting',
      name: 'Fellesrom per etasje',
      category: 'social',
      type: 'common',
      description: commonFacilities.social_meeting_places.description,
      location: commonFacilities.social_meeting_places.location
    });
  }

  // Elevators
  if (commonFacilities.elevators) {
    facilities.push({
      id: 'facility_elevators',
      name: 'Heiser',
      category: 'infrastructure',
      type: 'accessibility',
      capacity: `Min ${commonFacilities.elevators.minimum}`,
      description: commonFacilities.elevators.size,
      emergency_power: commonFacilities.elevators.emergency_power
    });
  }

  return facilities;
}

export const omsorgPlusFacilitiesSchema = {
  'Name': { title: {} },
  'ID': { rich_text: {} },
  'Category': { select: {} },
  'Type': { select: {} },
  'Capacity': { rich_text: {} },
  'Location': { rich_text: {} },
  'Description': { rich_text: {} },
  'Components': { multi_select: {} },
  'Emergency Power': { checkbox: {} }
};

export function transformOmsorgPlusFacility(facility) {
  const components = (facility.components || [])
    .slice(0, 20)
    .map(c => ({ name: String(c).replace(/,/g, ';').slice(0, 100) }));

  return {
    'Name': { title: [{ text: { content: facility.name || '' } }] },
    'ID': { rich_text: [{ text: { content: facility.id || '' } }] },
    'Category': facility.category ? { select: { name: facility.category } } : undefined,
    'Type': facility.type ? { select: { name: facility.type } } : undefined,
    'Capacity': facility.capacity ? { rich_text: [{ text: { content: facility.capacity } }] } : undefined,
    'Location': facility.location ? { rich_text: [{ text: { content: facility.location } }] } : undefined,
    'Description': facility.description ? { rich_text: [{ text: { content: facility.description.slice(0, 2000) } }] } : undefined,
    'Components': components.length > 0 ? { multi_select: components } : undefined,
    'Emergency Power': { checkbox: facility.emergency_power || false }
  };
}
