#!/usr/bin/env python3
"""
Meeting Reports Analysis and Matching Script
Analyzes all meeting reports and matches them to meetings in meetings.json
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Paths
BASE_DIR = Path(__file__).parent.parent
EXTRACTION_CACHE = BASE_DIR / "source" / "extraction-cache"
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
OUTPUT_DIR = BASE_DIR / "analysis"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

def load_meetings():
    """Load meetings from meetings.json"""
    with open(MEETINGS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['meetings']

def extract_date_from_filename(filename: str) -> Optional[str]:
    """Extract date from meeting report filename"""
    # Patterns to match different date formats
    patterns = [
        r'(\d{1,2})\s+(\w+)\s+(\d{4})',  # "11 MARS 2024"
        r'(\d{1,2})\.(\d{1,2})\.(\d{2,4})',  # "03.06.2026" or "24.06"
        r'(\d{1,2})\s+(\w+)\s+(\d{2})',  # "15 okt 24"
        r'(\d{4})-(\d{2})-(\d{2})',  # "2024-03-11"
    ]

    # Norwegian month names
    norwegian_months = {
        'januar': '01', 'februar': '02', 'mars': '03', 'april': '04',
        'mai': '05', 'juni': '06', 'juli': '07', 'august': '08',
        'september': '09', 'oktober': '10', 'okt': '10', 'november': '11',
        'desember': '12'
    }

    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            if len(match.groups()) == 3:
                day, month, year = match.groups()

                # Convert month name to number if needed
                if month.lower() in norwegian_months:
                    month = norwegian_months[month.lower()]

                # Normalize year
                if len(year) == 2:
                    year = '20' + year

                try:
                    # Validate and format date
                    date_obj = datetime.strptime(f"{year}-{month.zfill(2)}-{day.zfill(2)}", "%Y-%m-%d")
                    return date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    continue

    return None

def analyze_meeting_report(filepath: Path) -> Dict:
    """Analyze a single meeting report extraction file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract date from filename or content
    filename = data.get('file_name', filepath.name)
    extracted_date = extract_date_from_filename(filename)

    # Get meeting-specific info
    meeting_info = data.get('meeting_info', {})

    # Extract key fields
    result = {
        'filename': filename,
        'extraction_file': filepath.name,
        'date': extracted_date or data.get('meeting_date'),
        'full_text': data.get('full_text', ''),
        'document_type': data.get('document_type'),
        'entities': data.get('entities', {}),
        'action_items': meeting_info.get('action_items', []),
        'topics_discussed': meeting_info.get('topics_discussed', []),
        'decisions': meeting_info.get('decisions', []),
        'word_count': len(data.get('full_text', '').split())
    }

    return result

def find_meeting_reports():
    """Find all meeting report extraction files"""
    meeting_reports = []

    for filepath in EXTRACTION_CACHE.glob("*.json"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check if it's a meeting report
            filename = data.get('file_name', '').lower()
            doc_type = data.get('document_type', '')

            is_meeting_report = (
                doc_type == 'meeting_report' or
                'møte' in filename or
                'referat' in filename or
                'meeting' in filename.lower()
            )

            if is_meeting_report:
                report = analyze_meeting_report(filepath)
                meeting_reports.append(report)

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading {filepath.name}: {e}")
            continue

    return meeting_reports

def match_reports_to_meetings(reports: List[Dict], meetings: List[Dict]):
    """Match meeting reports to meetings by date and content"""
    matched = []
    unmatched_reports = []
    meetings_without_reports = []

    # Create date index for meetings
    meetings_by_date = {}
    for meeting in meetings:
        date = meeting.get('date')
        if date:
            if date not in meetings_by_date:
                meetings_by_date[date] = []
            meetings_by_date[date].append(meeting)

    # Match reports to meetings
    for report in reports:
        report_date = report['date']

        if report_date and report_date in meetings_by_date:
            # Found matching meeting(s)
            for meeting in meetings_by_date[report_date]:
                matched.append({
                    'meeting_id': meeting['id'],
                    'meeting_title': meeting['title'],
                    'date': report_date,
                    'report': report,
                    'match_confidence': 'high'
                })
        else:
            # No exact date match - try fuzzy matching by title
            unmatched_reports.append(report)

    # Find meetings without reports
    matched_meeting_ids = {m['meeting_id'] for m in matched}
    for meeting in meetings:
        if meeting['id'] not in matched_meeting_ids:
            meetings_without_reports.append({
                'meeting_id': meeting['id'],
                'meeting_title': meeting['title'],
                'date': meeting.get('date'),
                'organizer': meeting.get('organizer'),
                'participant_count': meeting.get('participant_count', 0)
            })

    return matched, unmatched_reports, meetings_without_reports

def generate_coverage_report(matched, unmatched_reports, meetings_without_reports, total_meetings):
    """Generate a comprehensive coverage report"""
    report = f"""
# MØTEREFERAT DEKNINGSRAPPORT
## Hovfaret 13 Prosjekt

**Generert:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 OVERSIKT

- **Totalt antall møter:** {total_meetings}
- **Møter med referat:** {len(matched)}
- **Møter uten referat:** {len(meetings_without_reports)}
- **Dekningsgrad:** {len(matched)/total_meetings*100:.1f}%

- **Referater funnet:** {len(matched) + len(unmatched_reports)}
- **Referater matchet til møter:** {len(matched)}
- **Referater uten match:** {len(unmatched_reports)}

---

## ✅ MØTER MED REFERAT ({len(matched)})

"""

    # Sort matched by date
    matched_sorted = sorted(matched, key=lambda x: x['date'] or '')

    for m in matched_sorted:
        report += f"""
### {m['date'] or 'Ukjent dato'} - {m['meeting_title']}

- **Meeting ID:** `{m['meeting_id']}`
- **Referat fil:** {m['report']['filename']}
- **Ordtelling:** {m['report']['word_count']} ord
- **Action items:** {len(m['report'].get('action_items', []))}
- **Match kvalitet:** {m['match_confidence']}
"""

    report += f"""

---

## ❌ MØTER UTEN REFERAT ({len(meetings_without_reports)})

"""

    # Sort meetings without reports by date
    missing_sorted = sorted(meetings_without_reports, key=lambda x: x['date'] or '')

    for m in missing_sorted:
        report += f"""
### {m['date'] or 'Ukjent dato'} - {m['meeting_title']}

- **Meeting ID:** `{m['meeting_id']}`
- **Organisert av:** {m['organizer'] or 'Ukjent'}
- **Deltakere:** {m['participant_count']}
"""

    if unmatched_reports:
        report += f"""

---

## ⚠️ REFERATER UTEN MØTE-MATCH ({len(unmatched_reports)})

Disse referatene ble funnet, men kunne ikke matches til et eksisterende møte:

"""

        for r in unmatched_reports:
            report += f"""
### {r['filename']}

- **Dato (ekstrahert):** {r['date'] or 'Kunne ikke ekstraheres'}
- **Ordtelling:** {r['word_count']} ord
- **Foreslått handling:** Opprett nytt møte i meetings.json eller match manuelt
"""

    report += """

---

## 🎯 ANBEFALTE HANDLINGER

### Høy prioritet:
1. Gjennomgå de {count_high} møtene uten referat og sjekk om det finnes dokumentasjon
2. Match de {count_unmatched} umatchede referatene manuelt
3. Kvalitetssikre eksisterende match

### Middels prioritet:
4. Ekstraher topics_discussed fra alle referater med ordtelling > 100
5. Legg til action_items i møter hvor det er relevant

### Lav prioritet:
6. Opprett møter for referater uten match (hvis de er reelle møter)
7. Forbedre automatisk dato-ekstraksjon

""".format(
        count_high=len(meetings_without_reports),
        count_unmatched=len(unmatched_reports)
    )

    return report

def main():
    """Main execution function"""
    print("🔍 Analyserer møtereferater...")

    # Load meetings
    meetings = load_meetings()
    total_meetings = len(meetings)
    print(f"   Lastet {total_meetings} møter fra meetings.json")

    # Find all meeting reports
    reports = find_meeting_reports()
    print(f"   Fant {len(reports)} møtereferater i extraction cache")

    # Match reports to meetings
    matched, unmatched_reports, meetings_without_reports = match_reports_to_meetings(reports, meetings)
    print(f"   ✅ Matchet {len(matched)} referater til møter")
    print(f"   ⚠️  {len(unmatched_reports)} referater uten match")
    print(f"   ❌ {len(meetings_without_reports)} møter uten referat")

    # Generate coverage report
    coverage_report = generate_coverage_report(
        matched,
        unmatched_reports,
        meetings_without_reports,
        total_meetings
    )

    # Save reports
    output_file = OUTPUT_DIR / "meeting_reports_coverage.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(coverage_report)

    print(f"\n✅ Rapport lagret til: {output_file}")

    # Save detailed JSON data
    json_output = {
        'generated': datetime.now().isoformat(),
        'summary': {
            'total_meetings': total_meetings,
            'meetings_with_reports': len(matched),
            'meetings_without_reports': len(meetings_without_reports),
            'coverage_percentage': len(matched)/total_meetings*100,
            'unmatched_reports': len(unmatched_reports)
        },
        'matched': matched,
        'unmatched_reports': unmatched_reports,
        'meetings_without_reports': meetings_without_reports
    }

    json_file = OUTPUT_DIR / "meeting_reports_analysis.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)

    print(f"✅ Detaljert analyse lagret til: {json_file}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 SAMMENDRAG")
    print(f"{'='*60}")
    print(f"Dekningsgrad: {len(matched)}/{total_meetings} ({len(matched)/total_meetings*100:.1f}%)")
    print(f"Manglende referater: {len(meetings_without_reports)}")
    print(f"Umatchede referater: {len(unmatched_reports)}")

if __name__ == '__main__':
    main()
