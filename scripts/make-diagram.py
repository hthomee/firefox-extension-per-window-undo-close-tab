#!/usr/bin/env python3
"""Writes docs/img/overview.en.svg: two small trees, what Firefox's built-in shortcut does and
what this add-on's command does. Palette and light direction match the icon (one teal ramp, light from the top left).
No canvas background: title and labels follow the colour scheme of the page they are shown on."""
import os
from xml.sax.saxutils import escape

TXT = {
 "en": {
  "title": "What the add-on changes",
  "r1_label": "Without the add-on, Firefox 116 and newer",
  "r1_root": ("Firefox's own shortcut", ["Mac: Cmd+Shift+T", "Windows and Linux: Ctrl+Shift+T"]),
  "r1_hub": ("One shared history", ["for all windows, in closing order"]),
  "r1_leaves": [
    ("A tab closed in another window", ["moves into the window you are in"]),
    ("A whole closed window", ["opens again as a new window"]),
    ("The entire previous session", ["comes back, often as several windows"]),
  ],
  "r2_label": "With the add-on",
  "r2_root": ("The add-on's shortcut", ["Mac: Option+Shift+T", "Windows and Linux: Alt+Shift+T"]),
  "r2_hub": ("This window's closed tabs only", ["nothing from any other window"]),
  "r2_leaves": [
    ("The last closed tab comes back", ["in this window"]),
    ("Everything else stays as it is", ["no tabs from other windows,", "no new windows,", "no session restore"]),
  ],
  "footer": "Tested on macOS with Firefox 157. Windows and Linux are untested.",
 },
}

FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Helvetica, Arial, sans-serif"
LINE = "#479a90"                 # tide
W, PAD = 1200, 40
ROOT_X, ROOT_W = PAD, 330
HUB_X, HUB_W = 430, 330
LEAF_X, LEAF_W = 810, W - PAD - 810
NODE_H = 76

def build(lang):
    t = TXT[lang]
    out = []
    a = out.append

    def node(x, y, w, h, fill, title, subs, tcol, scol, tsize=17, ssize=14):
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}"/>')
        n = len(subs)
        block = tsize + 6 + n * (ssize + 5)
        ty = y + (h - block) / 2 + tsize
        a(f'<text x="{x+20}" y="{ty:.0f}" font-size="{tsize}" font-weight="600" fill="{tcol}">{escape(title)}</text>')
        for i, s in enumerate(subs):
            a(f'<text x="{x+20}" y="{ty + 8 + (i+1)*(ssize+5) - 4:.0f}" font-size="{ssize}" fill="{scol}">{escape(s)}</text>')

    def link(x1, y1, x2, y2):
        mx = (x1 + x2) / 2
        a(f'<path d="M{x1} {y1} H{mx} V{y2} H{x2}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>')

    def tree(top, label, root, hub, leaves, theme):
        a(f'<text class="label" x="{PAD}" y="{top}" font-size="16" font-weight="600">{escape(label)}</text>')
        leaf_h = [26 + 22 + 19 * len(s) for _, s in leaves]
        gap = 14
        total = sum(leaf_h) + gap * (len(leaves) - 1)
        y0 = top + 26
        centre = y0 + total / 2
        ny = centre - NODE_H / 2
        # connectors first, so the nodes sit on top
        link(ROOT_X + ROOT_W, centre, HUB_X, centre)
        y = y0
        for h in leaf_h:
            link(HUB_X + HUB_W, centre, LEAF_X, y + h / 2)
            y += h + gap
        node(ROOT_X, ny, ROOT_W, NODE_H, theme["root"], root[0], root[1], theme["root_t"], theme["root_s"])
        node(HUB_X, ny, HUB_W, NODE_H, theme["hub"], hub[0], hub[1], theme["hub_t"], theme["hub_s"])
        y = y0
        for (title, subs), h in zip(leaves, leaf_h):
            node(LEAF_X, y, LEAF_W, h, theme["leaf"], title, subs, theme["leaf_t"], theme["leaf_s"], tsize=16, ssize=13.5)
            y += h + gap
        return y0 + total

    plain = {"root": "url(#plainRoot)", "hub": "url(#plainHub)", "leaf": "#e3eded",
             "root_t": "#1a3434", "root_s": "#3c5252", "hub_t": "#1a3434", "hub_s": "#3c5252",
             "leaf_t": "#1a3434", "leaf_s": "#3c5252"}
    teal = {"root": "url(#tealRoot)", "hub": "url(#tealHub)", "leaf": "#cfe8e4",
            "root_t": "#ffffff", "root_s": "#e3f2f0", "hub_t": "#ffffff", "hub_s": "#e3f2f0",
            "leaf_t": "#12302d", "leaf_s": "#2f5450"}

    # layout pass
    body = []
    saved = out
    out = body
    a = out.append
    end1 = tree(112, t["r1_label"], t["r1_root"], t["r1_hub"], t["r1_leaves"], plain)
    end2 = tree(end1 + 64, t["r2_label"], t["r2_root"], t["r2_hub"], t["r2_leaves"], teal)
    H = int(end2 + 64)
    out = saved
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
    a(f'<title>{escape(t["title"])}</title>')
    a('<style>.title,.label{fill:#1a3434}.foot{fill:#5c6b6b}'
      '@media (prefers-color-scheme: dark){.title,.label{fill:#e4efee}.foot{fill:#9db1b0}}</style>')
    a('<defs>'
      '<linearGradient id="plainRoot" x1="0" y1="0" x2="0.6" y2="1"><stop offset="0" stop-color="#f1f6f6"/><stop offset="1" stop-color="#d3e2e2"/></linearGradient>'
      '<linearGradient id="plainHub" x1="0" y1="0" x2="0.6" y2="1"><stop offset="0" stop-color="#f1f6f6"/><stop offset="1" stop-color="#d3e2e2"/></linearGradient>'
      '<linearGradient id="tealRoot" x1="0" y1="0" x2="0.6" y2="1"><stop offset="0" stop-color="#54aea3"/><stop offset="1" stop-color="#2f6360"/></linearGradient>'
      '<linearGradient id="tealHub" x1="0" y1="0" x2="0.6" y2="1"><stop offset="0" stop-color="#6ec4b9"/><stop offset="1" stop-color="#3c8a82"/></linearGradient>'
      '</defs>')
    a(f'<text class="title" x="{PAD}" y="58" font-size="26" font-weight="600">{escape(t["title"])}</text>')
    out.extend(body)
    a(f'<text class="foot" x="{PAD}" y="{H-24}" font-size="14">{escape(t["footer"])}</text>')
    a('</svg>')
    return "\n".join(out), H

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "img")
    for lang in ("en",):
        svg, h = build(lang)
        path = os.path.join(root, f"overview.{lang}.svg")
        open(path, "w").write(svg)
        print("wrote", os.path.normpath(path), "height", h)
