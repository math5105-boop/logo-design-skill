import math, sys
T = math.tan(math.radians(15))   # forward lean, exact 15°
K = 0.5523                        # quarter-circle cubic handle factor
CY = 128

def sh(p):
    x, y = p
    return (x + (CY - y) * T, y)

def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s

class P:
    def __init__(s): s.d = []
    def M(s, x, y): s.d.append(("M", [(x, y)])); return s
    def L(s, x, y): s.d.append(("L", [(x, y)])); return s
    def C(s, a, b, c): s.d.append(("C", [a, b, c])); return s
    def Z(s): s.d.append(("Z", [])); return s
    def quarter(s, cx, cy, r, a0, a1):
        """quarter arc from angle a0 to a1 (degrees, y down), |a1-a0|=90"""
        p0 = (cx + r*math.cos(math.radians(a0)), cy + r*math.sin(math.radians(a0)))
        p1 = (cx + r*math.cos(math.radians(a1)), cy + r*math.sin(math.radians(a1)))
        sgn = 1 if a1 > a0 else -1
        t0 = (-math.sin(math.radians(a0))*sgn, math.cos(math.radians(a0))*sgn)
        t1 = (-math.sin(math.radians(a1))*sgn, math.cos(math.radians(a1))*sgn)
        c0 = (p0[0] + t0[0]*K*r, p0[1] + t0[1]*K*r)
        c1 = (p1[0] - t1[0]*K*r, p1[1] - t1[1]*K*r)
        return s.C(c0, c1, p1)
    def out(s, shear=True):
        f = sh if shear else (lambda p: p)
        parts = []
        for cmd, pts in s.d:
            parts.append(cmd + " ".join(f"{fmt(f(p)[0])} {fmt(f(p)[1])}" for p in pts))
        return " ".join(parts)

def svg(title, paths, vb="0 0 256 256", w=256, h=256):
    body = "\n  ".join(f'<path fill="#111111" fill-rule="evenodd" d="{d}"/>' for d in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="title">\n  <title id="title">{title}</title>\n  {body}\n</svg>\n')

def concept_a():
    """Élan: T and J as one continuous forward-leaning stroke (shared stem)."""
    s = 40
    p = P()
    # crossbar 40..216, stem 128..168, hook outer r=72 centre (96,168), inner r=32
    p.M(40, 32).L(216, 32).L(216, 72).L(168, 72).L(168, 168)
    p.quarter(96, 168, 72, 0, 90).quarter(96, 168, 72, 90, 180)
    p.L(24, 152).L(64, 152).L(64, 168)
    p.quarter(96, 168, 32, 180, 90).quarter(96, 168, 32, 90, 0)
    p.L(128, 72).L(40, 72).Z()
    return [p.out()]

def concept_b():
    """Appui: the J wraps and carries the T inside one forward block."""
    p = P()
    # T: crossbar 32..224 x 24..68 ; stem 112..156 x 68..172
    p.M(32, 24).L(224, 24).L(224, 68).L(156, 68).L(156, 172).L(112, 172).L(112, 68).L(32, 68).Z()
    # J: stem 180..224 from 84 down; bottom hook to x 32, rising terminal 32..76 to y 140; outer radius 44 corners
    r = 44
    q = P()
    q.M(180, 84).L(224, 84).L(224, 232 - r)
    q.quarter(224 - r, 232 - r, r, 0, 90)
    q.L(32 + r, 232)
    q.quarter(32 + r, 232 - r, r, 90, 180)
    q.L(32, 140).L(76, 140).L(76, 188).L(180, 188).Z()
    return [p.out(), q.out()]

def concept_c():
    """Lancer: the T's crossbar is a launch; the stem drops and hooks in one sweep, crossbar detached ahead."""
    p = P()
    # crossbar split: left short block + long right bar with gap (start-line); stem/J shared
    p.M(24, 32).L(80, 32).L(80, 72).L(24, 72).Z()
    p.M(96, 32).L(232, 32).L(232, 72).L(96, 72).Z()
    q = P()
    q.M(128, 88).L(168, 88).L(168, 168)
    q.quarter(96, 168, 72, 0, 90).quarter(96, 168, 72, 90, 180)
    q.L(24, 136).L(64, 136).L(64, 168)
    q.quarter(96, 168, 32, 180, 90).quarter(96, 168, 32, 90, 0)
    q.L(128, 88).Z()
    return [p.out(), q.out()]

if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else "v1"
    for name, fn, t in [("a", concept_a, "Élan"), ("b", concept_b, "Appui"), ("c", concept_c, "Lancer")]:
        open(f"concept-{name}-{v}.svg", "w").write(svg(f"Jonathan Temam — {t}", fn()))
