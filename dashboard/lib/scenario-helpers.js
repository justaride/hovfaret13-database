/**
 * Scenario Helpers Module
 * Utilities for scenario comparison and visualization
 */

const ScenarioHelpers = {
  /**
   * Scenario metadata with colors and icons
   */
  SCENARIO_META: {
    'scenario_1': {
      label: 'Demolition & Rebuild',
      label_no: 'Nybygg og riving',
      icon: 'hammer',
      color: '#EF4444',
      description: 'Demolish existing building, construct new building',
      status_color: '#DC2626'
    },
    'scenario_2': {
      label: 'Rehabilitation',
      label_no: 'Rehabilitering',
      icon: 'recycle',
      color: '#10B981',
      description: 'Preserve and upgrade existing building',
      status_color: '#059669'
    },
    'scenario_3': {
      label: 'Rehabilitation + Extension',
      label_no: 'Påbygg (Omsorg+)',
      icon: 'building-2',
      color: '#3B82F6',
      description: 'Rehabilitate existing + add 3 floors of elderly housing',
      status_color: '#2563EB'
    }
  },

  /**
   * Comparison metrics with units and formatting
   */
  METRICS: {
    'total_co2': {
      label: 'Total CO₂ Emissions',
      label_no: 'Totale CO₂-utslipp',
      unit: 'tonnes',
      format: (value) => `${value.toLocaleString('nb-NO')} tonn`,
      icon: 'globe',
      description: 'Total carbon dioxide equivalent emissions',
      lowerIsBetter: true
    },
    'co2_per_m2': {
      label: 'CO₂ per m² BTA',
      label_no: 'CO₂ per m² BTA',
      unit: 'kg CO₂-ekv/m²',
      format: (value) => `${Math.round(value)} kg/m²`,
      icon: 'bar-chart-2',
      description: 'Carbon emissions per square meter',
      lowerIsBetter: true
    },
    'material_emissions': {
      label: 'Material Emissions per m²',
      label_no: 'Materialutslipp per m²',
      unit: 'kg CO₂-ekv/m²',
      format: (value) => `${Math.round(value)} kg/m²`,
      icon: 'box',
      description: 'Carbon emissions from materials',
      lowerIsBetter: true
    },
    'energy_consumption': {
      label: 'Energy Consumption',
      label_no: 'Energiforbruk',
      unit: 'kWh/m²/år',
      format: (value) => {
        if (typeof value === 'string') return value;
        return `${Math.round(value)} kWh/m²/år`;
      },
      icon: 'zap',
      description: 'Annual energy consumption per square meter',
      lowerIsBetter: true
    }
  },

  /**
   * Status badge metadata
   */
  STATUS_META: {
    'Not recommended': {
      color: '#EF4444',
      icon: 'x-circle',
      label: 'Not Recommended'
    },
    'Recommended baseline': {
      color: '#10B981',
      icon: 'check-circle',
      label: 'Recommended Baseline'
    },
    'Preferred option - maximizes social benefit': {
      color: '#3B82F6',
      icon: 'award',
      label: 'Preferred Option'
    }
  },

  /**
   * Get scenario metadata
   */
  getScenarioMeta(scenarioId) {
    return this.SCENARIO_META[scenarioId] || {
      label: scenarioId,
      icon: '📋',
      color: '#6B7280'
    };
  },

  /**
   * Get status badge metadata
   */
  getStatusMeta(status) {
    return this.STATUS_META[status] || {
      color: '#6B7280',
      icon: '📋',
      label: status
    };
  },

  /**
   * Calculate percentage difference from baseline
   */
  calculateDifference(value, baseline) {
    if (!baseline || baseline === 0) return 0;
    return ((value - baseline) / baseline) * 100;
  },

  /**
   * Format percentage with sign
   */
  formatPercentage(percentage, decimals = 0) {
    const sign = percentage > 0 ? '+' : '';
    return `${sign}${percentage.toFixed(decimals)}%`;
  },

  /**
   * Get color for percentage difference (red for bad, green for good)
   */
  getDifferenceColor(percentage, lowerIsBetter = true) {
    if (lowerIsBetter) {
      return percentage < 0 ? '#10B981' : '#EF4444';
    } else {
      return percentage > 0 ? '#10B981' : '#EF4444';
    }
  },

  /**
   * Calculate comparison stats between two scenarios
   */
  compareScenarios(scenario1, scenario2) {
    const comparisons = {};

    // CO₂ comparison
    const co2Diff = this.calculateDifference(
      scenario1.climate_impact.co2_per_m2_bta,
      scenario2.climate_impact.co2_per_m2_bta
    );
    comparisons.co2_per_m2 = {
      value: co2Diff,
      formatted: this.formatPercentage(co2Diff),
      color: this.getDifferenceColor(co2Diff, true)
    };

    // Material emissions comparison
    const materialDiff = this.calculateDifference(
      scenario1.climate_impact.material_emissions_per_m2,
      scenario2.climate_impact.material_emissions_per_m2
    );
    comparisons.material_emissions = {
      value: materialDiff,
      formatted: this.formatPercentage(materialDiff),
      color: this.getDifferenceColor(materialDiff, true)
    };

    // Total CO₂ comparison
    const totalDiff = this.calculateDifference(
      scenario1.climate_impact.total_co2_tonnes,
      scenario2.climate_impact.total_co2_tonnes
    );
    comparisons.total_co2 = {
      value: totalDiff,
      formatted: this.formatPercentage(totalDiff),
      color: this.getDifferenceColor(totalDiff, true)
    };

    return comparisons;
  },

  /**
   * Rank scenarios by a specific metric
   */
  rankScenarios(scenarios, metric = 'co2_per_m2') {
    const getValue = (scenario) => {
      switch (metric) {
        case 'total_co2':
          return scenario.climate_impact.total_co2_tonnes;
        case 'co2_per_m2':
          return scenario.climate_impact.co2_per_m2_bta;
        case 'material_emissions':
          return scenario.climate_impact.material_emissions_per_m2;
        case 'energy_consumption':
          const energy = scenario.energy_consumption_kwh_m2;
          return typeof energy === 'string' ? 999 : energy;
        default:
          return 0;
      }
    };

    const ranked = scenarios.map((scenario, index) => ({
      scenario,
      value: getValue(scenario),
      originalIndex: index
    }));

    // Sort by value (lower is better for all current metrics)
    ranked.sort((a, b) => a.value - b.value);

    // Add rank
    return ranked.map((item, index) => ({
      ...item,
      rank: index + 1
    }));
  },

  /**
   * Get best scenario for a specific metric
   */
  getBestScenario(scenarios, metric = 'co2_per_m2') {
    const ranked = this.rankScenarios(scenarios, metric);
    return ranked[0].scenario;
  },

  /**
   * Calculate scenario score based on multiple factors
   */
  calculateScenarioScore(scenario, weights = null) {
    // Default weights
    const defaultWeights = {
      co2_per_m2: 0.4,
      material_emissions: 0.3,
      energy_consumption: 0.2,
      social_benefit: 0.1
    };

    const w = weights || defaultWeights;

    // Normalize values (inverse for "lower is better" metrics)
    const maxCO2 = 700;
    const maxMaterial = 400;
    const maxEnergy = 250;

    const co2Score = 1 - (scenario.climate_impact.co2_per_m2_bta / maxCO2);
    const materialScore = 1 - (scenario.climate_impact.material_emissions_per_m2 / maxMaterial);

    const energyValue = typeof scenario.energy_consumption_kwh_m2 === 'string' ? 161 : scenario.energy_consumption_kwh_m2;
    const energyScore = 1 - (energyValue / maxEnergy);

    // Social benefit (higher for extension scenarios)
    const socialScore = scenario.id === 'scenario_3' ? 1 : 0.5;

    const totalScore = (
      co2Score * w.co2_per_m2 +
      materialScore * w.material_emissions +
      energyScore * w.energy_consumption +
      socialScore * w.social_benefit
    ) * 100;

    return Math.max(0, Math.min(100, totalScore));
  },

  /**
   * Generate chart data for comparison
   */
  generateChartData(scenarios, metric) {
    return scenarios.map(scenario => {
      const meta = this.getScenarioMeta(scenario.id);
      let value;

      switch (metric) {
        case 'total_co2':
          value = scenario.climate_impact.total_co2_tonnes;
          break;
        case 'co2_per_m2':
          value = scenario.climate_impact.co2_per_m2_bta;
          break;
        case 'material_emissions':
          value = scenario.climate_impact.material_emissions_per_m2;
          break;
        case 'energy_consumption':
          value = typeof scenario.energy_consumption_kwh_m2 === 'string' ? 161 : scenario.energy_consumption_kwh_m2;
          break;
        default:
          value = 0;
      }

      return {
        id: scenario.id,
        label: meta.label_no,
        value,
        color: meta.color
      };
    });
  },

  /**
   * Format number with Norwegian locale
   */
  formatNumber(value, decimals = 0) {
    if (typeof value === 'string') return value;
    return value.toLocaleString('nb-NO', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  },

  /**
   * Sanitize HTML to prevent XSS
   */
  sanitizeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },

  /**
   * SVG Icons for scenarios
   */
  icons: {
    chart() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="20" x2="12" y2="10"></line>
        <line x1="18" y1="20" x2="18" y2="4"></line>
        <line x1="6" y1="20" x2="6" y2="16"></line>
      </svg>`;
    },

    comparison() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="16 3 21 3 21 8"></polyline>
        <line x1="4" y1="20" x2="21" y2="3"></line>
        <polyline points="21 16 21 21 16 21"></polyline>
        <line x1="15" y1="15" x2="21" y2="21"></line>
        <line x1="4" y1="4" x2="9" y2="9"></line>
      </svg>`;
    },

    winner() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="8" r="7"></circle>
        <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline>
      </svg>`;
    },

    info() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
      </svg>`;
    },

    chevronDown() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>`;
    }
  }
};

// Make available globally
if (typeof window !== 'undefined') {
  window.ScenarioHelpers = ScenarioHelpers;
}
