"""Build the Jonathan Temam logo masters (symbol, lockups, wordmark) as outlined SVG.

Geometry of the symbol is a clean vector reconstruction of the client's approved mark.
Type is outlined from Archivo (OFL) so no font is needed to display the files.
"""
import os, sys
sys.path.insert(0, os.environ.get('TEXTPATH_DIR', '.'))
from textpath import text_path, cap_height

OUT = os.path.join(os.path.dirname(__file__), '..', 'logo', 'svg')
os.makedirs(OUT, exist_ok=True)

COL = {'noir': '#111214', 'blanc': '#FFFFFF', 'orange': '#FA4616', 'craie': '#F3F1EC'}

# Symbol: two closed polygons on an 837 × 412 box (T-blade + J)
BLADE = [(837, 0), (0, 228), (641, 103.4), (558.6, 163.3), (485, 321)]
J = [(492, 176), (293, 214.7), (409, 228), (372.2, 307), (141, 412), (405.9, 360.5)]
# Small-size cut: shorter, thicker tips so the idea survives 16–32 px
BLADE_S = [(837, 0), (167, 182.4), (641, 103.4), (558.6, 163.3), (485, 321)]
J_S = [(492, 176), (293, 214.7), (409, 228), (372.2, 307), (194, 401.7), (405.9, 360.5)]
SW, SH = 837, 412


def poly(pts, dx=0, dy=0, k=1.0):
    return 'M' + ' L'.join(f'{dx + x * k:.2f} {dy + y * k:.2f}' for x, y in pts) + ' Z'


def symbol_d(dx=0, dy=0, k=1.0, small=False):
    a, b = (BLADE_S, J_S) if small else (BLADE, J)
    return poly(a, dx, dy, k) + ' ' + poly(b, dx, dy, k)


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}"><title>{title}</title>{body}</svg>\n')


def save(name, w, h, body, title):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(svg(w, h, body, title))


# Wordmark settings
WM = dict(name='archivo', wght=700, wdth=125)
WM_TRACK = 40          # em/1000
DS = dict(name='archivo', wght=500, wdth=125)
DS_TRACK = 340


def wordmark(cap, x, y_base):
    size = cap / cap_height(100, **WM) * 100
    return text_path('JONATHAN TEMAM', size, x, y_base, tracking=WM_TRACK, **WM)


def descriptor(cap, x, y_base, target_w=None, centre=False):
    size = cap / cap_height(100, **DS) * 100
    txt = 'COACH SPORTIF'
    _, w = text_path(txt, size, 0, 0, tracking=DS_TRACK, **DS)
    if centre and target_w:
        x += (target_w - w) / 2
    return text_path(txt, size, x, y_base, tracking=DS_TRACK, **DS)


def build(colours):
    sym_c, txt_c, suffix = colours
    t = 'Jonathan Temam'
    # 1. Symbol
    save(f'jt-symbole-{suffix}.svg', SW, SH, f'<path fill="{sym_c}" d="{symbol_d()}"/>', f'{t} — symbole')
    # 2. Horizontal lockup: symbol height 412, wordmark cap = 0.22 × symbol height
    cap = 0.22 * SH
    gap = 0.30 * SH
    x0 = SW + gap
    _, wm_w = wordmark(cap, 0, 0)
    dcap = cap * 0.40
    lead = cap * 0.55
    block = cap + lead + dcap
    top = (SH - block) / 2 + 0.03 * SH          # optical: the mark's mass sits low
    d1, _ = wordmark(cap, x0, top + cap)
    d2, _ = descriptor(dcap, x0, top + cap + lead + dcap, target_w=wm_w)
    W = x0 + wm_w
    save(f'jt-horizontal-{suffix}.svg', W, SH,
         f'<path fill="{sym_c}" d="{symbol_d()}"/><path fill="{txt_c}" d="{d1}"/><path fill="{txt_c}" d="{d2}"/>',
         f'{t} — logo horizontal')
    # 3. Stacked lockup
    k = 1.0
    cap_v = 0.23 * SH
    _, wm_wv = wordmark(cap_v, 0, 0)
    Wv = max(wm_wv, SW)
    sx = (Wv - SW) / 2
    y = SH + 0.30 * SH
    d1, _ = wordmark(cap_v, (Wv - wm_wv) / 2, y + cap_v)
    dcap_v = cap_v * 0.40
    d2, _ = descriptor(dcap_v, (Wv - wm_wv) / 2, y + cap_v + cap_v * 0.55 + dcap_v, target_w=wm_wv, centre=True)
    Hv = y + cap_v + cap_v * 0.55 + dcap_v
    save(f'jt-vertical-{suffix}.svg', Wv, Hv,
         f'<path fill="{sym_c}" d="{symbol_d(sx, 0, k)}"/><path fill="{txt_c}" d="{d1}"/><path fill="{txt_c}" d="{d2}"/>',
         f'{t} — logo vertical')
    # 4. Wordmark only
    capw = 100
    d1, ww = wordmark(capw, 0, capw)
    dcw = capw * 0.40
    d2, _ = descriptor(dcw, 0, capw + capw * 0.55 + dcw, target_w=ww)
    save(f'jt-logotype-{suffix}.svg', ww, capw + capw * 0.55 + dcw,
         f'<path fill="{txt_c}" d="{d1}"/><path fill="{txt_c}" d="{d2}"/>', f'{t} — logotype')


build((COL['noir'], COL['noir'], 'noir'))
build((COL['blanc'], COL['blanc'], 'blanc'))
build((COL['orange'], COL['noir'], 'accent-clair'))
build((COL['orange'], COL['blanc'], 'accent-sombre'))
# Symbol in Orange Impulsion, and the small-size cut
save('jt-symbole-orange.svg', SW, SH, f'<path fill="{COL["orange"]}" d="{symbol_d()}"/>', 'Jonathan Temam — symbole')
save('jt-symbole-petite-taille.svg', SW, SH, f'<path fill="{COL["noir"]}" d="{symbol_d(small=True)}"/>',
     'Jonathan Temam — symbole petite taille')
# Square avatar / app master: symbol on a Noir Carbone tile
T = 1024
k = 0.86 * T / SW
dx, dy = (T - SW * k) / 2, (T - SH * k) / 2 - 0.01 * T
save('jt-avatar-noir.svg', T, T, f'<rect width="{T}" height="{T}" fill="{COL["noir"]}"/>'
     f'<path fill="#FFFFFF" d="{symbol_d(dx, dy, k)}"/>', 'Jonathan Temam — avatar')
save('jt-avatar-orange.svg', T, T, f'<rect width="{T}" height="{T}" fill="{COL["orange"]}"/>'
     f'<path fill="{COL["noir"]}" d="{symbol_d(dx, dy, k)}"/>', 'Jonathan Temam — avatar')
print('ok', sorted(os.listdir(OUT)))
