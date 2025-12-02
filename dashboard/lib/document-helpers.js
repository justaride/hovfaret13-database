/**
 * Document Helpers Module
 * Utilities for document handling and formatting
 */

const DocumentHelpers = {
  /**
   * Category metadata with icons, colors, and descriptions
   */
  CATEGORY_META: {
    'sustainability': {
      icon: 'recycle',
      label: 'Sustainability',
      description: 'Energy reports, climate calculations, environmental assessments',
      color: '#10B981'
    },
    'omsorg_plus': {
      icon: 'heart',
      label: 'Omsorg+',
      description: 'Omsorg+ concept documents and references',
      color: '#8B5CF6'
    },
    'stakeholder_engagement': {
      icon: 'users',
      label: 'Stakeholder Engagement',
      description: 'Tenant communications, neighbor meetings',
      color: '#06B6D4'
    },
    'presentations': {
      icon: 'presentation',
      label: 'Presentations',
      description: 'Project presentations and slides',
      color: '#F59E0B'
    },
    'meetings': {
      icon: 'file-text',
      label: 'Meetings',
      description: 'Meeting reports and protocols',
      color: '#3B82F6'
    },
    'architecture': {
      icon: 'drafting-compass',
      label: 'Architecture',
      description: 'R21 architectural drawings and plans',
      color: '#EF4444'
    },
    'regulatory': {
      icon: 'scale',
      label: 'Regulatory',
      description: 'Planning submissions and regulatory documents',
      color: '#EC4899'
    },
    'analysis_notes': {
      icon: 'clipboard-list',
      label: 'Analysis Notes',
      description: 'Claude analysis notes and working documents',
      color: '#6B7280'
    },
    'communications': {
      icon: 'megaphone',
      label: 'Communications',
      description: 'External communications and media',
      color: '#14B8A6'
    },
    'other': {
      icon: 'package',
      label: 'Other',
      description: 'Miscellaneous documents',
      color: '#9CA3AF'
    }
  },

  /**
   * File type metadata with icons and labels
   */
  FILE_TYPE_META: {
    'pdf_document': {
      icon: 'pdf',
      label: 'PDF',
      color: '#EF4444'
    },
    'google_doc_link': {
      icon: 'doc',
      label: 'Google Doc',
      color: '#3B82F6'
    },
    'generic_excel': {
      icon: 'excel',
      label: 'Excel',
      color: '#10B981'
    },
    'word_document': {
      icon: 'word',
      label: 'Word',
      color: '#3B82F6'
    },
    'markdown_document': {
      icon: 'markdown',
      label: 'Markdown',
      color: '#F59E0B'
    },
    'unknown': {
      icon: 'file',
      label: 'File',
      color: '#9CA3AF'
    }
  },

  /**
   * Get category metadata
   */
  getCategoryMeta(category) {
    return this.CATEGORY_META[category] || {
      icon: '📄',
      label: category,
      description: '',
      color: '#9CA3AF'
    };
  },

  /**
   * Get file type metadata
   */
  getFileTypeMeta(fileType) {
    return this.FILE_TYPE_META[fileType] || this.FILE_TYPE_META['unknown'];
  },

  /**
   * Truncate text with ellipsis
   */
  truncate(text, maxLength = 40) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
  },

  /**
   * Format date to Norwegian style
   */
  formatDate(dateString) {
    if (!dateString) return '';

    try {
      const date = new Date(dateString);
      const day = date.getDate();
      const months = [
        'januar', 'februar', 'mars', 'april', 'mai', 'juni',
        'juli', 'august', 'september', 'oktober', 'november', 'desember'
      ];
      const month = months[date.getMonth()];
      const year = date.getFullYear();

      return `${day}. ${month} ${year}`;
    } catch (e) {
      return dateString;
    }
  },

  /**
   * Format date to short format (DD.MM.YYYY)
   */
  formatDateShort(dateString) {
    if (!dateString) return '';

    try {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();

      return `${day}.${month}.${year}`;
    } catch (e) {
      return dateString;
    }
  },

  /**
   * Calculate statistics from documents
   */
  calculateStats(documents) {
    const stats = {
      total: documents.length,
      byCategory: {},
      byFileType: {},
      bySourceFolder: {},
      dateRange: {
        earliest: null,
        latest: null
      }
    };

    documents.forEach(doc => {
      // Count by category
      stats.byCategory[doc.category] = (stats.byCategory[doc.category] || 0) + 1;

      // Count by file type
      stats.byFileType[doc.file_type] = (stats.byFileType[doc.file_type] || 0) + 1;

      // Count by source folder
      stats.bySourceFolder[doc.source_folder] = (stats.bySourceFolder[doc.source_folder] || 0) + 1;

      // Track date range
      if (doc.extraction_date) {
        const date = new Date(doc.extraction_date);
        if (!stats.dateRange.earliest || date < stats.dateRange.earliest) {
          stats.dateRange.earliest = date;
        }
        if (!stats.dateRange.latest || date > stats.dateRange.latest) {
          stats.dateRange.latest = date;
        }
      }
    });

    return stats;
  },

  /**
   * Get SVG icon for file type
   */
  getFileTypeIcon(fileType) {
    const meta = this.getFileTypeMeta(fileType);

    const icons = {
      'pdf': `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 1h7l3 3v9a2 2 0 01-2 2H3a2 2 0 01-2-2V3a2 2 0 012-2z" stroke="currentColor" stroke-width="1.5" fill="none"/>
        <path d="M10 1v3h3" stroke="currentColor" stroke-width="1.5" fill="none"/>
        <text x="8" y="11" font-size="5" fill="currentColor" text-anchor="middle" font-weight="bold">PDF</text>
      </svg>`,

      'doc': `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 1h7l3 3v9a2 2 0 01-2 2H3a2 2 0 01-2-2V3a2 2 0 012-2z" stroke="currentColor" stroke-width="1.5" fill="none"/>
        <path d="M10 1v3h3M4 7h5M4 9h5M4 11h3" stroke="currentColor" stroke-width="1.5"/>
      </svg>`,

      'excel': `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 1h7l3 3v9a2 2 0 01-2 2H3a2 2 0 01-2-2V3a2 2 0 012-2z" stroke="currentColor" stroke-width="1.5" fill="none"/>
        <path d="M10 1v3h3M4 6h7M4 8h7M4 10h7M7 6v6" stroke="currentColor" stroke-width="1.5"/>
      </svg>`,

      'word': `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 1h7l3 3v9a2 2 0 01-2 2H3a2 2 0 01-2-2V3a2 2 0 012-2z" stroke="currentColor" stroke-width="1.5" fill="none"/>
        <path d="M10 1v3h3M4 7h5M4 9h5M4 11h3" stroke="currentColor" stroke-width="1.5"/>
      </svg>`,

      'markdown': `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 1h7l3 3v9a2 2 0 01-2 2H3a2 2 0 01-2-2V3a2 2 0 012-2z" stroke="currentColor" stroke-width="1.5" fill="none"/>
        <path d="M10 1v3h3M5 11V7l1.5 2 1.5-2v4M9.5 7l1.5 2 1.5-2" stroke="currentColor" stroke-width="1.5"/>
      </svg>`,

      'file': `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 1h7l3 3v9a2 2 0 01-2 2H3a2 2 0 01-2-2V3a2 2 0 012-2z" stroke="currentColor" stroke-width="1.5" fill="none"/>
        <path d="M10 1v3h3" stroke="currentColor" stroke-width="1.5" fill="none"/>
      </svg>`
    };

    return icons[meta.icon] || icons['file'];
  },

  /**
   * Get chevron icon (for expand/collapse)
   */
  getChevronIcon(isExpanded) {
    if (isExpanded) {
      return `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 10l4-4 4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>`;
    } else {
      return `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>`;
    }
  },

  /**
   * Sanitize HTML to prevent XSS
   */
  sanitizeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },

  /**
   * Generate document ID slug for DOM elements
   */
  getDocumentSlug(docId) {
    return docId.replace(/[^a-zA-Z0-9]/g, '_');
  }
};

// Export for use in browser
if (typeof window !== 'undefined') {
  window.DocumentHelpers = DocumentHelpers;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DocumentHelpers;
}
