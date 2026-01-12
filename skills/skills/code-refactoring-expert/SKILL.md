---
name: code-refactoring-expert
description: Expert guidance on refactoring code for improved maintainability, readability, and performance. Use this skill when cleaning up legacy code, reducing technical debt, applying design patterns, optimizing algorithms, improving code organization, or making code more testable and modular.
license: Apache-2.0
interop_metadata:
  skill_id: skills.code_refactoring_expert
  api_version: v1
  authentication: none
  rate_limit:
    requests_per_minute: 30
---

# Code Refactoring Expert

Expert guidance for transforming code into clean, maintainable, and efficient solutions while preserving functionality.

## Core Refactoring Principles

**The Golden Rules:**
1. **Preserve Behavior**: Refactoring should never change external behavior
2. **Small Steps**: Make incremental changes that can be easily verified
3. **Test Coverage**: Always have tests before refactoring
4. **Commit Often**: Each refactoring should be a separate, revertable commit

## Key Refactoring Techniques

### Extract Method
Break long functions into smaller, named pieces:

**Before:**
```javascript
function printOwing() {
  let outstanding = 0;
  console.log("********************");
  for (let o of orders) {
    outstanding += o.amount;
  }
  console.log(`name: ${customer.name}`);
  console.log(`amount: ${outstanding}`);
}
```

**After:**
```javascript
function printOwing() {
  printBanner();
  let outstanding = calculateOutstanding();
  printDetails(outstanding);
}
```

### Replace Conditional with Polymorphism
Eliminate complex switch statements:

**Before:**
```javascript
function calculatePay(employee) {
  switch (employee.type) {
    case "ENGINEER": return employee.monthlySalary;
    case "SALESPERSON": return employee.monthlySalary + employee.bonus;
    case "MANAGER": return employee.monthlySalary + employee.stockOptions;
  }
}
```

**After:**
```javascript
class Employee {
  calculatePay() { return this.monthlySalary; }
}
class Salesperson extends Employee {
  calculatePay() { return this.monthlySalary + this.bonus; }
}
```

### Extract Variable/Constant
Improve readability by naming expressions:

**Before:**
```javascript
if (platform.toUpperCase().indexOf("MAC") > -1 && browser.toUpperCase().indexOf("IE") > -1)
```

**After:**
```javascript
const isMacOs = platform.toUpperCase().includes("MAC");
const isIEBrowser = browser.toUpperCase().includes("IE");
if (isMacOs && isIEBrowser)
```

## Code Smells and Solutions

| Code Smell | Solution |
|------------|----------|
| Duplicated Code | Extract Method, Extract Class |
| Long Method | Extract Method |
| Large Class | Extract Class |
| Long Parameter List | Introduce Parameter Object |
| Divergent Change | Extract Class |
| Feature Envy | Move Method |
| Primitive Obsession | Replace Type Code with Class |
| Switch Statements | Replace with Polymorphism |

## Performance Optimizations

**Algorithm Selection:**
- Use hash maps for O(1) lookups instead of arrays O(n)
- Sort with appropriate algorithm
- Cache expensive computations

**Async Optimizations:**
```javascript
// Bad - sequential
await fetchUsers();
await fetchPosts();

// Good - parallel
await Promise.all([fetchUsers(), fetchPosts()]);
```

## Naming Conventions

- **Variables**: `userAge`, `totalPrice` (nouns)
- **Functions**: `calculateTotal()`, `validateEmail()` (verbs)
- **Booleans**: `isActive`, `hasPermission` (is/has/can/should)
- **Classes**: `UserManager`, `PaymentProcessor` (PascalCase nouns)

## Refactoring Workflow

1. **Identify** code that needs improvement
2. **Test** - ensure tests cover the code
3. **Refactor** - apply appropriate technique
4. **Verify** - run all tests
5. **Commit** - save the improvement

## Common Anti-Patterns

❌ **Don't:**
- Refactor without tests
- Change functionality along with structure
- Make large, sweeping changes
- Optimize prematurely

✅ **Do:**
- Keep changes small and focused
- Run tests frequently
- Improve readability as primary goal
- Document why changes were made

## Legacy Code Strategies

- **Sprout Method**: Add new behavior in new method
- **Wrap Method**: Wrap existing to add behavior
- Find injection points for testing
- Gradually increase coverage

## Working with This Skill

Provide:
1. The code that needs refactoring
2. Programming language
3. Specific issues or goals
4. Test coverage status
