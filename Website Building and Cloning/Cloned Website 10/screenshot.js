const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const url = require('url');

const VIEWPORTS = {
  desktop: { width: 1920, height: 1080 },
  laptop: { width: 1366, height: 768 },
  tablet: { width: 768, height: 1024 },
  mobile: { width: 375, height: 812 }
};

async function captureScreenshot(targetUrl, options = {}) {
  const {
    viewport = 'desktop',
    fullPage = true,
    selector = null,
    waitTime = 3000,
    outputDir = 'screenshots',
    retries = 3
  } = options;

  const browser = await chromium.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-web-security',
      '--allow-running-insecure-content'
    ]
  });
  const context = await browser.newContext({
    viewport: VIEWPORTS[viewport] || VIEWPORTS.desktop,
    deviceScaleFactor: 2,
    ignoreHTTPSErrors: true,
    bypassCSP: true
  });
  const page = await context.newPage();

  try {
    console.log(`Navigating to: ${targetUrl}`);
    
    let lastError;
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        await page.goto(targetUrl, {
          waitUntil: 'networkidle',
          timeout: 60000
        });
        break;
      } catch (err) {
        lastError = err;
        if (attempt < retries) {
          console.log(`Attempt ${attempt} failed, retrying...`);
          await page.waitForTimeout(2000);
        }
      }
    }
    if (lastError) throw lastError;

    await page.waitForTimeout(waitTime);

    if (fullPage) {
      await autoScroll(page);
    }

    const parsedUrl = new URL(targetUrl);
    const domain = parsedUrl.hostname.replace(/^www\./, '');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const folderPath = path.join(outputDir, domain);

    if (!fs.existsSync(folderPath)) {
      fs.mkdirSync(folderPath, { recursive: true });
    }

    let screenshotPath;
    if (selector) {
      const element = await page.$(selector);
      if (element) {
        screenshotPath = path.join(folderPath, `${timestamp}_${selector.replace(/[^a-zA-Z0-9]/g, '_')}.png`);
        await element.screenshot({ path: screenshotPath });
        console.log(`Element screenshot saved: ${screenshotPath}`);
      } else {
        console.log(`Selector "${selector}" not found. Taking full page screenshot.`);
        screenshotPath = path.join(folderPath, `${timestamp}_fullpage.png`);
        await page.screenshot({ path: screenshotPath, fullPage: true });
        console.log(`Full page screenshot saved: ${screenshotPath}`);
      }
    } else {
      screenshotPath = path.join(folderPath, `${timestamp}_fullpage.png`);
      await page.screenshot({ path: screenshotPath, fullPage: true });
      console.log(`Full page screenshot saved: ${screenshotPath}`);
    }

    return screenshotPath;

  } catch (error) {
    console.error('Screenshot failed:', error.message);
    throw error;
  } finally {
    await browser.close();
  }
}

async function autoScroll(page) {
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let totalHeight = 0;
      const distance = 300;
      const timer = setInterval(() => {
        const scrollHeight = document.body.scrollHeight;
        window.scrollBy(0, distance);
        totalHeight += distance;
        if (totalHeight >= scrollHeight || totalHeight > 50000) {
          clearInterval(timer);
          window.scrollTo(0, 0);
          resolve();
        }
      }, 50);
    });
  });
}

function parseArgs(args) {
  const options = {
    viewport: 'desktop',
    fullPage: true,
    selector: null,
    waitTime: 3000,
    outputDir: 'screenshots'
  };

  let url = null;

  for (let i = 2; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--viewport' && args[i + 1]) {
      options.viewport = args[++i];
    } else if (arg === '--selector' && args[i + 1]) {
      options.selector = args[++i];
    } else if (arg === '--wait' && args[i + 1]) {
      options.waitTime = parseInt(args[++i], 10);
    } else if (arg === '--output' && args[i + 1]) {
      options.outputDir = args[++i];
    } else if (arg === '--no-fullpage') {
      options.fullPage = false;
    } else if (!arg.startsWith('--')) {
      url = arg;
    }
  }

  return { url, options };
}

async function main() {
  const { url: targetUrl, options } = parseArgs(process.argv);

  if (!targetUrl) {
    console.log(`
Usage: node screenshot.js <url> [options]

Options:
  --viewport <type>    Desktop (default), laptop, tablet, mobile
  --selector <css>     Capture specific element (e.g., ".hero", "#header")
  --wait <ms>          Wait time in ms after load (default: 3000)
  --output <dir>       Output directory (default: screenshots)
  --no-fullpage        Capture only viewport

Examples:
  node screenshot.js https://example.com
  node screenshot.js https://example.com --viewport mobile
  node screenshot.js https://example.com --selector ".hero-section"
  node screenshot.js https://example.com --wait 5000 --viewport tablet
    `);
    process.exit(1);
  }

  try {
    await captureScreenshot(targetUrl, options);
  } catch (error) {
    process.exit(1);
  }
}

main();

module.exports = { captureScreenshot, VIEWPORTS };
