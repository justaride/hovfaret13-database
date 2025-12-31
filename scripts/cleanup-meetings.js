#!/usr/bin/env node
/**
 * Møtedata Kvalitetsopprydding - Fase 62
 *
 * Dette skriptet:
 * 1. Sletter ikke-møter
 * 2. Merger duplikater
 * 3. Fikser korrupt data
 * 4. Auto-tildeler møtetype
 * 5. Fyller manglende lokasjoner
 * 6. Oppdaterer metadata
 */

const fs = require('fs');
const path = require('path');

const MEETINGS_FILE = path.join(__dirname, '../data/meetings.json');
const BACKUP_FILE = path.join(__dirname, '../data/meetings.backup.json');

// Last inn data
const data = JSON.parse(fs.readFileSync(MEETINGS_FILE, 'utf8'));
const originalCount = data.meetings.length;

console.log(`\n=== MØTE-OPPRYDDING STARTER ===`);
console.log(`Originalt antall møter: ${originalCount}\n`);

// ============================================
// STEG 1: Slett ikke-møter
// ============================================
const NON_MEETINGS = [
  'm_unknown_date_det_er_jo_det',
  'm_unknown_date_notat_hva_skal_vi_mles_mot',
  'm_unknown_date_umiddelbare_oppgaver_denne_uken',
  'm_unknown_date_detaljert_sammendrag_av_samtalen_om_skolebygget',
  'm_unknown_date_rapport_mte_om_utviklingsprosjekt_p_skyen',
  'm_unknown_date_rapport_bydelsledernes_uttalelser_mte_om_omsorg'
];

console.log('STEG 1: Sletter ikke-møter...');
const beforeNonMeetings = data.meetings.length;
data.meetings = data.meetings.filter(m => !NON_MEETINGS.includes(m.id));
console.log(`  Slettet: ${beforeNonMeetings - data.meetings.length} ikke-møter\n`);

// ============================================
// STEG 2: Merge duplikater
// ============================================
const DUPLICATES_TO_REMOVE = [
  'm_2024-03-11__11_mars_2024',
  'm_2024-04-03__3_april_2024_',
  'm_2024-05-06__6_mai_2024',
  'm_2025-01-17_17_januar_25',
  'm_2025-03-07_7_mars_25'
];

const MERGE_PAIRS = [
  { keep: 'm_2024-03-11_urbania_hovfaret_13_konseptskisse_1_0', remove: 'm_2024-03-11__11_mars_2024' },
  { keep: 'm_2024-04-03_urbania_leveransem_te_konsepskisse_og_st', remove: 'm_2024-04-03__3_april_2024_' },
  { keep: 'm_2024-05-06_hovfaret_13_med_r21', remove: 'm_2024-05-06__6_mai_2024' },
  { keep: 'm_2025-01-17_hovfaret_13_status_m_te_', remove: 'm_2025-01-17_17_januar_25' },
  { keep: 'm_2025-03-07_hovfaret_13_statusm_tet', remove: 'm_2025-03-07_7_mars_25' }
];

console.log('STEG 2: Merger duplikater...');

// Først, merge informasjon fra duplikatene til hovedpostene
for (const pair of MERGE_PAIRS) {
  const keepMeeting = data.meetings.find(m => m.id === pair.keep);
  const removeMeeting = data.meetings.find(m => m.id === pair.remove);

  if (keepMeeting && removeMeeting) {
    // Merge deltakere
    if (removeMeeting.participants) {
      const existingNames = keepMeeting.participants?.map(p => p.name) || [];
      for (const p of removeMeeting.participants) {
        if (!existingNames.includes(p.name)) {
          keepMeeting.participants = keepMeeting.participants || [];
          keepMeeting.participants.push(p);
        }
      }
    }

    // Merge topics
    if (removeMeeting.topics_discussed) {
      const existingTopics = keepMeeting.topics_discussed || [];
      for (const t of removeMeeting.topics_discussed) {
        if (!existingTopics.includes(t)) {
          keepMeeting.topics_discussed = keepMeeting.topics_discussed || [];
          keepMeeting.topics_discussed.push(t);
        }
      }
    }

    // Oppdater participant_count
    if (keepMeeting.participants) {
      keepMeeting.participant_count = keepMeeting.participants.length;
    }

    console.log(`  Merged: ${pair.remove} → ${pair.keep}`);
  }
}

// Så fjern duplikatene
const beforeDuplicates = data.meetings.length;
data.meetings = data.meetings.filter(m => !DUPLICATES_TO_REMOVE.includes(m.id));
console.log(`  Slettet: ${beforeDuplicates - data.meetings.length} duplikater\n`);

// ============================================
// STEG 3: Fiks korrupt data
// ============================================
console.log('STEG 3: Fikser korrupt data...');

let corruptFixed = 0;
for (const m of data.meetings) {
  // Fiks korrupte lokasjoner
  if (m.location && (
    m.location.includes('**') ||
    m.location.includes('<br>') ||
    m.location.includes('\\') ||
    m.location.length > 100
  )) {
    // Prøv å trekke ut sted fra korrupt data
    if (m.location.includes('Laboratoriet')) {
      m.location = 'Laboratoriet, Harbitz torg';
    } else {
      m.location = 'Ukjent';
    }
    corruptFixed++;
  }

  // Fiks escape-tegn i titler
  if (m.title && m.title.includes('\\.')) {
    m.title = m.title.replace(/\\\./g, '.');
    corruptFixed++;
  }

  // Fiks dårlige titler
  if (m.id === 'm_2024-11-27__27_november_24') {
    m.title = 'Hovfaret 13 - Statusmøte november';
    corruptFixed++;
  }

  if (m.id === 'm_2025_06_24_med_james_lorentzen' || m.title === 'med James Lorentzen') {
    m.title = 'Møte med James Lorentzen - Hovfaret 13';
    m.location = 'Ukjent';
    corruptFixed++;
  }
}

console.log(`  Fikset: ${corruptFixed} korrupte felt\n`);

// ============================================
// STEG 4: Auto-tildel møtetype
// ============================================
console.log('STEG 4: Tildeler møtetyper...');

const EXTERNAL_ORGS = ['Oslo kommune', 'Bydel Ullern', 'Statsforvalteren', 'NCC', 'Skøyen områdeforum'];

let typesAssigned = 0;
for (const m of data.meetings) {
  if (m.type) continue; // Skip hvis allerede har type

  const title = (m.title || '').toLowerCase();
  const location = (m.location || '').toLowerCase();
  const participantOrgs = m.participants?.map(p => p.organization) || [];

  // Sjekk for telefon
  if (title.includes('telefon') || location.includes('telefon') || title.includes('tlf')) {
    m.type = 'Telefonsamtale';
  }
  // Sjekk for befaring
  else if (title.includes('befaring')) {
    m.type = 'Befaring';
  }
  // Sjekk for workshop
  else if (title.includes('workshop')) {
    m.type = 'Workshop';
  }
  // Sjekk for presentasjon
  else if (title.includes('presentasjon')) {
    m.type = 'Presentasjon';
  }
  // Sjekk for bydelsmøte
  else if (title.includes('bydel') || title.includes('nabolag')) {
    m.type = 'Bydelsmøte';
  }
  // Sjekk for eksterne deltakere
  else if (participantOrgs.some(org => EXTERNAL_ORGS.some(ext => org?.includes(ext)))) {
    m.type = 'Eksterne møter';
  }
  // Sjekk for kun interne deltakere
  else if (participantOrgs.every(org =>
    !org || org.includes('Natural State') || org.includes('Urbania')
  )) {
    m.type = 'Interne møter';
  }
  // Default
  else {
    m.type = 'Prosjektmøte';
  }

  typesAssigned++;
}

console.log(`  Tildelt type til: ${typesAssigned} møter\n`);

// ============================================
// STEG 5: Fyll manglende lokasjoner
// ============================================
console.log('STEG 5: Fyller manglende lokasjoner...');

let locationsFixed = 0;
for (const m of data.meetings) {
  if (!m.location || m.location === '' || m.location === 'Ukjent' || m.location === 'MANGLER') {
    // Sjekk om rapporten nevner sted
    const summary = m.report?.summary || m.summary || '';

    if (summary.includes('Hovfaret 13') || summary.includes('Hovfaret')) {
      m.location = 'Hovfaret 13';
    } else if (summary.includes('Natural State kontor') || summary.includes('St. Halvards gate')) {
      m.location = 'Natural State kontor';
    } else if (m.type === 'Telefonsamtale') {
      m.location = 'Telefon';
    } else if (summary.includes('Teams') || summary.includes('digitalt')) {
      m.location = 'Digitalt møte';
    } else {
      m.location = 'Ikke spesifisert';
    }
    locationsFixed++;
  }
}

console.log(`  Oppdatert lokasjon for: ${locationsFixed} møter\n`);

// ============================================
// STEG 6: Oppdater metadata
// ============================================
console.log('STEG 6: Oppdaterer metadata...');

data.metadata = {
  ...data.metadata,
  version: '2.83',
  total_meetings: data.meetings.length,
  last_updated: new Date().toISOString().split('T')[0],
  cleanup_note: 'Data quality cleanup phase 62 - removed duplicates, non-meetings, fixed corrupt data, added types'
};

// Sorter møter etter dato
data.meetings.sort((a, b) => a.date.localeCompare(b.date));

console.log(`  Ny versjon: ${data.metadata.version}`);
console.log(`  Totalt antall møter: ${data.metadata.total_meetings}\n`);

// ============================================
// LAGRE
// ============================================
console.log('=== LAGRER ENDRINGER ===');

// Backup først
fs.writeFileSync(BACKUP_FILE, fs.readFileSync(MEETINGS_FILE));
console.log(`  Backup lagret: ${BACKUP_FILE}`);

// Lagre oppdatert fil
fs.writeFileSync(MEETINGS_FILE, JSON.stringify(data, null, 2), 'utf8');
console.log(`  Oppdatert fil lagret: ${MEETINGS_FILE}`);

// ============================================
// OPPSUMMERING
// ============================================
console.log('\n=== OPPSUMMERING ===');
console.log(`  Før: ${originalCount} møter`);
console.log(`  Etter: ${data.meetings.length} møter`);
console.log(`  Slettet: ${originalCount - data.meetings.length} poster`);
console.log(`  Alle møter har nå type: ${data.meetings.every(m => m.type) ? 'JA' : 'NEI'}`);
console.log(`  Alle møter har lokasjon: ${data.meetings.every(m => m.location) ? 'JA' : 'NEI'}`);

// Vis type-fordeling
const typeCount = {};
data.meetings.forEach(m => {
  typeCount[m.type] = (typeCount[m.type] || 0) + 1;
});
console.log('\n  Møtetyper:');
Object.entries(typeCount).sort((a,b) => b[1] - a[1]).forEach(([t, c]) => {
  console.log(`    ${t}: ${c}`);
});

console.log('\n=== FERDIG ===\n');
