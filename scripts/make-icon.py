#!/usr/bin/env python3
"""Writes extension/icons/icon.svg. The undo arrow is computed so that it stays exact:
a 270 degree ring with a straight-cut tail and a triangular head, centred optically in the window body.
PNG sizes are rendered from the SVG with resvg (see scripts/make-icons.sh)."""
import math, os

R, r = 32.0, 19.0                 # ring outer / inner radius (width 13, readable at small sizes)
HEAD_DEG, TAIL_DEG = 225, 495     # clockwise from the head (upper left) to the tail (lower left)
OVERLAP = 0                       # degrees the ring runs into the head (0: the ring ends at the head's base)
HALF, LENGTH = 14.0, 18.0         # head: half base width, height
CENTER = (64.0, 73.0)             # optical centre of the arrow inside the window body (y 16..128)

def pol(rad, deg):
    t = math.radians(deg)
    return (rad * math.cos(t), rad * math.sin(t))

Rm = (R + r) / 2
t = math.radians(HEAD_DEG)
ur, tang = (math.cos(t), math.sin(t)), (-math.sin(t), math.cos(t))
base = pol(Rm, HEAD_DEG)
b1 = (base[0] + HALF * ur[0], base[1] + HALF * ur[1])
b2 = (base[0] - HALF * ur[0], base[1] - HALF * ur[1])
tip = (base[0] - LENGTH * tang[0], base[1] - LENGTH * tang[1])

start = HEAD_DEG - OVERLAP
pts = [pol(R, d) for d in range(start, TAIL_DEG + 1)] + [pol(r, d) for d in range(start, TAIL_DEG + 1)] + [b1, b2, tip]
dx = CENTER[0] - (min(p[0] for p in pts) + max(p[0] for p in pts)) / 2
dy = CENTER[1] - (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
f = lambda p: "%.2f %.2f" % (p[0] + dx, p[1] + dy)

ring = "M%s A%.1f %.1f 0 1 1 %s L%s A%.1f %.1f 0 1 0 %s Z" % (
    f(pol(R, start)), R, R, f(pol(R, TAIL_DEG)), f(pol(r, TAIL_DEG)), r, r, f(pol(r, start)))
head = "M%s L%s L%s Z" % (f(b1), f(tip), f(b2))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <title>Per-Window Undo Close Tab</title>
  <defs>
    <!-- palette: one teal ramp. mist #edf5f5, sage #b8d9d9, lagoon #6ec4b9, tide #479a90, deep #2f6360, night #1a3434 -->
    <!-- light comes from the top left everywhere: every gradient runs from top left to bottom right -->
    <linearGradient id="body" x1="0" y1="0" x2="0.55" y2="1">
      <stop offset="0" stop-color="#7ccdc2"/>
      <stop offset="0.32" stop-color="#54aea3"/>
      <stop offset="0.68" stop-color="#3c7c77"/>
      <stop offset="1" stop-color="#264f4d"/>
    </linearGradient>
    <linearGradient id="backTab" x1="0" y1="0" x2="0.45" y2="1">
      <stop offset="0" stop-color="#b6ddd7"/>
      <stop offset="1" stop-color="#86c6bc"/>
    </linearGradient>
    <linearGradient id="arrow" gradientUnits="userSpaceOnUse" x1="30" y1="40" x2="92" y2="108">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#dcefec"/>
    </linearGradient>
  </defs>

  <!-- tab in the background: same height and same slanted edge as the active tab, a mid tint of the same hue.
       The active tab covers only the lower part of its slant, so the bevel stays readable. The tab reaches down
       behind the window, so the window's rounded top-left corner shows the tab, never the transparent background. -->
  <path d="M0 70V6A6 6 0 0 1 6 0H20a5 5 0 0 1 4 1.9L36 16V70Z" fill="url(#backTab)"/>
  <!-- active tab and window body: one surface, so the tab is part of the window and takes the same gradient.
       Everything runs to the edge of the icon and the corners are tight (r 7, tabs r 6). -->
  <path d="M0 23A7 7 0 0 1 7 16H30V6A6 6 0 0 1 36 0H84a5 5 0 0 1 4 1.9L100 16H121A7 7 0 0 1 128 23V121A7 7 0 0 1 121 128H7A7 7 0 0 1 0 121Z" fill="url(#body)"/>

  <!-- undo arrow: filled, sharp-edged, no shadow. The hairline stroke closes the antialiasing seam between ring and head. -->
  <g fill="url(#arrow)" stroke="url(#arrow)" stroke-width="0.6" stroke-linejoin="miter">
    <path d="{ring}"/>
    <path d="{head}"/>
  </g>
</svg>
'''
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "extension", "icons", "icon.svg")
open(out, "w").write(svg)
print("wrote", os.path.normpath(out))
