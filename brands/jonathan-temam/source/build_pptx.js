// Build the editable PowerPoint version of the brand book from extract_charte.js output.
// Usage: node build_pptx.js <extract-dir> [out.pptx]
const pptxgen = require('pptxgenjs');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const DIR = process.argv[2];
const OUT = process.argv[3] || path.join(__dirname, '..', 'Jonathan-Temam_Charte-graphique.pptx');
const SKILL = process.env.PPTX_SKILL;
const pages = JSON.parse(fs.readFileSync(path.join(DIR, 'pages.json')));

const PX = 96;                      // CSS px per inch
const PT = 0.75;                    // pt per CSS px
const W = 1123 / PX, H = 794 / PX;  // A4 landscape

const SECTIONS = [[1, 'Ouverture'], [4, '01 — Plateforme de marque'], [8, '02 — Logo'], [16, '03 — Couleurs'],
  [19, '04 — Typographie'], [22, '05 — Éléments graphiques'], [27, '06 — Applications'], [34, '07 — Fichiers & contacts']];

const THEME = {
  name: 'Jonathan Temam', headFontFace: 'Archivo Expanded ExtraBold', bodyFontFace: 'Inter',
  colors: { dk1: '111214', lt1: 'FFFFFF', dk2: '2A2C30', lt2: 'F3F1EC', accent1: 'FA4616', accent2: '111214',
    accent3: '2A2C30', accent4: '888B8D', accent5: 'F3F1EC', accent6: 'FA4616', hlink: 'FA4616', folHlink: '888B8D' },
};

function face(r) {
  if (/Archivo/.test(r.font)) {
    if (r.w >= 750) return { fontFace: 'Archivo Expanded ExtraBold', bold: false };
    if (r.w >= 650) return { fontFace: 'Archivo Expanded', bold: true };
    if (r.w >= 550) return { fontFace: 'Archivo Expanded SemiBold', bold: false };
    return { fontFace: 'Archivo Expanded Medium', bold: false };
  }
  if (/Inter/.test(r.font)) {
    if (r.w >= 650) return { fontFace: 'Inter', bold: true };
    if (r.w >= 550) return { fontFace: 'Inter SemiBold', bold: false };
    if (r.w >= 450) return { fontFace: 'Inter Medium', bold: false };
    return { fontFace: 'Inter', bold: false };
  }
  if (/Mono/.test(r.font)) return { fontFace: 'Courier New', bold: false };
  if (/Georgia/.test(r.font)) return { fontFace: 'Georgia', bold: r.w >= 600 };
  return { fontFace: 'Arial', bold: r.w >= 600 };
}

// semi-transparent text is flattened onto the background colour under it (sampled from the page render)
const bgCache = new Map();
async function bgAt(num, x, y) {
  if (!bgCache.has(num)) bgCache.set(num, await sharp(path.join(DIR, 'bg', `bg-${String(num).padStart(2, '0')}.png`)).raw().toBuffer({ resolveWithObject: true }));
  const { data, info } = bgCache.get(num);
  const px = Math.min(info.width - 1, Math.round(x * 2)), py = Math.min(info.height - 1, Math.round(y * 2));
  const i = (py * info.width + px) * info.channels;
  return [data[i], data[i + 1], data[i + 2]];
}
function blend(hex, bg, a) {
  const fg = [0, 2, 4].map(k => parseInt(hex.slice(k, k + 2), 16));
  return fg.map((v, k) => Math.round(v * a + bg[k] * (1 - a)).toString(16).padStart(2, '0')).join('').toUpperCase();
}

const pngCache = new Map();
async function raster(src, wpx) {
  const key = src + '@' + Math.round(wpx);
  if (pngCache.has(key)) return pngCache.get(key);
  const target = Math.max(64, Math.round(wpx * 4));
  let buf;
  if (src.endsWith('.svg')) buf = await sharp(fs.readFileSync(src), { density: 600 }).resize({ width: target }).png().toBuffer();
  else buf = await sharp(src).resize({ width: Math.min(target, 1024) }).png().toBuffer();
  const data = 'image/png;base64,' + buf.toString('base64');
  pngCache.set(key, data);
  return data;
}

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: 'A4_PAYSAGE', width: W, height: H });
  pres.layout = 'A4_PAYSAGE';
  pres.title = 'Jonathan Temam — Charte graphique';
  pres.author = 'Jonathan Temam';
  pres.subject = 'Identité visuelle — version 1.0';
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

  let section = null;
  for (let i = 0; i < pages.length; i++) {
    const pg = pages[i], num = i + 1;
    const sec = SECTIONS.filter(([p]) => p <= num).pop()[1];
    if (sec !== section) { pres.addSection({ title: sec }); section = sec; }
    const slide = pres.addSlide({ sectionTitle: sec });
    slide.background = { path: path.join(DIR, 'bg', `bg-${String(num).padStart(2, '0')}.png`) };

    for (const [k, im] of pg.imgs.entries()) {
      slide.addImage({ data: await raster(im.src, im.w), x: im.x / PX, y: im.y / PX, w: im.w / PX, h: im.h / PX,
        altText: path.basename(im.src, path.extname(im.src)), objectName: `Logo ${k + 1}` });
    }

    for (const [k, b] of pg.blocks.entries()) {
      const runs = [];
      for (const r of b.runs) {
        if (r.br) { if (runs.length) runs[runs.length - 1].options.breakLine = true; continue; }
        if (!r.t) continue;
        const o = { ...face(r), fontSize: Math.round(r.size * PT * 10) / 10, color: r.color, italic: r.it };
        if (r.ls) o.charSpacing = Math.round(r.ls * PT * 100) / 100;
        if (r.alpha < 0.99) o.color = blend(r.color, await bgAt(num, b.x + b.w / 2, b.y + b.h / 2), r.alpha);
        if (r.strike) o.strike = 'sngStrike';
        // symbols missing from Archivo/Inter get a symbol font of their own
        r.t.split(/([✓✕☰↗])/).filter(Boolean).forEach(part => runs.push({ text: part,
          options: /^[✓✕☰↗]$/.test(part) ? { ...o, fontFace: 'Segoe UI Symbol', bold: false } : { ...o } }));
      }
      if (!runs.length) continue;
      const single = b.nowrap || b.lines <= 1;
      const maxSize = Math.max(...b.runs.filter(r => !r.br).map(r => r.size));
      let x, w;
      if (single) {
        const spaced = b.runs.some(r => r.ls > 0);
        const extra = b.w * (spaced ? 0.3 : 0.1) + 10;
        w = b.w + extra;
        x = b.align === 'center' ? b.x - extra / 2 : (b.align === 'right' || b.align === 'end') ? b.x - extra : b.x;
      } else {
        x = b.cx; w = b.cw + 6;
        if (b.align === 'center') x -= 3;
      }
      const pad = Math.max(2, b.lh * 0.15);
      slide.addText(runs, {
        x: x / PX, y: b.y / PX, w: w / PX, h: (b.h + pad) / PX,
        margin: 0, valign: 'top', isTextBox: true, wrap: !single, fit: 'none',
        align: b.align === 'center' ? 'center' : (b.align === 'right' || b.align === 'end') ? 'right' : 'left',
        lineSpacing: Math.round(Math.max(b.lh, maxSize) * PT * 10) / 10,
        objectName: `Texte ${k + 1} (${b.name})`,
      });
    }
  }
  await pres.writeFile({ fileName: OUT });
  if (SKILL) {
    const { applyTheme } = require(path.join(SKILL, 'scripts', 'apply_theme.js'));
    await applyTheme(OUT, THEME);
  }
  console.log('wrote', OUT);
})();
