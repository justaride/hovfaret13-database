#!/usr/bin/env python3
"""
Meeting Enrichment Script
Extracts structured data from meeting reports and adds to meetings.json
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Paths
BASE_DIR = Path(__file__).parent.parent
EXTRACTION_CACHE = BASE_DIR / "source" / "extraction-cache"
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
ANALYSIS_JSON = BASE_DIR / "analysis" / "meeting_reports_analysis.json"
OUTPUT_DIR = BASE_DIR / "analysis"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

def load_meetings():
    """Load meetings from meetings.json"""
    with open(MEETINGS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_analysis():
    """Load meeting reports analysis"""
    with open(ANALYSIS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_extraction_file(filename: str) -> Optional[Dict]:
    """Load a specific extraction file"""
    filepath = EXTRACTION_CACHE / filename
    if not filepath.exists():
        return None

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def extract_enrichment_data(extraction_data: Dict) -> Dict:
    """Extract relevant enrichment data from extraction file"""
    meeting_info = extraction_data.get('meeting_info', {})

    # Get action items
    action_items = meeting_info.get('action_items', [])

    # Get topics discussed
    topics_discussed = meeting_info.get('topics_discussed', [])

    # Get decisions
    decisions = meeting_info.get('decisions', [])

    # Get entities for additional context
    entities = extraction_data.get('entities', {})
    people_mentioned = entities.get('people', [])
    orgs_mentioned = entities.get('organizations', [])

    # Get source file path for report_link
    source_file = extraction_data.get('source_file', '')
    file_name = extraction_data.get('file_name', '')

    # Calculate content quality metrics
    full_text = extraction_data.get('full_text', '')
    word_count = len(full_text.split())

    return {
        'action_items': action_items,
        'topics_discussed': topics_discussed,
        'decisions': decisions,
        'report_link': source_file or file_name,
        'report_metadata': {
            'word_count': word_count,
            'people_mentioned': people_mentioned,
            'organizations_mentioned': orgs_mentioned,
            'extraction_date': extraction_data.get('extraction_date', '')
        }
    }

def quality_check_enrichment(enrichment: Dict, meeting: Dict) -> Dict:
    """Quality check the enrichment data and return QA report"""
    issues = []
    warnings = []
    quality_score = 100

    # Check if action items exist
    if not enrichment['action_items']:
        warnings.append('No action items found')
        quality_score -= 10

    # Check if topics discussed exist
    if not enrichment['topics_discussed']:
        warnings.append('No topics discussed found')
        quality_score -= 15

    # Check if decisions exist
    if not enrichment['decisions']:
        warnings.append('No decisions found')
        quality_score -= 10

    # Check word count
    word_count = enrichment['report_metadata']['word_count']
    if word_count < 100:
        issues.append(f'Very short report ({word_count} words)')
        quality_score -= 20
    elif word_count < 300:
        warnings.append(f'Short report ({word_count} words)')
        quality_score -= 10

    # Check if report_link is valid
    if not enrichment['report_link']:
        issues.append('No report link available')
        quality_score -= 15

    # Check for participant alignment
    # participants is an array of objects with 'name' field
    people_in_meeting = set(p['name'].lower() for p in meeting.get('participants', []) if isinstance(p, dict) and 'name' in p)
    people_in_report = set(p.lower() for p in enrichment['report_metadata']['people_mentioned'])

    # If there's significant mismatch, flag it
    if people_in_meeting and people_in_report:
        overlap = people_in_meeting.intersection(people_in_report)
        if len(overlap) == 0:
            warnings.append('No participant overlap between meeting and report')

    return {
        'quality_score': max(0, quality_score),
        'issues': issues,
        'warnings': warnings,
        'status': 'approved' if quality_score >= 70 and len(issues) == 0 else 'needs_review'
    }

def enrich_meetings(meetings_data: Dict, analysis_data: Dict) -> tuple:
    """Enrich meetings with report data"""
    enriched_count = 0
    qa_reports = []

    # Create lookup for meetings by ID
    meetings_by_id = {m['id']: m for m in meetings_data['meetings']}

    # Process matched reports
    matched_reports = analysis_data.get('matched', [])

    for match in matched_reports:
        meeting_id = match['meeting_id']
        report_info = match['report']
        extraction_file = report_info['extraction_file']

        # Load extraction file
        extraction_data = load_extraction_file(extraction_file)
        if not extraction_data:
            print(f"   ⚠️  Could not load extraction file: {extraction_file}")
            continue

        # Extract enrichment data
        enrichment = extract_enrichment_data(extraction_data)

        # Get the meeting
        if meeting_id not in meetings_by_id:
            print(f"   ⚠️  Meeting ID not found: {meeting_id}")
            continue

        meeting = meetings_by_id[meeting_id]

        # Quality check
        qa_result = quality_check_enrichment(enrichment, meeting)

        # Add enrichment data to meeting
        meeting['action_items'] = enrichment['action_items']
        meeting['topics_discussed'] = enrichment['topics_discussed']
        meeting['decisions'] = enrichment['decisions']
        meeting['report_link'] = enrichment['report_link']
        meeting['report_metadata'] = enrichment['report_metadata']

        enriched_count += 1

        # Record QA report
        qa_reports.append({
            'meeting_id': meeting_id,
            'meeting_title': meeting['title'],
            'date': meeting.get('date'),
            'enrichment': {
                'action_items_count': len(enrichment['action_items']),
                'topics_count': len(enrichment['topics_discussed']),
                'decisions_count': len(enrichment['decisions']),
                'word_count': enrichment['report_metadata']['word_count']
            },
            'quality_check': qa_result
        })

    # Update metadata
    meetings_data['metadata']['last_enrichment'] = {
        'date': datetime.now().isoformat(),
        'meetings_enriched': enriched_count,
        'script': 'enrich-meetings-with-reports.py'
    }

    return meetings_data, qa_reports

def generate_qa_report(qa_reports: List[Dict], total_enriched: int) -> str:
    """Generate quality assurance report"""

    # Categorize by quality
    approved = [r for r in qa_reports if r['quality_check']['status'] == 'approved']
    needs_review = [r for r in qa_reports if r['quality_check']['status'] == 'needs_review']

    # Calculate average quality score
    avg_score = sum(r['quality_check']['quality_score'] for r in qa_reports) / len(qa_reports) if qa_reports else 0

    report = f"""# MØTE-BERIKNING KVALITETSRAPPORT
## Hovfaret 13 Prosjekt

**Generert:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 OVERSIKT

- **Møter beriket:** {total_enriched}
- **Gjennomsnittlig kvalitet:** {avg_score:.1f}/100
- **Godkjent:** {len(approved)} møter
- **Trenger gjennomgang:** {len(needs_review)} møter

---

## ✅ GODKJENTE MØTER ({len(approved)})

Møter med kvalitetsscore ≥ 70 og ingen kritiske feil:

"""

    # Sort by quality score (best first)
    approved_sorted = sorted(approved, key=lambda x: x['quality_check']['quality_score'], reverse=True)

    for qa in approved_sorted:
        report += f"""
### {qa['date'] or 'Ukjent dato'} - {qa['meeting_title']}

- **Meeting ID:** `{qa['meeting_id']}`
- **Kvalitetsscore:** {qa['quality_check']['quality_score']}/100
- **Action items:** {qa['enrichment']['action_items_count']}
- **Topics discussed:** {qa['enrichment']['topics_count']}
- **Decisions:** {qa['enrichment']['decisions_count']}
- **Ordtelling:** {qa['enrichment']['word_count']} ord
"""

        if qa['quality_check']['warnings']:
            report += f"- **Advarsler:** {', '.join(qa['quality_check']['warnings'])}\n"

    if needs_review:
        report += f"""

---

## ⚠️ MØTER SOM TRENGER GJENNOMGANG ({len(needs_review)})

Møter med kvalitetsscore < 70 eller kritiske feil:

"""

        # Sort by quality score (worst first)
        review_sorted = sorted(needs_review, key=lambda x: x['quality_check']['quality_score'])

        for qa in review_sorted:
            report += f"""
### {qa['date'] or 'Ukjent dato'} - {qa['meeting_title']}

- **Meeting ID:** `{qa['meeting_id']}`
- **Kvalitetsscore:** {qa['quality_check']['quality_score']}/100
- **Action items:** {qa['enrichment']['action_items_count']}
- **Topics discussed:** {qa['enrichment']['topics_count']}
- **Decisions:** {qa['enrichment']['decisions_count']}
- **Ordtelling:** {qa['enrichment']['word_count']} ord
"""

            if qa['quality_check']['issues']:
                report += f"- **🚨 Kritiske feil:** {', '.join(qa['quality_check']['issues'])}\n"
            if qa['quality_check']['warnings']:
                report += f"- **⚠️ Advarsler:** {', '.join(qa['quality_check']['warnings'])}\n"

    report += """

---

## 🎯 ANBEFALINGER

### Data kvalitet:
"""

    if needs_review:
        report += f"""
1. Gjennomgå de {len(needs_review)} møtene som trenger review
2. Utfyll manglende action items, topics og decisions der det er mulig
3. Verifiser at korte referater (<300 ord) inneholder nødvendig informasjon
"""
    else:
        report += """
✅ Alle møter har godkjent kvalitet
"""

    report += f"""

### Neste steg:
1. Oppdater meeting dashboard for å vise møtereferat-data
2. Legg til lenker til originaldokumenter
3. Vurder om møter uten referater trenger oppfølging

**Total dekningsgrad:** {total_enriched}/37 møter har nå strukturert referat-data
"""

    return report

def save_backup(meetings_data: Dict):
    """Save backup of meetings.json before modifying"""
    backup_file = MEETINGS_JSON.with_suffix('.backup.json')
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(meetings_data, f, indent=2, ensure_ascii=False)
    print(f"   💾 Backup saved to: {backup_file}")

def main():
    """Main execution function"""
    print("🔍 Beriker møter med referat-data...")

    # Load data
    meetings_data = load_meetings()
    analysis_data = load_analysis()

    print(f"   Lastet {len(meetings_data['meetings'])} møter")
    print(f"   Fant {len(analysis_data['matched'])} matchede referater")

    # Save backup
    save_backup(meetings_data)

    # Enrich meetings
    enriched_data, qa_reports = enrich_meetings(meetings_data, analysis_data)
    enriched_count = enriched_data['metadata']['last_enrichment']['meetings_enriched']

    print(f"   ✅ Beriket {enriched_count} møter med referat-data")

    # Save enriched meetings.json
    with open(MEETINGS_JSON, 'w', encoding='utf-8') as f:
        json.dump(enriched_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Oppdatert meetings.json")

    # Generate QA report
    qa_report = generate_qa_report(qa_reports, enriched_count)

    qa_output_file = OUTPUT_DIR / "meeting_enrichment_qa.md"
    with open(qa_output_file, 'w', encoding='utf-8') as f:
        f.write(qa_report)

    print(f"✅ QA-rapport lagret til: {qa_output_file}")

    # Save detailed JSON
    qa_json_file = OUTPUT_DIR / "meeting_enrichment_qa.json"
    with open(qa_json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_enriched': enriched_count,
                'approved': len([r for r in qa_reports if r['quality_check']['status'] == 'approved']),
                'needs_review': len([r for r in qa_reports if r['quality_check']['status'] == 'needs_review']),
                'average_quality_score': sum(r['quality_check']['quality_score'] for r in qa_reports) / len(qa_reports) if qa_reports else 0
            },
            'qa_reports': qa_reports
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ Detaljert QA-data lagret til: {qa_json_file}")

    # Print summary
    approved = len([r for r in qa_reports if r['quality_check']['status'] == 'approved'])
    needs_review = len([r for r in qa_reports if r['quality_check']['status'] == 'needs_review'])

    print(f"\n{'='*60}")
    print(f"📊 SAMMENDRAG")
    print(f"{'='*60}")
    print(f"Møter beriket: {enriched_count}")
    print(f"Godkjent kvalitet: {approved}")
    print(f"Trenger gjennomgang: {needs_review}")

if __name__ == '__main__':
    main()
