/**
 * Stakeholder Helpers Module
 * Utilities for stakeholder handling and formatting
 */

const StakeholderHelpers = {
  /**
   * Person category metadata
   */
  PERSON_CATEGORIES: {
    'Core Team': {
      color: '#3B82F6',
      icon: 'star',
      description: 'Core project team members'
    },
    'Extended Team': {
      color: '#8B5CF6',
      icon: 'users',
      description: 'Extended team members'
    },
    'Consultants': {
      color: '#10B981',
      icon: 'briefcase',
      description: 'External consultants'
    },
    'Government Stakeholders': {
      color: '#EF4444',
      icon: 'landmark',
      description: 'Government representatives'
    }
  },

  /**
   * Organization category metadata
   */
  ORG_CATEGORIES: {
    'Core Project Team': {
      color: '#3B82F6',
      icon: 'building-2',
      description: 'Core project organizations'
    },
    'Technical Consultants': {
      color: '#10B981',
      icon: 'settings',
      description: 'Technical consulting firms'
    },
    'Government / Regulatory': {
      color: '#EF4444',
      icon: 'landmark',
      description: 'Government and regulatory bodies'
    },
    'Community / Neighbors': {
      color: '#F59E0B',
      icon: 'home',
      description: 'Community stakeholders and neighbors'
    }
  },

  /**
   * Organization type metadata
   */
  ORG_TYPES: {
    'property_owner': {
      label: 'Property Owner',
      icon: 'building-2'
    },
    'property_spv': {
      label: 'Property SPV',
      icon: 'building'
    },
    'consultant': {
      label: 'Consultant',
      icon: 'briefcase'
    },
    'government': {
      label: 'Government',
      icon: 'landmark'
    },
    'community': {
      label: 'Community',
      icon: 'users'
    },
    'neighbor_developer': {
      label: 'Neighbor/Developer',
      icon: 'home'
    }
  },

  /**
   * Engagement level colors
   */
  ENGAGEMENT_LEVELS: {
    'primary': { label: 'Primary', color: '#10B981' },
    'secondary': { label: 'Secondary', color: '#3B82F6' },
    'stakeholder': { label: 'Stakeholder', color: '#8B5CF6' },
    'supporting': { label: 'Supporting', color: '#6B7280' },
    'regulatory': { label: 'Regulatory', color: '#EF4444' },
    'neighbor': { label: 'Neighbor', color: '#F59E0B' }
  },

  /**
   * Get person category metadata
   */
  getPersonCategoryMeta(category) {
    return this.PERSON_CATEGORIES[category] || {
      color: '#9CA3AF',
      icon: 'user',
      description: category || 'Unknown'
    };
  },

  /**
   * Get organization category metadata
   */
  getOrgCategoryMeta(category) {
    return this.ORG_CATEGORIES[category] || {
      color: '#9CA3AF',
      icon: 'building-2',
      description: category || 'Unknown'
    };
  },

  /**
   * Get organization type metadata
   */
  getOrgTypeMeta(type) {
    return this.ORG_TYPES[type] || {
      label: type || 'Unknown',
      icon: 'clipboard'
    };
  },

  /**
   * Get engagement level metadata
   */
  getEngagementMeta(level) {
    return this.ENGAGEMENT_LEVELS[level] || {
      label: level || 'Unknown',
      color: '#9CA3AF'
    };
  },

  /**
   * Get person initials
   */
  getInitials(name) {
    if (!name) return '?';
    const parts = name.split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  },

  /**
   * Get avatar color from name
   */
  getAvatarColor(name) {
    const colors = [
      '#3B82F6', '#8B5CF6', '#10B981', '#F59E0B',
      '#EF4444', '#06B6D4', '#EC4899', '#14B8A6'
    ];
    if (!name) return colors[0];

    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
  },

  /**
   * Format expertise list
   */
  formatExpertise(expertise) {
    if (!expertise || expertise.length === 0) return '';
    return expertise.join(' • ');
  },

  /**
   * Sanitize HTML
   */
  sanitizeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },

  /**
   * Generate person ID slug for DOM
   */
  getPersonSlug(personId) {
    return personId.replace(/[^a-zA-Z0-9]/g, '_');
  },

  /**
   * Generate organization ID slug for DOM
   */
  getOrgSlug(orgId) {
    return orgId.replace(/[^a-zA-Z0-9]/g, '_');
  },

  /**
   * Get person icon SVG
   */
  getPersonIcon() {
    return `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="10" cy="7" r="3" stroke="currentColor" stroke-width="1.5" fill="none"/>
      <path d="M4 18c0-3.5 2.5-6 6-6s6 2.5 6 6" stroke="currentColor" stroke-width="1.5" fill="none"/>
    </svg>`;
  },

  /**
   * Get organization icon SVG
   */
  getOrgIcon() {
    return `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 18V4h7v3h7v11M3 18h14M3 18v-4h4M10 4V1M6 7h2M6 10h2M6 13h2M13 10h2M13 13h2" stroke="currentColor" stroke-width="1.5"/>
    </svg>`;
  },

  /**
   * Get email icon SVG
   */
  getEmailIcon() {
    return `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M2 4l6 4 6-4M2 4v8h12V4H2z" stroke="currentColor" stroke-width="1.5"/>
    </svg>`;
  },

  /**
   * Get phone icon SVG
   */
  getPhoneIcon() {
    return `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 2h3l1 3-2 2c1 2 3 3 3 3l2-2 3 1v3c-8 0-10-8-10-10z" stroke="currentColor" stroke-width="1.5"/>
    </svg>`;
  },

  /**
   * Get link icon SVG
   */
  getLinkIcon() {
    return `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M8 4h4v4M12 4L6 10M11 9v4H3V5h4" stroke="currentColor" stroke-width="1.5"/>
    </svg>`;
  },

  /**
   * Truncate bio text
   */
  truncateBio(bio, maxLength = 150) {
    if (!bio) return '';
    if (bio.length <= maxLength) return bio;
    return bio.substring(0, maxLength) + '...';
  }
};

// Export for browser
if (typeof window !== 'undefined') {
  window.StakeholderHelpers = StakeholderHelpers;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = StakeholderHelpers;
}
