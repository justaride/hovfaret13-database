#!/usr/bin/env python3
"""
Fase 12.3: Add remaining meetings from unknown-date files
"""

import json
from datetime import datetime
from pathlib import Path

def main():
    meetings_path = Path("/Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/data/meetings.json")

    with open(meetings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_meetings = [
        # 1. 2023-06-27 - Første store strategimøte
        {
            "id": "m_2023-06-27_strategimote_hovfaret_13",
            "date": "2023-06-27",
            "title": "Strategimøte Hovfaret 13 - Økologisk restaurering og sirkulær stedsutvikling",
            "organizer": "gabriel@naturalstate.no",
            "location": "Hovfaret 13",
            "participant_count": 4,
            "participants": [
                {"name": "Einar Holthe", "organization": "Natural State AS", "email": "einar@naturalstate.no"},
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Eirik", "organization": "Natural State AS", "email": None, "role": "Naturforvalter"},
                {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS", "email": "andreas@urbania.no"}
            ],
            "topics_discussed": [
                "Rivningsvedtaket og politisk strategi",
                "Økologisk restaurering av tomten",
                "Våtmark og biologisk mangfold ved Hoffselva",
                "Sirkulær stedsutvikling som konsept",
                "Allianse-bygging med beslutningstakere",
                "Visuell kommunikasjon og presentasjon"
            ],
            "decisions": [
                "Bygget skal beholdes og transformeres, ikke rives",
                "Fokus på økologisk restaurering av kantsonen langs elven",
                "Sirkulære prinsipper skal gjennomsyre hele prosjektet",
                "Diplomatisk tilnærming til beslutningstakere er avgjørende",
                "Prosjektet skal bli et utstillingsvindu for bærekraftig byutvikling"
            ],
            "action_items": [
                {"task": "Dokumentere biologisk mangfold på tomten", "responsible": "Eirik", "status": "pending"},
                {"task": "Lage skjøtselsplan for våtmarksystem", "responsible": "Eirik", "status": "pending"},
                {"task": "Utvikle visuell kommunikasjon", "responsible": "Gabriel", "status": "pending"},
                {"task": "Bygge allianser med lokale aktører", "responsible": "Team", "status": "pending"}
            ],
            "report": {
                "summary": "Første omfattende strategimøte for Hovfaret 13-prosjektet. Teamet - Einar, Gabriel, Eirik (naturforvalter) og Andreas - etablerer grunnleggende strategi: bygget skal beholdes gjennom overbevisende argumentasjon om bærekraft, sirkulær økonomi og økologisk verdi. Møtet markerer starten på Natural States involvering som rådgiver på stedsutvikling og bærekraft. Diskuterte detaljert hvordan området kan restaureres økologisk med fokus på våtmark langs Hoffselva.",
                "discussion": [
                    {
                        "heading": "Strategisk retning mot rivningsvedtak",
                        "content": "Andreas: 'Vi har jo gått inn for å beholde bygget... det høres jo ikke logisk ut å rive. Vi har jo jobbet med dette i 7 år nå.' Strategien er å overbevise beslutningstakere om at transformasjon er veien å gå. Det krever diplomatisk klokskap og å forstå at alle egentlig vil det beste for området."
                    },
                    {
                        "heading": "Økologisk restaurering",
                        "content": "Eirik presenterte plan for økologisk restaurering av tomten. Siden tomten ligger langs Hoffselva, er det en våtmarkstype med høy verdi for biologisk mangfold. Foreslår rewilding-prosess over noen år for å gjenskape naturlig habitat. Kartlegging av eksisterende biomangfold er første steg."
                    },
                    {
                        "heading": "Sirkulær stedsutvikling",
                        "content": "Einar: 'Vi må tenke helhetlig. Se bygget i sammenheng med landskapet... Det kan bli et signalprosjekt for framtidens bygging.' Sirkulære prinsipper inkluderer gjenbruk av materialer, lokale kretsløp for energi og vann, og design for lang levetid."
                    },
                    {
                        "heading": "Programmering og innhold",
                        "content": "Diskuterte mulige funksjoner: kontor, servering, aktive førsteetasjer. Andreas nevnte referansen Bosco Verticale i Milano som inspirasjon for grønt bygg. Fokus på møtet mellom bygg og landskap."
                    },
                    {
                        "heading": "Kommunikasjon og allianser",
                        "content": "Einar: 'Hovedmålet er å bygge allianser, arrangere dialogmøter der vi presenterer de gode utviklingsplanene.' Viktig å skape entusiasme uten å virke konfronterende. Andreas: 'Vi må stå for det vi mener er riktig. Ikke la oss presse til kompromisser vi ikke kan leve med.'"
                    }
                ],
                "quotes": [
                    "Det å rive det bygget ville vært ødeleggende for hele området, økologisk og sosialt. Det er hovedpoenget.",
                    "Vi må vise at sirkulære prinsipper fungerer i praksis. At det er mulig å beskrive og måle bærekraft på alle nivåer.",
                    "La oss ta den fighten. Stå opp for den.",
                    "Dette kan bli et fyrtårn for framtidens bygg."
                ],
                "context": "Dette møtet er det tidligste dokumenterte strategimøtet i prosjektet (2023). Det etablerer grunnprinsippene som fortsatt gjelder: transformasjon over riving, økologisk restaurering, sirkulær økonomi, og diplomatisk tilnærming. Interessant at Eirik (naturforvalter) var med tidlig - viser fokus på naturverdier fra start.",
                "metadata": {
                    "source": "transcript",
                    "source_file": "Mtereferat---Hovfaret-13.md",
                    "word_count": 600,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "Mtereferat---Hovfaret-13.md"
        },

        # 2. 2024-06-27 - Sirkulær økonomi og strategi
        {
            "id": "m_2024-06-27_sirkular_okonomi_strategi",
            "date": "2024-06-27",
            "title": "Sirkulær økonomi - Strateginotat og slides",
            "organizer": "gabriel@naturalstate.no",
            "location": "Natural State kontor",
            "participant_count": 3,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Einar Holthe", "organization": "Natural State AS", "email": "einar@naturalstate.no"},
                {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS", "email": "andreas@urbania.no"}
            ],
            "topics_discussed": [
                "Sirkulær økonomi som grunnpremiss",
                "Slide-innhold for konseptskisse",
                "11 strategiske hovedpunkter",
                "Hovfaret 13 som fyrtårn for sirkulær stedsutvikling"
            ],
            "decisions": [
                "Sirkulær økonomi skal være tydelig i konseptskissen",
                "Fire slides om sirkulær stedsutvikling skal utvikles",
                "Prosjektet posisjoneres som mulig katalysator for sirkulær områdeutvikling"
            ],
            "action_items": [
                {"task": "Ferdigstille slides om sirkulær økonomi", "responsible": "Gabriel", "status": "pending"},
                {"task": "Innarbeide sirkulære prinsipper i konseptskisse", "responsible": "Natural State", "status": "pending"}
            ],
            "report": {
                "summary": "Arbeidsmøte for å utvikle innhold om sirkulær økonomi til konseptskissen. Etablerte 11 strategiske hovedpunkter og fire slides som posisjonerer Hovfaret 13 som et 'fyrtårn for sirkulær stedsutvikling'. Fokus på å kombinere Natural States kompetanse på sirkulære strategier med prosjektets konkrete muligheter.",
                "discussion": [
                    {
                        "heading": "De 11 strategiske punktene",
                        "content": "1. Jobbe strategisk for å omgjøre rivningsvedtaket. 2. Bygge allianser med nøkkelaktører. 3. Utvikle helhetlig plan for økologisk restaurering. 4. Kartlegge stedets økologiske kvaliteter. 5. Skape overbevisende visuell kommunikasjon. 6. Utforske innovative løsninger (ref: Bosco Verticale). 7. Utvikle attraktiv programmering. 8. Koble energi- og materialbruk til økologisk strategi. 9. Jobbe tverrfaglig. 10. Sette tydelige milepæler. 11. Bruke Hovfaret 13 som fyrtårn."
                    },
                    {
                        "heading": "Slide-konsepter",
                        "content": "Slide 1: Hovfaret 13 som fyrtårn for sirkulær stedsutvikling - ambisjon, samarbeid, visjon. Slide 2: Sirkulære strategier - bevaring, ressursutnyttelse, delingstjenester, lokal produksjon. Slide 3: Sirkulære verdikjeder - nettverk, samarbeid, eksperimentering, partnerskap. Slide 4: På vei mot sirkulær bydel - katalysator for områdeutvikling, regional klynge."
                    }
                ],
                "quotes": [
                    "Ved å kombinere Natural States kompetanse på sirkulære strategier med prosjektets konkrete muligheter, kan Hovfaret 13 bli et utstillingsvindu for 'sirkulær stedsutvikling' i praksis."
                ],
                "context": "Dette møtet produserte konkret innhold til konseptskissen. De 11 punktene og fire slidene representerer kjernen i prosjektets bærekraftsargumentasjon. Dokumentet viser hvordan Natural State og Urbania samarbeider om å posisjonere prosjektet.",
                "metadata": {
                    "source": "working_document",
                    "source_files": ["27-JUNI TANKER.md", "MØTE 27JUNI.md"],
                    "word_count": 350,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "27-JUNI TANKER.md"
        },

        # 3. 2025-03-04 - Trym og Einar Vill Energi
        {
            "id": "m_2025-03-04_trym_einar_vill_energi",
            "date": "2025-03-04",
            "title": "Trym og Einar - Vill Energi og klimarapporter",
            "organizer": "gabriel@naturalstate.no",
            "location": "Natural State kontor",
            "participant_count": 3,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Trym", "organization": "Natural State AS", "email": "trym@naturalstate.no"},
                {"name": "Einar Holthe", "organization": "Natural State AS", "email": "einar@naturalstate.no"}
            ],
            "topics_discussed": [
                "Vill Energi-leveranse og tilbud",
                "Energikartlegging vs klimagassregnskap",
                "Tre scenarier for klimaberegning",
                "Klimarisikovurdering og taksonomi",
                "Nabotomtens miljødata"
            ],
            "decisions": [
                "Energikartlegging og klimagassregnskap er de to viktigste leveransene",
                "Klimarisikovurdering basert på taksonomi droppes - gjøres internt isteden",
                "Tre scenarier: ASIS, ASIS+3 etasjer, rive og bygge nytt",
                "All kommunikasjon med Vill Energi skal gå gjennom Trym"
            ],
            "action_items": [
                {"task": "Ringe Petter (Vill Energi) og avklare leveranser", "responsible": "Trym", "status": "pending"},
                {"task": "Få nytt tilbud kun for energikartlegging og klimagassregnskap", "responsible": "Trym", "status": "pending"},
                {"task": "Lage intern klimarisikovurdering basert på nabotomtdata", "responsible": "Gabriel/Einar", "status": "pending"}
            ],
            "report": {
                "summary": "Teknisk arbeidsmøte om Vill Energi-leveransen. Teamet avklarer at de to viktigste rapportene er energikartlegging (viser at bygget er 'godt nok') og klimagassregnskap (viser kostnaden ved riving). Klimarisikovurdering basert på EU-taksonomi droppes - for komplisert og gir ikke det politiske verktøyet som trengs. Isteden skal Natural State lage intern vurdering basert på nabotomtens miljødata.",
                "discussion": [
                    {
                        "heading": "De tre nødvendige leveransene",
                        "content": "Speaker 1: 'Det vi vil ha er en energikartlegging som sier noe om energi i hele prosjektet. At bygget er godt nok.' Speaker 2 avklarer: energikartlegging viser at bygget har gode energiegenskaper, klimagassregnskap viser klimakostnaden ved riving og gjenoppbygging."
                    },
                    {
                        "heading": "Tre scenarier for klimagassregnskap",
                        "content": "1. ASIS - bygget som det er i dag (grunnmodell). 2. ASIS pluss tre etasjer - påbygg. 3. Rive og bygge nytt med samme volum. Viktig poeng: ved å sammenligne disse får vi 'klimakostnaden ved å gjenoppbygge tilsvarende bygg'."
                    },
                    {
                        "heading": "Droppe taksonomi-rapporten",
                        "content": "Teamet diskuterer at klimarisikovurdering basert på EU-taksonomi ikke gir det de trenger for politisk behandling. 'Jeg ser jo ikke helt hvordan du skal få det til' (som bygningsingeniør). Beslutter å lage enklere intern vurdering isteden."
                    },
                    {
                        "heading": "Nabotomtens miljødata",
                        "content": "Nabotomten har omfattende miljøundersøkelser som kan brukes. 'Det er jo et steinkast unna.' Denne dataen kan brukes til naturrisiko-vurdering uten å bestille ny rapport."
                    }
                ],
                "quotes": [
                    "Bygge på tre etasjer på dagens bygg kan du kun gjøre hvis du har en Enova-kartlegging som viser at dagens bygg er ok.",
                    "Klimakostnaden ved å gjenoppbygge tilsvarende bygg her er dette. Det er helt avsindig.",
                    "Jeg tror ikke vi får det vi trenger [fra taksonomi-rapport]. Det vi burde få er ikke det vi får."
                ],
                "context": "Dette møtet viser den tekniske planleggingen bak bærekraftsdokumentasjonen. Vill Energi er leverandør, men teamet er kritisk til deler av deres tilbud. Beslutningen om å droppe taksonomi-rapporten og lage intern vurdering viser pragmatisk tilnærming.",
                "metadata": {
                    "source": "transcript",
                    "source_file": "trym-og-einar-vill-energi-4-mars.md",
                    "word_count": 400,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "trym-og-einar-vill-energi-4-mars.md"
        },

        # 4. 2025-03-07 - Urbania prosess (STORT MØTE)
        {
            "id": "m_2025-03-07_urbania_prosess_workshop",
            "date": "2025-03-07",
            "title": "Urbania prosess - Dispensasjonsstrategi og leietakerdialog",
            "organizer": "gabriel@naturalstate.no",
            "location": "Natural State kontor / Hovfaret 13",
            "participant_count": 5,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Einar Holthe", "organization": "Natural State AS", "email": "einar@naturalstate.no"},
                {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS", "email": "andreas@urbania.no"},
                {"name": "Knut Halvor", "organization": "Ekstern rådgiver", "email": None},
                {"name": "Teammedlem", "organization": "Natural State AS", "email": None}
            ],
            "topics_discussed": [
                "Dispensasjonsstrategi og juridisk grunnlag",
                "Leietakerdialog og studiokontorkonsept",
                "Bruksendring for første etasje",
                "Sosial bærekraft og frivillighet",
                "Møte med bydelen (Bente Otto)",
                "Nettside og offentlig lansering",
                "Grønnvasking og kommunikasjonsfarer"
            ],
            "decisions": [
                "Dispensasjon skal argumenteres på to grunnlag: vesentlige fordeler + KPA §6 unntak",
                "Leietakere kategoriseres etter kompatibilitet med studiokontorkonsept",
                "Bruksendring for første etasje ventes til etter bydelsmøte",
                "Møte med Bente Otto (bydelen) prioriteres før offentlig lansering",
                "Max Sibert (lab-leietaker) avvises pga byggeprosess-inkompatibilitet",
                "Nettside lanseres etter administrative møter"
            ],
            "action_items": [
                {"task": "Møte med Bente Otto (bydelen)", "responsible": "Andreas/Gabriel", "status": "pending"},
                {"task": "Kategorisere leietakere etter studiokontorkompatibilitet", "responsible": "Team", "status": "pending"},
                {"task": "Avvise Max Sibert høflig", "responsible": "Andreas", "status": "pending"},
                {"task": "Ferdigstille nettside", "responsible": "Team", "status": "pending"},
                {"task": "Kontakte Tore Strandskog (politiker)", "responsible": "Gabriel", "status": "pending"},
                {"task": "Snakke med Nabolagsfabrikken", "responsible": "Team", "status": "pending"}
            ],
            "report": {
                "summary": "Omfattende prosessmøte med hele teamet inkludert Knut Halvor som juridisk/strategisk rådgiver. Møtet dekket alt fra teknisk dispensasjonsstrategi til leietakerhåndtering og kommunikasjonsrisiko. Viktig beslutning: møte med bydelen (Bente Otto) skal tas FØR offentlig lansering. Knut Halvor bidro med juridisk perspektiv på dispensasjonsgrunnlag. Diskuterte også grønnvasking-debatten og viktigheten av å være 'superdiplomatiske'.",
                "discussion": [
                    {
                        "heading": "Dispensasjonsstrategi",
                        "content": "Knut Halvor: 'Hovedregelen på DISP er at fordelen er vesentlig større enn ulempene. Det må vi bygge opp en argumentasjon rundt.' To parallelle spor: 1) Dispensasjon fra gjeldende plan (vesentlighetskrav), 2) KPA §6 som åpner for avvik ved sosial bærekraft og stedsutvikling. Andreas: 'Vi må hjelpe saksbehandlerne til å forstå hva som har skjedd og finne grunnlag for å gi godkjenning.'"
                    },
                    {
                        "heading": "Leietakerdialog og studiokontorer",
                        "content": "Gjennomgang av alle leietakere med kompatibilitetsvurdering. Noen vil samle seg i studiokonsept, andre vil ikke. HK-arkitekter ville ikke la teamet ta bilder - 'det var det nivået de var på'. Mål: frigjøre areal ved å rasjonalisere leietakere til en eller to etasjer med studiokontorstruktur, øke kvadratmeterverdi."
                    },
                    {
                        "heading": "Avvisning av Max Sibert",
                        "content": "Lab-leietaker Max Sibert må avvises pga inkompatibilitet med byggeprosess. Gabriel: 'Det å bygge med vibrasjon og støy... han har temperatur- og fuktighetsstyrt lab. Dette kommer ikke til å gå.' Andreas må gi beskjed om at 'dette er byggeutvikling, det skal bygges og pigges.'"
                    },
                    {
                        "heading": "Sosial bærekraft og frivillighet",
                        "content": "Kartlegging av lokale aktører: Ullern frivillighetssentral (100 års dispensasjon, trenger lokaler), Skøyen Aktivitetssenter (masse aktiviteter, mangler kapasitet), Kirkens SOS (ikke utadrettet), Nabolagsfabrikken. Potensial for aktiviteter i første etasje og parkeringskjeller (idrett uten takhøydekrav)."
                    },
                    {
                        "heading": "Grønnvasking og kommunikasjonsrisiko",
                        "content": "Knut Halvor: 'Det er med sosialvasking og grønnvasking... det må være substans bak.' Einar: 'En gavete bydelen, da har jeg tatt full fyr' - referanse til OMA-debatten om Oslo Urban Week. Må være 'superdiplomatiske', ikke si 'her kommer vi og skal redde dere'. Radikalt prosjekttransparans, men moderat og respektfullt."
                    },
                    {
                        "heading": "Politisk strategi",
                        "content": "To nivåer: 1) Administrativt (Bente Otto) - avklare bydelens behov. 2) Politisk (Tore Strandskog i byutviklingskomiteen) - forankre saken. Tore Strandskog svarer ikke på henvendelser. Plan: gi to sjanser, deretter media og presse. 'Da får vi Aftenposten og alle til å ta dette opp.'"
                    }
                ],
                "quotes": [
                    "Hvis du klarer å bygge opp entusiasme hos saksbehandler i Plan og bygg, så er det utrolig hva du kan få til.",
                    "Vi må hele veien tenke til å styrke vår argumentasjon... både vesentlighetsbegrepet og KPA §6.",
                    "Sosialvasking og grønnvasking... det må være substans bak, ikke bare ord.",
                    "Vi skal være superdiplomatiske, ikke si at her kommer vi og skal redde dere."
                ],
                "context": "Dette er et av de mest omfattende møtene i prosjektet - over 55KB transkripsjon. Det viser kompleksiteten i prosessen: juridisk strategi, leietakerhåndtering, politisk navigering, og kommunikasjonsrisiko. Knut Halvors deltakelse gir juridisk tyngde. Møtet skjer i en kritisk fase før offentlig lansering.",
                "metadata": {
                    "source": "transcript",
                    "source_file": "Urbania-prosess-7-MARS.md",
                    "word_count": 800,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "Urbania-prosess-7-MARS.md"
        },

        # 5. 2025-08-22 - Andreas kjapp prat
        {
            "id": "m_2025-08-22_andreas_energiklassifisering",
            "date": "2025-08-22",
            "title": "Andreas - Energiklassifisering og grønn finansiering",
            "organizer": "gabriel@naturalstate.no",
            "location": "Hovfaret 13",
            "participant_count": 3,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS", "email": "andreas@urbania.no"},
                {"name": "Trym", "organization": "Natural State AS", "email": "trym@naturalstate.no"}
            ],
            "topics_discussed": [
                "Grønn belåning og energiklassifisering",
                "Faktisk energiforbruk vs beregnet",
                "Takstmannvurdering",
                "Møte for avklaring"
            ],
            "decisions": [
                "Møte avtales mandag 14:30 med Andreas og Trym",
                "Trym skal forklare energiklassifiseringsprosessen",
                "Diskrepans mellom reelt og beregnet energiforbruk skal avklares"
            ],
            "action_items": [
                {"task": "Avtale møte mandag 14:30", "responsible": "Gabriel", "status": "pending"},
                {"task": "Forberede energiklassifiseringsforklaring", "responsible": "Trym", "status": "pending"}
            ],
            "report": {
                "summary": "Kort samtale mellom Gabriel og Andreas om energiklassifisering og grønn finansiering. Andreas etterlyser avklaring på byggets faktiske energiklassifisering vs det som står i rapporter. Bygget bruker faktisk mindre energi enn beregnet - 'vi bruker mindre energi enn kanskje nyere bygg'. Avtaler møte med Trym for å rydde opp i dette.",
                "discussion": [
                    {
                        "heading": "Grønn belåning",
                        "content": "Andreas: 'I dag er grønn belåning blitt veldig, veldig [viktig]. Dette bygget er jo på vei til å bli grønt.' Diskuterer mulighet for forbehold i bankavtale - at energiklassifisering kan forbedres med lette tiltak, og da slår annen rentesats inn."
                    },
                    {
                        "heading": "Reelt vs beregnet energiforbruk",
                        "content": "Andreas har dokumentert lavere energiforbruk gjennom flere år enn det Trym/Vill Energi legger til grunn i beregningene. Har også investert 500.000 i frekvensregulerte vifter som ikke er reflektert. 'Bygget er et veldig bedre bygg i form enn et tilsvarende bygg med samme materialbruk.'"
                    }
                ],
                "quotes": [
                    "Dette bygget er jo på vei til å bli grønt.",
                    "Vi bruker mindre energi enn kanskje nyere bygg.",
                    "Jeg etterlyser hva slags klassifisering har bygget i dag, reelt."
                ],
                "context": "Kort operativ samtale som viser Andreas' engasjement i de tekniske detaljene. Grønn finansiering blir stadig viktigere, og Andreas vil ha dokumentasjon som reflekterer byggets faktiske ytelse, ikke teoretiske beregninger.",
                "metadata": {
                    "source": "transcript",
                    "source_files": ["22-august-kjapp-prat-med-andreas-og-gabriel.md", "ANDREAS-KJAPP-PRAT-22-AUGUST-2025.md", "andreas-kjapp-prat-urbania-22-August-m4a.md"],
                    "word_count": 250,
                    "consolidated_date": "2025-12-02",
                    "note": "Tre versjoner av samme samtale konsolidert"
                }
            },
            "source_file": "22-august-kjapp-prat-med-andreas-og-gabriel.md"
        }
    ]

    # Add meetings
    existing_ids = {m['id'] for m in data['meetings']}

    added = 0
    for meeting in new_meetings:
        if meeting['id'] not in existing_ids:
            data['meetings'].append(meeting)
            added += 1
            print(f"Added: {meeting['date']} - {meeting['title']}")
        else:
            print(f"Skipped (exists): {meeting['id']}")

    # Update metadata
    data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    data['metadata']['total_meetings'] = len(data['meetings'])
    data['metadata']['fase_12_3_enrichment'] = {
        'date': datetime.now().isoformat(),
        'meetings_added': added,
        'source': 'Downloads/Møter etter prompt Hovfaret 13/',
        'phase': '12.3',
        'note': 'Unknown-date files analyzed and dated'
    }

    # Sort by date
    data['meetings'].sort(key=lambda x: x['date'])

    # Write back
    with open(meetings_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Added {added} new meetings to meetings.json")
    print(f"Total meetings now: {len(data['meetings'])}")

if __name__ == '__main__':
    main()
