import sys, cairosvg, re
W=sys.argv[1] if len(sys.argv)>1 else 'v1'
D=open('D.txt').read()
L={}
L['D']=(D,0,500)
L['I']=("""M85 18 C98 44 118 62 150 68 C176 72 196 72 203 80 C209 120 208 200 202 252
C194 330 160 402 37 476 C96 410 126 330 129 258 C131 200 120 160 104 125 C90 92 78 50 85 18 Z""",0,230)
exec(open('letters.py').read())
exec(open('space.py').read())
TARGET=int(sys.argv[3]) if len(sys.argv)>3 else 40
def svg(word):
    xs=layout(L,word,TARGET); parts=[f'<path transform="translate({x},0)" d="{L[c][0]}"/>' for c,x in zip(word,xs)]
    w=xs[-1]+L[word[-1]][2]
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w+80} 560"><rect width="100%" height="100%" fill="#fff"/><g transform="translate(40,0)" fill="#111" fill-rule="evenodd">{"".join(parts)}</g></svg>'
s=svg(sys.argv[2] if len(sys.argv)>2 else 'DARWI')
open(f'{W}.svg','w').write(s); cairosvg.svg2png(bytestring=s.encode(),write_to=f'{W}.png',output_height=400)
