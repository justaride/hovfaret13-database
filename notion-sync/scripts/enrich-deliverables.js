import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = resolve(__dirname, '../../data');

// Responsible assignments based on category and context
const responsibleAssignments = {
  'd_008': ['kamran_surizehi'],      // Samle innspill - nabolagsmøte category
  'd_013': ['kamran_surizehi'],      // Facebook side - social media
  'd_014': ['kamran_surizehi'],      // Instagram - social media
  'd_017': ['kamran_surizehi'],      // 1 post i mnd - social media
  'd_019': ['kamran_surizehi'],      // Informere om Omsorg+ - tenant relations
  'd_020': ['kamran_surizehi'],      // Bekrefte kontrakter - tenant relations
  'd_021': ['andreas_thorsnes'],     // Rekruttering leietakere - Urbania
  'd_022': ['thomas_thorsen'],       // Bruksendringssøknad - external regulatory
  'd_024': ['kamran_surizehi'],      // Nabovarsel sendt - completed, NS coordinated
  'd_025': ['thomas_thorsen'],       // Konseptskisse 2.0 - R21
  'd_026': ['gabriel_boen'],         // Bærekrafts-kalkyle - NS sustainability
  'd_027': ['einar_holthe'],         // Stedsøkonomisk prognose - NS strategy
  'd_028': ['severin_docker'],       // NCC prosjektering - NCC
  'd_029': ['kamran_surizehi'],      // Gjøre klart Omsorg+ - NS
  'd_030': ['kamran_surizehi'],      // Medvirkningsrapport - NS
  'd_031': ['kamran_surizehi'],      // Påmelding nabolagsmøtet - NS
  'd_032': ['andreas_thorsnes'],     // Bank finansiering - Urbania
  'd_033': ['andreas_thorsnes'],     // Bankmøte - Urbania
  'd_034': ['gabriel_boen'],         // Kartlegge finansiering - NS
  'd_037': ['linda_marie_aas']       // Merkevareplattform - Parabol coordination
};

// Norwegian titles where missing (most are already Norwegian)
const norwegianTitles = {
  'd_002': 'Planlegging nabolagsmøte',
  'd_004': 'Presentasjon nabolagsmøte',
  'd_005': 'Heng opp invitasjoner',
  'd_006': 'Plansjer til Temastasjon - R21',
  'd_007': 'Oppsummering nabolagsmøte',
  'd_008': 'Samle innspill nabolagsmøte',
  'd_010': 'Landing page før nabolagsmøtet',
  'd_011': 'Kommunikasjonsstrategi',
  'd_012': 'Lage 4 artikler og publisere før jul',
  'd_013': 'Facebook side',
  'd_014': 'Instagram - Meta',
  'd_015': 'Post SoMe Hovfaret kanaler',
  'd_016': 'Post SoMe Natural State / NCC',
  'd_017': '1 post i mnd',
  'd_018': 'Leietakersamtaler',
  'd_021': 'Rekruttering temporære leietakere',
  'd_022': 'Bruksendringssøknad',
  'd_023': 'Rammeinnsendelse',
  'd_024': 'Nabovarsel sendt',
  'd_025': 'Konseptskisse 2.0',
  'd_026': 'Bærekrafts-kalkyle',
  'd_027': 'Stedsøkonomisk prognose 2.0',
  'd_028': 'Teoretisk prosjektering NCC',
  'd_029': 'Gjøre klart Omsorg+',
  'd_030': 'Medvirkningsrapport',
  'd_031': 'Påmelding nabolagsmøtet',
  'd_032': 'Bank finansiering',
  'd_033': 'Bankmøte',
  'd_034': 'Kartlegge finansiering og støtteordninger',
  'd_035': 'Bydelsutvalgsmøte',
  'd_036': 'Grunneierforum OMA møte',
  'd_037': 'Merkevareplattform - Parabol'
};

// Load deliverables
const deliverablesPath = resolve(dataDir, 'deliverables.json');
const data = JSON.parse(readFileSync(deliverablesPath, 'utf8'));

console.log('=== ENRICHING DELIVERABLES ===\n');

let assignedResponsible = 0;
let addedTitleNo = 0;

for (const del of data.deliverables) {
  // Assign responsible if empty
  if ((!del.responsible || del.responsible.length === 0) && responsibleAssignments[del.id]) {
    del.responsible = responsibleAssignments[del.id];
    assignedResponsible++;
    console.log(`✓ Responsible: ${del.id} - ${del.title.slice(0, 40)} → ${del.responsible.join(', ')}`);
  }

  // Add title_no if missing
  if (!del.title_no && norwegianTitles[del.id]) {
    del.title_no = norwegianTitles[del.id];
    addedTitleNo++;
    console.log(`✓ Title_no: ${del.id} - ${del.title_no}`);
  }
}

// Update metadata
data.metadata.last_updated = new Date().toISOString().split('T')[0];
data.metadata.enrichment_note = 'Assigned responsible persons and added Norwegian titles.';

// Write back
writeFileSync(deliverablesPath, JSON.stringify(data, null, 2));

// Count stats
const withResponsible = data.deliverables.filter(d => d.responsible && d.responsible.length > 0).length;
const withTitleNo = data.deliverables.filter(d => d.title_no).length;

console.log(`\n=== SUMMARY ===`);
console.log(`Assigned responsible: ${assignedResponsible}`);
console.log(`Added title_no: ${addedTitleNo}`);
console.log(`Deliverables with responsible: ${withResponsible}/${data.deliverables.length} (${Math.round(100*withResponsible/data.deliverables.length)}%)`);
console.log(`Deliverables with title_no: ${withTitleNo}/${data.deliverables.length} (${Math.round(100*withTitleNo/data.deliverables.length)}%)`);
console.log('Saved deliverables.json');
