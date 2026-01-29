#!/usr/bin/env python3
"""
Apply meeting data retrieved from Claude Web (Gmail, Calendar, Drive).
"""

import json
from datetime import datetime

MEETINGS_PATH = "data/meetings.json"

# Data from Claude Web search
CLAUDE_WEB_DATA = [
    {
        "date": "2024-06-03",
        "title": "Hovfaret 13 Stand Up",
        "time": "12:30-13:00",
        "participants": [
            {"name": "Einar Holthe", "organization": "Natural State AS"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Kort statusoppdatering på prosjektet",
            "Koordinering av pågående arbeid",
            "Planlegging av neste steg"
        ],
        "report": {
            "summary": "Kort intern koordineringsmøte for å synkronisere arbeidet mellom Einar og Gabriel på Hovfaret 13-prosjektet.",
            "context": "Rutine standup-møte mellom Natural State-team",
            "discussion": [
                {"heading": "Møtetype", "content": "Intern status og koordinering"}
            ]
        }
    },
    {
        "date": "2024-06-27",
        "title": "Urbania presentasjon Konseptskisse 2.0",
        "time": "13:00-14:30",
        "location": "Natural State kontor, St. Halvards gate 33",
        "organizer": "helene@naturalstate.no",
        "participants": [
            {"name": "Einar Holthe", "organization": "Natural State AS"},
            {"name": "Helene", "organization": "Natural State AS"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"},
            {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS"},
            {"name": "Thomas Thorsnes", "organization": "R21 Arkitekter"}
        ],
        "topics_discussed": [
            "Presentasjon av revidert konseptskisse versjon 2.0",
            "Feedback på første konseptskisse",
            "Videreutvikling av transformasjonsidé",
            "Tekniske aspekter ved transformasjon"
        ],
        "report": {
            "summary": "Presentasjon av forbedret og revidert konseptskisse (versjon 2.0) som bygget på feedback fra første versjon. Møtet markerte en iterativ utvikling av transformasjonsideen.",
            "context": "Dette var en viktig milepæl hvor den reviderte konseptskissen ble presentert. At Helene organiserte møtet tyder på at flere personer i Natural State nå var involvert.",
            "discussion": [
                {"heading": "Konseptskisse 2.0", "content": "Revidert versjon basert på feedback fra første presentasjon"},
                {"heading": "Transformasjonsidé", "content": "Tekniske og arkitektoniske aspekter ved transformasjon av eksisterende bygg"}
            ]
        }
    },
    {
        "date": "2024-09-09",
        "title": "Lørenveien + Hovfaret 13",
        "time": "08:30-09:00",
        "participants": [
            {"name": "Einar Holthe", "organization": "Natural State AS"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Status på Lørenveien-prosjektet",
            "Status på Hovfaret 13",
            "Koordinering mellom parallelle prosjekter",
            "Ressursfordeling"
        ],
        "report": {
            "summary": "Intern koordineringsmøte mellom Einar og Gabriel for å diskutere status på både Lørenveien og Hovfaret 13-prosjektene. Natural State jobbet med flere prosjekter samtidig og trengte å koordinere ressurser.",
            "discussion": [
                {"heading": "Parallelle prosjekter", "content": "Koordinering mellom Lørenveien og Hovfaret 13"},
                {"heading": "Ressursfordeling", "content": "Fordeling av Natural State ressurser mellom prosjektene"}
            ]
        }
    },
    {
        "date": "2024-09-19",
        "title": "Laara / Gabriel - A closer look - Hovfaret 13",
        "time": "11:00-12:00",
        "location": "Google Meet (meet.google.com/ejo-mimp-vkd)",
        "participants": [
            {"name": "Laara Matsen", "organization": "Natural State AS"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Prosjektets status og utviklingsfase",
            "Behov for kommunikasjonsstrategi",
            "Planlegging av nettside",
            "Kommunikasjonsbehov for reguleringsprosess"
        ],
        "decisions": [
            "Laara ble involvert i kommunikasjonsarbeidet",
            "Start på planlegging av kommunikasjonsstrategi",
            "Nettsideutvikling skulle påbegynnes"
        ],
        "report": {
            "summary": "Første møte mellom Gabriel og Laara (kommunikasjonsansvarlig i Natural State) for å introdusere Hovfaret 13-prosjektet og diskutere behov for kommunikasjonsplan, nettside og strategi for reguleringsprosessen.",
            "context": "Dette møtet markerte overgangen til en ny fase hvor prosjektet trengte profesjonell kommunikasjonsstøtte. Det signaliserte at prosjektet var modent nok til å kreve ekstern kommunikasjon.",
            "discussion": [
                {"heading": "Kommunikasjonsstrategi", "content": "Behov for profesjonell kommunikasjonsplan"},
                {"heading": "Nettside", "content": "Planlegging av prosjektnettside påbegynt"}
            ],
            "quotes": [
                "Hey Laara. Inviting you for a meeting to look at our Project Hovfaret 13, that is going into development strategy phase, where we need to look at a coms plan, developing a website etc."
            ]
        }
    },
    {
        "date": "2024-09-24",
        "title": "Laara / Gabriel URBANIA HOVFARET 13 COMS TALK",
        "time": "15:00-16:00",
        "participants": [
            {"name": "Laara Matsen", "organization": "Natural State AS"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Videre utvikling av kommunikasjonsstrategi",
            "Nettside-planlegging",
            "Budskap og posisjonering",
            "Timeline for kommunikasjonsarbeid"
        ],
        "report": {
            "summary": "Oppfølgingsmøte etter møtet 19. september. Laara og Gabriel fortsatte planleggingen av kommunikasjonsstrategien og nettsideutviklingen.",
            "discussion": [
                {"heading": "Kommunikasjonsstrategi", "content": "Videre utvikling av budskap og posisjonering"},
                {"heading": "Nettside", "content": "Planlegging av innhold og struktur"}
            ]
        }
    },
    {
        "date": "2024-09-27",
        "title": "Urbania/R21/Natural State - Hovfaret 13",
        "time": "08:30-10:00",
        "location": "Natural State kontor, St. Halvards gate 33",
        "organizer": "gabriel@naturalstate.no",
        "participants": [
            {"name": "Einar Holthe", "organization": "Natural State AS"},
            {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS"},
            {"name": "Thomas Thorsnes", "organization": "R21 Arkitekter"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"},
            {"name": "Andrea", "organization": "R21 Arkitekter"}
        ],
        "topics_discussed": [
            "Gjennomgang av R21s arkitekttegninger",
            "Initiering av interessentdialog",
            "Planlegging av leietakersamtaler",
            "Strategi for kommunal dialog",
            "Tekniske aspekter ved transformasjon"
        ],
        "decisions": [
            "Starte planlegging av interessentdialog",
            "R21s tegninger godkjent for videre arbeid",
            "Strategi for ekstern engasjement etablert"
        ],
        "report": {
            "summary": "Omfattende prosjektgruppemøte hvor R21s arkitekttegninger ble gjennomgått og hvor planlegging av interessentdialog ble initiert. Møtet markerte overgangen til en mer eksternt orientert fase av prosjektet.",
            "context": "Kritisk møte som markerte overgangen fra intern utvikling til ekstern engasjement med potensielle leietakere og andre interessenter. Dette var første gang Andrea fra R21 deltok, noe som tyder på økt kapasitet fra arkitektfirmaet.",
            "discussion": [
                {"heading": "Arkitekttegninger", "content": "Gjennomgang og godkjenning av R21s tegninger"},
                {"heading": "Interessentdialog", "content": "Initiering av dialog med leietakere og andre interessenter"},
                {"heading": "Ekstern fase", "content": "Overgang til mer eksternt orientert prosjektfase"}
            ]
        }
    },
    {
        "date": "2024-10-31",
        "title": "Hovfaret 13 - Nettside Workshop",
        "time": "10:30-12:30",
        "location": "Natural State kontor",
        "participants": [
            {"name": "Laara Matsen", "organization": "Natural State AS"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"},
            {"name": "Severin", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Nettsidestruktur og design",
            "Innhold og budskap",
            "Visuell identitet",
            "Teknisk plattform (Squarespace)",
            "Timeline for ferdigstillelse"
        ],
        "action_items": [
            "Utvikle første utkast til nettside",
            "Samle innhold og bilder",
            "Koordinere med designbyrå"
        ],
        "report": {
            "summary": "Dedikert 2-timers workshop for å utvikle nettsiden for Hovfaret 13. Laara, Gabriel og Severin jobbet med struktur, innhold og visuell identitet.",
            "discussion": [
                {"heading": "Workshop format", "content": "2-timers dedikert arbeidsmøte"},
                {"heading": "Nettside", "content": "Struktur, design og innhold for prosjektnettsiden"}
            ]
        }
    },
    {
        "date": "2024-11-06",
        "title": "Rask Avklaring. Hovfaret 13 elementer",
        "time": "08:30-09:00",
        "participants": [
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Avklaring av ulike prosjektelementer",
            "Koordinering av leveranser",
            "Forberedelser til kommende møter"
        ],
        "report": {
            "summary": "Gabriel satte av tid til intern avklaring og koordinering av ulike elementer i prosjektet. Solo arbeidsmøte for å strukturere videre arbeid.",
            "discussion": [
                {"heading": "Intern koordinering", "content": "Solo arbeidsmøte for å strukturere prosjektelementer"}
            ]
        }
    },
    {
        "date": "2024-11-12",
        "title": "Hovfaret 13 Website (framework)",
        "time": "09:00-11:00",
        "participants": [
            {"name": "Gabriel Freeman", "organization": "Natural State AS"},
            {"name": "Severin", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Teknisk rammeverk for nettsiden",
            "Squarespace-oppsett",
            "Struktur og navigasjon",
            "Integrasjoner"
        ],
        "action_items": [
            "Implementere teknisk løsning",
            "Sette opp domene",
            "Forberede for innholdsinnlegging"
        ],
        "report": {
            "summary": "To-timers arbeidsmøte mellom Gabriel og Severin for å jobbe med det tekniske rammeverket for nettsiden. Fokus på Squarespace-implementasjon og teknisk struktur.",
            "discussion": [
                {"heading": "Teknisk implementasjon", "content": "Squarespace-oppsett og teknisk rammeverk"},
                {"heading": "Struktur", "content": "Navigasjon og integrasjoner"}
            ]
        }
    },
    {
        "date": "2024-12-10",
        "title": "Snakke med Aktør for 1 etg Hovfaret 13",
        "time": "10:00-11:00",
        "participants": [
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Muligheter for servering/kafé i første etasje",
            "Leietakers behov og ønsker",
            "Økonomiske betingelser",
            "Timeline for etablering"
        ],
        "report": {
            "summary": "Gabriel hadde samtale med potensielle aktører for servering/kafédrift i byggets første etasje. Dette var del av strategien om å skape levende førsteetasjer med fellesfunksjoner.",
            "context": "Første etasje skulle ha aktive fellesarealer med restaurant/kafé. Dette var en sonderende samtale med potensielle aktører.",
            "discussion": [
                {"heading": "Førsteetasje aktivering", "content": "Sonderende samtale om servering/kafé muligheter"},
                {"heading": "Aktive fellesarealer", "content": "Strategi for levende førsteetasjer"}
            ]
        }
    },
    {
        "date": "2024-12-11",
        "title": "Befaring Hovfaret 13 - Energikartlegging mm.",
        "time": "09:30-10:30",
        "location": "Hovfaret 13, 0275 Oslo",
        "participants": [
            {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS"},
            {"name": "Petter", "organization": "Vill Energi"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"},
            {"name": "Trym", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Gjennomgang av byggets energisystemer",
            "Eksisterende tekniske anlegg",
            "Energiforbruk og målinger",
            "Oppgraderingsmuligheter",
            "Teknisk tilstand"
        ],
        "decisions": [
            "Vill Energi skulle utarbeide energikartleggingsrapport",
            "Trenger detaljert analyse for bærekraftsdokumentasjon"
        ],
        "action_items": [
            "Petter (Vill Energi) leverer rapport innen 14 dager",
            "Energiberegninger for transformasjon vs. nybygg",
            "Klimagassberegninger"
        ],
        "report": {
            "summary": "Fysisk befaring av Hovfaret 13 med energirådgiver fra Vill Energi. Petter gjennomgikk byggets tekniske anlegg og energisystemer for å kunne utarbeide detaljert energikartlegging. Dette arbeidet var essensielt for å dokumentere bærekraftsgevinstene ved transformasjon.",
            "context": "Kritisk for bærekraftsdokumentasjonen. Energikartleggingen skulle gi grunnlag for å argumentere for transformasjon fremfor riving. Senere analyser viste at faktisk energiforbruk (ca. 600 000 kWh/år) var betydelig lavere enn teoretisk beregning (1 425 000 kWh/år).",
            "discussion": [
                {"heading": "Energisystemer", "content": "Gjennomgang av eksisterende tekniske anlegg og systemer"},
                {"heading": "Energiforbruk", "content": "Kartlegging av faktisk vs. teoretisk energibruk"},
                {"heading": "Bærekraft", "content": "Grunnlag for dokumentasjon av miljøgevinster ved transformasjon"}
            ]
        }
    },
    {
        "date": "2025-01-09",
        "title": "Status Hovfaret 13 web",
        "time": "10:00-10:30",
        "organizer": "laara@naturalstate.no",
        "participants": [
            {"name": "Laara Matsen", "organization": "Natural State AS"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Status på nettsideutvikling",
            "Gjenstående innhold",
            "Timeline for lansering"
        ],
        "report": {
            "summary": "Statusmøte organisert av Laara for å gå gjennom nettsideutviklingen og holde momentum i nettsidearbeidet.",
            "discussion": [
                {"heading": "Nettside status", "content": "Gjennomgang av fremdrift og gjenstående arbeid"}
            ]
        }
    },
    {
        "date": "2025-01-27",
        "title": "viderefakturering hovfaret 13",
        "time": "11:00-11:15",
        "participants": [
            {"name": "Kristian", "organization": "Natural State AS"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Viderefakturering av kostnader til Urbania",
            "Økonomisk oppfølging av prosjektet",
            "Faktureringsrutiner",
            "Budsjettoppfølging"
        ],
        "report": {
            "summary": "Kort møte mellom Gabriel og Kristian (økonomiansvarlig i Natural State) for å koordinere viderefakturering av kostnader relatert til Hovfaret 13-prosjektet. Dette var del av profesjonell prosjektstyring med tydelig skille mellom faglig og økonomisk ansvar.",
            "context": "Natural State måtte håndtere økonomisk administrasjon og fakturering til Urbania for konsulentarbeidet.",
            "discussion": [
                {"heading": "Fakturering", "content": "Koordinering av viderefakturering til Urbania"}
            ]
        }
    },
    {
        "date": "2025-02-11",
        "title": "Miljørisiko kartlegging Hovfaret 13",
        "time": "11:30-12:00",
        "location": "Digitalt møte",
        "organizer": "gabriel@naturalstate.no",
        "participants": [
            {"name": "Knut Halvor Hansen", "organization": "BYKON"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"},
            {"name": "Trym", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Generell info om prosjektet (geografiske forhold, utomhusplan, trær)",
            "Kjente utfordringer",
            "Eksisterende sikkerhetsmål",
            "Kommunens vurdering av risiko",
            "Areal for planlagt påbygg",
            "Geotekniske forhold (Hoffselva/kvikkleire)",
            "Klimarisikoanalyse"
        ],
        "report": {
            "summary": "Teknisk møte for å kartlegge miljørisiko og klimarisikoaspekter ved Hovfaret 13-transformasjonen. Knut Halvor Hansen fra BYKON ledet diskusjonen om risikovurdering i sammenheng med Vill Energis energikartlegging.",
            "context": "Knut Halvor Hansen fra BYKON (byggherrerådgiver) ble involvert, noe som signaliserte at prosjektet gikk inn i en mer teknisk/bygningsfaglig fase. Hoffselva-området har kjente utfordringer med kvikkleire. Hovfaret 13s eksisterende fundament på peler ble sett som en styrke.",
            "discussion": [
                {"heading": "Miljørisiko", "content": "Kartlegging av miljørisiko og klimarisikoaspekter"},
                {"heading": "Geotekniske forhold", "content": "Vurdering av kvikkleire og fundamentering"},
                {"heading": "Bygningsfaglig fase", "content": "Overgang til mer teknisk prosjektfase"}
            ]
        }
    },
    {
        "date": "2025-07-04",
        "title": "Bærekraftsrapport - Hovfaret 13",
        "time": "10:00-12:00",
        "organizer": "linda@naturalstate.no",
        "participants": [
            {"name": "Linda", "organization": "Natural State AS"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Utvikling av omfattende bærekraftsrapport",
            "Klimagassberegninger (transformasjon vs. nybygg)",
            "Energianalyse og oppgraderingsmuligheter",
            "Livssyklus-analyse (LCA)",
            "Sirkulærøkonomi-dokumentasjon",
            "Samfunnsøkonomisk analyse"
        ],
        "decisions": [
            "48% lavere klimagassutslipp ved rehabilitering vs. nybygg",
            "50% reduksjon i energiforbruk mulig",
            "80-90% mindre avfall enn ved riving",
            "Besparelse på 2.549 tonn CO₂-ekvivalenter"
        ],
        "report": {
            "summary": "To-timers arbeidsmøte mellom Gabriel og Linda for å utvikle den omfattende bærekraftsrapporten som skulle dokumentere miljøgevinstene ved transformasjon fremfor riving. Rapporten basert på European Sustainability Reporting Standards (ESRS).",
            "context": "Bærekraftsrapporten var kritisk for å argumentere for unntak fra rivekravet i områdeplanen. Solid dokumentasjon var nødvendig for politisk gjennomførbarhet.",
            "discussion": [
                {"heading": "Klimagassberegninger", "content": "48% lavere utslipp ved rehabilitering vs. nybygg"},
                {"heading": "Energianalyse", "content": "50% reduksjon i energiforbruk mulig (fra 232 til 116 kWh/m²/år)"},
                {"heading": "Avfallsreduksjon", "content": "80-90% mindre avfall enn ved riving"},
                {"heading": "CO₂-besparelse", "content": "Besparelse på 2.549 tonn CO₂-ekvivalenter"}
            ]
        }
    },
    {
        "date": "2025-08-28",
        "title": "Kort Brief om Utviklingsprosess Hovfaret 13",
        "time": "10:00-11:00",
        "organizer": "gabriel@naturalstate.no",
        "participants": [
            {"name": "Nils-Erik Christiansen", "organization": "BER"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"}
        ],
        "topics_discussed": [
            "Overordnet utviklingsprosess for Hovfaret 13",
            "Prosjektets status og timeline",
            "Nøkkelutfordringer og muligheter",
            "Koordinering med andre aktører",
            "Verdivurdering og bankdialog"
        ],
        "report": {
            "summary": "Gabriel briefet Nils-Erik Christiansen fra BER om Hovfaret 13-prosjektets utviklingsprosess. Dette var del av å informere nye aktører som skulle være involvert i finansiering og verdivurdering.",
            "context": "NEC/Nils-Erik Christiansen fra BER ble introdusert til prosjektet. BER er involvert i verdivurdering og bankdialog.",
            "discussion": [
                {"heading": "Utviklingsprosess", "content": "Overordnet gjennomgang av prosjektstatus og timeline"},
                {"heading": "Finansiering", "content": "Introduksjon av BER for verdivurdering og bankdialog"}
            ]
        }
    },
    {
        "date": "2025-09-04",
        "title": "Hovfaret 13, koordinere rammesøknad",
        "time": "13:45-15:30",
        "location": "R21s kontor, Møterom Rådhusgata 21, Oslo",
        "organizer": "thomas@r21.no",
        "participants": [
            {"name": "Thomas Thorsnes", "organization": "R21 Arkitekter"},
            {"name": "Gabriel Freeman", "organization": "Natural State AS"},
            {"name": "Francisco Kocourek", "organization": "R21 Arkitekter"},
            {"name": "Liv W. Thorsnes", "organization": "BSRG landskapsarkitekter"}
        ],
        "topics_discussed": [
            "Koordinering av rammesøknad til kommunen",
            "Arkitektonisk dokumentasjon",
            "Landskapsarkitektur",
            "Tekniske tegninger og spesifikasjoner",
            "Timeline for innsending"
        ],
        "report": {
            "summary": "Kritisk koordineringsmøte hos R21 for å forberede formell rammesøknad til kommunen. Arkitektteamet samordnet dokumentasjon, tegninger og landskapsarkitektur for å kunne sende inn søknad. Dette var et viktig steg mot formalisering av transformasjonsprosjektet.",
            "context": "Dette var et kritisk koordineringsmøte for å forberede rammesøknad til kommunen. At møtet ble holdt hos R21 og organisert av Thomas Thorsnes tyder på at arkitektfirmaet tok en mer ledende rolle i den formelle søknadsprosessen.",
            "discussion": [
                {"heading": "Rammesøknad", "content": "Koordinering av formell søknad til kommunen"},
                {"heading": "Arkitektteam", "content": "Thomas Thorsnes (CEO/partner R21), Francisco Kocourek (R21 arkitekt), Liv W. Thorsnes (BSRG landskapsarkitekter)"},
                {"heading": "Dokumentasjon", "content": "Samordning av tegninger, spesifikasjoner og landskapsarkitektur"}
            ]
        }
    }
]


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_meeting(meetings, date_str):
    for m in meetings:
        if m.get("date") == date_str:
            return m
    return None


def update_meeting(meeting, new_data):
    """Update meeting with new data from Claude Web."""
    # Update time if provided
    if new_data.get("time"):
        meeting["time"] = new_data["time"]

    # Update location if provided
    if new_data.get("location"):
        meeting["location"] = new_data["location"]

    # Update organizer if provided
    if new_data.get("organizer"):
        meeting["organizer"] = new_data["organizer"]

    # Update participants if new data has more
    if new_data.get("participants"):
        if len(new_data["participants"]) > len(meeting.get("participants", [])):
            meeting["participants"] = new_data["participants"]
            meeting["participant_count"] = len(new_data["participants"])

    # Update topics if empty or new has more
    if new_data.get("topics_discussed"):
        if not meeting.get("topics_discussed") or len(new_data["topics_discussed"]) > len(meeting.get("topics_discussed", [])):
            meeting["topics_discussed"] = new_data["topics_discussed"]

    # Update decisions if provided
    if new_data.get("decisions"):
        meeting["decisions"] = new_data["decisions"]

    # Update action items if provided
    if new_data.get("action_items"):
        meeting["action_items"] = new_data["action_items"]

    # Update report if current is empty or new has more content
    if new_data.get("report"):
        current_report = meeting.get("report", {})
        new_report = new_data["report"]

        # Check if current report is empty or has no discussion
        if not current_report or not current_report.get("discussion"):
            meeting["report"] = new_report
        elif new_report.get("discussion") and len(new_report.get("discussion", [])) > len(current_report.get("discussion", [])):
            meeting["report"] = new_report

    # Add metadata
    meeting["report_metadata"] = {
        "enriched_date": datetime.now().isoformat(),
        "source": "claude_web_gmail_calendar_drive",
        "polished": True
    }

    return True


def main():
    print("=== Applying Claude Web Data ===\n")

    data = load_json(MEETINGS_PATH)
    meetings = data.get("meetings", [])

    updated = 0

    for new_data in CLAUDE_WEB_DATA:
        date_str = new_data["date"]
        print(f"Processing {date_str}...")

        meeting = find_meeting(meetings, date_str)

        if meeting:
            if update_meeting(meeting, new_data):
                updated += 1
                print(f"  Updated: {meeting.get('title', 'Unknown')[:50]}")
        else:
            print(f"  Meeting not found for {date_str}")

    # Update metadata
    data["metadata"]["claude_web_enrichment"] = {
        "date": datetime.now().isoformat(),
        "meetings_updated": updated,
        "source": "gmail_calendar_drive"
    }

    save_json(MEETINGS_PATH, data)

    print(f"\n=== Done! Updated {updated} meetings ===")


if __name__ == "__main__":
    main()
