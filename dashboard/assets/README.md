# Building Image Asset

## Required Image

**Filename:** `building-elevation.png`

**Location:** This directory (`dashboard/assets/`)

---

## Image Specifications

### Format:
- **Type:** PNG (preferred for transparency)
- **Alternative:** SVG, JPG also work

### Content:
- Architectural elevation/facade drawing of Hovfaret 13
- White or light-colored lines on dark/transparent background works best
- Shows building from street level
- Preferably with vertical dimension visible (5+ floors)

### Size:
- **Width:** ~900-1200px recommended
- **Height:** Proportional to building
- **File size:** Keep under 1MB for fast loading

### Style Considerations:
- **Line drawing style** works best with dark theme
- **Transparent background** (PNG) allows flexibility
- **White/light gray lines** create good contrast
- **Technical/architectural** style matches dashboard aesthetic

---

## How to Add

### Option 1: Direct Copy
```bash
# Copy your image file
cp /path/to/your/building-image.png building-elevation.png
```

### Option 2: Export from Design Tool
1. Open your architectural drawing in Illustrator/Figma/etc.
2. Export as PNG with transparent background
3. Save as `building-elevation.png` in this directory

### Option 3: Screenshot/Scan
1. Screenshot or scan your architectural drawing
2. Optional: Remove background in Photoshop/GIMP
3. Save as `building-elevation.png`

---

## Image Will Appear In:

### 1. Original Design (`index.html`)
- Full-width centered display
- Own section with border frame
- Caption below
- ~900px max width

### 2. Hero Background Variant (`index-variant-hero-bg.html`)
- Large transparent background (8% opacity)
- Behind title and stats
- Subtle atmospheric effect
- ~1200px centered

### 3. Split Screen Variant (`index-variant-split.html`)
- Left 50% of hero section
- Full height display
- Interactive hover effect (scale 1.02x)
- Prominent feature element

---

## Fallback Behavior

If `building-elevation.png` is not present:

- **Original design:** Image section hides automatically
- **Hero BG variant:** No background, solid color only
- **Split variant:** Shows placeholder text

No errors, everything gracefully degrades!

---

## Testing

After adding image:

```bash
# Refresh in browser
# Or open fresh:
open http://localhost:8888/index.html
open http://localhost:8888/index-variant-hero-bg.html
open http://localhost:8888/index-variant-split.html
```

---

## Example Processing

If you have a dark-background drawing and need to invert:

```bash
# Using ImageMagick (if installed)
convert input.png -negate -transparent black building-elevation.png

# Or using Python + Pillow
python3 << EOF
from PIL import Image, ImageOps
img = Image.open('input.png')
inverted = ImageOps.invert(img.convert('RGB'))
inverted.save('building-elevation.png')
EOF
```

---

## Current Status

- [ ] Image not yet added
- [ ] Directory created and ready
- [ ] All three design variants ready to display image

**Once image is added, check this box:** ✓

---

**Last Updated:** 2025-11-21
