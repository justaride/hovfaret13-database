import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../config.js';

export function loadSustainabilityScenarios() {
  const filePath = resolve(DATA_DIR, 'themes/sustainability.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));

  if (data.klimagassberegninger?.scenarios) {
    return Object.values(data.klimagassberegninger.scenarios);
  }

  if (data.scenarios) {
    return Array.isArray(data.scenarios) ? data.scenarios : Object.values(data.scenarios);
  }

  if (data.lca_analysis?.scenarios) {
    return Object.values(data.lca_analysis.scenarios);
  }

  return [];
}

export const sustainabilitySchema = {
  'Name': { title: {} },
  'ID': { rich_text: {} },
  'Description': { rich_text: {} },
  'Materials (tonnes CO2)': { number: {} },
  'Energy (tonnes CO2)': { number: {} },
  'Total CO2 (tonnes)': { number: {} },
  'Per m² Materials (kg)': { number: {} },
  'Per m² Energy (kg)': { number: {} },
  'Per m² Total (kg)': { number: {} },
  'Status': { select: {} },
  'CO2 Reduction vs Demolition (%)': { number: {} }
};

export function transformSustainabilityScenario(scenario) {
  const statusMap = {
    'not_recommended': 'Ikke anbefalt',
    'recommended': 'Anbefalt',
    'preferred': 'Foretrukket'
  };

  return {
    'Name': { title: [{ text: { content: (scenario.name || 'Unnamed Scenario').slice(0, 2000) } }] },
    'ID': { rich_text: [{ text: { content: scenario.id || '' } }] },
    'Description': { rich_text: [{ text: { content: (scenario.description || '').slice(0, 2000) } }] },
    'Materials (tonnes CO2)': { number: scenario.totals?.materials_tonnes || 0 },
    'Energy (tonnes CO2)': { number: scenario.totals?.energy_tonnes || 0 },
    'Total CO2 (tonnes)': { number: scenario.totals?.total_tonnes || 0 },
    'Per m² Materials (kg)': { number: scenario.per_bta?.materials_kg_m2 || 0 },
    'Per m² Energy (kg)': { number: scenario.per_bta?.energy_kg_m2 || 0 },
    'Per m² Total (kg)': { number: scenario.per_bta?.total_kg_m2 || 0 },
    'Status': scenario.status ? { select: { name: statusMap[scenario.status] || scenario.status } } : undefined,
    'CO2 Reduction vs Demolition (%)': { number: scenario.vs_scenario_1?.total_reduction_percent || 0 }
  };
}
