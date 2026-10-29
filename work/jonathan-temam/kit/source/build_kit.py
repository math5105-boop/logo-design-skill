"""Build the Jonathan Temam 'Lame' kit masters."""
import os, re, math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from gen import P, sh, fmt, T
from fit2 import bbox

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "masters")
os.makedirs(OUT, exist_ok=True)
ORANGE, INK, WHITE = "#FA4616", "#101820", "#FFFFFF"
FONTS = "/usr/share/fonts/opentype/inter/"

def lame(inner_c=42, inner_r=42):
    """J stem rolls into the blade crossbar; T stem cut at 45°; J hook tapers (inner arc sets the tip)."""
    p = P(); r = 44
    p.M(84, 32 + r)
    p.quarter(84 + r, 32 + r, r, 180, 270)
    p.L(248, 32).L(204, 76).L(196, 76)
    p.L(196, 168).L(152, 212).L(152, 76)
    p.L(128, 76).L(128, 168)
    p.quarter(64, 168, 64, 0, 90).quarter(64, 168, 64, 90, 180)
    if inner_c - inner_r > 0:                 # small-size cut: blunt tip of width inner_c - inner_r
        p.L(inner_c - inner_r, 168)
    p.quarter(inner_c, 168, inner_r, 180, 90).quarter(inner_c, 168, inner_r, 90, 0)
    return p.Z().out()

def transform_d(d, k, ox, oy):
    out = []; xy = 0
    for t in re.findall(r"[MLCQZ]|-?\d+(?:\.\d+)?", d):
        if t in "MLCQZ": out.append(t); continue
        out.append(fmt(float(t) * k + (ox if xy == 0 else oy))); xy ^= 1
    return re.sub(r"([MLCQZ]) ", r"\1", " ".join(out))

def place(d, x, y, h):
    """scale path so its height is h, top-left of bbox at (x, y); returns (d, width)"""
    x0, x1, y0, y1 = bbox([d]); k = h / (y1 - y0)
    return transform_d(d, k, x - x0 * k, y - y0 * k), (x1 - x0) * k

import uharfbuzz as hb

class Text:
    def __init__(self, font):
        blob = hb.Blob.from_file_path(FONTS + font); self.hbfont = hb.Font(hb.Face(blob))
        self.f = TTFont(FONTS + font); self.cmap = self.f.getBestCmap(); self.gs = self.f.getGlyphSet()
        self.upm = self.f["head"].unitsPerEm; self.cap = self.f["OS/2"].sCapHeight
    def shape(self, text):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True})
        order = self.f.getGlyphOrder()
        return [(order[i.codepoint], p.x_advance, p.x_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]
    def width(self, text, size, track):
        s = size / self.upm
        return sum(adv * s + track for _, adv, _ in self.shape(text)) - track
    def path(self, text, size, x, baseline, track=0, slant=True):
        s = size / self.upm; pen = SVGPathPen(self.gs); cx = x
        for g, adv, off in self.shape(text):
            tp = TransformPen(pen, (s, 0, s * T if slant else 0, -s, cx + off * s, baseline))
            self.gs[g].draw(tp); cx += adv * s + track
        return pen.getCommands()

NAME = Text("InterDisplay-Black.otf"); DESC = Text("InterDisplay-SemiBold.otf")

def svg(title, vb, paths):
    w, h = vb[2], vb[3]
    body = "\n  ".join(f'<path id="{i}" fill="{c}" fill-rule="evenodd" d="{d}"/>' for i, c, d in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(fmt(v) for v in vb)}" width="{fmt(w)}" '
            f'height="{fmt(h)}" role="img" aria-labelledby="title">\n  <title id="title">{title}</title>\n  {body}\n</svg>\n')

def write(name, title, vb, paths):
    open(f"{OUT}/{name}.svg", "w").write(svg(title, vb, paths))

def symbol_box(d, pad=18):
    x0, x1, y0, y1 = bbox([d]); k = min((256 - 2*pad) / (x1 - x0), (256 - 2*pad) / (y1 - y0))
    return transform_d(d, k, 128 - (x0 + x1) / 2 * k, 126 - (y0 + y1) / 2 * k)

def badge():
    t = P(); R = 44; x0, y0, x1, y1 = -28, -12, 276, 252
    t.M(x0 + R, y0).L(x1 - R, y0); t.quarter(x1 - R, y0 + R, R, 270, 360)
    t.L(x1, y1 - R); t.quarter(x1 - R, y1 - R, R, 0, 90)
    t.L(x0 + R, y1); t.quarter(x0 + R, y1 - R, R, 90, 180)
    t.L(x0, y0 + R); t.quarter(x0 + R, y0 + R, R, 180, 270); t.Z()
    return symbol_box(t.out() + " " + lame(), 16)

SYM = lame(); SMALL = lame(50, 34)
TITLE = "Jonathan Temam — coach sportif"

# --- symbol masters (256 square) ---
for nm, d in [("jt-symbol", SYM), ("jt-symbol-small", SMALL)]:
    sd = symbol_box(d)
    write(f"{nm}-color", TITLE, (0, 0, 256, 256), [("symbol", ORANGE, sd)])
    write(f"{nm}-black", TITLE, (0, 0, 256, 256), [("symbol", "#000000", sd)])
write("jt-badge-color", TITLE, (0, 0, 256, 256), [("badge", ORANGE, badge())])
write("jt-badge-dark", TITLE, (0, 0, 256, 256), [("badge", INK, badge())])

# --- lockups ---
def horizontal(name_c, sym_c, desc_c, suffix):
    H = 256; sh_ = 176; sy = (H - sh_) / 2
    sd, sw = place(SYM, 24, sy, sh_)
    unit = 44 * sh_ / 192                      # J stem width at this size (≈ clear-space unit)
    nx = 24 + sw + unit * 1.1
    size = 92; cap = NAME.cap * size / NAME.upm
    dsize = 36; dcap = DESC.cap * dsize / DESC.upm; gap = 26
    top = (H - (cap + gap + dcap)) / 2
    nd = NAME.path("JONATHAN TEMAM", size, nx, top + cap, track=2)
    dd = DESC.path("COACH SPORTIF", dsize, nx + 4, top + cap + gap + dcap, track=14)
    w = nx + max(NAME.width("JONATHAN TEMAM", size, 2) + cap * T, DESC.width("COACH SPORTIF", dsize, 14) + 4) + 24
    write(f"jt-horizontal-{suffix}", TITLE, (0, 0, w, H),
          [("symbol", sym_c, sd), ("name", name_c, nd), ("descriptor", desc_c, dd)])
    return w

def stacked(name_c, sym_c, desc_c, suffix):
    size = 92; cap = NAME.cap * size / NAME.upm; nw = NAME.width("JONATHAN TEMAM", size, 2) + cap * T
    dsize = 36; dcap = DESC.cap * dsize / DESC.upm; dw = DESC.width("COACH SPORTIF", dsize, 14) + dcap * T
    W = nw + 64; sh_ = 220
    x0, x1, y0, y1 = bbox([SYM]); sw = (x1 - x0) * sh_ / (y1 - y0)
    sd, _ = place(SYM, (W - sw) / 2, 32, sh_)
    ny = 32 + sh_ + 56 + cap
    nd = NAME.path("JONATHAN TEMAM", size, (W - nw) / 2, ny, track=2)
    dd = DESC.path("COACH SPORTIF", dsize, (W - dw) / 2, ny + 26 + dcap, track=14)
    write(f"jt-stacked-{suffix}", TITLE, (0, 0, W, ny + 26 + dcap + 32),
          [("symbol", sym_c, sd), ("name", name_c, nd), ("descriptor", desc_c, dd)])

def wordmark(c, suffix):
    size = 92; cap = NAME.cap * size / NAME.upm; nw = NAME.width("JONATHAN TEMAM", size, 2) + cap * T
    nd = NAME.path("JONATHAN TEMAM", size, 16, 16 + cap, track=2)
    write(f"jt-wordmark-{suffix}", TITLE, (0, 0, nw + 32, cap + 32), [("name", c, nd)])

for suffix, (n, s, d) in {"color": (INK, ORANGE, INK), "reversed": (WHITE, ORANGE, WHITE),
                          "black": ("#000000",) * 3, "white": (WHITE,) * 3, "orange": (ORANGE,) * 3}.items():
    horizontal(n, s, d, suffix); stacked(n, s, d, suffix)
wordmark(INK, "color"); wordmark(WHITE, "white")
print("ok")
