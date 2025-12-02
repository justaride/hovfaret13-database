#!/usr/bin/env python3
"""
Prepare Meeting Notes for Rewriting
Generates rewrite instructions that Claude Code can execute interactively.
"""

import json
from pathlib import Path
from typing import Dict, List

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
PROJECT_JSON = BASE_DIR / "data" / "project.json"
STAKEHOLDERS_ORGS = BASE_DIR / "data" / "stakeholders" / "organizations.json"

def load_json(filepath: Path) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_project_context() -> str:
    """Build comprehensive project context"""

    project = load_json(PROJECT_JSON)

    context = f"""# HOVFARET 13 - PROSJEKT-KONTEKST

## Bygget
- Adresse: {project['building']['address']}
- Byggeår: {project['building']['built_year']}
- Areal: {project['building']['gross_area']} m² BTA
- Etasjer: {project['building']['current_floors']} (designet for {project['building']['designed_for_floors']})

## Hovedmål
{project['project']['goal']}

## Utfordring
Områdeplanen krever riving, men prosjektet argumenterer for transformasjon:
- 48% lavere CO₂ med rehabilitering vs riving
- Eksisterende struktur designet for påbygg
- Sosial og økonomisk verdi bevares

## Scenarier
"""

    for scenario in project['scenarios']:
        context += f"\n{scenario['name']}:\n"
        context += f"  - Type: {scenario['type']}\n"
        context += f"  - {scenario['description']}\n"
        if scenario.get('co2_savings'):
            context += f"  - CO₂: {scenario['co2_savings']}\n"

    return context

def generate_batch_file(meetings: List[Dict], output_file: Path):
    """Generate a batch processing file with all meetings"""

    meetings_with_reports = [m for m in meetings if m.get('report_link')]

    content = f"""# BATCH RENSKRIVNING - MØTENOTATER
## Generert: 2025-11-22
## Totalt: {len(meetings_with_reports)} møter

---

"""

    for i, meeting in enumerate(meetings_with_reports, 1):
        report_link = meeting['report_link']
        report_path = BASE_DIR / report_link.replace('data/', '')

        content += f"""
## MØTE {i}/{len(meetings_with_reports)}

**ID:** {meeting['id']}
**Tittel:** {meeting['title']}
**Dato:** {meeting.get('date', 'Ukjent')}
**Original fil:** {report_path}
**Output fil:** data/polished_notes/{meeting.get('date', 'UKJENT')}_{meeting['id']}_POLISHED.md

**Deltakere:**
"""

        for p in meeting.get('participants', []):
            if isinstance(p, dict):
                content += f"- {p.get('name', 'Ukjent')} - {p.get('organization', 'Ukjent org')}\n"

        content += f"\n**Fil-sti for renskrivning:** `{report_path}`\n"
        content += "\n---\n"

    # Save batch file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return len(meetings_with_reports)

def main():
    """Main execution"""

    print("📋 FORBEREDER BATCH RENSKRIVNING")
    print("="*80)
    print()

    # Load data
    meetings_data = load_json(MEETINGS_JSON)
    meetings = meetings_data['meetings']

    # Build project context
    project_context = build_project_context()

    # Save project context
    context_file = BASE_DIR / "analysis" / "PROJECT_CONTEXT_FOR_REWRITING.md"
    with open(context_file, 'w', encoding='utf-8') as f:
        f.write(project_context)
    print(f"✅ Prosjekt-kontekst lagret: {context_file}")

    # Generate batch file
    batch_file = BASE_DIR / "analysis" / "BATCH_REWRITE_PLAN.md"
    count = generate_batch_file(meetings, batch_file)
    print(f"✅ Batch plan lagret: {batch_file}")
    print(f"   {count} møter klare for renskrivning")

    print()
    print("🎯 NESTE STEG:")
    print("1. Claude Code vil nå renskrive alle møtenotater automatisk")
    print("2. Hver renskrevet versjon lagres i data/polished_notes/")
    print("3. Prosessen bruker full prosjekt-kontekst for hvert møte")

    return count

if __name__ == '__main__':
    main()
