#!/usr/bin/env python3
"""
Automatisk prosessering av gjenværende møtenotater til profesjonelle møtereferater.
Basert på format og stil fra allerede renskrevne notater.
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path("/Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified")
INPUT_DIR = BASE_DIR / "data/restructured_notes"
OUTPUT_DIR = BASE_DIR / "data/polished_notes"
MEETINGS_FILE = BASE_DIR / "data/meetings.json"
PROJECT_FILE = BASE_DIR / "data/project.json"

# Allerede prosesserte
COMPLETED = [
    "2024-03-11_MØTE  11 MARS   2024.md",
    "UKJENT_DATO_MØTE  3  April  .md",
    "2024-05-06_MØTE  6  MAI   2024.md"
]

def load_meetings():
    """Last meetings.json"""
    with open(MEETINGS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['meetings']

def load_project():
    """Last project.json"""
    with open(PROJECT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_meeting_metadata(filename, meetings):
    """Finn meeting metadata fra meetings.json basert på filnavn"""
    # Fjern .md og match
    for meeting in meetings:
        report_link = meeting.get('report_link', '')
        if filename in report_link or filename.replace('.md', '') in report_link:
            return meeting
    return None

def process_note(input_file, output_file, meeting_meta, project_context):
    """Prosesser et møtenotat"""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract basic info from content
    lines = content.split('\n')
    title = lines[0].replace('# ', '').strip() if lines else "Møtereferat"

    # Build polished note
    polished = []
    polished.append(f"# {title}")
    polished.append("")

    # Metadata fra meetings.json
    if meeting_meta:
        date_str = meeting_meta.get('date', 'Ukjent')
        location = meeting_meta.get('location', 'Ikke spesifisert')
        organizer = meeting_meta.get('organizer', 'Ikke spesifisert')

        polished.append(f"**Dato:** {date_str}")
        if location and location != 'null':
            polished.append(f"**Sted:** {location}")
        if organizer and organizer != 'null':
            polished.append(f"**Organisert av:** {organizer}")
        polished.append("")

        # Deltakere
        polished.append("## Deltakere")
        polished.append("")
        participants = meeting_meta.get('participants', [])
        if participants:
            for p in participants:
                name = p.get('name', '')
                org = p.get('organization', '')
                email = p.get('email', '')
                polished.append(f"- **{name}** - {org} ({email})")
        else:
            polished.append("*Ingen deltakere registrert i metadata*")
        polished.append("")

        # Sammendrag (placeholder)
        polished.append("## Sammendrag")
        polished.append("")
        polished.append("*[Dette notatet er automatisk prosessert og krever manuell redigering av sammendrag]*")
        polished.append("")

        # Topics
        topics = meeting_meta.get('topics_discussed', [])
        if topics and len(topics) > 0:
            polished.append("## Diskusjonstemaer")
            polished.append("")
            for topic in topics:
                topic_clean = topic.replace('\\', '')
                polished.append(f"- {topic_clean}")
            polished.append("")

        # Diskusjon (fra original)
        polished.append("## Diskusjon")
        polished.append("")
        polished.append("*[Original innhold følger - krever manuell renskrivning]*")
        polished.append("")

        # Find discussion section
        in_discussion = False
        for line in lines:
            if line.startswith('## Diskusjon') or line.startswith('## Notater'):
                in_discussion = True
                continue
            if in_discussion and line.startswith('## '):
                break
            if in_discussion:
                polished.append(line)

        polished.append("")

        # Beslutninger
        polished.append("## Beslutninger")
        polished.append("")
        decisions = meeting_meta.get('decisions', [])
        if decisions and len(decisions) > 0:
            for decision in decisions:
                decision_clean = decision.replace('\\', '')
                polished.append(f"- {decision_clean}")
        else:
            polished.append("*Ingen beslutninger registrert*")
        polished.append("")

        # Action Items
        polished.append("## Action Items")
        polished.append("")
        action_items = meeting_meta.get('action_items', [])
        if action_items and len(action_items) > 0:
            for item in action_items:
                item_clean = item.replace('\\', '')
                polished.append(f"- {item_clean}")
        else:
            polished.append("*Ingen action items registrert*")
        polished.append("")

        # Kontekst
        polished.append("## Prosjekt-kontekst")
        polished.append("")
        polished.append("**Hovfaret 13** er et transformasjonsprosjekt for et kontorbygg fra 1989 på Skøyen, Oslo.")
        polished.append(f"Bygget står overfor rivningskrav i områdeplanen (vedtatt sept 2023), men prosjektet argumenterer for at rehabilitering gir 48% lavere CO₂-utslipp sammenlignet med riving og nybygg (456 vs 631 kg CO₂-ekv/m² BTA).")
        polished.append("")
        polished.append("Bygget er fundamentert for 12 etasjer (kun 5 bygget), noe som muliggjør vertikal utvidelse uten ny fundamentering.")
        polished.append("")

        # Footer
        polished.append("---")
        polished.append("*Renskrevet: 2025-11-22*")
        polished.append(f"*Basert på: {os.path.basename(input_file)}*")
        if meeting_meta.get('id'):
            polished.append(f"*Møte-ID: {meeting_meta['id']}*")
        polished.append("*Status: AUTOMATISK PROSESSERT - KREVER MANUELL REDIGERING*")
        polished.append("")

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(polished))

    return len(polished)

def main():
    """Main processing function"""

    print("=== Prosessering av møtenotater ===\n")

    # Load data
    meetings = load_meetings()
    project = load_project()

    print(f"Lastet {len(meetings)} møter fra meetings.json")
    print(f"Prosjekt: {project['project']['name']}\n")

    # Get all input files
    input_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.md')])

    # Filter out completed and report
    to_process = [f for f in input_files if f not in COMPLETED and f != 'restructuring_report.md']

    print(f"Totalt {len(input_files)} filer i input")
    print(f"Allerede prosessert: {len(COMPLETED)}")
    print(f"Skal prosessere: {len(to_process)}\n")

    # Process each file
    processed = 0
    for filename in to_process:
        input_path = INPUT_DIR / filename

        # Find meeting metadata
        meeting_meta = get_meeting_metadata(filename, meetings)

        # Generate output filename
        if meeting_meta and meeting_meta.get('id'):
            meeting_id = meeting_meta['id']
            date_prefix = meeting_meta.get('date', 'UKJENT').replace('-', '_')
            output_filename = f"{date_prefix}_{meeting_id}_POLISHED.md"
        else:
            output_filename = filename.replace('.md', '_POLISHED.md')

        output_path = OUTPUT_DIR / output_filename

        # Process
        try:
            lines_written = process_note(input_path, output_path, meeting_meta, project)
            processed += 1
            status = "✓" if meeting_meta else "⚠"
            print(f"{status} {filename} -> {output_filename} ({lines_written} lines)")
        except Exception as e:
            print(f"✗ ERROR: {filename} - {str(e)}")

    print(f"\n=== Ferdig ===")
    print(f"Prosesserte: {processed}/{len(to_process)}")
    print(f"\nOutput: {OUTPUT_DIR}")

    # Generate summary
    summary_path = OUTPUT_DIR / "_PROCESSING_SUMMARY.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# Prosesseringsrapport - Møtenotater\n\n")
        f.write(f"**Dato:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## Status\n\n")
        f.write(f"- Totalt møtenotater: {len(input_files) - 1} (eks. report)\n")
        f.write(f"- Manuelt prosessert (høy kvalitet): {len(COMPLETED)}\n")
        f.write(f"- Automatisk prosessert (krever redigering): {processed}\n")
        f.write(f"- Totalt prosessert: {len(COMPLETED) + processed}\n\n")
        f.write(f"## Manuelt prosesserte (høy kvalitet)\n\n")
        for f_name in COMPLETED:
            f.write(f"- {f_name}\n")
        f.write(f"\n## Automatisk prosesserte (krever manuell redigering)\n\n")
        for f_name in to_process:
            f.write(f"- {f_name}\n")
        f.write(f"\n## Neste steg\n\n")
        f.write(f"De automatisk prosesserte notatene har basisstruktur og metadata, ")
        f.write(f"men krever manuell renskrivning av:\n\n")
        f.write(f"1. Sammendrag\n")
        f.write(f"2. Diskusjonsseksjon (nå rå innhold)\n")
        f.write(f"3. Ekstrahere viktige sitater\n")
        f.write(f"4. Forbedre action items og beslutninger\n")
        f.write(f"5. Legge til kontekst og betydning\n\n")

    print(f"\nSammendrag skrevet til: {summary_path}")

if __name__ == "__main__":
    main()
