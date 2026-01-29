const ContentHeader = {
  inject(pageId) {
    const pageInfo = pageId ? PAGE_CONFIG.getPageInfo(pageId) : null;
    const tabId = pageId ? PAGE_CONFIG.getTabForPage(pageId) : "produksjon";
    const tabInfo = PAGE_CONFIG.tabs[tabId];
    const pageName =
      pageInfo?.name || document.title.replace(" - Hovfaret 13", "");

    const html = `
      <header class="content-header">
        <a href="index.html?tab=${tabId}" class="content-header-back">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          ${tabInfo?.label || "Oversikt"}
        </a>
        <h1 class="content-header-title">${pageName}</h1>
      </header>
    `;

    const existingOldHeader = document.querySelector(".app-header");
    if (existingOldHeader) existingOldHeader.remove();

    const existingTabHeader = document.querySelector(".tab-header");
    if (existingTabHeader) existingTabHeader.remove();

    const existingContentHeader = document.querySelector(".content-header");
    if (existingContentHeader) existingContentHeader.remove();

    document.querySelectorAll(".back-link").forEach((link) => link.remove());

    const existingNavBar = document.querySelector(".nav-bar");
    if (existingNavBar) existingNavBar.remove();

    const nav = document.createElement("div");
    nav.innerHTML = html;
    const header = nav.firstElementChild;
    document.body.insertBefore(header, document.body.firstChild);

    document.body.style.paddingTop = "48px";
  },
};

if (typeof window !== "undefined") {
  window.ContentHeader = ContentHeader;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = ContentHeader;
}
