# Jonathan Temam — identité visuelle

Branding complet du coach sportif Jonathan Temam, construit à partir de son monogramme JT existant avec le skill `logo-design`.

## Livrables

| Fichier | Contenu |
|---|---|
| `Jonathan-Temam_Charte-graphique.pdf` | Charte graphique de 36 pages (A4 paysage) : plateforme de marque, logo, couleurs, typographie, éléments graphiques, applications, motion, fichiers |
| `logo/svg/` | Masters vectoriels : horizontal, vertical, logotype, symbole, symbole petite taille et avatars, en noir, blanc et deux versions accent |
| `logo/png/` | Les mêmes fichiers en PNG transparents (2400 px de large, avatars en 1024 px) |
| `logo/web/` | `favicon.ico`, `favicon.svg`, icônes 16/32/48/192/512, apple-touch, maskable, `site.webmanifest`, `head-snippet.html` |
| `presentation/` | Planche de présentation client (HTML + 5 slides PNG) générée par `presentation_board.py` |
| `source/` | Scripts de génération, polices Archivo et Inter (SIL OFL) et HTML/CSS de la charte |

## Système en bref

- **Symbole** : les initiales J et T dessinées comme deux lames qui montent à 15°. Construit uniquement en lignes droites, sur des angles de 15°, 11°, 65° et 42°.
- **Couleurs** : Noir Carbone `#111214`, Blanc Craie `#F3F1EC`, Orange Impulsion `#FA4616` (Pantone 172 C), Graphite `#2A2C30`, Gris Acier `#888B8D`.
- **Typographie** : Archivo Expanded (titres, logotype) et Inter (textes). Les deux sont gratuites (Google Fonts, licence OFL).
- **Signature** : « Vise plus haut. »
- **Éléments graphiques** : découpes à 15°, « le Trait » (pointe effilée), motif « Sillage », 8 pictogrammes.

## Régénérer

```bash
cd source
python3 build_logos.py                                  # logo/svg/*
python3 build_charte.py                                 # charte.html
NODE_PATH=$(npm root -g) node render_charte.js          # PDF + aperçus (Playwright/Chromium)
```
Il faut `fonttools` et `brotli` pour `build_logos.py`, et `cairosvg` pour les PNG.

## Notes de passation

- **Vectorisation** : le symbole a été reconstruit à partir d'une photo d'écran, après correction de la perspective. Il a ensuite été superposé au tracé d'origine pour vérification. Si le fichier vectoriel original existe (Affinity ou Canva), comparez-le aux masters avant l'impression.
- **Tests effectués** : `svg_audit.py` (score 92/100). Le seul avertissement concerne l'arête extérieure à 42°, signalée comme proche de 45°. Elle est conservée pour rester fidèle au dessin du client. Le symbole a aussi été testé en 16, 32 et 48 px. En dessous de 32 px, utilisez `jt-symbole-petite-taille`, dont les pointes sont raccourcies et épaissies.
- **À confirmer** : les coordonnées (téléphone, e-mail, Instagram, SIRET) sont des exemples. Les chiffres et témoignages des maquettes servent d'illustration. Les teintes Pantone sont les plus proches : validez-les sur nuancier imprimé.
- **Photos** : les visuels photo de la charte sont des placeholders. La direction photo (p. 26) sert de brief pour une séance.
- **Marque** : un dépôt de marque (INPI) et une recherche d'antériorité restent recommandés avant une large diffusion.
