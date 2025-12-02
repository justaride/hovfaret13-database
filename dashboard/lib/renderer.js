/**
 * Renderer Module
 * Core rendering functions for timeline and events
 */

const Renderer = {
  /**
   * Icons map (Lucide icon names)
   */
  icons: {
    building: 'building',
    alert: 'alert-triangle',
    rocket: 'rocket',
    blueprint: 'drafting-compass',
    users: 'users',
    lightning: 'zap',
    leaf: 'leaf',
    government: 'landmark',
    document: 'file-text',
    target: 'target',
    calendar: 'calendar',
    person: 'user',
    meeting: 'clipboard'
  },

  /**
   * Format date for display
   */
  formatDate(dateStr) {
    if (!dateStr) return 'TBD';
    if (dateStr.match(/^\d{4}$/)) return dateStr; // Year only
    if (dateStr.match(/^\d{4}-Q\d$/)) return dateStr; // Quarter
    if (dateStr.match(/^\d{4}-\d{2}$/)) {
      // Year-month → "Sep 2023"
      const [year, month] = dateStr.split('-');
      const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      return `${monthNames[parseInt(month) - 1]} ${year}`;
    }
    if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
      // Full date → "11 Mar 2024"
      const [year, month, day] = dateStr.split('-');
      const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      return `${parseInt(day)} ${monthNames[parseInt(month) - 1]} ${year}`;
    }
    return dateStr;
  },

  /**
   * Render event card
   */
  renderEventCard(event, allData, expanded = false) {
    const iconName = this.icons[event.icon] || 'pin';
    const hasExecSummary = event.exec_summary && event.exec_summary.length > 0;
    const hasMeetings = event.linked_meetings && event.linked_meetings.length > 0;
    const hasDocuments = event.related_documents && event.related_documents.length > 0;

    const importanceClass = event.importance ? `importance-${event.importance}` : '';
    const expandedClass = expanded ? 'expanded' : '';

    let html = `
      <div class="event-card ${importanceClass} ${expandedClass}" data-event-id="${event.id}">
        <div class="event-header" onclick="Renderer.toggleEventCard('${event.id}')">
          <div class="event-icon"><i data-lucide="${iconName}"></i></div>
          <div class="event-main">
            <div class="event-date">${this.formatDate(event.date)}</div>
            <div class="event-title">${event.title}</div>
            ${event.title_no ? `<div class="event-title-no">${event.title_no}</div>` : ''}
          </div>
          <div class="event-indicators">
            ${hasMeetings ? `<span class="indicator meeting-indicator" title="${event.linked_meetings.length} meeting(s)"><i data-lucide="clipboard" class="icon-xs"></i> ${event.linked_meetings.length}</span>` : ''}
            ${hasDocuments ? `<span class="indicator doc-indicator" title="Related documents"><i data-lucide="file-text" class="icon-xs"></i></span>` : ''}
            ${event.importance === 'critical' ? `<span class="indicator critical-indicator">CRITICAL</span>` : ''}
          </div>
        </div>

        <div class="event-body">
          ${event.description ? `<p class="event-description">${event.description}</p>` : ''}

          ${hasExecSummary ? `
            <div class="event-exec-summary">
              <h4>Executive Summary</h4>
              <ul>
                ${event.exec_summary.map(point => `<li>${point}</li>`).join('')}
              </ul>
            </div>
          ` : ''}

          ${hasMeetings ? `
            <div class="event-meetings">
              <h4><i data-lucide="clipboard" class="icon-sm"></i> Related Meetings</h4>
              ${event.linked_meetings.map(m => {
                const meeting = allData.meetings.find(mtg => mtg.id === m.id);
                return `
                  <div class="meeting-link" onclick="Renderer.showMeetingDetails('${m.id}')">
                    <div class="meeting-title">${m.title}</div>
                    <div class="meeting-meta">${m.participant_count} participants</div>
                  </div>
                `;
              }).join('')}
            </div>
          ` : ''}

          ${hasDocuments ? `
            <div class="event-documents">
              <h4><i data-lucide="file-text" class="icon-sm"></i> Related Documents</h4>
              <ul>
                ${event.related_documents.map(docId => {
                  const doc = allData.documents.find(d => d.id === docId);
                  return `<li>${doc ? doc.title : docId}</li>`;
                }).join('')}
              </ul>
            </div>
          ` : ''}

          ${event.tags ? `
            <div class="event-tags">
              ${event.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
          ` : ''}
        </div>
      </div>
    `;

    return html;
  },

  /**
   * Render timeline layer
   */
  renderTimelineLayer(events, allData, layerName) {
    const html = `
      <div class="timeline-layer" data-layer="${layerName}">
        <h2 class="layer-title">${layerName === 'strategic' ? 'Strategic Overview' : 'Operational Timeline'}</h2>
        <div class="events-container">
          ${events.map(event => this.renderEventCard(event, allData)).join('')}
        </div>
      </div>
    `;
    return html;
  },

  /**
   * Toggle event card expansion
   */
  toggleEventCard(eventId) {
    const card = document.querySelector(`[data-event-id="${eventId}"]`);
    if (card) {
      card.classList.toggle('expanded');
    }
  },

  /**
   * Show meeting details in side panel
   */
  showMeetingDetails(meetingId) {
    console.log('Show meeting:', meetingId);
    // TODO: Implement side panel
    alert(`Meeting details: ${meetingId}\nSide panel coming soon!`);
  },

  /**
   * Render search results
   */
  renderSearchResults(results) {
    let html = '<div class="search-results">';

    if (results.events.length > 0) {
      html += `
        <div class="results-section">
          <h3>Events (${results.events.length})</h3>
          <ul>
            ${results.events.map(e => `
              <li onclick="Renderer.scrollToEvent('${e.id}')">
                <strong>${e.title}</strong>
                <span class="result-meta">${Renderer.formatDate(e.date)} • ${e.layer}</span>
              </li>
            `).join('')}
          </ul>
        </div>
      `;
    }

    if (results.meetings.length > 0) {
      html += `
        <div class="results-section">
          <h3>Meetings (${results.meetings.length})</h3>
          <ul>
            ${results.meetings.map(m => `
              <li onclick="Renderer.showMeetingDetails('${m.id}')">
                <strong>${m.title}</strong>
                <span class="result-meta">${Renderer.formatDate(m.date)}</span>
              </li>
            `).join('')}
          </ul>
        </div>
      `;
    }

    if (results.people.length > 0) {
      html += `
        <div class="results-section">
          <h3>People (${results.people.length})</h3>
          <ul>
            ${results.people.map(p => `
              <li>
                <strong>${p.name}</strong>
                <span class="result-meta">${p.organization || ''}</span>
              </li>
            `).join('')}
          </ul>
        </div>
      `;
    }

    if (results.documents.length > 0) {
      html += `
        <div class="results-section">
          <h3>Documents (${results.documents.length})</h3>
          <ul>
            ${results.documents.slice(0, 10).map(d => `
              <li>
                <strong>${d.title}</strong>
                <span class="result-meta">${d.category}</span>
              </li>
            `).join('')}
            ${results.documents.length > 10 ? `<li class="more">+${results.documents.length - 10} more</li>` : ''}
          </ul>
        </div>
      `;
    }

    if (results.events.length === 0 && results.meetings.length === 0 &&
        results.people.length === 0 && results.documents.length === 0) {
      html += '<p class="no-results">No results found</p>';
    }

    html += '</div>';
    return html;
  },

  /**
   * Scroll to event
   */
  scrollToEvent(eventId) {
    const card = document.querySelector(`[data-event-id="${eventId}"]`);
    if (card) {
      card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      card.classList.add('highlight');
      setTimeout(() => card.classList.remove('highlight'), 2000);

      // Expand if collapsed
      if (!card.classList.contains('expanded')) {
        card.classList.add('expanded');
      }
    }
  },

  /**
   * Render document card (compact or expanded)
   */
  renderDocumentCard(doc, isExpanded = false) {
    const helpers = window.DocumentHelpers;
    const categoryMeta = helpers.getCategoryMeta(doc.category);
    const fileTypeMeta = helpers.getFileTypeMeta(doc.file_type);
    const docSlug = helpers.getDocumentSlug(doc.id);

    const truncatedSource = helpers.truncate(doc.source_folder, 40);
    const truncatedName = helpers.truncate(doc.file_name, 60);
    const dateShort = helpers.formatDateShort(doc.extraction_date);

    const expandedClass = isExpanded ? 'expanded' : '';

    return `
      <div class="document-card ${expandedClass}" data-doc-id="${helpers.sanitizeHTML(doc.id)}" id="doc-${docSlug}">
        <div class="document-header" onclick="Renderer.toggleDocumentCard('${docSlug}')">
          <div class="document-icon" style="color: ${fileTypeMeta.color}">
            ${helpers.getFileTypeIcon(doc.file_type)}
          </div>
          <div class="document-main">
            <div class="document-filename" title="${helpers.sanitizeHTML(doc.file_name)}">
              ${helpers.sanitizeHTML(truncatedName)}
            </div>
            <div class="document-meta">
              <span class="document-type">${fileTypeMeta.label}</span>
              <span class="document-date">${dateShort}</span>
            </div>
          </div>
          <div class="document-expand-icon">
            ${helpers.getChevronIcon(isExpanded)}
          </div>
        </div>

        <div class="document-body">
          <div class="document-details">
            <div class="detail-row">
              <span class="detail-label">Category:</span>
              <span class="detail-value">${categoryMeta.label}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Source:</span>
              <span class="detail-value" title="${helpers.sanitizeHTML(doc.source_folder)}">
                ${helpers.sanitizeHTML(truncatedSource)}
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">ID:</span>
              <span class="detail-value document-id">${helpers.sanitizeHTML(doc.id)}</span>
            </div>
            ${doc.has_error ? `
              <div class="detail-row">
                <span class="detail-label">Status:</span>
                <span class="detail-value error"><i data-lucide="alert-triangle" class="icon-xs"></i> Has Error</span>
              </div>
            ` : ''}
          </div>
        </div>
      </div>
    `;
  },

  /**
   * Render category section
   */
  renderCategorySection(category, documents, isExpanded = false) {
    const helpers = window.DocumentHelpers;
    const categoryMeta = helpers.getCategoryMeta(category);
    const expandedClass = isExpanded ? 'expanded' : '';
    const categorySlug = category.replace(/[^a-zA-Z0-9]/g, '_');

    return `
      <div class="category-section ${expandedClass}" data-category="${category}" id="cat-${categorySlug}">
        <div class="category-header" onclick="Renderer.toggleCategory('${categorySlug}')">
          <div class="category-icon" style="color: ${categoryMeta.color}">
            ${helpers.getChevronIcon(isExpanded)}
          </div>
          <div class="category-main">
            <div class="category-title">
              <i data-lucide="${categoryMeta.icon}" class="icon-md" style="color: ${categoryMeta.color}"></i>
              ${categoryMeta.label}
            </div>
            <div class="category-description">${categoryMeta.description}</div>
          </div>
          <div class="category-count">
            ${documents.length}
          </div>
        </div>

        <div class="category-body">
          ${documents.map(doc => this.renderDocumentCard(doc, false)).join('')}
        </div>
      </div>
    `;
  },

  /**
   * Toggle document card expanded state
   */
  toggleDocumentCard(docSlug) {
    const card = document.getElementById(`doc-${docSlug}`);
    if (card) {
      const isExpanded = card.classList.contains('expanded');
      card.classList.toggle('expanded');

      // Update chevron icon
      const chevronContainer = card.querySelector('.document-expand-icon');
      if (chevronContainer) {
        chevronContainer.innerHTML = window.DocumentHelpers.getChevronIcon(!isExpanded);
      }
    }
  },

  /**
   * Toggle category expanded state
   */
  toggleCategory(categorySlug) {
    const section = document.getElementById(`cat-${categorySlug}`);
    if (section) {
      const isExpanded = section.classList.contains('expanded');
      section.classList.toggle('expanded');

      // Update chevron icon
      const chevronContainer = section.querySelector('.category-icon');
      if (chevronContainer) {
        chevronContainer.innerHTML = window.DocumentHelpers.getChevronIcon(!isExpanded);
      }
    }
  },

  /**
   * Render person card
   */
  renderPersonCard(person, isExpanded = false) {
    const helpers = window.StakeholderHelpers;
    const categoryMeta = helpers.getPersonCategoryMeta(person.category);
    const personSlug = helpers.getPersonSlug(person.id);
    const initials = helpers.getInitials(person.name);
    const avatarColor = helpers.getAvatarColor(person.name);
    const expandedClass = isExpanded ? 'expanded' : '';

    return `
      <div class="person-card ${expandedClass}" data-person-id="${helpers.sanitizeHTML(person.id)}" id="person-${personSlug}">
        <div class="person-header" onclick="Renderer.togglePersonCard('${personSlug}')">
          <div class="person-avatar" style="background-color: ${avatarColor}">
            ${initials}
          </div>
          <div class="person-main">
            <div class="person-name">${helpers.sanitizeHTML(person.name)}</div>
            <div class="person-title">${helpers.sanitizeHTML(person.title || '')}</div>
            <div class="person-org">${helpers.sanitizeHTML(person.organization || '')}</div>
          </div>
          <div class="person-category-badge" style="background-color: ${categoryMeta.color}20; color: ${categoryMeta.color}">
            <i data-lucide="${categoryMeta.icon}" class="icon-xs"></i> ${person.category}
          </div>
        </div>

        <div class="person-body">
          ${person.bio ? `
            <div class="person-bio">
              ${helpers.sanitizeHTML(person.bio)}
            </div>
          ` : ''}

          <div class="person-details">
            ${person.role_in_project ? `
              <div class="detail-row">
                <span class="detail-label">Role:</span>
                <span class="detail-value">${helpers.sanitizeHTML(person.role_in_project)}</span>
              </div>
            ` : ''}

            ${person.expertise && person.expertise.length > 0 ? `
              <div class="detail-row">
                <span class="detail-label">Expertise:</span>
                <span class="detail-value">${helpers.formatExpertise(person.expertise)}</span>
              </div>
            ` : ''}

            ${person.email ? `
              <div class="detail-row">
                <span class="detail-label">Email:</span>
                <span class="detail-value">
                  <a href="mailto:${person.email}" class="contact-link">
                    ${helpers.getEmailIcon()} ${person.email}
                  </a>
                </span>
              </div>
            ` : ''}

            ${person.phone ? `
              <div class="detail-row">
                <span class="detail-label">Phone:</span>
                <span class="detail-value">
                  <a href="tel:${person.phone}" class="contact-link">
                    ${helpers.getPhoneIcon()} ${person.phone}
                  </a>
                </span>
              </div>
            ` : ''}

            ${person.engagement ? `
              <div class="detail-row">
                <span class="detail-label">Meetings:</span>
                <span class="detail-value">${person.engagement.total_meetings || 0} meetings</span>
              </div>
            ` : ''}
          </div>
        </div>
      </div>
    `;
  },

  /**
   * Render organization card
   */
  renderOrganizationCard(org, people, isExpanded = false) {
    const helpers = window.StakeholderHelpers;
    const categoryMeta = helpers.getOrgCategoryMeta(org.category);
    const typeMeta = helpers.getOrgTypeMeta(org.type);
    const engagementMeta = helpers.getEngagementMeta(org.engagement_level);
    const orgSlug = helpers.getOrgSlug(org.id);
    const expandedClass = isExpanded ? 'expanded' : '';

    // Get people count for this org
    const orgPeople = people ? people.filter(p => p.organization_id === org.id) : [];

    return `
      <div class="org-card ${expandedClass}" data-org-id="${helpers.sanitizeHTML(org.id)}" id="org-${orgSlug}">
        <div class="org-header" onclick="Renderer.toggleOrgCard('${orgSlug}')">
          <div class="org-icon" style="color: ${categoryMeta.color}">
            ${helpers.getOrgIcon()}
          </div>
          <div class="org-main">
            <div class="org-name">${helpers.sanitizeHTML(org.name)}</div>
            <div class="org-type">${typeMeta.label}</div>
            <div class="org-role">${helpers.sanitizeHTML(org.role_in_project || '')}</div>
          </div>
          <div class="org-badges">
            <span class="org-category-badge" style="background-color: ${categoryMeta.color}20; color: ${categoryMeta.color}">
              <i data-lucide="${categoryMeta.icon}" class="icon-xs"></i> ${org.category}
            </span>
            ${orgPeople.length > 0 ? `
              <span class="org-people-badge">
                ${helpers.getPersonIcon()} ${orgPeople.length}
              </span>
            ` : ''}
          </div>
        </div>

        <div class="org-body">
          ${org.description ? `
            <div class="org-description">
              ${helpers.sanitizeHTML(org.description)}
            </div>
          ` : ''}

          <div class="org-details">
            ${org.engagement_level ? `
              <div class="detail-row">
                <span class="detail-label">Engagement:</span>
                <span class="detail-value" style="color: ${engagementMeta.color}">
                  ${engagementMeta.label}
                </span>
              </div>
            ` : ''}

            ${org.expertise && org.expertise.length > 0 ? `
              <div class="detail-row">
                <span class="detail-label">Expertise:</span>
                <span class="detail-value">${helpers.formatExpertise(org.expertise)}</span>
              </div>
            ` : ''}

            ${org.website ? `
              <div class="detail-row">
                <span class="detail-label">Website:</span>
                <span class="detail-value">
                  <a href="https://${org.website}" target="_blank" class="contact-link">
                    ${helpers.getLinkIcon()} ${org.website}
                  </a>
                </span>
              </div>
            ` : ''}

            ${orgPeople.length > 0 ? `
              <div class="detail-row">
                <span class="detail-label">Team:</span>
                <span class="detail-value">
                  ${orgPeople.map(p => helpers.sanitizeHTML(p.name)).join(', ')}
                </span>
              </div>
            ` : ''}
          </div>
        </div>
      </div>
    `;
  },

  /**
   * Toggle person card expanded state
   */
  togglePersonCard(personSlug) {
    const card = document.getElementById(`person-${personSlug}`);
    if (card) {
      card.classList.toggle('expanded');
    }
  },

  /**
   * Toggle organization card expanded state
   */
  toggleOrgCard(orgSlug) {
    const card = document.getElementById(`org-${orgSlug}`);
    if (card) {
      card.classList.toggle('expanded');
    }
  },

  // ===== MEETING RENDERING FUNCTIONS =====

  /**
   * Render meeting card
   */
  renderMeetingCard(meeting, expanded = false) {
    if (!meeting || !meeting.id) return '';

    // Get meeting metadata
    const meetingType = typeof MeetingHelpers !== 'undefined'
      ? MeetingHelpers.determineMeetingType(meeting)
      : 'other';
    const typeInfo = typeof MeetingHelpers !== 'undefined'
      ? MeetingHelpers.MEETING_TYPES[meetingType]
      : { label: 'Meeting', color: '#6B7280', icon: '📅' };

    const dateShort = typeof MeetingHelpers !== 'undefined'
      ? MeetingHelpers.formatDateShort(meeting.date)
      : meeting.date;
    const dateLong = typeof MeetingHelpers !== 'undefined'
      ? MeetingHelpers.formatDateLong(meeting.date)
      : meeting.date;
    const relativeTime = typeof MeetingHelpers !== 'undefined'
      ? MeetingHelpers.getRelativeTime(meeting.date)
      : '';

    const uniqueOrgs = typeof MeetingHelpers !== 'undefined'
      ? MeetingHelpers.getUniqueOrganizations(meeting)
      : [...new Set((meeting.participants || []).map(p => p.organization).filter(Boolean))];

    const realParticipantCount = typeof MeetingHelpers !== 'undefined'
      ? MeetingHelpers.getRealParticipantCount(meeting)
      : (meeting.participants || []).length;

    const isPast = typeof MeetingHelpers !== 'undefined'
      ? MeetingHelpers.isPast(meeting.date)
      : new Date(meeting.date) < new Date();

    const hasLocation = meeting.location && meeting.location.trim();
    const hasDataQualityNote = meeting.data_quality_note;
    const hasTopics = meeting.topics_discussed && meeting.topics_discussed.length > 0;
    const hasActionItems = meeting.action_items && meeting.action_items.length > 0;
    const hasDecisions = meeting.decisions && meeting.decisions.length > 0;
    const hasReport = meeting.report_link || meeting.report_metadata;

    const expandedClass = expanded ? 'expanded' : '';
    const timeClass = isPast ? 'past' : 'upcoming';

    return `
      <div class="meeting-card ${timeClass} ${expandedClass}" id="meeting-${meeting.id}" data-meeting-id="${meeting.id}">
        <div class="meeting-header" onclick="Renderer.toggleMeetingCard('${meeting.id}')">
          <div class="meeting-icon" style="color: ${typeInfo.color}"><i data-lucide="${typeInfo.icon}"></i></div>
          <div class="meeting-main">
            <div class="meeting-date">
              ${dateShort}
              ${relativeTime ? `<span class="relative-time">(${relativeTime})</span>` : ''}
            </div>
            <div class="meeting-title">${typeof MeetingHelpers !== 'undefined' ? MeetingHelpers.sanitizeHtml(meeting.title) : meeting.title}</div>
          </div>
          <div class="meeting-indicators">
            <span class="meeting-type-badge" style="background-color: ${typeInfo.color}20; color: ${typeInfo.color}; border-color: ${typeInfo.color}50;">
              ${typeInfo.label}
            </span>
            ${hasReport ? `
              <span class="participant-count" title="Meeting report available" style="color: #10B981;">
                <i data-lucide="file-text" class="icon-xs"></i>
              </span>
            ` : ''}
            ${realParticipantCount > 0 ? `
              <span class="participant-count" title="${realParticipantCount} participants">
                <i data-lucide="users" class="icon-xs"></i> ${realParticipantCount}
              </span>
            ` : ''}
            ${hasDataQualityNote ? `
              <span class="data-quality-indicator" title="${meeting.data_quality_note}">
                <i data-lucide="alert-triangle" class="icon-xs"></i>
              </span>
            ` : ''}
          </div>
        </div>

        <div class="meeting-body">
          <!-- Meeting Details -->
          <div class="meeting-details">
            <div class="detail-row">
              <span class="detail-label">
                <i data-lucide="calendar" class="icon-sm"></i> Date
              </span>
              <span class="detail-value">${dateLong}</span>
            </div>

            ${meeting.organizer ? `
              <div class="detail-row">
                <span class="detail-label">
                  <i data-lucide="mail" class="icon-sm"></i> Organizer
                </span>
                <span class="detail-value">
                  <a href="mailto:${meeting.organizer}">${meeting.organizer}</a>
                </span>
              </div>
            ` : ''}

            ${hasLocation ? `
              <div class="detail-row">
                <span class="detail-label">
                  <i data-lucide="map-pin" class="icon-sm"></i> Location
                </span>
                <span class="detail-value">${typeof MeetingHelpers !== 'undefined' ? MeetingHelpers.sanitizeHtml(meeting.location) : meeting.location}</span>
              </div>
            ` : ''}

            ${uniqueOrgs.length > 0 ? `
              <div class="detail-row">
                <span class="detail-label">
                  <i data-lucide="building" class="icon-sm"></i> Organizations
                </span>
                <span class="detail-value">
                  ${uniqueOrgs.map(org => `<span class="org-tag">${org}</span>`).join(' ')}
                </span>
              </div>
            ` : ''}
          </div>

          <!-- Participants -->
          ${realParticipantCount > 0 ? `
            <div class="meeting-participants">
              <h4><i data-lucide="users" class="icon-sm"></i> Participants (${realParticipantCount})</h4>
              <div class="participants-list">
                ${meeting.participants.map(p => {
                  const avatarColor = typeof MeetingHelpers !== 'undefined'
                    ? MeetingHelpers.getAvatarColor(p.name)
                    : '#6B7280';
                  const initials = typeof MeetingHelpers !== 'undefined'
                    ? MeetingHelpers.getInitials(p.name)
                    : p.name?.substring(0, 2).toUpperCase() || '?';

                  return `
                    <div class="participant-item">
                      <div class="participant-avatar" style="background-color: ${avatarColor};">
                        ${initials}
                      </div>
                      <div class="participant-info">
                        <div class="participant-name">${p.name || 'Unknown'}</div>
                        ${p.organization ? `<div class="participant-org">${p.organization}</div>` : ''}
                      </div>
                      ${p.email ? `
                        <a href="mailto:${p.email}" class="participant-email" title="Send email">
                          <i data-lucide="mail" class="icon-xs"></i>
                        </a>
                      ` : ''}
                    </div>
                  `;
                }).join('')}
              </div>
            </div>
          ` : '<p class="no-participants">No participants recorded</p>'}

          <!-- Topics Discussed -->
          ${hasTopics ? `
            <div class="meeting-topics">
              <h4><i data-lucide="message-circle" class="icon-sm"></i> Topics Discussed</h4>
              <ul>
                ${meeting.topics_discussed.map(topic => `<li>${topic}</li>`).join('')}
              </ul>
            </div>
          ` : ''}

          <!-- Action Items -->
          ${hasActionItems ? `
            <div class="meeting-topics">
              <h4><i data-lucide="check-square" class="icon-sm"></i> Action Items</h4>
              <ul>
                ${meeting.action_items.map(item => `<li>${item}</li>`).join('')}
              </ul>
            </div>
          ` : ''}

          <!-- Decisions -->
          ${hasDecisions ? `
            <div class="meeting-topics">
              <h4><i data-lucide="clipboard-check" class="icon-sm"></i> Decisions</h4>
              <ul>
                ${meeting.decisions.map(decision => `<li>${decision}</li>`).join('')}
              </ul>
            </div>
          ` : ''}

          <!-- Embedded Report -->
          ${meeting.report ? `
            <div class="embedded-report">
              <!-- Summary (alltid synlig) -->
              ${meeting.report.summary ? `
                <div class="report-summary">
                  <h4><i data-lucide="file-text" class="icon-sm"></i> Sammendrag</h4>
                  <p>${meeting.report.summary}</p>
                </div>
              ` : ''}

              <!-- Expandable Sections -->
              ${meeting.report.discussion && meeting.report.discussion.length > 0 ? `
                <div class="report-section" id="discussion-${meeting.id}">
                  <div class="report-section-header" onclick="Renderer.toggleReportSection('discussion-${meeting.id}')">
                    <div class="section-title">
                      <i data-lucide="message-square" class="icon-sm"></i>
                      <span>Diskusjon</span>
                    </div>
                    <i data-lucide="chevron-down" class="icon-sm chevron"></i>
                  </div>
                  <div class="report-section-content">
                    ${meeting.report.discussion.map(section => `
                      <div class="discussion-subsection">
                        <h5>${section.heading}</h5>
                        <div class="discussion-content">${section.content.replace(/\n/g, '<br>')}</div>
                      </div>
                    `).join('')}
                  </div>
                </div>
              ` : ''}

              ${meeting.report.decisions && meeting.report.decisions.length > 0 ? `
                <div class="report-section" id="decisions-${meeting.id}">
                  <div class="report-section-header" onclick="Renderer.toggleReportSection('decisions-${meeting.id}')">
                    <div class="section-title">
                      <i data-lucide="clipboard-check" class="icon-sm"></i>
                      <span>Beslutninger</span>
                    </div>
                    <i data-lucide="chevron-down" class="icon-sm chevron"></i>
                  </div>
                  <div class="report-section-content">
                    <ul class="decisions-list">
                      ${meeting.report.decisions.map(d => `<li>${d}</li>`).join('')}
                    </ul>
                  </div>
                </div>
              ` : ''}

              ${meeting.report.action_items && meeting.report.action_items.length > 0 ? `
                <div class="report-section" id="actions-${meeting.id}">
                  <div class="report-section-header" onclick="Renderer.toggleReportSection('actions-${meeting.id}')">
                    <div class="section-title">
                      <i data-lucide="check-square" class="icon-sm"></i>
                      <span>Action Items</span>
                    </div>
                    <i data-lucide="chevron-down" class="icon-sm chevron"></i>
                  </div>
                  <div class="report-section-content">
                    <div class="action-items-list">
                      ${meeting.report.action_items.map(item => `
                        <div class="action-item">
                          <div class="action-task"><strong>${item.task}</strong></div>
                          ${item.responsible ? `<div class="action-meta">Ansvarlig: ${item.responsible}${item.deadline ? ` • Frist: ${item.deadline}` : ''}</div>` : ''}
                        </div>
                      `).join('')}
                    </div>
                  </div>
                </div>
              ` : ''}

              ${meeting.report.quotes && meeting.report.quotes.length > 0 ? `
                <div class="report-section" id="quotes-${meeting.id}">
                  <div class="report-section-header" onclick="Renderer.toggleReportSection('quotes-${meeting.id}')">
                    <div class="section-title">
                      <i data-lucide="quote" class="icon-sm"></i>
                      <span>Viktige sitater</span>
                    </div>
                    <i data-lucide="chevron-down" class="icon-sm chevron"></i>
                  </div>
                  <div class="report-section-content">
                    ${meeting.report.quotes.map(quote => `
                      <blockquote class="meeting-quote">"${quote}"</blockquote>
                    `).join('')}
                  </div>
                </div>
              ` : ''}

              ${meeting.report.context ? `
                <div class="report-section" id="context-${meeting.id}">
                  <div class="report-section-header" onclick="Renderer.toggleReportSection('context-${meeting.id}')">
                    <div class="section-title">
                      <i data-lucide="info" class="icon-sm"></i>
                      <span>Kontekst og betydning</span>
                    </div>
                    <i data-lucide="chevron-down" class="icon-sm chevron"></i>
                  </div>
                  <div class="report-section-content">
                    <p>${meeting.report.context.replace(/\n/g, '<br>')}</p>
                  </div>
                </div>
              ` : ''}
            </div>
          ` : ''}

          <!-- Data Quality Note -->
          ${hasDataQualityNote ? `
            <div class="data-quality-note">
              <i data-lucide="alert-triangle" class="icon-sm"></i>
              <strong>Data Quality:</strong> ${meeting.data_quality_note}
            </div>
          ` : ''}
        </div>
      </div>
    `;
  },

  /**
   * Toggle meeting card expanded state
   */
  toggleMeetingCard(meetingId) {
    const card = document.getElementById(`meeting-${meetingId}`);
    if (card) {
      card.classList.toggle('expanded');
    }
  },

  /**
   * Toggle report section expanded state
   */
  toggleReportSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
      section.classList.toggle('expanded');

      // Re-initialize Lucide icons
      if (typeof lucide !== 'undefined') {
        lucide.createIcons();
      }
    }
  },

  /**
   * Open polished meeting note in new window
   */
  openPolishedNote(reportLink) {
    if (!reportLink) return;

    // Convert relative path to absolute
    const basePath = window.location.origin + window.location.pathname.replace(/\/[^\/]*$/, '');
    const fullPath = reportLink.startsWith('http')
      ? reportLink
      : `${basePath}/${reportLink}`;

    // Open in new window
    window.open(fullPath, '_blank', 'width=900,height=800,scrollbars=yes,resizable=yes');
  },

  /**
   * Render meetings grouped by month
   */
  renderMeetingsByMonth(monthGroups, expanded = false) {
    if (!monthGroups || monthGroups.length === 0) {
      return '<div class="empty-state">No meetings found</div>';
    }

    return monthGroups.map(group => {
      const meetingCount = group.meetings.length;
      const expandedClass = expanded ? 'expanded' : '';

      return `
        <div class="month-section ${expandedClass}" data-month="${group.label}">
          <div class="month-header" onclick="Renderer.toggleMonthSection('${group.label}')">
            <h3>
              <i data-lucide="calendar" class="icon-md"></i>
              ${group.label}
            </h3>
            <span class="month-count">${meetingCount} møte${meetingCount !== 1 ? 'r' : ''}</span>
            <span class="month-toggle">
              <i data-lucide="chevron-down" class="icon-sm"></i>
            </span>
          </div>
          <div class="month-meetings">
            ${group.meetings.map(meeting => this.renderMeetingCard(meeting, false)).join('')}
          </div>
        </div>
      `;
    }).join('');
  },

  /**
   * Toggle month section expanded state
   */
  toggleMonthSection(monthLabel) {
    const sections = document.querySelectorAll('.month-section');
    sections.forEach(section => {
      if (section.dataset.month === monthLabel) {
        section.classList.toggle('expanded');
      }
    });
  },

  // ===== SCENARIO RENDERING FUNCTIONS =====

  /**
   * Render scenario card
   */
  renderScenarioCard(scenario, comparisonData = null) {
    if (!scenario) return '';

    const meta = typeof ScenarioHelpers !== 'undefined'
      ? ScenarioHelpers.getScenarioMeta(scenario.id)
      : { label: scenario.name, label_no: scenario.name_no, icon: '📋', color: '#6B7280' };

    const statusMeta = typeof ScenarioHelpers !== 'undefined'
      ? ScenarioHelpers.getStatusMeta(scenario.status)
      : { label: scenario.status, color: '#6B7280', icon: '📋' };

    const hasComparison = comparisonData && !comparisonData.isBaseline;

    return `
      <div class="scenario-card" style="border-color: ${meta.color}40;">
        <div class="scenario-header" style="background: ${meta.color}15;">
          <div class="scenario-icon" style="color: ${meta.color};"><i data-lucide="${meta.icon}" class="icon-lg"></i></div>
          <div class="scenario-title-section">
            <h3 class="scenario-title">${meta.label}</h3>
            <div class="scenario-subtitle">${meta.label_no}</div>
          </div>
          <div class="scenario-status" style="background: ${statusMeta.color}20; border-color: ${statusMeta.color};">
            <i data-lucide="${statusMeta.icon}" class="icon-xs"></i> ${statusMeta.label}
          </div>
        </div>

        <div class="scenario-body">
          <p class="scenario-description">${scenario.description}</p>

          <div class="scenario-metrics">
            <div class="metric-card">
              <div class="metric-icon"><i data-lucide="globe" class="icon-xl"></i></div>
              <div class="metric-info">
                <div class="metric-value">${scenario.climate_impact.co2_per_m2_bta} kg/m²</div>
                <div class="metric-label">CO₂ per m² BTA</div>
                ${hasComparison ? `
                  <div class="metric-comparison" style="color: ${typeof ScenarioHelpers !== 'undefined' ? ScenarioHelpers.getDifferenceColor(comparisonData.comparison.co2_per_m2) : '#6B7280'};">
                    ${typeof ScenarioHelpers !== 'undefined' ? ScenarioHelpers.formatPercentage(comparisonData.comparison.co2_per_m2) : comparisonData.comparison.co2_per_m2.toFixed(0) + '%'} vs demolition
                  </div>
                ` : ''}
              </div>
            </div>

            <div class="metric-card">
              <div class="metric-icon"><i data-lucide="box" class="icon-xl"></i></div>
              <div class="metric-info">
                <div class="metric-value">${scenario.climate_impact.material_emissions_per_m2} kg/m²</div>
                <div class="metric-label">Material Emissions</div>
                ${hasComparison ? `
                  <div class="metric-comparison" style="color: ${typeof ScenarioHelpers !== 'undefined' ? ScenarioHelpers.getDifferenceColor(comparisonData.comparison.material_emissions) : '#6B7280'};">
                    ${typeof ScenarioHelpers !== 'undefined' ? ScenarioHelpers.formatPercentage(comparisonData.comparison.material_emissions) : comparisonData.comparison.material_emissions.toFixed(0) + '%'} vs demolition
                  </div>
                ` : ''}
              </div>
            </div>

            <div class="metric-card">
              <div class="metric-icon"><i data-lucide="bar-chart-2" class="icon-xl"></i></div>
              <div class="metric-info">
                <div class="metric-value">${scenario.climate_impact.total_co2_tonnes.toLocaleString('nb-NO')} tonn</div>
                <div class="metric-label">Total CO₂</div>
                ${hasComparison ? `
                  <div class="metric-comparison" style="color: ${typeof ScenarioHelpers !== 'undefined' ? ScenarioHelpers.getDifferenceColor(comparisonData.comparison.total_co2) : '#6B7280'};">
                    ${typeof ScenarioHelpers !== 'undefined' ? ScenarioHelpers.formatPercentage(comparisonData.comparison.total_co2) : comparisonData.comparison.total_co2.toFixed(0) + '%'} vs demolition
                  </div>
                ` : ''}
              </div>
            </div>

            <div class="metric-card">
              <div class="metric-icon"><i data-lucide="zap" class="icon-xl"></i></div>
              <div class="metric-info">
                <div class="metric-value">${typeof scenario.energy_consumption_kwh_m2 === 'string' ? scenario.energy_consumption_kwh_m2 : scenario.energy_consumption_kwh_m2 + ' kWh/m²/år'}</div>
                <div class="metric-label">Energy Consumption</div>
              </div>
            </div>
          </div>

          ${scenario.comparison_to_demolition ? `
            <div class="scenario-highlight">
              <strong>Key Benefit:</strong> ${scenario.comparison_to_demolition}
            </div>
          ` : ''}
        </div>
      </div>
    `;
  },

  /**
   * Render comparison chart (simple bar chart)
   */
  renderComparisonChart(scenarios, metric = 'co2_per_m2') {
    if (!scenarios || scenarios.length === 0) return '';

    const metricInfo = typeof ScenarioHelpers !== 'undefined'
      ? ScenarioHelpers.METRICS[metric]
      : { label: metric, icon: '📊' };

    const chartData = typeof ScenarioHelpers !== 'undefined'
      ? ScenarioHelpers.generateChartData(scenarios, metric)
      : scenarios.map(s => ({
          id: s.id,
          label: s.name_no,
          value: s.climate_impact.co2_per_m2_bta,
          color: '#3B82F6'
        }));

    const maxValue = Math.max(...chartData.map(d => d.value));

    return `
      <div class="comparison-chart">
        <h3 class="chart-title">
          <i data-lucide="${metricInfo.icon}" class="icon-md"></i> ${metricInfo.label_no || metricInfo.label}
        </h3>
        <div class="chart-bars">
          ${chartData.map(data => {
            const percentage = (data.value / maxValue) * 100;
            const meta = typeof ScenarioHelpers !== 'undefined'
              ? ScenarioHelpers.getScenarioMeta(data.id)
              : { color: data.color };

            return `
              <div class="chart-bar-container">
                <div class="chart-bar-label">${data.label}</div>
                <div class="chart-bar-wrapper">
                  <div class="chart-bar" style="width: ${percentage}%; background-color: ${meta.color};">
                    <span class="chart-bar-value">
                      ${typeof metricInfo.format === 'function' ? metricInfo.format(data.value) : data.value}
                    </span>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  },

  /**
   * Render scenario comparison grid
   */
  renderScenarioGrid(scenarios, comparisonMatrix) {
    if (!scenarios || scenarios.length === 0) {
      return '<div class="empty-state">No scenarios available</div>';
    }

    return `
      <div class="scenario-grid">
        ${comparisonMatrix.map(item =>
          this.renderScenarioCard(item.scenario, item)
        ).join('')}
      </div>
    `;
  }
};

// Export for browser
if (typeof window !== 'undefined') {
  window.Renderer = Renderer;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Renderer;
}
