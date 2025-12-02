#!/usr/bin/env python3
"""
Consolidate Meeting Reports
Parse polished notes into structured JSON and embed in meetings.json
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import shutil

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
POLISHED_DIR = BASE_DIR / "data" / "polished_notes"

def load_json(filepath: Path) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath: Path, data: Dict):
    """Save JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def parse_markdown_sections(content: str) -> Dict:
    """Parse markdown into structured sections"""

    # Extract summary (first paragraph after metadata)
    summary_match = re.search(r'## Sammendrag\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else ""

    # Extract discussion sections
    discussion = []
    discussion_match = re.search(r'## Diskusjon\s+(.*?)(?=\n## [^#]|\Z)', content, re.DOTALL)
    if discussion_match:
        disc_content = discussion_match.group(1)
        # Split by ### headings
        sections = re.split(r'\n### ', disc_content)
        for section in sections:
            if section.strip():
                lines = section.split('\n', 1)
                if len(lines) >= 2:
                    heading = lines[0].strip()
                    content_text = lines[1].strip()
                    discussion.append({
                        'heading': heading,
                        'content': content_text
                    })
                elif len(lines) == 1:
                    # No heading, treat as intro
                    discussion.append({
                        'heading': 'Introduksjon',
                        'content': lines[0].strip()
                    })

    # Extract decisions
    decisions = []
    decisions_match = re.search(r'## Beslutninger\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if decisions_match:
        dec_content = decisions_match.group(1)
        # Extract list items
        decisions = re.findall(r'[-*]\s+(.+?)(?=\n[-*]|\Z)', dec_content, re.DOTALL)
        decisions = [d.strip() for d in decisions if d.strip()]

    # Extract action items
    action_items = []
    actions_match = re.search(r'## Action Items[^\n]*\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if actions_match:
        actions_content = actions_match.group(1)
        # Parse action items with structure: **[Task]** - Ansvarlig: [Person] - Frist: [Date]
        action_pattern = r'\*\*(.+?)\*\*\s*-\s*Ansvarlig:\s*(.+?)(?:\s*-\s*Frist:\s*(.+?))?(?=\n|$)'
        for match in re.finditer(action_pattern, actions_content):
            action_items.append({
                'task': match.group(1).strip(),
                'responsible': match.group(2).strip(),
                'deadline': match.group(3).strip() if match.group(3) else None
            })

    # Extract quotes
    quotes = []
    quotes_match = re.search(r'## Viktige sitater\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if quotes_match:
        quotes_content = quotes_match.group(1)
        quotes = re.findall(r'>\s*"(.+?)"', quotes_content)

    # Extract context
    context = ""
    context_match = re.search(r'## Kontekst og betydning\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if context_match:
        context = context_match.group(1).strip()

    # Extract topics discussed
    topics = []
    topics_match = re.search(r'## Diskusjonstemaer\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if topics_match:
        topics_content = topics_match.group(1)
        topics = re.findall(r'[-*]\s+(.+?)(?=\n[-*]|\Z)', topics_content)
        topics = [t.strip() for t in topics if t.strip()]

    return {
        'summary': summary,
        'topics': topics,
        'discussion': discussion,
        'decisions': decisions,
        'action_items': action_items,
        'quotes': quotes,
        'context': context
    }

def extract_metadata(content: str) -> Dict:
    """Extract metadata from markdown"""
    metadata = {}

    # Extract date
    date_match = re.search(r'\*\*Dato:\*\*\s*(.+)', content)
    if date_match:
        metadata['date'] = date_match.group(1).strip()

    # Extract location
    loc_match = re.search(r'\*\*Sted:\*\*\s*(.+)', content)
    if loc_match:
        metadata['location'] = loc_match.group(1).strip()

    # Extract word count
    word_count = len(re.findall(r'\w+', content))
    metadata['word_count'] = word_count

    return metadata

def consolidate_meeting(meeting: Dict, polished_note_path: Path) -> Dict:
    """Consolidate meeting with parsed polished note"""

    if not polished_note_path or not polished_note_path.exists():
        return meeting

    # Read polished note
    with open(polished_note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse sections
    sections = parse_markdown_sections(content)
    metadata = extract_metadata(content)

    # Build report structure
    report = {
        'summary': sections['summary'],
        'topics': sections['topics'],
        'discussion': sections['discussion'],
        'decisions': sections['decisions'],
        'action_items': sections['action_items'],
        'quotes': sections['quotes'],
        'context': sections['context'],
        'metadata': {
            'word_count': metadata.get('word_count', 0),
            'source': 'polished_note',
            'consolidated_date': datetime.now().strftime('%Y-%m-%d'),
            'sections': []
        }
    }

    # Determine available sections
    available_sections = []
    if report['summary']: available_sections.append('summary')
    if report['topics']: available_sections.append('topics')
    if report['discussion']: available_sections.append('discussion')
    if report['decisions']: available_sections.append('decisions')
    if report['action_items']: available_sections.append('action_items')
    if report['quotes']: available_sections.append('quotes')
    if report['context']: available_sections.append('context')

    report['metadata']['sections'] = available_sections
    report['metadata']['has_full_report'] = len(available_sections) >= 4

    # Add to meeting
    meeting['report'] = report

    # Update legacy fields for backwards compatibility
    if report['decisions']:
        meeting['decisions'] = report['decisions']
    if report['action_items']:
        meeting['action_items'] = [a['task'] for a in report['action_items']]
    if report['topics']:
        meeting['topics_discussed'] = report['topics']

    return meeting

def main():
    """Main execution"""
    print("📋 KONSOLIDERER MØTENOTATER...")
    print("="*60)
    print()

    # Backup
    backup_path = MEETINGS_JSON.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    shutil.copy(MEETINGS_JSON, backup_path)
    print(f"💾 Backup: {backup_path.name}")
    print()

    # Load meetings
    meetings_data = load_json(MEETINGS_JSON)
    meetings = meetings_data['meetings']

    # Process each meeting
    consolidated = 0
    skipped = 0

    for meeting in meetings:
        # Find polished note
        report_link = meeting.get('report_link', '')

        if not report_link or 'polished_notes' not in report_link:
            skipped += 1
            continue

        polished_path = BASE_DIR / report_link

        if not polished_path.exists():
            print(f"⚠️  Fil finnes ikke: {polished_path.name}")
            skipped += 1
            continue

        # Consolidate
        consolidate_meeting(meeting, polished_path)
        consolidated += 1

        print(f"✅ {meeting['title'][:50]}")
        if meeting.get('report'):
            sections = meeting['report']['metadata']['sections']
            print(f"   Seksjoner: {', '.join(sections)}")

    # Update metadata
    meetings_data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    meetings_data['metadata']['embedded_reports'] = consolidated

    # Save
    save_json(MEETINGS_JSON, meetings_data)

    print()
    print("="*60)
    print("RESULTAT")
    print("="*60)
    print(f"Konsolidert: {consolidated} møter")
    print(f"Hoppet over: {skipped} møter")
    print()
    print("✅ meetings.json oppdatert med embedded reports!")
    print()
    print("🎯 NESTE STEG:")
    print("   Implementer embedded rendering i dashboard")

if __name__ == '__main__':
    main()
