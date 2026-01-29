#!/usr/bin/env node
/**
 * Build enhanced timeline with meeting links and executive summaries
 * Output: data/timeline-enhanced.json
 */

const fs = require('fs');
const path = require('path');

// Load data
const dataDir = path.join(__dirname, '../data');
const timeline = JSON.parse(fs.readFileSync(path.join(dataDir, 'timeline.json'), 'utf8'));
const meetings = JSON.parse(fs.readFileSync(path.join(dataDir, 'meetings.json'), 'utf8'));
const people = JSON.parse(fs.readFileSync(path.join(dataDir, 'stakeholders/people.json'), 'utf8'));

// Helper: normalize date to YYYY-MM-DD
function normalizeDate(dateStr) {
  if (!dateStr) return null;
  if (dateStr.match(/^\d{4}$/)) return dateStr;
  if (dateStr.match(/^\d{4}-\d{2}$/)) return dateStr;
  if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/)) return dateStr;
  return null;
}

// Helper: check if dates match
function datesMatch(eventDate, meetingDate) {
  const eDate = normalizeDate(eventDate);
  const mDate = normalizeDate(meetingDate);
  if (!eDate || !mDate) return false;
  if (eDate === mDate) return true;
  if (eDate.length === 7 && mDate.startsWith(eDate)) return true;
  if (eDate.length === 4 && mDate.startsWith(eDate)) return true;
  return false;
}

// Build meeting lookup
const meetingsByDate = {};
meetings.meetings.forEach(meeting => {
  const date = normalizeDate(meeting.date);
  if (date) {
    if (!meetingsByDate[date]) meetingsByDate[date] = [];
    meetingsByDate[date].push(meeting);
  }
});

// Manual executive summaries for strategic events
const execSummaries = {
  "s_001": {
    "exec_summary": [
      "Concrete structure designed for 12 floors (only 5 built)",
      "Foundation has capacity for vertical extension",
      "Key enabler for transformation vs demolition"
    ]
  },
  "s_002": {
    "exec_summary": [
      "Area plan requires demolition + 10m setback from Hoffselva",
      "Triggers need for transformation argument",
      "Core regulatory challenge for project"
    ]
  },
  "s_003": {
    "exec_summary": [
      "First formal meeting: Urbania, Natural State, architects",
      "Systematic transformation concept work begins",
      "Establishes project team structure"
    ]
  },
  "s_004": {
    "exec_summary": [
      "R21 delivers 6 complete scenario plans",
      "Includes office, housing, Omsorg+, mixed-use",
      "Provides concrete options for decision-making"
    ]
  },
  "s_005": {
    "exec_summary": [
      "Transformation plans presented to current tenants",
      "Dialogue about transition timeline established",
      "Tenant cooperation secured"
    ]
  },
  "s_006": {
    "exec_summary": [
      "Path to 50% energy reduction documented",
      "Enova support eligibility confirmed",
      "Energy upgrade strategy established"
    ],
    "related_documents": ["doc_energy_report_2025_04_11"]
  },
  "s_007": {
    "exec_summary": [
      "Transformation: 456 kg CO₂-ekv/m² BTA",
      "Demolition + new: 631 kg CO₂-ekv/m² BTA",
      "48% lower emissions → core sustainability argument"
    ],
    "related_documents": ["doc_climate_calculations_v2"]
  },
  "s_008": {
    "exec_summary": [
      "Meeting with Bydel Ullern leaders (Ingrid Hopp, Tore Strandskog)",
      "District needs 70+ elderly housing units",
      "Omsorg+ partnership potential identified"
    ]
  },
  "s_009": {
    "exec_summary": [
      "ESRS-aligned comprehensive sustainability report",
      "Consolidates environmental, social, economic arguments",
      "Complete case for transformation vs demolition"
    ]
  },
  "s_010": {
    "exec_summary": [
      "Target: Q4 2025 framework application submission",
      "To Plan- og bygningsetaten Oslo",
      "Depends on finalizing preferred scenario"
    ]
  }
};

// Enhance strategic events
console.log('Enhancing strategic events...\n');
const enhancedStrategic = timeline.events.strategic.map(event => {
  const enhanced = { ...event };

  // Add exec summary if available
  if (execSummaries[event.id]) {
    enhanced.exec_summary = execSummaries[event.id].exec_summary;
    if (execSummaries[event.id].related_documents) {
      enhanced.related_documents = execSummaries[event.id].related_documents;
    }
  }

  // Find matching meetings
  const matchingMeetings = [];
  meetings.meetings.forEach(meeting => {
    if (datesMatch(event.date, meeting.date)) {
      matchingMeetings.push({
        id: meeting.id,
        title: meeting.title,
        participant_count: meeting.participant_count
      });
    }
  });

  if (matchingMeetings.length > 0) {
    enhanced.linked_meetings = matchingMeetings;
    console.log(`✓ ${event.id}: ${matchingMeetings.length} meeting(s) linked`);
  } else {
    console.log(`  ${event.id}: No meetings`);
  }

  return enhanced;
});

// Enhance operational events
console.log('\nEnhancing operational events...\n');
const enhancedOperational = timeline.events.operational.map(event => {
  const enhanced = { ...event };

  // Find matching meetings
  const matchingMeetings = [];
  meetings.meetings.forEach(meeting => {
    if (datesMatch(event.date, meeting.date)) {
      matchingMeetings.push({
        id: meeting.id,
        title: meeting.title,
        participant_count: meeting.participant_count
      });
    }
  });

  if (matchingMeetings.length > 0) {
    enhanced.linked_meetings = matchingMeetings;
  }

  return enhanced;
});

// Build output
const enhancedTimeline = {
  ...timeline,
  metadata: {
    ...timeline.metadata,
    version: "2.2",
    last_updated: new Date().toISOString().split('T')[0],
    description: "Enhanced timeline with meeting links and executive summaries",
    enhancement_notes: "Strategic events have exec_summary arrays. Events with meetings have linked_meetings arrays."
  },
  events: {
    strategic: enhancedStrategic,
    operational: enhancedOperational
  }
};

// Write output
const outputPath = path.join(dataDir, 'timeline-enhanced.json');
fs.writeFileSync(outputPath, JSON.stringify(enhancedTimeline, null, 2));

console.log(`\n✅ Enhanced timeline written to: ${outputPath}`);
console.log(`\nStrategic events: ${enhancedStrategic.length}`);
console.log(`Operational events: ${enhancedOperational.length}`);
console.log(`\nEvents with exec summaries: ${enhancedStrategic.filter(e => e.exec_summary).length}`);
console.log(`Strategic events with meetings: ${enhancedStrategic.filter(e => e.linked_meetings).length}`);
console.log(`Operational events with meetings: ${enhancedOperational.filter(e => e.linked_meetings).length}`);
