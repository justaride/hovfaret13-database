/**
 * Navigation Component
 * Reusable navigation bar for all dashboard pages
 */

const Navigation = {
  /**
   * Render navigation bar
   */
  render(currentPage = '') {
    return `
      <nav class="nav-bar">
        <div class="nav-content">
          <a href="index.html" class="nav-home">
            <span class="nav-icon">🏗️</span>
            <span class="nav-title">Hovfaret 13</span>
          </a>
          <div class="nav-breadcrumb">
            ${currentPage ? `<span class="nav-separator">→</span><span class="nav-current">${currentPage}</span>` : ''}
          </div>
        </div>
      </nav>
    `;
  },

  /**
   * Inject navigation into page
   */
  inject(currentPage = '') {
    const nav = document.createElement('div');
    nav.innerHTML = this.render(currentPage);
    document.body.insertBefore(nav.firstElementChild, document.body.firstChild);
  }
};

// Export for browser
if (typeof window !== 'undefined') {
  window.Navigation = Navigation;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Navigation;
}
