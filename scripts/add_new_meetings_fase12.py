#!/usr/bin/env python3
"""
Fase 12.2: Add 11 new meetings to meetings.json
Based on source files from /Users/gabrielboen/Downloads/Møter etter prompt Hovfaret 13/
"""

import json
from datetime import datetime
from pathlib import Path

def main():
    meetings_path = Path("/Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/data/meetings.json")

    with open(meetings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 11 new meetings to add
    new_meetings = [
        # 1. 2025-04-29: Trym Vill Energi
        {
            "id": "m_2025-04-29_trym_vill_energi_hovfaret",
            "date": "2025-04-29",
            "title": "Trym - Vill Energi Hovfaret 13",
            "organizer": "gabriel@naturalstate.no",
            "location": "Teams/Telefon",
            "participant_count": 2,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Trym", "organization": "Natural State AS", "email": "trym@naturalstate.no"}
            ],
            "topics_discussed": [
                "Energirapport fra Vill Energi",
                "Klimagassberegning og -rapport",
                "Sammenheng mellom energiklasse og rivekrav",
                "One-pager for argumentasjon",
                "Møte med bydelen om velferd"
            ],
            "decisions": [
                "Linda skal gjennomgå og ferdigstille energiberegningen",
                "Vill Energi skal svare på mail om endringer i rapporten",
                "One-pager skal koble energirapport og klimagassberegning",
                "Møte planlegges med bydelen om velferd og eldreomsorg"
            ],
            "action_items": [
                {"task": "Ferdigstille energiberegning", "responsible": "Linda", "status": "pending"},
                {"task": "Svare Vill Energi på mail", "responsible": "Gabriel", "status": "pending"},
                {"task": "Lage one-pager om energi og klima", "responsible": "Trym/Gabriel", "status": "pending"},
                {"task": "Møte bydelen om velferdstjenester", "responsible": "Team", "status": "pending"}
            ],
            "report": {
                "summary": "Oppfølgingsmøte mellom Gabriel og Trym om energirapporten fra Vill Energi og klimagassberegningen for Hovfaret 13. Diskuterte behovet for å koble energirapporten med klimaargumentasjonen for å motbevise at bygget bør rives. Vill Energi har levert rapport, men med mangler. Viktig innsikt: energirapporten viser at bygget kan oppgraderes med små tiltak, noe som fjerner argumentet for riving basert på dårlig energistandard. Planlegger møte med bydelen om bruk som omsorgsbygg.",
                "discussion": [
                    {
                        "heading": "Energirapport og kvalitetssikring",
                        "content": "Vill Energi har levert energirapport, men kvaliteten er ikke tilfredsstillende. Trym har forsøkt å få dem til å forbedre, men velger nå å gi ærlig tilbakemelding. Linda skal ferdigstille beregningene basert på det som er levert."
                    },
                    {
                        "heading": "Koblingen mellom energi og klima",
                        "content": "Kritisk poeng: Klimagassrapporten viser nybygg vs gammelt bygg, men går ikke inn på byggets faktiske stand. Hvis noen argumenterer at bygget bør rives fordi det er gammelt og dårlig, må vi kunne vise til energirapporten som beviser at bygget er i god stand og kan oppgraderes med små tiltak. Dette er filosofien bak energirapporten - å fjerne rivekravet basert på energiargumentet."
                    },
                    {
                        "heading": "Møte med bydelen",
                        "content": "Planlagt møte mandag med bydelen om velferdstjenester. Eldreomsorgen lenger oppe i gata har setningsskader fra utgravning. Bydelen kan ha interesse av å bruke bygget til offentlige tjenester. Energiklassifisering er viktig for offentlige leietakere - må avklare minstekrav."
                    }
                ],
                "quotes": [
                    "Hvis de kun ser klimagassrapporten og sier 'bygget burde jo rives fordi det er gammelt', så kan vi si 'her er energirapporten som viser at bygget er mer enn kapabelt til å fortsette med små endringer.'",
                    "Det er den eneste de kan bruke mot oss - at det faktisk er bedre med nybygg. Fordi klimagassrapporten går ikke inn på det."
                ],
                "context": "Dette møtet er del av arbeidet med å bygge teknisk dokumentasjon for å motbevise rivekravet. Vill Energi er innleid for energikartlegging, og Linda hos Natural State arbeider med å konsolidere dataene. Møtet viser den strategiske koblingen mellom energidokumentasjon og politisk argumentasjon.",
                "metadata": {
                    "source": "transcript",
                    "source_file": "trym vill energi hovfaret 29.04.txt",
                    "word_count": 350,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "trym vill energi hovfaret 29.04.txt"
        },

        # 2. 2025-05-06: Jan Thomas NCC + Andreas etter Bente Otto
        {
            "id": "m_2025-05-06_jan_thomas_ncc_hovfaret",
            "date": "2025-05-06",
            "title": "Jan Thomas - Nordic Circle Construction + Andreas oppfølging",
            "organizer": "gabriel@naturalstate.no",
            "location": "Telefon/Teams",
            "participant_count": 3,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Jan Thomas", "organization": "Nordic Circle Construction", "email": None},
                {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS", "email": "andreas@urbania.no"}
            ],
            "topics_discussed": [
                "Nordic Circle Construction og sirkulære løsninger",
                "Omsorg+ som utviklingsscenario",
                "Møte med bydelsledere",
                "Energi- og klimarapporter",
                "Thomas R21 arkitekt og sirkulær bygging"
            ],
            "decisions": [
                "Skal kontakte Thomas (R21) om Nordic Circle Construction-perspektivet",
                "Andreas bekrefter interesse for reell bærekraft, ikke bare merkelapper",
                "Vil bruke prosjektet som showcase for sirkulære løsninger",
                "Segmentanalyse kan gjøres når bestillingen er raffinert"
            ],
            "action_items": [
                {"task": "Sende mail til Thomas R21 om NCC", "responsible": "Gabriel", "status": "pending"},
                {"task": "Dele Vill Energi-rapport", "responsible": "Gabriel", "status": "pending"},
                {"task": "Teknisk arbeidsmøte med arkitekt og Trym", "responsible": "Gabriel", "status": "pending"},
                {"task": "Undersøke FutureBilt-relevans", "responsible": "Gabriel", "status": "pending"}
            ],
            "report": {
                "summary": "To samtaler samme dag: Først med Jan Thomas om Nordic Circle Construction og sirkulære byggeløsninger for Hovfaret 13, deretter kort oppfølging med Andreas etter møte med Bente Otto om Omsorg+-krav. Jan Thomas-samtalen fokuserte på hvordan prosjektet kan bli et showcase for sirkulære løsninger i byggebransjen, med fokus på materialer, byggesystemer og verdikjeder. Andreas-samtalen bekreftet behov for å avklare Omsorg+-kravspesifikasjon med bydelen.",
                "discussion": [
                    {
                        "heading": "Nordic Circle Construction-perspektivet",
                        "content": "Jan Thomas representerer Nordic Circle Construction og diskuterer hvordan Hovfaret 13 kan brukes som case for sirkulære byggeløsninger. Andreas er med i NCC og har interesse av å finne løsninger som prosjektet kan investere i. Diskuterte muligheten for å bruke massivtre, Nordic Circle stål, gjenbruksbetong, og andre sirkulære materialer i påbygget."
                    },
                    {
                        "heading": "Reell bærekraft vs merkelapper",
                        "content": "Andreas beskrives som 'på motsatt side av skalaen' når det gjelder sertifiseringer - han bryr seg ikke om BREEAM eller andre merkelapper, kun om 'reell bærekraft'. Dette gir frihet til å fokusere på faktisk klimaeffekt fremfor compliance-øvelser."
                    },
                    {
                        "heading": "Arkitektrollen og sirkulæritet",
                        "content": "Thomas (sønn av Andreas, R21 arkitekt) har tegnet forslagene med grønne fasader og solceller. Han beskrives som 'veldig teknisk og rasjonell'. Planlegger møte for å diskutere sirkulære materialvalg og begrensninger."
                    },
                    {
                        "heading": "Omsorg+-krav (oppfølging med Andreas)",
                        "content": "Kort samtale etter Andreas' møte med Bente Otto. Diskuterte behovet for å forstå Omsorg+-kravspesifikasjonen - hvilke servicefunksjoner må være i første etasje (frisør, apotek etc). Gabriel skal finne kravspekken og sende til Andreas og Thomas for å vurdere planløsning."
                    }
                ],
                "quotes": [
                    "Andreas er på motsatt side av skalaen - han kunne ikke brydd seg mindre om BREEAM eller Futurebuilt. Det er 'reell bærekraft' som gjelder.",
                    "Hvis vi er skikkelig smarte her, Jan Thomas, og er litt sånn kapitalister, så finner vi en løsning som vi får Andreas til å kjøpe. Men først så har det nye NCC-fondet investert i det selskapet.",
                    "Hun nevnte noe om 108 hybelhus - det tallet har vi, men det ville de ikke ha. Det krever mye mer jobb."
                ],
                "context": "Disse samtalene representerer koblingen mellom det tekniske (sirkulære byggeløsninger) og det programmatiske (Omsorg+-behov). Nordic Circle Construction er et nettverk for sirkulær bygging der Andreas er involvert. Samtalen med Andreas kom rett etter et møte med bydelsrepresentanter om eldrebehov.",
                "metadata": {
                    "source": "transcript",
                    "source_files": ["jan thomas hovfaret 13 - NCC (May 6 13.10.05).txt", "kort prat med andreas etter bente otto ( urbania hovfaret ) (May 6 15.31.24).txt"],
                    "word_count": 450,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "jan thomas hovfaret 13 - NCC (May 6 13.10.05).txt"
        },

        # 3. 2025-05-21: Bærekraftsrapport structure
        {
            "id": "m_2025-05-21_barekraftsrapport_struktur",
            "date": "2025-05-21",
            "title": "Bærekraftsrapport - Strukturering og ESRS",
            "organizer": "gabriel@naturalstate.no",
            "location": "Natural State kontor",
            "participant_count": 3,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Linda", "organization": "Natural State AS", "email": None},
                {"name": "Einar Holthe", "organization": "Natural State AS", "email": "einar@naturalstate.no"}
            ],
            "topics_discussed": [
                "ESRS-struktur for bærekraftsrapport",
                "Klimagassberegninger og LCA",
                "Regulatorisk kontekst (Paris, FN, EU Green Deal)",
                "Scenarioanalyse (1, 2, 3)",
                "Mennesker og samfunn-dimensjonen",
                "Møte med bydelsledere neste dag"
            ],
            "decisions": [
                "Rapporten endres fra ESRS-type til bærekraftsvurdering",
                "Fokus på data vi faktisk har, ikke spekulasjon",
                "Klimadelen ferdigstilles først til møte",
                "Scope 1, 2, 3 beskrives kvalitativt, ikke kvantitativt ennå"
            ],
            "action_items": [
                {"task": "Ferdigstille klimadelen til fredag", "responsible": "Linda", "status": "pending"},
                {"task": "Lage 3-4 slides med klimauttak til bydelsmøte", "responsible": "Linda", "status": "pending"},
                {"task": "Skissere verdikjeder for scenario 1, 2, 3", "responsible": "Linda", "status": "pending"},
                {"task": "Legge inn sirkulære tiltak i materialkapittel", "responsible": "Linda", "status": "pending"}
            ],
            "report": {
                "summary": "Arbeidsmøte for å strukturere bærekraftsrapporten for Hovfaret 13. Linda, Gabriel og Einar gjennomgår dokumentstrukturen som følger ESRS-inspirert oppsett. Rapporten transformeres fra en ren ESRS-rapport til en 'bærekraftsvurdering' som gir anbefaling basert på tilgjengelige data. Viktig erkjennelse: må holde seg til det man vet og har data på, ikke presse argumentasjonen for langt. Diskuterer struktur: regulatorisk kontekst, klimagassberegninger, energitiltak, natur/biodiversitet, mennesker/samfunn, økonomiske aspekter.",
                "discussion": [
                    {
                        "heading": "Rapportstruktur og ESRS",
                        "content": "Rapporten er strukturert med beskrivelse, sammendrag, formål, begreper, og regulatorisk kontekst. Internasjonal kontekst inkluderer Paris-avtalen, FNs bærekraftsmål, EU Green Deal, Fit for 55, EPBD (Energy Performance of Buildings), EU Taxonomy, og Circular Economy Action Plan. ESRS nevnes men brukes ikke direkte - rapporten er mer en vurdering enn en compliance-rapport."
                    },
                    {
                        "heading": "De tre scenariene",
                        "content": "Rapporten analyserer tre utviklingsscenarier for bygget. Hvert scenario vurderes på klima/miljø, natur/biodiversitet, mennesker/samfunn, og økonomi. Viktig å vise hvordan de ulike scenariene påvirker scope 1, 2, 3 i verdikjeden - oppstrøms, egen operasjon, nedstrøms."
                    },
                    {
                        "heading": "Energitiltak og vindusdilemma",
                        "content": "Vinduer er en 'trigger' for Andreas - han mener utskifting ikke gir mening når man ser på klimaavtrykket av nye vinduer. Linda har regnet på alternative tiltakskombinasjon utover Vill Energis anbefalinger, men tør ikke anbefale egne tiltak uten fagkompetanse. Energieffektivisering er likevel det tiltaket som sparer mest over tid."
                    },
                    {
                        "heading": "Forberedelse til bydelsmøte",
                        "content": "Møte med bydelsledere neste dag (22. mai). Gabriel vil ikke overlesse med informasjon - hovedmål er å høre ut bydelsledernes behov. 3-4 slides med klimauttak fra Vill Energi er nok. Viktigste er å få sitater fra bydelsledere som kan brukes i videre argumentasjon."
                    }
                ],
                "quotes": [
                    "Det gir null mening å lage en ESRS-type rapport - vi har gjort det om til en bærekraftsvurdering hvor vi ser på scenariene og dataene vi har for å gi en anbefaling.",
                    "Det er lurt å bare holde oss til det vi vet og har data på, og ikke prøve å presse det mer enn det som er. Det kan bare slå feil.",
                    "Bydelslederne bestemmer jo ingenting - det viktigste er å få tydelige sitater som kan brukes videre."
                ],
                "context": "Dette møtet kommer dagen før det viktige møtet med bydelsledere (22. mai). Rapporten som utvikles skal tjene som faglig grunnlag for argumentasjonen mot rivekravet. ESRS (European Sustainability Reporting Standards) brukes som inspirasjon for struktur, men tilpasses til en prosjektspesifikk vurdering.",
                "metadata": {
                    "source": "transcript",
                    "source_file": "21-MAI-2025.md",
                    "word_count": 400,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "21-MAI-2025.md"
        },

        # 4. 2025-08-29: Linda og Gabriel bærekraft + KOMS brief
        {
            "id": "m_2025-08-29_barekraft_og_koms_brief",
            "date": "2025-08-29",
            "title": "Bærekraftsstatus + KOMS kommunikasjonsbriefing",
            "organizer": "gabriel@naturalstate.no",
            "location": "Natural State kontor",
            "participant_count": 3,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Linda", "organization": "Natural State AS", "email": None},
                {"name": "KOMS representant", "organization": "KOMS", "email": None}
            ],
            "topics_discussed": [
                "Status på bærekraftsrapporten",
                "Energitiltak og vindusdilemma",
                "Nettside og kommunikasjonsstrategi",
                "Sosiale medier (Instagram)",
                "Innholdsproduksjon og video",
                "Squarespace og teknisk eierskap"
            ],
            "decisions": [
                "Bærekraftsrapporten fokuserer på klima-delen først",
                "Nettsiden trenger oppdatering med tydeligere budskap",
                "Instagram-konto skal opprettes med ca 1 post/måned",
                "Video er viktigste format for rekkevidde",
                "Leietaker-intervjuer kan være godt innhold"
            ],
            "action_items": [
                {"task": "Ferdigstille klimadelen av rapporten", "responsible": "Linda", "status": "pending"},
                {"task": "Oppdatere nettside med konseptskisse-merking", "responsible": "KOMS/Jurei", "status": "pending"},
                {"task": "Opprette Instagram-konto", "responsible": "KOMS", "status": "pending"},
                {"task": "Vurdere leietaker-videoer", "responsible": "KOMS/Severin", "status": "pending"},
                {"task": "Avklare Squarespace-eierskap med Mike", "responsible": "Gabriel", "status": "pending"}
            ],
            "report": {
                "summary": "To møter samme dag: Først statusmøte med Linda om bærekraftsrapporten, deretter brief med KOMS om kommunikasjon og nettside. Bærekraftsrapporten har endret karakter fra ESRS-type til praktisk bærekraftsvurdering. Kommunikasjonsmøtet fokuserte på nettside, sosiale medier, og innholdsstrategi. Prosjektet er i en mellomfase der man ikke vet eksakt hva bygget skal bli, noe som gjør kommunikasjon utfordrende.",
                "discussion": [
                    {
                        "heading": "Bærekraftsrapport status (Linda)",
                        "content": "Rapporten har utviklet seg fra ESRS-inspirert til en mer praktisk bærekraftsvurdering. Fokus er på å bruke data man faktisk har (energirapport, LCA) og ikke spekulere. Energitiltak diskuteres - Linda har regnet på alternative kombinasjoner utover Vill Energis anbefalinger, men tør ikke anbefale uten fagkompetanse. Andreas' vindus-skepsis noteres."
                    },
                    {
                        "heading": "Kommunikasjonsstrategi (KOMS)",
                        "content": "Nettsiden er laget av eksterne (på deres konto, Gabriel er admin). Teknisk overføring til egen bruker er uavklart - Jurei kan hjelpe. Prosjektet har utfordring: ikke helt klart hva bygget skal bli (næring, bolig, omsorg+, hotell). Dette gjør det vanskelig å kommunisere tydelig budskap."
                    },
                    {
                        "heading": "Innholdsstrategi og sosiale medier",
                        "content": "Instagram skal opprettes med lav frekvens (1 post/måned). Video er viktigste format for rekkevidde. Forslag: leietaker-intervjuer, korte intro-videoer, dokumentasjon fra eventuelle arrangementer. Call-to-action er uklar - mest om synlighet og å ha et sted å vise til ved presseoppslag."
                    },
                    {
                        "heading": "Tidsplan og prosess",
                        "content": "Rammesøknad for Omsorg+ er sendt/skal sendes. Møte med byutviklingsbyråd 10. september. Prosjektet har optimisme for rask avklaring, men kan ta tid. Man vil 'trykke på play' og gjøre prosjektet synlig, legge press ved behov."
                    }
                ],
                "quotes": [
                    "Det er ikke helt entydig hvor prosjektet skal, hva det skal bli til, men vi skal fortelle den historien også.",
                    "Det er et ganske stygt bygg. Det er så å si umulig å ta gode bilder av sånne ting.",
                    "Vi har ikke gått ut med det, fordi vi ville snakke med James Lorentzen, få det møte med han først."
                ],
                "context": "Møtene skjer i en fase der prosjektet forbereder offentlig lansering og politisk trykk. Bærekraftsrapporten skal tjene som faglig dokumentasjon, mens kommunikasjonsarbeidet skal bygge synlighet og momentum. Møte med byutviklingsbyråd James Lorentzen er planlagt 10. september.",
                "metadata": {
                    "source": "transcript",
                    "source_files": ["hovfaret bærekraft LINDA OG GABRIEL  (2025-08-29 14.42.03).txt", "kort brief Hovfaret 13 KOMS  (2025-08-29 13.37.20).txt"],
                    "word_count": 420,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "hovfaret bærekraft LINDA OG GABRIEL  (2025-08-29 14.42.03).txt"
        },

        # 5. 2025-09-02: Andreas kort prat + Stedsøkonomisk prognose Einar
        {
            "id": "m_2025-09-02_andreas_og_einar_stedsokonomi",
            "date": "2025-09-02",
            "title": "Andreas oppfølging + Stedsøkonomisk prognose Einar",
            "organizer": "gabriel@naturalstate.no",
            "location": "Telefon",
            "participant_count": 3,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS", "email": "andreas@urbania.no"},
                {"name": "Einar Holthe", "organization": "Natural State AS", "email": "einar@naturalstate.no"}
            ],
            "topics_discussed": [
                "Takstmannvurdering for banken",
                "Stedsøkonomisk inntektsprognose",
                "Leieprisberegninger",
                "Studiekontorkonsept",
                "Utnyttelsesgrad og verdiskapning"
            ],
            "decisions": [
                "Andreas venter på takstmann for bankdokumenter",
                "Einar arbeider med inntektsprognose for ulike scenarier",
                "Studiekontormodell gir høyere inntekt per kvm",
                "Leieprisene må kartlegges mer detaljert"
            ],
            "action_items": [
                {"task": "Få takstmannvurdering", "responsible": "Andreas", "status": "pending"},
                {"task": "Ferdigstille inntektsprognose", "responsible": "Einar", "status": "pending"},
                {"task": "Kartlegge leiepriser for ulike konsepter", "responsible": "Einar/Gabriel", "status": "pending"}
            ],
            "report": {
                "summary": "To korte samtaler: Først med Andreas om praktiske forhold (takstmann, bankdokumenter), deretter med Einar om stedsøkonomisk arbeid. Andreas venter på takstmann for å få bankpapirer i orden. Einar jobber med inntektsprognose som viser at studiekontorkonseptet kan gi betydelig høyere inntekt per kvadratmeter enn tradisjonell kontorleie - potensielt dobling av inntekt ved mer effektiv utnyttelse.",
                "discussion": [
                    {
                        "heading": "Andreas - praktiske forhold",
                        "content": "Kort samtale om status. Andreas venter på takstmann som skal gjøre vurdering for banken. Dokumenter trengs for finansiering. Ingen store nyheter, mest oppfølging på praktiske forhold."
                    },
                    {
                        "heading": "Stedsøkonomisk prognose",
                        "content": "Einar arbeider med inntektsprognose for ulike utviklingsscenarier. Nøkkelinnsikt: studiekontorkonseptet (små enheter, fleksible arbeidsplasser) kan gi 20.000 kr/mnd for et 32 kvm kontor, sammenlignet med tradisjonell leie på ca 10.000 kr. Dette dobler potensielt inntekten ved omlegging."
                    },
                    {
                        "heading": "Leiepris og utnyttelse",
                        "content": "Diskusjon om hvordan leiepriser beregnes. Dagens modell: ca 1.850 kr/kvm + felleskostnader. Med studiekontorer får man høyere pris per kvm fordi leietakere verdsetter fleksibilitet og service. Felleskostnader fordeles på flere, noe som gjør enheter mer attraktive."
                    }
                ],
                "quotes": [
                    "Potensialet er der - vi kan ha fått dobbelt den inntekten ved å være mer effektiv og sette opp ferdige studiebord.",
                    "Når du har et sånt miljø med 15 forskjellige miljøer som snakker positivt om stedet, får du helt annen dynamikk."
                ],
                "context": "Disse samtalene er del av det løpende arbeidet med å dokumentere økonomisk potensial i transformasjon vs. riving. Stedsøkonomisk analyse er et kjerneverktøy for Natural State, og skal vise at intelligent transformasjon gir bedre avkastning enn nybygg.",
                "metadata": {
                    "source": "transcript",
                    "source_files": ["andreas hovfaret kort prat .  (2025-09-02 16.09.28).txt", "stedsøkonomisk prognose Einar Hovfaret 13  (2025-09-02 13.05.28).txt"],
                    "word_count": 300,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "andreas hovfaret kort prat .  (2025-09-02 16.09.28).txt"
        },

        # 6. 2025-09-27: URBANIA HOVFARET 13 - Comprehensive meeting
        {
            "id": "m_2025-09-27_urbania_hovfaret_workshop",
            "date": "2025-09-27",
            "title": "Urbania Hovfaret 13 - Konseptworkshop med R21",
            "organizer": "gabriel@naturalstate.no",
            "location": "Hovfaret 13 / Natural State kontor",
            "participant_count": 4,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Einar Holthe", "organization": "Natural State AS", "email": "einar@naturalstate.no"},
                {"name": "Thomas Thorsnes", "organization": "R21 Arkitekter AS", "email": None},
                {"name": "Andreas Thorsnes", "organization": "Urbania Eiendom AS", "email": "andreas@urbania.no"}
            ],
            "topics_discussed": [
                "Fire utviklingsscenarier gjennomgang",
                "Energikartlegging og klimagassregnskap",
                "Fasadeendringer og grønne løsninger",
                "Omsorg+, hotell, bokollektiv alternativer",
                "Inntektspotensial og stedsøkonomi",
                "Husbanken-finansiering",
                "Kulturminnevern og tidstypisk arkitektur"
            ],
            "decisions": [
                "Fem etasjer næring er alternativ 1 (dagens situasjon optimalisert)",
                "Fire etasjer næring + fire etasjer bolig er alternativ 2",
                "Syv etasjer bolig + næring i første er alternativ 3",
                "Åtte etasjer næring er alternativ 4",
                "Energikartlegging og ombrukskartlegging skal søkes støtte til",
                "Form med inntrukket påbygg og rund trapp som monument er valgt retning"
            ],
            "action_items": [
                {"task": "Søke Enova om energikartlegging", "responsible": "Gabriel/Vill Energi", "status": "pending"},
                {"task": "Søke Resirkel om ombrukskartlegging", "responsible": "Gabriel", "status": "pending"},
                {"task": "Lage leietakerliste med arealfordeling", "responsible": "Andreas/Gabriel", "status": "pending"},
                {"task": "Planlegge husmøte med leietakere", "responsible": "Gabriel", "status": "pending"},
                {"task": "Oppdatere tegninger med underetasjer", "responsible": "Thomas R21", "status": "pending"},
                {"task": "Lage inntektsprognose for studiokontorer", "responsible": "Einar", "status": "pending"}
            ],
            "report": {
                "summary": "Omfattende konseptworkshop med R21 Arkitekter og Natural State for å gjennomgå fire utviklingsscenarier for Hovfaret 13. Møtet var svært produktivt med detaljert gjennomgang av arkitektoniske løsninger, programmatiske alternativer (næring, bolig, hotell, omsorg+), og finansieringsstrategier. Viktig gjennombrudd: arkitektene presenterte en elegant formløsning med inntrukket påbygg som gir bygget et 'nøkternt' uttrykk - møtt med 'nøktern entusiasme' (vestlandsk for 'veldig bra'). Diskuterte Husbanken-finansiering, kulturminneaspekter, og inntektspotensial ved studiokontorer.",
                "discussion": [
                    {
                        "heading": "De fire scenariene",
                        "content": "Alternativ 1: Fem etasjer næring - dagens bygg transformert til foregangeksempel på viderebruk. Fasadeendringer, pergola ved inngang, aktiv førsteetasje. Alternativ 2: Fire etasjer næring + fire etasjer bolig - mest sannsynlig scenario. Alternativ 3: Syv etasjer bolig + næring i første etasje. Alternativ 4: Åtte etasjer rent næringsbygg. Alle alternativer beholder aktiv førsteetasje og underetasjer som parkering/boder."
                    },
                    {
                        "heading": "Arkitektonisk formgrep",
                        "content": "Thomas R21 presenterte skisser der påbygget er inntrukket fra eksisterende fasade, med den runde trappen bevart som et 'monument'. Dette gir en elegant overgang mellom gammelt og nytt, og bygget ser 'ikke så voldsomt ut'. Fasaden kan oppgraderes med grønne elementer og varevindu på innsiden (som gjort på Industribrygg) for bedre energieffektivitet uten å endre det tidstypiske uttrykket."
                    },
                    {
                        "heading": "Programmatiske alternativer",
                        "content": "Diskuterte hotell (21 rom per etasje), bokollektiv (18 enheter), studentboliger, omsorgsboliger. Viktig innsikt: hotell er 'næring' regulatorisk, men overnatting - dette åpner muligheter. HDO-boliger (Husbank-støttede omsorgsboliger) gir 50% tilskudd til kjøp. Einar anbefaler å skille studentkollektiv og omsorgstrapp i kommunikasjonen - helt ulike finansieringsmodeller."
                    },
                    {
                        "heading": "Energi og miljødokumentasjon",
                        "content": "Energikartlegging må gjøres for å ha faktabasert argumentasjon. Vill Energi/Per har 100% treff på Enova-søknader om energikartlegging. Resirkel kan søke om ombrukskartlegging. Asplan Viak er kontaktet for klimagassberegning. Bygget bruker under 40 kWh/m² i dag - 'veldig beskjedent for et slikt bygg'."
                    },
                    {
                        "heading": "Inntektspotensial og stedsøkonomi",
                        "content": "Dagens leie: ca 1,5 mill på 14 leietakere. Med studiokontorkonsept kan dette øke til 3 mill+ - nesten dobling. Nøkkelen er å dele opp i mindre enheter (32, 21, 21 kvm) og ta høyere pris per kvm. Einar skal lage detaljert inntektsprognose. Viktig: felleskostnader fordeles på flere, service inkluderes, og miljøet blir mer attraktivt."
                    },
                    {
                        "heading": "Husbanken og finansiering",
                        "content": "Husbanken kan finansiere transformasjon med energioppgradering. Referanse til Wilswaterslien-prosjektet. Universell utforming trengs, men ikke full tilgjengelighet. Lars Halvorsen i Husbanken er kontaktperson. HDO-boliger (hjemmebaserte omsorgsboliger) gir 50% tilskudd ved vedtak om hjemmehjelp."
                    }
                ],
                "quotes": [
                    "Det er en nøktern entusiasme. Sånn at du sier på Vestlandet: 'Det er ikke så gale.' Det betyr veldig, veldig bra!",
                    "Potensialet er der - vi kan ha fått dobbelt den inntekten ved å være mer effektiv og sette opp ferdige studiebord.",
                    "Hvis du klarer å bygge opp entusiasme hos saksbehandler i Plan og bygg, så er det utrolig hva du kan få til.",
                    "Det er et bygg som er fleksibelt. Det er bygd og prosjektert for utvikling. Fortiden beregnet inn det økte behovet."
                ],
                "context": "Dette er et av de viktigste arbeidsmøtene i prosjektet - her kobles arkitektur, økonomi, og strategi sammen. R21 Arkitekter ledes av Thomas (sønn av Andreas), noe som gir tett samarbeid. Møtet skjer etter sommerferien, i en fase der prosjektet forbereder rammesøknad og politisk trykk. Natural States stedsøkonomiske metodikk demonstreres.",
                "metadata": {
                    "source": "transcript",
                    "source_file": "URBANIA HOVFARET 13 (Sep 27 08.44.09).txt",
                    "word_count": 800,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "URBANIA HOVFARET 13 (Sep 27 08.44.09).txt"
        },

        # 7. 2025-10-14: Hovfaret preik
        {
            "id": "m_2025-10-14_hovfaret_befaring_og_diskusjon",
            "date": "2025-10-14",
            "title": "Hovfaret 13 - Befaring og prosjektdiskusjon",
            "organizer": "gabriel@naturalstate.no",
            "location": "Hovfaret 13",
            "participant_count": 3,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Einar Holthe", "organization": "Natural State AS", "email": "einar@naturalstate.no"},
                {"name": "Ekstern rådgiver", "organization": None, "email": None}
            ],
            "topics_discussed": [
                "Bygningsbefaring og teknisk status",
                "Leietakeroversikt og arealfordeling",
                "Interessentkartlegging og nabolag",
                "Filosofiske refleksjoner om liv og arbeid",
                "Konkurrenter i området",
                "Prosjektets fremtid"
            ],
            "decisions": [
                "Leietakerliste skal oppdateres med kontaktinfo",
                "Interessentoversikt over nabolaget skal lages",
                "Kantinen kan lånes gratis til arrangementer",
                "Fokus på å skape mer 'liv' i bygget"
            ],
            "action_items": [
                {"task": "Oppdatere leietakerliste med kontaktinfo", "responsible": "Gabriel", "status": "pending"},
                {"task": "Kartlegge interessenter i nabolaget", "responsible": "Gabriel", "status": "pending"},
                {"task": "Kontakte bydelen (venteliste)", "responsible": "Gabriel", "status": "pending"},
                {"task": "Vurdere arrangement i kantinen", "responsible": "Gabriel", "status": "pending"}
            ],
            "report": {
                "summary": "Befaring i bygget med gjennomgang av alle etasjer, leietakere, og tekniske installasjoner. Samtalen ble også filosofisk - diskuterte livsrefleksjoner, tap, og mening. Praktisk fokus på å kartlegge interessenter i nabolaget og skape mer aktivitet i bygget. Bygget beskrives som 'dødt' - kantinen brukes ikke, leietakere holder seg for seg selv. Mulighet for å bruke kantinen til arrangementer for å skape 'content' og liv.",
                "discussion": [
                    {
                        "heading": "Bygningsbefaring",
                        "content": "Gjennomgang av alle etasjer med fokus på leietakere og arealfordeling. Første etasje har to butikker som selger mot bedrifter (ikke publikum). Kantinen er ikke i drift. Leietakere inkluderer Svein, Anneke, og flere kontorleietakere. Parkeringskjeller har boder, lagerfunksjoner. Ventilasjon er separate anlegg for garasje og sentralbygget."
                    },
                    {
                        "heading": "Byggets atmosfære",
                        "content": "Bygget beskrives som 'veldig dødt'. Leietakere bruker ikke fellesarealene. Kantinen står tom. Noen bruker egne innganger og ser aldri andre. Gabriel oppfordrer folk til å bruke fellesarealer men det er motstand. Potensial for å skape mer liv gjennom studiokontorer og aktivering."
                    },
                    {
                        "heading": "Konkurrenter og marked",
                        "content": "Diskusjon om konkurrerende lokaler i området: Holm Eindahl, Møller (nybygg), Trenger, Klaveness (modernisert). Utfordring: disse har bedre fasiliteter og mer moderne uttrykk. Hovfaret må differensiere seg gjennom pris, miljø, og konsept - ikke konkurrere på standard kontorfasiliteter."
                    },
                    {
                        "heading": "Filosofiske refleksjoner",
                        "content": "Samtalen tok en personlig vending med refleksjoner om tap (Gabriel mistet datteren sin for fire år siden), mening i livet, og betydningen av lys og natur. Diskuterte LED-revolusjonens påvirkning på menneskers døgnrytme og helse. Disse personlige innsiktene farger Gabriels tilnærming til prosjekter."
                    },
                    {
                        "heading": "Interessentkartlegging",
                        "content": "Behov for oversikt over dialoger med organisasjoner og interessenter i nabolaget. Hoff-Elvens venner er en potensiell samarbeidspartner, men tidligere kontakt var problematisk. Ullern frivillighetssentral sitter i en garasje oppe i området. Oslo kommune bydel ønsker å være i bygget men har ikke fått lov."
                    }
                ],
                "quotes": [
                    "Det er for meg helt fundamentalt dette med lys. Hun (datteren) hadde veldig spesielle øyne.",
                    "Vi er predatorer som utvikles for fort - vi tenker ikke over konsekvensene.",
                    "Det er veldig dødt her. Kantinen blir ikke brukt. Det er bomtrist å komme til oss.",
                    "Hver dag er en gave. Livet er vakkert. Det var ikke evig. Hvis det ikke hadde vært noe ende, så hadde det ikke gitt noe mening."
                ],
                "context": "Dette møtet er en blanding av praktisk befaring og dypere samtaler om mening og motivasjon. Det gir innsikt i byggets nåværende tilstand og utfordringer, samt Gabriels personlige drivkrefter bak prosjektet. Befaringen dokumenterer fysiske forhold og identifiserer muligheter for aktivering.",
                "metadata": {
                    "source": "transcript",
                    "source_file": "Hovfaret preik  (Oct 14 12.39.11).txt",
                    "word_count": 550,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "Hovfaret preik  (Oct 14 12.39.11).txt"
        },

        # 8. 2025-12-03: Hovfaret diskusjon
        {
            "id": "m_2025-12-03_hovfaret_ncc_ombruk",
            "date": "2025-12-03",
            "title": "Hovfaret 13 - NCC og ombrukskartlegging",
            "organizer": "gabriel@naturalstate.no",
            "location": "Telefon/Teams",
            "participant_count": 2,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Trym", "organization": "Natural State AS", "email": "trym@naturalstate.no"}
            ],
            "topics_discussed": [
                "NCC (Nordic Circle Construction) status",
                "Ombrukskartlegging",
                "Potensiell lab-leietaker",
                "Områdeutvikling Skøyen"
            ],
            "decisions": [
                "Ombrukskartlegging skal prioriteres",
                "Lab-leietaker er interessant mulighet",
                "NCC-kobling skal følges opp"
            ],
            "action_items": [
                {"task": "Følge opp ombrukskartlegging", "responsible": "Gabriel", "status": "pending"},
                {"task": "Avklare lab-leietaker interesse", "responsible": "Gabriel", "status": "pending"}
            ],
            "report": {
                "summary": "Kort oppfølgingssamtale om status på NCC-kobling og ombrukskartlegging. Diskuterte mulighet for lab-leietaker i bygget, noe som kunne styrke prosjektets profil. Ombrukskartlegging sees som viktig neste steg for å dokumentere gjenbrukspotensial.",
                "discussion": [
                    {
                        "heading": "NCC og ombruk",
                        "content": "Oppfølging på Nordic Circle Construction-koblingen. Ombrukskartlegging er neste viktige dokumentasjon som trengs. Dette vil vise potensial for gjenbruk av materialer ved eventuell ombygging."
                    },
                    {
                        "heading": "Lab-leietaker",
                        "content": "Diskusjon om potensiell leietaker som driver lab/forskningsvirksomhet. Dette kunne passe godt i bygget og styrke profilen som kunnskapsmiljø."
                    }
                ],
                "context": "Kort oppfølgingssamtale i en travel periode. Prosjektet er i fasen der teknisk dokumentasjon bygges opp parallelt med at man holder kontakt med potensielle leietakere.",
                "metadata": {
                    "source": "transcript",
                    "source_file": "Hovfaret (Dec 3 11.51.35).txt",
                    "word_count": 150,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "Hovfaret (Dec 3 11.51.35).txt"
        },

        # 9. 2025-12-18: Trym tilbud Vill Energi
        {
            "id": "m_2025-12-18_trym_vill_energi_tilbud",
            "date": "2025-12-18",
            "title": "Trym - Vill Energi tilbud og Enova-støtte",
            "organizer": "gabriel@naturalstate.no",
            "location": "Telefon",
            "participant_count": 2,
            "participants": [
                {"name": "Gabriel Bøen", "organization": "Natural State AS", "email": "gabriel@naturalstate.no"},
                {"name": "Trym", "organization": "Natural State AS", "email": "trym@naturalstate.no"}
            ],
            "topics_discussed": [
                "Vill Energi tilbud og prising",
                "Enova-støtte muligheter",
                "Energikartlegging kostnader"
            ],
            "decisions": [
                "Vill Energi-tilbud skal vurderes",
                "Enova-støtte skal søkes for energikartlegging"
            ],
            "action_items": [
                {"task": "Vurdere Vill Energi tilbud", "responsible": "Trym/Gabriel", "status": "pending"},
                {"task": "Søke Enova om støtte", "responsible": "Gabriel", "status": "pending"}
            ],
            "report": {
                "summary": "Kort samtale om tilbud fra Vill Energi på energikartlegging og muligheter for Enova-støtte. Diskuterte prising og hvordan dette passer inn i prosjektets totale budsjett for dokumentasjon.",
                "discussion": [
                    {
                        "heading": "Vill Energi tilbud",
                        "content": "Gjennomgang av tilbud fra Vill Energi på energikartlegging. Prising diskuteres i forhold til hva som kan dekkes av Enova-støtte."
                    },
                    {
                        "heading": "Enova-finansiering",
                        "content": "Enova gir støtte til energikartlegging av eksisterende bygg. Per/Vill Energi har erfaring med søknader og god treffrate. Dette kan redusere prosjektets egne kostnader betydelig."
                    }
                ],
                "context": "Møtet handler om praktisk finansiering av energidokumentasjon. Vill Energi er leverandør av energikartlegging, og Enova er statlig støtteordning for energitiltak i bygg.",
                "metadata": {
                    "source": "transcript",
                    "source_file": "TRYM TILBUD VILL ENERGI HOVFARET (Dec 18 15.52.18).txt",
                    "word_count": 120,
                    "consolidated_date": "2025-12-02"
                }
            },
            "source_file": "TRYM TILBUD VILL ENERGI HOVFARET (Dec 18 15.52.18).txt"
        }
    ]

    # Add all new meetings to the meetings list
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
    data['metadata']['fase_12_enrichment'] = {
        'date': datetime.now().isoformat(),
        'meetings_added': added,
        'source': 'Downloads/Møter etter prompt Hovfaret 13/',
        'phase': '12.2'
    }

    # Sort meetings by date
    data['meetings'].sort(key=lambda x: x['date'])

    # Write back
    with open(meetings_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Added {added} new meetings to meetings.json")
    print(f"Total meetings now: {len(data['meetings'])}")

if __name__ == '__main__':
    main()
