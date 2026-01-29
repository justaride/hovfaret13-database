#!/usr/bin/env python3
"""
Rewrite Meeting Notes with LLM
Uses project context and meeting metadata to create high-quality,
consistent meeting reports from raw notes.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import anthropic

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"
PROJECT_JSON = BASE_DIR / "data" / "project.json"
STAKEHOLDERS_ORGS = BASE_DIR / "data" / "stakeholders" / "organizations.json"
RESTRUCTURED_DIR = BASE_DIR / "data" / "restructured_notes"
POLISHED_DIR = BASE_DIR / "data" / "polished_notes"

# Create polished notes directory
POLISHED_DIR.mkdir(exist_ok=True)

def load_json(filepath: Path) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_markdown(filepath: Path, content: str):
    """Save markdown file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def build_project_context() -> str:
    """Build comprehensive project context for LLM"""

    # Load project data
    project = load_json(PROJECT_JSON)
    orgs = load_json(STAKEHOLDERS_ORGS)

    context = f"""# PROSJEKT-KONTEKST: HOVFARET 13

## Bygget
- **Adresse:** {project['building']['address']}
- **Byggeår:** {project['building']['built_year']}
- **Areal:** {project['building']['gross_area']} m² BTA
- **Etasjer:** {project['building']['current_floors']} (designet for {project['building']['designed_for_floors']})

## Prosjektmål
{project['project']['goal']}

## Hovedutfordring
Områdeplanen krever riving, men prosjektet argumenterer for transformasjon pga:
- 48% lavere CO₂-utslipp med rehabilitering vs riving
- Eksisterende struktur designet for påbygg
- Sosial og økonomisk verdi

## Hovedscenarier
"""

    for scenario in project['scenarios']:
        context += f"\n### {scenario['name']}"
        context += f"\n- **Type:** {scenario['type']}"
        context += f"\n- **Beskrivelse:** {scenario['description']}"
        if scenario.get('co2_savings'):
            context += f"\n- **CO₂-besparelse:** {scenario['co2_savings']}"

    context += "\n\n## Nøkkelaktører\n"
    for org in orgs['organizations'][:10]:  # Top 10
        context += f"\n- **{org['name']}** ({org['type']})"

    return context

def build_meeting_context(meeting: Dict) -> str:
    """Build specific meeting context"""

    context = f"""# MØTE-METADATA

**ID:** {meeting['id']}
**Dato:** {meeting.get('date', 'Ukjent')}
**Tittel:** {meeting['title']}
**Organisator:** {meeting.get('organizer', 'Ikke spesifisert')}
**Lokasjon:** {meeting.get('location', 'Ikke spesifisert')}

## Deltakere ({meeting.get('participant_count', 0)} personer)
"""

    for participant in meeting.get('participants', []):
        if isinstance(participant, dict):
            name = participant.get('name', 'Ukjent')
            org = participant.get('organization', 'Ukjent organisasjon')
            email = participant.get('email', '')
            context += f"\n- **{name}** - {org}"
            if email:
                context += f" ({email})"

    return context

def create_rewrite_prompt(meeting: Dict, raw_notes: str, project_context: str) -> str:
    """Create LLM prompt for rewriting meeting notes"""

    meeting_ctx = build_meeting_context(meeting)

    prompt = f"""{project_context}

{meeting_ctx}

---

# OPPGAVE: RENSKRIVE MØTENOTAT

Du skal renskrive rånotatene fra dette møtet til et profesjonelt, velstrukturert møtereferat.

## RÅNOTATER (fra original fil):

{raw_notes}

---

## INSTRUKSJONER FOR RENSKRIVNING:

1. **Behold all faktisk informasjon** - ikke oppfinn noe nytt
2. **Bruk prosjekt-konteksten** - forklar begreper og roller når relevant
3. **Ekstraher action items** - finn alle handlingspunkter, også implisitte
4. **Identifiser decisions** - finn alle beslutninger som ble tatt
5. **Strukturer topics** - organiser diskusjonstemaer logisk
6. **Rydd språk** - gjør teksten profesjonell men naturlig
7. **Behold detaljer** - spesifikke tall, navn, sitater er viktige

## OUTPUT-FORMAT:

Skriv møtereferatet i følgende Markdown-format:

```markdown
# [Møtetittel - lag en god, beskrivende tittel]

**Dato:** [Dato]
**Tid:** [Hvis nevnt i notater]
**Sted:** [Lokasjon]
**Organisert av:** [Organisator]

## Deltakere

[Liste over deltakere med organisasjon]

## Sammendrag

[2-3 setninger som oppsummerer møtets hovedbudskap]

## Agenda / Diskusjonstemaer

[Strukturert liste over hovedtemaer som ble diskutert]

## Diskusjon

[Detaljert beskrivelse av diskusjonen, organisert etter tema]

### [Tema 1]

[Innhold...]

### [Tema 2]

[Innhold...]

## Beslutninger

[Liste over alle beslutninger som ble tatt]

## Action Items / Handlingspunkter

[Strukturert liste med handlingspunkter. Format:]
- **[Oppgave]** - Ansvarlig: [Person/Org] - Frist: [Hvis nevnt]

## Viktige sitater / innsikter

[Hvis det er særlig viktige sitater eller innsikter]

## Vedlegg / Referanser

[Hvis det er lenker, dokumenter eller referanser nevnt]

---
*Møtereferat renskrevet: {datetime.now().strftime('%Y-%m-%d')}*
*Basert på: [original filnavn]*
```

## VIKTIG:
- Bruk norsk språk
- Behold alle spesifikke tall og fakta
- Hvis noe er uklart, behold original formulering
- Marker usikkerhet med [?] hvis nødvendig
- Bruk prosjekt-konteksten til å gi bedre forståelse

Skriv nå det renskrevne møtereferatet:"""

    return prompt

def rewrite_note_with_llm(meeting: Dict, raw_notes: str, project_context: str) -> str:
    """Use Claude to rewrite meeting note"""

    # Get API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    # Create client
    client = anthropic.Anthropic(api_key=api_key)

    # Create prompt
    prompt = create_rewrite_prompt(meeting, raw_notes, project_context)

    # Call Claude
    print(f"   🤖 Ber Claude om å renskrive notat...")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        temperature=0.3,  # Lower temperature for more consistent output
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract response
    polished_content = message.content[0].text

    return polished_content

def process_meeting(meeting: Dict, project_context: str, dry_run: bool = False) -> Optional[str]:
    """Process a single meeting note"""

    # Get report link
    report_link = meeting.get('report_link')
    if not report_link:
        print(f"   ⚠️  Ingen rapport-lenke for møte: {meeting['title']}")
        return None

    # Find the note file
    report_path = BASE_DIR / report_link.replace('data/', '')

    if not report_path.exists():
        print(f"   ❌ Fil finnes ikke: {report_path}")
        return None

    # Read raw notes
    with open(report_path, 'r', encoding='utf-8') as f:
        raw_notes = f.read()

    print(f"\n{'='*80}")
    print(f"Renskriver: {meeting['title'][:60]}")
    print(f"Dato: {meeting.get('date', 'Ukjent')}")
    print(f"Deltakere: {meeting.get('participant_count', 0)}")
    print(f"Original fil: {report_path.name}")
    print(f"Lengde: {len(raw_notes)} tegn")

    if dry_run:
        print("   [DRY RUN - hopper over LLM-kall]")
        return None

    # Rewrite with LLM
    try:
        polished_content = rewrite_note_with_llm(meeting, raw_notes, project_context)

        # Create output filename
        date_str = meeting.get('date', 'UKJENT_DATO')
        safe_title = meeting['id'].replace('m_', '').replace('unknown_date_', '')
        output_filename = f"{date_str}_{safe_title}_POLISHED.md"
        output_path = POLISHED_DIR / output_filename

        # Save polished note
        save_markdown(output_path, polished_content)

        print(f"   ✅ Renskrevet notat lagret: {output_filename}")
        print(f"   📊 Ny lengde: {len(polished_content)} tegn")

        return str(output_path)

    except Exception as e:
        print(f"   ❌ Feil ved renskrivning: {e}")
        return None

def main():
    """Main execution"""
    import sys

    print("📝 RENSKRIVER MØTENOTATER MED LLM")
    print("="*80)
    print()

    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ANTHROPIC_API_KEY environment variable ikke satt!")
        print()
        print("Sett API-nøkkel først:")
        print("export ANTHROPIC_API_KEY='your-key-here'")
        return

    # Load data
    print("📂 Laster data...")
    meetings_data = load_json(MEETINGS_JSON)
    meetings = meetings_data['meetings']

    # Build project context
    print("🏗️  Bygger prosjekt-kontekst...")
    project_context = build_project_context()
    print(f"   Kontekst: {len(project_context)} tegn")
    print()

    # Filter meetings with reports
    meetings_with_reports = [m for m in meetings if m.get('report_link')]
    print(f"Fant {len(meetings_with_reports)} møter med rapporter")
    print()

    # Check for arguments
    dry_run = '--dry-run' in sys.argv
    test_mode = '--test' in sys.argv

    if dry_run:
        print("🧪 DRY RUN MODE - ingen LLM-kall")
        print()

    if test_mode:
        print("🧪 TEST MODE - prosesserer kun 3 første møter")
        meetings_with_reports = meetings_with_reports[:3]
        print()

    # Process each meeting
    results = {
        'processed': 0,
        'skipped': 0,
        'failed': 0,
        'output_files': []
    }

    for i, meeting in enumerate(meetings_with_reports, 1):
        print(f"\n[{i}/{len(meetings_with_reports)}]")

        output_path = process_meeting(meeting, project_context, dry_run)

        if output_path:
            results['processed'] += 1
            results['output_files'].append(output_path)
        elif output_path is None and not dry_run:
            results['failed'] += 1
        else:
            results['skipped'] += 1

    # Summary
    print(f"\n{'='*80}")
    print("📊 SAMMENDRAG")
    print(f"{'='*80}")
    print(f"Prosessert: {results['processed']}")
    print(f"Hoppet over: {results['skipped']}")
    print(f"Feilet: {results['failed']}")
    print()

    if results['output_files']:
        print(f"✅ Renskrevne notater lagret i: {POLISHED_DIR}")
        print()
        print("📁 Filer:")
        for filepath in results['output_files'][:10]:
            print(f"   - {Path(filepath).name}")
        if len(results['output_files']) > 10:
            print(f"   ... og {len(results['output_files']) - 10} til")

    print()
    print("🎯 NESTE STEG:")
    print("1. Gjennomgå noen av de renskrevne notatene")
    print("2. Hvis kvaliteten er bra, oppdater meetings.json med nye lenker")
    print("3. Slett gamle restructured_notes hvis fornøyd")

if __name__ == '__main__':
    main()
