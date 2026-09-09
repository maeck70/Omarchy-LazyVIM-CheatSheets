# Omarchy Quattro Keybindings Cheatsheet

A complete, high-contrast, printable 2-page cheatsheet (US Letter Portrait, 8.5 × 11 in) for **Omarchy Quattro** running on **Hyprland**.

Available in both digital **Dark Theme** and ink-friendly **Light / Print Theme**.

---

## Previews

### Dark Theme
| Page 1: Windows & System | Page 2: Apps, Media & Hardware |
| :---: | :---: |
| <img src="previews/dark-page-1.png" width="400" alt="Dark Theme Page 1"/> | <img src="previews/dark-page-2.png" width="400" alt="Dark Theme Page 2"/> |

### Light Theme (Print-Ready)
| Page 1: Windows & System | Page 2: Apps, Media & Hardware |
| :---: | :---: |
| <img src="previews/light-page-1.png" width="400" alt="Light Theme Page 1"/> | <img src="previews/light-page-2.png" width="400" alt="Light Theme Page 2"/> |

---

## Downloads (PDF & SVG)

| Document | Format | Description |
| :--- | :--- | :--- |
| [**`omarchy-keybindings.pdf`**](omarchy-keybindings.pdf) | PDF (2 Pages) | Default 2-page cheatsheet (Dark theme, 8.5 × 11 in) |
| [**`omarchy-keybindings-light.pdf`**](omarchy-keybindings-light.pdf) | PDF (2 Pages) | High-contrast, ink-friendly 2-page cheatsheet for printing |
| [**`omarchy-keybindings-dark.pdf`**](omarchy-keybindings-dark.pdf) | PDF (2 Pages) | High-contrast dark theme 2-page cheatsheet |
| [**`omarchy-keybindings-p1.pdf`**](omarchy-keybindings-p1.pdf) | PDF (1 Page) | Page 1 standalone PDF (Windows, Workspaces & System) |
| [**`omarchy-keybindings-p2.pdf`**](omarchy-keybindings-p2.pdf) | PDF (1 Page) | Page 2 standalone PDF (Apps, Capture & Hardware) |
| [**`omarchy-keybindings-p1-light.svg`**](omarchy-keybindings-p1-light.svg) | SVG Source | Page 1 vector source (Light theme) |
| [**`omarchy-keybindings-p2-light.svg`**](omarchy-keybindings-p2-light.svg) | SVG Source | Page 2 vector source (Light theme) |
| [**`omarchy-keybindings-p1-dark.svg`**](omarchy-keybindings-p1-dark.svg) | SVG Source | Page 1 vector source (Dark theme) |
| [**`omarchy-keybindings-p2-dark.svg`**](omarchy-keybindings-p2-dark.svg) | SVG Source | Page 2 vector source (Dark theme) |

---

## Logical Group Overview

### Page 1: Windows, Navigation, Workspaces & System Menus
1. **Window Management**: Close window (`SUPER+W`), close all (`CTRL+ALT+DEL`), floating/tiling (`SUPER+T`), fullscreen modes (`SUPER+F`, `SUPER+CTRL+F`, `SUPER+ALT+F`), split toggle (`SUPER+J`), pop out (`SUPER+O`), pseudo window (`SUPER+P`), and layout mode (`SUPER+L`).
2. **Focus & Navigation**: Directional focus (`SUPER+←↓↑→`), window swap (`SUPER+SHIFT+←↓↑→`), window cycling (`ALT+TAB`), monitor focus (`CTRL+ALT+TAB`), and interactive mouse drag/resize.
3. **Window Resizing & Gaps**: Keyboard resizing (100px standard, 25px fine, 300px coarse), transparency toggle (`SUPER+BACKSPACE`), window gaps toggle, 1:1 square aspect, and screen zoom.
4. **Workspaces & Monitors**: Direct workspace switching (`SUPER+1–10`), moving windows (`SUPER+SHIFT+1–10`, silent move), monitor transfer, scratchpad (`SUPER+S / ALT+S`), display scaling, and laptop screen controls.
5. **Window Grouping (Tabs)**: Group toggling (`SUPER+G`), moving in/out of groups, tab cycling, tab navigation, and direct tab slot selection (`SUPER+ALT+1–5`).
6. **Omarchy System & Menus**: Root launcher (`SUPER+SPACE`), applications menu (`SUPER+ALT+SPACE`), power menu (`SUPER+ESC`), bar toggle, wallpaper switcher, theme switcher, and interactive key search (`SUPER+K`).

### Page 2: Core Applications, Web Apps, Capture & Hardware
7. **Core Applications & Terminals**: Ghostty terminal (`SUPER+ENTER`), browser (`SUPER+SHIFT+ENTER`), private browser, Nautilus file manager (Home & CWD), Neovim, Tmux, Herdr, Docker TUI, Obsidian, Omawrite, and 1Password.
8. **Web Apps & Online Tools**: ChatGPT, Grok AI, HEY Email & compose, Calendar, Signal messenger, WhatsApp Web, Google Messages, Google Photos, Google Maps, X (Twitter), and YouTube.
9. **Clipboard, Voice & Utilities**: Universal copy/paste/cut across GUI and terminal apps, clipboard history (`SUPER+CTRL+V`), emoji picker, AI agent launcher, Voxtype push-to-talk (`F9`), web app video download, and media transcoding.
10. **Screen Capture & OCR**: Screenshot (`PRINT`), screen recording (`ALT+PRINT`), color picker, screen OCR text extractor, capture menu, webcam overlay sizing, and slurp window/screen capture.
11. **Notifications & HUD Status**: Dismissing notifications, notification history, silence mode (DND), quick reminders, and floating time/battery/weather HUDs.
12. **Audio, Media & Hardware**: Volume controls (5% standard, 1% fine), microphone mute, playback controls, display and keyboard brightness adjustments, touchpad toggle, and desktop calculator.

---

## Regenerating Sheets

The cheatsheets are generated programmatically via Python and rendered to PDF using `rsvg-convert`:

```bash
# Requirements: python3, rsvg-convert (librsvg)
python3 generate_cheatsheet.py
```
