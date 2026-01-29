#!/usr/bin/env python3
"""
Enrich meetings from Google Drive markdown files.
"""

import json
import os
import re
from datetime import datetime

MEETINGS_PATH = "data/meetings.json"
DRIVE_PATH = "/Users/gabrielboen/Library/CloudStorage/GoogleDrive-gabriel@naturalstate.no/My Drive/H13 Backup Process Nov 25/MIRO ting. MØTE RAPPORTER VIKTIG ER HER "

# Direct mapping from markdown files to meeting dates
FILE_MAPPINGS = [
    {
        "file": "MØTE 03.06 2026.md",  # Actually June 3, 2025
        "date": "2025-06-03",
        "match_title": "Oppfølging Prosjekt Gruppen"
    },
    {
        "file": "MØTE  15 okt 24.md",
        "date": "2024-10-15",
        "match_title": "Oppfølging"
    },
    {
        "file": "Møtereferat URBANIA 27 JUNI 2024.docx",  # Will use extraction cache
        "date": "2024-06-27",
        "match_title": "Strategimøte Urbania"
    }
]


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_markdown(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None


def clean_text(text):
    if not text:
        return text
    text = text.replace('\\-', '-')
    text = text.replace('\\(', '(')
    text = text.replace('\\)', ')')
    text = text.replace('\\/', '/')
    text = text.replace('&#x2F;', '/')
    text = text.replace('\\.', '.')
    text = text.replace('&quot;', '"')
    return text


def parse_meeting_markdown(content):
    """Parse detailed meeting markdown into report structure."""
    content = clean_text(content)
    lines = content.split('\n')

    report = {
        "summary": "",
        "topics": [],
        "discussion": [],
        "decisions": [],
        "action_items": [],
        "quotes": [],
        "context": ""
    }

    current_heading = None
    current_content = []
    current_level = 0

    for line in lines:
        stripped = line.strip()

        # H1 - Main title
        if stripped.startswith('# ') and not stripped.startswith('## '):
            if not report["summary"]:
                report["summary"] = stripped[2:].strip()
            continue

        # H2 - Major sections
        if stripped.startswith('## '):
            if current_heading and current_content:
                content_text = '\n'.join(current_content).strip()
                if content_text:
                    report["discussion"].append({
                        "heading": current_heading,
                        "content": content_text
                    })
            current_heading = stripped[3:].strip()
            current_content = []
            current_level = 2
            continue

        # H3 - Subsections
        if stripped.startswith('### '):
            if current_heading and current_content:
                content_text = '\n'.join(current_content).strip()
                if content_text:
                    report["discussion"].append({
                        "heading": current_heading,
                        "content": content_text
                    })
            current_heading = stripped[4:].strip()
            current_content = []
            current_level = 3
            continue

        # Bullet points
        if stripped.startswith('- '):
            item = stripped[2:].strip()
            if current_heading:
                heading_lower = current_heading.lower()
                if any(kw in heading_lower for kw in ['konklusjon', 'beslutning', 'vedtak']):
                    report["decisions"].append(item)
                elif any(kw in heading_lower for kw in ['oppfølging', 'action', 'tiltak', 'neste', 'handlingspunkt']):
                    report["action_items"].append(item)
                elif any(kw in heading_lower for kw in ['tema', 'topic', 'agenda']):
                    report["topics"].append(item)
                else:
                    current_content.append(stripped)
            continue

        # Numbered items (action items often)
        if re.match(r'^\d+\.', stripped):
            item = re.sub(r'^\d+\.\s*', '', stripped).strip()
            if current_heading and any(kw in current_heading.lower() for kw in ['handlingspunkt', 'neste', 'oppfølging']):
                report["action_items"].append(item)
            else:
                current_content.append(stripped)
            continue

        # Regular content
        if stripped:
            current_content.append(stripped)

    # Save last section
    if current_heading and current_content:
        content_text = '\n'.join(current_content).strip()
        if content_text:
            report["discussion"].append({
                "heading": current_heading,
                "content": content_text
            })

    # Extract topics from discussion if none explicit
    if not report["topics"] and report["discussion"]:
        report["topics"] = [d["heading"] for d in report["discussion"][:8]]

    return report


def find_meeting(meetings, date_str, title_match=None):
    for m in meetings:
        if m.get("date") == date_str:
            if title_match:
                if title_match.lower() in m.get("title", "").lower():
                    return m
            else:
                return m
    # Fallback - just by date
    for m in meetings:
        if m.get("date") == date_str:
            return m
    return None


def main():
    print("=== Enriching from Google Drive ===\n")

    data = load_json(MEETINGS_PATH)
    meetings = data.get("meetings", [])
    enriched = 0

    # Process June 3, 2025 meeting (detailed report)
    print("Processing June 3, 2025 meeting...")
    june3_path = os.path.join(DRIVE_PATH, "MØTE 03.06 2026.md")
    content = read_markdown(june3_path)
    if content:
        meeting = find_meeting(meetings, "2025-06-03", "Oppfølging")
        if meeting:
            report = parse_meeting_markdown(content)
            if report and report.get("discussion"):
                # Only update if current report is empty or has no discussion
                if not meeting.get("report") or not meeting.get("report", {}).get("discussion"):
                    meeting["report"] = report
                    meeting["report_metadata"] = {
                        "enriched_date": datetime.now().isoformat(),
                        "source_file": "MØTE 03.06 2026.md",
                        "polished": True
                    }
                    print(f"  Enriched with {len(report['discussion'])} sections")
                    enriched += 1
                else:
                    print("  Already has report, checking if new is better...")
                    if len(report.get("discussion", [])) > len(meeting.get("report", {}).get("discussion", [])):
                        meeting["report"] = report
                        enriched += 1
                        print(f"  Updated with better report ({len(report['discussion'])} sections)")

    # Process October 15, 2024 meeting
    print("\nProcessing October 15, 2024 meeting...")
    oct15_path = os.path.join(DRIVE_PATH, "MØTE  15 okt 24.md")
    content = read_markdown(oct15_path)
    if content:
        meeting = find_meeting(meetings, "2024-10-15")
        if meeting:
            report = parse_meeting_markdown(content)
            if report and report.get("discussion"):
                if not meeting.get("report") or not meeting.get("report", {}).get("discussion"):
                    meeting["report"] = report
                    meeting["report_metadata"] = {
                        "enriched_date": datetime.now().isoformat(),
                        "source_file": "MØTE  15 okt 24.md",
                        "polished": True
                    }
                    print(f"  Enriched with {len(report['discussion'])} sections")
                    enriched += 1

    # Process other markdown files
    other_files = [
        ("MØTE  27 November 24.md", "2024-11-27"),
        ("MØTE 17  Januar 25.md", "2025-01-17"),
        ("MØTE 7  Mars 25.md", "2025-03-07"),
        ("MØTE 24.06.md", "2025-06-24"),
        ("Leietagermøte.md", "2025-01-10"),
        ("MØTE  19 Desember.md", "2024-12-19"),
        ("MØTE  6  MAI 2024.md", "2024-05-06"),
        ("MØTE  3  April 2024 .md", "2024-04-03"),
        ("MØTE  11 MARS 2024.md", "2024-03-11"),
    ]

    for filename, date_str in other_files:
        filepath = os.path.join(DRIVE_PATH, filename)
        content = read_markdown(filepath)
        if content and len(content) > 500:  # Only if substantial content
            meeting = find_meeting(meetings, date_str)
            if meeting:
                current_report = meeting.get("report", {})
                if not current_report or not current_report.get("discussion"):
                    report = parse_meeting_markdown(content)
                    if report and report.get("discussion"):
                        meeting["report"] = report
                        meeting["report_metadata"] = {
                            "enriched_date": datetime.now().isoformat(),
                            "source_file": filename,
                            "polished": True
                        }
                        print(f"Enriched {date_str} from {filename}")
                        enriched += 1

    # Update metadata
    data["metadata"]["last_drive_enrichment"] = {
        "date": datetime.now().isoformat(),
        "meetings_enriched": enriched
    }

    save_json(MEETINGS_PATH, data)
    print(f"\n=== Done! Enriched {enriched} meetings ===")


if __name__ == "__main__":
    main()
