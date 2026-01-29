#!/usr/bin/env node
/**
 * Match timeline events to meetings by date
 * Creates enriched timeline data with meeting links
 */

const fs = require('fs');
const path = require('path');

// Load data
const dataDir = path.join(__dirname, '../data');
const timeline = JSON.parse(fs.readFileSync(path.join(dataDir, 'timeline.json'), 'utf8'));
const meetings = JSON.parse(fs.readFileSync(path.join(dataDir, 'meetings.json'), 'utf8'));

// Helper: normalize date to YYYY-MM-DD
function normalizeDate(dateStr) {
  if (!dateStr) return null;
  if (dateStr.match(/^\d{4}$/)) return dateStr; // Year only
  if (dateStr.match(/^\d{4}-\d{2}$/)) return dateStr; // Year-month
  if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/)) return dateStr; // Full date
  return null;
}

// Helper: check if dates match (exact or same month/year)
function datesMatch(eventDate, meetingDate) {
  const eDate = normalizeDate(eventDate);
  const mDate = normalizeDate(meetingDate);

  if (!eDate || !mDate) return false;

  // Exact match
  if (eDate === mDate) return true;

  // Month match for events with only year-month
  if (eDate.length === 7 && mDate.startsWith(eDate)) return true;

  // Year match for events with only year
  if (eDate.length === 4 && mDate.startsWith(eDate)) return true;

  return false;
}

// Build meeting lookup by date
const meetingsByDate = {};
meetings.meetings.forEach(meeting => {
  const date = normalizeDate(meeting.date);
  if (date) {
    if (!meetingsByDate[date]) {
      meetingsByDate[date] = [];
    }
    meetingsByDate[date].push(meeting);
  }
});

// Process strategic events
console.log('\n=== STRATEGIC EVENTS ===\n');
let matchedCount = 0;

timeline.events.strategic.forEach(event => {
  console.log(`\n${event.id}: ${event.date} - ${event.title}`);

  const matchingMeetings = [];

  // Direct date match
  if (meetingsByDate[event.date]) {
    matchingMeetings.push(...meetingsByDate[event.date]);
  }

  // Check all meetings for fuzzy matches
  meetings.meetings.forEach(meeting => {
    if (datesMatch(event.date, meeting.date)) {
      if (!matchingMeetings.find(m => m.id === meeting.id)) {
        matchingMeetings.push(meeting);
      }
    }
  });

  if (matchingMeetings.length > 0) {
    matchedCount++;
    console.log(`  ✓ MATCHED: ${matchingMeetings.length} meeting(s)`);
    matchingMeetings.forEach(m => {
      console.log(`    - ${m.title}`);
      console.log(`      ID: ${m.id}`);
      console.log(`      Participants: ${m.participant_count}`);
    });
  } else {
    console.log(`  ✗ No meetings found`);
  }
});

console.log(`\n\nMatched ${matchedCount} out of ${timeline.events.strategic.length} strategic events\n`);

// Process operational events
console.log('\n=== OPERATIONAL EVENTS ===\n');
let opMatchedCount = 0;

timeline.events.operational.forEach(event => {
  const matchingMeetings = [];

  if (meetingsByDate[event.date]) {
    matchingMeetings.push(...meetingsByDate[event.date]);
  }

  meetings.meetings.forEach(meeting => {
    if (datesMatch(event.date, meeting.date)) {
      if (!matchingMeetings.find(m => m.id === meeting.id)) {
        matchingMeetings.push(meeting);
      }
    }
  });

  if (matchingMeetings.length > 0) {
    opMatchedCount++;
    console.log(`${event.id}: ${event.date} - ${event.title}`);
    console.log(`  ✓ ${matchingMeetings.length} meeting(s): ${matchingMeetings.map(m => m.id).join(', ')}`);
  }
});

console.log(`\n\nMatched ${opMatchedCount} out of ${timeline.events.operational.length} operational events\n`);

// Summary statistics
console.log('\n=== SUMMARY ===');
console.log(`Strategic events: ${matchedCount}/${timeline.events.strategic.length} matched`);
console.log(`Operational events: ${opMatchedCount}/${timeline.events.operational.length} matched`);
console.log(`Total meetings available: ${meetings.meetings.length}`);
console.log(`\nEvents without meetings can be enriched from document summaries.`);
