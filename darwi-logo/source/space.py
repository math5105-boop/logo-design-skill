import cairosvg, io, numpy as np
from PIL import Image
def mask(p):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="700" height="560" viewBox="0 0 700 560"><rect width="700" height="560" fill="#fff"/><path fill-rule="evenodd" d="{p}"/></svg>'
    return np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert('L'))<128
def layout(L, word, target=40, band=(110,450)):
    xs=[0]; ms=[mask(L[c][0]) for c in word]
    for i in range(1,len(word)):
        a,b=ms[i-1],ms[i]; best=None
        for y in range(*band):
            ra=np.where(a[y])[0]; rb=np.where(b[y])[0]
            if len(ra) and len(rb):
                g=rb.min()-ra.max()   # gap if same origin
                best=g if best is None else min(best,g)
        xs.append(xs[-1]-best+target)
    return xs
