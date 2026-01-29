import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../config.js';

// Color mappings for timeline
const layerColors = {
  'strategic': 'red',
  'operational': 'blue'
};

const importanceColors = {
  'critical': 'red',
  'high': 'orange',
  'medium': 'yellow',
  'low': 'gray'
};

const categoryColors = {
  'milestone': 'green',
  'meeting': 'blue',
  'submission': 'orange',
  'approval': 'green',
  'deadline': 'red',
  'event': 'purple',
  'decision': 'yellow'
};

const tagColors = {
  'sustainability': 'green',
  'bærekraft': 'green',
  'regulatory': 'orange',
  'regulering': 'orange',
  'omsorg': 'purple',
  'technical': 'blue',
  'teknisk': 'blue',
  'stakeholder': 'pink',
  'financial': 'yellow'
};

function getTagColor(tag) {
  const lowerTag = tag.toLowerCase();
  for (const [key, color] of Object.entries(tagColors)) {
    if (lowerTag.includes(key)) {
      return color;
    }
  }
  return 'default';
}

export function loadTimeline() {
  const filePath = resolve(DATA_DIR, 'timeline.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));

  const events = [];

  if (data.events?.strategic) {
    for (const event of data.events.strategic) {
      events.push({ ...event, layer: 'strategic' });
    }
  }

  if (data.events?.operational) {
    for (const event of data.events.operational) {
      events.push({ ...event, layer: 'operational' });
    }
  }

  if (data.strategic_milestones) {
    for (const event of data.strategic_milestones) {
      events.push({ ...event, layer: 'strategic' });
    }
  }

  if (data.operational_events) {
    for (const event of data.operational_events) {
      events.push({ ...event, layer: 'operational' });
    }
  }

  return events;
}

export const timelineSchema = {
  'Title': { title: {} },
  'ID': { rich_text: {} },
  'Date': { date: {} },
  'Description': { rich_text: {} },
  'Layer': { select: {} },
  'Phase': { rich_text: {} },
  'Category': { select: {} },
  'Importance': { select: {} },
  'Icon': { select: {} },
  'Tags': { multi_select: {} },
  'Source Verified': { rich_text: {} }
};

function parseTimelineDate(dateStr) {
  if (!dateStr) return null;

  if (/^\d{4}$/.test(dateStr)) {
    return `${dateStr}-01-01`;
  }
  if (/^\d{4}-\d{2}$/.test(dateStr)) {
    return `${dateStr}-01`;
  }
  if (/^\d{4}-\d{2}-\d{2}/.test(dateStr)) {
    return dateStr.split('T')[0];
  }
  return null;
}

export function transformTimelineEvent(event) {
  const title = event.title_no || event.title || 'Untitled Event';
  const date = parseTimelineDate(event.date);

  return {
    'Title': { title: [{ text: { content: title.slice(0, 2000) } }] },
    'ID': { rich_text: [{ text: { content: event.id || '' } }] },
    'Date': date ? { date: { start: date } } : undefined,
    'Description': { rich_text: [{ text: { content: (event.description || '').slice(0, 2000) } }] },
    'Layer': event.layer ? { select: { name: event.layer } } : undefined,
    'Phase': { rich_text: [{ text: { content: event.phase || '' } }] },
    'Category': event.category ? { select: { name: event.category.slice(0, 100) } } : undefined,
    'Importance': event.importance ? { select: { name: event.importance } } : undefined,
    'Icon': event.icon ? { select: { name: event.icon.slice(0, 100) } } : undefined,
    'Tags': { multi_select: (event.tags || []).slice(0, 100).map(t => ({ name: t.slice(0, 100) })) },
    'Source Verified': { rich_text: [{ text: { content: (event.source_verified || '').slice(0, 2000) } }] }
  };
}
