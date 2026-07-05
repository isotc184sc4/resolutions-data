import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

await page.goto('http://127.0.0.1:5173/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2000);

// Get all h1, h2 tags
const headings = await page.locator('h1, h2').all();
console.log('Headings found:', headings.length);
for (let i = 0; i < Math.min(5, headings.length); i++) {
  const text = await headings[i].textContent();
  console.log(`  ${i}: ${text}`);
}

// Get all links
const links = await page.locator('a').all();
console.log('\nLinks found:', links.length);
for (let i = 0; i < Math.min(10, links.length); i++) {
  const text = await links[i].textContent();
  const href = await links[i].getAttribute('href');
  console.log(`  ${i}: ${text} -> ${href}`);
}

// Get all buttons
const buttons = await page.locator('button').all();
console.log('\nButtons found:', buttons.length);
for (let i = 0; i < Math.min(5, buttons.length); i++) {
  const text = await buttons[i].textContent();
  console.log(`  ${i}: ${text}`);
}

// Take screenshot
await page.screenshot({ path: '/tmp/qa-screenshots/debug-home.png' });

await browser.close();
