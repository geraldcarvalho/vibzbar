#!/usr/bin/env python3
"""
The drawing vocabulary the ornaments are built from: stroke and wash
helpers, the six glass shapes, and the garnish.  ornaments.py imports it.

Everything is drawn in its own local space -- for a glass, rim at y=0
growing down, centred on x=0 -- so a garnish is positioned against the
glass rather than against the page, and the arrangement scales as one.

The book's twelve plates are photographs and are not generated here.
"""
import base64, math, pathlib, random

W, H = 1760, 1240
PX, PY, PW, PH = 88.0, 270.0, 1582.0, 698.0        # the open book
GUT = PX + PW / 2                                   # the spine
LCX = PX + PW * 0.25                                # left page centre
RCX = PX + PW * 0.75                                # right page centre
PCY = PY + PH / 2

INK   = '#2b2721'
INK_2 = '#6b6154'
LAV   = '#9a6a3e'
LAV_D = '#9a6a3e'
PAPER = '#f5f3f0'


SITE = pathlib.Path('/Users/geraldcarvalho/Dropbox/My Mac (Geralds-MacBook-Pro.local)'
                    '/Documents/Claude_Projects/vibz-site')
OUT  = SITE / 'vibz'
FONT = SITE / 'sketchbook' / 'instrument-serif.woff2'

# An SVG used as an image is an isolated document -- it cannot reach the
# page's @font-face, so the display face travels inside each file.
FONT_CSS = ("@font-face{font-family:'IS';font-style:normal;font-weight:400;"
            "src:url(data:font/woff2;base64,%s) format('woff2')}"
            % base64.b64encode(FONT.read_bytes()).decode('ascii'))


# ----------------------------------------------------------------- helpers
def stroke(d, w=3.4, c=INK, o=1.0, dash=None, fill='none'):
    x = ('<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f" '
         'stroke-linecap="round" stroke-linejoin="round" opacity="%.3f"'
         % (d, fill, c, w, o))
    if dash:
        x += ' stroke-dasharray="%s"' % dash
    return x + '/>'


def wash(d, c=LAV, o=0.20):
    """one flat lay-in of colour behind the line, like a single wash"""
    return '<path d="%s" fill="%s" opacity="%.3f"/>' % (d, c, o)


def circ(cx, cy, r, w=3.4, c=INK, o=1.0, fill='none'):
    return ('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="%s" '
            'stroke-width="%.2f" opacity="%.3f"/>' % (cx, cy, r, fill, c, w, o))


def ell(cx, cy, rx, ry, w=3.4, c=INK, o=1.0, fill='none'):
    return ('<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="%s" '
            'stroke="%s" stroke-width="%.2f" opacity="%.3f"/>'
            % (cx, cy, rx, ry, fill, c, w, o))


def text(x, y, s, size=34, fam="'IS',Georgia,serif", c=INK, o=1.0,
         anchor='start', ls=0.0, italic=False):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return ('<text x="%.2f" y="%.2f" font-family="%s" font-size="%.1f" '
            'fill="%s" opacity="%.3f" text-anchor="%s" letter-spacing="%.2f"%s>'
            '%s</text>' % (x, y, fam, size, c, o, anchor, ls,
                           ' font-style="italic"' if italic else '', s))


def grp(sx, sy, content, scale=1.0, rot=0.0):
    t = 'translate(%.2f,%.2f)' % (sx, sy)
    if rot:   t += ' rotate(%.2f)' % rot
    if scale != 1.0: t += ' scale(%.4f)' % scale
    return '<g transform="%s">%s</g>' % (t, content)


# ------------------------------------------------------------- the glasses
# Each returns (svg, height, half_width) in local space: rim at y=0.

def g_coupe():
    bowl = 'M -104 0 C -104 62 -58 96 0 96 C 58 96 104 62 104 0 Z'
    s = (wash(bowl)
         + stroke('M -104 0 C -104 62 -58 96 0 96 C 58 96 104 62 104 0')
         + stroke('M -113 0 L 113 0', 3.8)
         + stroke('M 0 96 L 0 176')
         + stroke('M -58 180 C -58 170 58 170 58 180')
         + ell(0, 181, 58, 8, 3.4))
    return s, 190, 113, 400


def g_martini():
    bowl = 'M -106 0 L 0 112 L 106 0 Z'
    s = (wash(bowl)
         + stroke('M -106 0 L 0 112 L 106 0')
         + stroke('M -115 0 L 115 0', 3.8)
         + stroke('M 0 112 L 0 180')
         + ell(0, 185, 56, 8, 3.4))
    return s, 194, 115, 420


def g_rocks():
    s = (wash('M -74 40 L -70 118 Q -70 132 -54 132 L 54 132 '
              'Q 70 132 70 118 L 74 40 Z')
         + stroke('M -78 0 L -70 118 Q -70 132 -54 132 L 54 132 '
                  'Q 70 132 70 118 L 78 0')
         + stroke('M -87 0 L 87 0', 3.8)
         + stroke('M -74 38 L 74 38', 2.2, INK_2, .45))
    return s, 134, 87, 300


def g_highball():
    s = (wash('M -49 56 L -45 196 Q -45 208 -32 208 L 32 208 '
              'Q 45 208 45 196 L 49 56 Z')
         + stroke('M -54 0 L -45 196 Q -45 208 -32 208 L 32 208 '
                  'Q 45 208 45 196 L 54 0')
         + stroke('M -63 0 L 63 0', 3.8)
         + stroke('M -50 54 L 50 54', 2.2, INK_2, .45))
    return s, 210, 63, 430


def g_flute():
    s = (wash('M -38 14 C -38 96 -16 140 0 150 C 16 140 38 96 38 14 Z')
         + stroke('M -40 0 C -40 96 -16 142 0 152 C 16 142 40 96 40 0')
         + stroke('M -49 0 L 49 0', 3.8)
         + stroke('M 0 152 L 0 212')
         + ell(0, 217, 50, 8, 3.4))
    return s, 226, 50, 470


def g_balloon():
    bowl = 'M -108 2 C -122 74 -86 132 0 132 C 86 132 122 74 108 2 Z'
    s = (wash(bowl)
         + stroke('M -108 2 C -122 74 -86 132 0 132 C 86 132 122 74 108 2')
         + stroke('M -117 0 L 117 0', 3.8)
         + stroke('M 0 132 L 0 194')
         + stroke('M -62 198 C -62 188 62 188 62 198')
         + ell(0, 199, 62, 9, 3.4))
    return s, 208, 117, 450


# ------------------------------------------------------------- the garnish
def citrus(cx, cy, r, c=INK, o=1.0, seg=8):
    out = [wash('M %.2f %.2f m %.2f 0 a %.2f %.2f 0 1 0 %.2f 0 '
                'a %.2f %.2f 0 1 0 %.2f 0' % (cx, cy, -r, r, r, 2 * r, r, r, -2 * r),
                LAV, .16 * o),
           circ(cx, cy, r, 3.0, c, o),
           circ(cx, cy, r * 0.80, 1.8, c, .55 * o)]
    for i in range(seg):
        a0 = (i / seg) * 2 * math.pi + 0.17
        a1 = ((i + 1) / seg) * 2 * math.pi - 0.17
        out.append(stroke('M %.2f %.2f L %.2f %.2f A %.2f %.2f 0 0 1 %.2f %.2f Z'
                          % (cx, cy,
                             cx + math.cos(a0) * r * .72, cy + math.sin(a0) * r * .72,
                             r * .72, r * .72,
                             cx + math.cos(a1) * r * .72, cy + math.sin(a1) * r * .72),
                          1.6, c, .5 * o))
    return ''.join(out)


def wedge(x, y, s=1.0, c=INK, rot=0, o=1.0):
    """a cut wedge of citrus -- rind, pith and flesh, seen edge on"""
    rind = 'M -62 34 A 62 62 0 0 1 62 34 Z'
    pith = 'M -52 34 A 52 52 0 0 1 52 34 Z'
    parts = [wash(rind, LAV, .16 * o), stroke(rind, 3.0, c, o),
             stroke(pith, 1.8, c, .5 * o)]
    for k in (-1, 0, 1):
        parts.append(stroke('M %.1f 34 L %.1f %.1f' % (k * 17, k * 26, -6),
                            1.5, c, .45 * o))
    return grp(x, y, ''.join(parts), s, rot)


def wheel_on_rim(hw, r=46, side=1, c=INK):
    """a wheel of citrus notched over the rim, the way it is actually served"""
    cx = side * hw * 0.62
    return (citrus(cx, -6, r, c)
            + stroke('M %.1f %.1f L %.1f %.1f' % (cx, -6 + r * .12, cx, -6 + r),
                     2.2, PAPER, 1.0)
            + stroke('M %.1f %.1f L %.1f %.1f' % (cx, -6 + r * .18, cx, -6 + r * .96),
                     1.6, c, .45))


def leaf_sprig(x, y, s=1.0, c=INK, rot=0, n=3):
    leaf = 'M 0 0 C -19 -14 -29 -43 -13 -59 C 4 -45 8 -18 0 0 Z'
    parts = [stroke('M 0 0 C -5 -40 -7 -80 -5 -116', 3.0, c)]
    for i, (r2, dx, dy, sc) in enumerate(
            [(-30, -3, -34, 1.0), (28, 1, -56, .9), (-12, -5, -82, .74)][:n]):
        parts.append(grp(dx, dy, wash(leaf, LAV, .2) + stroke(leaf, 2.6, c)
                         + stroke('M 0 0 C -10 -18 -14 -37 -12 -52', 1.5, c, .45),
                         sc, r2))
    return grp(x, y, ''.join(parts), s, rot)


def rosemary(x, y, s=1.0, c=INK, rot=-12):
    """needles curve away from the stem and shorten toward the tip, or the
       sprig reads as a fishbone"""
    parts = [stroke('M 0 0 C -6 -46 -8 -94 -3 -140', 3.2, c)]
    for i in range(13):
        t = i / 12.0
        yy = -16 - t * 118
        ln = 34 * (1 - t * .5)
        bx = -6 + t * 3
        for sgn in (-1, 1):
            parts.append(stroke('M %.1f %.1f Q %.1f %.1f %.1f %.1f'
                                % (bx, yy,
                                   bx + sgn * ln * .5, yy - ln * .5,
                                   bx + sgn * ln * .72, yy - ln * 1.02),
                                1.9, c, .8))
    return grp(x, y, ''.join(parts), s, rot)


def beans(x, y, s=1.0, c=INK):
    parts = []
    for dx, dy, r2 in ((0, 0, -20), (46, 7, 14), (23, -33, 3)):
        parts.append(grp(dx, dy, ell(0, 0, 19, 13, 2.6, c)
                         + stroke('M -13 0 C -5 -7 5 -7 13 0', 1.9, c, .65), 1.0, r2))
    return grp(x, y, ''.join(parts), s)


def cube(x, y, s=1.0, c=INK, o=.9):
    body = 'M -46 -20 L 0 -44 L 46 -20 L 46 32 L 0 56 L -46 32 Z'
    return grp(x, y, wash(body, LAV, .13)
               + stroke(body, 2.8, c, o)
               + stroke('M -46 -20 L 0 4 L 46 -20', 2.3, c, o * .75)
               + stroke('M 0 4 L 0 56', 2.3, c, o * .75), s)


def bubbles(x, y, c=INK, n=8, spread_x=22):
    random.seed(int(x * 7 + y))
    out = []
    yy = 0
    for i in range(n):
        t = i / float(n - 1)
        out.append(circ(x + random.uniform(-spread_x, spread_x), y + yy,
                        5.2 - t * 3.0, 2.0, c, .8 - t * .5))
        yy -= random.uniform(26, 40)
    return ''.join(out)


def saltrim(y, half, c=INK, seed=1):
    random.seed(seed)
    out = []
    for i in range(30):
        t = i / 29.0
        out.append(circ(-half + t * half * 2, y + random.uniform(-4, 8),
                        random.uniform(1.7, 3.3), 0, c, .48, fill=c))
    return ''.join(out)


def shelf(hw, y, c=INK, o=.15):
    """the faint rule the drink is stood on"""
    return stroke('M %.1f %.1f L %.1f %.1f' % (-hw, y, hw, y), 1.3, c, o)


# --------------------------------------------------------------- the paper
def defs():
    return f'''<defs>
  <linearGradient id="pg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#faf8f5"/>
    <stop offset=".52" stop-color="{PAPER}"/>
    <stop offset="1" stop-color="#edeae5"/>
  </linearGradient>
  <linearGradient id="spine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{INK}" stop-opacity="0"/>
    <stop offset=".38" stop-color="{INK}" stop-opacity=".09"/>
    <stop offset=".5" stop-color="{INK}" stop-opacity=".16"/>
    <stop offset=".62" stop-color="{INK}" stop-opacity=".09"/>
    <stop offset="1" stop-color="{INK}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="halo" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{LAV}" stop-opacity=".30"/>
    <stop offset="1" stop-color="{LAV}" stop-opacity="0"/>
  </radialGradient>
  <filter id="grainf" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="5"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <clipPath id="page"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}"/></clipPath>
  <style>{FONT_CSS}</style>
</defs>'''


def paper():
    return f'''
  <rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" fill="url(#pg)"/>
  <g opacity=".085"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}"
       filter="url(#grainf)"/></g>
  <rect x="{GUT - 76}" y="{PY}" width="152" height="{PH}" fill="url(#spine)"/>
  <line x1="{GUT}" y1="{PY + 14}" x2="{GUT}" y2="{PY + PH - 14}"
        stroke="{INK}" stroke-width="1" opacity=".15"/>
  <rect x="{PX + .7}" y="{PY + .7}" width="{PW - 1.4}" height="{PH - 1.4}"
        fill="none" stroke="{INK}" stroke-width="1.4" opacity=".12"/>'''


# ---------------------------------------------------------------- a spread
def spread(name, sub, drink_svg, notes, method):
    body = ['<ellipse cx="%.1f" cy="%.1f" rx="312" ry="252" fill="url(#halo)"/>'
            % (LCX, PCY + 6), drink_svg]

    x, y = RCX - 258, PY + 172
    body.append(text(x, y, name, 76))
    body.append(stroke('M %.1f %.1f L %.1f %.1f' % (x, y + 28, x + 92, y + 28),
                       2.6, LAV_D, .9))
    body.append(text(x, y + 66, sub, 26, 'Georgia,serif', INK_2, .72,
                     ls=1.0, italic=True))

    yy = y + 134
    for line in notes:
        body.append(circ(x + 6, yy - 9, 3.4, 0, LAV_D, .85, fill=LAV_D))
        body.append(text(x + 28, yy, line, 28, 'Georgia,serif', INK, .82))
        yy += 48

    yy += 18
    body.append(stroke('M %.1f %.1f L %.1f %.1f' % (x, yy, x + 440, yy),
                       1.2, INK, .17))
    body.append(text(x, yy + 42, method, 21, 'Georgia,serif', INK_2, .6, ls=1.7))

    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d">%s%s'
            '<g clip-path="url(#page)">%s</g></svg>'
            % (W, H, W, H, defs(), paper(), ''.join(body)))


def drink(glass_fn, garnish_fn=None, lift=0.0):
    """Centre a glass on the left page and draw its garnish in the same space.
       budget is how far either side of the glass the art may reach before it
       runs off the paper, so the recipes can place things safely."""
    g, gh, hw, target = glass_fn()
    s = target / gh
    budget = (LCX - PX - 26) / s
    inner = g + (garnish_fn(gh, hw, budget) if garnish_fn else '')
    return grp(LCX, PCY - (gh * s) / 2 + lift, inner, s)


