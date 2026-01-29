#!/usr/bin/env python3
"""
Enrich sparse meetings in meetings.json with content from extraction cache.
"""

import json
import os
import re
from datetime import datetime

# Paths
MEETINGS_PATH = "data/meetings.json"
EXTRACTION_CACHE = "source/extraction-cache"

# Mapping of sparse meetings to source files
ENRICHMENT_MAP = {
    # November 27, 2024 meeting
    "2024-11-27": {
        "source": "extract_MØTE  27 November 24_20251120160321.json",
        "meeting_title_contains": "27 November"
    },
    # January 17, 2025 meeting
    "2025-01-17": {
        "source": "extract_MØTE 17  Januar 25_20251120160321.json",
        "meeting_title_contains": "17"
    },
    # October 15, 2024 meeting
    "2024-10-15": {
        "source": "extract_MØTE  15 okt 24_20251120160321.json",
        "meeting_title_contains": "Oppfølging"
    },
    # December 19, 2024 meeting
    "2024-12-19": {
        "source": "extract_MØTE  19 Desember_20251120160321.json",
        "meeting_title_contains": "Desember"
    },
    # Tenant meeting (January 10, 2025)
    "2025-01-10": {
        "source": "extract_Leietagermøte_20251120160321.json",
        "meeting_title_contains": "LEIETAKER"
    }
}

# Meetings to CREATE (don't exist in meetings.json yet)
NEW_MEETINGS = {
    "2024-06-27": {
        "source": "extract_Møtereferat URBANIA 27 JUNI 2024_20251120160322.json",
        "title": "Strategimøte Urbania/Natural State - Hovfaret 13",
        "organizer": "gabriel@naturalstate.no",
        "location": "Hovfaret 13, Skøyen",
        "participants": [
            {"name": "Einar Holthe", "organization": "Natural State AS", "email": "einar@naturalstate.no"},
            {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
            {"name": "Eirik", "organization": "Natural State AS"},
            {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS", "email": "andreas@urbania.no"}
        ]
    }
}


def load_json(path):
    """Load JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    """Save JSON file with pretty formatting."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clean_text(text):
    """Clean markdown escape sequences."""
    if not text:
        return text
    # Remove backslash escapes
    text = text.replace('\\-', '-')
    text = text.replace('\\(', '(')
    text = text.replace('\\)', ')')
    text = text.replace('\\/', '/')
    text = text.replace('&#x2F;', '/')
    text = text.replace('\\.', '.')
    return text


def parse_markdown_content(full_text):
    """Parse markdown content into structured report format."""
    if not full_text:
        return None

    full_text = clean_text(full_text)

    # Extract sections
    lines = full_text.split('\n')

    report = {
        "summary": "",
        "topics": [],
        "discussion": [],
        "decisions": [],
        "action_items": [],
        "quotes": [],
        "context": ""
    }

    current_section = None
    current_heading = None
    current_content = []

    for line in lines:
        line = line.strip()

        # H1 - Main title (skip, use as context)
        if line.startswith('# '):
            if not report["summary"]:
                report["summary"] = line[2:]
            continue

        # H2 - Major sections
        if line.startswith('## '):
            # Save previous section
            if current_heading and current_content:
                report["discussion"].append({
                    "heading": current_heading,
                    "content": '\n'.join(current_content)
                })
            current_heading = line[3:]
            current_content = []
            continue

        # H3 - Subsections
        if line.startswith('### '):
            if current_heading and current_content:
                report["discussion"].append({
                    "heading": current_heading,
                    "content": '\n'.join(current_content)
                })
            current_heading = line[4:]
            current_content = []
            continue

        # Bullet points - could be topics, decisions, or action items
        if line.startswith('- '):
            item = line[2:].strip()
            if current_heading:
                heading_lower = current_heading.lower()
                if 'konklusjon' in heading_lower or 'beslutning' in heading_lower or 'vedtak' in heading_lower:
                    report["decisions"].append(item)
                elif 'oppfølging' in heading_lower or 'action' in heading_lower or 'tiltak' in heading_lower or 'neste' in heading_lower:
                    report["action_items"].append(item)
                elif 'tema' in heading_lower or 'topic' in heading_lower or 'agenda' in heading_lower:
                    report["topics"].append(item)
                else:
                    current_content.append(line)
            else:
                current_content.append(line)
            continue

        # Numbered items
        if re.match(r'^\d+\.', line):
            item = re.sub(r'^\d+\.\s*', '', line).strip()
            if current_heading:
                heading_lower = current_heading.lower()
                if 'oppfølging' in heading_lower or 'action' in heading_lower or 'neste' in heading_lower:
                    report["action_items"].append(item)
                else:
                    current_content.append(line)
            continue

        # Regular content
        if line:
            current_content.append(line)

    # Save last section
    if current_heading and current_content:
        report["discussion"].append({
            "heading": current_heading,
            "content": '\n'.join(current_content)
        })

    # Generate summary if not already set
    if not report["summary"] and report["discussion"]:
        # Use first discussion section as summary
        first_content = report["discussion"][0]["content"] if report["discussion"] else ""
        report["summary"] = first_content[:500] + "..." if len(first_content) > 500 else first_content

    # Extract topics from discussion headings if no explicit topics
    if not report["topics"] and report["discussion"]:
        report["topics"] = [d["heading"] for d in report["discussion"][:5]]

    return report


def find_meeting_by_date_and_title(meetings, date_str, title_contains):
    """Find a meeting by date and title substring."""
    for meeting in meetings:
        if meeting.get("date") == date_str:
            if title_contains.lower() in meeting.get("title", "").lower():
                return meeting
        # Also check if date matches without specific title
        if meeting.get("date") == date_str and not title_contains:
            return meeting

    # Fallback: just find by date
    for meeting in meetings:
        if meeting.get("date") == date_str:
            return meeting

    return None


def enrich_meeting(meeting, source_path):
    """Enrich a single meeting with source content."""
    if not os.path.exists(source_path):
        print(f"  Source file not found: {source_path}")
        return False

    try:
        source_data = load_json(source_path)
        full_text = source_data.get("full_text", "")

        if not full_text:
            print(f"  No content in source file")
            return False

        # Parse the content
        report = parse_markdown_content(full_text)

        if report:
            # Add report to meeting
            meeting["report"] = report

            # Update topics if empty
            if not meeting.get("topics_discussed") and report.get("topics"):
                meeting["topics_discussed"] = report["topics"]

            # Update decisions if empty
            if not meeting.get("decisions") and report.get("decisions"):
                meeting["decisions"] = report["decisions"]

            # Update action items if empty
            if not meeting.get("action_items") and report.get("action_items"):
                meeting["action_items"] = report["action_items"]

            # Add report metadata
            meeting["report_metadata"] = {
                "enriched_date": datetime.now().isoformat(),
                "source_file": source_data.get("file_name", ""),
                "polished": True
            }

            print(f"  Enriched with {len(report.get('discussion', []))} sections")
            return True

    except Exception as e:
        print(f"  Error enriching: {e}")
        return False

    return False


def create_new_meeting(date_str, config, source_path):
    """Create a new meeting entry from source content."""
    if not os.path.exists(source_path):
        print(f"  Source file not found: {source_path}")
        return None

    try:
        source_data = load_json(source_path)
        full_text = source_data.get("full_text", "")

        if not full_text:
            print(f"  No content in source file")
            return None

        # Parse the content
        report = parse_markdown_content(full_text)

        if report:
            # Create new meeting structure
            meeting_id = f"m_{date_str}_{config['title'].lower().replace(' ', '_').replace('-', '_')[:30]}"

            new_meeting = {
                "id": meeting_id,
                "date": date_str,
                "title": config["title"],
                "organizer": config.get("organizer", ""),
                "location": config.get("location", ""),
                "participant_count": len(config.get("participants", [])),
                "participants": config.get("participants", []),
                "topics_discussed": report.get("topics", []),
                "decisions": report.get("decisions", []),
                "action_items": report.get("action_items", []),
                "report": report,
                "report_metadata": {
                    "created_date": datetime.now().isoformat(),
                    "source_file": source_data.get("file_name", ""),
                    "polished": True
                }
            }

            return new_meeting

    except Exception as e:
        print(f"  Error creating meeting: {e}")
        return None

    return None


def main():
    print("=== Enriching Sparse Meetings ===\n")

    # Load meetings
    meetings_data = load_json(MEETINGS_PATH)
    meetings = meetings_data.get("meetings", [])

    enriched_count = 0
    created_count = 0

    # First, create new meetings that don't exist
    print("=== Creating New Meetings ===")
    for date_str, config in NEW_MEETINGS.items():
        print(f"\nCreating meeting for {date_str}...")

        # Check if meeting already exists
        existing = find_meeting_by_date_and_title(meetings, date_str, config.get("title", "")[:10])
        if existing:
            print(f"  Meeting already exists: {existing.get('title', '')[:40]}")
            continue

        source_path = os.path.join(EXTRACTION_CACHE, config["source"])
        new_meeting = create_new_meeting(date_str, config, source_path)

        if new_meeting:
            meetings.append(new_meeting)
            created_count += 1
            print(f"  Created: {new_meeting['title'][:50]}")

    # Then enrich existing sparse meetings
    print("\n=== Enriching Existing Meetings ===")
    for date_str, config in ENRICHMENT_MAP.items():
        print(f"\nProcessing {date_str}...")

        # Find meeting
        meeting = find_meeting_by_date_and_title(
            meetings,
            date_str,
            config.get("meeting_title_contains", "")
        )

        if not meeting:
            print(f"  Meeting not found for date {date_str}")
            continue

        print(f"  Found: {meeting.get('title', 'Unknown')[:50]}")

        # Check if already has report
        if meeting.get("report") and meeting["report"].get("discussion"):
            print(f"  Already has report, skipping")
            continue

        # Enrich
        source_path = os.path.join(EXTRACTION_CACHE, config["source"])
        if enrich_meeting(meeting, source_path):
            enriched_count += 1

    # Sort meetings by date
    meetings.sort(key=lambda m: m.get("date", "0000-00-00"))
    meetings_data["meetings"] = meetings

    # Update metadata
    meetings_data["metadata"]["last_enrichment"] = {
        "date": datetime.now().isoformat(),
        "meetings_enriched": enriched_count,
        "meetings_created": created_count,
        "script": "enrich-sparse-meetings.py"
    }
    meetings_data["metadata"]["total_meetings"] = len(meetings)

    # Save
    save_json(MEETINGS_PATH, meetings_data)

    print(f"\n=== Done! Created {created_count}, Enriched {enriched_count} meetings ===")


if __name__ == "__main__":
    main()
