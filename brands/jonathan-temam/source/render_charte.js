// Render charte.html to PDF and per-page PNG previews with the pre-installed Playwright Chromium.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const here = __dirname, root = path.dirname(here);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 1.5 });
  await page.goto('file://' + path.join(here, 'charte.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const only = process.argv[2];
  if (!only) {
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: path.join(root, 'Jonathan-Temam_Charte-graphique.pdf'), preferCSSPageSize: true, printBackground: true });
    await page.emulateMedia({ media: 'screen' });
  }
  const outDir = process.argv[3] || path.join(root, 'apercus');
  require('fs').mkdirSync(outDir, { recursive: true });
  const n = await page.locator('section.page').count();
  for (let i = 1; i <= n; i++) {
    if (only && only !== 'all' && !only.split(',').includes(String(i))) continue;
    await page.locator('#p' + i).screenshot({ path: path.join(outDir, `page-${String(i).padStart(2, '0')}.png`) });
  }
  await browser.close();
  console.log('rendered', n, 'pages');
})();
