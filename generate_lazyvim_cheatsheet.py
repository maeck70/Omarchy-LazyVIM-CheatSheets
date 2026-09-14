#!/usr/bin/env python3
"""
LazyVim Keybindings Cheatsheet Generator
Generates a two-page Letter Size Portrait (8.5in x 11in) Cheatsheet in SVG and PDF.
Features larger, highly readable typography strictly fitting within 2 portrait pages.
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

# Page 1: Core Editing, Motions, Precision Manipulation & Buffers
PAGE_1_SECTIONS = [
    # Column 0
    {
        "col": 0,
        "title": "MOTIONS & CURSOR NAVIGATION",
        "color_dark": "#34d399",
        "color_light": "#059669",
        "items": [
            ("h / j / k / l", "Move cursor left, down, up, right"),
            ("gj / gk", "Move down / up by visual screen line"),
            ("w / b", "Jump to start of next / previous word"),
            ("e / ge", "Jump to end of current / previous word"),
            ("0 / ^ / $", "Start of line / First non-blank / End"),
            ("gg / G", "Jump to first / last line of file"),
            ("{count}G / :{n}", "Jump directly to line number {n}"),
            ("H / M / L", "Move cursor to screen High / Middle / Low"),
            ("zt / zz / zb", "Scroll viewport: current line to top/mid/bot"),
            ("CTRL + O / I", "Jump backward / forward in jump list"),
            ("%", "Jump to matching paren, bracket, or block"),
            ("s / S", "Flash: jump anywhere on screen / Treesitter"),
        ]
    },
    {
        "col": 0,
        "title": "EDITING, OPERATORS & LINES",
        "color_dark": "#38bdf8",
        "color_light": "#0284c7",
        "items": [
            ("i / I", "Insert before cursor / at line start"),
            ("a / A", "Append after cursor / at end of line"),
            ("o / O", "Open new line below / above in insert mode"),
            ("c / d / y", "Change (cut+insert), Delete, Yank (copy)"),
            ("cc / dd / yy", "Change, delete, or yank current line"),
            ("x / s / S", "Delete char / Substitute char / Substitute line"),
            ("ALT + j / k", "Move active line or block down / up"),
            ("p / P", "Put (paste) clipboard text after / before"),
            ("u / CTRL + R", "Undo last modification / Redo change"),
            (".", "Repeat last text-editing modification"),
            (">> / <<", "Indent / unindent line right / left"),
            ("J / gJ", "Join line below with space / without space"),
        ]
    },
    {
        "col": 0,
        "title": "TEXT OBJECTS (OPERATOR + OBJECT)",
        "color_dark": "#fbbf24",
        "color_light": "#d97706",
        "items": [
            ("Operator + i / a", "Operator + Inner (content) / Around (border)"),
            ("iw / aw", "Inner word / A word (with trailing space)"),
            ("i\" / a\"", "Inner / around double quotes (or ' or `)"),
            ("i( / a(", "Inner / around parentheses () (or ib / ab)"),
            ("i{ / a{", "Inner / around curly braces {} (or iB / aB)"),
            ("i[ / a[", "Inner / around square brackets []"),
            ("it / at", "Inner / around HTML or XML markup tag"),
            ("ip / ap", "Inner / around paragraph block"),
            ("if / af", "Treesitter: Inner / around function"),
            ("ic / ac", "Treesitter: Inner / around class"),
            ("ih", "GitSigns: Inner Git hunk under cursor"),
        ]
    },

    # Column 1
    {
        "col": 1,
        "title": "IN-LINE FIND, REGISTERS & MARKS",
        "color_dark": "#2dd4bf",
        "color_light": "#0f766e",
        "items": [
            ("f{c} / F{c}", "Find character inline forward / backward"),
            ("t{c} / T{c}", "Till character inline (stop 1 char before)"),
            ("; / ,", "Repeat last inline character find same / opp"),
            ("* / #", "Search next / prev match of word under cursor"),
            ("CTRL + S", "Quick save current file (:w)"),
            ("\"+y / \"+p", "Yank / paste with desktop system clipboard"),
            ("\"0p", "Paste last yanked text (ignores deletes)"),
            ("\"_d", "Delete to black-hole reg (no overwrite)"),
            ("q{reg} / q", "Record macro into register a-z / Stop"),
            ("@{reg} / @@", "Play recorded macro / Repeat last macro"),
            ("m{a-z} / '{a-z}", "Set local mark a-z / Jump to mark line"),
        ]
    },
    {
        "col": 1,
        "title": "VISUAL & MULTI-LINE EDITING",
        "color_dark": "#fb7185",
        "color_light": "#e11d48",
        "items": [
            ("v / V", "Enter character visual mode / Line visual"),
            ("CTRL + V", "Enter block visual mode (column editing)"),
            ("o", "Switch cursor between visual selection ends"),
            ("gv", "Reselect previous visual highlight area"),
            ("I{txt} ESC", "Block mode: insert text before lines"),
            ("A{txt} ESC", "Block mode: append text after lines"),
            ("c{txt} ESC", "Block mode: change & replace column block"),
            ("< / >", "Shift lines left / right (retains selection)"),
            ("CTRL + SPACE", "Treesitter: expand selection scope"),
            ("BACKSPACE", "Treesitter: shrink selection scope"),
            (":sort / :sort u", "Sort highlighted lines alphabetically / Unique"),
        ]
    },
    {
        "col": 1,
        "title": "BUFFERS & TAB MANAGEMENT",
        "color_dark": "#c084fc",
        "color_light": "#7e22ce",
        "items": [
            ("SHIFT + h / l", "Prev / next open buffer (<S-h> / <S-l>)"),
            ("[b / ]b", "Navigate to previous / next buffer in tabline"),
            ("<leader> + bb / `", "Switch to other (last visited) buffer"),
            ("<leader> + bd", "Delete current buffer (Snacks bufdelete)"),
            ("<leader> + bo", "Delete all other buffers except active"),
            ("<leader> + bp", "Toggle pinned status of current buffer"),
            ("<leader> + bP", "Delete all non-pinned open buffers"),
            ("<leader> + bj", "Pick buffer interactively by badge letter"),
            ("<leader><tab> + new / d", "Open new tab (:tabnew) / Close tab"),
            ("<leader><tab> + ] / [", "Navigate to next / previous tab page"),
            ("<leader><tab> + o / l", "Close other tabs / Jump to last tab"),
        ]
    },
]

# Page 2: Windows, LSP, UI Toggles, Diagnostics, Pickers, Git & Sessions
PAGE_2_SECTIONS = [
    # Column 0
    {
        "col": 0,
        "title": "WINDOWS & SPLIT MANAGEMENT",
        "color_dark": "#38bdf8",
        "color_light": "#0284c7",
        "items": [
            ("CTRL + h / j / k / l", "Focus left / lower / upper / right split"),
            ("<leader> + -", "Split horizontally (new window below)"),
            ("<leader> + |", "Split vertically (new window right)"),
            ("<leader> + wd", "Close active split window (<C-w>c)"),
            ("<leader> + wm / uZ", "Toggle maximize / zoom active split"),
            ("CTRL + ↑ / ↓", "Resize split: increase / decrease height"),
            ("CTRL + ← / →", "Resize split: decrease / increase width"),
            ("CTRL + W + =", "Equalize dimensions across all open splits"),
            ("CTRL + W + HJKL", "Move active split to far left / bot / top / right"),
            ("CTRL + W + s / v", "Standard horizontal / vertical window split"),
            ("CTRL + W + SPACE", "Which-key Window Hydra mode (resize)"),
        ]
    },
    {
        "col": 0,
        "title": "LSP CODE INTELLIGENCE",
        "color_dark": "#2dd4bf",
        "color_light": "#0d9488",
        "items": [
            ("gd", "Goto definition of symbol under cursor"),
            ("gD", "Goto declaration of symbol under cursor"),
            ("gr", "Find all references of symbol in project"),
            ("gI", "Goto implementation of interface / symbol"),
            ("gy", "Goto type definition of symbol"),
            ("K", "Display hover documentation & signature"),
            ("gK / CTRL + K", "Display signature help (Normal / Insert)"),
            ("<leader> + ca", "Open LSP code actions menu (Normal & Visual)"),
            ("<leader> + cr", "Smart rename symbol everywhere in project"),
            ("<leader> + cR", "Smart rename file and update imports"),
            ("<leader> + cf", "Format active buffer or visual selection"),
        ]
    },
    {
        "col": 0,
        "title": "UI TOGGLES & SETTINGS (<leader>u)",
        "color_dark": "#fbbf24",
        "color_light": "#b45309",
        "items": [
            ("<leader> + uf / uF", "Toggle auto-format (global / buffer)"),
            ("<leader> + ud", "Toggle inline diagnostic virtual text"),
            ("<leader> + ul / uL", "Toggle line numbers / relative line numbers"),
            ("<leader> + us", "Toggle spell checking on / off"),
            ("<leader> + uw", "Toggle soft line wrapping on / off"),
            ("<leader> + uz", "Toggle Zen mode (distraction-free writing)"),
            ("<leader> + uh", "Toggle LSP inlay parameter hints"),
            ("<leader> + uT", "Toggle Treesitter syntax highlighting"),
            ("<leader> + ub", "Toggle background colorscheme dark / light"),
            ("<leader> + uG", "Toggle Git signs gutter column"),
            ("<leader> + un", "Dismiss all active floating notifications"),
        ]
    },

    # Column 1
    {
        "col": 1,
        "title": "DIAGNOSTICS, QUICKFIX & TROUBLE",
        "color_dark": "#f43f5e",
        "color_light": "#be123c",
        "items": [
            ("<leader> + cd", "Display line diagnostics in hover window"),
            ("]d / [d", "Jump to next / previous diagnostic issue"),
            ("]e / [e", "Jump to next / previous diagnostic error"),
            ("]w / [w", "Jump to next / previous diagnostic warning"),
            ("<leader> + xx", "Toggle Trouble workspace diagnostics panel"),
            ("<leader> + xX", "Toggle Trouble buffer-only diagnostics"),
            ("<leader> + cs", "Toggle Trouble document symbols outline"),
            ("<leader> + cS", "Toggle Trouble LSP references & definitions"),
            ("]q / [q", "Jump to next / previous Trouble / quickfix item"),
            ("]t / [t", "Jump to next / previous TODO comment"),
            ("<leader> + xt / xT", "Todo comments in Trouble (All / Fix)"),
        ]
    },
    {
        "col": 1,
        "title": "SEARCH, FIND & PICKERS (<leader>f/s)",
        "color_dark": "#a78bfa",
        "color_light": "#6d28d9",
        "items": [
            ("<leader> + <space>", "Fuzzy find files in project root"),
            ("<leader> + ff / fF", "Find files (project root / cwd)"),
            ("<leader> + fr / fR", "Browse recent files (all / cwd)"),
            ("<leader> + fn", "Create new empty file buffer (:enew)"),
            ("<leader> + e / fe", "Toggle file explorer tree (Neo-Tree / Snacks)"),
            ("<leader> + /", "Live grep search across project root"),
            ("<leader> + sg / sG", "Live grep search (project root / cwd)"),
            ("<leader> + sw / sW", "Search word under cursor (project / cwd)"),
            ("<leader> + sb", "Fuzzy search lines in current buffer"),
            ("<leader> + sk", "Search interactive keymaps list (Which-Key)"),
            ("<leader> + sr", "Search and replace across project (Grug-Far)"),
        ]
    },
    {
        "col": 1,
        "title": "GIT, TERMINAL & SESSIONS",
        "color_dark": "#a3e635",
        "color_light": "#3f6212",
        "items": [
            ("<leader> + gg / gG", "Open Lazygit terminal UI (Root Dir / cwd)"),
            ("]h / [h", "Jump to next / previous Git change hunk"),
            ("<leader> + ghs / ghr", "Stage current Git hunk / Reset (revert) hunk"),
            ("<leader> + ghu", "Undo last staged Git hunk"),
            ("<leader> + ghp", "Preview Git hunk diff inline"),
            ("<leader> + ghb / ghB", "View Git blame for current line / buffer"),
            ("CTRL + /", "Toggle floating terminal in project root"),
            ("<leader> + fT", "Toggle floating terminal in cwd"),
            ("CTRL + \\ + CTRL + N", "Escape terminal mode back to normal"),
            ("<leader> + . / S", "Toggle scratchpad buffer / Select scratchpad"),
            ("<leader> + qs / ql", "Restore project session / Restore last session"),
            ("<leader> + qq", "Save all modified files and quit LazyVim (:qa)"),
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
    # Split on " + " or " / "
    parts = re.split(r'(\s+\+\s+|\s+/\s+)', key_str)
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
    has_bracket = any(c in text for c in '()[]{}<>\'"`')
    extra = 1.6 if has_bracket else 0.0
    if length == 1:
        return 12.0 + extra
    elif length == 2:
        return 15.5 + extra
    elif length == 3:
        return 19.5 + extra
    elif length == 4:
        return 23.5 + extra
    elif length == 5:
        return 27.5 + extra
    else:
        return length * 4.4 + 5.5 + extra


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
        key_mod_bg = "#083344"
        key_mod_border = "#06b6d4"
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
        1: "KEYBINDINGS CHEATSHEET • PAGE 1: MOTIONS, EDITING &amp; ESSENTIALS",
        2: "KEYBINDINGS CHEATSHEET • PAGE 2: WINDOWS, LSP, TROUBLE &amp; TOOLS",
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
    svg.append(f'<text x="{MARGIN_LEFT}" y="28.0" class="doc-title" fill="{text_primary}">LAZY<tspan fill="{accent_title}">VIM</tspan></text>')
    svg.append(f'<text x="{MARGIN_LEFT}" y="43.0" class="doc-subtitle" fill="{text_secondary}">{subtitle_text}</text>')

    # Top Right Legend Pill
    legend_w = 250.0
    legend_x = PAGE_WIDTH - MARGIN_RIGHT - legend_w
    legend_y = 17.5
    svg.append(f'<rect x="{legend_x}" y="{legend_y}" width="{legend_w}" height="25" rx="3.5" ry="3.5" fill="{legend_pill_bg}" stroke="{card_border}" stroke-width="0.8"/>')

    legend_keys = [
        ("<leader>", "Space", key_mod_bg, key_mod_border, key_mod_text),
        ("CTRL", "Ctrl", key_bg, key_border, key_text),
        ("ALT", "Alt", key_bg, key_border, key_text),
        ("SHIFT", "Shift", key_bg, key_border, key_text),
        ("ESC", "Normal", key_bg, key_border, key_text),
    ]
    cur_lx = legend_x + 6.0
    for key_lbl, desc_lbl, k_bg, k_brd, k_col in legend_keys:
        kw = get_token_width(key_lbl)
        svg.append(f'<rect x="{cur_lx}" y="{legend_y + 4.5}" width="{kw}" height="15.0" rx="2.2" ry="2.2" fill="{k_bg}" stroke="{k_brd}" stroke-width="0.6"/>')
        svg.append(f'<text x="{cur_lx + kw/2.0}" y="{legend_y + 14.8}" text-anchor="middle" class="key-label" fill="{k_col}">{escape_xml(key_lbl)}</text>')
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

                        is_leader = ("<leader>" in val or val in ("<space>", "SPACE"))
                        b_fill = key_mod_bg if is_leader else key_bg
                        b_stroke = key_mod_border if is_leader else key_border
                        b_text = key_mod_text if is_leader else key_text
                        b_stroke_w = "0.75" if is_leader else "0.6"

                        svg.append(f'<rect x="{token_x:.2f}" y="{badge_y:.2f}" width="{badge_w:.2f}" height="{badge_h}" rx="2.2" ry="2.2" fill="{b_fill}" stroke="{b_stroke}" stroke-width="{b_stroke_w}"/>')
                        svg.append(f'<text x="{token_x + badge_w/2.0:.2f}" y="{row_y - 0.5:.2f}" text-anchor="middle" class="key-label" fill="{b_text}">{escape_xml(val)}</text>')
                        token_x += badge_w + 1.8

                # Description: aligned cleanly with no cutoff
                desc_x = max(96.0, token_x + 3.8)
                svg.append(f'<text x="{desc_x:.2f}" y="{row_y:.2f}" class="desc-text">{escape_xml(desc_str)}</text>')

            svg.append('</g>')
            current_y += card_h + CARD_GAP

    # Bottom Footer
    svg.append(f'<line x1="{MARGIN_LEFT}" y1="{FOOTER_DIVIDER_Y}" x2="{PAGE_WIDTH - MARGIN_RIGHT}" y2="{FOOTER_DIVIDER_Y}" stroke="{divider_color}" stroke-width="0.8"/>')
    svg.append(f'<text x="{MARGIN_LEFT}" y="{FOOTER_Y}" class="footer-text">LAZYVIM • NEOVIM 0.10+ • PRESS <tspan fill="{accent_title}" font-weight="700">&lt;leader&gt;sk</tspan> OR <tspan fill="{accent_title}" font-weight="700">&lt;leader&gt;?</tspan> FOR LIVE KEYMAPS</text>')
    svg.append(f'<text x="{PAGE_WIDTH - MARGIN_RIGHT}" y="{FOOTER_Y}" text-anchor="end" class="footer-text">PAGE {page_num} OF {total_pages} • LETTER PORTRAIT</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    previews_dir = os.path.join(output_dir, "previews")
    os.makedirs(previews_dir, exist_ok=True)

    # 1. Dark Theme SVGs
    dark_p1_svg = os.path.join(output_dir, "lazyvim-cheatsheet-p1-dark.svg")
    dark_p2_svg = os.path.join(output_dir, "lazyvim-cheatsheet-p2-dark.svg")
    with open(dark_p1_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(1, 2, PAGE_1_SECTIONS, "dark"))
    with open(dark_p2_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(2, 2, PAGE_2_SECTIONS, "dark"))
    print(f"Generated {dark_p1_svg} and {dark_p2_svg}")

    # 2. Light Theme SVGs
    light_p1_svg = os.path.join(output_dir, "lazyvim-cheatsheet-p1-light.svg")
    light_p2_svg = os.path.join(output_dir, "lazyvim-cheatsheet-p2-light.svg")
    with open(light_p1_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(1, 2, PAGE_1_SECTIONS, "light"))
    with open(light_p2_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(2, 2, PAGE_2_SECTIONS, "light"))
    print(f"Generated {light_p1_svg} and {light_p2_svg}")

    # 3. Default SVGs (default to dark)
    default_p1_svg = os.path.join(output_dir, "lazyvim-cheatsheet-p1.svg")
    default_p2_svg = os.path.join(output_dir, "lazyvim-cheatsheet-p2.svg")
    with open(default_p1_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(1, 2, PAGE_1_SECTIONS, "dark"))
    with open(default_p2_svg, "w", encoding="utf-8") as f:
        f.write(render_page_svg(2, 2, PAGE_2_SECTIONS, "dark"))

    # Convert to 2-Page Portrait PDFs
    dark_pdf = os.path.join(output_dir, "lazyvim-cheatsheet-dark.pdf")
    light_pdf = os.path.join(output_dir, "lazyvim-cheatsheet-light.pdf")
    default_pdf = os.path.join(output_dir, "lazyvim-cheatsheet.pdf")

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
    p1_pdf = os.path.join(output_dir, "lazyvim-cheatsheet-p1.pdf")
    p2_pdf = os.path.join(output_dir, "lazyvim-cheatsheet-p2.pdf")
    subprocess.run(["rsvg-convert", "-f", "pdf", "--page-width=8.5in", "--page-height=11in", "-o", p1_pdf, default_p1_svg], check=True)
    subprocess.run(["rsvg-convert", "-f", "pdf", "--page-width=8.5in", "--page-height=11in", "-o", p2_pdf, default_p2_svg], check=True)
    print(f"Rendered {p1_pdf} and {p2_pdf}")

    # Generate High-Resolution PNG Previews (150 DPI -> 1275x1650)
    previews = [
        (dark_p1_svg, os.path.join(previews_dir, "lazyvim-dark-page-1.png")),
        (dark_p2_svg, os.path.join(previews_dir, "lazyvim-dark-page-2.png")),
        (light_p1_svg, os.path.join(previews_dir, "lazyvim-light-page-1.png")),
        (light_p2_svg, os.path.join(previews_dir, "lazyvim-light-page-2.png")),
    ]
    for svg_path, png_path in previews:
        subprocess.run([
            "rsvg-convert",
            "-d", "150",
            "-p", "150",
            "-o", png_path,
            svg_path
        ], check=True)
        print(f"Generated preview: {png_path}")

    print("All LazyVim two-page portrait sheets and previews generated successfully.")


if __name__ == "__main__":
    main()
