// Regenerates the main downloadable resume PDF from static/resume_pdf.html.
// Usage: node scripts/generate_static_resume_pdf.js
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(__dirname, '..');
const HTML_PATH = path.join(ROOT, 'static', 'resume_pdf.html');
const PDF_PATH = path.join(ROOT, 'static', 'Prashanth_Kumar_Kadasi_Resume.pdf');

(async () => {
  const html = fs.readFileSync(HTML_PATH, 'utf8');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: PDF_PATH,
    format: 'Letter',
    printBackground: true,
    margin: { top: '0px', bottom: '0px', left: '0px', right: '0px' },
  });
  await browser.close();
  console.log('Generated:', PDF_PATH);
})();
