import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = resolve(__dirname, '../../data');

// Descriptions for operational events (based on context)
const operationalDescriptions = {
  'o_001': 'Hovfaret 13 ble bygget med betongstruktur dimensjonert for 12 etasjer. Fundamentet muliggjør fremtidig vertikal utvidelse.',
  'o_002': 'Bygget fikk energimerke som dokumenterer energiforbruk og potensial for forbedringer.',
  'o_003': 'Byplangrep for Skøyen-området ble vedtatt med retningslinjer for fremtidig utvikling.',
  'o_004': 'Oslo bystyre vedtar områdeplan som krever riving av H13 og 10m tilbaketrekning fra Hoffselva.',
  'o_005': 'Områdeplanen sendes til Statsforvalteren for vurdering av innsigelser.',
  'o_006': 'Møte med byråd for byutvikling James Stove Lorentzen om transformasjonsmulighetene.',
  'o_007': 'Første formelle prosjektmøte mellom Urbania, Natural State og arkitekter. Systematisk arbeid starter.',
  'o_008': 'Natural State leverer konseptskisse og strategidokument til Urbania.',
  'o_009': 'R21 Arkitekter engasjeres for å utvikle detaljerte planer og scenarioer.',
  'o_010': 'R21 leverer 6 utviklingsscenarier inkludert kontor, bolig, Omsorg+ og kombinasjonsløsninger.',
  'o_011': 'Innspill sendt til Oslo kommunes planstrategi (KPS) om transformasjon fremfor riving.',
  'o_012': 'Planforutsetninger for bruksendring og transformasjon dokumenteres systematisk.',
  'o_013': 'Vill Energi gjennomfører befaring for energikartlegging og identifisering av tiltak.',
  'o_014': 'Transformasjonsplaner presenteres for nåværende leietakere. Dialog om overgang etableres.',
  'o_015': 'Kartlegging av miljørisiko inkludert grunnforhold, materialer og eksponering.',
  'o_016': 'Vill Energi leverer energirapport som viser vei til 50% energireduksjon og Enova-støtte.',
  'o_017': 'Klimagassberegninger v2 viser 48% CO₂-besparelse ved transformasjon vs. riving.',
  'o_018': 'Møte med Bente Otto fra Bydel Ullern om behov for omsorgsboliger i området.',
  'o_019': 'Omsorg+ presentasjoner fullført med 73 enheter og fellesfunksjoner.',
  'o_020': 'Omfattende bærekraftsrapport i henhold til ESRS-rammeverket ferdigstilles.',
  'o_021': 'Koordineringsmøte for rammesøknad med fokus på regulatorisk strategi.',
  'o_022': 'R21 leverer endelige tegninger, 3D-visualiseringer og planmateriale.'
};

// Norwegian titles for operational events
const operationalTitlesNo = {
  'o_001': 'Bygget oppført',
  'o_004': 'Rivingskrav vedtatt',
  'o_005': 'Plan sendt til Statsforvalteren',
  'o_007': 'PROSJEKTOPPSTART - Konseptskisse 1.0',
  'o_009': 'R21 Arkitekter engasjert',
  'o_010': 'R21 leverer 6 scenarioer',
  'o_014': 'Leietakerpresentasjon',
  'o_016': 'Energirapport levert',
  'o_017': 'Klimaberegninger v2 levert',
  'o_018': 'Møte med Bente Otto (Bydel Ullern)',
  'o_019': 'Omsorg+ presentasjoner fullført',
  'o_020': 'Bærekraftsrapport levert',
  'o_022': 'Endelig R21 leveranse (tegninger og planer)'
};

// Load timeline
const timelinePath = resolve(dataDir, 'timeline.json');
const data = JSON.parse(readFileSync(timelinePath, 'utf8'));

console.log('=== ENRICHING TIMELINE ===\n');

// Fix metadata counts
const strategicCount = data.events.strategic.length;
const operationalCount = data.events.operational.length;

console.log(`Strategic events: ${strategicCount} (was ${data.layers.strategic.event_count})`);
console.log(`Operational events: ${operationalCount} (was ${data.layers.operational.event_count})`);

data.layers.strategic.event_count = strategicCount;
data.layers.operational.event_count = operationalCount;

// Enrich operational events
let addedDescriptions = 0;
let addedTitlesNo = 0;

for (const event of data.events.operational) {
  // Add description if missing
  if (!event.description && operationalDescriptions[event.id]) {
    event.description = operationalDescriptions[event.id];
    addedDescriptions++;
    console.log(`✓ Description: ${event.id} - ${event.title.slice(0, 40)}...`);
  }

  // Add title_no if missing
  if (!event.title_no && operationalTitlesNo[event.id]) {
    event.title_no = operationalTitlesNo[event.id];
    addedTitlesNo++;
    console.log(`✓ Title_no: ${event.id} - ${event.title_no}`);
  }
}

// Update metadata
data.metadata.last_updated = new Date().toISOString().split('T')[0];
data.metadata.enrichment_note = 'Added descriptions and Norwegian titles for operational events.';

// Write back
writeFileSync(timelinePath, JSON.stringify(data, null, 2));

console.log(`\n=== SUMMARY ===`);
console.log(`Fixed metadata: strategic ${strategicCount}, operational ${operationalCount}`);
console.log(`Added descriptions: ${addedDescriptions}`);
console.log(`Added title_no: ${addedTitlesNo}`);
console.log('Saved timeline.json');
