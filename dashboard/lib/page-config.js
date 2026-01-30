const PAGE_CONFIG = {
  tabs: {
    prosjektstyring: {
      label: "Prosjektstyring",
      icon: "📊",
      pages: [
        {
          id: "command-center",
          name: "Command Center",
          desc: "Beslutninger og faser",
          href: "command-center.html",
        },
        {
          id: "timeline",
          name: "Tidslinje",
          desc: "1989-2027",
          href: "timeline.html",
        },
        {
          id: "meetings",
          name: "Møter",
          desc: "70 møter med rapporter",
          href: "meetings.html",
        },
        {
          id: "stakeholders",
          name: "Interessenter",
          desc: "23 personer, 16 org",
          href: "stakeholders.html",
        },
        {
          id: "deliverables",
          name: "Leveranser",
          desc: "37 leveranser",
          href: "deliverables.html",
        },
        {
          id: "regulatory-status",
          name: "Regulatorisk status",
          desc: "Søknadsstatus",
          href: "regulatory-status.html",
        },
      ],
    },
    presentasjoner: {
      label: "Presentasjoner",
      icon: "📖",
      pages: [
        {
          id: "master",
          name: "Master",
          desc: "Longread-kronikk",
          href: "master.html",
        },
        {
          id: "rammesoeknad",
          name: "Rammesøknad",
          desc: "Komplett pakke",
          href: "rammesoeknad.html",
        },
      ],
    },
    produksjon: {
      label: "Produksjonsrom",
      icon: "🔧",
      categories: {
        databaser: {
          label: "Databaser",
          pages: [
            {
              id: "documents",
              name: "Dokumenter",
              desc: "271 dokumenter",
              href: "documents.html",
            },
          ],
        },
        presentasjoner: {
          label: "Presentasjoner",
          pages: [
            {
              id: "konseptskisse",
              name: "Konseptskisse 1.0",
              desc: "Original",
              href: "konseptskisse.html",
            },
            {
              id: "konseptskisse-2",
              name: "Konseptskisse 2.0",
              desc: "Desember 2025",
              href: "konseptskisse-2.html",
            },
            {
              id: "konseptskisse-3",
              name: "Konseptskisse 3.0",
              desc: "16 slides",
              href: "konseptskisse-3.html",
            },
            {
              id: "slides-library",
              name: "Slide-bibliotek",
              desc: "Standalone slides",
              href: "slides-library.html",
            },
            {
              id: "timeline-slides",
              name: "Tidslinje-slides",
              desc: "Presentasjonsformat",
              href: "timeline-slides.html",
            },
          ],
        },
        visualiseringer: {
          label: "Visualiseringer",
          pages: [
            {
              id: "solstudie",
              name: "Solstudie",
              desc: "Animasjon",
              href: "solstudie.html",
            },
            {
              id: "visual-stories",
              name: "Visuelle historier",
              desc: "Storytelling",
              href: "visual-stories.html",
            },
            {
              id: "stakeholder-journey",
              name: "Interessentreise",
              desc: "Presentasjonsmodus",
              href: "stakeholder-journey.html",
            },
          ],
        },
        tekster: {
          label: "Tekster",
          pages: [
            {
              id: "text-library",
              name: "Tekstbibliotek",
              desc: "Ulike stemmer",
              href: "text-library.html",
            },
            {
              id: "communication-strategy",
              name: "Kommunikasjon",
              desc: "Strategi",
              href: "communication-strategy.html",
            },
          ],
        },
        analyser: {
          label: "Analyser",
          pages: [
            {
              id: "sustainability-complete",
              name: "Bærekraft",
              desc: "LCA og klimadata",
              href: "sustainability-complete.html",
            },
            {
              id: "analytics",
              name: "Analyse",
              desc: "Statistikk",
              href: "analytics.html",
            },
            {
              id: "market-insight",
              name: "Markedsinnsikt",
              desc: "Demografi",
              href: "market-insight.html",
            },
            {
              id: "natur-miljo",
              name: "Natur & Miljø",
              desc: "Konsekvensutredning",
              href: "natur-miljo.html",
            },
            {
              id: "miljo-argumenter",
              name: "Miljøargumenter",
              desc: "Søkbar base",
              href: "miljo-argumenter.html",
            },
            {
              id: "miljoeargumentasjon-teknisk",
              name: "Teknisk Miljøarg.",
              desc: "Med rapportreferanser",
              href: "miljoeargumentasjon-teknisk.html",
            },
            {
              id: "miljoeargumentasjon-dokument",
              name: "Miljødokument",
              desc: "Formell presentasjon",
              href: "miljoeargumentasjon-dokument.html",
            },
            {
              id: "naturpositivitet",
              name: "Naturpositivitet",
              desc: "NiN-kartlegging & tiltak",
              href: "naturpositivitet.html",
            },
            {
              id: "orret",
              name: "Ørret i Hoffselva",
              desc: "Forskningsprosjekt",
              href: "orret.html",
            },
            {
              id: "professor-henvendelse",
              name: "Professorhenvendelse",
              desc: "Fagvurdering ørret/skygge",
              href: "professor-henvendelse.html",
            },
            {
              id: "scenarios",
              name: "Scenarier",
              desc: "Sammenligning",
              href: "scenarios.html",
            },
          ],
        },
        status: {
          label: "Status",
          pages: [
            {
              id: "status-december-2025-complete",
              name: "Status Des 2025",
              desc: "Komplett",
              href: "status-december-2025-complete.html",
            },
            {
              id: "status-december-2025",
              name: "Status Des (enkel)",
              desc: "Enkel versjon",
              href: "status-december-2025.html",
            },
          ],
        },
        konsept: {
          label: "Konsept",
          pages: [
            {
              id: "omsorg-plus",
              name: "Omsorg+",
              desc: "73 enheter",
              href: "omsorg-plus.html",
            },
            {
              id: "utleie",
              name: "Utleie",
              desc: "Lokaler",
              href: "utleie.html",
            },
            {
              id: "ncc-partnership",
              name: "NCC Partnership",
              desc: "Nordic Circle",
              href: "ncc-partnership.html",
            },
            {
              id: "place-economy",
              name: "Stedsøkonomi",
              desc: "Verdimodell",
              href: "place-economy.html",
            },
          ],
        },
        rapporter: {
          label: "Rapporter",
          pages: [
            {
              id: "sustainability-report",
              name: "Bærekraftsrapport",
              desc: "83 sider",
              href: "sustainability-report.html",
            },
            {
              id: "barekraftsrapport-overview",
              name: "Rapport oversikt",
              desc: "Gap-analyse",
              href: "barekraftsrapport-overview.html",
            },
            {
              id: "barekraftsrapport-2",
              name: "Rapport arbeidsrom",
              desc: "Redigering",
              href: "barekraftsrapport-2.html",
            },
          ],
        },
        annet: {
          label: "Annet",
          pages: [
            {
              id: "project-story",
              name: "Prosjekthistorie",
              desc: "Longread",
              href: "project-story.html",
            },
            {
              id: "timelines",
              name: "Tidslinjebibliotek",
              desc: "Alle tidslinjer",
              href: "timelines.html",
            },
            {
              id: "participation",
              name: "Medvirkning",
              desc: "Dialogprosesser",
              href: "participation.html",
            },
            {
              id: "overview",
              name: "Oversikt",
              desc: "Prosjektstatus",
              href: "overview.html",
            },
          ],
        },
      },
    },
  },

  getTabForPage(pageId) {
    for (const [tabId, tab] of Object.entries(this.tabs)) {
      if (tab.pages) {
        if (tab.pages.some((p) => p.id === pageId)) return tabId;
      }
      if (tab.categories) {
        for (const cat of Object.values(tab.categories)) {
          if (cat.pages.some((p) => p.id === pageId)) return tabId;
        }
      }
    }
    return "produksjon";
  },

  getPageInfo(pageId) {
    for (const tab of Object.values(this.tabs)) {
      if (tab.pages) {
        const page = tab.pages.find((p) => p.id === pageId);
        if (page) return page;
      }
      if (tab.categories) {
        for (const cat of Object.values(tab.categories)) {
          const page = cat.pages.find((p) => p.id === pageId);
          if (page) return page;
        }
      }
    }
    return null;
  },

  getAllPages() {
    const pages = [];
    for (const tab of Object.values(this.tabs)) {
      if (tab.pages) pages.push(...tab.pages);
      if (tab.categories) {
        for (const cat of Object.values(tab.categories)) {
          pages.push(...cat.pages);
        }
      }
    }
    return pages;
  },
};

if (typeof window !== "undefined") {
  window.PAGE_CONFIG = PAGE_CONFIG;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = PAGE_CONFIG;
}
