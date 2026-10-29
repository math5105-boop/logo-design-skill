// Extract every page of charte.html into: a text-free background PNG, editable text blocks and
// movable logo images (positions in CSS px on a 1123 × 794 page). Used by build_pptx.js.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = process.argv[2];
fs.mkdirSync(path.join(OUT, 'bg'), { recursive: true });

function collect() {
  const SKIP = el => el.closest('svg, style, .div-num, .pfoot .pf-sym');
  const isBlock = el => getComputedStyle(el).display !== 'inline';
  const blockOf = node => { let e = node.parentElement; while (e && !isBlock(e)) e = e.parentElement; return e; };
  const hex = c => {
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return { hex: '000000', a: 1 };
    const p = m[1].split(',').map(s => parseFloat(s));
    return { hex: p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase(), a: p.length > 3 ? p[3] : 1 };
  };
  const out = [];
  const toWrap = [];
  document.querySelectorAll('section.page').forEach((pg, pi) => {
    const pr = pg.getBoundingClientRect();
    const walker = document.createTreeWalker(pg, NodeFilter.SHOW_TEXT);
    const groups = new Map();
    let n;
    while ((n = walker.nextNode())) {
      if (!n.textContent.trim() || SKIP(n.parentElement)) continue;
      const b = blockOf(n);
      if (!groups.has(b)) groups.set(b, []);
      groups.get(b).push(n);
    }
    const blocks = [];
    groups.forEach((nodes, b) => {
      // runs in document order, with <br> as line breaks, without descending into child blocks
      const runs = [];
      const walk = el => {
        for (const c of el.childNodes) {
          if (c.nodeType === 3) {
            if (!nodes.includes(c)) continue;
            const cs = getComputedStyle(c.parentElement);
            let t = c.textContent.replace(/\s+/g, ' ');
            if (cs.textTransform === 'uppercase') t = t.toUpperCase();
            const col = hex(cs.color);
            runs.push({ t, font: cs.fontFamily, w: +cs.fontWeight, it: cs.fontStyle === 'italic', stretch: cs.fontStretch,
              size: parseFloat(cs.fontSize), color: col.hex, alpha: col.a * +cs.opacity,
              ls: cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing),
              strike: cs.textDecorationLine.includes('line-through'), deco: hex(cs.textDecorationColor).hex });
          } else if (c.nodeType === 1) {
            if (c.tagName === 'BR') runs.push({ br: true });
            else if (!isBlock(c) && !c.closest('svg')) walk(c);
          }
        }
      };
      walk(b);
      // trim leading/trailing spaces per line
      let first = runs.find(r => !r.br); if (first) first.t = first.t.replace(/^ /, '');
      for (let i = 0; i < runs.length; i++) {
        if (runs[i].br) { if (runs[i - 1] && !runs[i - 1].br) runs[i - 1].t = runs[i - 1].t.replace(/ $/, ''); if (runs[i + 1] && !runs[i + 1].br) runs[i + 1].t = runs[i + 1].t.replace(/^ /, ''); }
      }
      const last = [...runs].reverse().find(r => !r.br); if (last) last.t = last.t.replace(/ $/, '');
      // union of text rects
      let x1 = 1e9, y1 = 1e9, x2 = -1e9, y2 = -1e9;
      nodes.forEach(t => { const r = document.createRange(); r.selectNodeContents(t);
        for (const q of r.getClientRects()) { if (q.width < 0.5) continue; x1 = Math.min(x1, q.left); y1 = Math.min(y1, q.top); x2 = Math.max(x2, q.right); y2 = Math.max(y2, q.bottom); } });
      const cs = getComputedStyle(b);
      const br = b.getBoundingClientRect();
      const lh = cs.lineHeight === 'normal' ? parseFloat(cs.fontSize) * 1.2 : parseFloat(cs.lineHeight);
      const content = { x: br.left + parseFloat(cs.paddingLeft), w: br.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) };
      const pre = cs.whiteSpace.startsWith('pre');
      if (pre) runs.splice(0, runs.length, ...b.innerText.split('\n').flatMap((l, i, a) => {
        const r = { t: l, font: cs.fontFamily, w: +cs.fontWeight, it: false, stretch: cs.fontStretch, size: parseFloat(cs.fontSize), color: hex(cs.color).hex, alpha: 1, ls: 0 };
        return i < a.length - 1 ? [r, { br: true }] : [r];
      }));
      blocks.push({ x: x1 - pr.left, y: y1 - pr.top, w: x2 - x1, h: y2 - y1, cx: content.x - pr.left, cw: content.w,
        lh, align: cs.textAlign, nowrap: cs.whiteSpace === 'nowrap' || pre, lines: Math.round((y2 - y1) / lh), runs,
        name: (b.className && typeof b.className === 'string' ? b.className.split(' ')[0] : b.tagName.toLowerCase()) });
      toWrap.push(...nodes);
    });
    // logos: plain <img> without effects become separate pictures
    const imgs = [];
    pg.querySelectorAll('img').forEach(im => {
      const cs = getComputedStyle(im);
      if (cs.transform !== 'none' || cs.filter !== 'none' || parseFloat(cs.borderRadius) > 0 || im.closest('.bad')) return;
      const r = im.getBoundingClientRect();
      if (r.width < 2) return;
      imgs.push({ src: decodeURI(im.src.replace('file://', '')), x: r.left - pr.left, y: r.top - pr.top, w: r.width, h: r.height, op: +cs.opacity });
      im.classList.add('__img');
    });
    out.push({ blocks, imgs, dark: pg.classList.contains('dark') });
  });
  // hide text only after every page has been measured; <x-t> matches no page CSS selector
  toWrap.forEach(t => { const s = document.createElement('x-t'); t.replaceWith(s); s.appendChild(t); });
  const st = document.createElement('style');
  st.textContent = 'x-t{color:transparent!important;text-decoration-color:transparent!important;-webkit-text-stroke:0!important}.__img{visibility:hidden!important}';
  document.head.appendChild(st);
  return out;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(__dirname, 'charte.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const data = await page.evaluate(collect);
  await page.waitForTimeout(200);
  const n = await page.locator('section.page').count();
  for (let i = 1; i <= n; i++) await page.locator('#p' + i).screenshot({ path: path.join(OUT, 'bg', `bg-${String(i).padStart(2, '0')}.png`) });
  fs.writeFileSync(path.join(OUT, 'pages.json'), JSON.stringify(data, null, 1));
  await browser.close();
  console.log('pages', data.length, 'blocks', data.reduce((a, p) => a + p.blocks.length, 0), 'imgs', data.reduce((a, p) => a + p.imgs.length, 0));
})();
