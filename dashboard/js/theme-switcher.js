/**
 * Theme Switcher Component
 * Allows users to switch between different color themes
 * Persists theme choice in localStorage
 */

const ThemeSwitcher = {
  // Available themes
  themes: {
    'technical': { name: 'Technical Dark', file: 'skins/technical.css', icon: '🌙' },
    'technical-dusk': { name: 'Technical Dusk', file: 'skins/technical-dusk.css', icon: '🌆' },
    'technical-twilight': { name: 'Technical Twilight', file: 'skins/technical-twilight.css', icon: '🌇' },
    'technical-day': { name: 'Technical Day', file: 'skins/technical-day.css', icon: '🌄' }
  },

  // Default theme
  defaultTheme: 'technical-dusk',

  // Current theme
  currentTheme: null,

  // Initialize theme switcher
  init() {
    // Get saved theme or use default
    this.currentTheme = localStorage.getItem('hovfaret-theme') || this.defaultTheme;

    // Load the theme
    this.loadTheme(this.currentTheme);

    // Inject switcher UI into navigation
    this.injectUI();
  },

  // Load a theme by name
  loadTheme(themeName) {
    const theme = this.themes[themeName];
    if (!theme) {
      console.warn(`Theme "${themeName}" not found, using default`);
      themeName = this.defaultTheme;
    }

    // Remove existing theme link if any
    const existingLink = document.getElementById('theme-stylesheet');
    if (existingLink) {
      existingLink.remove();
    }

    // Create new theme link
    const link = document.createElement('link');
    link.id = 'theme-stylesheet';
    link.rel = 'stylesheet';
    link.href = theme.file;
    document.head.appendChild(link);

    // Update current theme
    this.currentTheme = themeName;

    // Save to localStorage
    localStorage.setItem('hovfaret-theme', themeName);

    console.log(`Theme loaded: ${theme.name}`);
  },

  // Switch to a different theme
  switchTheme(themeName) {
    if (themeName === this.currentTheme) return;

    this.loadTheme(themeName);

    // Update UI
    this.updateUI();

    // Optional: Add a subtle transition effect
    document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    setTimeout(() => {
      document.body.style.transition = '';
    }, 300);
  },

  // Inject theme switcher UI into navigation bar
  injectUI() {
    const navBar = document.querySelector('.nav-bar .nav-content');
    if (!navBar) {
      console.warn('Navigation bar not found, theme switcher UI not injected');
      return;
    }

    // Create theme switcher container
    const container = document.createElement('div');
    container.className = 'theme-switcher';
    container.style.cssText = 'margin-left: auto; display: flex; align-items: center; gap: 0.5rem;';

    // Create theme selector dropdown
    const select = document.createElement('select');
    select.id = 'theme-select';
    select.style.cssText = `
      padding: 0.4rem 0.8rem;
      background: var(--bg-tertiary, #1a2028);
      border: 1px solid var(--border-primary, #30363d);
      border-radius: 4px;
      color: var(--text-primary, #e6edf3);
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s;
      font-family: var(--font-sans);
    `;

    // Add options
    Object.entries(this.themes).forEach(([key, theme]) => {
      const option = document.createElement('option');
      option.value = key;
      option.textContent = `${theme.icon} ${theme.name}`;
      if (key === this.currentTheme) {
        option.selected = true;
      }
      select.appendChild(option);
    });

    // Add change event listener
    select.addEventListener('change', (e) => {
      this.switchTheme(e.target.value);
    });

    // Add hover effect using mouseenter/mouseleave
    select.addEventListener('mouseenter', () => {
      select.style.borderColor = 'var(--accent-primary, #58a6ff)';
      select.style.background = 'var(--bg-hover, #232930)';
    });

    select.addEventListener('mouseleave', () => {
      select.style.borderColor = 'var(--border-primary, #30363d)';
      select.style.background = 'var(--bg-tertiary, #1a2028)';
    });

    container.appendChild(select);
    navBar.appendChild(container);
  },

  // Update UI to reflect current theme
  updateUI() {
    const select = document.getElementById('theme-select');
    if (select) {
      select.value = this.currentTheme;
    }
  }
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => ThemeSwitcher.init());
} else {
  ThemeSwitcher.init();
}

// Export for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ThemeSwitcher;
}
