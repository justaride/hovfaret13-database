import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../config.js';

// Color mappings for deliverables
const statusColors = {
  'completed': 'green',
  'in_progress': 'blue',
  'not_started': 'gray',
  'in_planning': 'yellow',
  'in_production': 'orange',
  'blocked': 'red'
};

const importanceColors = {
  'critical': 'red',
  'high': 'orange',
  'medium': 'yellow',
  'low': 'gray'
};

const categoryColors = {
  'Nabolag og Interessenter': 'pink',
  'Kommunikasjon': 'blue',
  'Prosjektstyring': 'purple',
  'Regulering og Søknad': 'orange',
  'Bærekraft': 'green',
  'Teknisk': 'gray',
  'Markedsføring': 'yellow'
};

function getCategoryColor(category) {
  for (const [key, color] of Object.entries(categoryColors)) {
    if (category && category.toLowerCase().includes(key.toLowerCase().split(' ')[0])) {
      return color;
    }
  }
  return 'default';
}

export function loadDeliverables() {
  const filePath = resolve(DATA_DIR, 'deliverables.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));

  if (data.deliverables && Array.isArray(data.deliverables)) {
    const categories = {};
    for (const cat of (data.categories || [])) {
      categories[cat.id] = cat.name;
    }
    return data.deliverables.map(del => ({
      ...del,
      category_name: categories[del.category] || del.category
    }));
  }

  const deliverables = [];
  for (const category of (data.categories || [])) {
    for (const del of (category.deliverables || [])) {
      deliverables.push({
        ...del,
        category_id: category.id,
        category_name: category.name
      });
    }
  }
  return deliverables;
}

export const deliverablesSchema = {
  'Title': { title: {} },
  'ID': { rich_text: {} },
  'Category': { select: {} },
  'Status': { select: {} },
  'Start Date': { date: {} },
  'End Date': { date: {} },
  'Responsible': { rich_text: {} },
  'Importance': { select: {} },
  'URL': { url: {} }
};

function parseDate(dateStr) {
  if (!dateStr) return null;
  const match = dateStr.match(/(\d{2})\/(\d{2})\/(\d{4})/);
  if (match) {
    return `${match[3]}-${match[2]}-${match[1]}`;
  }
  if (/^\d{4}-\d{2}-\d{2}/.test(dateStr)) {
    return dateStr.split('T')[0];
  }
  return null;
}

export function transformDeliverable(del) {
  let startDate = null;
  let endDate = null;

  if (del.dates) {
    if (typeof del.dates === 'string') {
      const parts = del.dates.split(' - ');
      startDate = parseDate(parts[0]);
      endDate = parseDate(parts[1] || parts[0]);
    } else {
      startDate = del.dates.start || null;
      endDate = del.dates.end || null;
    }
  }

  const statusMap = {
    'FULLFØRT': 'completed',
    'PÅGÅR': 'in_progress',
    'IKKE STARTET': 'not_started',
    'PLANLEGGES': 'in_planning',
    'I PRODUKSJON': 'in_production',
    'completed': 'completed',
    'in_progress': 'in_progress',
    'not_started': 'not_started'
  };

  const status = statusMap[del.status] || del.status || 'not_started';

  const responsible = Array.isArray(del.responsible)
    ? del.responsible.join(', ')
    : (del.responsible || '');

  return {
    'Title': { title: [{ text: { content: (del.title || del.title_no || 'Untitled').slice(0, 2000) } }] },
    'ID': { rich_text: [{ text: { content: del.id || `del_${Date.now()}` } }] },
    'Category': del.category_name ? { select: { name: del.category_name.slice(0, 100) } } : undefined,
    'Status': { select: { name: status } },
    'Start Date': startDate ? { date: { start: startDate } } : undefined,
    'End Date': endDate ? { date: { start: endDate } } : undefined,
    'Responsible': { rich_text: [{ text: { content: responsible.slice(0, 2000) } }] },
    'Importance': del.importance ? { select: { name: del.importance } } : undefined,
    'URL': del.url ? { url: del.url } : undefined
  };
}
