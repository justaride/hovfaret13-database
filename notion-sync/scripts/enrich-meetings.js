import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = resolve(__dirname, '../../data');

function extractOutcomes(meeting) {
  let outcomes = [];

  // 1. Add decisions if present
  if (meeting.decisions && meeting.decisions.length > 0) {
    outcomes = outcomes.concat(meeting.decisions);
  }

  // 2. Add action items if present
  if (meeting.action_items && meeting.action_items.length > 0) {
    for (const ai of meeting.action_items) {
      outcomes.push(`Oppgave: ${ai.task}${ai.responsible ? ` (${ai.responsible})` : ''}`);
    }
  }

  // 3. If no outcomes yet, extract from summary
  if (outcomes.length === 0) {
    const summary = meeting.summary || (meeting.report && meeting.report.summary) || '';
    if (summary) {
      // Split into sentences and take first 2-3 meaningful ones
      const sentences = summary.split(/[.!?]+/).filter(s => s.trim().length > 20);
      const selected = sentences.slice(0, 3).map(s => s.trim());
      if (selected.length > 0) {
        outcomes = selected;
      }
    }
  }

  return outcomes;
}

// Load meetings
const meetingsPath = resolve(dataDir, 'meetings.json');
const data = JSON.parse(readFileSync(meetingsPath, 'utf8'));

console.log('=== ENRICHING MEETINGS WITH OUTCOMES ===\n');

let enriched = 0;
for (const m of data.meetings) {
  if (!m.outcomes || m.outcomes.length === 0) {
    const newOutcomes = extractOutcomes(m);
    if (newOutcomes.length > 0) {
      m.outcomes = newOutcomes;
      enriched++;
      console.log(`✓ ${m.date} | ${m.title.slice(0, 50)}...`);
      console.log(`  Outcomes: ${newOutcomes.length} items`);
    }
  }
}

// Update metadata
data.metadata.last_updated = new Date().toISOString().split('T')[0];
data.metadata.enrichment_note = 'Outcomes derived from decisions, action_items, and summary text.';

// Write back
writeFileSync(meetingsPath, JSON.stringify(data, null, 2));

console.log(`\n=== SUMMARY ===`);
console.log(`Enriched: ${enriched} meetings`);

// Verify
const verify = JSON.parse(readFileSync(meetingsPath, 'utf8'));
const withOutcomes = verify.meetings.filter(m => m.outcomes && m.outcomes.length > 0).length;
console.log(`Meetings with outcomes: ${withOutcomes}/${verify.meetings.length} (${Math.round(100*withOutcomes/verify.meetings.length)}%)`);
