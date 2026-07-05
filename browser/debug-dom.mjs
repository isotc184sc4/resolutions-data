import playwright from 'playwright';

const browser = await playwright.chromium.launch({ headless: true });
const page = await browser.newPage();

page.on('console', msg => console.log(`[CONSOLE] ${msg.type()}: ${msg.text()}`));
page.on('response', res => {
  if (res.url().includes('/data/') || res.url().includes('resolutions')) {
    console.log(`[RESPONSE] ${res.status()} ${res.url()}`);
  }
});

await page.goto('http://127.0.0.1:5173/', { waitUntil: 'networkidle' });

// Wait a bit for Vue to hydrate
await page.waitForTimeout(2000);

// Check what's in the DOM
const html = await page.content();
console.log('\n=== CHECKING DOM ===');
console.log('Has .std-results:', html.includes('std-results'));
console.log('Has .std-results__card:', html.includes('std-results__card'));
console.log('Has resolution data:', html.includes('ISO/TC 184/SC 4'));

// Try to find any card-like elements
const cards = await page.locator('[class*="card"]').count();
console.log(`Found ${cards} elements with "card" in class`);

const results = await page.locator('[class*="results"]').count();
console.log(`Found ${results} elements with "results" in class`);

// Check if data was fetched
const dataCheck = await page.evaluate(() => {
  return {
    hasWindow: typeof window !== 'undefined',
    hasVue: typeof window.__VUE__ !== 'undefined',
    bodyHTML: document.body.innerHTML.substring(0, 500)
  };
});
console.log('\nData check:', dataCheck);

await browser.close();
