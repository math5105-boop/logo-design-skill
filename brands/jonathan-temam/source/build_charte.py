"""Build the Jonathan Temam brand guidelines (charte graphique) as HTML, then PDF + page previews.

Usage: python3 build_charte.py            -> charte.html, ../Jonathan-Temam_Charte-graphique.pdf, ../apercus/*.png
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOGO = '../logo/svg/'

C = dict(noir='#111214', craie='#F3F1EC', orange='#FA4616', graphite='#2A2C30', acier='#888B8D', blanc='#FFFFFF')
BLADE = [(837, 0), (0, 228), (641, 103.4), (558.6, 163.3), (485, 321)]
J = [(492, 176), (293, 214.7), (409, 228), (372.2, 307), (141, 412), (405.9, 360.5)]


def poly(pts):
    return 'M' + ' L'.join(f'{x:g} {y:g}' for x, y in pts) + ' Z'


SYM_D = poly(BLADE) + ' ' + poly(J)


def sym(cls='', style='', color='currentColor'):
    """Inline symbol (837 × 412)."""
    return (f'<svg class="sym {cls}" style="{style}" viewBox="0 0 837 412" aria-hidden="true">'
            f'<path fill="{color}" d="{SYM_D}"/></svg>')


def needle(w=220, h=10, color='currentColor', cls='trait', flip=False):
    """'Le Trait': the tapering blade of the symbol used as a graphic device."""
    d = f'M0 {h} L{w} 0 L{w * 0.985:.1f} {h} Z' if not flip else f'M{w} {h} L0 0 L{w * 0.015:.1f} {h} Z'
    return f'<svg class="{cls}" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path fill="{color}" d="{d}"/></svg>'


def pattern_svg(w, h, color, bg='none', opacity=1.0, scale=1.0, uid='p'):
    """'Sillage' pattern: staggered needles at the brand angle (15°)."""
    pw, ph = 180 * scale, 48 * scale
    n1 = f'M0 {14*scale:.1f} L{120*scale:.1f} {-18*scale:.1f} L{112*scale:.1f} {2*scale:.1f} Z'
    n2 = f'M{90*scale:.1f} {38*scale:.1f} L{210*scale:.1f} {6*scale:.1f} L{202*scale:.1f} {26*scale:.1f} Z'
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">'
            f'<defs><pattern id="{uid}" width="{pw:.1f}" height="{ph:.1f}" patternUnits="userSpaceOnUse">'
            f'<path d="{n1}" fill="{color}"/><path d="{n2}" fill="{color}"/>'
            f'<path d="M{-90*scale:.1f} {38*scale:.1f} L{30*scale:.1f} {6*scale:.1f} L{22*scale:.1f} {26*scale:.1f} Z" fill="{color}"/>'
            f'<path d="M{180*scale:.1f} {14*scale:.1f} L{300*scale:.1f} {-18*scale:.1f} L{292*scale:.1f} {2*scale:.1f} Z" fill="{color}"/>'
            f'</pattern></defs>'
            f'<rect width="100%" height="100%" fill="{bg}"/>'
            f'<rect width="100%" height="100%" fill="url(#{uid})" opacity="{opacity}"/></svg>')


ICONS = {
    'Force': '<path d="M6 18v12M11 13v22M37 13v22M42 18v12M11 24h26"/>',
    'Cardio': '<path d="M4 27h10l4-11 6 21 5-15 3 5h12"/>',
    'Chrono': '<circle cx="24" cy="27" r="15"/><path d="M24 27l7-7M19 5h10M24 5v7"/>',
    'Objectif': '<circle cx="22" cy="26" r="16"/><circle cx="22" cy="26" r="8"/><path d="M22 26L42 8M35 7h8v8"/>',
    'Planning': '<path d="M6 11h36v31H6zM6 19h36M15 6v9M33 6v9M17 30l5 5 9-10"/>',
    'Progression': '<path d="M5 42h9v-8h9v-8h9v-8h11M34 8h9v9M43 8L28 23"/>',
    'Nutrition': '<path d="M24 15c-9-6-18 0-17 11 1 10 8 17 17 15 9 2 16-5 17-15 1-11-8-17-17-11zM24 15c0-5 3-8 7-10"/>',
    'Visio': '<path d="M8 9h32v23H8zM3 39h42M20 16l9 5-9 5z"/>',
}


def icon(name, size=48, color='currentColor', sw=3):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="square" stroke-linejoin="miter">{ICONS[name]}</svg>')


# ---------------------------------------------------------------- page scaffolding
PAGES = []


def page(body, cls='', title=None, num=True, dark=False):
    PAGES.append((body, cls, title, num, dark))


def head(kicker, title, intro=''):
    return (f'<div class="head"><div class="kicker">{kicker}</div><h2>{title}</h2>'
            + (f'<p class="intro">{intro}</p>' if intro else '') + '</div>')


def divider(n, title, sub, items):
    lis = ''.join(f'<li>{i}</li>' for i in items)
    page(f'''
<div class="div-pattern">{pattern_svg(1123, 794, '#ffffff', opacity=0.05, uid='dp'+n)}</div>
<div class="div-num">{n}</div>
<div class="div-body"><h1>{title}</h1><p>{sub}</p><ul>{lis}</ul></div>
{sym('div-sym', color=C['orange'])}
''', cls='divider', dark=True)


# ================================================================= 01 COVER
page(f'''
<div class="cover-pattern">{pattern_svg(1123, 794, '#ffffff', opacity=0.045, uid='cp')}</div>
<div class="cover-top"><img src="{LOGO}jt-logotype-blanc.svg" style="height:34px"></div>
{sym('cover-sym', color=C['blanc'])}
<div class="cover-bottom">
  <div class="kicker orange">Identité visuelle · Version 1.0</div>
  <h1>Charte<br>graphique</h1>
  {needle(420, 12, C['orange'])}
  <div class="cover-meta"><span>Octobre 2026</span><span>Document de référence — usage interne &amp; prestataires</span></div>
</div>
''', cls='cover', num=False, dark=True)

# ================================================================= SOMMAIRE
toc = [('01', 'Plateforme de marque', 'Mission, valeurs, personnalité, ton', 4),
       ('02', 'Logo', 'Concept, construction, versions, règles', 8),
       ('03', 'Couleurs', 'Palette, codes, proportions, contrastes', 16),
       ('04', 'Typographie', 'Familles, hiérarchie, usages', 19),
       ('05', 'Éléments graphiques', 'Angle, trait, motif, pictos, photo', 22),
       ('06', 'Applications', 'Papeterie, social, textile, web, motion', 27),
       ('07', 'Fichiers & contacts', 'Livrables et nomenclature', 34)]
rows = ''.join(f'<div class="toc-row"><span class="toc-n">{n}</span><span class="toc-t">{t}</span>'
               f'<span class="toc-s">{s}</span><span class="toc-p">p. {p:02d}</span></div>' for n, t, s, p in toc)
page(f'''
<div class="toc-wrap">
  <div class="toc-left">
    <div class="kicker">Sommaire</div>
    <h2>Tout ce qu'il faut pour faire vivre la marque.</h2>
    {needle(260, 9, C['orange'])}
  </div>
  <div class="toc-list">{rows}</div>
</div>''', title='Sommaire')

# ================================================================= INTRO
page(f'''
<div class="two-col">
  <div>
    {head('Introduction', 'Une identité taillée<br>pour avancer.')}
    <p class="lead">Ce document rassemble les règles qui font vivre l'identité visuelle de <b>Jonathan Temam, coach sportif</b>.
    Il s'adresse à toutes les personnes qui produisent un support pour la marque : Jonathan lui-même, graphistes,
    imprimeurs, brodeurs, développeurs web, partenaires et salles.</p>
    <p>Une marque forte ne naît pas d'un logo seul, mais de la <b>répétition cohérente</b> des mêmes signes : un symbole,
    deux couleurs fortes, deux typographies, un angle. Chaque post, chaque t-shirt, chaque carte de visite construit la
    même image — et la rend plus reconnaissable que la précédente.</p>
    <p>Les règles sont pensées pour être simples à appliquer, y compris dans Canva. En cas de doute,
    privilégiez toujours la version la plus sobre : noir, blanc, et beaucoup d'espace.</p>
  </div>
  <div class="intro-card">
    <div class="kicker">Comment utiliser ce guide</div>
    <ol class="steps">
      <li><b>Comprendre</b><span>La plateforme de marque (01) explique ce que la marque dit et comment elle le dit.</span></li>
      <li><b>Choisir le bon fichier</b><span>Le logo (02) et la liste des fichiers (07) indiquent quelle version utiliser, où.</span></li>
      <li><b>Composer</b><span>Couleurs (03), typographie (04) et éléments graphiques (05) forment la boîte à outils.</span></li>
      <li><b>S'inspirer</b><span>Les applications (06) montrent le système en situation réelle.</span></li>
    </ol>
  </div>
</div>
<div class="kit-band">
  <div><b>1</b><span>symbole</span></div><div><b>4</b><span>versions du logo</span></div>
  <div><b>5</b><span>couleurs</span></div><div><b>2</b><span>typographies</span></div><div><b>15°</b><span>un angle de marque</span></div>
</div>''', title='Introduction')

# ================================================================= 01 PLATEFORME
divider('01', 'Plateforme<br>de marque', 'Ce que la marque défend, et la manière dont elle s\'exprime.',
        ['Mission, vision, promesse', 'Valeurs', 'Personnalité & ton de voix'])

page(f'''
{head('01 — Plateforme de marque', 'Le cap.')}
<div class="grid3 mt">
  <div class="card"><div class="kicker orange">Mission</div><p class="big-p">Amener chaque personne accompagnée
  au-delà de ce qu'elle pensait possible — avec méthode, exigence et bienveillance.</p></div>
  <div class="card"><div class="kicker orange">Vision</div><p class="big-p">Faire du sport un réflexe durable,
  pas une résolution de janvier. Un coaching qui transforme le corps <i>et</i> les habitudes.</p></div>
  <div class="card"><div class="kicker orange">Promesse</div><p class="big-p">Un cap clair, un suivi précis,
  des progrès mesurables à chaque étape.</p></div>
</div>
<div class="sig-band">
  <div><div class="kicker">Signature de marque</div><div class="signature">Vise plus haut.</div></div>
  <p>Trois mots qui prolongent le symbole : une trajectoire qui monte. Elle s'emploie en fin de message,
  en accroche de campagne ou sous le logo dans les grands formats — jamais modifiée, jamais traduite.</p>
</div>
<div class="grid3 small mt-s">
  <div><div class="kicker">Publics</div><p>Particuliers actifs de 25 à 55 ans (remise en forme, perte de poids, force) ·
  sportifs amateurs préparant un objectif · entreprises et petits groupes.</p></div>
  <div><div class="kicker">Offre</div><p>Coaching individuel · small group training · préparation physique ·
  programmes et suivi à distance.</p></div>
  <div><div class="kicker">Positionnement</div><p>Premium mais accessible : l'exigence d'un préparateur physique,
  la proximité d'un coach personnel.</p></div>
</div>''', title='Plateforme de marque')

vals = [('Exigence', 'Chaque séance a un objectif. Chaque exercice a une raison. Le travail bien fait, sans raccourci.'),
        ('Progression', 'On mesure, on ajuste, on avance. Le progrès se voit, se chiffre et se célèbre.'),
        ('Engagement', 'Présent, ponctuel, impliqué. Le coach s\'engage autant que la personne accompagnée.'),
        ('Proximité', 'Écouter avant de prescrire. Un accompagnement humain, adapté à la vie réelle de chacun.')]
vcards = ''.join(f'<div class="value"><div class="v-n">0{i+1}</div>{needle(120, 6, C["orange"])}'
                 f'<h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(vals))
page(f'''{head('01 — Plateforme de marque', 'Quatre valeurs.', 'Elles guident les décisions — du choix d\'une photo à la manière de répondre à un message.')}
<div class="grid4 mt">{vcards}</div>''', title='Valeurs')

page(f'''{head('01 — Plateforme de marque', 'Personnalité & ton de voix.')}
<div class="two-col mt">
  <div>
    <div class="adj">{''.join(f'<span>{a}</span>' for a in ['Direct', 'Motivant', 'Précis', 'Bienveillant', 'Énergique'])}</div>
    <table class="tone">
      <tr><th>La marque est…</th><th>…mais n'est pas</th></tr>
      <tr><td>Directe</td><td>Brutale</td></tr>
      <tr><td>Motivante</td><td>Culpabilisante</td></tr>
      <tr><td>Exigeante</td><td>Élitiste</td></tr>
      <tr><td>Énergique</td><td>Agitée ou criarde</td></tr>
      <tr><td>Experte</td><td>Jargonneuse</td></tr>
    </table>
  </div>
  <div>
    <div class="kicker">Principes d'écriture</div>
    <ul class="rules">
      <li>Phrases courtes. Verbes d'action. Un message par publication.</li>
      <li>Des faits concrets plutôt que des superlatifs : séries, semaines, kilos, minutes.</li>
      <li>Tutoiement sur les réseaux sociaux ; vouvoiement pour les entreprises et les devis.</li>
      <li>Un emoji maximum par message, jamais dans un titre.</li>
    </ul>
    <div class="say do"><b>✓ À dire</b>« Trois séances par semaine, douze semaines, un objectif. On commence lundi ? »</div>
    <div class="say dont"><b>✕ À éviter</b>« NO PAIN NO GAIN !!! 💪🔥🔥 Deviens une machine »</div>
  </div>
</div>
<div class="channels">
  <div><div class="kicker">Instagram</div><p>« 4 semaines de travail, +20 kg au squat. Fier de toi, Karim. Prochaine étape : 100 kg. »</p></div>
  <div><div class="kicker">Message client</div><p>« Séance de demain décalée à 18 h. On garde le même programme, prévois de l'eau. »</p></div>
  <div><div class="kicker">Entreprise</div><p>« Nous proposons un programme de 8 semaines pour vos équipes, adapté à tous les niveaux. »</p></div>
</div>''', title='Personnalité & ton')

# ================================================================= 02 LOGO
divider('02', 'Logo', 'Le symbole, ses versions et les règles qui le protègent.',
        ['Concept', 'Construction', 'Versions', 'Zone de protection & tailles', 'Couleurs & fonds', 'Interdits'])

# concept page with 3 readings
def reading(highlight):
    if highlight == 'jt':
        return (f'<svg viewBox="-20 -20 877 452"><path fill="{C["noir"]}" d="{poly(BLADE)}"/>'
                f'<path fill="{C["orange"]}" d="{poly(J)}"/></svg>')
    if highlight == 't':
        return (f'<svg viewBox="-20 -20 877 452"><path fill="{C["orange"]}" d="{poly(BLADE)}"/>'
                f'<path fill="{C["noir"]}" d="{poly(J)}"/></svg>')
    return (f'<svg viewBox="-20 -100 877 532"><path fill="{C["noir"]}" d="{SYM_D}"/>'
            f'<path d="M0 140 L700 -47" stroke="{C["orange"]}" stroke-width="12" stroke-dasharray="6 26"/>'
            f'<path d="M800 -74 L690 -80 L716 -16 Z" fill="{C["orange"]}"/></svg>')


page(f'''
<div class="concept">
  <div class="concept-hero">{sym('', color=C['noir'])}</div>
  <div class="concept-text">
    {head('02 — Logo', 'Un monogramme<br>en mouvement.')}
    <p class="lead">Les initiales <b>J</b> et <b>T</b> sont dessinées comme deux lames qui s'élancent vers le haut à droite.
    Le symbole se lit d'un coup d'œil : un nom, une direction, une énergie.</p>
  </div>
</div>
<div class="grid3 readings">
  <div>{reading('t')}<h3>Le T</h3><p>La longue barre et la lame descendante forment le T de Temam — une lettre devenue trajectoire.</p></div>
  <div>{reading('jt')}<h3>Le J</h3><p>Le J de Jonathan s'emboîte sous le T, en contre-forme : deux initiales, un seul geste.</p></div>
  <div>{reading('arrow')}<h3>L'élan</h3><p>L'ensemble monte à 15° et pointe vers l'avant : la progression, la vitesse, l'objectif.</p></div>
</div>''', title='Concept')

# construction page
def ext(p, q, a=-0.25, b=1.25):
    (x1, y1), (x2, y2) = p, q
    return (x1 + (x2 - x1) * a, y1 + (y2 - y1) * a, x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)


lines = [((0, 228), (837, 0), '15°', C['orange']),
         ((0, 228), (641, 103.4), '11°', '#3D7BFF'),
         ((293, 214.7), (492, 176), '11°', '#3D7BFF'),
         ((141, 412), (405.9, 360.5), '11°', '#3D7BFF'),
         ((558.6, 163.3), (485, 321), '65°', '#18A058'),
         ((492, 176), (405.9, 360.5), '65°', '#18A058'),
         ((409, 228), (372.2, 307), '65°', '#18A058'),
         ((837, 0), (485, 321), '42°', '#8A8F98')]
ls = ''.join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"/>' % (*ext(p, q), c)
             for p, q, _, c in lines)
grid = ''.join(f'<line x1="{x}" y1="-80" x2="{x}" y2="492" stroke="#d9d6cf" stroke-width="1"/>' for x in range(0, 838, 93))
grid += ''.join(f'<line x1="-80" y1="{y}" x2="917" y2="{y}" stroke="#d9d6cf" stroke-width="1"/>' for y in range(0, 413, 103))
pts = ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="{C["noir"]}" stroke-width="2.5"/>' for x, y in BLADE + J)
page(f'''
{head('02 — Logo', 'Construction.', 'Le symbole est construit uniquement en lignes droites, sur quatre angles qui se répondent. Ce sont ces angles — et surtout le 15° — qui structurent tout le système graphique.')}
<div class="constr">
  <svg viewBox="-90 -90 1017 592" class="constr-svg">
    {grid}
    <path d="{SYM_D}" fill="{C['noir']}" opacity="0.92"/>
    {ls}{pts}
    <text x="-80" y="470" class="dim">837 × 412 — ratio 2,03 : 1</text>
  </svg>
  <div class="legend">
    <div><i style="background:{C['orange']}"></i><b>15°</b><span>Arête supérieure — l'angle de marque, repris dans les mises en page.</span></div>
    <div><i style="background:#3D7BFF"></i><b>11°</b><span>Parallèles : bas de la barre, haut du crochet et base du J.</span></div>
    <div><i style="background:#18A058"></i><b>65°</b><span>Fûts parallèles du T et du J : le rythme de la lettre.</span></div>
    <div><i style="background:#8A8F98"></i><b>42°</b><span>Lame extérieure : la pointe qui ferme le T.</span></div>
    <p class="note">Formes pleines, sans courbe ni dégradé : le logo se découpe, se brode et se grave sans perte.
    Le symbole ne doit jamais être redessiné — utilisez toujours les fichiers fournis.</p>
  </div>
</div>''', title='Construction')

# versions
page(f'''
{head('02 — Logo', 'Les versions du logo.', 'Quatre versions pour s\'adapter à chaque format. Le symbole et le nom gardent toujours les mêmes proportions entre eux.')}
<div class="versions">
  <div class="v-tile wide"><div class="v-art"><img src="{LOGO}jt-horizontal-noir.svg" style="width:78%"></div>
    <div class="v-cap"><b>Horizontal — version principale</b><span>Site web, en-têtes, signatures, documents, bannières.</span></div></div>
  <div class="v-tile"><div class="v-art"><img src="{LOGO}jt-vertical-noir.svg" style="width:62%"></div>
    <div class="v-cap"><b>Vertical</b><span>Formats carrés ou hauts : textile, affiches, roll-up.</span></div></div>
  <div class="v-tile"><div class="v-art"><img src="{LOGO}jt-symbole-noir.svg" style="width:56%"></div>
    <div class="v-cap"><b>Symbole</b><span>Avatars, icônes, broderie, signature visuelle quand le nom est déjà présent.</span></div></div>
  <div class="v-tile"><div class="v-art"><img src="{LOGO}jt-logotype-noir.svg" style="width:78%"></div>
    <div class="v-cap"><b>Logotype</b><span>Petits espaces horizontaux, mentions, partenariats.</span></div></div>
  <div class="v-tile dark"><div class="v-art"><img src="{LOGO}jt-avatar-noir.svg" style="width:42%;border-radius:50%"></div>
    <div class="v-cap"><b>Avatar</b><span>Photo de profil Instagram, WhatsApp, Google.</span></div></div>
</div>
<p class="foot-note">Le logotype est composé en Archivo Expanded Bold et vectorisé. Ne jamais le retaper au clavier.</p>''',
     title='Versions')

# clear space and min sizes
SH = 412
X = SH / 4
page(f'''
{head('02 — Logo', 'Zone de protection & tailles minimales.')}
<div class="two-col cs">
  <div>
    <div class="cs-art">
      <div class="cs-zone">
        <img src="{LOGO}jt-horizontal-noir.svg">
        <span class="x x-t">X</span><span class="x x-b">X</span><span class="x x-l">X</span><span class="x x-r">X</span>
      </div>
    </div>
    <p><b>X = un quart de la hauteur du symbole.</b> Aucun texte, image ou bord de page ne doit entrer dans cette zone.
    Elle grandit et rétrécit avec le logo : c'est une proportion, jamais une distance fixe.</p>
  </div>
  <div>
    <div class="cs-x">
      <svg viewBox="-40 -10 920 430"><path d="{SYM_D}" fill="{C['noir']}"/>
      {''.join(f'<line x1="-30" x2="880" y1="{X*i:.0f}" y2="{X*i:.0f}" stroke="{C["orange"]}" stroke-width="2" stroke-dasharray="8 8"/>' for i in range(5))}
      <rect x="-36" y="0" width="22" height="{X:.0f}" fill="{C['orange']}"/><text x="-60" y="62" class="xl">X</text></svg>
    </div>
    <table class="spec">
      <tr><th>Version</th><th>Écran</th><th>Impression</th></tr>
      <tr><td>Horizontal</td><td>140 px de large</td><td>35 mm</td></tr>
      <tr><td>Vertical</td><td>90 px de large</td><td>22 mm</td></tr>
      <tr><td>Logotype</td><td>110 px de large</td><td>28 mm</td></tr>
      <tr><td>Symbole</td><td>32 px de large</td><td>8 mm</td></tr>
      <tr><td>Symbole petite taille</td><td>16 – 31 px</td><td>4 – 8 mm · broderie</td></tr>
    </table>
    <p class="note">Sous 32 px, utilisez le fichier <code>jt-symbole-petite-taille</code> : pointes raccourcies et
    épaissies pour rester lisibles (favicon, petites broderies).</p>
  </div>
</div>''', title='Zone de protection')

# colour versions
cv = [('jt-horizontal-noir.svg', C['craie'], 'Noir sur Craie', 'Version principale', ''),
      ('jt-horizontal-blanc.svg', C['noir'], 'Blanc sur Noir', 'Version inversée', ''),
      ('jt-horizontal-accent-sombre.svg', C['noir'], 'Accent sur Noir', 'Symbole Orange Impulsion — signature forte', ''),
      ('jt-horizontal-accent-clair.svg', C['blanc'], 'Accent sur Blanc', 'Symbole orange, nom en noir', ''),
      ('jt-horizontal-noir.svg', C['orange'], 'Noir sur Orange', 'Supports promotionnels', ''),
      ('jt-horizontal-blanc.svg', C['graphite'], 'Blanc sur Graphite', 'Alternative au noir', '')]
tiles = ''.join(f'<div class="cv"><div class="cv-art" style="background:{bg}"><img src="{LOGO}{f}"></div>'
                f'<b>{t}</b><span>{s}</span></div>' for f, bg, t, s, _ in cv)
page(f'''
{head('02 — Logo', 'Versions couleur & fonds autorisés.', 'Le logo vit d\'abord en noir et blanc. L\'Orange Impulsion est réservé au symbole, pour signer avec force.')}
<div class="grid3 cvs">{tiles}</div>
<p class="foot-note">Le blanc sur Orange est déconseillé pour le nom (contraste 3,5:1) : réservez-le au symbole seul en grand format.</p>''',
     title='Versions couleur')

# photos
page(f'''
{head('02 — Logo', 'Logo sur image.', 'Sur une photo, le logo se place toujours sur une zone calme et contrastée. Si aucune zone ne convient, utilisez le cartouche.')}
<div class="grid3 photos">
  <div><div class="ph ph-dark"><img src="{LOGO}jt-horizontal-blanc.svg" class="ph-logo tl"></div>
  <b>✓ Blanc sur zone sombre</b><span>Le cas le plus courant : salles, éclairages latéraux.</span></div>
  <div><div class="ph ph-light"><img src="{LOGO}jt-horizontal-noir.svg" class="ph-logo bl"></div>
  <b>✓ Noir sur zone claire</b><span>Extérieurs, ciels, murs clairs.</span></div>
  <div><div class="ph ph-busy"><div class="cartouche"><img src="{LOGO}jt-symbole-blanc.svg"></div></div>
  <b>✓ Cartouche sur fond chargé</b><span>Carré Noir Carbone, symbole blanc, marge = X.</span></div>
</div>''', title='Logo sur image')

# misuse
def bad(inner, label, bg='#fff'):
    return (f'<div class="bad"><div class="bad-art" style="background:{bg}">{inner}<span class="cross">✕</span></div>'
            f'<span>{label}</span></div>')


hz = f'{LOGO}jt-horizontal-noir.svg'
mis = ''.join([
    bad(f'<img src="{hz}" style="width:72%;transform:scaleX(1.35) scaleY(.75)">', 'Déformer, étirer ou écraser'),
    bad(f'<img src="{hz}" style="width:72%;filter:invert(32%) sepia(90%) saturate(2000%) hue-rotate(200deg)">', 'Changer les couleurs'),
    bad(f'<img src="{hz}" style="width:66%;transform:rotate(-12deg)">', 'Pivoter ou incliner'),
    bad(f'<img src="{hz}" style="width:72%;filter:drop-shadow(6px 6px 3px rgba(0,0,0,.55))">', 'Ajouter ombres ou effets'),
    bad(f'<div style="display:flex;align-items:center;gap:10px;width:80%"><img src="{LOGO}jt-logotype-noir.svg" style="width:62%"><img src="{LOGO}jt-symbole-noir.svg" style="width:34%"></div>', 'Réorganiser les éléments'),
    bad(f'<div style="display:flex;align-items:center;gap:12px;width:80%">{sym("", "width:40%", C["noir"])}<span style="font:italic 700 17px Georgia,serif;color:#111">Jonathan Temam</span></div>', 'Retaper le nom dans une autre police'),
    bad(f'<img src="{LOGO}jt-horizontal-noir.svg" style="width:72%">', 'Contraste insuffisant', bg=C['graphite']),
    bad(f'<img src="{LOGO}jt-horizontal-noir.svg" style="width:72%;position:relative">', 'Fond chargé sans cartouche', bg='repeating-linear-gradient(105deg,#d24a20 0 14px,#2b2b2b 14px 26px,#e8d9b0 26px 40px)'),
])
page(f'''{head('02 — Logo', 'Ce qu\'il ne faut pas faire.', 'Le logo est un fichier, pas un dessin à refaire. Toute modification, même légère, affaiblit la reconnaissance.')}
<div class="grid4 bads">{mis}</div>''', title='Interdits')

# ================================================================= 03 COULEURS
divider('03', 'Couleurs', 'Une palette courte et contrastée : du noir pour l\'exigence, de l\'orange pour l\'élan.',
        ['Palette & codes', 'Proportions', 'Contrastes & accessibilité'])

pal = [('Noir Carbone', C['noir'], '17 · 18 · 20', '60 · 50 · 40 · 100<br><small>texte : 0 · 0 · 0 · 100</small>', 'Black 6 C', 'Principale', '#fff'),
       ('Blanc Craie', C['craie'], '243 · 241 · 236', '0 · 1 · 3 · 5', 'Warm Gray 1 C à 30 %', 'Principale', C['noir']),
       ('Orange Impulsion', C['orange'], '250 · 70 · 22', '0 · 85 · 100 · 0', '172 C', 'Accent', C['noir']),
       ('Graphite', C['graphite'], '42 · 44 · 48', '70 · 60 · 50 · 75', '426 C', 'Secondaire', '#fff'),
       ('Gris Acier', C['acier'], '136 · 139 · 141', '0 · 1 · 0 · 45', 'Cool Gray 8 C', 'Secondaire', C['noir'])]
sw = ''.join(f'''<div class="swatch"><div class="sw-c" style="background:{h};color:{fg}"><span class="sw-role">{role}</span><b>{n}</b></div>
<dl><dt>HEX</dt><dd>{h}</dd><dt>RVB</dt><dd>{rgb}</dd><dt>CMJN</dt><dd>{cmyk}</dd><dt>Pantone</dt><dd>{pms}</dd></dl></div>'''
             for n, h, rgb, cmyk, pms, role, fg in pal)
page(f'''{head('03 — Couleurs', 'La palette.')}
<div class="swatches">{sw}</div>
<p class="foot-note">RVB/HEX pour les écrans · CMJN pour l'impression quadri · Pantone pour les tons directs, le textile et la signalétique.
Les références Pantone sont les plus proches : validez-les sur nuancier imprimé avant toute production.</p>''', title='Palette')

contr = [(C['craie'], C['noir'], 'Craie sur Noir', '16,6:1', 'AAA'),
         (C['noir'], C['craie'], 'Noir sur Craie', '16,6:1', 'AAA'),
         (C['orange'], C['noir'], 'Orange sur Noir', '5,3:1', 'AA'),
         (C['noir'], C['orange'], 'Noir sur Orange', '5,3:1', 'AA'),
         (C['acier'], C['noir'], 'Acier sur Noir', '5,5:1', 'AA'),
         (C['orange'], C['craie'], 'Orange sur Craie', '3,1:1', 'Grands titres uniquement')]
ct = ''.join(f'<div class="ct" style="background:{bg};color:{fg}"><span class="ct-a">Aa</span>'
             f'<span class="ct-l">{lab}<br><b>{r} · {v}</b></span></div>' for fg, bg, lab, r, v in contr)
page(f'''{head('03 — Couleurs', 'Proportions & contrastes.', 'Le noir et la craie portent la marque ; l\'orange ponctue. Trop d\'orange, et il ne signale plus rien.')}
<div class="ratio">
  <div style="flex:50;background:{C['noir']};color:#fff">Noir Carbone<b>50 %</b></div>
  <div style="flex:30;background:{C['craie']};color:{C['noir']}">Blanc Craie<b>30 %</b></div>
  <div style="flex:10;background:{C['graphite']};color:#fff">Graphite<b>10 %</b></div>
  <div style="flex:7;background:{C['orange']};color:{C['noir']}">Orange<b>7 %</b></div>
  <div style="flex:3;background:{C['acier']};color:{C['noir']}"><b>3 %</b></div>
</div>
<div class="grid6 cts">{ct}</div>
<p class="foot-note">Ratios calculés selon WCAG 2.1. L'orange n'est jamais utilisé pour du texte courant sur fond clair : réservez-le aux titres, chiffres clés, boutons sur fond noir et au symbole.</p>''',
     title='Proportions')

# ================================================================= 04 TYPO
divider('04', 'Typographie', 'Deux familles libres de droits : une pour frapper, une pour expliquer.',
        ['Archivo Expanded — titres', 'Inter — textes', 'Hiérarchie'])

page(f'''{head('04 — Typographie', 'Archivo Expanded.', 'Titres, accroches, chiffres clés. Large, solide, toujours en capitales. C\'est la police du logotype.')}
<div class="spec-type">
  <div class="aa archivo">Aa</div>
  <div>
    <div class="alpha archivo">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789 — €%+ ! ? &amp;</div>
    <div class="weights">
      <span class="archivo" style="font-weight:500">Medium 500</span>
      <span class="archivo" style="font-weight:700">Bold 700</span>
      <span class="archivo" style="font-weight:800">ExtraBold 800</span>
      <span class="archivo" style="font-weight:800;font-style:italic">ExtraBold Italic</span>
    </div>
    <ul class="rules small">
      <li>Largeur <b>Expanded (125)</b> — réglage « wdth » de la police variable.</li>
      <li>Titres en capitales, approche +1 à +4 %, interlignage 95–105 %.</li>
      <li>L'italique est réservé aux chiffres de performance (temps, kilos, séries).</li>
      <li>Licence SIL Open Font License · Google Fonts · gratuite, usage commercial autorisé.</li>
    </ul>
  </div>
</div>
<div class="sample-line">Vise plus haut. <span>−12 kg · 5×5 · 42:15</span></div>''', title='Archivo')

page(f'''{head('04 — Typographie', 'Inter & hiérarchie.')}
<div class="two-col">
  <div>
    <div class="spec-type small">
      <div class="aa inter">Aa</div>
      <div><div class="alpha inter">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789</div>
      <p class="note">Inter — textes courants, interfaces, légendes. Regular 400, Medium 500, SemiBold 600.
      Licence SIL OFL · Google Fonts.<br>Polices de secours : Arial / Helvetica.</p></div>
    </div>
  </div>
  <div class="hier">
    <div class="h-row"><span class="h-l">Surtitre<br><small>Archivo Exp. Medium 11 pt · capitales · +30 %</small></span><span class="kicker orange">Programme 12 semaines</span></div>
    <div class="h-row"><span class="h-l">Titre 1<br><small>Archivo Exp. ExtraBold 40 pt · capitales</small></span><span class="h1s">Vise plus haut.</span></div>
    <div class="h-row"><span class="h-l">Titre 2<br><small>Archivo Exp. Bold 20 pt</small></span><span class="h2s">Préparation physique</span></div>
    <div class="h-row"><span class="h-l">Chiffre clé<br><small>Archivo Exp. ExtraBold Italic</small></span><span class="kpi">−12 kg</span></div>
    <div class="h-row"><span class="h-l">Texte<br><small>Inter Regular 10–11 pt · interligne 150 %</small></span><span class="body-s">Un bilan complet, un plan d'entraînement sur mesure et un suivi chaque semaine pour progresser sans se blesser.</span></div>
    <div class="h-row"><span class="h-l">Légende<br><small>Inter Medium 8 pt · Gris Acier</small></span><span class="cap-s">Séance small group — Paris 11e</span></div>
  </div>
</div>''', title='Inter & hiérarchie')

# ================================================================= 05 ELEMENTS
divider('05', 'Éléments<br>graphiques', 'Des outils dérivés du symbole pour reconnaître la marque, même sans logo.',
        ['L\'angle 15° & le Trait', 'Le motif Sillage', 'Pictogrammes', 'Direction photo'])

page(f'''{head('05 — Éléments graphiques', 'L\'angle 15° & le Trait.', 'Deux signatures issues du symbole. L\'angle de son arête supérieure découpe les images et les aplats ; sa pointe effilée devient un trait de soulignement.')}
<div class="grid3 angle mt">
  <div><div class="ang-demo"><div class="ang-cut"></div><div class="ang-txt">15°</div></div>
    <b>Découpe à 15°</b><span>Coins d'images, bandeaux et aplats sont coupés à 15°, montant vers la droite. Un seul angle par composition.</span></div>
  <div><div class="trait-demo"><div class="t-title">Force &amp;<br>mobilité</div>{needle(260, 10, C['orange'])}</div>
    <b>Le Trait</b><span>Souligne un titre, sépare deux blocs, marque une progression. Toujours effilé vers la gauche, pointe vers la droite.</span></div>
  <div><div class="badge-demo"><div class="badge"><span>Séance</span><b>N°24</b></div>{needle(160, 6, C['craie'])}</div>
    <b>Étiquette</b><span>Aplat noir, texte Archivo, trait orange ou craie. Pour numéroter séances, semaines, étapes.</span></div>
</div>''', title='Angle & Trait')

page(f'''{head('05 — Éléments graphiques', 'Le motif « Sillage ».', 'Des lames effilées en quinconce, comme une trace de vitesse. Il habille les fonds, les dos de cartes, le textile et les publications sans texte.')}
<div class="grid3 patterns mt">
  <div><div class="pat">{pattern_svg(330, 250, '#ffffff', C['noir'], 0.14, 0.9, 'pa')}</div><b>Sur Noir</b><span>Blanc à 10–15 % d'opacité.</span></div>
  <div><div class="pat">{pattern_svg(330, 250, C['noir'], C['craie'], 0.08, 0.9, 'pb')}</div><b>Sur Craie</b><span>Noir à 6–10 %.</span></div>
  <div><div class="pat">{pattern_svg(330, 250, C['noir'], C['orange'], 0.9, 0.9, 'pc')}</div><b>Orange Impulsion</b><span>Pleine intensité, pour textile et goodies.</span></div>
</div>
<p class="foot-note">Le motif ne se combine jamais avec le logo dans la même zone : laissez toujours au logo sa zone de protection sur un aplat.</p>''',
     title='Motif')

ic = ''.join(f'<div class="ic"><div class="ic-box">{icon(n, 56)}</div><span>{n}</span></div>' for n in ICONS)
ic2 = ''.join(f'<div class="ic"><div class="ic-box dark">{icon(n, 40, C["orange"])}</div></div>' for n in list(ICONS)[:4])
page(f'''{head('05 — Éléments graphiques', 'Pictogrammes.', 'Un jeu de pictogrammes linéaires, angles vifs et extrémités carrées, pour présenter l\'offre et rythmer les supports.')}
<div class="icons">{ic}</div>
<div class="two-col mt-s"><ul class="rules small"><li>Grille de 48 × 48, trait de 3 unités, angles vifs, aucune courbe décorative.</li>
<li>Une seule couleur : Noir, Blanc ou Orange Impulsion selon le fond.</li><li>Taille minimale : 20 px / 6 mm.</li></ul>
<div class="icons small">{ic2}</div></div>''', title='Pictogrammes')

page(f'''{head('05 — Éléments graphiques', 'Direction photo.', 'Les photos montrent l\'effort réel, pas la pose. Lumière franche, contraste marqué, mouvement dans le cadre.')}
<div class="photo-dir">
  <div class="pd-main"><div class="pd-img a"></div><div class="pd-cut"></div>
    <div class="pd-txt"><div class="kicker orange">Exemple de composition · visuel d'illustration</div><div class="h2s light">L'effort,<br>pas la pose.</div></div>
    <img src="{LOGO}jt-symbole-blanc.svg" class="pd-logo"></div>
  <div class="pd-rules">
    <div class="kicker">À rechercher</div>
    <ul class="rules small"><li><b>Action</b> — en plein mouvement : sprint, levée, impact.</li>
    <li><b>Lumière latérale</b> — ombres franches, peau texturée, sueur visible.</li>
    <li><b>Diagonales</b> — corps et cadrage qui montent vers la droite, comme le symbole.</li>
    <li><b>Traitement</b> — tons neutres et froids désaturés ; l'orange vient des aplats, pas des filtres.</li></ul>
    <div class="kicker mt-s">À éviter</div>
    <ul class="rules small neg"><li>Photos de banque d'images posées et souriantes face caméra.</li>
    <li>Filtres colorés, vignettages, néons.</li><li>Selfies de miroir, avant/après sans consentement écrit.</li></ul>
  </div>
</div>''', title='Direction photo')

# ================================================================= 06 APPLICATIONS
divider('06', 'Applications', 'Le système en situation : ce que les gens verront, toucheront et porteront.',
        ['Papeterie', 'Réseaux sociaux', 'Textile', 'Accessoires & événementiel', 'Web', 'Motion'])

page(f'''{head('06 — Applications', 'Papeterie.')}
<div class="stationery">
  <div class="bc-stack">
    <div class="bc bc-front">{sym('bc-sym', color='#fff')}<div class="bc-tag">Vise plus haut.</div></div>
    <div class="bc bc-back">
      <div class="bc-name">Jonathan Temam</div><div class="bc-role">Coach sportif · Préparateur physique</div>
      {needle(70, 4, C['orange'])}
      <div class="bc-info">+33 6 00 00 00 00<br>contact@jonathantemam.fr<br>@jonathan.temam</div>
    </div>
    <p class="cap-s">Carte de visite 85 × 55 mm — recto Noir Carbone, verso Blanc Craie · papier 350 g non couché.</p>
  </div>
  <div class="letter">
    <div class="lt-head"><img src="{LOGO}jt-horizontal-noir.svg"></div>
    <div class="lt-body"><div class="lt-to">Madame Durand<br>Service RH — Atelier Nord<br>75011 Paris</div>
    <div class="lt-obj">Objet : programme de coaching collectif</div>
    {''.join('<div class="lt-line"></div>' for _ in range(9))}<div class="lt-line short"></div></div>
    <div class="lt-foot">{needle(40, 3, C['orange'])}<span>Jonathan Temam · Coach sportif · contact@jonathantemam.fr · SIRET 000 000 000 00000</span></div>
  </div>
  <div class="mail">
    <div class="kicker">Signature e-mail</div>
    <div class="mail-box"><div class="mail-sym">{sym('', color=C['noir'])}</div><div><b>Jonathan Temam</b><span>Coach sportif</span>
    <span class="o">+33 6 00 00 00 00 · jonathantemam.fr</span></div></div>
  </div>
</div>''', title='Papeterie')

# social
def post(kind):
    if kind == 'quote':
        return (f'<div class="post" style="background:{C["noir"]};color:#fff"><div class="pq">La discipline<br>bat la<br><span class="o">motivation.</span></div>'
                f'{needle(90, 5, C["orange"])}{sym("p-sym", color="#fff")}</div>')
    if kind == 'prog':
        return (f'<div class="post" style="background:{C["orange"]};color:{C["noir"]}"><div class="p-k">Nouveau</div>'
                f'<div class="pq">Programme<br>12 semaines</div><div class="p-s">Force · Cardio · Mobilité<br>Démarrage le 4 novembre</div>'
                f'{sym("p-sym", color=C["noir"])}</div>')
    if kind == 'kpi':
        return (f'<div class="post" style="background:{C["craie"]};color:{C["noir"]}"><div class="p-k">Résultats</div>'
                f'<div class="pkpi">−12<small>kg</small></div><div class="p-s">16 semaines · 3 séances / semaine<br>Témoignage client (exemple)</div>'
                f'{sym("p-sym", color=C["noir"])}</div>')
    if kind == 'pattern':
        return f'<div class="post">{pattern_svg(300, 300, "#fff", C["noir"], 0.14, 0.6, "pp"+str(id(kind)))}{sym("p-sym big", color=C["orange"])}</div>'
    if kind == 'photo':
        return f'<div class="post pd-img b"><div class="p-cut"></div>{sym("p-sym", color="#fff")}</div>'
    return f'<div class="post" style="background:{C["graphite"]};color:#fff"><div class="p-k">Conseil n°08</div><div class="pq sm">Dormir<br>est un<br>entraînement.</div>{sym("p-sym", color=C["orange"])}</div>'


grid9 = ''.join(post(k) for k in ['quote', 'photo', 'prog', 'kpi', 'pattern', 'tip', 'photo', 'quote', 'kpi', 'tip', 'prog', 'photo'])
page(f'''{head('06 — Applications', 'Réseaux sociaux.')}
<div class="social">
  <div class="phone"><div class="ph-screen">
    <div class="ig-head"><img src="{LOGO}jt-avatar-noir.svg" class="ig-av"><div class="ig-stats"><b>248</b><span>publications</span></div><div class="ig-stats"><b>12,4 k</b><span>abonnés</span></div><div class="ig-stats"><b>310</b><span>suivi(e)s</span></div></div>
    <div class="ig-bio"><b>Jonathan Temam</b><br>Coach sportif · Préparation physique<br>Vise plus haut. ↗ Bilan offert</div>
    <div class="ig-grid">{grid9}</div></div></div>
  <div class="posts">
    <div class="post-row">{post('quote')}{post('prog')}{post('kpi')}</div>
    <div class="post-legend"><span><b>Citation</b> Noir, mot-clé en orange</span><span><b>Annonce</b> Orange, texte noir</span><span><b>Résultat</b> Craie, chiffre en italique</span></div>
    <ul class="rules small"><li>Symbole toujours en bas à droite, même taille et même marge sur tous les posts.</li>
    <li>Alterner photo / aplat pour un profil rythmé ; jamais deux aplats orange côte à côte.</li>
    <li>Formats : 1080 × 1350 (post) et 1080 × 1920 (story).</li></ul>
    <div class="kicker mt-s">Stories à la une</div>
    <div class="highlights">{''.join(f'<div><span class="hl">{icon(i, 26, C["orange"])}</span><small>{t}</small></div>' for i, t in [('Force', 'Coaching'), ('Progression', 'Résultats'), ('Planning', 'Programmes'), ('Nutrition', 'Nutrition'), ('Visio', 'En ligne')])}</div>
  </div>
  <div class="story"><div class="pd-img a st-img"></div><div class="st-cut"></div>
    <div class="st-txt"><div class="kicker orange">Story</div><div class="pq sm light">Séance<br>du jour</div><div class="st-list">5 × 5 Squat<br>4 × 8 Rowing<br>3 × 12 Fentes</div></div>
    <img src="{LOGO}jt-symbole-blanc.svg" class="st-logo"></div>
</div>''', title='Réseaux sociaux')

TSHIRT = 'M95 22 L58 32 L8 78 L44 120 L70 100 L70 304 L230 304 L230 100 L256 120 L292 78 L242 32 L205 22 C192 52 108 52 95 22 Z'
page(f'''{head('06 — Applications', 'Textile.', 'Le textile est le premier support de visibilité d\'un coach : il doit se reconnaître de loin, à l\'entraînement comme en dehors.')}
<div class="textile">
  <div class="tee"><svg viewBox="0 0 300 320"><path d="{TSHIRT}" fill="{C['noir']}"/><path d="M95 22 C108 52 192 52 205 22" fill="none" stroke="#2c2e33" stroke-width="6"/>
    <g transform="translate(176 92) scale(0.052)"><path fill="#fff" d="{SYM_D}"/></g></svg><b>T-shirt — face</b><span>Symbole blanc côté cœur, 8 cm, sérigraphie ou flex.</span></div>
  <div class="tee"><svg viewBox="0 0 300 320"><path d="{TSHIRT}" fill="{C['noir']}"/><path d="M95 22 C108 52 192 52 205 22" fill="none" stroke="#2c2e33" stroke-width="6"/>
    <g transform="translate(92 110) scale(0.139)"><path fill="{C['orange']}" d="{SYM_D}"/></g>
    <text x="150" y="200" text-anchor="middle" class="tee-t">VISE PLUS HAUT.</text></svg><b>T-shirt — dos</b><span>Symbole Orange Impulsion 25 cm et signature.</span></div>
  <div class="tee"><svg viewBox="0 0 300 320"><path d="{TSHIRT}" fill="{C['craie']}" stroke="#d8d4cb" stroke-width="2"/><path d="M95 22 C108 52 192 52 205 22" fill="none" stroke="#d8d4cb" stroke-width="6"/>
    <g transform="translate(103 115) scale(0.112)"><path fill="{C['noir']}" d="{SYM_D}"/></g></svg><b>T-shirt clients</b><span>Craie, symbole noir centré : tenue offerte aux élèves.</span></div>
  <div class="tee"><svg viewBox="0 0 300 320"><path d="M40 210 C40 120 90 78 150 78 C210 78 260 120 260 210 Z" fill="{C['noir']}"/>
    <path d="M40 210 L260 210 C276 210 292 222 296 238 L4 238 C8 222 24 210 40 210 Z" fill="#202226"/><circle cx="150" cy="80" r="6" fill="#202226"/>
    <g transform="translate(108 140) scale(0.1)"><path fill="#fff" d="{SYM_D}"/></g></svg><b>Casquette</b><span>Broderie blanche, version petite taille sous 4 cm.</span></div>
</div>''', title='Textile')

page(f'''{head('06 — Applications', 'Accessoires & événementiel.')}
<div class="acc">
  <div class="bottle"><svg viewBox="0 0 120 340"><rect x="36" y="6" width="48" height="34" rx="6" fill="{C['graphite']}"/>
    <rect x="20" y="40" width="80" height="292" rx="22" fill="{C['noir']}"/><rect x="20" y="300" width="80" height="10" fill="{C['orange']}"/>
    <g transform="translate(29 160) scale(0.075)"><path fill="#fff" d="{SYM_D}"/></g></svg><b>Gourde</b><span>Inox noir mat, marquage laser blanc.</span></div>
  <div class="tote"><svg viewBox="0 0 260 320"><path d="M80 90 C80 20 180 20 180 90" fill="none" stroke="{C['noir']}" stroke-width="9"/>
    <rect x="20" y="88" width="220" height="226" fill="{C['craie']}" stroke="#d8d4cb" stroke-width="2"/>
    <g transform="translate(53 150) scale(0.18)"><path fill="{C['noir']}" d="{SYM_D}"/></g>
    <text x="130" y="262" text-anchor="middle" class="tee-t" style="fill:{C['noir']}">VISE PLUS HAUT.</text></svg><b>Tote bag</b><span>Coton naturel, sérigraphie noire 1 couleur.</span></div>
  <div class="towel"><svg viewBox="0 0 220 320"><rect x="20" y="10" width="180" height="300" fill="{C['orange']}"/>
    <rect x="20" y="268" width="180" height="16" fill="{C['noir']}"/>
    <g transform="translate(66 220) scale(0.105)"><path fill="{C['noir']}" d="{SYM_D}"/></g></svg><b>Serviette</b><span>Microfibre orange, broderie noire.</span></div>
  <div class="rollup"><div class="ru-tile"><div class="ru">{pattern_svg(130, 330, '#fff', C['noir'], 0.1, 0.45, 'ru')}
    <div class="ru-in">{sym('ru-sym', color=C['orange'])}<img src="{LOGO}jt-logotype-blanc.svg"><div class="ru-t">Coaching<br>individuel<br>&amp; collectif</div>{needle(80, 4, C['orange'])}<div class="ru-b">Bilan offert</div></div></div></div>
    <b>Roll-up 85 × 200 cm</b><span>Salons, salles partenaires, événements.</span></div>
</div>''', title='Accessoires')

page(f'''{head('06 — Applications', 'Web.')}
<div class="web">
  <div class="browser"><div class="br-bar"><i></i><i></i><i></i><span>jonathantemam.fr</span></div>
    <div class="site">
      <div class="site-pattern">{pattern_svg(820, 470, '#fff', 'none', 0.06, 0.8, 'sp')}</div>
      <div class="nav"><img src="{LOGO}jt-horizontal-blanc.svg"><div class="nav-l"><span>Coaching</span><span>Programmes</span><span>Résultats</span><span>Contact</span></div><span class="btn">Réserver</span></div>
      <div class="hero"><div class="kicker orange">Coach sportif · Paris &amp; en ligne</div>
        <div class="h-big">Vise<br>plus haut.</div>
        <p>Coaching individuel, small group et préparation physique. Un plan clair, un suivi chaque semaine.</p>
        <span class="btn big">Réserver mon bilan offert</span></div>
      {sym('site-sym', color=C['orange'])}
      <div class="site-strip">{''.join(f'<div>{icon(n, 26, C["orange"])}<span>{n}</span></div>' for n in ['Force', 'Cardio', 'Nutrition', 'Visio'])}</div>
    </div></div>
  <div class="mobile"><div class="m-screen"><div class="m-nav"><img src="{LOGO}jt-symbole-blanc.svg"><span>☰</span></div>
    <div class="kicker orange sm">Programme</div><div class="m-h">12 semaines<br>pour changer<br>de niveau.</div>{needle(80, 4, C['orange'])}
    <div class="m-card"><b>−12<small> kg</small></b><span>en moyenne sur 16 semaines*</span></div>
    <span class="btn">Commencer</span></div>
    <div class="app-icons"><img src="../logo/web/apple-touch-icon.png"><img src="../logo/web/favicon-48.png" class="fav"><img src="../logo/web/favicon-32.png" class="fav s"></div></div>
</div>
<p class="foot-note">Boutons Orange Impulsion avec texte Noir Carbone · fond de site Noir Carbone · favicon et icônes d'application fournis (dossier logo/web). *Chiffres d'illustration.</p>''',
     title='Web')

# motion storyboard
def frame(clip_b, clip_j, text=False, n='', label=''):
    k = abs(hash(n)) % 10**6
    return (f'<div class="mf"><div class="mf-art"><svg viewBox="-60 -60 957 532">'
            f'<defs><clipPath id="cb{k}"><rect x="{837 - clip_b}" y="-50" width="{clip_b + 10}" height="520"/></clipPath>'
            f'<clipPath id="cj{k}"><rect x="-10" y="-10" width="{clip_j}" height="520"/></clipPath></defs>'
            f'<path clip-path="url(#cb{k})" fill="#fff" d="{poly(BLADE)}"/>'
            f'<path clip-path="url(#cj{k})" fill="{C["orange"] if clip_j < 900 else "#fff"}" d="{poly(J)}"/></svg>'
            + (f'<img src="{LOGO}jt-logotype-blanc.svg" class="mf-wm">' if text else '')
            + f'</div><b>{n}</b><span>{label}</span></div>')


page(f'''{head('06 — Applications', 'Motion — l\'animation du logo.', 'Pour les vidéos, reels et l\'ouverture du site. 1,6 seconde, du trait à la signature.')}
<div class="motion">
  {frame(260, 0, n='0,0 s', label='La pointe entre par la droite et trace la barre.')}
  {frame(837, 0, n='0,4 s', label='La lame descend : le T est formé.')}
  {frame(837, 560, n='0,8 s', label='Le J glisse en contre-mouvement, en orange.')}
  {frame(837, 1000, text=True, n='1,6 s', label='Tout se fige en blanc, le nom apparaît.')}
</div>
<ul class="rules small two"><li>Courbe d'accélération « expo-out » : départ rapide, arrivée douce — l'élan, pas le rebond.</li>
<li>Toujours terminer sur le logo statique exact. Pas de rotation, pas de rebond, pas d'effet 3D.</li>
<li>Son (optionnel) : un « whoosh » court et sec, synchronisé sur la lame à 0,4 s.</li>
<li>Livrable conseillé : MP4 / MOV avec transparence et fichier Lottie pour le web.</li></ul>''', title='Motion')

# ================================================================= 07 FICHIERS
divider('07', 'Fichiers<br>&amp; contacts', 'Le bon fichier, au bon endroit.', ['Arborescence des livrables', 'Quel format pour quel usage'])

page(f'''{head('07 — Fichiers & contacts', 'Les fichiers livrés.')}
<div class="two-col files">
  <pre class="tree">jonathan-temam/
├─ Jonathan-Temam_Charte-graphique.pdf
├─ Jonathan-Temam_Charte-graphique.pptx  modifiable
├─ Jonathan-Temam_Logos-vectoriels.zip
├─ polices/   Archivo Expanded + Inter (.ttf)
├─ logo/
│  ├─ svg/ pdf/ eps/   masters vectoriels
│  │  ├─ jt-horizontal-{{noir|blanc|accent-…}}
│  │  ├─ jt-vertical-{{…}} · jt-logotype-{{…}}
│  │  ├─ jt-symbole-{{noir|blanc|orange|…}}
│  │  ├─ jt-symbole-petite-taille
│  │  └─ jt-avatar-{{noir|orange}}
│  ├─ png/   mêmes fichiers, fond transparent
│  └─ web/   favicon, icônes, webmanifest
├─ presentation/   planche de présentation
└─ source/   scripts de génération</pre>
  <div>
    <table class="spec">
      <tr><th>Usage</th><th>Format</th></tr>
      <tr><td>Web, réseaux, Canva</td><td>SVG ou PNG</td></tr>
      <tr><td>Imprimeur, sérigraphie, broderie</td><td>PDF / EPS / SVG + codes CMJN / Pantone</td></tr>
      <tr><td>Modifier cette charte</td><td>.pptx + polices installées</td></tr>
      <tr><td>Photo de profil</td><td>jt-avatar-noir.png</td></tr>
      <tr><td>Navigateur, smartphone</td><td>dossier web/</td></tr>
      <tr><td>Fond sombre</td><td>versions « blanc » ou « accent-sombre »</td></tr>
    </table>
    <div class="kicker mt-s">Nomenclature</div>
    <p class="note"><code>jt-[version]-[couleur].[format]</code> — ex. <code>jt-vertical-blanc.png</code>.
    Les PNG sont exportés à 2400 px de large ; pour une impression grand format, utilisez toujours le SVG.</p>
    <div class="contact"><div class="kicker">Contact marque</div><b>Jonathan Temam</b><span>contact@jonathantemam.fr · +33 6 00 00 00 00</span>
    <span class="cap-s">Coordonnées à confirmer avant impression.</span></div>
  </div>
</div>''', title='Fichiers')

# back cover
page(f'''<div class="cover-pattern">{pattern_svg(1123, 794, '#ffffff', opacity=0.045, uid='bp')}</div>
<div class="back"><img src="{LOGO}jt-vertical-accent-sombre.svg"><div class="signature light">Vise plus haut.</div></div>''',
     cls='cover', num=False, dark=True)

# ---------------------------------------------------------------- CSS
CSS = open(os.path.join(HERE, 'charte.css')).read()


def build_html():
    out = []
    total = len(PAGES)
    for i, (body, cls, title, num, dark) in enumerate(PAGES, 1):
        foot = ''
        if num:
            foot = (f'<div class="pfoot"><span>{sym("pf-sym")}Jonathan Temam — Charte graphique</span>'
                    f'<span>{title or ""}</span><span class="pn">{i:02d}</span></div>')
        out.append(f'<section class="page {cls} {"dark" if dark else ""}" id="p{i}">{body}{foot}</section>')
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Jonathan Temam — Charte graphique</title><style>{CSS}</style></head><body>{''.join(out)}</body></html>'''


if __name__ == '__main__':
    html = build_html()
    path = os.path.join(HERE, 'charte.html')
    open(path, 'w').write(html)
    print('pages', len(PAGES), '->', path)
