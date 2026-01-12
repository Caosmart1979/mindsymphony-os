# Playwright E2E Testing Quick Reference

## 🎯 Common Commands

### Basic Test Commands
```bash
# Run all tests
npm test

# Run on specific browser
npm run test:chromium    # Chrome/Edge
npm run test:firefox     # Firefox
npm run test:webkit      # Safari

# Run with visible browser (headed mode)
npm run test:headed

# Debug tests with Playwright Inspector
npm run test:debug

# View HTML report
npm run test:report
```

### Browser Management
```bash
# Install browsers
npm run test:install

# Force reinstall browsers
npx playwright install --force --with-deps

# Check installed browsers
npx playwright --version
```

## 📝 Test File Structure

### Basic Test Template
```typescript
import { test, expect } from '@playwright/test';

test.describe('Test Suite Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup before each test
  });

  test('test description', async ({ page }) => {
    // Test code here
  });

  test.afterEach(async ({ page }) => {
    // Cleanup after each test
  });
});
```

## 🎨 Common Selectors

```typescript
// By text
page.getByText('Submit')

// By role
page.getByRole('button', { name: 'Submit' })

// By ID
page.locator('#submit-button')

// By CSS selector
page.locator('button.submit')

// By data-testid
page.getByTestId('submit-button')

// By label (form inputs)
page.getByLabel('Username')
```

## ⚙️ Common Actions

```typescript
// Navigation
await page.goto('https://example.com')
await page.goForward()
await page.goBack()
await page.reload()

// Click
await page.click('button')
await page.getByText('Submit').click()

// Type
await page.fill('input[name="email"]', 'test@example.com')
await page.type('input[name="email"]', 'test@example.com')

// Select
await page.selectOption('select#country', 'US')

// Check/Uncheck
await page.check('input[type="checkbox"]')
await page.uncheck('input[type="checkbox"]')

// Upload
await page.setInputFiles('input[type="file"]', 'file.pdf')

// Hover
await page.hover('button')

# Wait
await page.waitForLoadState('networkidle')
await page.waitForTimeout(1000)
await page.waitForSelector('.loaded')
```

## 🧪 Assertions

```typescript
// Page title
await expect(page).toHaveTitle('Page Title')

// URL
await expect(page).toHaveURL('https://example.com')

# Element visibility
await expect(page.locator('.header')).toBeVisible()

// Text content
await expect(page.locator('h1')).toHaveText('Welcome')

// Element count
await expect(page.locator('li')).toHaveCount(5)

// Attribute value
await expect(page.locator('input')).toHaveAttribute('type', 'email')

// CSS class
await expect(page.locator('div')).toHaveClass(/active/)

// Value
await expect(page.locator('input')).toHaveValue('test@example.com')
```

## 🌐 API Testing

```typescript
test('API test', async ({ request }) => {
  // GET request
  const response = await request.get('https://api.example.com/users')
  
  // POST request
  const postResponse = await request.post('https://api.example.com/users', {
    data: {
      name: 'John Doe',
      email: 'john@example.com'
    }
  })

  // Assertions
  expect(response.status()).toBe(200)
  const data = await response.json()
  expect(data).toHaveProperty('id')
})
```

## 📸 Screenshots & Videos

```typescript
// Take screenshot
await page.screenshot({ path: 'screenshot.png' })
await page.screenshot({ 
  path: 'screenshot.png', 
  fullPage: true 
})

// Element screenshot
await page.locator('.header').screenshot({ path: 'header.png' })
```

## 🎭 Page Objects Pattern

```typescript
// pages/LoginPage.ts
class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.fill('input[name="email"]', email)
    await this.page.fill('input[name="password"]', password)
    await this.page.click('button[type="submit"]')
  }
}

// Test file
test('login test', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.login('user@example.com', 'password')
})
```

## 🐛 Debugging

```typescript
// Pause execution
await page.pause()

// Slow motion (in config)
use: {
  launchOptions: {
    slowMo: 1000 // 1 second delay
  }
}

// Trace viewer
npx playwright show-trace trace.zip
```

## 📊 Test Organization

```typescript
// Skip test
test.skip('skip this test', async ({ page }) => {
  // This test won't run
})

// Skip conditionally
test('skip on webkit', async ({ page, browserName }) => {
  test.skip(browserName === 'webkit', 'Not supported on WebKit')
  // Test code
})

// Only run this test
test.only('run only this test', async ({ page }) => {
  // Only this test will run
})

// Fixtures
test.use({ viewport: { width: 600, height: 800 } })
test('mobile viewport test', async ({ page }) => {
  // Test with mobile viewport
})
```

## 🎨 Best Practices

1. **Use data-testid** attributes for stable selectors
2. **Wait for elements** instead of using timeouts
3. **Use page objects** for complex interactions
4. **Keep tests independent** - don't rely on test execution order
5. **Use beforeEach/afterEach** for setup/teardown
6. **Descriptive test names** - explain what is being tested
7. **One assertion per test** for better debugging
8. **Use expect().toMatchSnapshot()** for visual regression

## 🚫 Common Pitfalls

1. ❌ Using CSS selectors that depend on implementation
2. ❌ Hard-coding timeouts
3. ❌ Testing third-party dependencies
4. ❌ Complex test logic
5. ❌ Fragile selectors (dynamic IDs, generated classes)
6. ❌ Not cleaning up test data

## ✅ Do's

1. ✅ Use data-testid attributes
2. ✅ Test user behavior, not implementation
3. ✅ Keep tests simple and focused
4. ✅ Use descriptive names
5. ✅ Mock external dependencies
6. ✅ Clean up after tests

## 📱 Mobile Testing

```typescript
// In playwright.config.ts
projects: [
  {
    name: 'Mobile Chrome',
    use: { ...devices['Pixel 5'] },
  },
  {
    name: 'Mobile Safari',
    use: { ...devices['iPhone 12'] },
  },
]
```

## 🌍 Multi-language Support

```typescript
test('localized content', async ({ page }) => {
  await page.goto('https://example.com')
  await page.getByRole('button', { name: /accept/i }).click()
  
  // Get by text with regex
  await expect(page.getByText(/welcome/i)).toBeVisible()
})
```

## 🔐 Authentication

```typescript
test.use({ storageState: 'auth.json' })

test('authenticated test', async ({ page }) => {
  // Already authenticated
  await page.goto('https://example.com/dashboard')
  await expect(page).toHaveURL(/dashboard/)
})
```

---

**For more details, see the full documentation:**
- [Playwright Docs](https://playwright.dev)
- [API Reference](https://playwright.dev/docs/api/class-playwright)
- [Best Practices](https://playwright.dev/docs/best-practices)
