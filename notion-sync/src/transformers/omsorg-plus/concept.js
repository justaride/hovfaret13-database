import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../../config.js';

export function loadOmsorgPlusConcept() {
  const filePath = resolve(DATA_DIR, 'themes/omsorg-plus.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));

  // Create single concept record combining multiple sections
  return [{
    id: 'omsorg_plus_concept',
    ...data.concept,
    ...data.proposed_design,
    financing: data.financing.husbanken_support,
    market_position: data.market_position,
    competitive_advantages: data.competitive_advantages,
    areas: data.areas.hovfaret_13,
    next_steps: data.next_steps
  }];
}

export const omsorgPlusConceptSchema = {
  'Name': { title: {} },
  'Purpose': { rich_text: {} },
  'Target Group': { rich_text: {} },
  'Age Minimum': { number: {} },
  'Care Level': { rich_text: {} },
  'Unit Count': { number: {} },
  'Total BTA (m²)': { number: {} },
  'Scenario': { rich_text: {} },
  'Key Features': { multi_select: {} },
  'Ownership Model': { select: {} },
  'Regulatory Framework': { rich_text: {} },
  'Collaborators': { multi_select: {} },
  'Service Area Ratio': { rich_text: {} },
  'Units BRA (m²)': { number: {} },
  'Service Areas (m²)': { number: {} },
  'Husbanken Max/Unit': { rich_text: {} },
  'Subsidy Coverage': { rich_text: {} },
  'Binding Period (years)': { number: {} },
  'Total Oslo Facilities': { number: {} },
  'Market Position': { rich_text: {} },
  'Next Steps': { rich_text: {} }
};

export function transformOmsorgPlusConcept(concept) {
  const keyFeatures = (concept.key_features || [])
    .slice(0, 100)
    .map(f => ({ name: f.replace(/,/g, ';').slice(0, 100) }));

  const collaborators = (concept.collaborators || [])
    .slice(0, 100)
    .map(c => ({ name: c.replace(/,/g, ';').slice(0, 100) }));

  const nextSteps = (concept.next_steps || []).join('\n');

  return {
    'Name': { title: [{ text: { content: concept.name || 'Omsorg+ Konsept' } }] },
    'Purpose': { rich_text: [{ text: { content: (concept.purpose || '').slice(0, 2000) } }] },
    'Target Group': { rich_text: [{ text: { content: (concept.target_group?.description || '').slice(0, 2000) } }] },
    'Age Minimum': { number: concept.target_group?.age_minimum || 67 },
    'Care Level': { rich_text: [{ text: { content: (concept.target_group?.care_level || '').slice(0, 2000) } }] },
    'Unit Count': { number: concept.unit_count || 73 },
    'Total BTA (m²)': { number: concept.total_bta_m2 || 8472 },
    'Scenario': { rich_text: [{ text: { content: (concept.scenario || '').slice(0, 2000) } }] },
    'Key Features': { multi_select: keyFeatures },
    'Ownership Model': concept.ownership_model ? { select: { name: concept.ownership_model.slice(0, 100) } } : undefined,
    'Regulatory Framework': { rich_text: [{ text: { content: (concept.regulatory_framework || '').slice(0, 2000) } }] },
    'Collaborators': { multi_select: collaborators },
    'Service Area Ratio': { rich_text: [{ text: { content: `${concept.areas?.service_percent || 31}% vs ${15}-20% typisk` } }] },
    'Units BRA (m²)': { number: concept.areas?.units_bra_m2 || 2958 },
    'Service Areas (m²)': { number: concept.areas?.service_areas_m2 || 2068 },
    'Husbanken Max/Unit': { rich_text: [{ text: { content: (concept.financing?.max_per_unit_oslo || '2 124 000 kr').slice(0, 2000) } }] },
    'Subsidy Coverage': { rich_text: [{ text: { content: (concept.financing?.coverage || '45%').slice(0, 2000) } }] },
    'Binding Period (years)': { number: parseInt(concept.financing?.binding_period) || 30 },
    'Total Oslo Facilities': { number: concept.market_position?.total_oslo_facilities || 13 },
    'Market Position': { rich_text: [{ text: { content: (concept.market_position?.key_insight || '').slice(0, 2000) } }] },
    'Next Steps': { rich_text: [{ text: { content: nextSteps.slice(0, 2000) } }] }
  };
}
