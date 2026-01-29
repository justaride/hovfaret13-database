/**
 * Meeting Helpers Module
 * Utilities for meeting handling and formatting
 */

const MeetingHelpers = {
  /**
   * Meeting type metadata with icons and colors
   */
  MEETING_TYPES: {
    'core_team': {
      label: 'Core Team',
      icon: 'star',
      color: '#3B82F6',
      description: 'Internal core team meeting'
    },
    'project_group': {
      label: 'Project Group',
      icon: 'building',
      color: '#8B5CF6',
      description: 'Full project group including consultants'
    },
    'external': {
      label: 'External',
      icon: 'handshake',
      color: '#10B981',
      description: 'Meeting with external stakeholders'
    },
    'government': {
      label: 'Government',
      icon: 'landmark',
      color: '#EF4444',
      description: 'Meeting with government officials'
    },
    'tenant': {
      label: 'Tenant',
      icon: 'home',
      color: '#F59E0B',
      description: 'Meeting with tenants'
    },
    'site_visit': {
      label: 'Site Visit',
      icon: 'map-pin',
      color: '#06B6D4',
      description: 'On-site inspection or walkthrough'
    },
    'workshop': {
      label: 'Workshop',
      icon: 'wrench',
      color: '#EC4899',
      description: 'Workshop or collaborative session'
    },
    'status': {
      label: 'Status',
      icon: 'bar-chart-2',
      color: '#14B8A6',
      description: 'Status update meeting'
    },
    'other': {
      label: 'Other',
      icon: 'calendar',
      color: '#6B7280',
      description: 'General meeting'
    }
  },

  /**
   * Determine meeting type based on title, participants, and location
   */
  determineMeetingType(meeting) {
    const title = meeting.title?.toLowerCase() || '';
    const location = meeting.location?.toLowerCase() || '';
    const participants = meeting.participants || [];
    const orgs = [...new Set(participants.map(p => p.organization))];

    // Site visit
    if (location.includes('hovfaret') || title.includes('befaring')) {
      return 'site_visit';
    }

    // Workshop
    if (title.includes('workshop')) {
      return 'workshop';
    }

    // Status meeting
    if (title.includes('status') || title.includes('oppfølging')) {
      return 'status';
    }

    // Tenant meeting
    if (title.includes('leietaker')) {
      return 'tenant';
    }

    // Government meeting
    if (title.includes('bydel') || title.includes('ullern') ||
        orgs.some(org => org?.includes('Bydel'))) {
      return 'government';
    }

    // External meeting
    if (orgs.length > 3 || orgs.some(org =>
        org && !['Natural State AS', 'Urbania Eiendom AS', 'R21 Arkitekter AS'].includes(org))) {
      return 'external';
    }

    // Project group (core team + consultants)
    if (orgs.includes('R21 Arkitekter AS') || orgs.includes('Vill Energi AS') ||
        orgs.includes('Bykon AS')) {
      return 'project_group';
    }

    // Core team (only Natural State + Urbania)
    const coreTeamOrgs = ['Natural State AS', 'Urbania Eiendom AS'];
    if (orgs.every(org => coreTeamOrgs.includes(org))) {
      return 'core_team';
    }

    return 'other';
  },

  /**
   * Format Norwegian date (long format)
   */
  formatDateLong(dateString) {
    if (!dateString) return 'Ukjent dato';
    const date = new Date(dateString);
    const options = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };
    return date.toLocaleDateString('nb-NO', options);
  },

  /**
   * Format Norwegian date (short format)
   */
  formatDateShort(dateString) {
    if (!dateString) return 'Ukjent';
    const date = new Date(dateString);
    const options = {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    };
    return date.toLocaleDateString('nb-NO', options);
  },

  /**
   * Get relative time description (e.g., "3 months ago", "in 2 months")
   */
  getRelativeTime(dateString) {
    if (!dateString) return 'Ukjent';

    const date = new Date(dateString);
    const now = new Date();
    const diffMs = date - now;
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffMonths = Math.floor(diffDays / 30);
    const diffYears = Math.floor(diffDays / 365);

    if (diffDays === 0) return 'I dag';
    if (diffDays === 1) return 'I morgen';
    if (diffDays === -1) return 'I går';

    if (diffDays > 0) {
      // Future
      if (diffDays < 7) return `Om ${diffDays} dager`;
      if (diffDays < 30) return `Om ${Math.floor(diffDays / 7)} uker`;
      if (diffMonths < 12) return `Om ${diffMonths} måneder`;
      return `Om ${diffYears} år`;
    } else {
      // Past
      const absDays = Math.abs(diffDays);
      const absMonths = Math.abs(diffMonths);
      const absYears = Math.abs(diffYears);

      if (absDays < 7) return `${absDays} dager siden`;
      if (absDays < 30) return `${Math.floor(absDays / 7)} uker siden`;
      if (absMonths < 12) return `${absMonths} måneder siden`;
      return `${absYears} år siden`;
    }
  },

  /**
   * Check if meeting is in the past
   */
  isPast(dateString) {
    if (!dateString) return false;
    const date = new Date(dateString);
    const now = new Date();
    return date < now;
  },

  /**
   * Check if meeting is upcoming
   */
  isUpcoming(dateString) {
    if (!dateString) return false;
    const date = new Date(dateString);
    const now = new Date();
    return date >= now;
  },

  /**
   * Get unique organizations from meeting
   */
  getUniqueOrganizations(meeting) {
    if (!meeting.participants) return [];
    const orgs = meeting.participants
      .map(p => p.organization)
      .filter(org => org);
    return [...new Set(orgs)];
  },

  /**
   * Get unique participants count (real count, not placeholder)
   */
  getRealParticipantCount(meeting) {
    if (!meeting.participants || meeting.participants.length === 0) {
      return 0;
    }
    return meeting.participants.length;
  },

  /**
   * Truncate text to max length
   */
  truncate(text, maxLength = 100) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
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
   * SVG Icons
   */
  icons: {
    calendar() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="16" y1="2" x2="16" y2="6"></line>
        <line x1="8" y1="2" x2="8" y2="6"></line>
        <line x1="3" y1="10" x2="21" y2="10"></line>
      </svg>`;
    },

    location() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
        <circle cx="12" cy="10" r="3"></circle>
      </svg>`;
    },

    people() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>`;
    },

    organization() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>`;
    },

    email() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
        <polyline points="22,6 12,13 2,6"></polyline>
      </svg>`;
    },

    warning() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
        <line x1="12" y1="9" x2="12" y2="13"></line>
        <line x1="12" y1="17" x2="12.01" y2="17"></line>
      </svg>`;
    },

    chevronDown() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>`;
    },

    chevronUp() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
      </svg>`;
    },

    timeline() {
      return `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="2" x2="12" y2="22"></line>
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
      </svg>`;
    }
  },

  /**
   * Generate avatar color based on name
   */
  getAvatarColor(name) {
    if (!name) return '#6B7280';

    const colors = [
      '#EF4444', '#F59E0B', '#10B981', '#3B82F6',
      '#8B5CF6', '#EC4899', '#06B6D4', '#14B8A6'
    ];

    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }

    return colors[Math.abs(hash) % colors.length];
  },

  /**
   * Get initials from name
   */
  getInitials(name) {
    if (!name) return '?';
    const parts = name.trim().split(' ');
    if (parts.length === 1) {
      return parts[0].substring(0, 2).toUpperCase();
    }
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  },

  /**
   * Group meetings by year and month
   */
  groupByMonth(meetings) {
    const groups = {};

    meetings.forEach(meeting => {
      if (!meeting.date) return;

      const date = new Date(meeting.date);
      const year = date.getFullYear();
      const month = date.getMonth();
      const monthNames = [
        'Januar', 'Februar', 'Mars', 'April', 'Mai', 'Juni',
        'Juli', 'August', 'September', 'Oktober', 'November', 'Desember'
      ];

      const key = `${year}-${String(month + 1).padStart(2, '0')}`;
      const label = `${monthNames[month]} ${year}`;

      if (!groups[key]) {
        groups[key] = {
          label,
          year,
          month,
          meetings: []
        };
      }

      groups[key].meetings.push(meeting);
    });

    return Object.values(groups).sort((a, b) => {
      if (a.year !== b.year) return b.year - a.year;
      return b.month - a.month;
    });
  },

  /**
   * Get meeting statistics
   */
  getStatistics(meetings) {
    const total = meetings.length;
    const past = meetings.filter(m => this.isPast(m.date)).length;
    const upcoming = meetings.filter(m => this.isUpcoming(m.date)).length;

    const types = {};
    meetings.forEach(meeting => {
      const type = this.determineMeetingType(meeting);
      types[type] = (types[type] || 0) + 1;
    });

    const allOrgs = new Set();
    const allParticipants = new Set();
    meetings.forEach(meeting => {
      this.getUniqueOrganizations(meeting).forEach(org => allOrgs.add(org));
      (meeting.participants || []).forEach(p => {
        if (p.name) allParticipants.add(p.name);
      });
    });

    return {
      total,
      past,
      upcoming,
      types,
      totalOrganizations: allOrgs.size,
      totalParticipants: allParticipants.size
    };
  }
};

// Make available globally
if (typeof window !== 'undefined') {
  window.MeetingHelpers = MeetingHelpers;
}
