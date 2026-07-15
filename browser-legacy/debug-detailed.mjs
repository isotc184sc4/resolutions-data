import playwright from 'playwright';

const browser = await playwright.chromium.launch({ headless: true });
const page = await browser.newPage();

let consoleMessages = [];
page.on('console', msg => {
  const text = `[${msg.type()}] ${msg.text()}`;
  consoleMessages.push(text);
  console.log(text);
});

await page.goto('http://127.0.0.1:5173/', { waitUntil: 'networkidle' });

// Wait for Vue to hydrate and data to load
await page.waitForTimeout(3000);

// Check the actual state
const state = await page.evaluate(() => {
  return {
    appMounted: !!document.querySelector('#app [data-v-app]'),
    hasStdResults: !!document.querySelector('.std-results'),
    cardCount: document.querySelectorAll('.std-results__card').length,
    loadingContainer: !!document.querySelector('.loading-container'),
    skeletonCards: document.querySelectorAll('.skeleton-card').length,
    bodyHTML: document.body.innerHTML.substring(0, 1000)
  };
});

console.log('\n=== STATE CHECK ===');
console.log(JSON.stringify(state, null, 2));

console.log('\n=== CONSOLE MESSAGES ===');
consoleMessages.forEach(msg => console.log(msg));

await browser.close();
