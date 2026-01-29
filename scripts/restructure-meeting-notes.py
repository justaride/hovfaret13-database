#!/usr/bin/env python3
"""
Meeting Notes Restructuring Script
Takes unstructured notes and restructures them using metadata from meetings.json
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETING_NOTES_DIR = Path("/Users/gabrielboen/Downloads/Møter hovfaret ")
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
PARSED_JSON = BASE_DIR / "analysis" / "meeting_notes_parsed.json"
OUTPUT_DIR = BASE_DIR / "data" / "restructured_notes"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# Standard meeting note template
MEETING_NOTE_TEMPLATE = """# {title}

**Dato:** {date}
**Sted:** {location}
**Organisert av:** {organizer}

## Deltakere

{participants}

## Agenda / Topics Discussed

{topics}

## Diskusjon / Notater

{content}

## Beslutninger

{decisions}

## Action Items / Handlingspunkter

{action_items}

## Vedlegg / Lenker

{attachments}

---
*Møtereferat oppdatert: {updated}*
"""

def load_meetings():
    """Load meetings from meetings.json"""
    with open(MEETINGS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {m['id']: m for m in data['meetings']}

def load_parsed_notes():
    """Load parsed meeting notes"""
    with open(PARSED_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['notes'], data['gaps']

def format_participants(participants: List) -> str:
    """Format participants list for template"""
    if not participants:
        return "_Ingen deltakere registrert_"

    formatted = []
    for p in participants:
        if isinstance(p, dict):
            name = p.get('name', 'Ukjent')
            org = p.get('organization', '')
            email = p.get('email', '')

            line = f"- **{name}**"
            if org:
                line += f" ({org})"
            if email:
                line += f" - [{email}](mailto:{email})"
            formatted.append(line)
        else:
            # String participant
            formatted.append(f"- {p}")

    return "\n".join(formatted)

def format_list_items(items: List[str], empty_text: str = "_Ingen registrert_") -> str:
    """Format list items for template"""
    if not items:
        return empty_text

    return "\n".join(f"- {item}" for item in items)

def extract_content_sections(full_text: str) -> Dict[str, str]:
    """Extract different sections from unstructured content"""
    # Remove common headers that we'll add in template
    content = full_text

    # Remove title (first heading)
    content = re.sub(r'^#\s+.+?\n', '', content, count=1, flags=re.MULTILINE)

    # Remove participant sections (we'll use meetings.json data)
    content = re.sub(r'##?\s*(?:Deltakere?|Tilstede|Participants):?\s*\n(?:[-*]\s*.+\n?)+', '', content, flags=re.IGNORECASE | re.MULTILINE)

    # Remove action items sections (we'll restructure)
    content = re.sub(r'##?\s*(?:Action\s*items?|Handlingspunkter?):?\s*\n(?:[-*]\s*.+\n?)+', '', content, flags=re.IGNORECASE | re.MULTILINE)

    # Remove decision sections (we'll restructure)
    content = re.sub(r'##?\s*(?:Beslutninger?|Decisions?|Vedtak):?\s*\n(?:[-*]\s*.+\n?)+', '', content, flags=re.IGNORECASE | re.MULTILINE)

    # Clean up multiple blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)

    return {
        'content': content.strip()
    }

def extract_topics_from_headings(content: str) -> List[str]:
    """Extract topics from markdown headings"""
    topics = []

    # Find all ## headings that aren't meta sections
    heading_pattern = r'^##\s+(.+)$'
    headings = re.findall(heading_pattern, content, re.MULTILINE)

    # Filter out common meta-headings
    exclude = [
        'deltakere', 'participants', 'action items', 'handlingspunkter',
        'beslutninger', 'decisions', 'vedtak', 'agenda', 'notater',
        'notes', 'diskusjon', 'discussion', 'bakgrunn', 'background'
    ]

    for heading in headings:
        clean = heading.strip()
        if clean and not any(ex in clean.lower() for ex in exclude):
            topics.append(clean)

    return topics

def smart_extract_action_items(content: str, existing_items: List[str]) -> List[str]:
    """Extract action items using multiple strategies"""
    action_items = existing_items.copy()

    # Strategy 1: Look for common action phrases in Norwegian
    action_phrases = [
        r'vi\s+(?:må|skal|bør|trenger\s+å)\s+(.+?)(?:\.|$)',
        r'(?:oppgave|handling):?\s+(.+?)(?:\.|$)',
        r'(?:neste\s+steg|next\s+step):?\s+(.+?)(?:\.|$)',
        r'(?:følg\s+opp|follow\s+up):?\s+(.+?)(?:\.|$)',
        r'(?:avtale|agreed):?\s+(.+?)(?:\.|$)',
    ]

    for pattern in action_phrases:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            item = match.strip()
            if len(item) > 10 and len(item) < 200 and item not in action_items:
                action_items.append(item)

    # Deduplicate
    return list(dict.fromkeys(action_items))[:10]  # Max 10 items

def smart_extract_decisions(content: str, existing_decisions: List[str]) -> List[str]:
    """Extract decisions using multiple strategies"""
    decisions = existing_decisions.copy()

    # Strategy 1: Look for decision keywords
    decision_phrases = [
        r'(?:vi|det\s+ble)\s+(?:besluttet|vedtatt|ble\s+enige\s+om)\s+(?:at\s+)?(.+?)(?:\.|$)',
        r'enighet\s+om\s+(.+?)(?:\.|$)',
        r'konklusjon:?\s+(.+?)(?:\.|$)',
        r'beslutning:?\s+(.+?)(?:\.|$)',
    ]

    for pattern in decision_phrases:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            decision = match.strip()
            if len(decision) > 15 and len(decision) < 300 and decision not in decisions:
                decisions.append(decision)

    # Deduplicate
    return list(dict.fromkeys(decisions))[:10]  # Max 10 decisions

def restructure_note(note: Dict, meeting: Optional[Dict] = None) -> str:
    """Restructure a meeting note using template and metadata"""

    # Get metadata from meeting if available, otherwise from note
    if meeting:
        title = meeting.get('title', note['title'])
        date = meeting.get('date', note['date'])
        location = meeting.get('location', note.get('location', '_Ikke spesifisert_'))
        organizer = meeting.get('organizer', '_Ikke spesifisert_')
        participants_data = meeting.get('participants', [])
    else:
        title = note['title']
        date = note['date'] or '_Ukjent dato_'
        location = note.get('location', '_Ikke spesifisert_')
        organizer = '_Ikke spesifisert_'
        participants_data = note.get('participants', [])

    # Format date nicely if available
    if date and date != '_Ukjent dato_':
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_formatted = date_obj.strftime('%d. %B %Y')
            # Translate month to Norwegian
            months_no = {
                'January': 'januar', 'February': 'februar', 'March': 'mars',
                'April': 'april', 'May': 'mai', 'June': 'juni',
                'July': 'juli', 'August': 'august', 'September': 'september',
                'October': 'oktober', 'November': 'november', 'December': 'desember'
            }
            for en, no in months_no.items():
                date_formatted = date_formatted.replace(en, no)
        except:
            date_formatted = date
    else:
        date_formatted = '_Ukjent dato_'

    # Extract content sections
    content_sections = extract_content_sections(note['content'])

    # Get topics (from note + extract from headings)
    topics = note.get('topics_discussed', [])
    if not topics:
        topics = extract_topics_from_headings(note['content'])

    # Smart extract action items
    action_items = smart_extract_action_items(
        note['content'],
        note.get('action_items', [])
    )

    # Smart extract decisions
    decisions = smart_extract_decisions(
        note['content'],
        note.get('decisions', [])
    )

    # Format all sections
    formatted_note = MEETING_NOTE_TEMPLATE.format(
        title=title,
        date=date_formatted,
        location=location,
        organizer=organizer,
        participants=format_participants(participants_data),
        topics=format_list_items(topics, "_Ingen spesifikke topics registrert_"),
        content=content_sections['content'],
        decisions=format_list_items(decisions, "_Ingen beslutninger registrert_"),
        action_items=format_list_items(action_items, "_Ingen handlingspunkter registrert_"),
        attachments="_Ingen vedlegg_",
        updated=datetime.now().strftime('%Y-%m-%d %H:%M')
    )

    return formatted_note

def generate_restructuring_report(results: List[Dict]) -> str:
    """Generate report on restructuring process"""

    total = len(results)
    with_meeting = len([r for r in results if r['matched_meeting']])
    improved = len([r for r in results if r['improvements_made']])

    report = f"""# MØTENOTATER OMSTRUKTURERING RAPPORT
## Hovfaret 13 Prosjekt

**Generert:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 OVERSIKT

- **Totalt notater omstrukturert:** {total}
- **Matchet med møte-metadata:** {with_meeting}
- **Forbedringer gjort:** {improved}

---

## ✅ OMSTRUKTURERTE NOTATER

"""

    for result in sorted(results, key=lambda x: x['output_filename']):
        report += f"""
### {result['original_filename']}

- **Ny fil:** `{result['output_filename']}`
- **Matchet møte:** {'✅ Ja' if result['matched_meeting'] else '❌ Nei'}
- **Forbedringer:**
  - Deltakere lagt til: {'✅' if result['added_participants'] else '❌'}
  - Metadata lagt til: {'✅' if result['added_metadata'] else '❌'}
  - Action items forbedret: {'✅' if result['improved_actions'] else '❌'}
  - Decisions forbedret: {'✅' if result['improved_decisions'] else '❌'}
  - Topics forbedret: {'✅' if result['improved_topics'] else '❌'}
"""

    report += f"""

---

## 🎯 NESTE STEG

1. **Gjennomgå omstrukturerte notater** i `{OUTPUT_DIR}/`
2. **Manuell kvalitetssikring** av action items og decisions
3. **Oppdater meetings.json** med lenker til nye notater
4. **Erstatt originale notater** med omstrukturerte versjoner
5. **Integrer i dashboard** for visning

---

## 📂 FILER

Alle omstrukturerte notater finnes i:
```
{OUTPUT_DIR}/
```

Bruk disse som grunnlag for oppdatering av meetings.json.
"""

    return report

def main():
    """Main execution function"""
    print("🔄 Omstrukturerer møtenotater med metadata fra meetings.json...")

    # Load data
    meetings = load_meetings()
    notes, gaps = load_parsed_notes()

    print(f"   Lastet {len(meetings)} møter fra meetings.json")
    print(f"   Lastet {len(notes)} parsede notater")

    # Process each note
    results = []

    for note in notes:
        # Try to match with meeting
        meeting = None
        matched = False

        if note['date']:
            # Find meeting with matching date
            for meeting_id, m in meetings.items():
                if m.get('date') == note['date']:
                    meeting = m
                    matched = True
                    print(f"   ✅ Matchet: {note['filename']} → {meeting['title']}")
                    break

        if not matched:
            print(f"   ⚠️  Ingen match: {note['filename']}")

        # Restructure note
        restructured = restructure_note(note, meeting)

        # Generate output filename
        if note['date']:
            output_filename = f"{note['date']}_{note['filename']}"
        else:
            output_filename = f"UKJENT_DATO_{note['filename']}"

        # Save restructured note
        output_path = OUTPUT_DIR / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(restructured)

        # Track improvements
        improvements = {
            'original_filename': note['filename'],
            'output_filename': output_filename,
            'matched_meeting': matched,
            'added_participants': matched and meeting and meeting.get('participants'),
            'added_metadata': matched and meeting,
            'improved_actions': len(smart_extract_action_items(note['content'], note.get('action_items', []))) > len(note.get('action_items', [])),
            'improved_decisions': len(smart_extract_decisions(note['content'], note.get('decisions', []))) > len(note.get('decisions', [])),
            'improved_topics': len(extract_topics_from_headings(note['content'])) > len(note.get('topics_discussed', [])),
            'improvements_made': True  # Always true since we add structure
        }

        results.append(improvements)

    # Generate report
    report = generate_restructuring_report(results)

    report_path = OUTPUT_DIR / "restructuring_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Omstrukturert {len(results)} notater")
    print(f"✅ Lagret i: {OUTPUT_DIR}/")
    print(f"✅ Rapport: {report_path}")

    # Save results as JSON
    json_path = OUTPUT_DIR / "restructuring_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_restructured': len(results),
                'matched_with_meeting': len([r for r in results if r['matched_meeting']]),
                'participants_added': len([r for r in results if r['added_participants']]),
                'metadata_added': len([r for r in results if r['added_metadata']])
            },
            'results': results
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON-data: {json_path}")

    # Print summary
    matched = len([r for r in results if r['matched_meeting']])
    print(f"\n{'='*60}")
    print(f"📊 SAMMENDRAG")
    print(f"{'='*60}")
    print(f"Notater omstrukturert: {len(results)}")
    print(f"Matchet med møte: {matched}/{len(results)}")
    print(f"Forbedret metadata: {matched}")

if __name__ == '__main__':
    main()
