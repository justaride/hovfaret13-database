const TabRouter = {
  getCurrentTab() {
    const params = new URLSearchParams(window.location.search);
    return params.get("tab") || "prosjektstyring";
  },

  setTab(tabId) {
    const params = new URLSearchParams(window.location.search);
    params.set("tab", tabId);
    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.history.pushState({ tab: tabId }, "", newUrl);
    window.dispatchEvent(
      new CustomEvent("tabchange", { detail: { tab: tabId } }),
    );
  },

  getTabFromPage(pageId) {
    if (typeof PAGE_CONFIG !== "undefined") {
      return PAGE_CONFIG.getTabForPage(pageId);
    }
    return "prosjektstyring";
  },

  buildPageUrl(href, tabId) {
    if (tabId) {
      return `${href}?tab=${tabId}`;
    }
    return href;
  },

  init() {
    window.addEventListener("popstate", (e) => {
      if (e.state && e.state.tab) {
        window.dispatchEvent(
          new CustomEvent("tabchange", { detail: { tab: e.state.tab } }),
        );
      }
    });
  },
};

if (typeof window !== "undefined") {
  window.TabRouter = TabRouter;
  TabRouter.init();
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = TabRouter;
}
