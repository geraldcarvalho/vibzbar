#!/usr/bin/env python3
"""
The ornaments the layout hangs off.  Meng To used watercolour botanicals;
VIBZ has its own motif -- the single flowing line from its motion language,
and the topographic wave of its pattern system -- so those are drawn here
instead, in his ink rather than the brand's indigo.

The canvases keep the originals' exact aspect ratios (760x1053, 760x1924,
353x453, 1500x638) because the layout sizes each by width and lets height
follow, so a different ratio silently moves the whole page.
"""
import math, pathlib
import draw as S

OUT = S.OUT
INK, INK_2, EARTH = S.INK, S.INK_2, S.LAV_D


def svg(w, h, body, defs=''):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d"><defs>%s</defs>%s</svg>'
            % (w, h, w, h, defs, body))


def flow(x0, y0, w, h, n=7, phase=0.0, c=INK, o=.5, wid=2.6, amp=.28):
    """a bundle of the brand's flowing line, drawn as contour after contour"""
    out = []
    for i in range(n):
        t = i / float(n - 1) if n > 1 else 0
        off = (t - .5) * h * .9
        a = h * amp * (1 - abs(t - .5) * .7)
        d = 'M %.1f %.1f' % (x0, y0 + off)
        seg = w / 3.0
        for k in range(3):
            sx = x0 + seg * k
            sgn = 1 if (k + i + phase) % 2 < 1 else -1
            d += (' C %.1f %.1f %.1f %.1f %.1f %.1f'
                  % (sx + seg * .32, y0 + off - a * sgn,
                     sx + seg * .68, y0 + off + a * sgn,
                     sx + seg, y0 + off))
        out.append(S.stroke(d, wid * (1 - t * .3), c, o * (1 - abs(t - .5) * .8)))
    return ''.join(out)


def botany_left():
    """the line rising out of the bottom-left corner"""
    b = [flow(-140, 700, 900, 520, 9, 0, INK, .55, 3.0, .22),
         flow(-90, 940, 760, 300, 6, 1, EARTH, .40, 2.4, .26)]
    return svg(760, 1053, ''.join(b))


def botany_right():
    """a taller fall of the same line down the right edge"""
    b = [flow(-120, 1180, 900, 900, 10, 1, INK, .50, 3.2, .20),
         flow(-60, 1620, 820, 420, 6, 0, EARTH, .36, 2.4, .24)]
    return svg(760, 1924, ''.join(b))


def divider():
    """A hairline with the brand's wave at its centre.  The layout draws this
       at `100% auto` inside a ~46px strip, so only a thin band across the
       middle is ever seen -- everything must live in that band."""
    W, H = 1500, 638
    cy = H / 2
    b = []
    for sgn in (-1, 1):
        b.append(S.stroke('M %.1f %.1f L %.1f %.1f'
                          % (750 + sgn * 130, cy, 750 + sgn * 600, cy), 2.2, INK, .45))
        b.append(S.circ(750 + sgn * 640, cy, 4.5, 0, EARTH, .7, fill=EARTH))
    b.append(flow(620, cy, 260, 70, 3, 0, INK, .85, 2.8, .34))
    return svg(W, H, ''.join(b))


def bloom():
    """a coupe and the line it sits on, beside the About copy"""
    g, gh, hw, _ = S.g_coupe()
    b = [flow(-40, 250, 430, 300, 7, 0, EARTH, .30, 2.4, .26),
         S.grp(176, 96, g, 1.28),
         S.stroke('M 40 402 L 312 402', 1.6, INK, .25)]
    return svg(353, 453, ''.join(b))


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (('botany-left', botany_left), ('botany-right', botany_right),
                     ('divider', divider), ('bloom', bloom)):
        p = OUT / ('%s.svg' % name)
        p.write_text(fn(), encoding='utf-8')
        print('%-18s %6.1f KB' % (p.name, p.stat().st_size / 1024))
