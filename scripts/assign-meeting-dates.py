#!/usr/bin/env python3
"""
Assign Meeting Dates Script
Assigns dates to meetings with unknown dates based on:
- Filename analysis
- Content analysis
- Context from other meetings
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
RESTRUCTURED_DIR = BASE_DIR / "data" / "restructured_notes"

# Norwegian months mapping
NORWEGIAN_MONTHS = {
    'januar': '01', 'februar': '02', 'mars': '03', 'april': '04',
    'mai': '05', 'juni': '06', 'juli': '07', 'august': '08',
    'september': '09', 'oktober': '10', 'okt': '10', 'november': '11', 'nov': '11',
    'desember': '12', 'des': '12'
}

def load_json(filepath: Path) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath: Path, data: Dict):
    """Save JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_date_from_filename(filename: str) -> Optional[Tuple[int, int, Optional[int]]]:
    """Extract day, month, year from filename"""
    # Pattern 1: "MØTE  13 MAI  -2035.md" or "MØTE  22 MAI  .md"
    pattern1 = r'MØTE\s+(\d{1,2})\s+(\w+)\s+'
    match = re.search(pattern1, filename, re.IGNORECASE)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()
        month = int(NORWEGIAN_MONTHS.get(month_str, 0))

        # Try to find year in filename
        year_match = re.search(r'(\d{4})', filename)
        if year_match:
            year = int(year_match.group(1))
            # Fix obvious typo: 2035 → 2025
            if year == 2035:
                year = 2025
        else:
            year = None

        if month > 0:
            return (day, month, year)

    # Pattern 2: "MØTE 24.06 2025"
    pattern2 = r'MØTE\s+(\d{1,2})\.(\d{1,2})\s+(\d{4})'
    match = re.search(pattern2, filename, re.IGNORECASE)
    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        return (day, month, year)

    return None

def search_date_in_content(filepath: Path) -> Optional[str]:
    """Search for explicit dates in file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for explicit date patterns in content
        # Pattern: "Tirsdag 13. mai 2025"
        pattern1 = r'(\d{1,2})\.\s*(\w+)\s+(\d{4})'
        match = re.search(pattern1, content)
        if match:
            day = int(match.group(1))
            month_str = match.group(2).lower()
            year = int(match.group(3))
            month = NORWEGIAN_MONTHS.get(month_str)
            if month:
                return f"{year}-{month}-{day:02d}"

        # Pattern: "Dato: DD.MM.YYYY"
        pattern2 = r'Dato[:\s]+(\d{1,2})\.(\d{1,2})\.(\d{4})'
        match = re.search(pattern2, content)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3))
            return f"{year}-{month:02d}-{day:02d}"

    except Exception as e:
        print(f"   ⚠️  Error reading {filepath}: {e}")

    return None

def propose_date(meeting: Dict, meetings_data: Dict) -> Optional[str]:
    """Propose a date for a meeting based on available information"""

    # Check if meeting already has a date
    if meeting.get('date'):
        return meeting['date']

    # Get report link
    report_link = meeting.get('report_link', '')
    if not report_link:
        return None

    # Get filename from report_link
    filename = Path(report_link).name

    # First, check file content for explicit date
    report_path = BASE_DIR / report_link.replace('data/', '')
    if report_path.exists():
        content_date = search_date_in_content(report_path)
        if content_date:
            return content_date

    # Extract from filename
    date_parts = extract_date_from_filename(filename)
    if not date_parts:
        return None

    day, month, year = date_parts

    # If no year, infer from context
    if not year:
        # Get all existing meeting dates to understand the timeline
        existing_dates = [m['date'] for m in meetings_data['meetings'] if m.get('date')]
        existing_dates.sort()

        # Strategy: Most meetings seem to be in 2024-2025 timeframe
        # If month is >= current month (November = 11), use 2024
        # Otherwise use 2025
        if month >= 11:
            year = 2024
        else:
            year = 2025

    return f"{year}-{month:02d}-{day:02d}"

def main():
    """Main execution function"""
    print("📅 Tildeler datoer til møter med ukjent dato...")
    print()

    # Load meetings data
    meetings_data = load_json(MEETINGS_JSON)
    meetings = meetings_data['meetings']

    # Find meetings without dates
    meetings_without_dates = [m for m in meetings if not m.get('date') or m['date'] is None]

    print(f"Fant {len(meetings_without_dates)} møter uten dato:")
    print()

    # Propose dates for each
    proposals = []
    for meeting in meetings_without_dates:
        proposed_date = propose_date(meeting, meetings_data)

        if proposed_date:
            proposals.append({
                'meeting': meeting,
                'proposed_date': proposed_date,
                'filename': Path(meeting.get('report_link', '')).name if meeting.get('report_link') else 'N/A'
            })

    # Display proposals
    if not proposals:
        print("❌ Ingen datoforslag funnet.")
        return

    print(f"{'='*80}")
    print(f"DATOFORSLAG")
    print(f"{'='*80}")
    print()

    for i, prop in enumerate(proposals, 1):
        meeting = prop['meeting']
        print(f"{i}. {meeting['title'][:60]}")
        print(f"   ID: {meeting['id']}")
        print(f"   Foreslått dato: {prop['proposed_date']}")
        print(f"   Kilde: {prop['filename']}")
        print()

    # Update meetings automatically
    updates_count = 0
    for prop in proposals:
        meeting_id = prop['meeting']['id']
        new_date = prop['proposed_date']

        # Find and update the meeting in the list
        for m in meetings_data['meetings']:
            if m['id'] == meeting_id:
                m['date'] = new_date
                updates_count += 1

                # Also update data_quality_note
                if m.get('data_quality_note'):
                    m['data_quality_note'] = f"Auto-assigned date from filename/content - needs verification"

                print(f"   ✅ Oppdatert: {m['title'][:50]} → {new_date}")
                break

    # Update metadata
    meetings_data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')

    # Save updated meetings.json
    save_json(MEETINGS_JSON, meetings_data)

    print()
    print(f"✅ Oppdatert {updates_count} møter med nye datoer!")
    print(f"📝 meetings.json er lagret.")
    print()
    print("🔍 NESTE STEG:")
    print("   1. Verifiser at datoene er korrekte (sjekk kalender/e-post)")
    print("   2. Fjern 'data_quality_note' fra verifiserte møter")
    print("   3. Fortsett med manuell kvalitetssikring")

if __name__ == '__main__':
    main()
