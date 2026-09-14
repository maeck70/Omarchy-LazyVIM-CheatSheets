#!/usr/bin/env python3
"""
Omarchy Keybindings Cheatsheet Generator
Generates a two-page Letter Size Portrait (8.5in x 11in) Cheatsheet in SVG and PDF.
Features larger, highly readable typography while strictly fitting within 2 portrait pages.
Supports both high-contrast Dark and Light (print-ready) themes.
"""

import os
import re
import subprocess

# Letter Portrait dimensions in typographic points (72 pt/in -> 8.5in x 11in)
PAGE_WIDTH = 612.0
PAGE_HEIGHT = 792.0

MARGIN_LEFT = 18.0
MARGIN_RIGHT = 18.0
MARGIN_TOP = 15.0
MARGIN_BOTTOM = 13.0

HEADER_Y = 15.0
HEADER_HEIGHT = 40.0
HEADER_DIVIDER_Y = 57.0

CONTENT_Y = 64.0
FOOTER_DIVIDER_Y = 769.0
FOOTER_Y = 780.0

USABLE_HEIGHT = FOOTER_DIVIDER_Y - CONTENT_Y  # 705.0 pt
NUM_COLS = 2
COL_GAP = 12.0
USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT  # 576.0 pt
COL_WIDTH = (USABLE_WIDTH - (NUM_COLS - 1) * COL_GAP) / NUM_COLS  # 282.0 pt

CARD_RADIUS = 5.0
CARD_HEADER_HEIGHT = 17.5
CARD_GAP = 8.5
KEYCAP_HEIGHT = 12.2
KEYCAP_Y_OFFSET = -8.6

FONT_SANS = "'Liberation Sans', 'Noto Sans', -apple-system, BlinkMacSystemFont, sans-serif"
FONT_MONO = "'JetBrainsMono Nerd Font', 'Liberation Mono', 'Noto Sans Mono', monospace"

# Page 1: System, Navigation, Workspaces & Desktop
PAGE_1_SECTIONS = [
    # Column 1
    {
        "col": 0,
        "title": "WINDOW MANAGEMENT",
        "color_dark": "#38bdf8",
        "color_light": "#0284c7",
        "items": [
            ("SUPER + W", "Close active focused window"),
            ("CTRL + ALT + DEL", "Close all open windows"),
            ("SUPER + T", "Toggle window floating / tiling"),
            ("SUPER + F", "Toggle fullscreen mode"),
            ("SUPER + CTRL + F", "Toggle tiled fullscreen mode"),
            ("SUPER + ALT + F", "Toggle full width (maximized)"),
            ("SUPER + J", "Toggle window split (H / V)"),
            ("SUPER + O", "Pop out (float & pin on top)"),
            ("SUPER + P", "Toggle pseudo window mode"),
            ("SUPER + L", "Toggle workspace layout mode"),
            ("SUPER + Home", "Restore saved window width"),
            ("SUPER + ALT + Home", "Save current window width"),
        ]
    },
    {
        "col": 0,
        "title": "FOCUS & NAVIGATION",
        "color_dark": "#0ea5e9",
        "color_light": "#0369a1",
        "items": [
            ("SUPER + ← ↓ ↑ →", "Move window focus in direction"),
            ("SUPER + SHIFT + ← ↓ ↑ →", "Swap active window position"),
            ("ALT + TAB", "Cycle focus to next window"),
            ("SHIFT + ALT + TAB", "Cycle focus to previous window"),
            ("CTRL + ALT + TAB", "Move focus to next monitor"),
            ("SHIFT + CTRL + ALT + TAB", "Move focus to previous monitor"),
            ("SUPER + Left Drag", "Move floating or tiled window"),
            ("SUPER + Right Drag", "Resize window interactively"),
            ("SUPER + Scroll ⇅", "Cycle workspace forward / back"),
            ("ALT + TAB (Hold)", "Reveal active window on top"),
        ]
    },
    {
        "col": 0,
        "title": "WINDOW RESIZING & GAPS",
        "color_dark": "#60a5fa",
        "color_light": "#1d4ed8",
        "items": [
            ("SUPER + - / =", "Expand / shrink width (100px)"),
            ("SUPER + ALT + - / =", "Fine adjust width (25px)"),
            ("SUPER + CTRL + - / =", "Coarse adjust width (300px)"),
            ("SUPER + SHIFT + - / =", "Shrink / expand height (100px)"),
            ("SUPER + SHIFT + ALT + - / =", "Fine adjust height (25px)"),
            ("SUPER + SHIFT + CTRL + - / =", "Coarse adjust height (300px)"),
            ("SUPER + BACKSPACE", "Toggle window transparency"),
            ("SUPER + SHIFT + BACKSPACE", "Toggle workspace window gaps"),
            ("SUPER + CTRL + BACKSPACE", "Toggle 1:1 square aspect ratio"),
            ("SUPER + CTRL + Z / ALT+Z", "Zoom in screen / Reset zoom"),
        ]
    },

    # Column 2
    {
        "col": 1,
        "title": "WORKSPACES & MONITORS",
        "color_dark": "#c084fc",
        "color_light": "#7e22ce",
        "items": [
            ("SUPER + 1–10", "Switch directly to workspace 1–10"),
            ("SUPER + SHIFT + 1–10", "Move focused window to ws 1–10"),
            ("SUPER + SHIFT + ALT + 1–10", "Move window silently to ws 1–10"),
            ("SUPER + TAB", "Switch to next workspace"),
            ("SUPER + SHIFT + TAB", "Switch to previous workspace"),
            ("SUPER + CTRL + TAB", "Switch to former active workspace"),
            ("SUPER + SHIFT + ALT + ←↓↑→", "Move ws to target monitor"),
            ("SUPER + S / ALT+S", "Toggle / Move to scratchpad"),
            ("SUPER + /", "Increase monitor display scaling"),
            ("SUPER + ALT + /", "Decrease monitor display scaling"),
            ("SUPER + CTRL + DEL", "Toggle laptop display on / off"),
            ("SUPER + CTRL + ALT + DEL", "Toggle laptop display mirroring"),
        ]
    },
    {
        "col": 1,
        "title": "WINDOW GROUPING (TABS)",
        "color_dark": "#a78bfa",
        "color_light": "#5b21b6",
        "items": [
            ("SUPER + G", "Toggle window grouping into tabs"),
            ("SUPER + ALT + G", "Move active window out of group"),
            ("SUPER + ALT + ← ↓ ↑ →", "Move window into adjacent group"),
            ("SUPER + ALT + TAB", "Next tab window in current group"),
            ("SUPER + SHIFT + ALT + TAB", "Previous tab in group"),
            ("SUPER + CTRL + ← / →", "Focus grouped window left / right"),
            ("SUPER + ALT + 1–5", "Switch directly to group tab 1–5"),
            ("SUPER + ALT + Scroll ⇅", "Cycle through window tabs in group"),
        ]
    },
    {
        "col": 1,
        "title": "OMARCHY SYSTEM & MENUS",
        "color_dark": "#fbbf24",
        "color_light": "#b45309",
        "items": [
            ("SUPER + SPACE", "Open Omarchy root launcher menu"),
            ("SUPER + ALT + SPACE", "Open applications launcher menu"),
            ("SUPER + ESC / XF86Power", "Open system power & session menu"),
            ("SUPER + SHIFT + SPACE", "Toggle top system status bar"),
            ("SUPER + CTRL + SPACE", "Open wallpaper background switcher"),
            ("SUPER + SHIFT + CTRL + SPACE", "Open theme switcher menu"),
            ("SUPER + K", "Open live keybindings menu"),
            ("SUPER + CTRL + L", "Lock workstation screen immediately"),
            ("SUPER + CTRL + O", "Open quick toggles settings menu"),
            ("SUPER + CTRL + H", "Open hardware configuration menu"),
            ("SUPER + CTRL + S", "Open Omarchy share & export menu"),
            ("SUPER + CTRL + 1–9", "Toggle top bar quick panels 1–9"),
        ]
    },
]

# Page 2: Applications, Web Apps, Screen Capture, Media & Controls
PAGE_2_SECTIONS = [
    # Column 1
    {
        "col": 0,
        "title": "CORE APPLICATIONS & TERMINALS",
        "color_dark": "#34d399",
        "color_light": "#047857",
        "items": [
            ("SUPER + ENTER", "Launch default terminal (Ghostty)"),
            ("SUPER + SHIFT + ENTER / B", "Launch primary web browser"),
            ("SUPER + SHIFT + ALT + B", "Launch private incognito browser"),
            ("SUPER + SHIFT + F", "Open file manager (Home directory)"),
            ("SUPER + SHIFT + ALT + F", "Open file manager (terminal CWD)"),
            ("SUPER + SHIFT + N", "Launch primary code editor (Neovim)"),
            ("SUPER + ALT + ENTER", "Launch Tmux session (SUPER+ALT+K)"),
            ("SUPER + CTRL + ENTER", "Launch Herdr manager (SUPER+CTRL+K)"),
            ("SUPER + SHIFT + D", "Launch Docker container dashboard"),
            ("SUPER + SHIFT + O", "Launch Obsidian knowledge base"),
            ("SUPER + SHIFT + W", "Launch Omawrite distraction-free"),
            ("SUPER + SHIFT + /", "Open 1Password password vault"),
        ]
    },
    {
        "col": 0,
        "title": "WEB APPS & ONLINE TOOLS",
        "color_dark": "#2dd4bf",
        "color_light": "#0f766e",
        "items": [
            ("SUPER + SHIFT + A", "Open ChatGPT web assistant app"),
            ("SUPER + SHIFT + ALT + A", "Open Grok AI assistant app"),
            ("SUPER + SHIFT + E", "Open primary email client (HEY)"),
            ("SUPER + SHIFT + ALT + E", "Open compose new email window"),
            ("SUPER + SHIFT + C", "Open primary calendar app (HEY)"),
            ("SUPER + SHIFT + G", "Launch Signal desktop messenger"),
            ("SUPER + SHIFT + ALT + G", "Open WhatsApp Web messenger app"),
            ("SUPER + SHIFT + CTRL + G", "Open Google Messages (SMS/RCS)"),
            ("SUPER + SHIFT + P", "Open Google Photos web library"),
            ("SUPER + SHIFT + S", "Open Google Maps navigation app"),
            ("SUPER + SHIFT + X / ALT+X", "Open X (Twitter) / New post"),
            ("SUPER + SHIFT + Y", "Launch YouTube web media player"),
        ]
    },
    {
        "col": 0,
        "title": "CLIPBOARD, VOICE & UTILITIES",
        "color_dark": "#fb7185",
        "color_light": "#be123c",
        "items": [
            ("SUPER + C", "Universal copy (GUI and terminal)"),
            ("SUPER + V", "Universal paste (GUI and terminal)"),
            ("SUPER + X", "Universal cut text selection"),
            ("SUPER + CTRL + V", "Open clipboard history panel"),
            ("SUPER + CTRL + E", "Open emoji & symbol picker"),
            ("SUPER + SHIFT + CTRL + A", "Open Omarchy AI agent picker"),
            ("SUPER + CTRL + X", "Toggle voice dictation (Voxtype)"),
            ("F9 (Push-to-Talk)", "Voice dictation (hold to speak)"),
            ("SHIFT + ALT + D / L", "Webapp Video DL / Copy URL"),
            ("SUPER + CTRL + .", "Transcode video / audio file"),
        ]
    },

    # Column 2
    {
        "col": 1,
        "title": "SCREEN CAPTURE & OCR",
        "color_dark": "#f43f5e",
        "color_light": "#9f1239",
        "items": [
            ("PRINT", "Interactive area screenshot capture"),
            ("ALT + PRINT", "Toggle screen recording on / off"),
            ("SUPER + PRINT", "Color picker (Hyprpicker hex/rgb)"),
            ("SUPER + CTRL + PRINT", "Extract text (OCR) from screen"),
            ("SUPER + CTRL + C", "Open capture options quick menu"),
            ("SUPER + ALT + [ / ]", "Resize webcam overlay PIP (– / +)"),
            ("RETURN / CTRL+RETURN", "Slurp: capture window / screen"),
            ("TAB / CTRL+TAB", "Slurp: cycle next / prev window"),
        ]
    },
    {
        "col": 1,
        "title": "NOTIFICATIONS & HUD STATUS",
        "color_dark": "#e879f9",
        "color_light": "#a21caf",
        "items": [
            ("SUPER + Comma", "Dismiss last popup notification"),
            ("SUPER + SHIFT + Comma", "Dismiss all popup notifications"),
            ("SUPER + ALT + Comma", "Invoke action of last notification"),
            ("SUPER + SHIFT + ALT + Comma", "Open full notification history"),
            ("SUPER + CTRL + Comma", "Toggle silence notifications (DND)"),
            ("SUPER + CTRL + R", "Set quick reminder timer"),
            ("SUPER + CTRL + ALT + R", "Show active reminders HUD"),
            ("SUPER + SHIFT + CTRL + R", "Clear all active reminders"),
            ("SUPER + CTRL + ALT + T", "Display floating time HUD"),
            ("SUPER + CTRL + ALT + B", "Display floating battery HUD"),
            ("SUPER + CTRL + ALT + W", "Display floating weather HUD"),
            ("SUPER + CTRL + N / I", "Toggle nightlight / Idle lock"),
        ]
    },
    {
        "col": 1,
        "title": "AUDIO, MEDIA & HARDWARE",
        "color_dark": "#a3e635",
        "color_light": "#3f6212",
        "items": [
            ("Vol + / Vol -", "Volume output up / down (5% steps)"),
            ("ALT + Vol + / -", "Precise volume up / down (1%)"),
            ("Mute / MicMute", "Toggle audio mute / Mic mute"),
            ("SHIFT + Mute", "Switch active audio output sink"),
            ("Play / Pause", "Media playback play / pause"),
            ("Next / Prev Track", "Skip track (or ALT / SH+ALT+Play)"),
            ("SHIFT + Play / Pause", "Switch active media source"),
            ("Bright + / Bright -", "Display brightness (5% steps)"),
            ("ALT + Bright + / -", "Precise brightness (1% steps)"),
            ("SHIFT + Bright + / -", "Brightness max (100%) / min (1%)"),
            ("KbdBright + / -", "Keyboard backlight brightness / cycle"),
            ("Touchpad Toggle", "Touchpad toggle on / off"),
            ("SUPER + CTRL + A / B", "Audio / Bluetooth settings panel"),
            ("SUPER + CTRL + D / W / P", "Display / Net / Power panel"),
            ("SUPER + CTRL + Q / XF86Calc", "Open calculator (omacalc)"),
        ]
    },
]


def escape_xml(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))


def parse_key_tokens(key_str):
    tokens = []
    parts = re.split(r'(\s*\+\s*|\s*/\s*)', key_str)
    for p in parts:
        p_clean = p.strip()
        if not p_clean:
            continue
        if p_clean in ('+', '/'):
            tokens.append(('sep', p_clean))
        else:
            tokens.append(('key', p_clean))
    return tokens


def get_token_width(text):
    """
    Computes precise typographic badge width in points for monospace labels.
    """
    length = len(text)
    if any(c in text for c in '←↓↑→⇅'):
        return max(12.5, length * 4.8 + 5.5)
    if length == 1:
        return 12.0
    elif length == 2:
        return 15.5
    elif length == 3:
        return 19.5
    elif length == 4:
        return 23.5
    elif length == 5:
        return 27.5
    else:
        return length * 4.4 + 5.5


def render_page_svg(page_num, total_pages, sections, theme="dark"):
    is_dark = (theme == "dark")
    
    if is_dark:
        bg_color = "#070a12"
        card_bg = "#0d1322"
        card_border = "#1c263c"
        header_bg = "#151e33"
        text_primary = "#ffffff"
        text_secondary = "#94a3b8"
        text_desc = "#cbd5e1"
        key_bg = "#19243b"
        key_border = "#2f3e5c"
        key_text = "#f8fafc"
        key_mod_bg = "#1e293b"
        key_mod_border = "#38bdf8"
        key_mod_text = "#38bdf8"
        sep_color = "#475569"
        divider_color = "#1c263c"
        footer_text = "#64748b"
        legend_pill_bg = "#0f172a"
        accent_title = "#38bdf8"
    else:
        # High contrast, clean modern light theme with soft slate canvas and white cards
        bg_color = "#edf2f7"
        card_bg = "#ffffff"
        card_border = "#cbd5e1"
        header_bg = "#f1f5f9"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        text_desc = "#1e293b"
        key_bg = "#f8fafc"
        key_border = "#94a3b8"
        key_text = "#0f172a"
        key_mod_bg = "#e0f2fe"
        key_mod_border = "#0284c7"
        key_mod_text = "#0369a1"
        sep_color = "#64748b"
        divider_color = "#cbd5e1"
        footer_text = "#475569"
        legend_pill_bg = "#ffffff"
        accent_title = "#0284c7"

    page_subtitles = {
        1: "KEYBINDINGS CHEATSHEET • PAGE 1: WINDOWS &amp; SYSTEM",
        2: "KEYBINDINGS CHEATSHEET • PAGE 2: APPS, MEDIA &amp; HARDWARE",
    }
    subtitle_text = page_subtitles.get(page_num, f"PAGE {page_num} OF {total_pages}")

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="8.5in" height="11in" viewBox="0 0 {PAGE_WIDTH} {PAGE_HEIGHT}">')
    
    # Enhanced, Larger Typography Styles
    svg.append('<defs>')
    svg.append(f'''<style>
      .font-sans {{ font-family: {FONT_SANS}; }}
      .font-mono {{ font-family: {FONT_MONO}; }}
      .doc-title {{ font-family: {FONT_SANS}; font-size: 18.0px; font-weight: 800; letter-spacing: 0.6px; }}
      .doc-subtitle {{ font-family: {FONT_SANS}; font-size: 7.6px; font-weight: 600; letter-spacing: 0.3px; }}
      .card-title {{ font-family: {FONT_SANS}; font-size: 8.8px; font-weight: 700; letter-spacing: 0.4px; }}
      .key-label {{ font-family: {FONT_MONO}; font-size: 6.6px; font-weight: 700; }}
      .key-sep {{ font-family: {FONT_MONO}; font-size: 6.2px; font-weight: 600; fill: {sep_color}; }}
      .desc-text {{ font-family: {FONT_SANS}; font-size: 7.6px; font-weight: 450; fill: {text_desc}; }}
      .footer-text {{ font-family: {FONT_SANS}; font-size: 6.8px; font-weight: 500; fill: {footer_text}; }}
      .legend-label {{ font-family: {FONT_SANS}; font-size: 6.8px; font-weight: 500; fill: {text_secondary}; }}
    </style>''')
    svg.append('</defs>')

    # Canvas Background
    svg.append(f'<rect width="{PAGE_WIDTH}" height="{PAGE_HEIGHT}" fill="{bg_color}"/>')

    # Top Header
    svg.append(f'<text x="{MARGIN_LEFT}" y="28.0" class="doc-title" fill="{text_primary}">OMARCHY <tspan fill="{accent_title}">QUATTRO</tspan></text>')
    svg.append(f'<text x="{MARGIN_LEFT}" y="43.0" class="doc-subtitle" fill="{text_secondary}">{subtitle_text}</text>')

    # Top Right Legend Pill
    legend_w = 246.0
    legend_x = PAGE_WIDTH - MARGIN_RIGHT - legend_w
    legend_y = 17.5
    svg.append(f'<rect x="{legend_x}" y="{legend_y}" width="{legend_w}" height="25" rx="3.5" ry="3.5" fill="{legend_pill_bg}" stroke="{card_border}" stroke-width="0.8"/>')
    
    legend_keys = [
        ("SUPER", "Win", key_mod_bg, key_mod_border, key_mod_text),
        ("ALT", "Alt", key_bg, key_border, key_text),
        ("CTRL", "Ctrl", key_bg, key_border, key_text),
        ("SHIFT", "Shift", key_bg, key_border, key_text),
        ("XF86", "Media", key_bg, key_border, key_text),
    ]
    cur_lx = legend_x + 6.0
    for key_lbl, desc_lbl, k_bg, k_brd, k_col in legend_keys:
        kw = get_token_width(key_lbl)
        svg.append(f'<rect x="{cur_lx}" y="{legend_y + 4.5}" width="{kw}" height="15.0" rx="2.2" ry="2.2" fill="{k_bg}" stroke="{k_brd}" stroke-width="0.6"/>')
        svg.append(f'<text x="{cur_lx + kw/2.0}" y="{legend_y + 14.8}" text-anchor="middle" class="key-label" fill="{k_col}">{key_lbl}</text>')
        cur_lx += kw + 2.8
        svg.append(f'<text x="{cur_lx}" y="{legend_y + 14.8}" class="legend-label">{desc_lbl}</text>')
        cur_lx += len(desc_lbl) * 3.8 + 5.5

    # Header Divider Line
    svg.append(f'<line x1="{MARGIN_LEFT}" y1="{HEADER_DIVIDER_Y}" x2="{PAGE_WIDTH - MARGIN_RIGHT}" y2="{HEADER_DIVIDER_Y}" stroke="{divider_color}" stroke-width="0.8"/>')

    # Organize cards by column (2 columns per page)
    cards_by_col = [[], []]
    for sec in sections:
        cards_by_col[sec["col"]].append(sec)

    total_avail_h = FOOTER_DIVIDER_Y - CONTENT_Y  # 705.0 pt

    for col_idx in range(NUM_COLS):
        col_x = MARGIN_LEFT + col_idx * (COL_WIDTH + COL_GAP)
        col_cards = cards_by_col[col_idx]
        num_cards = len(col_cards)
        
        total_card_gaps = (num_cards - 1) * CARD_GAP
        avail_for_cards = total_avail_h - total_card_gaps
        
        total_items = sum(len(c["items"]) for c in col_cards)
        total_headers = num_cards * CARD_HEADER_HEIGHT
        avail_for_rows = avail_for_cards - total_headers
        row_step = avail_for_rows / max(1, total_items)
        
        current_y = CONTENT_Y
        for i, card in enumerate(col_cards):
            item_count = len(card["items"])
            card_h = CARD_HEADER_HEIGHT + item_count * row_step
            card_w = COL_WIDTH
            accent = card["color_dark"] if is_dark else card["color_light"]

            svg.append(f'<g transform="translate({col_x:.2f}, {current_y:.2f})">')
            
            # Card Base
            svg.append(f'<rect width="{card_w:.2f}" height="{card_h:.2f}" rx="{CARD_RADIUS}" ry="{CARD_RADIUS}" fill="{card_bg}" stroke="{card_border}" stroke-width="0.85"/>')
            
            # Card Header Bar
            svg.append(f'<path d="M 0,{CARD_RADIUS} A {CARD_RADIUS},{CARD_RADIUS} 0 0,1 {CARD_RADIUS},0 L {card_w - CARD_RADIUS:.2f},0 A {CARD_RADIUS},{CARD_RADIUS} 0 0,1 {card_w:.2f},{CARD_RADIUS} L {card_w:.2f},{CARD_HEADER_HEIGHT} L 0,{CARD_HEADER_HEIGHT} Z" fill="{header_bg}"/>')
            svg.append(f'<line x1="0" y1="{CARD_HEADER_HEIGHT}" x2="{card_w:.2f}" y2="{CARD_HEADER_HEIGHT}" stroke="{card_border}" stroke-width="0.6"/>')
            
            # Left accent pill
            svg.append(f'<rect x="0" y="2.5" width="3.2" height="{CARD_HEADER_HEIGHT - 5.0:.2f}" rx="1.6" fill="{accent}"/>')
            
            # Card Title
            svg.append(f'<text x="9.5" y="12.0" class="card-title" fill="{accent}">{escape_xml(card["title"])}</text>')
            
            # Keybinding rows
            first_row_y = CARD_HEADER_HEIGHT + row_step * 0.70
            for r_idx, (key_str, desc_str) in enumerate(card["items"]):
                row_y = first_row_y + r_idx * row_step
                tokens = parse_key_tokens(key_str)
                
                token_x = 7.0
                for kind, val in tokens:
                    if kind == 'sep':
                        sep_w = 5.0 if val in ('+', '/') else 3.8
                        svg.append(f'<text x="{token_x + sep_w/2.0:.2f}" y="{row_y - 0.2:.2f}" text-anchor="middle" class="key-sep">{escape_xml(val)}</text>')
                        token_x += sep_w + 1.2
                    else:
                        badge_w = get_token_width(val)
                        badge_h = KEYCAP_HEIGHT
                        badge_y = row_y + KEYCAP_Y_OFFSET
                        
                        is_super = ("SUPER" in val)
                        b_fill = key_mod_bg if is_super else key_bg
                        b_stroke = key_mod_border if is_super else key_border
                        b_text = key_mod_text if is_super else key_text
                        b_stroke_w = "0.75" if is_super else "0.6"
                        
                        svg.append(f'<rect x="{token_x:.2f}" y="{badge_y:.2f}" width="{badge_w:.2f}" height="{badge_h}" rx="2.2" ry="2.2" fill="{b_fill}" stroke="{b_stroke}" stroke-width="{b_stroke_w}"/>')
                        svg.append(f'<text x="{token_x + badge_w/2.0:.2f}" y="{row_y - 0.5:.2f}" text-anchor="middle" class="key-label" fill="{b_text}">{escape_xml(val)}</text>')
                        token_x += badge_w + 1.8

                # Description: aligned cleanly with no cutoff
                desc_x = max(100.0, token_x + 3.8)
                svg.append(f'<text x="{desc_x:.2f}" y="{row_y:.2f}" class="desc-text">{escape_xml(desc_str)}</text>')

            svg.append('</g>')
            current_y += card_h + CARD_GAP

    # Bottom Footer
    svg.append(f'<line x1="{MARGIN_LEFT}" y1="{FOOTER_DIVIDER_Y}" x2="{PAGE_WIDTH - MARGIN_RIGHT}" y2="{FOOTER_DIVIDER_Y}" stroke="{divider_color}" stroke-width="0.8"/>')
    svg.append(f'<text x="{MARGIN_LEFT}" y="{FOOTER_Y}" class="footer-text">OMARCHY QUATTRO • HYPRLAND 0.54+ • PRESS <tspan fill="{accent_title}" font-weight="700">SUPER + K</tspan> FOR LIVE MENU</text>')
    svg.append(f'<text x="{PAGE_WIDTH - MARGIN_RIGHT}" y="{FOOTER_Y}" text-anchor="end" class="footer-text">PAGE {page_num} OF {total_pages} • LETTER PORTRAIT</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)

    # 1. Dark Theme SVGs
    dark_p1_svg = os.path.join(output_dir, "omarchy-keybindings-p1-dark.svg")
    dark_p2_svg = os.path.join(output_dir, "omarchy-keybindings-p2-dark.svg")
    with open(dark_p1_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(1, 2, PAGE_1_SECTIONS, "dark"))
    with open(dark_p2_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(2, 2, PAGE_2_SECTIONS, "dark"))
    print(f"Generated {dark_p1_svg} and {dark_p2_svg}")

    # 2. Light Theme SVGs
    light_p1_svg = os.path.join(output_dir, "omarchy-keybindings-p1-light.svg")
    light_p2_svg = os.path.join(output_dir, "omarchy-keybindings-p2-light.svg")
    with open(light_p1_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(1, 2, PAGE_1_SECTIONS, "light"))
    with open(light_p2_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(2, 2, PAGE_2_SECTIONS, "light"))
    print(f"Generated {light_p1_svg} and {light_p2_svg}")

    # 3. Default SVGs (default to dark)
    default_p1_svg = os.path.join(output_dir, "omarchy-keybindings-p1.svg")
    default_p2_svg = os.path.join(output_dir, "omarchy-keybindings-p2.svg")
    with open(default_p1_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(1, 2, PAGE_1_SECTIONS, "dark"))
    with open(default_p2_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(2, 2, PAGE_2_SECTIONS, "dark"))

    # Convert to 2-Page Portrait PDFs
    dark_pdf = os.path.join(output_dir, "omarchy-keybindings-dark.pdf")
    light_pdf = os.path.join(output_dir, "omarchy-keybindings-light.pdf")
    default_pdf = os.path.join(output_dir, "omarchy-keybindings.pdf")

    # Dark PDF (2 pages)
    subprocess.run([
        "rsvg-convert",
        "-f", "pdf",
        "--page-width=8.5in",
        "--page-height=11in",
        "-o", dark_pdf,
        dark_p1_svg,
        dark_p2_svg
    ], check=True)
    print(f"Rendered {dark_pdf} (2 pages)")

    # Light PDF (2 pages)
    subprocess.run([
        "rsvg-convert",
        "-f", "pdf",
        "--page-width=8.5in",
        "--page-height=11in",
        "-o", light_pdf,
        light_p1_svg,
        light_p2_svg
    ], check=True)
    print(f"Rendered {light_pdf} (2 pages)")

    # Default PDF (2 pages)
    subprocess.run([
        "rsvg-convert",
        "-f", "pdf",
        "--page-width=8.5in",
        "--page-height=11in",
        "-o", default_pdf,
        default_p1_svg,
        default_p2_svg
    ], check=True)
    print(f"Rendered {default_pdf} (2 pages)")

    # Individual page PDFs
    p1_pdf = os.path.join(output_dir, "omarchy-keybindings-p1.pdf")
    p2_pdf = os.path.join(output_dir, "omarchy-keybindings-p2.pdf")
    subprocess.run(["rsvg-convert", "-f", "pdf", "--page-width=8.5in", "--page-height=11in", "-o", p1_pdf, default_p1_svg], check=True)
    subprocess.run(["rsvg-convert", "-f", "pdf", "--page-width=8.5in", "--page-height=11in", "-o", p2_pdf, default_p2_svg], check=True)
    print(f"Rendered {p1_pdf} and {p2_pdf}")

    print("All two-page portrait sheets generated successfully.")


if __name__ == "__main__":
    main()
