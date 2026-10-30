import sys, cairosvg, numpy as np, io
from PIL import Image
L={}; L['D']=(open('D.txt').read(),0,500)
exec(open('letters.py').read()); exec(open('space.py').read())
OUT=sys.argv[1]; word='DARWI'; xs=layout(L,word,52)
paths=''.join(f'<path transform="translate({x} 0)" d="{" ".join(L[c][0].split())}"/>' for c,x in zip(word,xs))
# tight bbox
probe=f'<svg xmlns="http://www.w3.org/2000/svg" width="3000" height="560" viewBox="0 0 3000 560"><g transform="translate(100 0)">{paths}</g></svg>'
a=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=probe.encode()))))[...,3]>0
ys,xx=np.where(a); x0,x1,y0,y1=xx.min()-100-2,xx.max()-100+2,ys.min()-2,ys.max()+2
vb=f'{x0} {y0} {x1-x0} {y1-y0}'
def svg(fill,title): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}"><title>{title}</title><g fill="{fill}" fill-rule="evenodd">{paths}</g></svg>\n'
for name,fill in [('darwi-logo-noir','#000000'),('darwi-logo-blanc','#FFFFFF')]:
    open(f'{OUT}/{name}.svg','w').write(svg(fill,'DARWI'))
# letters individually
for c in 'ARWI':
    open(f'{OUT}/lettre-{c}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 520"><path fill="#000000" fill-rule="evenodd" d="{" ".join(L[c][0].split())}"/></svg>\n')
cairosvg.svg2png(url=f'{OUT}/darwi-logo-noir.svg',write_to=f'{OUT}/darwi-logo-noir.png',output_width=2400)
cairosvg.svg2png(url=f'{OUT}/darwi-logo-blanc.svg',write_to=f'{OUT}/darwi-logo-blanc.png',output_width=2400)
# preview sheet
W,H=1600,1200; sheet=Image.new('RGB',(W,H),'#fff')
from PIL import ImageDraw
def put(svgfile,w,xy):
    im=Image.open(io.BytesIO(cairosvg.svg2png(url=svgfile,output_width=w))).convert('RGBA'); sheet.paste(im,xy,im); return im.size
ImageDraw.Draw(sheet).rectangle([0,560,W,H],fill='#111111')
put(f'{OUT}/darwi-logo-noir.svg',1300,(150,140))
put(f'{OUT}/darwi-logo-blanc.svg',1000,(300,640))
x=150
for w in (480,240,120,60):
    put(f'{OUT}/darwi-logo-blanc.svg',w,(x,1040)); x+=w+60
sheet.save(f'{OUT}/apercu.png')
print(vb)
