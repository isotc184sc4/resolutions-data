import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

await page.goto('http://127.0.0.1:5173/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);

// Get page HTML
const html = await page.content();

// Check for std-results__card
if (html.includes('std-results__card')) {
  console.log('✓ Page contains std-results__card');
} else {
  console.log('✗ Page does NOT contain std-results__card');
}

// Check for resolution data
if (html.includes('resolution')) {
  console.log('✓ Page contains "resolution"');
} else {
  console.log('✗ Page does NOT contain "resolution"');
}

// Get all elements with class std-results__card
const cards = await page.locator('.std-results__card').count();
console.log(`Found ${cards} elements with class std-results__card`);

// Get all elements with class meeting-card
const meetingCards = await page.locator('.meeting-card').count();
console.log(`Found ${meetingCards} elements with class meeting-card`);

// Get all router-link elements
const routerLinks = await page.locator('router-link').count();
console.log(`Found ${routerLinks} router-link elements`);

// Get all a elements
const allLinks = await page.locator('a').count();
console.log(`Found ${allLinks} a elements`);

// Check if data is loaded
const isLoaded = await page.evaluate(() => {
  return document.querySelector('.std-results') !== null;
});
console.log(`std-results element exists: ${isLoaded}`);

// Get the std-results element
const stdResults = await page.locator('.std-results').count();
console.log(`Found ${stdResults} .std-results elements`);

// Take screenshot
await page.screenshot({ path: '/tmp/qa-screenshots/debug4.png' });

await browser.close();
