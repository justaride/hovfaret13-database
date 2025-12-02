# Hvordan Legge Til Bygningsbildet

## Raskeste måte:

### Steg 1: Lagre bildet fra chatten

Bildet du sendte i Claude-chatten:

1. **Høyreklikk på bildet** i chatten
2. Velg **"Lagre bilde som..."** eller **"Save Image As..."**
3. Naviger til: `/Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard/assets/`
4. Gi det navnet: **`building-elevation.png`**
5. Klikk **Lagre**

### Steg 2: Refresh browseren

```bash
# Refresh http://localhost:8888/index.html
# Eller trykk Cmd+R i browseren
```

Bygget vil nå vises:
- ✅ Som subtil transparent bakgrunn bak HELE siden (4% opacity)
- ✅ Som feature-bilde i hero-seksjonen

---

## Alternativ måte (via Terminal):

Hvis bildet ligger et annet sted:

```bash
# 1. Finn bildet ditt
ls -lt ~/Downloads/*.png | head -5

# 2. Kopier til riktig sted (bytt ut stien)
cp ~/Downloads/ditt-bilde.png \
   /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard/assets/building-elevation.png

# 3. Sjekk at det er der
ls -lh /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard/assets/
```

---

## Hva skjer når bildet er lagt til?

### Du vil se:

1. **Hele siden:**
   - Bygget som FULLSKJERM bakgrunn (8% opacity)
   - Fixed position - følger når du scroller
   - Cover mode - fyller hele viewport
   - Sentrert, skaleres automatisk

2. **Hero-seksjon:**
   - Elegant glassmorphic boks med backdrop blur
   - "Hovfaret 13" i Space Grotesk font (gradient)
   - "videre bruk" håndskrevet under (Caveat font)
   - Blå border med hover-glow
   - INGEN feature-bilde - kun bakgrunn

3. **Design:**
   - Original layout bevart
   - Oversiktlig struktur
   - Bygget legger til atmosfære uten å dominere
   - Modern, 2025-trendende glassmorphism

---

## Hvis bildet IKKE vises:

### Sjekk:

1. **Filnavn er riktig:**
   ```bash
   # Må være EKSAKT dette navnet:
   building-elevation.png

   # Ikke:
   building-elevation (1).png
   Building-Elevation.png
   bygning.png
   ```

2. **Lokasjon er riktig:**
   ```bash
   # Må ligge i:
   /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard/assets/

   # IKKE:
   /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/assets/
   /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard/
   ```

3. **Server kjører:**
   ```bash
   # Må kjøre fra dashboard-mappen:
   cd /Users/gabrielboen/2.0-Hovfaret13-NewStructureSimplified/dashboard
   python3 -m http.server 8888
   ```

4. **Har du refreshet browser?**
   - Trykk `Cmd + R` (Mac)
   - Eller `Cmd + Shift + R` (hard refresh)

---

## Feilsøking:

### Sjekk browser console:

1. Åpne Developer Tools (`Cmd + Option + I`)
2. Gå til **Console**-tab
3. Se etter 404-feil på `building-elevation.png`

Hvis du ser 404:
- Filnavnet eller plasseringen er feil
- Følg stegene over nøye

---

## Justere opacity (valgfritt):

Hvis bygget i bakgrunnen er for sterkt eller for svakt:

1. Åpne `dashboard/index.html` i editor
2. Finn linje ~23:
   ```css
   opacity: 0.08;  /* <-- Juster dette tallet */
   ```
3. Endre verdien:
   - `0.04` = Veldig subtil
   - `0.06` = Subtil
   - `0.08` = Medium synlig (standard)
   - `0.10` = Tydelig
   - `0.12` = Ganske synlig
4. Lagre og refresh

**Anbefaling:** 0.08 gir god balanse mellom tilstedeværelse og diskresjon.

---

## Test at det fungerer:

```bash
# Åpne homepage
open http://localhost:8888/index.html

# Du skal nå se:
✓ Bygget som fullskjerm bakgrunn (8% opacity)
✓ Glassmorphic hero-boks med blur
✓ "Hovfaret 13" i Space Grotesk font (gradient)
✓ "videre bruk" håndskrevet under
✓ Hover effect på hero-boks (border glow)
✓ Bygget følger deg når du scroller
```

---

**Trengs hjelp?**
- Sjekk at server kjører: `ps aux | grep python3 | grep 8888`
- Se server-logg for feil
- Prøv hard refresh: `Cmd + Shift + R`

**Status:**
- [ ] Bilde ikke lagt til ennå
- [ ] Klar til å legge til når du vil

---

**Oppdatert:** 2025-11-21 (v2.8.0)
**Design:** Fullscreen background + Glassmorphic hero
