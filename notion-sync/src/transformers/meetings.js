import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../config.js';

// Topic color mapping
const topicColors = {
  'sustainability': 'green',
  'bærekraft': 'green',
  'miljø': 'green',
  'klima': 'green',
  'regulatory': 'orange',
  'regulering': 'orange',
  'søknad': 'orange',
  'tillatelse': 'orange',
  'technical': 'blue',
  'teknisk': 'blue',
  'bygg': 'blue',
  'konstruksjon': 'blue',
  'strategic': 'red',
  'strategi': 'red',
  'financial': 'yellow',
  'finans': 'yellow',
  'økonomi': 'yellow',
  'omsorg': 'purple',
  'helse': 'purple',
  'stakeholder': 'pink',
  'interessent': 'pink',
  'nabo': 'pink'
};

function getTopicColor(topic) {
  const lowerTopic = topic.toLowerCase();
  for (const [key, color] of Object.entries(topicColors)) {
    if (lowerTopic.includes(key)) {
      return color;
    }
  }
  return 'default';
}

export function loadMeetings() {
  const filePath = resolve(DATA_DIR, 'meetings.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));
  return data.meetings || [];
}

export const meetingsSchema = {
  'Title': { title: {} },
  'ID': { rich_text: {} },
  'Date': { date: {} },
  'Location': { rich_text: {} },
  'Organizer': { rich_text: {} },
  'Participant Count': { number: {} },
  'Participants': { relation: { database_id: 'PLACEHOLDER' } },
  'Topics': { multi_select: {} },
  'Summary': { rich_text: {} },
  'Outcomes': { rich_text: {} },
  'Source File': { rich_text: {} }
};

export function transformMeeting(meeting) {
  const summary = meeting.report?.summary || meeting.summary || '';
  let outcomes = (meeting.outcomes || []).join('\n');

  // Fallback: use first part of summary if no outcomes
  if (!outcomes && summary) {
    outcomes = summary.slice(0, 500);
  }

  return {
    'Title': { title: [{ text: { content: (meeting.title || 'Untitled Meeting').slice(0, 2000) } }] },
    'ID': { rich_text: [{ text: { content: meeting.id || '' } }] },
    'Date': meeting.date ? { date: { start: meeting.date } } : undefined,
    'Location': { rich_text: [{ text: { content: (meeting.location || '').slice(0, 2000) } }] },
    'Organizer': { rich_text: [{ text: { content: (meeting.organizer || '').slice(0, 2000) } }] },
    'Participant Count': { number: meeting.participant_count || meeting.participants?.length || 0 },
    'Topics': { multi_select: (meeting.topics_discussed || []).slice(0, 100).map(t => ({ name: t.replace(/,/g, ';').slice(0, 100) })) },
    'Summary': { rich_text: [{ text: { content: summary.slice(0, 2000) } }] },
    'Outcomes': { rich_text: [{ text: { content: outcomes.slice(0, 2000) } }] },
    'Source File': { rich_text: [{ text: { content: (meeting.source_file || '').slice(0, 2000) } }] }
  };
}

export function getParticipantNames(meeting) {
  return (meeting.participants || []).map(p => p.name);
}

export function getMeetingContent(meeting) {
  const blocks = [];

  // Meeting summary callout at top
  const summary = meeting.report?.summary || meeting.summary || '';
  if (summary) {
    blocks.push({
      object: 'block',
      type: 'callout',
      callout: {
        rich_text: [{ type: 'text', text: { content: summary.slice(0, 2000) } }],
        icon: { type: 'emoji', emoji: '📋' },
        color: 'gray_background'
      }
    });
    blocks.push({ object: 'block', type: 'divider', divider: {} });
  }

  // Decisions in green callout
  if (meeting.decisions?.length) {
    blocks.push({
      object: 'block',
      type: 'callout',
      callout: {
        rich_text: [{
          type: 'text',
          text: { content: '✅ Beslutninger' },
          annotations: { bold: true }
        }],
        icon: { type: 'emoji', emoji: '🎯' },
        color: 'green_background'
      }
    });
    meeting.decisions.forEach(d => {
      blocks.push({
        object: 'block',
        type: 'bulleted_list_item',
        bulleted_list_item: {
          rich_text: [{ type: 'text', text: { content: d.slice(0, 2000) } }],
          color: 'green'
        }
      });
    });
    blocks.push({ object: 'block', type: 'divider', divider: {} });
  }

  // Action items in orange callout with checkboxes
  if (meeting.action_items?.length) {
    blocks.push({
      object: 'block',
      type: 'callout',
      callout: {
        rich_text: [{
          type: 'text',
          text: { content: '📌 Oppgaver' },
          annotations: { bold: true }
        }],
        icon: { type: 'emoji', emoji: '⚡' },
        color: 'orange_background'
      }
    });
    meeting.action_items.forEach(item => {
      const text = typeof item === 'string'
        ? item
        : `${item.task}${item.responsible ? ` → ${item.responsible}` : ''}`;
      blocks.push({
        object: 'block',
        type: 'to_do',
        to_do: {
          rich_text: [{ type: 'text', text: { content: text.slice(0, 2000) } }],
          checked: item.status === 'completed',
          color: 'orange'
        }
      });
    });
    blocks.push({ object: 'block', type: 'divider', divider: {} });
  }

  // Discussion in toggle for cleaner view
  if (meeting.report?.discussion?.length) {
    blocks.push({
      object: 'block',
      type: 'toggle',
      toggle: {
        rich_text: [{
          type: 'text',
          text: { content: '💬 Diskusjon (klikk for å utvide)' },
          annotations: { bold: true }
        }],
        color: 'blue',
        children: meeting.report.discussion.slice(0, 20).flatMap(section => {
          const sectionBlocks = [];
          if (section.heading) {
            sectionBlocks.push({
              object: 'block',
              type: 'heading_3',
              heading_3: {
                rich_text: [{ type: 'text', text: { content: section.heading.slice(0, 2000) } }],
                color: 'blue'
              }
            });
          }
          if (section.content) {
            sectionBlocks.push({
              object: 'block',
              type: 'paragraph',
              paragraph: { rich_text: [{ type: 'text', text: { content: section.content.slice(0, 2000) } }] }
            });
          }
          return sectionBlocks;
        })
      }
    });
  }

  // Participants list in collapsible toggle
  if (meeting.participants?.length) {
    const participantNames = meeting.participants
      .map(p => typeof p === 'string' ? p : p.name)
      .filter(Boolean)
      .join(', ');

    if (participantNames) {
      blocks.push({
        object: 'block',
        type: 'toggle',
        toggle: {
          rich_text: [{
            type: 'text',
            text: { content: `👥 Deltakere (${meeting.participants.length})` },
            annotations: { bold: true }
          }],
          color: 'purple',
          children: [{
            object: 'block',
            type: 'paragraph',
            paragraph: { rich_text: [{ type: 'text', text: { content: participantNames.slice(0, 2000) } }] }
          }]
        }
      });
    }
  }

  return blocks.slice(0, 100);
}
