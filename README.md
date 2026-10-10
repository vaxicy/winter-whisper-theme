<p align="center">
  <img src="https://raw.githubusercontent.com/vaxicy/winter-whisper-theme/main/logo/logo128.png" width="128" alt="Winter Whisper Theme icon">
</p>

<h1 align="center">Winter Whisper Theme</h1>

<p align="center">A calm winter Chrome theme in muted lavender, soft periwinkle and icy blue.</p>

<p align="center">
  <img src="https://img.shields.io/badge/Chrome%20Web%20Store-theme-blue?logo=googlechrome" alt="Chrome Web Store">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-Non--Commercial-lightgrey" alt="license">
</p>

## About

Winter Whisper Theme brings a quiet winter moment to Chrome. A muted lavender frame wraps the top of the window, the toolbar, active tab and bookmarks bar cool into pale periwinkle, and the new tab page opens on icy blue so the page you are reading stays the brightest thing on screen. Deep gray-violet ink keeps tab titles, bookmark labels, toolbar icons and the address bar sharp on the light surfaces, and deep mist lavender marks the new tab header and every link. Active and inactive windows share one frame colour, so nothing shifts when the window loses focus. The design is flat colour throughout — no wallpaper, no textures, no gradients — and the transparent icon distils it into a six-arm snowflake above two breeze lines.

## Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Mist Lavender | `#A9A4D0` | Window frame (active and inactive) and window button background |
| Pale Periwinkle | `#D6DBF5` | Toolbar, active tab and bookmarks bar |
| Cool White | `#F7F9FF` | Omnibox (address bar) field |
| Icy Blue | `#E8EEFD` | New tab page background |
| Gray Violet Ink | `#373449` | Tab, bookmark, toolbar and new-tab text, toolbar icons |
| Deep Mist Lavender | `#686287` | New tab page header and links |
| Soft Periwinkle | `#C1C1E6` | Breeze lines in the icon (artwork only) |

The first six rows are the browser surfaces set in `manifest.json`. The last one is an artwork tone: it lives in the icon and in the store previews, and is deliberately kept out of the browser chrome where a paler tint would drop below readable contrast.

## Chrome UI notes

Not every pixel in the window comes from the manifest — Chrome and the operating system paint some of them — so the store previews follow what a real install renders:

- **Google wordmark on the new tab page:** drawn by Chrome as a single flat tint computed from the new tab background, so it appears soft blue here rather than as the four-colour brand mark.
- **Shortcut tiles:** Chrome tints the round shortcut buttons the same way, so they pick up the same pale blue tone instead of a fixed brand colour.
- **Window buttons, hover fills and separators:** painted by Chrome and Windows, and left in their own neutral tones on the lavender frame.
- **Address bar:** a cool white field with Chrome's own focus outline, which stays legible against the pale periwinkle toolbar.
- **AI cards and the *Customize Chrome* button:** Chrome's own dark surfaces, untouched by the theme.

## Features

- Muted lavender frame with a pale periwinkle toolbar and active tab for calm, readable browser chrome.
- Flat, solid colour design with no wallpaper, textures or gradients.
- Icy blue new tab page with deep gray-violet text and deep mist lavender header and links.
- One continuous frame colour whether the window is focused or not.
- Single-tone Google wordmark drawn by Chrome itself through `ntp_logo_alternate`.
- Pure theme: no scripts, no permissions, nothing collected.

## Install

### From source (unpacked)

1. Download or clone this repository.
2. Open Chrome and navigate to `chrome://extensions`.
3. Enable **Developer mode** in the top-right corner.
4. Click **Load unpacked** and select this folder.
5. The theme applies immediately; reset it any time under Settings, then Appearance, then Themes.

### From the Chrome Web Store

The store listing is in preparation. Until it is live, load the unpacked copy with the steps above.

## Preview

### Store screenshots · 1280×800

**Browser interface** — the themed window with a bookmarks bar and the new tab page.

![Winter Whisper Theme browser preview](https://raw.githubusercontent.com/vaxicy/winter-whisper-theme/main/store-assets/screenshots/en/screenshot-1-browser.png)

**Palette & highlights** — the tones the theme is built from and what each one controls.

![Winter Whisper Theme palette](https://raw.githubusercontent.com/vaxicy/winter-whisper-theme/main/store-assets/screenshots/en/screenshot-2-introduction.png)

### Store promo tiles

**Marquee tile · 1400×560** — “Soft lavender. Winter blue. A calmer space for everyday browsing.”

![Winter Whisper Theme marquee](https://raw.githubusercontent.com/vaxicy/winter-whisper-theme/main/store-assets/promo/1400x560.png)

**Small tile · 440×280** — “A quiet winter moment in every tab.”

<p align="center">
  <img src="https://raw.githubusercontent.com/vaxicy/winter-whisper-theme/main/store-assets/promo/440x280.png" width="440" alt="Winter Whisper Theme promo tile">
</p>

These are illustrative English HTML/CSS layouts rendered by headless Chromium and calibrated against a real installed Chrome session. Browser surfaces take their colours from `manifest.json`; the Chrome-painted details — the soft blue Google wordmark and shortcut circles, the white search field, the dark AI cards and the dark *Customize Chrome* button — follow the reference browser, and the sampled tones are listed in [`store-assets/ASSET-NOTES.md`](store-assets/ASSET-NOTES.md). Tabs and bookmarks use generic English labels. These are not native captures, so controls and new tab content can vary by browser version and operating system.

## Files

| File | Description |
|------|-------------|
| `manifest.json` | Chrome theme manifest (MV3) with an inline `theme` block — single source of truth for every colour |
| `logo/logo128.png` | Theme and store icon, 128x128, the only size the manifest references |
| `store-assets/screenshots/en/` | Store listing screenshots (1280x800) |
| `store-assets/promo/` | Promo tiles (440x280 and 1400x560) |
| `store-assets/references/` | The browser, introduction and promo mock-up HTML plus their PNG renders |
| `store-assets/ASSET-NOTES.md` | Calibration notes: which tones are manifest colours and which are sampled from Chrome |
| `store-assets/store-description.txt` | Store listing copy (English) |
| `scripts/generate-logo.py` | Draws the transparent 128x128 icon with Pillow |
| `scripts/generate-store-assets.py` | Renders both screenshots and both promo tiles from `manifest.json` colours |
| `scripts/requirements.txt` | Python dependencies for the asset generators |
| `scripts/package.ps1` | Builds the release ZIP and the store upload ZIP |
| `LICENSE` | Non-Commercial License (bilingual) |
| `.gitignore` | Keeps local caches, nested archives and scratch files out of the repository |

## Regenerating the assets

```
pip install -r scripts/requirements.txt
playwright install chromium

python scripts/generate-logo.py
python scripts/generate-store-assets.py
```

The logo script exports only `logo/logo128.png` with a transparent background and antialiased edges. The store generator renders all four assets in one pass — both screenshots and both promo tiles — and keeps the HTML sources in `store-assets/references/`, so a style change is made in the script and re-rendered, never patched onto a PNG. The approved logo is read from disk and is not redrawn by the store generator.

## Packaging

```
powershell -ExecutionPolicy Bypass -File scripts/package.ps1 -Force
```

Writes two archives to the default folder `D:\迅雷下载\vibe coding`:

- `winter-whisper-theme-1.0.0.zip` — the complete project with `manifest.json` at the archive root.
- `winter-whisper-theme-1.0.0-upload.zip` — `manifest.json` plus the `logo` folder only, for the Chrome Web Store upload form.

`-Force` overwrites existing archives, and `-OutputDirectory` sends them somewhere else. The script checks the manifest inside the ZIP against this project, confirms that every file the manifest references is present, and rejects repository metadata, local caches and nested archives. The screenshots and promo tiles travel inside the full ZIP, but the store form still needs them uploaded one by one: `store-assets/screenshots/en/` fills the two screenshot slots, `store-assets/promo/1400x560.png` is the marquee tile and `store-assets/promo/440x280.png` is the small tile.

## License

Non-Commercial License — personal use permitted, commercial use requires permission. See [LICENSE](LICENSE).
