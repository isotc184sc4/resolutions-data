import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const screenshotDir = '/tmp/qa-screenshots';
if (!fs.existsSync(screenshotDir)) {
  fs.mkdirSync(screenshotDir, { recursive: true });
}

const results = [];
const BASE_URL = 'http://127.0.0.1:5173';

async function test(name, fn) {
  try {
    console.log(`\n🧪 Running: ${name}`);
    await fn();
    results.push({ test: name, status: 'PASS' });
    console.log(`✅ PASS: ${name}`);
  } catch (error) {
    results.push({ test: name, status: 'FAIL', error: error.message });
    console.log(`❌ FAIL: ${name}`);
    console.log(`   Error: ${error.message}`);
  }
}

async function runTests() {
  const browser = await chromium.launch({ 
    headless: true
  });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Test 1: Home page loads
  await test('Test 1: Home page loads', async () => {
    await page.goto(`${BASE_URL}/`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Verify ISO/TC 184/SC 4 branding in header
    const headerBrand = await page.locator('a:has-text("ISO/TC 184/SC 4")').first();
    if (!await headerBrand.isVisible()) {
      throw new Error('ISO/TC 184/SC 4 branding not visible');
    }
    
    // Verify hero section with title
    const heroTitle = await page.locator('h1:has-text("Industrial Decisions")').first();
    if (!await heroTitle.isVisible()) {
      throw new Error('Hero section title not visible');
    }
    
    // Verify resolution cards (router-link elements)
    const resolutionCards = await page.locator('.std-results__card').count();
    if (resolutionCards === 0) {
      throw new Error('No resolution cards found');
    }
    
    // Verify About link
    const aboutLink = await page.locator('a[href="/about"]').first();
    if (!await aboutLink.isVisible()) {
      throw new Error('About link not visible');
    }
    
    await page.screenshot({ path: `${screenshotDir}/01-home.png` });
  });

  // Test 2: About page loads
  await test('Test 2: About page loads and shows content', async () => {
    await page.goto(`${BASE_URL}/`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Click About link
    const aboutLink = await page.locator('a[href="/about"]').first();
    await aboutLink.click();
    await page.waitForTimeout(2000);
    
    // Verify URL
    if (!page.url().includes('/about')) {
      throw new Error(`URL not /about, got ${page.url()}`);
    }
    
    // Verify "About This Archive" heading
    const heading = await page.locator('h1, h2').filter({ hasText: /About|Archive/ }).first();
    if (!await heading.isVisible()) {
      throw new Error('About This Archive heading not visible');
    }
    
    // Verify Edoxen Format section
    const edoxenSection = await page.locator('text=Edoxen').first();
    if (!await edoxenSection.isVisible()) {
      throw new Error('Edoxen Format section not visible');
    }
    
    // Verify Action Types section
    const actionSection = await page.locator('text=Action').first();
    if (!await actionSection.isVisible()) {
      throw new Error('Action Types section not visible');
    }
    
    // Verify URN Identifiers section
    const urnSection = await page.locator('text=urn:iso:tc:184:sc:4:resolution').first();
    if (!await urnSection.isVisible()) {
      throw new Error('URN Identifiers section not visible');
    }
    
    // Verify Data Pipeline section
    const pipelineSection = await page.locator('text=Pipeline').first();
    if (!await pipelineSection.isVisible()) {
      throw new Error('Data Pipeline section not visible');
    }
    
    await page.screenshot({ path: `${screenshotDir}/02-about.png` });
  });

  // Test 3: Resolution detail shows URN
  await test('Test 3: Resolution detail shows URN', async () => {
    await page.goto(`${BASE_URL}/`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Click first resolution card
    const card = await page.locator('.std-results__card').first();
    await card.click();
    await page.waitForTimeout(2000);
    
    // Verify URN bar
    const urnBar = await page.locator('text=urn:iso:tc:184:sc:4:resolution').first();
    if (!await urnBar.isVisible()) {
      throw new Error('URN bar not visible');
    }
    
    // Verify copy button
    const copyBtn = await page.locator('button:has-text("Copy")').first();
    if (!await copyBtn.isVisible()) {
      throw new Error('Copy button not visible');
    }
    
    await page.screenshot({ path: `${screenshotDir}/03-resolution-detail.png` });
  });

  // Test 4: Meeting detail shows URN
  await test('Test 4: Meeting detail shows URN', async () => {
    await page.goto(`${BASE_URL}/meetings`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Click first meeting card
    const meeting = await page.locator('.std-results__card').first();
    await meeting.click();
    await page.waitForTimeout(2000);
    
    // Verify Meeting URN
    const urnBar = await page.locator('text=urn:iso:tc:184:sc:4:meeting').first();
    if (!await urnBar.isVisible()) {
      throw new Error('Meeting URN bar not visible');
    }
    
    await page.screenshot({ path: `${screenshotDir}/04-meeting-detail.png` });
  });

  // Test 5: Dark mode toggle
  await test('Test 5: Dark mode toggle works', async () => {
    await page.goto(`${BASE_URL}/`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Find and click dark mode toggle (first button in header)
    const buttons = await page.locator('button').all();
    if (buttons.length === 0) {
      throw new Error('No buttons found');
    }
    
    // Try to find the theme toggle button
    let toggle = null;
    for (const btn of buttons) {
      const ariaLabel = await btn.getAttribute('aria-label');
      if (ariaLabel && (ariaLabel.includes('dark') || ariaLabel.includes('theme'))) {
        toggle = btn;
        break;
      }
    }
    
    if (!toggle) {
      // Try first button if no aria-label found
      toggle = buttons[0];
    }
    
    await toggle.click();
    await page.waitForTimeout(500);
    
    // Check if dark mode is applied
    const html = await page.locator('html');
    const classList = await html.getAttribute('class');
    if (!classList.includes('dark')) {
      throw new Error('Dark mode class not applied');
    }
    
    await page.screenshot({ path: `${screenshotDir}/05-dark-mode.png` });
    
    // Navigate to about and verify dark mode persists
    const aboutLink = await page.locator('a[href="/about"]').first();
    await aboutLink.click();
    await page.waitForTimeout(2000);
    
    const htmlAbout = await page.locator('html');
    const classListAbout = await htmlAbout.getAttribute('class');
    if (!classListAbout.includes('dark')) {
      throw new Error('Dark mode not persisted on about page');
    }
    
    await page.screenshot({ path: `${screenshotDir}/06-dark-mode-about.png` });
  });

  // Test 6: Footer About link
  await test('Test 6: Footer About link', async () => {
    await page.goto(`${BASE_URL}/`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    
    // Scroll to footer
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);
    
    // Find About link in footer
    const footerAbout = await page.locator('footer a[href="/about"]').first();
    if (!await footerAbout.isVisible()) {
      throw new Error('About link not visible in footer');
    }
    
    await footerAbout.click();
    await page.waitForTimeout(2000);
    
    // Verify navigation to /about
    if (!page.url().includes('/about')) {
      throw new Error(`Footer link did not navigate to /about, got ${page.url()}`);
    }
  });

  await browser.close();

  // Print results
  console.log('\n\n📊 TEST RESULTS:');
  console.log('================');
  results.forEach(r => {
    const status = r.status === 'PASS' ? '✅' : '❌';
    console.log(`${status} ${r.test}`);
    if (r.error) {
      console.log(`   ${r.error}`);
    }
  });

  const passed = results.filter(r => r.status === 'PASS').length;
  const total = results.length;
  console.log(`\n${passed}/${total} tests passed`);
  console.log(`\nScreenshots saved to: ${screenshotDir}`);
}

runTests().catch(console.error);
