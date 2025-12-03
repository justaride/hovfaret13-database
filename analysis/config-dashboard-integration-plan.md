# Config.json Dashboard Integration Plan

## Mål
Implementere `config.json` som single source of truth for alle nøkkeltall i dashboards.

---

## Fase 1: Config Loader Library

### Opprett `dashboard/lib/config-loader.js`
```javascript
// Singleton config loader
const ConfigLoader = {
  config: null,

  async load() {
    if (this.config) return this.config;
    const response = await fetch('../data/config.json');
    this.config = await response.json();
    return this.config;
  },

  get(path) {
    // Support dot notation: 'metrics.meetings_total'
    const keys = path.split('.');
    let value = this.config;
    for (const key of keys) {
      value = value?.[key];
    }
    return value;
  }
};
```

---

## Fase 2: Dashboard Oppdateringer

### Prioritet 1 - Høyt trafikk dashboards
| Dashboard | Felt fra config.json |
|-----------|---------------------|
| `index.html` | `metrics.meetings_total`, `metrics.documents_total`, `metrics.stakeholders.*` |
| `meetings.html` | `metrics.meetings_total` |
| `documents.html` | `metrics.documents_total` |
| `stakeholders.html` | `metrics.stakeholders.people`, `metrics.stakeholders.organizations` |

### Prioritet 2 - Tematiske dashboards
| Dashboard | Felt fra config.json |
|-----------|---------------------|
| `sustainability.html` | `sustainability.*`, `scenarios.*` |
| `scenarios.html` | `scenarios.*`, `sustainability.co2_savings_percent` |
| `regulatory-status.html` | `regulatory_status.*`, `key_dates.*` |
| `deliverables.html` | `metrics.deliverables_total` |

### Prioritet 3 - Oversikt dashboards
| Dashboard | Felt fra config.json |
|-----------|---------------------|
| `overview.html` | `building.*`, `project.*`, `metrics.*` |
| `timeline.html` | `metrics.timeline.*`, `key_dates.*` |
| `analytics.html` | Alle metrics |

---

## Fase 3: Implementeringsmønster

### Eksempel: index.html oppdatering

**Før (hardkodet):**
```html
<span class="module-badge count">70</span>
```

**Etter (dynamisk):**
```javascript
// I init-funksjon
const config = await ConfigLoader.load();
document.querySelector('[data-module="meetings"] .count').textContent =
  config.metrics.meetings_total;
```

### HTML-struktur med data-attributter:
```html
<span class="module-badge count" data-config="metrics.meetings_total">-</span>
```

### Universal oppdateringsfunksjon:
```javascript
async function initConfigValues() {
  const config = await ConfigLoader.load();
  document.querySelectorAll('[data-config]').forEach(el => {
    const path = el.dataset.config;
    const value = ConfigLoader.get(path);
    if (value !== undefined) {
      el.textContent = value;
    }
  });
}
```

---

## Fase 4: Config.json Utvidelser

### Legg til manglende felt:
```json
{
  "dashboard_metrics": {
    "decisions_count": 108,
    "actions_count": 119,
    "extracted_documents": 458
  }
}
```

---

## Implementeringsrekkefølge

1. **Uke 1**: Opprett config-loader.js, test med index.html
2. **Uke 2**: Implementer i Prioritet 1 dashboards
3. **Uke 3**: Implementer i Prioritet 2 dashboards
4. **Uke 4**: Implementer i Prioritet 3 dashboards, dokumenter

---

## Fordeler

- **Konsistens**: Alle tall synkronisert
- **Vedlikehold**: Ett sted å oppdatere tall
- **Feilforebygging**: Reduserer risiko for avvik
- **Automatisering**: Kan kobles til CI/CD for validering

---

## Risiko og mitigering

| Risiko | Mitigering |
|--------|------------|
| Nettverksfeil ved config-lasting | Fallback til hardkodede verdier |
| Cache-problemer | Cache-busting med versjonsnummer |
| Breaking changes i config | Versjonering i metadata.version |

---

*Opprettet: 2025-12-03*
*Siste oppdatering: 2025-12-03*
