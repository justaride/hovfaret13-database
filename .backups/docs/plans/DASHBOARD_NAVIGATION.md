# Dashboard Navigation Guide

## Structure Overview

```
dashboard/
├── index.html              # Homepage with all dashboard links
├── timeline-v2.html        # Timeline view (with nav)
├── lib/
│   ├── navigation.js       # Reusable navigation component
│   ├── data-loader.js      # Data loading
│   └── renderer.js         # Rendering
├── skins/
│   └── technical.css       # Includes nav styling
└── assets/
    └── building-elevation.png  # Building image (to be added)
```

## Navigation System

All dashboard pages include a sticky navigation bar at the top:

```
🏗️ Hovfaret 13 → [Current Page Name]
```

- **Left:** Home link (returns to index.html)
- **Right:** Breadcrumb showing current page

### How It Works

The navigation is injected via JavaScript:

```javascript
// In any dashboard page
<script src="lib/navigation.js"></script>
<script>
  Navigation.inject('Page Name Here');
</script>
```

This adds a sticky nav bar at the top of the page automatically.

## Homepage (index.html)

**URL:** http://localhost:8888/index.html

### Features:

1. **Hero Section**
   - Large "Hovfaret 13" title
   - Building elevation image (architectural drawing)
   - Project subtitle

2. **Project Info Cards**
   - Location: Hovfaret 13, Skøyen, Oslo
   - Built: 1989
   - Area: 6,100 m² BTA
   - CO₂ savings: 48% lower
   - Owner: Urbania Eiendom AS
   - Status: Under planlegging

3. **Dashboard Cards**

| Card | Status | Link | Description |
|------|--------|------|-------------|
| **Project Timeline** | ✅ Available | `timeline-v2.html` | 32 events, 37 meetings, 3 views |
| **Document Explorer** | 🔜 Coming Soon | - | 271 documents, 10 categories |
| **Stakeholder Network** | 🔜 Coming Soon | - | 22 people, 13 organizations |
| **Scenario Comparison** | 🔜 Coming Soon | - | 6 scenarios, CO₂ comparison |
| **Meeting Browser** | 🔜 Coming Soon | - | 37 meetings, full transcripts |
| **Sustainability Report** | 🔜 Coming Soon | - | ESRS-aligned report |

### Card Interactions:

- **Available cards** (Timeline): Click to navigate → Full interactivity
- **Coming soon cards**: Disabled, shows "Coming Soon" badge

## Adding Building Image

To display the architectural drawing on the homepage:

```bash
# Copy your building elevation image
cp /path/to/your/building-image.png dashboard/assets/building-elevation.png
```

The image should be:
- **Format:** PNG with transparent background (preferred)
- **Content:** Architectural elevation/facade drawing
- **Size:** ~900px wide recommended
- **Style:** Line drawing (white/light lines on dark bg works best)

If no image is present, the image section will hide automatically (via `onerror` handler).

## Creating New Dashboard Pages

When creating new pages, follow this template:

```html
<!DOCTYPE html>
<html lang="no">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title - Hovfaret 13</title>
  <link rel="stylesheet" href="skins/technical.css">
</head>
<body>
  <div class="container">
    <!-- Your content here -->
  </div>

  <!-- Navigation -->
  <script src="lib/navigation.js"></script>
  <script>
    Navigation.inject('Your Page Name');
  </script>

  <!-- Other scripts -->
  <script src="lib/data-loader.js"></script>
  <!-- ... -->
</body>
</html>
```

**Key requirements:**
1. Include `skins/technical.css` for consistent styling
2. Include `lib/navigation.js` and call `Navigation.inject('Page Name')`
3. Use `.container` class for main content
4. Navigation will automatically link back to homepage

## Navigation Styling

Navigation CSS is included in `skins/technical.css`:

- **Sticky positioning**: Stays at top when scrolling
- **Backdrop blur**: Slightly transparent with blur effect
- **Dark theme**: Matches technical skin colors
- **Responsive**: Adjusts for mobile screens
- **Hover effects**: Home link highlights on hover

### Customization:

To customize navigation appearance, edit these classes in `technical.css`:

```css
.nav-bar { /* Main navigation container */ }
.nav-content { /* Inner content wrapper */ }
.nav-home { /* Home link */ }
.nav-icon { /* Building icon */ }
.nav-title { /* "Hovfaret 13" text */ }
.nav-breadcrumb { /* Current page indicator */ }
.nav-separator { /* Arrow separator */ }
.nav-current { /* Current page name */ }
```

## URL Structure

All pages are accessible via:

```
http://localhost:8888/
├── index.html              # Homepage (also accessible as /)
├── timeline-v2.html        # Timeline view
├── documents.html          # (coming soon)
├── stakeholders.html       # (coming soon)
├── scenarios.html          # (coming soon)
├── meetings.html           # (coming soon)
└── sustainability.html     # (coming soon)
```

## Testing Navigation

1. **Start server:**
   ```bash
   cd dashboard
   python3 -m http.server 8888
   ```

2. **Open homepage:**
   ```
   http://localhost:8888/index.html
   ```

3. **Test navigation:**
   - Click "Project Timeline" card → Should open timeline-v2.html
   - Click "🏗️ Hovfaret 13" in nav bar → Should return to homepage
   - Verify breadcrumb shows "Project Timeline"

4. **Check sticky behavior:**
   - Scroll down on timeline page
   - Navigation bar should stay at top

## Updating Index Page

To add new dashboard cards to the homepage, edit `index.html`:

```html
<!-- New card template -->
<a href="your-page.html" class="dashboard-card available" style="text-decoration: none;">
  <span class="card-badge">Available</span>
  <div class="card-icon">🎯</div>
  <div class="card-title">Your Page Title</div>
  <div class="card-description">
    Description of what this page does.
  </div>
  <div class="card-stats">
    <div class="card-stat">
      <div class="card-stat-value">100</div>
      <div class="card-stat-label">Items</div>
    </div>
  </div>
</a>
```

**Change badge from "Coming Soon" to "Available" when ready:**

```html
<!-- Before: -->
<span class="card-badge coming-soon">Coming Soon</span>

<!-- After: -->
<span class="card-badge">Available</span>
```

## Best Practices

1. **Always include navigation** on every dashboard page
2. **Use descriptive page names** in breadcrumb
3. **Keep card descriptions concise** (2-3 sentences max)
4. **Update card stats** when data changes
5. **Test navigation links** before marking as "Available"
6. **Maintain consistent styling** via `technical.css`

---

**Last Updated:** 2025-11-21
**Version:** 2.6.0
