import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../../config.js';

export function loadOmsorgPlusUnits() {
  const filePath = resolve(DATA_DIR, 'themes/omsorg-plus.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));

  const units = [];

  // Expand unit types into individual units
  for (const unitType of (data.units || [])) {
    const count = unitType.count_in_project || 1;
    for (let i = 1; i <= count; i++) {
      units.push({
        id: `${unitType.id}_${String(i).padStart(3, '0')}`,
        unit_number: i,
        ...unitType
      });
    }
  }

  return units;
}

export const omsorgPlusUnitsSchema = {
  'Name': { title: {} },
  'Unit ID': { rich_text: {} },
  'Unit Type': { select: {} },
  'Type Name': { rich_text: {} },
  'Total Area (m²)': { number: {} },
  'Distribution (%)': { number: {} },
  'Target Occupants': { number: {} },
  'Living Room Area (m²)': { number: {} },
  'Bedroom Area (m²)': { number: {} },
  'Bathroom Area (m²)': { number: {} },
  'Entrance Area (m²)': { number: {} },
  'Balcony Area (m²)': { number: {} },
  'Living Room Features': { multi_select: {} },
  'Bedroom Features': { multi_select: {} },
  'Bathroom Features': { multi_select: {} },
  'Entrance Features': { multi_select: {} },
  'Balcony Features': { multi_select: {} }
};

function extractFeatures(room) {
  if (!room || !room.features) return [];
  return room.features
    .slice(0, 20)
    .map(f => ({ name: f.replace(/,/g, ';').slice(0, 100) }));
}

export function transformOmsorgPlusUnit(unit) {
  const rooms = unit.rooms || {};

  return {
    'Name': { title: [{ text: { content: `${unit.name_no || unit.type} #${unit.unit_number}` } }] },
    'Unit ID': { rich_text: [{ text: { content: unit.id || '' } }] },
    'Unit Type': unit.type ? { select: { name: unit.type.slice(0, 100) } } : undefined,
    'Type Name': { rich_text: [{ text: { content: unit.name_no || '' } }] },
    'Total Area (m²)': { number: unit.total_area_m2 || 0 },
    'Distribution (%)': { number: unit.distribution_percent || 0 },
    'Target Occupants': { number: unit.target_occupants || 1 },
    'Living Room Area (m²)': rooms.living_room_kitchen ? { number: rooms.living_room_kitchen.area_m2 } : undefined,
    'Bedroom Area (m²)': rooms.bedroom ? { number: rooms.bedroom.area_m2 } : undefined,
    'Bathroom Area (m²)': rooms.bathroom ? { number: rooms.bathroom.area_m2 } : undefined,
    'Entrance Area (m²)': rooms.entrance ? { number: rooms.entrance.area_m2 } : undefined,
    'Balcony Area (m²)': rooms.balcony ? { number: rooms.balcony.area_m2 } : undefined,
    'Living Room Features': { multi_select: extractFeatures(rooms.living_room_kitchen) },
    'Bedroom Features': { multi_select: extractFeatures(rooms.bedroom) },
    'Bathroom Features': { multi_select: extractFeatures(rooms.bathroom) },
    'Entrance Features': { multi_select: extractFeatures(rooms.entrance) },
    'Balcony Features': { multi_select: extractFeatures(rooms.balcony) }
  };
}
