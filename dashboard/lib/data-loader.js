/**
 * Data Loader Module
 * Loads and caches JSON data for dashboard
 */

const DataLoader = {
  cache: {},

  /**
   * Load JSON file with caching
   */
  async loadJSON(filepath) {
    if (this.cache[filepath]) {
      return this.cache[filepath];
    }

    try {
      const response = await fetch(filepath);
      if (!response.ok) {
        throw new Error(`Failed to load ${filepath}: ${response.statusText}`);
      }
      const data = await response.json();
      this.cache[filepath] = data;
      return data;
    } catch (error) {
      console.error(`Error loading ${filepath}:`, error);
      throw error;
    }
  },

  /**
   * Load all core data files
   */
  async loadAllData() {
    console.log('Loading data...');

    const [
      timelineEnhanced,
      meetings,
      people,
      organizations,
      documents,
      project,
      sustainability
    ] = await Promise.all([
      this.loadJSON('../data/timeline-enhanced.json'),
      this.loadJSON('../data/meetings.json'),
      this.loadJSON('../data/stakeholders/people.json'),
      this.loadJSON('../data/stakeholders/organizations.json'),
      this.loadJSON('../data/documents.json'),
      this.loadJSON('../data/project.json'),
      this.loadJSON('../data/themes/sustainability.json')
    ]);

    console.log('✓ All data loaded');

    return {
      timeline: timelineEnhanced,
      meetings: meetings.meetings,
      people: people.people,
      organizations: organizations.organizations,
      documents: documents.documents,
      project,
      sustainability
    };
  },

  /**
   * Get meeting by ID
   */
  getMeetingById(meetings, meetingId) {
    return meetings.find(m => m.id === meetingId);
  },

  /**
   * Get person by ID
   */
  getPersonById(people, personId) {
    return people.find(p => p.id === personId);
  },

  /**
   * Get organization by ID
   */
  getOrganizationById(organizations, orgId) {
    return organizations.find(o => o.id === orgId);
  },

  /**
   * Get document by ID
   */
  getDocumentById(documents, docId) {
    return documents.find(d => d.id === docId);
  },

  /**
   * Get meetings for specific date
   */
  getMeetingsByDate(meetings, date) {
    return meetings.filter(m => m.date === date);
  },

  /**
   * Search across all data
   */
  search(data, query) {
    const q = query.toLowerCase();
    const results = {
      events: [],
      meetings: [],
      people: [],
      documents: []
    };

    // Search strategic events
    data.timeline.events.strategic.forEach(event => {
      const searchableText = [
        event.title,
        event.title_no,
        event.description,
        ...(event.exec_summary || []),
        ...(event.tags || [])
      ].join(' ').toLowerCase();

      if (searchableText.includes(q)) {
        results.events.push({ ...event, layer: 'strategic' });
      }
    });

    // Search operational events
    data.timeline.events.operational.forEach(event => {
      const searchableText = [
        event.title,
        event.title_no,
        event.description || ''
      ].join(' ').toLowerCase();

      if (searchableText.includes(q)) {
        results.events.push({ ...event, layer: 'operational' });
      }
    });

    // Search meetings
    data.meetings.forEach(meeting => {
      const searchableText = [
        meeting.title,
        meeting.location || '',
        ...(meeting.participants || []).map(p => p.name)
      ].join(' ').toLowerCase();

      if (searchableText.includes(q)) {
        results.meetings.push(meeting);
      }
    });

    // Search people
    data.people.forEach(person => {
      const searchableText = [
        person.name,
        person.organization || '',
        person.role || '',
        person.bio || ''
      ].join(' ').toLowerCase();

      if (searchableText.includes(q)) {
        results.people.push(person);
      }
    });

    // Search documents
    data.documents.forEach(doc => {
      const searchableText = [
        doc.title,
        doc.title_no || '',
        doc.category,
        doc.description || ''
      ].join(' ').toLowerCase();

      if (searchableText.includes(q)) {
        results.documents.push(doc);
      }
    });

    return results;
  },

  /**
   * Filter events by criteria
   */
  filterEvents(events, filters) {
    return events.filter(event => {
      // Filter by phase
      if (filters.phase && event.phase !== filters.phase) {
        return false;
      }

      // Filter by importance
      if (filters.importance && event.importance !== filters.importance) {
        return false;
      }

      // Filter by tags
      if (filters.tags && filters.tags.length > 0) {
        if (!event.tags || !filters.tags.some(tag => event.tags.includes(tag))) {
          return false;
        }
      }

      // Filter by has meeting
      if (filters.hasMeeting !== undefined) {
        const hasMeeting = event.linked_meetings && event.linked_meetings.length > 0;
        if (filters.hasMeeting !== hasMeeting) {
          return false;
        }
      }

      // Filter by date range
      if (filters.dateFrom && event.date < filters.dateFrom) {
        return false;
      }
      if (filters.dateTo && event.date > filters.dateTo) {
        return false;
      }

      return true;
    });
  },

  /**
   * Search documents by filename, category, and source folder
   */
  searchDocuments(documents, query) {
    const q = query.toLowerCase().trim();
    if (!q) return documents;

    return documents.filter(doc => {
      const searchableText = [
        doc.file_name,
        doc.category,
        doc.source_folder,
        doc.id
      ].join(' ').toLowerCase();

      return searchableText.includes(q);
    });
  },

  /**
   * Get documents by category
   */
  getDocumentsByCategory(documents, category) {
    return documents.filter(d => d.category === category);
  },

  /**
   * Filter documents by criteria
   */
  filterDocuments(documents, filters) {
    return documents.filter(doc => {
      // Filter by category
      if (filters.category && filters.category !== 'all' && doc.category !== filters.category) {
        return false;
      }

      // Filter by file type
      if (filters.fileType && filters.fileType !== 'all' && doc.file_type !== filters.fileType) {
        return false;
      }

      // Filter by source folder
      if (filters.source && filters.source !== 'all' && doc.source_folder !== filters.source) {
        return false;
      }

      return true;
    });
  },

  /**
   * Sort documents by criteria
   */
  sortDocuments(documents, sortBy) {
    const sorted = [...documents];

    switch (sortBy) {
      case 'newest':
        return sorted.sort((a, b) => new Date(b.extraction_date) - new Date(a.extraction_date));
      case 'oldest':
        return sorted.sort((a, b) => new Date(a.extraction_date) - new Date(b.extraction_date));
      case 'name-asc':
        return sorted.sort((a, b) => a.file_name.localeCompare(b.file_name));
      case 'name-desc':
        return sorted.sort((a, b) => b.file_name.localeCompare(a.file_name));
      case 'category':
        return sorted.sort((a, b) => a.category.localeCompare(b.category));
      default:
        return sorted;
    }
  },

  /**
   * Get unique file types from documents
   */
  getUniqueFileTypes(documents) {
    const types = new Set(documents.map(d => d.file_type));
    return Array.from(types).sort();
  },

  /**
   * Get unique source folders from documents
   */
  getUniqueSourceFolders(documents) {
    const sources = new Set(documents.map(d => d.source_folder));
    return Array.from(sources).sort();
  },

  /**
   * Group documents by category
   */
  groupDocumentsByCategory(documents) {
    const groups = {};
    documents.forEach(doc => {
      if (!groups[doc.category]) {
        groups[doc.category] = [];
      }
      groups[doc.category].push(doc);
    });
    return groups;
  },

  /**
   * Convert people object to array
   */
  getPeopleArray(peopleObj) {
    return Object.values(peopleObj);
  },

  /**
   * Convert organizations object to array
   */
  getOrganizationsArray(orgsObj) {
    return Object.values(orgsObj);
  },

  /**
   * Search stakeholders (people + organizations)
   */
  searchStakeholders(people, organizations, query) {
    const q = query.toLowerCase().trim();
    if (!q) return { people, organizations };

    const filteredPeople = people.filter(person => {
      const searchableText = [
        person.name,
        person.organization,
        person.title,
        person.role_in_project,
        person.bio || '',
        ...(person.expertise || [])
      ].join(' ').toLowerCase();
      return searchableText.includes(q);
    });

    const filteredOrgs = organizations.filter(org => {
      const searchableText = [
        org.name,
        org.type,
        org.category,
        org.description,
        org.role_in_project,
        ...(org.expertise || [])
      ].join(' ').toLowerCase();
      return searchableText.includes(q);
    });

    return { people: filteredPeople, organizations: filteredOrgs };
  },

  /**
   * Filter people by criteria
   */
  filterPeople(people, filters) {
    return people.filter(person => {
      if (filters.category && filters.category !== 'all' && person.category !== filters.category) {
        return false;
      }
      if (filters.organization && filters.organization !== 'all' && person.organization_id !== filters.organization) {
        return false;
      }
      return true;
    });
  },

  /**
   * Filter organizations by criteria
   */
  filterOrganizations(organizations, filters) {
    return organizations.filter(org => {
      if (filters.category && filters.category !== 'all' && org.category !== filters.category) {
        return false;
      }
      if (filters.type && filters.type !== 'all' && org.type !== filters.type) {
        return false;
      }
      return true;
    });
  },

  /**
   * Get unique person categories
   */
  getPersonCategories(people) {
    const categories = new Set(people.map(p => p.category).filter(Boolean));
    return Array.from(categories).sort();
  },

  /**
   * Get unique organization categories
   */
  getOrganizationCategories(organizations) {
    const categories = new Set(organizations.map(o => o.category).filter(Boolean));
    return Array.from(categories).sort();
  },

  /**
   * Get unique organization types
   */
  getOrganizationTypes(organizations) {
    const types = new Set(organizations.map(o => o.type).filter(Boolean));
    return Array.from(types).sort();
  },

  /**
   * Group people by category
   */
  groupPeopleByCategory(people) {
    const groups = {};
    people.forEach(person => {
      const category = person.category || 'Other';
      if (!groups[category]) {
        groups[category] = [];
      }
      groups[category].push(person);
    });
    return groups;
  },

  /**
   * Group organizations by category
   */
  groupOrganizationsByCategory(organizations) {
    const groups = {};
    organizations.forEach(org => {
      const category = org.category || 'Other';
      if (!groups[category]) {
        groups[category] = [];
      }
      groups[category].push(org);
    });
    return groups;
  },

  /**
   * Get people by organization
   */
  getPeopleByOrganization(people, orgId) {
    return people.filter(p => p.organization_id === orgId);
  },

  // ===== MEETING FUNCTIONS =====

  /**
   * Search meetings by title, participants, organization, location
   */
  searchMeetings(meetings, query) {
    const q = query.toLowerCase().trim();
    if (!q) return meetings;

    return meetings.filter(meeting => {
      const searchableText = [
        meeting.title,
        meeting.location || '',
        meeting.organizer || '',
        ...(meeting.participants || []).map(p => p.name),
        ...(meeting.participants || []).map(p => p.organization),
        ...(meeting.participants || []).map(p => p.email)
      ].join(' ').toLowerCase();

      return searchableText.includes(q);
    });
  },

  /**
   * Filter meetings by criteria
   */
  filterMeetings(meetings, filters) {
    return meetings.filter(meeting => {
      // Filter by date range
      if (filters.dateFrom && meeting.date < filters.dateFrom) {
        return false;
      }
      if (filters.dateTo && meeting.date > filters.dateTo) {
        return false;
      }

      // Filter by meeting type (requires MeetingHelpers)
      if (filters.type && filters.type !== 'all' && typeof MeetingHelpers !== 'undefined') {
        const meetingType = MeetingHelpers.determineMeetingType(meeting);
        if (meetingType !== filters.type) {
          return false;
        }
      }

      // Filter by organization
      if (filters.organization && filters.organization !== 'all') {
        const orgs = (meeting.participants || []).map(p => p.organization);
        if (!orgs.includes(filters.organization)) {
          return false;
        }
      }

      // Filter by participant
      if (filters.participant && filters.participant !== 'all') {
        const participants = (meeting.participants || []).map(p => p.name);
        if (!participants.includes(filters.participant)) {
          return false;
        }
      }

      // Filter by time (past/upcoming)
      if (filters.timeFilter === 'past' && typeof MeetingHelpers !== 'undefined') {
        if (!MeetingHelpers.isPast(meeting.date)) {
          return false;
        }
      }
      if (filters.timeFilter === 'upcoming' && typeof MeetingHelpers !== 'undefined') {
        if (!MeetingHelpers.isUpcoming(meeting.date)) {
          return false;
        }
      }

      // Filter by has participants
      if (filters.hasParticipants !== undefined) {
        const hasParticipants = meeting.participants && meeting.participants.length > 0;
        if (filters.hasParticipants !== hasParticipants) {
          return false;
        }
      }

      return true;
    });
  },

  /**
   * Sort meetings by criteria
   */
  sortMeetings(meetings, sortBy) {
    const sorted = [...meetings];

    switch (sortBy) {
      case 'newest':
        return sorted.sort((a, b) => new Date(b.date) - new Date(a.date));
      case 'oldest':
        return sorted.sort((a, b) => new Date(a.date) - new Date(b.date));
      case 'title-asc':
        return sorted.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
      case 'title-desc':
        return sorted.sort((a, b) => (b.title || '').localeCompare(a.title || ''));
      case 'participants':
        return sorted.sort((a, b) => b.participant_count - a.participant_count);
      default:
        return sorted;
    }
  },

  /**
   * Group meetings by month
   */
  groupMeetingsByMonth(meetings) {
    if (typeof MeetingHelpers !== 'undefined') {
      return MeetingHelpers.groupByMonth(meetings);
    }

    // Fallback if MeetingHelpers not loaded
    const groups = {};
    meetings.forEach(meeting => {
      if (!meeting.date) return;
      const yearMonth = meeting.date.substring(0, 7); // YYYY-MM
      if (!groups[yearMonth]) {
        groups[yearMonth] = { label: yearMonth, meetings: [] };
      }
      groups[yearMonth].meetings.push(meeting);
    });
    return Object.values(groups);
  },

  /**
   * Get unique meeting types
   */
  getUniqueMeetingTypes(meetings) {
    if (typeof MeetingHelpers === 'undefined') {
      return [];
    }

    const types = new Set();
    meetings.forEach(meeting => {
      const type = MeetingHelpers.determineMeetingType(meeting);
      types.add(type);
    });
    return Array.from(types).sort();
  },

  /**
   * Get unique organizations from meetings
   */
  getUniqueOrganizationsFromMeetings(meetings) {
    const orgs = new Set();
    meetings.forEach(meeting => {
      (meeting.participants || []).forEach(p => {
        if (p.organization) orgs.add(p.organization);
      });
    });
    return Array.from(orgs).sort();
  },

  /**
   * Get unique participants from meetings
   */
  getUniqueParticipants(meetings) {
    const participants = new Set();
    meetings.forEach(meeting => {
      (meeting.participants || []).forEach(p => {
        if (p.name) participants.add(p.name);
      });
    });
    return Array.from(participants).sort();
  },

  /**
   * Get meetings by participant
   */
  getMeetingsByParticipant(meetings, participantName) {
    return meetings.filter(meeting => {
      return (meeting.participants || []).some(p => p.name === participantName);
    });
  },

  /**
   * Get meetings by organization
   */
  getMeetingsByOrganization(meetings, organizationName) {
    return meetings.filter(meeting => {
      return (meeting.participants || []).some(p => p.organization === organizationName);
    });
  },

  /**
   * Get past meetings
   */
  getPastMeetings(meetings) {
    if (typeof MeetingHelpers === 'undefined') {
      const now = new Date();
      return meetings.filter(m => m.date && new Date(m.date) < now);
    }
    return meetings.filter(m => MeetingHelpers.isPast(m.date));
  },

  /**
   * Get upcoming meetings
   */
  getUpcomingMeetings(meetings) {
    if (typeof MeetingHelpers === 'undefined') {
      const now = new Date();
      return meetings.filter(m => m.date && new Date(m.date) >= now);
    }
    return meetings.filter(m => MeetingHelpers.isUpcoming(m.date));
  },

  /**
   * Get meeting statistics
   */
  getMeetingStatistics(meetings) {
    if (typeof MeetingHelpers !== 'undefined') {
      return MeetingHelpers.getStatistics(meetings);
    }

    // Fallback basic stats
    return {
      total: meetings.length,
      past: this.getPastMeetings(meetings).length,
      upcoming: this.getUpcomingMeetings(meetings).length
    };
  },

  // ===== SCENARIO FUNCTIONS =====

  /**
   * Get scenarios from project data
   */
  getScenarios(projectData) {
    if (!projectData || !projectData.scenarios || !projectData.scenarios.options) {
      return [];
    }
    return projectData.scenarios.options;
  },

  /**
   * Get scenario by ID
   */
  getScenarioById(scenarios, scenarioId) {
    return scenarios.find(s => s.id === scenarioId);
  },

  /**
   * Get preferred scenario
   */
  getPreferredScenario(projectData) {
    const scenarios = this.getScenarios(projectData);
    const preferredId = projectData.scenarios?.preferred;
    if (!preferredId) return null;
    return this.getScenarioById(scenarios, preferredId);
  },

  /**
   * Compare scenario against baseline (demolition)
   */
  compareToBaseline(scenario, baseline) {
    if (!baseline || !scenario) return null;

    const co2Diff = ((scenario.climate_impact.co2_per_m2_bta - baseline.climate_impact.co2_per_m2_bta) / baseline.climate_impact.co2_per_m2_bta) * 100;
    const materialDiff = ((scenario.climate_impact.material_emissions_per_m2 - baseline.climate_impact.material_emissions_per_m2) / baseline.climate_impact.material_emissions_per_m2) * 100;
    const totalDiff = ((scenario.climate_impact.total_co2_tonnes - baseline.climate_impact.total_co2_tonnes) / baseline.climate_impact.total_co2_tonnes) * 100;

    return {
      co2_per_m2: co2Diff,
      material_emissions: materialDiff,
      total_co2: totalDiff,
      co2_saved_tonnes: baseline.climate_impact.total_co2_tonnes - scenario.climate_impact.total_co2_tonnes
    };
  },

  /**
   * Rank scenarios by a specific metric
   */
  rankScenariosByMetric(scenarios, metric = 'co2_per_m2') {
    if (typeof ScenarioHelpers !== 'undefined') {
      return ScenarioHelpers.rankScenarios(scenarios, metric);
    }

    // Fallback simple ranking
    const getValue = (scenario) => {
      switch (metric) {
        case 'total_co2':
          return scenario.climate_impact.total_co2_tonnes;
        case 'co2_per_m2':
          return scenario.climate_impact.co2_per_m2_bta;
        case 'material_emissions':
          return scenario.climate_impact.material_emissions_per_m2;
        default:
          return 0;
      }
    };

    return scenarios
      .map((s, i) => ({ scenario: s, value: getValue(s), index: i }))
      .sort((a, b) => a.value - b.value)
      .map((item, rank) => ({ ...item, rank: rank + 1 }));
  },

  /**
   * Get best scenario for a specific metric
   */
  getBestScenarioFor(scenarios, metric) {
    const ranked = this.rankScenariosByMetric(scenarios, metric);
    return ranked[0]?.scenario;
  },

  /**
   * Calculate scenario statistics
   */
  getScenarioStatistics(scenarios) {
    if (!scenarios || scenarios.length === 0) {
      return {
        total: 0,
        recommended: 0,
        preferred: null
      };
    }

    const stats = {
      total: scenarios.length,
      recommended: scenarios.filter(s => s.status?.includes('Recommended')).length,
      preferred: scenarios.find(s => s.status?.includes('Preferred'))?.id || null,
      metrics: {
        co2_range: {
          min: Math.min(...scenarios.map(s => s.climate_impact.co2_per_m2_bta)),
          max: Math.max(...scenarios.map(s => s.climate_impact.co2_per_m2_bta))
        },
        material_range: {
          min: Math.min(...scenarios.map(s => s.climate_impact.material_emissions_per_m2)),
          max: Math.max(...scenarios.map(s => s.climate_impact.material_emissions_per_m2))
        }
      }
    };

    return stats;
  },

  /**
   * Generate comparison matrix for all scenarios
   */
  generateComparisonMatrix(scenarios) {
    const baseline = scenarios.find(s => s.id === 'scenario_1'); // Demolition
    if (!baseline) return [];

    return scenarios.map(scenario => {
      if (scenario.id === baseline.id) {
        return {
          scenario,
          comparison: null,
          isBaseline: true
        };
      }

      return {
        scenario,
        comparison: this.compareToBaseline(scenario, baseline),
        isBaseline: false
      };
    });
  },

  // ===== PROJECT OVERVIEW FUNCTIONS =====

  /**
   * Extract all decisions across meetings with context
   */
  extractAllDecisions(meetings) {
    const decisions = [];

    meetings.forEach(meeting => {
      // From report.decisions
      if (meeting.report && meeting.report.decisions) {
        meeting.report.decisions.forEach(decision => {
          decisions.push({
            decision: decision,
            meeting_id: meeting.id,
            meeting_title: meeting.title,
            meeting_date: meeting.date,
            source: 'report'
          });
        });
      }

      // From legacy decisions field
      if (meeting.decisions && !meeting.report) {
        meeting.decisions.forEach(decision => {
          decisions.push({
            decision: decision,
            meeting_id: meeting.id,
            meeting_title: meeting.title,
            meeting_date: meeting.date,
            source: 'legacy'
          });
        });
      }
    });

    // Sort by date (newest first)
    return decisions.sort((a, b) => b.meeting_date.localeCompare(a.meeting_date));
  },

  /**
   * Extract all action items across meetings with details
   */
  extractAllActionItems(meetings) {
    const actionItems = [];

    meetings.forEach(meeting => {
      // From report.action_items (structured)
      if (meeting.report && meeting.report.action_items) {
        meeting.report.action_items.forEach(item => {
          actionItems.push({
            task: item.task,
            responsible: item.responsible || 'Not assigned',
            deadline: item.deadline || 'No deadline',
            meeting_id: meeting.id,
            meeting_title: meeting.title,
            meeting_date: meeting.date,
            source: 'report',
            status: this.inferActionStatus(item, meeting.date)
          });
        });
      }

      // From legacy action_items field (strings)
      if (meeting.action_items && !meeting.report) {
        meeting.action_items.forEach(item => {
          actionItems.push({
            task: item,
            responsible: 'Not assigned',
            deadline: 'No deadline',
            meeting_id: meeting.id,
            meeting_title: meeting.title,
            meeting_date: meeting.date,
            source: 'legacy',
            status: 'unknown'
          });
        });
      }
    });

    // Sort by date (newest first)
    return actionItems.sort((a, b) => b.meeting_date.localeCompare(a.meeting_date));
  },

  /**
   * Infer action item status based on deadline and meeting date
   */
  inferActionStatus(item, meetingDate) {
    if (!item.deadline || item.deadline === 'No deadline') return 'pending';

    const today = new Date().toISOString().split('T')[0];
    const deadlineDate = this.parseNorwegianDate(item.deadline);

    if (!deadlineDate) return 'pending';

    if (deadlineDate < today) return 'overdue';
    if (deadlineDate === today) return 'due-today';
    return 'pending';
  },

  /**
   * Parse Norwegian date formats (e.g., "April 2024", "Q2 2024")
   */
  parseNorwegianDate(dateStr) {
    if (!dateStr) return null;

    // ISO format
    if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/)) return dateStr;

    // Month year format: "April 2024"
    const monthMatch = dateStr.match(/(\w+)\s+(\d{4})/);
    if (monthMatch) {
      const months = {
        'januar': '01', 'februar': '02', 'mars': '03', 'april': '04',
        'mai': '05', 'juni': '06', 'juli': '07', 'august': '08',
        'september': '09', 'oktober': '10', 'november': '11', 'desember': '12',
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
      };
      const monthNum = months[monthMatch[1].toLowerCase()];
      if (monthNum) return `${monthMatch[2]}-${monthNum}-01`;
    }

    // Quarter format: "Q2 2024"
    const quarterMatch = dateStr.match(/Q(\d)\s+(\d{4})/);
    if (quarterMatch) {
      const quarter = parseInt(quarterMatch[1]);
      const year = quarterMatch[2];
      const month = (quarter - 1) * 3 + 1;
      return `${year}-${String(month).padStart(2, '0')}-01`;
    }

    return null;
  },

  /**
   * Calculate meeting statistics
   */
  calculateMeetingStats(meetings) {
    const today = new Date().toISOString().split('T')[0];

    const stats = {
      total: meetings.length,
      past: 0,
      upcoming: 0,
      withReports: 0,
      withDecisions: 0,
      withActionItems: 0,
      totalDecisions: 0,
      totalActionItems: 0,
      byType: {},
      byMonth: {},
      participantEngagement: {}
    };

    meetings.forEach(meeting => {
      // Past/upcoming
      if (meeting.date < today) {
        stats.past++;
      } else {
        stats.upcoming++;
      }

      // Reports
      if (meeting.report) stats.withReports++;

      // Decisions
      const hasDecisions = (meeting.report && meeting.report.decisions && meeting.report.decisions.length > 0) ||
                          (meeting.decisions && meeting.decisions.length > 0);
      if (hasDecisions) {
        stats.withDecisions++;
        stats.totalDecisions += (meeting.report?.decisions?.length || meeting.decisions?.length || 0);
      }

      // Action items
      const hasActions = (meeting.report && meeting.report.action_items && meeting.report.action_items.length > 0) ||
                        (meeting.action_items && meeting.action_items.length > 0);
      if (hasActions) {
        stats.withActionItems++;
        stats.totalActionItems += (meeting.report?.action_items?.length || meeting.action_items?.length || 0);
      }

      // By type
      const type = meeting.meeting_type || 'other';
      stats.byType[type] = (stats.byType[type] || 0) + 1;

      // By month
      const month = meeting.date.substring(0, 7); // YYYY-MM
      stats.byMonth[month] = (stats.byMonth[month] || 0) + 1;

      // Participant engagement
      (meeting.participants || []).forEach(p => {
        const name = p.name;
        if (!stats.participantEngagement[name]) {
          stats.participantEngagement[name] = {
            name: name,
            organization: p.organization,
            meetings: 0,
            lastMeeting: null
          };
        }
        stats.participantEngagement[name].meetings++;
        if (!stats.participantEngagement[name].lastMeeting || meeting.date > stats.participantEngagement[name].lastMeeting) {
          stats.participantEngagement[name].lastMeeting = meeting.date;
        }
      });
    });

    return stats;
  },

  /**
   * Get recent activity (meetings, decisions, actions)
   */
  getRecentActivity(meetings, limit = 10) {
    const activities = [];

    // Sort meetings by date (newest first)
    const sortedMeetings = [...meetings].sort((a, b) => b.date.localeCompare(a.date));

    sortedMeetings.slice(0, limit).forEach(meeting => {
      activities.push({
        type: 'meeting',
        date: meeting.date,
        title: meeting.title,
        meeting_id: meeting.id,
        details: `${meeting.participant_count} deltakere`
      });

      // Add decisions from this meeting
      if (meeting.report && meeting.report.decisions) {
        meeting.report.decisions.slice(0, 2).forEach(decision => {
          activities.push({
            type: 'decision',
            date: meeting.date,
            title: decision,
            meeting_id: meeting.id,
            meeting_title: meeting.title
          });
        });
      }

      // Add action items from this meeting
      if (meeting.report && meeting.report.action_items) {
        meeting.report.action_items.slice(0, 2).forEach(item => {
          activities.push({
            type: 'action',
            date: meeting.date,
            title: item.task,
            responsible: item.responsible,
            meeting_id: meeting.id,
            meeting_title: meeting.title
          });
        });
      }
    });

    // Sort all activities by date
    return activities.sort((a, b) => b.date.localeCompare(a.date)).slice(0, limit);
  },

  /**
   * Get stakeholder engagement ranking
   */
  getStakeholderEngagement(meetings) {
    const stats = this.calculateMeetingStats(meetings);
    const engagement = Object.values(stats.participantEngagement);

    // Sort by number of meetings (most active first)
    return engagement.sort((a, b) => b.meetings - a.meetings);
  },

  /**
   * Calculate project health indicators
   */
  calculateProjectHealth(meetings, events) {
    const today = new Date().toISOString().split('T')[0];
    const stats = this.calculateMeetingStats(meetings);

    // Meeting frequency (meetings per month in last 6 months)
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
    const sixMonthsAgoStr = sixMonthsAgo.toISOString().split('T')[0];

    const recentMeetings = meetings.filter(m => m.date >= sixMonthsAgoStr && m.date <= today);
    const meetingFrequency = recentMeetings.length / 6;

    // Documentation coverage
    const documentationCoverage = (stats.withReports / stats.total) * 100;

    // Decision velocity (decisions per meeting)
    const decisionVelocity = stats.totalDecisions / stats.total;

    // Action tracking (percentage of meetings with action items)
    const actionTracking = (stats.withActionItems / stats.total) * 100;

    return {
      meetingFrequency: meetingFrequency.toFixed(1),
      documentationCoverage: documentationCoverage.toFixed(0),
      decisionVelocity: decisionVelocity.toFixed(1),
      actionTracking: actionTracking.toFixed(0),
      totalMeetings: stats.total,
      totalDecisions: stats.totalDecisions,
      totalActions: stats.totalActionItems
    };
  }
};

// Export for use in browser
if (typeof window !== 'undefined') {
  window.DataLoader = DataLoader;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DataLoader;
}
