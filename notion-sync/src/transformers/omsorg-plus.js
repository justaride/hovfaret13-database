import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../config.js';

export function loadOmsorgPlusUnits() {
  const filePath = resolve(DATA_DIR, 'themes/omsorg-plus.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));

  const units = [];

  if (data.unit_types) {
    for (const unitType of data.unit_types) {
      const count = unitType.count_in_project || 1;
      for (let i = 1; i <= count; i++) {
        units.push({
          ...unitType,
          unit_number: i,
          unit_id: `${unitType.id}_${i}`
        });
      }
    }
  }

  if (data.housing_program?.unit_mix) {
    for (const unit of data.housing_program.unit_mix) {
      units.push({
        ...unit,
        unit_id: unit.id || `unit_${units.length + 1}`
      });
    }
  }

  if (units.length === 0 && data.units) {
    return data.units;
  }

  return units.length > 0 ? units : [data];
}

export const omsorgPlusSchema = {
  'Name': { title: {} },
  'Unit Type': { select: {} },
  'Total Area (m2)': { number: {} },
  'Distribution (%)': { number: {} },
  'Target Occupants': { number: {} },
  'Count': { number: {} },
  'Living Area (m2)': { number: {} },
  'Bedroom Area (m2)': { number: {} },
  'Bathroom Area (m2)': { number: {} },
  'Floor': { select: {} }
};

export function transformOmsorgPlusUnit(unit) {
  const name = unit.type
    ? `${unit.type} #${unit.unit_number || 1}`
    : `Unit ${unit.unit_id || 'Unknown'}`;

  return {
    'Name': { title: [{ text: { content: name.slice(0, 2000) } }] },
    'Unit Type': unit.type ? { select: { name: unit.type.slice(0, 100) } } : undefined,
    'Total Area (m2)': { number: unit.total_area_m2 || 0 },
    'Distribution (%)': { number: unit.distribution_percent || 0 },
    'Target Occupants': { number: unit.target_occupants || 0 },
    'Count': { number: unit.count_in_project || 1 },
    'Living Area (m2)': { number: unit.rooms?.living_room_kitchen?.area_m2 || unit.rooms?.stue_kjokken?.area_m2 || 0 },
    'Bedroom Area (m2)': { number: unit.rooms?.bedroom?.area_m2 || unit.rooms?.soverom?.area_m2 || 0 },
    'Bathroom Area (m2)': { number: unit.rooms?.bathroom?.area_m2 || unit.rooms?.bad?.area_m2 || 0 },
    'Floor': unit.floor ? { select: { name: String(unit.floor) } } : undefined
  };
}
