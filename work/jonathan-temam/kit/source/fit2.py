"""Fit paths into 256 box (pad 20), centred, true bbox by sampling Béziers."""
import re, sys
from gen import fmt
def bbox(ds):
    xs, ys = [], []
    for d in ds:
        toks = re.findall(r"[MLCZ]|-?\d+(?:\.\d+)?", d); i = 0; cur = None
        while i < len(toks):
            t = toks[i]
            if t == "Z": i += 1; continue
            n = {"M": 1, "L": 1, "C": 3}[t]
            pts = [(float(toks[i+1+2*j]), float(toks[i+2+2*j])) for j in range(n)]; i += 1 + 2*n
            if t == "C":
                for k in range(21):
                    u = k/20; a = [cur] + pts
                    x = sum(c*p[0] for c, p in zip([(1-u)**3, 3*u*(1-u)**2, 3*u*u*(1-u), u**3], a))
                    y = sum(c*p[1] for c, p in zip([(1-u)**3, 3*u*(1-u)**2, 3*u*u*(1-u), u**3], a))
                    xs.append(x); ys.append(y)
            else: xs.append(pts[0][0]); ys.append(pts[0][1])
            cur = pts[-1]
    return min(xs), max(xs), min(ys), max(ys)
if __name__ != '__main__': files = []
else: pad = float(sys.argv[1]); files = sys.argv[2:]
for f in files:
    s = open(f).read(); ds = re.findall(r' d="([^"]+)"', s)
    x0, x1, y0, y1 = bbox(ds); avail = 256 - 2*pad
    k = min(avail/(x1-x0), avail/(y1-y0))
    ox = 128 - (x0+x1)/2*k; oy = 126 - (y0+y1)/2*k
    def tr(d):
        out = []; xy = 0
        for t in re.findall(r"[MLCZ]|-?\d+(?:\.\d+)?", d):
            if t in "MLCZ": out.append(t); continue
            out.append(fmt(float(t)*k + (ox if xy == 0 else oy))); xy ^= 1
        return re.sub(r"([MLCZ]) ", r"\1", " ".join(out))
    for d in ds: s = s.replace(d, tr(d))
    open(f, "w").write(s); print(f, round(k, 3))
