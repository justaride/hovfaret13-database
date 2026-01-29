#!/usr/bin/env python3
"""
Apply Note Matches Script
Applies the matching analysis results:
- Matches notes to existing meetings (high confidence matches)
- Creates new meetings for unmatched notes
- Updates meetings.json
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
SUGGESTED_MEETINGS = BASE_DIR / "analysis" / "suggested_new_meetings.json"
PARSED_NOTES = BASE_DIR / "analysis" / "meeting_notes_parsed.json"
RESTRUCTURED_DIR = BASE_DIR / "data" / "restructured_notes"

# Matching confidence threshold
HIGH_CONFIDENCE_THRESHOLD = 50.0

def load_json(filepath: Path) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath: Path, data: Dict):
    """Save JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_backup(filepath: Path):
    """Create backup of file"""
    backup_path = filepath.with_suffix('.backup_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json')
    shutil.copy(filepath, backup_path)
    return backup_path

def find_potential_match(note: Dict, meetings: List[Dict]) -> tuple:
    """Find potential meeting match for a note"""
    # Import matching logic from previous script
    import re

    note_title = note['title'].lower()
    note_content = note['content'].lower()

    best_match = None
    best_score = 0

    for meeting in meetings:
        score = 0

        # Check title similarity
        meeting_title = meeting['title'].lower()
        if note_title in meeting_title or meeting_title in note_title:
            score += 30

        # Check for common words in title
        note_words = set(re.findall(r'\w+', note_title))
        meeting_words = set(re.findall(r'\w+', meeting_title))
        common_words = note_words.intersection(meeting_words)
        if len(common_words) >= 2:
            score += 10 * len(common_words)

        # Check for date proximity
        if note.get('date') and meeting.get('date'):
            try:
                note_date = datetime.strptime(note['date'], '%Y-%m-%d')
                meeting_date = datetime.strptime(meeting['date'], '%Y-%m-%d')
                days_diff = abs((note_date - meeting_date).days)
                if days_diff == 0:
                    score += 50
                elif days_diff <= 7:
                    score += 20
            except:
                pass

        if score > best_score:
            best_score = score
            best_match = meeting

    return best_match, best_score

def enrich_meeting_with_note(meeting: Dict, note: Dict) -> Dict:
    """Enrich meeting with data from note"""
    # Add report link
    if note.get('date'):
        report_filename = f"{note['date']}_{note['filename']}"
    else:
        report_filename = f"UKJENT_DATO_{note['filename']}"

    meeting['report_link'] = f"data/restructured_notes/{report_filename}"

    # Add or merge action items
    note_actions = note.get('action_items', [])
    existing_actions = meeting.get('action_items', [])
    all_actions = existing_actions + [a for a in note_actions if a not in existing_actions]
    meeting['action_items'] = all_actions

    # Add or merge topics
    note_topics = note.get('topics_discussed', [])
    existing_topics = meeting.get('topics_discussed', [])
    all_topics = existing_topics + [t for t in note_topics if t not in existing_topics]
    meeting['topics_discussed'] = all_topics

    # Add or merge decisions
    note_decisions = note.get('decisions', [])
    existing_decisions = meeting.get('decisions', [])
    all_decisions = existing_decisions + [d for d in note_decisions if d not in existing_decisions]
    meeting['decisions'] = all_decisions

    # Add report metadata
    meeting['report_metadata'] = {
        'word_count': note['word_count'],
        'matched_from_note': note['filename'],
        'match_date': datetime.now().isoformat()
    }

    return meeting

def generate_meeting_id(title: str, date: str = None) -> str:
    """Generate unique meeting ID"""
    import re

    if date:
        date_part = date.replace('-', '_')
    else:
        date_part = 'unknown_date'

    # Clean title for ID
    title_clean = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    title_part = '_'.join(title_clean.split()[:6])

    return f"m_{date_part}_{title_part}"

def create_new_meeting_from_note(note: Dict) -> Dict:
    """Create new meeting entry from note"""
    # Extract or estimate date
    date = note.get('date')

    # Generate meeting ID
    meeting_id = generate_meeting_id(note['title'], date)

    # Create report link
    if date:
        report_filename = f"{date}_{note['filename']}"
    else:
        report_filename = f"UKJENT_DATO_{note['filename']}"

    new_meeting = {
        'id': meeting_id,
        'date': date,
        'title': note['title'],
        'organizer': None,
        'location': note.get('location'),
        'participant_count': len(note.get('participants', [])),
        'participants': [
            {'name': p, 'organization': None, 'email': None}
            for p in note.get('participants', [])
        ],
        'action_items': note.get('action_items', []),
        'topics_discussed': note.get('topics_discussed', []),
        'decisions': note.get('decisions', []),
        'report_link': f"data/restructured_notes/{report_filename}",
        'report_metadata': {
            'word_count': note['word_count'],
            'source': 'Downloaded meeting notes - auto-created',
            'needs_review': True,
            'created_date': datetime.now().isoformat()
        },
        'data_quality_note': 'Auto-generated from meeting notes - needs manual review'
    }

    return new_meeting

def main():
    """Main execution function"""
    print("🔧 Matcher notater og oppdaterer meetings.json...")

    # Create backup
    backup_path = create_backup(MEETINGS_JSON)
    print(f"   💾 Backup opprettet: {backup_path}")

    # Load data
    meetings_data = load_json(MEETINGS_JSON)
    parsed_notes_data = load_json(PARSED_NOTES)

    meetings = meetings_data['meetings']
    all_notes = parsed_notes_data['notes']

    # Find already matched meetings
    meetings_by_date = {m['date']: m for m in meetings if m.get('date')}

    # Process unmatched notes
    matched_notes = []
    new_meetings = []
    enriched_meetings = []

    for note in all_notes:
        # Skip if already matched by date
        if note.get('date') and note['date'] in meetings_by_date:
            matched = meetings_by_date[note['date']]
            enriched = enrich_meeting_with_note(matched, note)
            enriched_meetings.append(enriched)
            print(f"   ✅ Beriket eksisterende: {matched['title']}")
            continue

        # Try to find match
        match, score = find_potential_match(note, meetings)

        if match and score >= HIGH_CONFIDENCE_THRESHOLD:
            # High confidence match - enrich existing meeting
            enriched = enrich_meeting_with_note(match, note)
            enriched_meetings.append(enriched)
            matched_notes.append({
                'note': note['filename'],
                'meeting': match['title'],
                'score': score
            })
            print(f"   ✅ Matchet: {note['filename']} → {match['title']} (score: {score:.0f})")
        else:
            # No good match - create new meeting
            new_meeting = create_new_meeting_from_note(note)
            new_meetings.append(new_meeting)
            print(f"   ➕ Opprettet nytt møte: {note['title']}")

    # Update existing meetings in the list
    meetings_dict = {m['id']: m for m in meetings}
    for enriched in enriched_meetings:
        meetings_dict[enriched['id']] = enriched

    # Add new meetings
    for new_meeting in new_meetings:
        # Check for ID collision
        base_id = new_meeting['id']
        counter = 1
        while new_meeting['id'] in meetings_dict:
            new_meeting['id'] = f"{base_id}_{counter}"
            counter += 1

        meetings_dict[new_meeting['id']] = new_meeting

    # Update meetings list
    meetings_data['meetings'] = list(meetings_dict.values())

    # Update metadata
    meetings_data['metadata']['total_meetings'] = len(meetings_data['meetings'])
    meetings_data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    meetings_data['metadata']['last_enrichment'] = {
        'date': datetime.now().isoformat(),
        'meetings_enriched': len(enriched_meetings),
        'new_meetings_created': len(new_meetings),
        'high_confidence_matches': len(matched_notes),
        'script': 'apply-note-matches.py'
    }

    # Save updated meetings.json
    save_json(MEETINGS_JSON, meetings_data)

    print(f"\n✅ meetings.json oppdatert!")

    # Generate summary report
    summary = {
        'generated': datetime.now().isoformat(),
        'backup_file': str(backup_path),
        'statistics': {
            'total_meetings_before': len(meetings),
            'total_meetings_after': len(meetings_data['meetings']),
            'meetings_enriched': len(enriched_meetings),
            'new_meetings_created': len(new_meetings),
            'high_confidence_matches': len(matched_notes)
        },
        'matched_notes': matched_notes,
        'new_meetings': [m['id'] for m in new_meetings]
    }

    summary_path = BASE_DIR / "analysis" / "matching_applied_summary.json"
    save_json(summary_path, summary)

    print(f"✅ Sammendrag lagret til: {summary_path}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 SAMMENDRAG")
    print(f"{'='*60}")
    print(f"Møter før: {len(meetings)}")
    print(f"Møter etter: {len(meetings_data['meetings'])}")
    print(f"Møter beriket: {len(enriched_meetings)}")
    print(f"Nye møter opprettet: {len(new_meetings)}")
    print(f"High-confidence matcher: {len(matched_notes)}")

    print(f"\n{'='*60}")
    print(f"🎯 NESTE STEG")
    print(f"{'='*60}")
    print(f"1. Gjennomgå meetings.json for kvalitetssikring")
    print(f"2. Oppdater manglende deltakere og metadata")
    print(f"3. Verifiser at alle lenker til notater er korrekte")
    print(f"4. Fjern 'data_quality_note' når møter er verifisert")

if __name__ == '__main__':
    main()
