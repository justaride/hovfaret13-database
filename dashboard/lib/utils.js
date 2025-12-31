'use strict';

/**
 * Utility Functions - Hovfaret 13 Dashboard
 * Shared utilities for all dashboard pages.
 */

const Utils = {
  /**
   * Sanitize string to prevent XSS attacks
   * @param {string} str - String to sanitize
   * @returns {string} Sanitized string
   */
  sanitize(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  },

  /**
   * Get initials from a name
   * @param {string} name - Full name
   * @returns {string} Initials (2 characters)
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
   * Get a consistent color for an avatar based on name
   * @param {string} name - Name to hash
   * @returns {string} Color hex code
   */
  getAvatarColor(name) {
    if (!name) return '#6B7280';
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return this.colors[Math.abs(hash) % this.colors.length];
  },

  /**
   * Format date in Norwegian long format
   * @param {string} dateStr - ISO date string
   * @returns {string} Formatted date (e.g., "15. januar 2025")
   */
  formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr;
    const day = date.getDate();
    const month = this.monthNames[date.getMonth()];
    const year = date.getFullYear();
    return `${day}. ${month} ${year}`;
  },

  /**
   * Format date in short format
   * @param {string} dateStr - ISO date string
   * @returns {string} Formatted date (e.g., "15.01.2025")
   */
  formatDateShort(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr;
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
  },

  /**
   * Format date as relative time in Norwegian
   * @param {string} dateStr - ISO date string
   * @returns {string} Relative time (e.g., "2 dager siden")
   */
  formatRelativeDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr;

    const now = new Date();
    const diffMs = now - date;
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'I dag';
    if (diffDays === 1) return 'I går';
    if (diffDays < 7) return `${diffDays} dager siden`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} uker siden`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} måneder siden`;
    return `${Math.floor(diffDays / 365)} år siden`;
  },

  /**
   * Truncate text to a maximum length
   * @param {string} text - Text to truncate
   * @param {number} maxLength - Maximum length
   * @returns {string} Truncated text with ellipsis if needed
   */
  truncate(text, maxLength = 100) {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
  },

  /**
   * Check if a date is in the past
   * @param {string} dateStr - ISO date string
   * @returns {boolean} True if date is in the past
   */
  isPast(dateStr) {
    if (!dateStr) return false;
    return new Date(dateStr) < new Date();
  },

  /**
   * Check if a date is in the future
   * @param {string} dateStr - ISO date string
   * @returns {boolean} True if date is in the future
   */
  isFuture(dateStr) {
    if (!dateStr) return false;
    return new Date(dateStr) > new Date();
  },

  /**
   * Convert ID to URL-safe slug
   * @param {string} id - ID to convert
   * @returns {string} URL-safe slug
   */
  toSlug(id) {
    if (!id) return '';
    return id.toLowerCase().replace(/_/g, '-');
  },

  /**
   * Debounce a function
   * @param {Function} func - Function to debounce
   * @param {number} wait - Wait time in milliseconds
   * @returns {Function} Debounced function
   */
  debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  /**
   * Format number with Norwegian thousand separators
   * @param {number} num - Number to format
   * @returns {string} Formatted number
   */
  formatNumber(num) {
    if (num === null || num === undefined) return '';
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  },

  /**
   * Parse query parameters from URL
   * @returns {Object} Query parameters as key-value pairs
   */
  getQueryParams() {
    const params = {};
    const searchParams = new URLSearchParams(window.location.search);
    for (const [key, value] of searchParams) {
      params[key] = value;
    }
    return params;
  },

  // Color palette for avatars
  colors: [
    '#3B82F6', // Blue
    '#10B981', // Green
    '#F59E0B', // Amber
    '#EF4444', // Red
    '#8B5CF6', // Purple
    '#EC4899', // Pink
    '#14B8A6', // Teal
    '#F97316'  // Orange
  ],

  // Norwegian month names
  monthNames: [
    'januar', 'februar', 'mars', 'april', 'mai', 'juni',
    'juli', 'august', 'september', 'oktober', 'november', 'desember'
  ],

  // Norwegian month names (short)
  monthNamesShort: [
    'jan', 'feb', 'mar', 'apr', 'mai', 'jun',
    'jul', 'aug', 'sep', 'okt', 'nov', 'des'
  ]
};

// Make Utils available globally
if (typeof window !== 'undefined') {
  window.Utils = Utils;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Utils;
}
