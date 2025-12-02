# Design Variants for Homepage

Jeg har laget 3 forskjellige design-variantfor hvor jeg integrerer bygningsbildet på forskjellige måter:

## 📋 Oversikt

| Variant | Fil | Stil | Fokus |
|---------|-----|------|-------|
| **Original** | `index.html` | Bilde som egen seksjon | Balansert, tradisjonell |
| **Hero Background** | `index-variant-hero-bg.html` | Bilde som transparent bakgrunn | Subtil, elegant |
| **Split Screen** | `index-variant-split.html` | 50/50 split med bilde | Moderne, visuell |

---

## 1. Original Design (index.html)

**Stil:** Klassisk layout med bilde som egen seksjon

### Layout:
```
┌─────────────────────────────┐
│     Hovfaret 13 Title       │
│     Subtitle                │
├─────────────────────────────┤
│                             │
│   [Building Image]          │
│   Full width, centered      │
│                             │
├─────────────────────────────┤
│   Project Info Grid         │
│   (6 stat cards)            │
├─────────────────────────────┤
│   Dashboard Cards           │
│   (3x2 grid)                │
└─────────────────────────────┘
```

### Fordeler:
- ✅ Tydelig fokus på bygget
- ✅ Enkel struktur
- ✅ Bilde får full oppmerksomhet
- ✅ Fungerer godt på mobil

### Egenskaper:
- Bilde vises i egen ramme med border
- Caption under bildet
- Hover effect (lys opp)
- Graceful fallback hvis bilde mangler

---

## 2. Hero Background Variant (index-variant-hero-bg.html)

**Stil:** Bygget som stor, transparent bakgrunnselement

### Layout:
```
┌─────────────────────────────┐
│  [Transparent Building BG]  │
│  ┌───────────────────────┐  │
│  │  Hovfaret 13 Title    │  │
│  │  Subtitle             │  │
│  └───────────────────────┘  │
│  ┌───────────────────────┐  │
│  │  Key Stats Grid       │  │
│  │  (4 big numbers)      │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
├─────────────────────────────┤
│   Dashboard Cards           │
│   (3x2 grid)                │
└─────────────────────────────┘
```

### Fordeler:
- ✅ Elegant og subtil
- ✅ Fokus på data og tall
- ✅ Bygget skaper dybde uten å dominere
- ✅ Profesjonell look

### Egenskaper:
- Building image: 8% opacity, centered
- Stats grid med backdrop blur (glassmorphism)
- Big numbers (1989, 6100, 48%, 50%)
- Text overlays building seamlessly

---

## 3. Split Screen Variant (index-variant-split.html)

**Stil:** 50/50 split-screen med bygget på venstre side

### Layout:
```
┌──────────────┬──────────────┐
│              │              │
│  [Building]  │  Title       │
│  Image       │  Tagline     │
│  Full        │  4 Stats     │
│  Height      │  [CTA Btn]   │
│              │              │
└──────────────┴──────────────┘
├─────────────────────────────┤
│  Dashboard Modules          │
│  (Compact 6-grid)           │
└─────────────────────────────┘
```

### Fordeler:
- ✅ Moderne, visuell
- ✅ Bygget er hovedfokus
- ✅ Clean separation
- ✅ Strong CTA button

### Egenskaper:
- 50/50 split på desktop
- Building image: full height, interactive (hover scale)
- Big prominent CTA button to timeline
- Compact dashboard cards below
- Mobile: stacks vertically (image on top)

---

## Sammenligning

### Visual Impact:
| Variant | Impact | Best For |
|---------|--------|----------|
| Original | ⭐⭐⭐ | Traditional, balanced presentation |
| Hero BG | ⭐⭐⭐⭐ | Data-focused, professional dashboards |
| Split | ⭐⭐⭐⭐⭐ | Visual storytelling, marketing |

### Byggets rolle:
- **Original**: Bilde = Own section
- **Hero BG**: Bilde = Atmospheric background
- **Split**: Bilde = Co-star element

### Kompleksitet:
- **Original**: Simple ⚙️
- **Hero BG**: Medium ⚙️⚙️
- **Split**: Medium ⚙️⚙️

### Mobile Experience:
- **Original**: ⭐⭐⭐⭐⭐ (works perfectly)
- **Hero BG**: ⭐⭐⭐⭐ (background reduces on small screens)
- **Split**: ⭐⭐⭐⭐ (stacks well vertically)

---

## Testing Variants

For å teste hver variant:

```bash
# Start server hvis ikke allerede kjører
cd dashboard
python3 -m http.server 8888

# Åpne hver variant:
open http://localhost:8888/index.html                    # Original
open http://localhost:8888/index-variant-hero-bg.html    # Hero Background
open http://localhost:8888/index-variant-split.html      # Split Screen
```

---

## Recommendation

**For Technical Dashboard (data-focused):**
→ **Hero Background Variant**
- Profesjonell
- Data i fokus
- Subtil bruk av arkitektur

**For Public Website (storytelling):**
→ **Split Screen Variant**
- Visuelt sterkt
- Bygget får oppmerksomhet
- Modern look

**For Balanced Approach:**
→ **Original Design**
- Trygt valg
- Enkel å vedlikeholde
- Bilde og data begge synlige

---

## Customization

Alle varianter støtter:
- Dark theme (technical skin)
- Responsive design
- Hover effects
- Graceful fallback hvis bilde mangler
- Same navigation system

---

## Next Steps

1. **Test alle tre** i browser
2. **Velg favoritt** basert på bruk
3. **Rename chosen variant** til `index.html`
4. **Add building image** til `assets/building-elevation.png`
5. **Optional**: Mix elements fra forskjellige varianter

---

## ✅ Final Design Chosen

**Selected:** Custom variant based on Original + Hero Background hybrid

The final implementation combines the best of both:
- Original layout structure (clean, oversiktlig)
- Fullscreen building background (like Hero BG variant)
- Glassmorphic hero box (new element)
- Modern typography (Space Grotesk + Caveat)

See `index.html` for the implemented design.

---

**Created:** 2025-11-21
**Version:** 2.8.0 (Final Design Implemented)
