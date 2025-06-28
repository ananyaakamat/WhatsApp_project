# Playwright Testing Best Practices Guide for AI Assistants

## Table of Contents

1. [Introduction](#introduction)
2. [Setup and Configuration](#setup-and-configuration)
3. [Page Object Model](#page-object-model)
4. [Test Organization and Structure](#test-organization-and-structure)
5. [Locator Strategies](#locator-strategies)
6. [Assertions and Waiting](#assertions-and-waiting)
7. [Test Data Management](#test-data-management)
8. [Cross-Browser Testing](#cross-browser-testing)
9. [Performance and Debugging](#performance-and-debugging)
10. [CI/CD Integration](#cicd-integration)
11. [Common Patterns and Anti-Patterns](#common-patterns-and-anti-patterns)
12. [Quick Reference Checklist](#quick-reference-checklist)

## Introduction

This guide provides comprehensive Playwright testing best practices specifically designed for AI assistants to understand and apply. It covers modern browser automation, testing patterns, accessibility testing, and performance optimization.

### Key Principles for AI Test Generation

- **Reliability**: Write stable, non-flaky tests that work consistently
- **Maintainability**: Create tests that are easy to update and modify
- **Readability**: Use clear, descriptive test code and comments
- **Efficiency**: Optimize for speed and resource usage
- **Coverage**: Test critical user journeys and edge cases

## Setup and Configuration

### Project Structure

```typescript
// Good: Well-organized project structure
project/
├── tests/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── registration.spec.ts
│   ├── e2e/
│   │   ├── checkout.spec.ts
│   │   └── search.spec.ts
│   ├── api/
│   │   └── user-api.spec.ts
│   └── visual/
│       └── homepage.spec.ts
├── pages/
│   ├── auth/
│   │   ├── login-page.ts
│   │   └── registration-page.ts
│   ├── common/
│   │   ├── header.ts
│   │   └── footer.ts
│   └── base-page.ts
├── fixtures/
│   ├── test-data.ts
│   └── custom-fixtures.ts
├── utils/
│   ├── test-helpers.ts
│   └── api-helpers.ts
├── playwright.config.ts
└── package.json

// Bad: Flat structure without organization
tests/
├── test1.spec.ts
├── test2.spec.ts
├── test3.spec.ts
├── page1.ts
├── page2.ts
└── helper.ts
```

### Configuration Best Practices

```typescript
// Good: Comprehensive Playwright configuration
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  // Test directory
  testDir: "./tests",

  // Test timeout and retry configuration
  timeout: 30000,
  expect: {
    timeout: 5000,
  },
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  // Reporter configuration
  reporter: [
    ["html"],
    ["json", { outputFile: "test-results.json" }],
    ["junit", { outputFile: "test-results.xml" }],
    process.env.CI ? ["github"] : ["list"],
  ],

  // Global test setup
  globalSetup: require.resolve("./utils/global-setup"),
  globalTeardown: require.resolve("./utils/global-teardown"),

  use: {
    // Base URL for tests
    baseURL: process.env.BASE_URL || "http://localhost:3000",

    // Browser context options
    headless: !!process.env.CI,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,

    // Tracing and debugging
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",

    // Locator options
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  // Browser projects for cross-browser testing
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
    {
      name: "mobile-chrome",
      use: { ...devices["Pixel 5"] },
    },
    {
      name: "mobile-safari",
      use: { ...devices["iPhone 12"] },
    },
  ],

  // Web server for testing
  webServer: {
    command: "npm run start",
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});

// Bad: Minimal configuration without proper setup
export default defineConfig({
  testDir: "./tests",
  use: {
    headless: true,
  },
});
```

## Page Object Model

### Base Page Implementation

```typescript
// Good: Well-structured base page with common functionality
// pages/base-page.ts
import { Page, Locator, expect } from "@playwright/test";

export abstract class BasePage {
  protected page: Page;
  protected url: string;

  constructor(page: Page, url: string = "") {
    this.page = page;
    this.url = url;
  }

  /**
   * Navigate to the page and wait for it to load
   */
  async goto(): Promise<void> {
    await this.page.goto(this.url);
    await this.waitForPageLoad();
  }

  /**
   * Wait for page to be fully loaded
   */
  async waitForPageLoad(): Promise<void> {
    await this.page.waitForLoadState("networkidle");
    await this.page.waitForLoadState("domcontentloaded");
  }

  /**
   * Take a screenshot of the current page
   */
  async screenshot(name: string): Promise<void> {
    await this.page.screenshot({
      path: `screenshots/${name}.png`,
      fullPage: true,
    });
  }

  /**
   * Wait for an element to be visible
   */
  async waitForVisible(locator: Locator): Promise<void> {
    await expect(locator).toBeVisible();
  }

  /**
   * Get page title
   */
  async getTitle(): Promise<string> {
    return await this.page.title();
  }

  /**
   * Check if current URL matches expected pattern
   */
  async verifyUrl(pattern: string | RegExp): Promise<void> {
    await expect(this.page).toHaveURL(pattern);
  }

  /**
   * Wait for API response
   */
  async waitForApiResponse(urlPattern: string | RegExp): Promise<void> {
    await this.page.waitForResponse(urlPattern);
  }

  /**
   * Handle alerts and dialogs
   */
  async acceptDialog(): Promise<void> {
    this.page.on("dialog", (dialog) => dialog.accept());
  }

  /**
   * Scroll element into view
   */
  async scrollIntoView(locator: Locator): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
  }
}

// Bad: Page without proper structure or reusable methods
export class Page {
  constructor(private page: any) {}

  async click(selector: string) {
    await this.page.click(selector);
  }
}
```

### Specific Page Implementation

```typescript
// Good: Well-structured page object with clear methods and locators
// pages/auth/login-page.ts
import { Page, Locator, expect } from "@playwright/test";
import { BasePage } from "../base-page";

export class LoginPage extends BasePage {
  // Locators defined as properties for reusability
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;
  readonly rememberMeCheckbox: Locator;
  readonly loadingSpinner: Locator;

  constructor(page: Page) {
    super(page, "/login");

    // Use descriptive, stable locators
    this.emailInput = page.getByLabel("Email address");
    this.passwordInput = page.getByLabel("Password");
    this.loginButton = page.getByRole("button", { name: "Sign in" });
    this.errorMessage = page.getByTestId("error-message");
    this.forgotPasswordLink = page.getByRole("link", {
      name: "Forgot password?",
    });
    this.rememberMeCheckbox = page.getByLabel("Remember me");
    this.loadingSpinner = page.getByTestId("loading-spinner");
  }

  /**
   * Perform login with email and password
   */
  async login(email: string, password: string): Promise<void> {
    await this.fillEmail(email);
    await this.fillPassword(password);
    await this.clickLoginButton();
    await this.waitForLoginComplete();
  }

  /**
   * Fill email field with validation
   */
  async fillEmail(email: string): Promise<void> {
    await this.emailInput.fill(email);
    await expect(this.emailInput).toHaveValue(email);
  }

  /**
   * Fill password field
   */
  async fillPassword(password: string): Promise<void> {
    await this.passwordInput.fill(password);
    // Don't validate password value for security
    await expect(this.passwordInput).toBeFocused();
  }

  /**
   * Click login button and wait for response
   */
  async clickLoginButton(): Promise<void> {
    // Wait for button to be enabled
    await expect(this.loginButton).toBeEnabled();

    // Click and wait for navigation or error
    await Promise.race([
      this.loginButton.click(),
      this.page.waitForURL("**/dashboard"),
      this.errorMessage.waitFor(),
    ]);
  }

  /**
   * Wait for login process to complete
   */
  async waitForLoginComplete(): Promise<void> {
    // Wait for loading spinner to disappear
    await this.loadingSpinner.waitFor({ state: "hidden" });

    // Verify either successful navigation or error display
    await Promise.race([
      expect(this.page).toHaveURL(/.*\/dashboard/),
      expect(this.errorMessage).toBeVisible(),
    ]);
  }

  /**
   * Get error message text
   */
  async getErrorMessage(): Promise<string> {
    await this.errorMessage.waitFor();
    return (await this.errorMessage.textContent()) || "";
  }

  /**
   * Toggle remember me checkbox
   */
  async toggleRememberMe(): Promise<void> {
    await this.rememberMeCheckbox.check();
    await expect(this.rememberMeCheckbox).toBeChecked();
  }

  /**
   * Click forgot password link
   */
  async clickForgotPassword(): Promise<void> {
    await this.forgotPasswordLink.click();
    await expect(this.page).toHaveURL(/.*\/forgot-password/);
  }

  /**
   * Verify login page is displayed
   */
  async verifyLoginPageDisplayed(): Promise<void> {
    await expect(this.emailInput).toBeVisible();
    await expect(this.passwordInput).toBeVisible();
    await expect(this.loginButton).toBeVisible();
    await expect(this.page).toHaveTitle(/.*Login.*/);
  }

  /**
   * Verify login form validation
   */
  async verifyFormValidation(): Promise<void> {
    // Try to submit empty form
    await this.loginButton.click();

    // Check for validation messages
    await expect(this.emailInput).toHaveAttribute("aria-invalid", "true");
    await expect(this.passwordInput).toHaveAttribute("aria-invalid", "true");
  }
}

// Bad: Page object without clear structure or proper locators
export class LoginPage {
  constructor(private page: any) {}

  async login(email: string, password: string) {
    await this.page.fill("#email", email); // Fragile CSS selector
    await this.page.fill("#password", password);
    await this.page.click(".submit-btn"); // Generic class selector
  }
}
```

## Test Organization and Structure

### Test Structure Best Practices

```typescript
// Good: Well-organized test with clear structure and descriptions
// tests/auth/login.spec.ts
import { test, expect } from "@playwright/test";
import { LoginPage } from "../../pages/auth/login-page";
import { DashboardPage } from "../../pages/dashboard/dashboard-page";
import { testData } from "../../fixtures/test-data";

test.describe("User Authentication", () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
    await loginPage.goto();
  });

  test.describe("Successful Login", () => {
    test("should login with valid credentials", async ({ page }) => {
      // Arrange
      const { email, password } = testData.validUser;

      // Act
      await loginPage.login(email, password);

      // Assert
      await expect(page).toHaveURL(/.*\/dashboard/);
      await expect(dashboardPage.welcomeMessage).toContainText("Welcome back");
      await expect(dashboardPage.userProfileMenu).toBeVisible();
    });

    test('should remember user when "Remember Me" is checked', async ({
      page,
      context,
    }) => {
      // Arrange
      const { email, password } = testData.validUser;

      // Act
      await loginPage.toggleRememberMe();
      await loginPage.login(email, password);

      // Verify session persistence
      const cookies = await context.cookies();
      const rememberCookie = cookies.find(
        (cookie) => cookie.name === "remember_token"
      );

      // Assert
      expect(rememberCookie).toBeDefined();
      expect(rememberCookie?.expires).toBeGreaterThan(Date.now() / 1000);
    });
  });

  test.describe("Failed Login Attempts", () => {
    test("should show error for invalid email", async () => {
      // Arrange
      const invalidCredentials = {
        email: "invalid@example.com",
        password: testData.validUser.password,
      };

      // Act
      await loginPage.login(
        invalidCredentials.email,
        invalidCredentials.password
      );

      // Assert
      const errorMessage = await loginPage.getErrorMessage();
      expect(errorMessage).toContain("Invalid email or password");
      await expect(loginPage.errorMessage).toBeVisible();
      await expect(loginPage.emailInput).toBeFocused();
    });

    test("should handle multiple failed attempts with rate limiting", async () => {
      // Arrange
      const invalidCredentials = {
        email: testData.validUser.email,
        password: "wrongpassword",
      };

      // Act - Attempt login multiple times
      for (let i = 0; i < 3; i++) {
        await loginPage.login(
          invalidCredentials.email,
          invalidCredentials.password
        );
        await loginPage.waitForVisible(loginPage.errorMessage);
      }

      // Fourth attempt should show rate limiting
      await loginPage.login(
        invalidCredentials.email,
        invalidCredentials.password
      );

      // Assert
      const errorMessage = await loginPage.getErrorMessage();
      expect(errorMessage).toContain("Too many failed attempts");
      await expect(loginPage.loginButton).toBeDisabled();
    });
  });

  test.describe("Form Validation", () => {
    test("should validate required fields", async () => {
      // Act
      await loginPage.verifyFormValidation();

      // Assert - Fields should be marked as invalid
      await expect(loginPage.emailInput).toHaveAttribute(
        "aria-invalid",
        "true"
      );
      await expect(loginPage.passwordInput).toHaveAttribute(
        "aria-invalid",
        "true"
      );
    });

    test("should validate email format", async () => {
      // Arrange
      const invalidEmails = [
        "invalid",
        "test@",
        "@example.com",
        "test..test@example.com",
      ];

      for (const email of invalidEmails) {
        // Act
        await loginPage.fillEmail(email);
        await loginPage.clickLoginButton();

        // Assert
        await expect(loginPage.emailInput).toHaveAttribute(
          "aria-invalid",
          "true"
        );

        // Clean up for next iteration
        await loginPage.emailInput.clear();
      }
    });
  });

  test.describe("Accessibility", () => {
    test("should be accessible to screen readers", async ({ page }) => {
      // Check for proper ARIA labels and roles
      await expect(loginPage.emailInput).toHaveAttribute("aria-label");
      await expect(loginPage.passwordInput).toHaveAttribute("aria-label");
      await expect(loginPage.loginButton).toHaveAttribute("role", "button");

      // Check for keyboard navigation
      await page.keyboard.press("Tab");
      await expect(loginPage.emailInput).toBeFocused();

      await page.keyboard.press("Tab");
      await expect(loginPage.passwordInput).toBeFocused();

      await page.keyboard.press("Tab");
      await expect(loginPage.loginButton).toBeFocused();
    });

    test("should have proper color contrast", async ({ page }) => {
      // Use axe-playwright for accessibility testing
      await page.goto("/login");

      // This would require @axe-core/playwright
      // const results = await page.accessibility.snapshot();
      // expect(results.violations).toHaveLength(0);
    });
  });
});

// Bad: Poorly organized test without clear structure
test("login test", async ({ page }) => {
  await page.goto("/login");
  await page.fill("#email", "test@example.com");
  await page.fill("#password", "password");
  await page.click("button");
  await expect(page).toHaveURL("/dashboard");
});
```

## Locator Strategies

### Modern Locator Best Practices

```typescript
// Good: Using semantic and stable locators
class ModernLocators {
  constructor(private page: Page) {}

  // Prefer user-facing locators
  getByRoleLocators() {
    return {
      // Buttons
      submitButton: this.page.getByRole("button", { name: "Submit" }),
      cancelButton: this.page.getByRole("button", { name: "Cancel" }),

      // Links
      homeLink: this.page.getByRole("link", { name: "Home" }),

      // Form controls
      emailInput: this.page.getByRole("textbox", { name: "Email" }),
      passwordInput: this.page.getByRole("textbox", { name: "Password" }),

      // Lists and items
      navigationMenu: this.page.getByRole("navigation"),
      menuItems: this.page.getByRole("menuitem"),
    };
  }

  // Use labels for form elements
  getByLabelLocators() {
    return {
      firstName: this.page.getByLabel("First name"),
      lastName: this.page.getByLabel("Last name"),
      birthDate: this.page.getByLabel("Date of birth"),
      newsletter: this.page.getByLabel("Subscribe to newsletter"),
    };
  }

  // Use test IDs for complex elements
  getByTestIdLocators() {
    return {
      userProfile: this.page.getByTestId("user-profile"),
      shoppingCart: this.page.getByTestId("shopping-cart"),
      productCard: this.page.getByTestId("product-card"),
      errorAlert: this.page.getByTestId("error-alert"),
    };
  }

  // Use text content for unique text
  getByTextLocators() {
    return {
      welcomeMessage: this.page.getByText("Welcome back!"),
      successMessage: this.page.getByText("Operation completed successfully"),
      productTitle: this.page.getByText("iPhone 14 Pro"),
    };
  }

  // Combine locators for precision
  combinedLocators() {
    return {
      // Locate within a specific section
      headerLoginButton: this.page
        .getByRole("banner")
        .getByRole("button", { name: "Login" }),

      // Filter by additional attributes
      primarySubmitButton: this.page
        .getByRole("button", { name: "Submit" })
        .filter({ hasText: "Primary" }),

      // Use nth for multiple matches
      firstProductCard: this.page.getByTestId("product-card").first(),

      // Chain locators
      userMenuLogout: this.page
        .getByTestId("user-menu")
        .getByRole("button", { name: "Logout" }),
    };
  }
}

// Bad: Fragile CSS and XPath selectors
class BadLocators {
  constructor(private page: Page) {}

  badSelectors() {
    return {
      // Fragile CSS selectors
      button: this.page.locator(".btn.btn-primary.submit-btn"),
      input: this.page.locator("div > form > input:nth-child(3)"),

      // Complex XPath
      complexXPath: this.page.locator(
        '//div[@class="container"]//button[contains(text(), "Submit")]'
      ),

      // ID-based selectors (can change)
      submitButton: this.page.locator("#submit-btn-123"),

      // Tag-based selectors (too generic)
      allButtons: this.page.locator("button"),
    };
  }
}
```

## Assertions and Waiting

### Modern Assertion Patterns

```typescript
// Good: Comprehensive assertion patterns with proper waiting
class ModernAssertions {
  constructor(private page: Page) {}

  async demonstrateAssertions() {
    const loginButton = this.page.getByRole("button", { name: "Login" });
    const errorMessage = this.page.getByTestId("error-message");
    const userProfile = this.page.getByTestId("user-profile");

    // Visibility assertions with auto-waiting
    await expect(loginButton).toBeVisible();
    await expect(errorMessage).toBeHidden();

    // Text content assertions
    await expect(this.page.getByRole("heading")).toHaveText("Welcome");
    await expect(errorMessage).toContainText("Invalid credentials");

    // Attribute assertions
    await expect(loginButton).toBeEnabled();
    await expect(loginButton).toHaveAttribute("type", "submit");
    await expect(loginButton).toHaveClass(/primary/);

    // URL and title assertions
    await expect(this.page).toHaveURL("/dashboard");
    await expect(this.page).toHaveTitle(/Dashboard/);

    // Form value assertions
    const emailInput = this.page.getByLabel("Email");
    await expect(emailInput).toHaveValue("user@example.com");
    await expect(emailInput).toBeEmpty(); // For empty fields

    // State assertions
    await expect(this.page.getByLabel("Remember me")).toBeChecked();
    await expect(loginButton).toBeFocused();

    // Count assertions
    await expect(this.page.getByRole("listitem")).toHaveCount(5);

    // Screenshot assertions for visual testing
    await expect(this.page).toHaveScreenshot("dashboard.png");
    await expect(userProfile).toHaveScreenshot("user-profile.png");
  }

  async demonstrateWaitingStrategies() {
    // Wait for element states
    await this.page.getByTestId("loading-spinner").waitFor({ state: "hidden" });
    await this.page.getByText("Content loaded").waitFor({ state: "visible" });

    // Wait for network responses
    await this.page.waitForResponse("/api/users");
    await this.page.waitForResponse(
      (response) =>
        response.url().includes("/api/") && response.status() === 200
    );

    // Wait for page events
    await this.page.waitForLoadState("networkidle");
    await this.page.waitForLoadState("domcontentloaded");

    // Wait for functions to return truthy values
    await this.page.waitForFunction(
      () => document.querySelector('[data-testid="chart"]')?.children.length > 0
    );

    // Wait for URL changes
    await this.page.waitForURL("**/dashboard");

    // Custom waiting with timeout
    await this.page.getByText("Processing...").waitFor({
      state: "hidden",
      timeout: 30000,
    });
  }

  async demonstrateConditionalLogic() {
    const cookieBanner = this.page.getByTestId("cookie-banner");

    // Handle optional elements
    if (await cookieBanner.isVisible()) {
      await this.page.getByRole("button", { name: "Accept Cookies" }).click();
      await cookieBanner.waitFor({ state: "hidden" });
    }

    // Count-based conditional logic
    const notifications = this.page.getByTestId("notification");
    const notificationCount = await notifications.count();

    if (notificationCount > 0) {
      for (let i = 0; i < notificationCount; i++) {
        await notifications
          .nth(i)
          .getByRole("button", { name: "Dismiss" })
          .click();
      }
    }

    // Wait for either of multiple conditions
    await Promise.race([
      expect(this.page.getByText("Success")).toBeVisible(),
      expect(this.page.getByText("Error")).toBeVisible(),
    ]);
  }
}

// Bad: Manual waits and unreliable assertions
class BadAssertions {
  constructor(private page: Page) {}

  async badPractices() {
    // Manual sleeps (unreliable)
    await this.page.wait(2000);

    // Checking existence instead of visibility
    const element = await this.page.$(".some-element");
    expect(element).toBeTruthy(); // Element might not be visible

    // Not waiting for dynamic content
    const text = await this.page.textContent(".dynamic-content");
    expect(text).toBe("Expected text"); // Might not be loaded yet

    // Generic error handling
    try {
      await this.page.click(".button");
    } catch (error) {
      // Ignoring specific error types
    }
  }
}
```

## Test Data Management

### Data-Driven Testing Patterns

```typescript
// Good: Comprehensive test data management
// fixtures/test-data.ts
export interface User {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role: "admin" | "user" | "moderator";
}

export interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}

export const testData = {
  users: {
    validUser: {
      email: "john.doe@example.com",
      password: "SecurePassword123!",
      firstName: "John",
      lastName: "Doe",
      role: "user" as const,
    },
    adminUser: {
      email: "admin@example.com",
      password: "AdminPassword123!",
      firstName: "Admin",
      lastName: "User",
      role: "admin" as const,
    },
    invalidUser: {
      email: "invalid@example.com",
      password: "wrongpassword",
      firstName: "Invalid",
      lastName: "User",
      role: "user" as const,
    },
  },

  products: {
    electronics: [
      {
        id: "prod-001",
        name: "iPhone 14 Pro",
        price: 999.99,
        category: "smartphones",
        inStock: true,
      },
      {
        id: "prod-002",
        name: "MacBook Pro",
        price: 2499.99,
        category: "laptops",
        inStock: false,
      },
    ],
  },

  // Test scenarios for data-driven testing
  loginScenarios: [
    {
      description: "valid credentials",
      email: "john.doe@example.com",
      password: "SecurePassword123!",
      expectedResult: "success",
      expectedUrl: "/dashboard",
    },
    {
      description: "invalid email",
      email: "invalid@example.com",
      password: "SecurePassword123!",
      expectedResult: "error",
      expectedMessage: "Invalid email or password",
    },
    {
      description: "empty password",
      email: "john.doe@example.com",
      password: "",
      expectedResult: "validation_error",
      expectedMessage: "Password is required",
    },
  ],

  // Form validation test data
  emailValidation: {
    valid: [
      "user@example.com",
      "test.email@domain.co.uk",
      "user+tag@example.org",
    ],
    invalid: [
      "invalid-email",
      "@example.com",
      "user@",
      "user..email@example.com",
    ],
  },
};

// Factory functions for generating test data
export class TestDataFactory {
  static createRandomUser(): User {
    const timestamp = Date.now();
    return {
      email: `user.${timestamp}@example.com`,
      password: "TestPassword123!",
      firstName: `FirstName${timestamp}`,
      lastName: `LastName${timestamp}`,
      role: "user",
    };
  }

  static createRandomProduct(): Product {
    const timestamp = Date.now();
    return {
      id: `prod-${timestamp}`,
      name: `Product ${timestamp}`,
      price: Math.random() * 1000,
      category: "electronics",
      inStock: Math.random() > 0.5,
    };
  }
}

// Bad: Hardcoded test data scattered throughout tests
test("login test", async ({ page }) => {
  await page.fill("#email", "hardcoded@example.com"); // Hardcoded
  await page.fill("#password", "password123"); // Insecure, hardcoded
  // ...
});
```

### Custom Fixtures for Test Setup

```typescript
// Good: Custom fixtures for reusable test setup
// fixtures/custom-fixtures.ts
import { test as base, Page } from "@playwright/test";
import { LoginPage } from "../pages/auth/login-page";
import { DashboardPage } from "../pages/dashboard/dashboard-page";
import { ApiHelper } from "../utils/api-helpers";
import { testData, TestDataFactory } from "./test-data";

interface CustomFixtures {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedUser: void;
  apiHelper: ApiHelper;
  testUser: typeof testData.users.validUser;
}

export const test = base.extend<CustomFixtures>({
  // Page object fixtures
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },

  // API helper fixture
  apiHelper: async ({ request }, use) => {
    const apiHelper = new ApiHelper(request);
    await use(apiHelper);
  },

  // Authenticated user fixture
  authenticatedUser: async ({ page, loginPage }, use) => {
    await loginPage.goto();
    await loginPage.login(
      testData.users.validUser.email,
      testData.users.validUser.password
    );
    await use();
  },

  // Random test user fixture
  testUser: async ({ apiHelper }, use) => {
    const user = TestDataFactory.createRandomUser();

    // Create user via API
    await apiHelper.createUser(user);

    await use(user);

    // Cleanup: Delete user after test
    await apiHelper.deleteUser(user.email);
  },
});

export { expect } from "@playwright/test";

// Usage in tests
test("dashboard should display user information", async ({
  authenticatedUser,
  dashboardPage,
}) => {
  // Test starts with user already authenticated
  await expect(dashboardPage.welcomeMessage).toBeVisible();
  await expect(dashboardPage.userProfile).toContainText(
    testData.users.validUser.firstName
  );
});

// Bad: Manual setup in every test
test("dashboard test", async ({ page }) => {
  // Repeated login code in every test
  await page.goto("/login");
  await page.fill("#email", "user@example.com");
  await page.fill("#password", "password");
  await page.click("button");
  await page.waitForURL("/dashboard");
  // Test logic...
});
```

## Cross-Browser Testing

### Browser-Specific Configurations

```typescript
// Good: Comprehensive cross-browser testing setup
// playwright.config.ts (browser projects section)
export default defineConfig({
  projects: [
    // Desktop browsers
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        // Chrome-specific settings
        launchOptions: {
          args: [
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor",
          ],
        },
      },
    },
    {
      name: "firefox",
      use: {
        ...devices["Desktop Firefox"],
        // Firefox-specific settings
        launchOptions: {
          firefoxUserPrefs: {
            "dom.webnotifications.enabled": false,
          },
        },
      },
    },
    {
      name: "webkit",
      use: {
        ...devices["Desktop Safari"],
        // WebKit-specific settings
      },
    },

    // Mobile browsers
    {
      name: "mobile-chrome",
      use: {
        ...devices["Pixel 5"],
        isMobile: true,
        hasTouch: true,
      },
    },
    {
      name: "mobile-safari",
      use: {
        ...devices["iPhone 12"],
        isMobile: true,
        hasTouch: true,
      },
    },

    // Tablet browsers
    {
      name: "tablet-chrome",
      use: {
        ...devices["iPad Pro"],
        isMobile: false,
        hasTouch: true,
      },
    },

    // Different viewport sizes
    {
      name: "desktop-large",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1920, height: 1080 },
      },
    },
    {
      name: "desktop-small",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1280, height: 720 },
      },
    },
  ],
});

// Browser-specific test implementation
class CrossBrowserTests {
  static async handleBrowserDifferences(page: Page, browserName: string) {
    switch (browserName) {
      case "webkit":
        // Safari-specific handling
        await page.addInitScript(() => {
          // Polyfills or Safari-specific code
        });
        break;

      case "firefox":
        // Firefox-specific handling
        await page
          .context()
          .grantPermissions(["clipboard-read", "clipboard-write"]);
        break;

      case "chromium":
        // Chrome-specific handling
        await page.context().clearCookies();
        break;
    }
  }

  static async detectMobileDevice(page: Page): Promise<boolean> {
    return await page.evaluate(() => {
      return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
      );
    });
  }

  static async handleTouchGestures(page: Page, element: Locator) {
    const isMobile = await this.detectMobileDevice(page);

    if (isMobile) {
      // Use touch gestures on mobile
      await element.tap();
    } else {
      // Use mouse clicks on desktop
      await element.click();
    }
  }
}

// Test with browser-specific logic
test.describe("Cross-browser functionality", () => {
  test("should handle file uploads across browsers", async ({
    page,
    browserName,
  }) => {
    const fileInput = page.getByLabel("Upload file");
    const testFile = "test-data/sample.pdf";

    // Browser-specific file upload handling
    if (browserName === "webkit") {
      // Safari requires different approach
      await fileInput.setInputFiles(testFile);
      await page.waitForTimeout(1000); // Safari needs extra time
    } else {
      await fileInput.setInputFiles(testFile);
    }

    await expect(page.getByText("File uploaded successfully")).toBeVisible();
  });

  test("should handle clipboard operations", async ({ page, browserName }) => {
    const textToCopy = "Test clipboard content";

    if (browserName === "firefox") {
      // Firefox requires explicit permission
      await page
        .context()
        .grantPermissions(["clipboard-read", "clipboard-write"]);
    }

    await page.evaluate((text) => {
      navigator.clipboard.writeText(text);
    }, textToCopy);

    const clipboardContent = await page.evaluate(() => {
      return navigator.clipboard.readText();
    });

    expect(clipboardContent).toBe(textToCopy);
  });
});

// Bad: No browser-specific considerations
test("file upload", async ({ page }) => {
  await page.setInputFiles("#file", "test.pdf"); // May fail on Safari
  // No browser-specific handling
});
```

## Performance and Debugging

### Performance Testing with Playwright

```typescript
// Good: Comprehensive performance testing
class PerformanceTests {
  static async measurePageLoadTime(page: Page): Promise<number> {
    const startTime = Date.now();
    await page.goto("/");
    await page.waitForLoadState("networkidle");
    return Date.now() - startTime;
  }

  static async measureInteractionTime(
    page: Page,
    action: () => Promise<void>
  ): Promise<number> {
    const startTime = Date.now();
    await action();
    return Date.now() - startTime;
  }

  static async captureNetworkMetrics(page: Page) {
    const responses: any[] = [];

    page.on("response", (response) => {
      responses.push({
        url: response.url(),
        status: response.status(),
        timing: response.timing(),
        size: response.headers()["content-length"],
      });
    });

    return responses;
  }

  static async analyzePagePerformance(page: Page) {
    // Capture performance metrics
    const metrics = await page.evaluate(() => {
      const navigation = performance.getEntriesByType(
        "navigation"
      )[0] as PerformanceNavigationTiming;
      const paint = performance.getEntriesByType("paint");

      return {
        // Navigation timing
        domContentLoaded:
          navigation.domContentLoadedEventEnd -
          navigation.domContentLoadedEventStart,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,

        // Paint timing
        firstPaint: paint.find((p) => p.name === "first-paint")?.startTime,
        firstContentfulPaint: paint.find(
          (p) => p.name === "first-contentful-paint"
        )?.startTime,

        // Resource timing
        totalResources: performance.getEntriesByType("resource").length,
      };
    });

    return metrics;
  }
}

// Performance test implementation
test.describe("Performance Tests", () => {
  test("homepage should load within acceptable time", async ({ page }) => {
    const loadTime = await PerformanceTests.measurePageLoadTime(page);

    expect(loadTime).toBeLessThan(3000); // 3 seconds threshold

    const metrics = await PerformanceTests.analyzePagePerformance(page);

    expect(metrics.firstContentfulPaint).toBeLessThan(1500); // 1.5 seconds
    expect(metrics.domContentLoaded).toBeLessThan(2000); // 2 seconds
  });

  test("search should respond quickly", async ({ page }) => {
    await page.goto("/search");

    const searchTime = await PerformanceTests.measureInteractionTime(
      page,
      async () => {
        await page.getByPlaceholder("Search...").fill("test query");
        await page.getByRole("button", { name: "Search" }).click();
        await page.waitForSelector('[data-testid="search-results"]');
      }
    );

    expect(searchTime).toBeLessThan(2000); // 2 seconds for search
  });

  test("should not have excessive network requests", async ({ page }) => {
    const responses = await PerformanceTests.captureNetworkMetrics(page);

    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");

    // Analyze network requests
    const apiCalls = responses.filter((r) => r.url.includes("/api/"));
    const largeResources = responses.filter(
      (r) => parseInt(r.size || "0") > 1024 * 1024 // > 1MB
    );

    expect(apiCalls.length).toBeLessThan(10); // Reasonable API call limit
    expect(largeResources.length).toBeLessThan(3); // Limit large resources
  });
});

// Debugging helpers
class DebuggingHelpers {
  static async capturePageState(page: Page, testName: string) {
    // Take screenshot
    await page.screenshot({
      path: `debug/${testName}-screenshot.png`,
      fullPage: true,
    });

    // Save page HTML
    const html = await page.content();
    require("fs").writeFileSync(`debug/${testName}-page.html`, html);

    // Capture console logs
    const logs = await page.evaluate(() => {
      return (window as any).testLogs || [];
    });
    require("fs").writeFileSync(
      `debug/${testName}-logs.json`,
      JSON.stringify(logs, null, 2)
    );
  }

  static async setupConsoleCapture(page: Page) {
    // Capture console messages
    page.on("console", (msg) => {
      console.log(`Console ${msg.type()}: ${msg.text()}`);
    });

    // Capture page errors
    page.on("pageerror", (error) => {
      console.error("Page error:", error.message);
    });

    // Capture failed requests
    page.on("requestfailed", (request) => {
      console.error(
        "Request failed:",
        request.url(),
        request.failure()?.errorText
      );
    });
  }

  static async waitForStableState(page: Page, timeout = 5000) {
    // Wait for no new network requests for a period
    let requestCount = 0;

    page.on("request", () => requestCount++);
    page.on("response", () => requestCount--);

    await page.waitForFunction(() => requestCount === 0, { timeout });
  }
}

// Bad: No performance considerations or debugging
test("simple test", async ({ page }) => {
  await page.goto("/");
  await page.click("button"); // No timing measurements
  // No error handling or debugging info
});
```

## CI/CD Integration

### GitHub Actions Configuration

```yaml
# Good: Comprehensive GitHub Actions workflow
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    # Run tests nightly
    - cron: '0 2 * * *'

env:
  NODE_VERSION: '18'

jobs:
  test:
    name: Run Playwright Tests
    timeout-minutes: 60
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        browser: [chromium, firefox, webkit]
        shard: [1/4, 2/4, 3/4, 4/4]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Install Playwright Browsers
      run: npx playwright install --with-deps ${{ matrix.browser }}

    - name: Start application
      run: |
        npm run build
        npm run start &
        npx wait-on http://localhost:3000

    - name: Run Playwright tests
      run: |
        npx playwright test --project=${{ matrix.browser }} --shard=${{ matrix.shard }}
      env:
        PLAYWRIGHT_BASE_URL: http://localhost:3000

    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: playwright-report-${{ matrix.browser }}-${{ matrix.shard }}
        path: |
          playwright-report/
          test-results/
        retention-days: 30

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      if: matrix.browser == 'chromium' && matrix.shard == '1/4'
      with:
        file: ./coverage/lcov.info

  visual-tests:
    name: Visual Regression Tests
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Install Playwright
      run: npx playwright install chromium

    - name: Run visual tests
      run: npx playwright test --project=visual

    - name: Upload visual test results
      uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: visual-test-failures
        path: test-results/

  mobile-tests:
    name: Mobile Device Tests
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Install Playwright
      run: npx playwright install chromium

    - name: Run mobile tests
      run: npx playwright test --project=mobile-chrome --project=mobile-safari

  security-tests:
    name: Security and Accessibility Tests
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'

    - name: Install dependencies
      run: |
        npm ci
        npm install @axe-core/playwright

    - name: Install Playwright
      run: npx playwright install chromium

    - name: Run accessibility tests
      run: npx playwright test --project=accessibility

    - name: Run security tests
      run: npx playwright test --project=security

# Bad: Minimal CI configuration
name: Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: npm test
```

## Common Patterns and Anti-Patterns

### Best Practices Summary

```typescript
// Good: Comprehensive test demonstrating all best practices
test.describe("E-commerce Checkout Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Setup with proper error handling
    await page.goto("/");
    await page.waitForLoadState("networkidle");
  });

  test("complete purchase journey", async ({ page, browserName }) => {
    // Use descriptive test names and clear test structure

    // Page object pattern
    const productPage = new ProductPage(page);
    const cartPage = new CartPage(page);
    const checkoutPage = new CheckoutPage(page);

    // Step 1: Select product
    await productPage.goto();
    await productPage.selectProduct("iPhone 14 Pro");
    await productPage.addToCart();

    // Verify cart update
    await expect(page.getByTestId("cart-count")).toHaveText("1");

    // Step 2: Review cart
    await cartPage.goto();
    await cartPage.verifyProductInCart("iPhone 14 Pro");
    await cartPage.proceedToCheckout();

    // Step 3: Complete checkout
    await checkoutPage.fillShippingInformation({
      firstName: "John",
      lastName: "Doe",
      address: "123 Main St",
      city: "New York",
      zipCode: "10001",
    });

    await checkoutPage.selectShippingMethod("standard");
    await checkoutPage.fillPaymentInformation({
      cardNumber: "4111111111111111",
      expiryDate: "12/25",
      cvv: "123",
    });

    // Handle browser-specific differences
    if (browserName === "webkit") {
      await page.waitForTimeout(1000); // Safari needs extra time
    }

    await checkoutPage.placeOrder();

    // Verify successful completion
    await expect(page).toHaveURL(/.*\/order-confirmation/);
    await expect(page.getByText("Order placed successfully")).toBeVisible();

    // Verify order details
    const orderNumber = await page.getByTestId("order-number").textContent();
    expect(orderNumber).toMatch(/^ORD-\d{8}$/);
  });

  test("should handle payment failures gracefully", async ({ page }) => {
    // Test error scenarios
    const checkoutPage = new CheckoutPage(page);

    await checkoutPage.goto();
    await checkoutPage.fillPaymentInformation({
      cardNumber: "4000000000000002", // Declined card
      expiryDate: "12/25",
      cvv: "123",
    });

    await checkoutPage.placeOrder();

    // Verify error handling
    await expect(page.getByText("Payment declined")).toBeVisible();
    await expect(page.getByTestId("payment-form")).toBeVisible();

    // Verify user can retry
    await checkoutPage.fillPaymentInformation({
      cardNumber: "4111111111111111", // Valid card
      expiryDate: "12/25",
      cvv: "123",
    });

    await checkoutPage.placeOrder();
    await expect(page).toHaveURL(/.*\/order-confirmation/);
  });
});

// Bad: Poor test structure and practices
test("checkout", async ({ page }) => {
  await page.goto("/");
  await page.click(".product"); // Fragile selector
  await page.click("#add-cart"); // Fragile selector
  await page.fill("#card", "4111111111111111"); // No verification
  await page.click(".submit"); // No waiting or verification
  // No assertions or error handling
});
```

## Quick Reference Checklist

### Test Structure ✅

- [ ] Use descriptive test and describe block names
- [ ] Follow AAA pattern (Arrange, Act, Assert)
- [ ] Group related tests with describe blocks
- [ ] Use beforeEach/afterEach for setup and cleanup
- [ ] Implement proper error handling and timeouts

### Locator Strategy ✅

- [ ] Prefer user-facing locators (getByRole, getByLabel, getByText)
- [ ] Use getByTestId for complex elements
- [ ] Avoid fragile CSS selectors and XPath
- [ ] Combine locators for precision when needed
- [ ] Use semantic HTML attributes for better locators

### Page Object Model ✅

- [ ] Create reusable page objects with clear methods
- [ ] Use a base page class for common functionality
- [ ] Define locators as class properties
- [ ] Include wait strategies in page methods
- [ ] Document complex page interactions

### Assertions and Waiting ✅

- [ ] Use auto-waiting assertions (expect().toBeVisible())
- [ ] Wait for specific conditions, not arbitrary timeouts
- [ ] Handle dynamic content with proper waiting
- [ ] Use conditional logic for optional elements
- [ ] Implement proper error state verification

### Cross-Browser Testing ✅

- [ ] Configure multiple browser projects
- [ ] Handle browser-specific differences
- [ ] Test on mobile and tablet devices
- [ ] Consider viewport size variations
- [ ] Test touch vs. mouse interactions

### Performance and Debugging ✅

- [ ] Implement performance monitoring
- [ ] Use tracing and screenshots for debugging
- [ ] Capture console logs and network requests
- [ ] Monitor resource loading and timing
- [ ] Set up proper error reporting

### CI/CD Integration ✅

- [ ] Configure parallel test execution
- [ ] Implement test sharding for large suites
- [ ] Set up proper artifact collection
- [ ] Use matrix strategies for browser testing
- [ ] Configure scheduled test runs

### Test Data Management ✅

- [ ] Use structured test data with TypeScript interfaces
- [ ] Implement data factories for dynamic data
- [ ] Use custom fixtures for test setup
- [ ] Separate test data from test logic
- [ ] Implement proper test data cleanup

This guide provides a comprehensive foundation for writing high-quality Playwright tests that are reliable, maintainable, and easily understood by AI assistants. It emphasizes modern practices, proper error handling, and scalable test architecture patterns.
