#!/usr/bin/env python3
"""
Identify Duplicate Meetings Script
Identifies meetings that might be duplicates based on:
- Same date
- Similar content/topics
- Overlapping participants
"""

import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).parent.parent
MEETINGS_JSON = BASE_DIR / "data" / "meetings.json"

def load_json(filepath: Path) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_topic_words(meeting: Dict) -> Set[str]:
    """Extract significant words from topics and title"""
    words = set()

    # From title
    title = meeting.get('title', '').lower()
    words.update(title.split())

    # From topics
    for topic in meeting.get('topics_discussed', []):
        words.update(topic.lower().split())

    # Remove common words
    stopwords = {'og', 'av', 'i', 'på', 'med', 'til', 'for', 'om', 'det', 'er', 'en', 'et'}
    words = {w for w in words if len(w) > 2 and w not in stopwords}

    return words

def calculate_similarity(m1: Dict, m2: Dict) -> float:
    """Calculate similarity score between two meetings"""
    score = 0.0

    # Same date (base requirement)
    if m1.get('date') != m2.get('date'):
        return 0.0

    # Topic overlap
    topics1 = get_topic_words(m1)
    topics2 = get_topic_words(m2)
    if topics1 and topics2:
        overlap = len(topics1.intersection(topics2))
        union = len(topics1.union(topics2))
        if union > 0:
            score += (overlap / union) * 40

    # Participant overlap
    participants1 = {p['name'].lower() for p in m1.get('participants', []) if isinstance(p, dict)}
    participants2 = {p['name'].lower() for p in m2.get('participants', []) if isinstance(p, dict)}
    if participants1 and participants2:
        overlap = len(participants1.intersection(participants2))
        score += overlap * 10

    # Same organizer
    if m1.get('organizer') and m2.get('organizer'):
        if m1['organizer'] == m2['organizer']:
            score += 20

    # Both have reports
    if m1.get('report_link') and m2.get('report_link'):
        score += 10

    return score

def analyze_duplicates(meetings: List[Dict]) -> Dict:
    """Analyze meetings for potential duplicates"""

    # Group meetings by date
    by_date = defaultdict(list)
    for meeting in meetings:
        date = meeting.get('date')
        if date:
            by_date[date].append(meeting)

    # Find dates with multiple meetings
    potential_duplicates = {}

    for date, date_meetings in by_date.items():
        if len(date_meetings) > 1:
            # Analyze each pair
            pairs = []
            for i, m1 in enumerate(date_meetings):
                for m2 in date_meetings[i+1:]:
                    similarity = calculate_similarity(m1, m2)
                    if similarity > 10:  # Only report if some similarity
                        pairs.append({
                            'meeting1': m1,
                            'meeting2': m2,
                            'similarity': similarity,
                            'recommendation': 'merge' if similarity > 30 else 'review'
                        })

            if pairs:
                potential_duplicates[date] = {
                    'count': len(date_meetings),
                    'meetings': date_meetings,
                    'pairs': pairs
                }

    return potential_duplicates

def main():
    """Main execution function"""
    print("🔍 Analyserer møter for duplikater...")
    print()

    # Load meetings data
    meetings_data = load_json(MEETINGS_JSON)
    meetings = meetings_data['meetings']

    # Analyze for duplicates
    duplicates = analyze_duplicates(meetings)

    if not duplicates:
        print("✅ Ingen åpenbare duplikater funnet.")
        return

    print(f"{'='*80}")
    print(f"POTENSIELLE DUPLIKATER")
    print(f"{'='*80}")
    print()

    # Display results
    for date, data in sorted(duplicates.items()):
        print(f"📅 {date} - {data['count']} møter")
        print()

        # List all meetings on this date
        for i, meeting in enumerate(data['meetings'], 1):
            print(f"   {i}. {meeting['title'][:60]}")
            print(f"      ID: {meeting['id']}")
            print(f"      Deltakere: {meeting.get('participant_count', 0)}")
            print(f"      Rapport: {'Ja' if meeting.get('report_link') else 'Nei'}")
            if meeting.get('report_link'):
                filename = Path(meeting['report_link']).name
                print(f"              {filename[:60]}")
            print()

        # Show similarity analysis
        print("   LIKHETSSCORE:")
        for pair in data['pairs']:
            m1_title = pair['meeting1']['title'][:40]
            m2_title = pair['meeting2']['title'][:40]
            score = pair['similarity']
            rec = pair['recommendation']

            icon = "🔀" if rec == 'merge' else "⚠️"
            print(f"   {icon} {m1_title} ↔️ {m2_title}")
            print(f"      Score: {score:.0f}/100 - {rec.upper()}")

        print()
        print(f"   {'─'*76}")
        print()

    # Summary
    print(f"{'='*80}")
    print(f"SAMMENDRAG")
    print(f"{'='*80}")
    print()

    total_dates_with_duplicates = len(duplicates)
    total_potential_duplicates = sum(d['count'] for d in duplicates.values())

    print(f"Datoer med multiple møter: {total_dates_with_duplicates}")
    print(f"Totalt møter på disse datoene: {total_potential_duplicates}")
    print()
    print("ANBEFALINGER:")
    print()
    print("1. 🔀 MERGE - Høy sannsynlighet for at det er samme møte")
    print("   → Slå sammen møtene, kombiner data")
    print()
    print("2. ⚠️  REVIEW - Kan være separate møter samme dag")
    print("   → Verifiser med kalender/e-post")
    print()
    print("NESTE STEG:")
    print("- Sjekk møtenotater for å bekrefte")
    print("- Sjekk kalender for eksakt tidspunkt")
    print("- Slå sammen hvis samme møte")
    print("- Oppdater titler hvis separate møter")

if __name__ == '__main__':
    main()
