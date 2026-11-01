// Runs browser_check.js against rendered/ in headless Chromium, serving only rendered/ on 127.0.0.1.
// Uses the locally installed playwright-core 1.52 and its Chromium 1169 (R1 used Playwright Chromium too).
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require(process.env.PW_CORE || 'C:/Users/reall/AppData/Local/Temp/pw-1.52.0/node_modules/playwright-core');
const ROOT = __dirname, SITE = path.join(ROOT, 'rendered');
const R1SVG = path.join(ROOT, '..', 'WPE_Core2_Reader_Fix_R1_20261031', 'assets', 'incline-block-corrected.svg');
const R2SVG = path.join(ROOT, 'assets', 'incline-block-corrected-r2.svg');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };

(async () => {
  const pre = [];
  // Geometry identical: everything except the 37° label line must be byte-identical to R1's asset.
  const strip = s => s.split('\n').filter(l => !l.includes('>37°</text>')).join('\n');
  const a = fs.readFileSync(R1SVG, 'utf8'), b = fs.readFileSync(R2SVG, 'utf8');
  pre.push({ name: 'R2-L2 Incline geometry identical to R1 (only the 37° label line differs)', pass: strip(a) === strip(b) && a !== b });

  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '') || 'core2.html';
    const file = path.resolve(SITE, rel);
    if (!file.startsWith(SITE) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const url = `http://127.0.0.1:${server.address().port}/core2.html`;
  const browser = await chromium.launch({ headless: true });
  const page = await (await browser.newContext()).newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  let result;
  try {
    await page.goto(url, { waitUntil: 'load' });
    const fn = eval(fs.readFileSync(path.join(ROOT, 'browser_check.js'), 'utf8'));
    result = await fn(page);
  } catch (e) {
    result = { pass: false, error: String(e) };
  }
  await browser.close(); server.close();
  result.checks = (result.checks || []).concat(pre);
  result.page_errors = errors;
  result.passed = result.checks.filter(c => c.pass).length;
  result.total = result.checks.length;
  result.pass = !result.error && result.checks.every(c => c.pass) && errors.length === 0;
  result.browser = 'playwright-core 1.52 headless Chromium (ms-playwright chromium-1169)';
  result.url = url;
  console.log(JSON.stringify(result, null, 1));
  process.exit(result.pass ? 0 : 1);
})();
