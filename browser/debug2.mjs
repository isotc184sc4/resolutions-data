import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

await page.goto('http://127.0.0.1:5173/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2000);

// Get all links with href containing resolution
const resLinks = await page.locator('a[href*="resolution"]').all();
console.log('Resolution links found:', resLinks.length);
for (let i = 0; i < Math.min(5, resLinks.length); i++) {
  const href = await resLinks[i].getAttribute('href');
  const text = await resLinks[i].textContent();
  console.log(`  ${i}: ${text} -> ${href}`);
}

// Get all links
const allLinks = await page.locator('a').all();
console.log('\nAll links found:', allLinks.length);
for (let i = 0; i < Math.min(15, allLinks.length); i++) {
  const href = await allLinks[i].getAttribute('href');
  const text = await allLinks[i].textContent();
  console.log(`  ${i}: ${text} -> ${href}`);
}

await browser.close();
