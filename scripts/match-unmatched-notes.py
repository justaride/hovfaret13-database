#!/usr/bin/env python3
"""
Match Unmatched Notes Script
Analyzes unmatched notes and either matches them to existing meetings
or creates new meeting entries for them
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
PARSED_JSON = BASE_DIR / "analysis" / "meeting_notes_parsed.json"
OUTPUT_DIR = BASE_DIR / "analysis"

def load_meetings():
    """Load meetings from meetings.json"""
    with open(MEETINGS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_parsed_notes():
    """Load parsed meeting notes"""
    with open(PARSED_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_potential_matches(note: Dict, meetings: List[Dict]) -> List[Tuple[Dict, float, str]]:
    """Find potential meeting matches for a note based on various criteria"""
    matches = []

    note_title = note['title'].lower()
    note_content = note['content'].lower()
    note_participants = [p.lower() for p in note.get('participants', [])]

    for meeting in meetings:
        score = 0.0
        reasons = []

        # Check title similarity
        meeting_title = meeting['title'].lower()
        if note_title in meeting_title or meeting_title in note_title:
            score += 30
            reasons.append('Title match')

        # Check for common words in title
        note_words = set(re.findall(r'\w+', note_title))
        meeting_words = set(re.findall(r'\w+', meeting_title))
        common_words = note_words.intersection(meeting_words)
        if len(common_words) >= 2:
            score += 10 * len(common_words)
            reasons.append(f'{len(common_words)} common title words')

        # Check participant overlap
        meeting_participants = [p['name'].lower() for p in meeting.get('participants', []) if isinstance(p, dict)]
        participant_overlap = set(note_participants).intersection(set(meeting_participants))
        if participant_overlap:
            score += 20 * len(participant_overlap)
            reasons.append(f'{len(participant_overlap)} matching participants')

        # Check for date proximity (if note has estimated date)
        if note.get('date') and meeting.get('date'):
            try:
                note_date = datetime.strptime(note['date'], '%Y-%m-%d')
                meeting_date = datetime.strptime(meeting['date'], '%Y-%m-%d')
                days_diff = abs((note_date - meeting_date).days)
                if days_diff == 0:
                    score += 50
                    reasons.append('Exact date match')
                elif days_diff <= 7:
                    score += 20
                    reasons.append(f'{days_diff} days apart')
            except:
                pass

        # Check for keywords in content
        keywords = ['hovfaret', 'omsorg', 'leietaker', 'energi', 'nabolag']
        for keyword in keywords:
            if keyword in note_content and keyword in meeting_title:
                score += 5
                reasons.append(f'Keyword: {keyword}')

        if score > 0:
            matches.append((meeting, score, ', '.join(reasons)))

    # Sort by score (highest first)
    matches.sort(key=lambda x: x[1], reverse=True)

    return matches[:5]  # Return top 5 matches

def extract_date_from_content(content: str) -> Optional[str]:
    """Try to extract date from note content"""
    # Look for date patterns in content
    patterns = [
        r'dato:?\s*(\d{1,2})[.\s]+(\w+)[.\s]+(\d{4})',
        r'(\d{1,2})[.\s]+(\w+)[.\s]+(\d{4})',
    ]

    norwegian_months = {
        'januar': '01', 'februar': '02', 'mars': '03', 'april': '04',
        'mai': '05', 'juni': '06', 'juli': '07', 'august': '08',
        'september': '09', 'oktober': '10', 'november': '11', 'desember': '12'
    }

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            try:
                day, month, year = match.groups()
                month_num = norwegian_months.get(month.lower(), month)
                if month_num.isdigit():
                    date_obj = datetime.strptime(f"{year}-{month_num.zfill(2)}-{day.zfill(2)}", "%Y-%m-%d")
                    return date_obj.strftime("%Y-%m-%d")
            except:
                continue

    return None

def suggest_new_meeting(note: Dict) -> Dict:
    """Suggest a new meeting entry for a note"""
    # Try to extract date from content if not in filename
    date = note.get('date')
    if not date:
        date = extract_date_from_content(note['content'])

    # Generate meeting ID
    if date:
        date_part = date.replace('-', '_')
    else:
        date_part = 'unknown_date'

    # Clean title for ID
    title_clean = re.sub(r'[^a-zA-Z0-9\s]', '', note['title'].lower())
    title_part = '_'.join(title_clean.split()[:5])

    meeting_id = f"m_{date_part}_{title_part}"

    # Suggest meeting structure
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
        'report_link': f"data/restructured_notes/{note.get('date', 'UKJENT_DATO')}_{note['filename']}",
        'report_metadata': {
            'word_count': note['word_count'],
            'source': 'Downloaded meeting notes',
            'needs_review': True
        }
    }

    return new_meeting

def generate_matching_report(unmatched_notes: List[Dict], meetings: List[Dict]) -> str:
    """Generate report with matching suggestions"""

    report = f"""# NOTAT-MATCHING ANALYSE
## Hovfaret 13 Prosjekt

**Generert:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 OVERSIKT

- **Umatchede notater:** {len(unmatched_notes)}
- **Totalt møter i database:** {len(meetings)}

---

## 🔍 MATCHING FORSLAG

"""

    new_meetings_suggested = []

    for note in unmatched_notes:
        report += f"""
### {note['filename']}

**Tittel:** {note['title']}
**Dato (fra filnavn):** {note.get('date', 'Ukjent')}
**Ordtelling:** {note['word_count']} ord

"""

        # Find potential matches
        matches = find_potential_matches(note, meetings)

        if matches:
            report += "**Mulige matcher:**\n\n"
            for meeting, score, reasons in matches:
                report += f"- **{meeting['title']}** (Score: {score:.0f})\n"
                report += f"  - Dato: {meeting.get('date', 'Ukjent')}\n"
                report += f"  - Grunner: {reasons}\n"
                report += f"  - Meeting ID: `{meeting['id']}`\n\n"
        else:
            report += "**Ingen gode matcher funnet.**\n\n"

        # Suggest new meeting
        new_meeting = suggest_new_meeting(note)
        new_meetings_suggested.append(new_meeting)

        report += "**Forslag: Opprett nytt møte**\n\n"
        report += f"```json\n{json.dumps(new_meeting, indent=2, ensure_ascii=False)}\n```\n\n"
        report += "---\n"

    # Summary section
    report += f"""

## 🎯 ANBEFALINGER

### Steg 1: Gjennomgå matcher
- Gå gjennom hver forslag ovenfor
- For notater med gode matcher (score > 30):
  - Verifiser at det er riktig møte
  - Oppdater notatets filnavn med riktig dato
  - Kjør omstrukturering på nytt

### Steg 2: Opprett nye møter
- For notater uten gode matcher:
  - Bruk det foreslåtte møte-objektet
  - Juster dato, deltakere, og metadata etter behov
  - Legg til i meetings.json

### Steg 3: Manuell review
- **{len([n for n in new_meetings_suggested if not n['date']])} notater mangler dato** - må undersøkes manuelt
- **{len([n for n in new_meetings_suggested if not n['participants']])} notater mangler deltakere** - kan fylles ut fra møteinnkallinger

---

## 📂 NYE MØTER (JSON)

Total foreslåtte nye møter: {len(new_meetings_suggested)}

**Lagret til:** `analysis/suggested_new_meetings.json`

For å legge til alle foreslåtte møter i meetings.json:
1. Gjennomgå suggested_new_meetings.json
2. Juster datoer og deltakere etter behov
3. Kopier inn i meetings.json under "meetings" array
4. Oppdater "total_meetings" i metadata
"""

    return report, new_meetings_suggested

def main():
    """Main execution function"""
    print("🔍 Analyserer umatchede notater...")

    # Load data
    meetings_data = load_meetings()
    meetings = meetings_data['meetings']
    notes_data = load_parsed_notes()
    all_notes = notes_data['notes']

    print(f"   Lastet {len(meetings)} møter")
    print(f"   Lastet {len(all_notes)} notater")

    # Find unmatched notes (notes without a date match in meetings)
    meetings_by_date = {m['date']: m for m in meetings if m.get('date')}

    unmatched_notes = []
    for note in all_notes:
        if not note.get('date') or note['date'] not in meetings_by_date:
            unmatched_notes.append(note)

    print(f"   Fant {len(unmatched_notes)} umatchede notater")

    # Generate matching report
    report, new_meetings = generate_matching_report(unmatched_notes, meetings)

    # Save report
    report_path = OUTPUT_DIR / "note_matching_analysis.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Matching-rapport lagret til: {report_path}")

    # Save suggested new meetings
    new_meetings_path = OUTPUT_DIR / "suggested_new_meetings.json"
    with open(new_meetings_path, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'count': len(new_meetings),
            'meetings': new_meetings
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ Foreslåtte nye møter lagret til: {new_meetings_path}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 SAMMENDRAG")
    print(f"{'='*60}")
    print(f"Umatchede notater analysert: {len(unmatched_notes)}")
    print(f"Nye møter foreslått: {len(new_meetings)}")

    # Count notes with potential matches
    notes_with_matches = 0
    for note in unmatched_notes:
        matches = find_potential_matches(note, meetings)
        if matches and matches[0][1] > 30:  # Good match threshold
            notes_with_matches += 1

    print(f"Notater med gode matcher: {notes_with_matches}")
    print(f"Notater som trenger nye møter: {len(new_meetings) - notes_with_matches}")

if __name__ == '__main__':
    main()
