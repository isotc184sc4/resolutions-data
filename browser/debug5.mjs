import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

// Capture console messages
const consoleLogs = [];
page.on('console', msg => {
  consoleLogs.push({ type: msg.type(), text: msg.text() });
});

// Capture errors
page.on('pageerror', err => {
  console.log('Page error:', err);
});

await page.goto('http://127.0.0.1:5173/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);

console.log('Console logs:');
consoleLogs.forEach(log => {
  console.log(`  [${log.type}] ${log.text}`);
});

// Check if data is loaded
const dataLoaded = await page.evaluate(() => {
  return window.__data !== undefined;
});
console.log(`Data loaded: ${dataLoaded}`);

// Check the app state
const appState = await page.evaluate(() => {
  const app = document.querySelector('#app');
  return {
    appExists: app !== null,
    appHTML: app ? app.innerHTML.substring(0, 200) : 'N/A'
  };
});
console.log('App state:', appState);

await browser.close();
