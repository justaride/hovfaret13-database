const TabHeader = {
  currentTab: "prosjektstyring",
  currentPageId: null,

  render(pageId = null) {
    this.currentPageId = pageId;
    const tab = pageId
      ? PAGE_CONFIG.getTabForPage(pageId)
      : TabRouter.getCurrentTab();
    this.currentTab = tab;

    return `
      <header class="tab-header">
        <div class="tab-header-content">
          <a href="index.html" class="tab-logo">
            <div class="tab-logo-icon">H13</div>
            <span class="tab-logo-text">Hovfaret 13</span>
          </a>
          <nav class="tab-nav">
            ${this.renderTabs()}
          </nav>
          <div class="tab-header-stats">
            <div class="tab-stat">
              <span class="tab-stat-value">70</span>
              <span class="tab-stat-label">Møter</span>
            </div>
            <div class="tab-stat">
              <span class="tab-stat-value">271</span>
              <span class="tab-stat-label">Dokumenter</span>
            </div>
          </div>
        </div>
        ${pageId ? this.renderSubNav(tab) : ""}
      </header>
    `;
  },

  renderTabs() {
    return Object.entries(PAGE_CONFIG.tabs)
      .map(
        ([id, tab]) => `
      <a href="index.html?tab=${id}"
         class="tab-nav-item ${this.currentTab === id ? "active" : ""}"
         data-tab="${id}">
        <span class="tab-nav-icon">${tab.icon}</span>
        <span class="tab-nav-label">${tab.label}</span>
      </a>
    `,
      )
      .join("");
  },

  renderSubNav(tabId) {
    const tab = PAGE_CONFIG.tabs[tabId];
    if (!tab) return "";

    let pages = [];
    if (tab.pages) {
      pages = tab.pages;
    } else if (tab.categories) {
      pages = Object.values(tab.categories).flatMap((cat) => cat.pages);
    }

    if (pages.length === 0) return "";

    return `
      <div class="tab-subnav">
        <div class="tab-subnav-content">
          ${pages
            .map(
              (page) => `
            <a href="${page.href}?tab=${tabId}"
               class="tab-subnav-item ${this.currentPageId === page.id ? "active" : ""}"
               title="${page.desc}">
              ${page.name}
            </a>
          `,
            )
            .join("")}
        </div>
      </div>
    `;
  },

  inject(pageId = null) {
    const existingHeader = document.querySelector(".tab-header");
    if (existingHeader) existingHeader.remove();

    const nav = document.createElement("div");
    nav.innerHTML = this.render(pageId);

    const header = nav.firstElementChild;
    document.body.insertBefore(header, document.body.firstChild);

    this.adjustExistingHeader();
    this.attachEventListeners();
    this.adjustBodyPadding();
  },

  adjustExistingHeader() {
    const appHeader = document.querySelector(".app-header");
    if (appHeader) {
      appHeader.style.position = "relative";
      appHeader.style.top = "auto";
      appHeader.style.zIndex = "auto";
      const backLink = appHeader.querySelector(".back-link");
      if (backLink) backLink.remove();
    }
    const pageHeader = document.querySelector(".header");
    if (pageHeader) {
      const backLink = pageHeader.querySelector(".back-link");
      if (backLink) backLink.remove();
    }
  },

  attachEventListeners() {
    document.querySelectorAll(".tab-nav-item").forEach((item) => {
      item.addEventListener("click", (e) => {
        if (
          window.location.pathname.endsWith("index.html") ||
          window.location.pathname.endsWith("/")
        ) {
          e.preventDefault();
          const tabId = item.dataset.tab;
          TabRouter.setTab(tabId);
          this.updateActiveTab(tabId);
        }
      });
    });

    window.addEventListener("tabchange", (e) => {
      this.updateActiveTab(e.detail.tab);
    });
  },

  updateActiveTab(tabId) {
    this.currentTab = tabId;
    document.querySelectorAll(".tab-nav-item").forEach((item) => {
      item.classList.toggle("active", item.dataset.tab === tabId);
    });
  },

  adjustBodyPadding() {
    const header = document.querySelector(".tab-header");
    if (header) {
      const height = header.offsetHeight;
      document.body.style.paddingTop = `${height}px`;
    }
  },
};

if (typeof window !== "undefined") {
  window.TabHeader = TabHeader;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = TabHeader;
}
