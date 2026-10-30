import sys, numpy as np, potrace
from PIL import Image, ImageFilter
im=Image.open(sys.argv[1]).convert('RGBA')
bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
g=bg.convert('L').resize((2048,2048),Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))
a=np.array(g)<128
ys,xs=np.where(a); print('bbox',xs.min()/4,ys.min()/4,xs.max()/4,ys.max()/4, file=sys.stderr)
plist=potrace.Bitmap(a).trace(turdsize=50, alphamax=1.1, opticurve=True, opttolerance=0.4)
s=0.25
f=lambda p:f"{p.x*s:.1f} {p.y*s:.1f}"
d=[]
for c in plist:
    d.append("M"+f(c.start_point))
    for seg in c.segments:
        if seg.is_corner: d.append("L"+f(seg.c)+" L"+f(seg.end_point))
        else: d.append("C"+f(seg.c1)+" "+f(seg.c2)+" "+f(seg.end_point))
    d.append("Z")
print(" ".join(d))
