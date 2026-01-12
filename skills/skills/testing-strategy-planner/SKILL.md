---
name: testing-strategy-planner
description: Comprehensive testing strategy and implementation guidance. Use this skill when planning test coverage, writing unit tests, integration tests, E2E tests, choosing testing frameworks, implementing TDD/BDD, mocking, test automation, or improving code quality through testing.
license: Apache-2.0
---

# Testing Strategy Planner

Expert guidance for creating comprehensive, maintainable testing strategies that ensure code quality and reliability.

## Testing Pyramid

```
        /\
       /  \      E2E Tests (10%)
      /____\     - Critical user flows
     /      \    - Slow, fragile
    /        \
   /  Integration \  (30%)
  /______________\  - API contracts
 /                \ - Database interactions
/   Unit Tests     \ (60%)
/__________________\ - Fast, isolated
```

## Test Types

### Unit Tests
**Purpose**: Test individual functions/classes in isolation

**Example (Jest):**
```javascript
describe('UserService', () => {
  it('should create user with valid data', () => {
    const user = userService.createUser({
      name: 'John',
      email: 'john@example.com'
    });
    expect(user.id).toBeDefined();
    expect(user.name).toBe('John');
  });

  it('should throw error for invalid email', () => {
    expect(() => {
      userService.createUser({ name: 'John', email: 'invalid' });
    }).toThrow('Invalid email');
  });
});
```

**Best Practices:**
- Test one thing per test
- Use descriptive test names
- Arrange-Act-Assert pattern
- Mock external dependencies

### Integration Tests
**Purpose**: Test how modules work together

**Example (Supertest):**
```javascript
describe('POST /api/users', () => {
  it('should create user and return 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@example.com' })
      .expect(201);
    
    expect(response.body).toHaveProperty('id');
    expect(response.body.email).toBe('john@example.com');
  });
});
```

### End-to-End Tests
**Purpose**: Test critical user flows

**Example (Playwright):**
```javascript
test('user can complete checkout flow', async ({ page }) => {
  await page.goto('https://shop.example.com');
  await page.click('[data-testid="product-1"]');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="cart"]');
  await page.click('[data-testid="checkout"]');
  await page.fill('[name="email"]', 'user@example.com');
  await page.click('[data-testid="place-order"]');
  await expect(page.locator('.success-message')).toBeVisible();
});
```

## Test-Driven Development (TDD)

**Red-Green-Refactor Cycle:**
1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while tests pass

**Example:**
```javascript
// 1. Write failing test (Red)
test('calculateTotal returns sum of prices', () => {
  const items = [{ price: 10 }, { price: 20 }];
  expect(calculateTotal(items)).toBe(30);
});

// 2. Write minimal code (Green)
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// 3. Refactor (if needed)
```

## Behavior-Driven Development (BDD)

**Given-When-Then Pattern:**
```javascript
describe('User Authentication', () => {
  given('a user with valid credentials', () => {
    when('they login with correct password', () => {
      then('they should be authenticated', () => {
        // Test implementation
      });
    });
  });
});
```

## Mocking and Stubbing

**When to Mock:**
- External APIs (weather, payment services)
- Database calls
- File system operations
- Time-dependent code

**Example (Jest):**
```javascript
// Mock external API
jest.mock('./paymentService');

test('should process payment', async () => {
  paymentService.charge.mockResolvedValue({ success: true });
  
  const result = await checkoutService.processPayment(userId, amount);
  
  expect(result.success).toBe(true);
  expect(paymentService.charge).toHaveBeenCalledWith(amount);
});
```

## Test Coverage

**Coverage Goals:**
- **Lines**: >80% (critical paths 100%)
- **Branches**: >75%
- **Functions**: >80%
- **Statements**: >80%

**Coverage Tools:**
```bash
# Jest
npm test -- --coverage

# Istanbul
nyc npm test

# Python pytest
pytest --cov=src --cov-report=html
```

**What NOT to Test:**
- Third-party libraries (they should be tested)
- Configuration files
- Simple getters/setters
- Auto-generated code

## Framework Recommendations

**JavaScript/TypeScript:**
- **Unit**: Jest, Vitest
- **Integration**: Supertest, MSW
- **E2E**: Playwright, Cypress
- **Mocking**: MSW, faker.js

**Python:**
- **Unit**: pytest, unittest
- **Integration**: pytest, requests-mock
- **E2E**: Playwright for Python
- **Mocking**: unittest.mock, pytest-mock

**Go:**
- **Testing**: testing package, testify
- **Mocking**: gomock, mockery
- **Fuzzing**: testing/fuzz

**Rust:**
- **Unit**: built-in test framework
- **Property-based**: proptest
- **Fuzzing**: cargo-fuzz

## Test Organization

**Structure:**
```
src/
  services/
    userService.ts
tests/
  unit/
    services/
      userService.test.ts
  integration/
    api/
      users.test.ts
  e2e/
    flows/
      checkout.spec.ts
```

**Naming Conventions:**
- Files: `*.test.ts`, `*.spec.ts`, `test_*.py`
- Tests: `should [expected behavior] when [state]`
- Describe blocks: Use feature/module names

## CI/CD Integration

**GitHub Actions Example:**
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3
```

## Testing Anti-Patterns

❌ **Don't:**
- Test implementation details (test behavior, not code)
- Write brittle tests (break on refactoring)
- Mock everything (test real interactions)
- Test multiple things in one test
- Ignore test failures
- Write tests after code (without TDD)

✅ **Do:**
- Test user-facing behavior
- Write isolated tests
- Use meaningful assertions
- Keep tests fast
- Maintain test code quality
- Run tests in CI/CD

## Testing Checklist

**Unit Tests:**
- [ ] Public methods tested
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] External dependencies mocked

**Integration Tests:**
- [ ] API contracts verified
- [ ] Database operations tested
- [ ] External service interactions tested

**E2E Tests:**
- [ ] Critical user flows covered
- [ ] Multiple browsers/devices
- [ ] Error scenarios tested

**General:**
- [ ] Tests run in CI/CD
- [ ] Coverage threshold met
- [ ] Tests are fast and reliable
- [ ] Test documentation exists

## Performance Testing

**Load Testing (k6):**
```javascript
import http from 'k6/http';
import { check } from 'k6';

export default function() {
  const res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
}
```

## Working with This Skill

Provide:
1. Programming language and framework
2. Type of application (API, web, mobile)
3. Current testing situation (coverage, frameworks)
4. Specific testing challenges
5. Quality requirements and constraints

This skill will help you create a comprehensive testing strategy.
