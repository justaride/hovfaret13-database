#!/usr/bin/env python3
"""
Update meetings.json with links to polished notes
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
POLISHED_DIR = BASE_DIR / "data" / "polished_notes"

def load_json(filepath: Path):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath: Path, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_polished_note(meeting_id: str, date: str) -> Path:
    """Find polished note for a meeting"""

    # Try exact match first
    pattern1 = f"{date}_{meeting_id}_POLISHED.md"
    match = POLISHED_DIR / pattern1
    if match.exists():
        return match

    # Try with underscores instead of dashes in date
    date_underscore = date.replace('-', '_')
    pattern2 = f"{date_underscore}_{meeting_id}_POLISHED.md"
    match = POLISHED_DIR / pattern2
    if match.exists():
        return match

    # Search for any file containing the meeting_id
    for file in POLISHED_DIR.glob(f"*{meeting_id}*_POLISHED.md"):
        return file

    # Search by date
    for file in POLISHED_DIR.glob(f"{date}*_POLISHED.md"):
        return file

    for file in POLISHED_DIR.glob(f"{date_underscore}*_POLISHED.md"):
        return file

    return None

def main():
    print("📝 Oppdaterer meetings.json med polished notes...")
    print()

    # Create backup
    backup_path = MEETINGS_JSON.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    shutil.copy(MEETINGS_JSON, backup_path)
    print(f"💾 Backup: {backup_path}")
    print()

    # Load meetings
    meetings_data = load_json(MEETINGS_JSON)
    meetings = meetings_data['meetings']

    # Update meetings with polished note links
    updated = 0
    not_found = 0

    for meeting in meetings:
        meeting_id = meeting['id']
        date = meeting.get('date')

        if not date:
            continue

        # Find polished note
        polished_note = find_polished_note(meeting_id, date)

        if polished_note:
            # Update meeting with polished note link
            relative_path = f"data/polished_notes/{polished_note.name}"

            # Store old report_link as original_report_link
            if meeting.get('report_link') and 'polished_notes' not in meeting.get('report_link', ''):
                meeting['original_report_link'] = meeting['report_link']

            # Update to polished note
            meeting['report_link'] = relative_path

            # Add polished metadata
            if 'report_metadata' not in meeting:
                meeting['report_metadata'] = {}

            meeting['report_metadata']['polished'] = True
            meeting['report_metadata']['polished_date'] = datetime.now().strftime('%Y-%m-%d')

            updated += 1
            print(f"✅ {meeting['title'][:50]}")
            print(f"   → {polished_note.name}")
        else:
            not_found += 1
            print(f"⚠️  Ingen polished note funnet: {meeting['title'][:50]}")

    # Update metadata
    meetings_data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    meetings_data['metadata']['polished_notes_linked'] = updated

    # Save
    save_json(MEETINGS_JSON, meetings_data)

    print()
    print(f"{'='*60}")
    print(f"RESULTAT")
    print(f"{'='*60}")
    print(f"Oppdatert: {updated} møter")
    print(f"Ikke funnet: {not_found} møter")
    print()
    print("✅ meetings.json oppdatert!")

if __name__ == '__main__':
    main()
