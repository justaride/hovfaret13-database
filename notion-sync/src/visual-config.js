/**
 * Visual configuration for Notion database presentation
 * Defines icons, colors, and styling for each database type
 */

// Organization icons based on type
export const organizationIcons = {
  'Consultant': '🏢',
  'Government': '🏛️',
  'Owner': '🔑',
  'Contractor': '🔧',
  'Architect': '📐',
  'Engineering': '⚙️',
  'Legal': '⚖️',
  'Financial': '💰',
  'default': '🏢'
};

// People icons based on category/role
export const peopleIcons = {
  'Project Owner': '👔',
  'Consultant': '💼',
  'Architect': '📐',
  'Engineer': '⚙️',
  'Government': '🏛️',
  'Legal': '⚖️',
  'Financial': '💰',
  'Technical': '🔧',
  'default': '👤'
};

// Meeting icons based on type/topics
export const meetingIcons = {
  'strategic': '🎯',
  'regulatory': '📋',
  'technical': '⚙️',
  'sustainability': '🌱',
  'stakeholder': '🤝',
  'planning': '📅',
  'review': '🔍',
  'default': '🗣️'
};

// Document icons based on category
export const documentIcons = {
  'Report': '📊',
  'Technical': '⚙️',
  'Regulatory': '📋',
  'Financial': '💰',
  'Presentation': '📽️',
  'Contract': '📝',
  'Drawing': '📐',
  'Photo': '📷',
  'default': '📄'
};

// Timeline icons based on type
export const timelineIcons = {
  'strategic': '🎯',
  'operational': '⚡',
  'milestone': '🏁',
  'deadline': '⏰',
  'meeting': '🗣️',
  'submission': '📤',
  'approval': '✅',
  'default': '📅'
};

// Deliverable icons based on status
export const deliverableIcons = {
  'completed': '✅',
  'in_progress': '🔄',
  'not_started': '⏳',
  'blocked': '🚫',
  'default': '📦'
};

// Omsorg+ icons
export const omsorgPlusIcons = {
  'concept': '🏠',
  'floor': '🏗️',
  'unit': '🚪',
  'facility': '🏥',
  'compliance': '✅'
};

// Sustainability icons
export const sustainabilityIcons = {
  'recommended': '🌱',
  'preferred': '⭐',
  'not_recommended': '⚠️',
  'default': '♻️'
};

// Select/multi-select colors
export const selectColors = {
  // Status colors
  'completed': 'green',
  'in_progress': 'blue',
  'not_started': 'gray',
  'blocked': 'red',
  'pending': 'yellow',

  // Category colors
  'Sustainability': 'green',
  'Regulatory': 'orange',
  'Technical': 'blue',
  'Financial': 'purple',
  'Legal': 'brown',
  'Strategic': 'red',
  'Operational': 'gray',

  // Engagement levels
  'high': 'green',
  'medium': 'yellow',
  'low': 'gray',

  // Type colors
  'Consultant': 'blue',
  'Government': 'purple',
  'Owner': 'green',
  'Contractor': 'orange'
};

// Callout colors for meeting content
export const calloutColors = {
  'decision': 'green',
  'action': 'orange',
  'risk': 'red',
  'note': 'gray',
  'important': 'yellow',
  'success': 'green',
  'warning': 'orange'
};

// Get icon for a record based on database and properties
export function getRecordIcon(dbName, record) {
  switch (dbName) {
    case 'organizations':
      return { emoji: organizationIcons[record.type] || organizationIcons.default };

    case 'people':
      return { emoji: peopleIcons[record.category] || peopleIcons.default };

    case 'meetings':
      const topics = record.topics_discussed || [];
      if (topics.some(t => t.toLowerCase().includes('strateg'))) return { emoji: meetingIcons.strategic };
      if (topics.some(t => t.toLowerCase().includes('regulat'))) return { emoji: meetingIcons.regulatory };
      if (topics.some(t => t.toLowerCase().includes('bærekraft') || t.toLowerCase().includes('sustain'))) return { emoji: meetingIcons.sustainability };
      if (topics.some(t => t.toLowerCase().includes('tekn'))) return { emoji: meetingIcons.technical };
      return { emoji: meetingIcons.default };

    case 'documents':
      return { emoji: documentIcons[record.category] || documentIcons.default };

    case 'timeline':
      return { emoji: timelineIcons[record.type] || timelineIcons.default };

    case 'deliverables':
      return { emoji: deliverableIcons[record.status] || deliverableIcons.default };

    case 'omsorgPlusConcept':
      return { emoji: omsorgPlusIcons.concept };

    case 'omsorgPlusFloors':
      return { emoji: omsorgPlusIcons.floor };

    case 'omsorgPlusUnits':
      return { emoji: omsorgPlusIcons.unit };

    case 'omsorgPlusFacilities':
      return { emoji: omsorgPlusIcons.facility };

    case 'omsorgPlusCompliance':
      return { emoji: omsorgPlusIcons.compliance };

    case 'sustainability':
      return { emoji: sustainabilityIcons[record.status] || sustainabilityIcons.default };

    default:
      return { emoji: '📋' };
  }
}

// Get database icon
export function getDatabaseIcon(dbName) {
  const icons = {
    'organizations': '🏢',
    'people': '👥',
    'meetings': '🗓️',
    'documents': '📁',
    'timeline': '📅',
    'deliverables': '📦',
    'omsorgPlusConcept': '🏠',
    'omsorgPlusFloors': '🏗️',
    'omsorgPlusUnits': '🚪',
    'omsorgPlusFacilities': '🏥',
    'omsorgPlusCompliance': '✅',
    'sustainability': '🌱'
  };
  return { emoji: icons[dbName] || '📋' };
}
