import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

await page.goto('http://127.0.0.1:5173/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);

// Take screenshot
await page.screenshot({ path: '/tmp/qa-screenshots/debug-home-full.png' });

// Get page content
const content = await page.content();
console.log('Page length:', content.length);

// Check for resolution data
if (content.includes('resolution')) {
  console.log('Page contains "resolution"');
}

// Get all divs with data attributes
const divs = await page.locator('div[data-id]').all();
console.log('Divs with data-id:', divs.length);

// Get all elements with href containing resolution
const elements = await page.locator('[href*="resolution"]').all();
console.log('Elements with href containing resolution:', elements.length);

// Get all router links
const routerLinks = await page.locator('router-link').all();
console.log('Router links:', routerLinks.length);
for (let i = 0; i < Math.min(5, routerLinks.length); i++) {
  const to = await routerLinks[i].getAttribute('to');
  const text = await routerLinks[i].textContent();
  console.log(`  ${i}: ${text} -> ${to}`);
}

await browser.close();
