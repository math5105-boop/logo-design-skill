"""Outline text to SVG path data using a (variable) font instance."""
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
F=__import__('os').path.join(__import__('os').path.dirname(__file__), 'fonts') + '/'
FONTS={'archivo':F+'Archivo-Variable.woff2',
       'inter':F+'Inter-{w}.woff2'}
_cache={}
def font(name, wght=700, wdth=125):
    k=(name,wght,wdth)
    if k in _cache: return _cache[k]
    if name=='archivo':
        f=TTFont(FONTS['archivo']); f=instantiateVariableFont(f,{'wght':wght,'wdth':wdth})
    else:
        f=TTFont(FONTS['inter'].format(w=wght))
    _cache[k]=f; return f
def text_path(txt, size, x=0, y=0, tracking=0, **kw):
    """Return (path_d, advance_width). y is baseline. tracking in em/1000."""
    f=font(**kw); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    s=size/upm; pen=SVGPathPen(gs); cx=0.0; names=[cmap[ord(c)] for c in txt]
    # simple kerning via GPOS is skipped; tracking applied uniformly
    for i,n in enumerate(names):
        tp=TransformPen(pen,(s,0,0,-s,x+cx,y)); gs[n].draw(tp)
        cx+=gs[n].width*s + (tracking/1000*size if i<len(names)-1 else 0)
    return pen.getCommands(), cx
def cap_height(size, **kw):
    f=font(**kw); return f['OS/2'].sCapHeight*size/f['head'].unitsPerEm
