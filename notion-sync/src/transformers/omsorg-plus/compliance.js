import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../../config.js';

export function loadOmsorgPlusCompliance() {
  const filePath = resolve(DATA_DIR, 'themes/omsorg-plus.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));

  const compliance = [];
  const requirements = data.requirements || {};

  for (const [category, details] of Object.entries(requirements)) {
    // Skip the summary entry
    if (category === 'husbanken_compliance') continue;

    // Extract items - handle both array of strings and array of objects
    let items = [];
    if (details.items) {
      items = details.items.map(item => {
        if (typeof item === 'string') return item;
        if (item.system) return `${item.system}: ${item.specification}`;
        return JSON.stringify(item);
      });
    }

    compliance.push({
      id: `compliance_${category}`,
      category: category,
      category_name: formatCategoryName(category),
      status: details.status || 'UNKNOWN',
      items: items,
      zones: details.zones || [],
      minimum_standard: details.minimum_standard || '',
      preferred_standard: details.preferred_standard || ''
    });
  }

  return compliance;
}

function formatCategoryName(category) {
  const names = {
    'location': 'Beliggenhet',
    'building_construction': 'Bygningskonstruksjon',
    'installations': 'Installasjoner',
    'energy': 'Energi',
    'security': 'Sikkerhet'
  };
  return names[category] || category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

export const omsorgPlusComplianceSchema = {
  'Category': { title: {} },
  'ID': { rich_text: {} },
  'Status': { select: {} },
  'Requirement Items': { multi_select: {} },
  'Details': { rich_text: {} },
  'Zones': { multi_select: {} },
  'Minimum Standard': { rich_text: {} },
  'Preferred Standard': { rich_text: {} }
};

export function transformOmsorgPlusCompliance(compliance) {
  const items = (compliance.items || [])
    .slice(0, 20)
    .map(i => ({ name: i.replace(/,/g, ';').slice(0, 100) }));

  const zones = (compliance.zones || [])
    .slice(0, 10)
    .map(z => ({ name: z.replace(/,/g, ';').slice(0, 100) }));

  // Create detailed description from items
  const details = (compliance.items || []).join('\n');

  return {
    'Category': { title: [{ text: { content: compliance.category_name || compliance.category } }] },
    'ID': { rich_text: [{ text: { content: compliance.id || '' } }] },
    'Status': compliance.status ? { select: { name: compliance.status } } : undefined,
    'Requirement Items': items.length > 0 ? { multi_select: items } : undefined,
    'Details': details ? { rich_text: [{ text: { content: details.slice(0, 2000) } }] } : undefined,
    'Zones': zones.length > 0 ? { multi_select: zones } : undefined,
    'Minimum Standard': compliance.minimum_standard ? { rich_text: [{ text: { content: compliance.minimum_standard } }] } : undefined,
    'Preferred Standard': compliance.preferred_standard ? { rich_text: [{ text: { content: compliance.preferred_standard } }] } : undefined
  };
}
