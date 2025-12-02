#!/usr/bin/env python3
"""
Improved Meeting Notes Parser
Extracts high-quality structured data from downloaded meeting notes
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETING_NOTES_DIR = Path("/Users/gabrielboen/Downloads/Møter hovfaret ")
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
OUTPUT_DIR = BASE_DIR / "analysis"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_date_from_filename(filename: str) -> Optional[str]:
    """Extract date from meeting note filename with better patterns"""
    # Remove .md extension
    filename = filename.replace('.md', '')

    # Norwegian month names
    norwegian_months = {
        'januar': '01', 'februar': '02', 'mars': '03', 'april': '04',
        'mai': '05', 'juni': '06', 'juli': '07', 'august': '08',
        'september': '09', 'oktober': '10', 'okt': '10', 'november': '11',
        'desember': '12', 'des': '12'
    }

    # Patterns to match different date formats
    patterns = [
        # "11 MARS 2024", "11 MARS   2024"
        (r'(\d{1,2})\s+(\w+)\s+(\d{4})', lambda m: (m.group(3), norwegian_months.get(m.group(2).lower(), m.group(2)), m.group(1))),
        # "03.06 2025", "03.06  2025"
        (r'(\d{1,2})\.(\d{1,2})\s+(\d{4})', lambda m: (m.group(3), m.group(2), m.group(1))),
        # "15 okt 2024"
        (r'(\d{1,2})\s+(\w+)\s+(\d{4})', lambda m: (m.group(3), norwegian_months.get(m.group(2).lower(), m.group(2)), m.group(1))),
        # "06 August 2025" (English month)
        (r'(\d{1,2})\s+(\w+)\s+(\d{4})', lambda m: (m.group(3), get_english_month(m.group(2)), m.group(1))),
        # "Januar 2025" (month year only - use first of month)
        (r'(\w+)\s+(\d{4})', lambda m: (m.group(2), norwegian_months.get(m.group(1).lower(), '01'), '01')),
    ]

    for pattern, extractor in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            try:
                year, month, day = extractor(match)
                # Convert month name to number if needed
                if not month.isdigit():
                    month = norwegian_months.get(month.lower(), '01')

                # Validate and format date
                date_obj = datetime.strptime(f"{year}-{month.zfill(2)}-{day.zfill(2)}", "%Y-%m-%d")
                return date_obj.strftime("%Y-%m-%d")
            except (ValueError, AttributeError):
                continue

    return None

def get_english_month(month_name: str) -> str:
    """Convert English month name to number"""
    months = {
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }
    return months.get(month_name.lower(), '01')

def extract_participants(content: str) -> List[str]:
    """Extract participant names from meeting notes"""
    participants = []

    # Look for participant sections
    patterns = [
        r'##?\s*Deltakere?:?\s*\n((?:[-*]\s*.+\n?)+)',
        r'##?\s*Tilstede:?\s*\n((?:[-*]\s*.+\n?)+)',
        r'##?\s*Participants?:?\s*\n((?:[-*]\s*.+\n?)+)',
        r'##?\s*Attendees?:?\s*\n((?:[-*]\s*.+\n?)+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            lines = match.group(1).strip().split('\n')
            for line in lines:
                # Remove bullet points and clean
                name = re.sub(r'^[-*]\s*', '', line.strip())
                # Remove email/organization in parentheses
                name = re.sub(r'\s*\([^)]+\)', '', name)
                # Remove titles
                name = re.sub(r',\s*\w+\s*$', '', name)
                if name:
                    participants.append(name.strip())

    # Also look for names in the first few lines
    if not participants:
        lines = content.split('\n')[:10]
        for line in lines:
            # Look for patterns like "Med: Name1, Name2"
            if re.match(r'Med:?|Tilstede:?|Deltakere:?', line, re.IGNORECASE):
                names = re.sub(r'^[^:]+:\s*', '', line)
                participants.extend([n.strip() for n in names.split(',') if n.strip()])

    return participants

def extract_action_items(content: str) -> List[str]:
    """Extract action items with improved detection"""
    action_items = []

    # Look for action items section
    patterns = [
        r'##?\s*(?:Action\s*items?|Handlingspunkter?|Oppfølgingspunkter?|To\s*do):?\s*\n((?:[-*]\s*.+\n?)+)',
        r'##?\s*(?:Neste\s*steg|Videre\s*arbeid):?\s*\n((?:[-*]\s*.+\n?)+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            lines = match.group(1).strip().split('\n')
            for line in lines:
                # Remove bullet points
                item = re.sub(r'^[-*]\s*', '', line.strip())
                if item and len(item) > 5:
                    action_items.append(item)

    # Look for numbered action items
    numbered_pattern = r'##?\s*(?:Action\s*items?|Handlingspunkter?):?\s*\n((?:\d+\.\s*.+\n?)+)'
    match = re.search(numbered_pattern, content, re.IGNORECASE | re.MULTILINE)
    if match:
        lines = match.group(1).strip().split('\n')
        for line in lines:
            item = re.sub(r'^\d+\.\s*', '', line.strip())
            if item and len(item) > 5:
                action_items.append(item)

    return action_items

def extract_topics(content: str) -> List[str]:
    """Extract discussion topics from headings and sections"""
    topics = []

    # Extract all headings (## Topic or ### Topic)
    heading_pattern = r'^##\s+(.+)$'
    headings = re.findall(heading_pattern, content, re.MULTILINE)

    # Filter out common meta-headings
    exclude_keywords = [
        'deltakere', 'participants', 'action items', 'handlingspunkter',
        'bakgrunn', 'background', 'møtereferat', 'meeting notes',
        'innledning', 'konklusjon', 'oppsummering', 'summary'
    ]

    for heading in headings:
        # Clean heading
        clean_heading = heading.strip()
        # Check if not a meta-heading
        if not any(keyword in clean_heading.lower() for keyword in exclude_keywords):
            if clean_heading and len(clean_heading) > 5:
                topics.append(clean_heading)

    return topics

def extract_decisions(content: str) -> List[str]:
    """Extract decisions from meeting notes"""
    decisions = []

    # Look for decision sections
    patterns = [
        r'##?\s*(?:Decisions?|Beslutninger?|Vedtak):?\s*\n((?:[-*]\s*.+\n?)+)',
        r'##?\s*(?:Konklusjoner?|Conclusions?):?\s*\n((?:[-*]\s*.+\n?)+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            lines = match.group(1).strip().split('\n')
            for line in lines:
                decision = re.sub(r'^[-*]\s*', '', line.strip())
                if decision and len(decision) > 5:
                    decisions.append(decision)

    # Look for decision keywords in text
    decision_keywords = [
        r'(?:Vi|Det\s+ble)\s+(?:besluttet|vedtatt|ble\s+enige\s+om)\s+(?:at\s+)?(.+?)(?:\.|$)',
        r'(?:Enighet\s+om|Beslutning:?)\s+(.+?)(?:\.|$)',
    ]

    for pattern in decision_keywords:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            decision = match.strip()
            if decision and len(decision) > 10 and decision not in decisions:
                decisions.append(decision)

    return decisions[:10]  # Limit to 10 decisions

def extract_location(content: str) -> Optional[str]:
    """Extract meeting location"""
    # Look for location patterns
    patterns = [
        r'(?:Sted|Location|Lokasjon):?\s*(.+?)(?:\n|$)',
        r'(?:Møtested):?\s*(.+?)(?:\n|$)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            if location and len(location) > 3:
                return location

    return None

def extract_meeting_title(content: str, filename: str) -> str:
    """Extract meeting title from content or filename"""
    # Try to get first heading
    heading_pattern = r'^#\s+(.+)$'
    match = re.search(heading_pattern, content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Remove common prefixes
        title = re.sub(r'^(?:MØTE|Meeting|MØTEREFERAT)[-:\s]*', '', title, flags=re.IGNORECASE)
        if title and len(title) > 5:
            return title

    # Fallback to filename
    title = filename.replace('.md', '')
    title = re.sub(r'^MØTE\s*', 'Møte ', title, flags=re.IGNORECASE)
    return title

def calculate_quality_score(parsed_data: Dict) -> Tuple[int, List[str], List[str]]:
    """Calculate quality score and identify issues"""
    score = 100
    issues = []
    warnings = []

    # Check content length
    word_count = len(parsed_data['content'].split())
    if word_count < 50:
        issues.append(f'Very short content ({word_count} words)')
        score -= 30
    elif word_count < 200:
        warnings.append(f'Short content ({word_count} words)')
        score -= 10

    # Check participants
    if not parsed_data['participants']:
        warnings.append('No participants identified')
        score -= 15

    # Check action items
    if not parsed_data['action_items']:
        warnings.append('No action items found')
        score -= 10

    # Check topics
    if not parsed_data['topics_discussed']:
        warnings.append('No topics extracted')
        score -= 10

    # Check decisions
    if not parsed_data['decisions']:
        warnings.append('No decisions found')
        score -= 10

    # Check date
    if not parsed_data['date']:
        issues.append('Could not extract date from filename')
        score -= 15

    return max(0, score), issues, warnings

def parse_meeting_note(filepath: Path) -> Dict:
    """Parse a single meeting note file with improved extraction"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = filepath.name

    # Extract all components
    parsed = {
        'filename': filename,
        'filepath': str(filepath),
        'date': extract_date_from_filename(filename),
        'title': extract_meeting_title(content, filename),
        'participants': extract_participants(content),
        'action_items': extract_action_items(content),
        'topics_discussed': extract_topics(content),
        'decisions': extract_decisions(content),
        'location': extract_location(content),
        'content': content,
        'word_count': len(content.split()),
    }

    # Calculate quality
    score, issues, warnings = calculate_quality_score(parsed)
    parsed['quality_score'] = score
    parsed['quality_issues'] = issues
    parsed['quality_warnings'] = warnings

    return parsed

def load_meetings():
    """Load meetings from meetings.json"""
    with open(MEETINGS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['meetings']

def match_note_to_meeting(note: Dict, meetings: List[Dict]) -> Optional[Dict]:
    """Match a meeting note to a meeting in meetings.json"""
    if not note['date']:
        return None

    # Find meetings with matching date
    for meeting in meetings:
        if meeting.get('date') == note['date']:
            return meeting

    return None

def identify_gaps(notes: List[Dict], meetings: List[Dict]) -> Dict:
    """Identify meetings without notes and notes without meetings"""
    notes_by_date = {n['date']: n for n in notes if n['date']}
    meetings_by_date = {m['date']: m for m in meetings if m.get('date')}

    # Meetings without notes
    meetings_without_notes = []
    for date, meeting in meetings_by_date.items():
        if date not in notes_by_date:
            meetings_without_notes.append({
                'date': date,
                'title': meeting['title'],
                'id': meeting['id'],
                'participant_count': meeting.get('participant_count', 0)
            })

    # Notes without meetings
    notes_without_meetings = []
    for date, note in notes_by_date.items():
        if date not in meetings_by_date:
            notes_without_meetings.append({
                'date': date,
                'title': note['title'],
                'filename': note['filename']
            })

    # Notes that don't match (no date extracted)
    notes_no_date = [n for n in notes if not n['date']]

    return {
        'meetings_without_notes': meetings_without_notes,
        'notes_without_meetings': notes_without_meetings,
        'notes_no_date': notes_no_date
    }

def generate_quality_report(notes: List[Dict], gaps: Dict) -> str:
    """Generate comprehensive quality and gap analysis report"""

    total_notes = len(notes)
    high_quality = len([n for n in notes if n['quality_score'] >= 80])
    medium_quality = len([n for n in notes if 60 <= n['quality_score'] < 80])
    low_quality = len([n for n in notes if n['quality_score'] < 60])
    avg_score = sum(n['quality_score'] for n in notes) / total_notes if notes else 0

    report = f"""# MØTENOTATER KVALITETSANALYSE
## Hovfaret 13 Prosjekt

**Generert:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 OVERSIKT

### Møtenotater funnet:
- **Totalt:** {total_notes} filer
- **Gjennomsnittlig kvalitet:** {avg_score:.1f}/100
- **Høy kvalitet (≥80):** {high_quality} notater
- **Medium kvalitet (60-79):** {medium_quality} notater
- **Lav kvalitet (<60):** {low_quality} notater

### Gap-analyse:
- **Møter uten notater:** {len(gaps['meetings_without_notes'])}
- **Notater uten møte-match:** {len(gaps['notes_without_meetings'])}
- **Notater uten dato:** {len(gaps['notes_no_date'])}

---

## ✅ HØY KVALITET ({high_quality} notater)

Notater med score ≥ 80:

"""

    # High quality notes
    high_quality_notes = sorted(
        [n for n in notes if n['quality_score'] >= 80],
        key=lambda x: x['quality_score'],
        reverse=True
    )

    for note in high_quality_notes:
        report += f"""
### {note['date'] or 'Ukjent dato'} - {note['title']}

- **Fil:** {note['filename']}
- **Kvalitetsscore:** {note['quality_score']}/100
- **Ordtelling:** {note['word_count']} ord
- **Deltakere:** {len(note['participants'])}
- **Action items:** {len(note['action_items'])}
- **Topics:** {len(note['topics_discussed'])}
- **Decisions:** {len(note['decisions'])}
"""
        if note['quality_warnings']:
            report += f"- **Advarsler:** {', '.join(note['quality_warnings'])}\n"

    # Medium quality notes
    if medium_quality > 0:
        report += f"""

---

## ⚠️ MEDIUM KVALITET ({medium_quality} notater)

Notater med score 60-79:

"""
        medium_quality_notes = sorted(
            [n for n in notes if 60 <= n['quality_score'] < 80],
            key=lambda x: x['quality_score'],
            reverse=True
        )

        for note in medium_quality_notes:
            report += f"""
### {note['date'] or 'Ukjent dato'} - {note['title']}

- **Fil:** {note['filename']}
- **Kvalitetsscore:** {note['quality_score']}/100
- **Ordtelling:** {note['word_count']} ord
- **Action items:** {len(note['action_items'])}
- **Topics:** {len(note['topics_discussed'])}
- **Decisions:** {len(note['decisions'])}
"""
            if note['quality_issues']:
                report += f"- **🚨 Issues:** {', '.join(note['quality_issues'])}\n"
            if note['quality_warnings']:
                report += f"- **⚠️ Advarsler:** {', '.join(note['quality_warnings'])}\n"

    # Low quality notes
    if low_quality > 0:
        report += f"""

---

## 🔴 LAV KVALITET ({low_quality} notater)

Notater med score < 60 - trenger forbedring:

"""
        low_quality_notes = sorted(
            [n for n in notes if n['quality_score'] < 60],
            key=lambda x: x['quality_score']
        )

        for note in low_quality_notes:
            report += f"""
### {note['date'] or 'Ukjent dato'} - {note['title']}

- **Fil:** {note['filename']}
- **Kvalitetsscore:** {note['quality_score']}/100
- **Ordtelling:** {note['word_count']} ord
"""
            if note['quality_issues']:
                report += f"- **🚨 Kritiske issues:** {', '.join(note['quality_issues'])}\n"
            if note['quality_warnings']:
                report += f"- **⚠️ Advarsler:** {', '.join(note['quality_warnings'])}\n"

    # Gap analysis
    report += f"""

---

## 🔍 GAP-ANALYSE

### Møter uten notater ({len(gaps['meetings_without_notes'])})

Disse møtene i meetings.json mangler notater:

"""

    for meeting in sorted(gaps['meetings_without_notes'], key=lambda x: x['date']):
        report += f"""
- **{meeting['date']}** - {meeting['title']}
  - Meeting ID: `{meeting['id']}`
  - Deltakere: {meeting['participant_count']}
"""

    if gaps['notes_without_meetings']:
        report += f"""

### Notater uten møte-match ({len(gaps['notes_without_meetings'])})

Disse notatene har ikke matchende møte i meetings.json:

"""
        for note in sorted(gaps['notes_without_meetings'], key=lambda x: x['date']):
            report += f"""
- **{note['date']}** - {note['title']}
  - Fil: {note['filename']}
  - **Handling:** Opprett nytt møte i meetings.json
"""

    if gaps['notes_no_date']:
        report += f"""

### Notater uten dato ({len(gaps['notes_no_date'])})

Disse notatene mangler dato i filnavnet:

"""
        for note in gaps['notes_no_date']:
            report += f"""
- **{note['title']}**
  - Fil: {note['filename']}
  - **Handling:** Rename fil med dato eller manuell matching
"""

    # Recommendations
    report += f"""

---

## 🎯 ANBEFALTE HANDLINGER

### Prioritet 1: Forbedre lavkvalitets-notater
1. Gjennomgå de {low_quality} notatene med lav kvalitet
2. Utfyll manglende action items, topics og decisions
3. Legg til deltakerliste hvis mulig
4. Sørg for at hvert notat har minst 200 ord

### Prioritet 2: Fylle gap
5. Finn eller opprett notater for de {len(gaps['meetings_without_notes'])} møtene uten dokumentasjon
6. Opprett møter i meetings.json for de {len(gaps['notes_without_meetings'])} notatene uten match
7. Rename {len(gaps['notes_no_date'])} filer uten dato

### Prioritet 3: Kvalitetssikring
8. Re-parse alle notater med forbedret skript
9. Manuell gjennomgang av viktige møter
10. Valider at all informasjon er korrekt

### Neste steg:
- Bruk dette skriptet til å oppdatere meetings.json med forbedret data
- Lag backup før oppdatering
- Generer ny kvalitetsrapport etter forbedringer

**Dekningsgrad:** {total_notes - len(gaps['notes_no_date'])}/{total_notes} notater har dato og kan matches
"""

    return report

def main():
    """Main execution function"""
    print("🔍 Parser møtenotater med forbedret kvalitet...")

    # Check if directory exists
    if not MEETING_NOTES_DIR.exists():
        print(f"❌ Finner ikke mappen: {MEETING_NOTES_DIR}")
        return

    # Parse all meeting notes
    notes = []
    note_files = list(MEETING_NOTES_DIR.glob("*.md"))

    print(f"   Fant {len(note_files)} møtenotat-filer")

    for filepath in note_files:
        try:
            note = parse_meeting_note(filepath)
            notes.append(note)
            score_emoji = "✅" if note['quality_score'] >= 80 else "⚠️" if note['quality_score'] >= 60 else "🔴"
            print(f"   {score_emoji} {filepath.name} - Score: {note['quality_score']}/100")
        except Exception as e:
            print(f"   ❌ Error parsing {filepath.name}: {e}")

    # Load meetings
    meetings = load_meetings()
    print(f"\n   Lastet {len(meetings)} møter fra meetings.json")

    # Identify gaps
    gaps = identify_gaps(notes, meetings)

    print(f"\n   📊 Gap-analyse:")
    print(f"      Møter uten notater: {len(gaps['meetings_without_notes'])}")
    print(f"      Notater uten match: {len(gaps['notes_without_meetings'])}")
    print(f"      Notater uten dato: {len(gaps['notes_no_date'])}")

    # Generate quality report
    quality_report = generate_quality_report(notes, gaps)

    # Save reports
    quality_output = OUTPUT_DIR / "meeting_notes_quality_analysis.md"
    with open(quality_output, 'w', encoding='utf-8') as f:
        f.write(quality_report)

    print(f"\n✅ Kvalitetsrapport lagret til: {quality_output}")

    # Save JSON data
    json_output = OUTPUT_DIR / "meeting_notes_parsed.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_notes': len(notes),
                'average_quality': sum(n['quality_score'] for n in notes) / len(notes) if notes else 0,
                'high_quality': len([n for n in notes if n['quality_score'] >= 80]),
                'medium_quality': len([n for n in notes if 60 <= n['quality_score'] < 80]),
                'low_quality': len([n for n in notes if n['quality_score'] < 60]),
            },
            'notes': notes,
            'gaps': gaps
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON-data lagret til: {json_output}")

    # Print summary
    avg_score = sum(n['quality_score'] for n in notes) / len(notes) if notes else 0
    print(f"\n{'='*60}")
    print(f"📊 SAMMENDRAG")
    print(f"{'='*60}")
    print(f"Notater parsed: {len(notes)}")
    print(f"Gjennomsnittlig kvalitet: {avg_score:.1f}/100")
    print(f"Høy kvalitet (≥80): {len([n for n in notes if n['quality_score'] >= 80])}")
    print(f"Medium kvalitet (60-79): {len([n for n in notes if 60 <= n['quality_score'] < 80])}")
    print(f"Lav kvalitet (<60): {len([n for n in notes if n['quality_score'] < 60])}")
    print(f"\nMøter uten notater: {len(gaps['meetings_without_notes'])}")

if __name__ == '__main__':
    main()
