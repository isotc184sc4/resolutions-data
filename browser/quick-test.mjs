import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

await page.goto('http://localhost:5202/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);

// Take screenshot
await page.screenshot({ path: '/tmp/qa-screenshots/test-page.png' });

// Get page content
const content = await page.content();
console.log(content.substring(0, 500));

await browser.close();
