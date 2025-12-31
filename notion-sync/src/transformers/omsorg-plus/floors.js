import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../../config.js';

export function loadOmsorgPlusFloors() {
  const filePath = resolve(DATA_DIR, 'themes/omsorg-plus.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));

  return (data.floors || []).map(floor => ({
    id: `floor_${floor.floor.replace(/[-\s]/g, '_').toLowerCase()}`,
    ...floor
  }));
}

export const omsorgPlusFloorsSchema = {
  'Name': { title: {} },
  'Floor Code': { rich_text: {} },
  'Norwegian Name': { rich_text: {} },
  'Type': { select: {} },
  'Functions': { multi_select: {} },
  'Units Per Floor': { number: {} },
  'Common Area (m²)': { number: {} },
  'Service Area (m²)': { number: {} },
  'Bike Storage (m²)': { number: {} },
  'Parking (m²)': { number: {} },
  'Unit Distribution': { rich_text: {} }
};

export function transformOmsorgPlusFloor(floor) {
  // Handle different function formats (array or object)
  let functions = [];
  if (Array.isArray(floor.functions)) {
    functions = floor.functions;
  } else if (typeof floor.functions === 'object' && floor.functions !== null) {
    // Flatten object values into array
    functions = Object.values(floor.functions).flat();
  }

  // Format unit distribution if present
  let unitDistribution = '';
  if (floor.unit_distribution) {
    unitDistribution = Object.entries(floor.unit_distribution)
      .map(([size, count]) => `${count}x ${size}`)
      .join(', ');
  }

  return {
    'Name': { title: [{ text: { content: `${floor.floor} - ${floor.name_no}` } }] },
    'Floor Code': { rich_text: [{ text: { content: floor.floor || '' } }] },
    'Norwegian Name': { rich_text: [{ text: { content: floor.name_no || '' } }] },
    'Type': floor.type ? { select: { name: floor.type } } : undefined,
    'Functions': {
      multi_select: functions
        .slice(0, 100)
        .map(f => ({ name: String(f).replace(/,/g, ';').slice(0, 100) }))
    },
    'Units Per Floor': floor.units_per_floor ? { number: floor.units_per_floor } : undefined,
    'Common Area (m²)': floor.common_area_m2 ? { number: floor.common_area_m2 } : undefined,
    'Service Area (m²)': floor.service_area_m2 ? { number: floor.service_area_m2 } : undefined,
    'Bike Storage (m²)': floor.bike_storage_m2 ? { number: floor.bike_storage_m2 } : undefined,
    'Parking (m²)': floor.parking_m2 ? { number: floor.parking_m2 } : undefined,
    'Unit Distribution': unitDistribution ? { rich_text: [{ text: { content: unitDistribution } }] } : undefined
  };
}
