# Unit Testing Best Practices Guide for AI Assistants

## Table of Contents
1. [Introduction](#introduction)
2. [Universal Testing Principles](#universal-testing-principles)
3. [Test Naming Conventions](#test-naming-conventions)
4. [Test Structure and Organization](#test-structure-and-organization)
5. [Assertion Best Practices](#assertion-best-practices)
6. [Test Data Management](#test-data-management)
7. [Mocking and Test Doubles](#mocking-and-test-doubles)
8. [Test Categories and Scope](#test-categories-and-scope)
9. [Common Anti-Patterns to Avoid](#common-anti-patterns-to-avoid)
10. [Language-Specific Examples](#language-specific-examples)
11. [CI/CD Integration](#cicd-integration)
12. [Quick Reference Checklist](#quick-reference-checklist)

## Introduction

This guide provides comprehensive unit testing best practices designed for AI assistants to understand and apply across multiple programming languages. It covers universal testing principles, language-agnostic patterns, and specific examples for Python, Java, and .NET/C#.

### Key Principles for AI Test Generation
- **Fast Execution**: Unit tests should run quickly (milliseconds)
- **Isolation**: Each test should be independent and not affect others
- **Repeatability**: Tests should produce consistent results every time
- **Self-Validating**: Tests should clearly indicate pass/fail status
- **Timely**: Tests should be written close to the production code they test
- **Clear Intent**: Test purpose should be immediately obvious from reading

## Universal Testing Principles

### The Three Laws of Test-Driven Development (TDD)
1. **First Law**: You may not write production code until you have written a failing unit test
2. **Second Law**: You may not write more of a unit test than is sufficient to fail
3. **Third Law**: You may not write more production code than is sufficient to pass the currently failing test

### F.I.R.S.T. Principles
- **Fast**: Tests should run quickly
- **Independent**: Tests should not depend on each other
- **Repeatable**: Tests should be repeatable in any environment
- **Self-Validating**: Tests should have a boolean output (pass/fail)
- **Timely**: Tests should be written just before the production code

### Test Pyramid Structure
```
    /\
   /  \    E2E Tests (Few)
  /____\
 /      \   Integration Tests (Some)
/_______\__ Unit Tests (Many)
```

## Test Naming Conventions

### Universal Naming Pattern
Use descriptive names that clearly communicate:
- **What** is being tested
- **When** (under what conditions)
- **Then** (expected behavior)

#### Recommended Patterns

**Method_Scenario_ExpectedBehavior**
```python
# Python
def test_withdraw_amount_greater_than_balance_raises_exception(self):
    pass

def test_calculate_discount_for_premium_customer_returns_twenty_percent(self):
    pass
```

```java
// Java
@Test
public void withdraw_AmountGreaterThanBalance_RaisesException() {
    // Test implementation
}

@Test
public void calculateDiscount_ForPremiumCustomer_ReturnsTwentyPercent() {
    // Test implementation
}
```

```csharp
// C#
[Test]
public void Withdraw_AmountGreaterThanBalance_ThrowsException()
{
    // Test implementation
}

[Test]
public void CalculateDiscount_ForPremiumCustomer_ReturnsTwentyPercent()
{
    // Test implementation
}
```

**Should_ExpectedBehavior_When_Scenario**
```python
# Python
def test_should_raise_exception_when_withdraw_amount_exceeds_balance(self):
    pass

def test_should_return_twenty_percent_discount_when_customer_is_premium(self):
    pass
```

**Given_When_Then Pattern**
```python
# Python
def test_given_premium_customer_when_calculating_discount_then_returns_twenty_percent(self):
    pass
```

## Test Structure and Organization

### AAA Pattern (Arrange, Act, Assert)
The most widely adopted pattern for structuring unit tests.

#### Python Example
```python
import unittest
from unittest.mock import Mock
from myapp.services import PaymentService
from myapp.models import Customer, Order

class TestPaymentService(unittest.TestCase):
    
    def test_process_payment_for_valid_order_returns_success(self):
        # Arrange
        payment_gateway = Mock()
        payment_gateway.charge.return_value = {"status": "success", "transaction_id": "123"}
        payment_service = PaymentService(payment_gateway)
        customer = Customer(id=1, name="John Doe", email="john@example.com")
        order = Order(id=100, customer=customer, total=50.00)
        
        # Act
        result = payment_service.process_payment(order)
        
        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.transaction_id, "123")
        payment_gateway.charge.assert_called_once_with(
            amount=50.00,
            customer_email="john@example.com"
        )
```

#### Java Example
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class PaymentServiceTest {
    
    @Mock
    private PaymentGateway paymentGateway;
    
    private PaymentService paymentService;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        paymentService = new PaymentService(paymentGateway);
    }
    
    @Test
    void processPayment_ForValidOrder_ReturnsSuccess() {
        // Arrange
        Customer customer = new Customer(1, "John Doe", "john@example.com");
        Order order = new Order(100, customer, 50.00);
        PaymentResult mockResult = new PaymentResult(true, "123");
        when(paymentGateway.charge(50.00, "john@example.com")).thenReturn(mockResult);
        
        // Act
        PaymentResult result = paymentService.processPayment(order);
        
        // Assert
        assertTrue(result.isSuccess());
        assertEquals("123", result.getTransactionId());
        verify(paymentGateway).charge(50.00, "john@example.com");
    }
}
```

#### C# Example
```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using MyApp.Services;
using MyApp.Models;

[TestClass]
public class PaymentServiceTests
{
    private Mock<IPaymentGateway> _paymentGatewayMock;
    private PaymentService _paymentService;
    
    [TestInitialize]
    public void Setup()
    {
        _paymentGatewayMock = new Mock<IPaymentGateway>();
        _paymentService = new PaymentService(_paymentGatewayMock.Object);
    }
    
    [TestMethod]
    public void ProcessPayment_ForValidOrder_ReturnsSuccess()
    {
        // Arrange
        var customer = new Customer(1, "John Doe", "john@example.com");
        var order = new Order(100, customer, 50.00m);
        var mockResult = new PaymentResult(true, "123");
        _paymentGatewayMock
            .Setup(x => x.Charge(50.00m, "john@example.com"))
            .Returns(mockResult);
        
        // Act
        var result = _paymentService.ProcessPayment(order);
        
        // Assert
        Assert.IsTrue(result.Success);
        Assert.AreEqual("123", result.TransactionId);
        _paymentGatewayMock.Verify(x => x.Charge(50.00m, "john@example.com"), Times.Once);
    }
}
```

### Test Class Organization

#### Group Related Tests
```python
# Python - Group by functionality
class TestUserRegistration(unittest.TestCase):
    """Tests for user registration functionality"""
    
    def test_register_with_valid_email_creates_user(self):
        pass
    
    def test_register_with_duplicate_email_raises_exception(self):
        pass
    
    def test_register_with_invalid_email_format_raises_exception(self):
        pass

class TestUserAuthentication(unittest.TestCase):
    """Tests for user authentication functionality"""
    
    def test_login_with_valid_credentials_returns_token(self):
        pass
    
    def test_login_with_invalid_password_raises_exception(self):
        pass
```

#### Use Nested Classes for Complex Scenarios
```java
// Java - Nested test classes for organization
class UserServiceTest {
    
    @Nested
    @DisplayName("User Registration")
    class UserRegistration {
        
        @Test
        @DisplayName("Should create user with valid email")
        void register_WithValidEmail_CreatesUser() {
            // Test implementation
        }
        
        @Test
        @DisplayName("Should throw exception with duplicate email")
        void register_WithDuplicateEmail_ThrowsException() {
            // Test implementation
        }
    }
    
    @Nested
    @DisplayName("User Authentication")
    class UserAuthentication {
        
        @Test
        @DisplayName("Should return token with valid credentials")
        void login_WithValidCredentials_ReturnsToken() {
            // Test implementation
        }
    }
}
```

## Assertion Best Practices

### Use Descriptive AssertionsAlways provide clear, descriptive assertion messages that explain what went wrong.

#### Python Examples
```python
# Good: Clear assertion messages
def test_calculate_discount_for_premium_customer_returns_correct_amount(self):
    # Arrange
    customer = Customer(membership_type="premium")
    order = Order(total=100.00)
    
    # Act
    discount = calculate_discount(customer, order)
    
    # Assert
    self.assertEqual(
        discount, 20.00,
        f"Expected 20% discount for premium customer, but got {discount}"
    )
    self.assertIsInstance(
        discount, float,
        "Discount should be returned as a float value"
    )

# Bad: Unclear assertion messages
def test_discount_calculation(self):
    customer = Customer(membership_type="premium")
    order = Order(total=100.00)
    discount = calculate_discount(customer, order)
    self.assertEqual(discount, 20.00)  # No message - unclear what failed
```

#### Java Examples
```java
// Good: Clear assertion messages with AssertJ
@Test
void calculateDiscount_ForPremiumCustomer_ReturnsCorrectAmount() {
    // Arrange
    Customer customer = new Customer(MembershipType.PREMIUM);
    Order order = new Order(100.00);
    
    // Act
    double discount = discountCalculator.calculate(customer, order);
    
    // Assert
    assertThat(discount)
        .as("Premium customer should receive 20% discount")
        .isEqualTo(20.00);
    assertThat(discount)
        .as("Discount should be a positive value")
        .isPositive();
}

// Good: Clear assertion messages with JUnit 5
@Test
void calculateDiscount_ForPremiumCustomer_ReturnsCorrectAmount() {
    // Arrange
    Customer customer = new Customer(MembershipType.PREMIUM);
    Order order = new Order(100.00);
    
    // Act
    double discount = discountCalculator.calculate(customer, order);
    
    // Assert
    assertEquals(20.00, discount, 
        "Premium customer should receive 20% discount");
    assertTrue(discount > 0, 
        "Discount should be a positive value");
}
```

#### C# Examples
```csharp
// Good: Clear assertion messages with FluentAssertions
[TestMethod]
public void CalculateDiscount_ForPremiumCustomer_ReturnsCorrectAmount()
{
    // Arrange
    var customer = new Customer(MembershipType.Premium);
    var order = new Order(100.00m);
    
    // Act
    var discount = _discountCalculator.Calculate(customer, order);
    
    // Assert
    discount.Should().Be(20.00m, "premium customer should receive 20% discount");
    discount.Should().BePositive("discount should be a positive value");
}

// Good: Clear assertion messages with MSTest
[TestMethod]
public void CalculateDiscount_ForPremiumCustomer_ReturnsCorrectAmount()
{
    // Arrange
    var customer = new Customer(MembershipType.Premium);
    var order = new Order(100.00m);
    
    // Act
    var discount = _discountCalculator.Calculate(customer, order);
    
    // Assert
    Assert.AreEqual(20.00m, discount, 
        "Premium customer should receive 20% discount");
    Assert.IsTrue(discount > 0, 
        "Discount should be a positive value");
}
```

### One Logical Assertion Per Test
Each test should verify one specific behavior or outcome.

```python
# Good: Single logical assertion
def test_user_registration_creates_user_with_correct_email(self):
    # Arrange
    email = "test@example.com"
    
    # Act
    user = register_user(email, "password123")
    
    # Assert
    self.assertEqual(user.email, email)

def test_user_registration_creates_user_with_hashed_password(self):
    # Arrange
    password = "password123"
    
    # Act
    user = register_user("test@example.com", password)
    
    # Assert
    self.assertNotEqual(user.password, password)
    self.assertTrue(password_hasher.verify(password, user.password))

# Bad: Multiple unrelated assertions
def test_user_registration(self):
    user = register_user("test@example.com", "password123")
    self.assertEqual(user.email, "test@example.com")  # Testing email
    self.assertNotEqual(user.password, "password123")  # Testing password
    self.assertIsNotNone(user.created_at)  # Testing timestamp
    self.assertTrue(user.is_active)  # Testing status
```

## Test Data Management

### Use Test Data Builders for Complex Objects

#### Python Example
```python
class CustomerBuilder:
    def __init__(self):
        self.id = 1
        self.name = "John Doe"
        self.email = "john@example.com"
        self.membership_type = "standard"
        self.is_active = True
    
    def with_id(self, customer_id):
        self.id = customer_id
        return self
    
    def with_email(self, email):
        self.email = email
        return self
    
    def as_premium_member(self):
        self.membership_type = "premium"
        return self
    
    def as_inactive(self):
        self.is_active = False
        return self
    
    def build(self):
        return Customer(
            id=self.id,
            name=self.name,
            email=self.email,
            membership_type=self.membership_type,
            is_active=self.is_active
        )

# Usage in tests
def test_premium_customer_gets_discount(self):
    # Arrange
    customer = (CustomerBuilder()
                .with_email("premium@example.com")
                .as_premium_member()
                .build())
    
    # Act & Assert
    discount = calculate_discount(customer, Order(100.00))
    self.assertEqual(discount, 20.00)
```

#### Java Example
```java
public class CustomerTestDataBuilder {
    private int id = 1;
    private String name = "John Doe";
    private String email = "john@example.com";
    private MembershipType membershipType = MembershipType.STANDARD;
    private boolean isActive = true;
    
    public CustomerTestDataBuilder withId(int id) {
        this.id = id;
        return this;
    }
    
    public CustomerTestDataBuilder withEmail(String email) {
        this.email = email;
        return this;
    }
    
    public CustomerTestDataBuilder asPremiumMember() {
        this.membershipType = MembershipType.PREMIUM;
        return this;
    }
    
    public CustomerTestDataBuilder asInactive() {
        this.isActive = false;
        return this;
    }
    
    public Customer build() {
        return new Customer(id, name, email, membershipType, isActive);
    }
}

// Usage in tests
@Test
void premiumCustomer_GetsDiscount() {
    // Arrange
    Customer customer = new CustomerTestDataBuilder()
        .withEmail("premium@example.com")
        .asPremiumMember()
        .build();
    
    // Act & Assert
    double discount = discountCalculator.calculate(customer, new Order(100.00));
    assertEquals(20.00, discount);
}
```

### Use Parameterized Tests for Multiple Scenarios

#### Python Example
```python
import pytest

class TestDiscountCalculation:
    
    @pytest.mark.parametrize("membership_type,order_total,expected_discount", [
        ("standard", 100.00, 0.00),
        ("premium", 100.00, 20.00),
        ("vip", 100.00, 30.00),
        ("premium", 50.00, 10.00),
        ("vip", 200.00, 60.00),
    ])
    def test_calculate_discount_for_different_membership_types(
        self, membership_type, order_total, expected_discount
    ):
        # Arrange
        customer = Customer(membership_type=membership_type)
        order = Order(total=order_total)
        
        # Act
        discount = calculate_discount(customer, order)
        
        # Assert
        assert discount == expected_discount
```

#### Java Example
```java
@ParameterizedTest
@CsvSource({
    "STANDARD, 100.00, 0.00",
    "PREMIUM, 100.00, 20.00",
    "VIP, 100.00, 30.00",
    "PREMIUM, 50.00, 10.00",
    "VIP, 200.00, 60.00"
})
void calculateDiscount_ForDifferentMembershipTypes_ReturnsCorrectAmount(
    MembershipType membershipType, double orderTotal, double expectedDiscount) {
    
    // Arrange
    Customer customer = new Customer(membershipType);
    Order order = new Order(orderTotal);
    
    // Act
    double discount = discountCalculator.calculate(customer, order);
    
    // Assert
    assertEquals(expectedDiscount, discount);
}
```

#### C# Example
```csharp
[DataTestMethod]
[DataRow(MembershipType.Standard, 100.00, 0.00)]
[DataRow(MembershipType.Premium, 100.00, 20.00)]
[DataRow(MembershipType.Vip, 100.00, 30.00)]
[DataRow(MembershipType.Premium, 50.00, 10.00)]
[DataRow(MembershipType.Vip, 200.00, 60.00)]
public void CalculateDiscount_ForDifferentMembershipTypes_ReturnsCorrectAmount(
    MembershipType membershipType, double orderTotal, double expectedDiscount)
{
    // Arrange
    var customer = new Customer(membershipType);
    var order = new Order(orderTotal);
    
    // Act
    var discount = _discountCalculator.Calculate(customer, order);
    
    // Assert
    Assert.AreEqual(expectedDiscount, discount);
}
```## Mocking and Test Doubles

### Types of Test Doubles

#### Dummy Objects
Objects passed around but never actually used (usually just to fill parameter lists).

#### Fake Objects
Working implementations with simplified functionality (e.g., in-memory database).

#### Stubs
Provide canned answers to calls made during the test.

#### Spies
Stubs that record information about how they were called.

#### Mocks
Objects pre-programmed with expectations about calls they will receive.

### Mocking Best Practices

#### Python with unittest.mock
```python
from unittest.mock import Mock, patch, MagicMock
import unittest

class TestEmailService(unittest.TestCase):
    
    def test_send_email_calls_smtp_gateway_with_correct_parameters(self):
        # Arrange
        smtp_gateway = Mock()
        email_service = EmailService(smtp_gateway)
        recipient = "test@example.com"
        subject = "Test Subject"
        body = "Test Body"
        
        # Act
        email_service.send_email(recipient, subject, body)
        
        # Assert
        smtp_gateway.send.assert_called_once_with(
            to=recipient,
            subject=subject,
            body=body
        )
    
    def test_send_email_handles_smtp_exception_gracefully(self):
        # Arrange
        smtp_gateway = Mock()
        smtp_gateway.send.side_effect = SMTPException("Connection failed")
        email_service = EmailService(smtp_gateway)
        
        # Act & Assert
        with self.assertRaises(EmailDeliveryException):
            email_service.send_email("test@example.com", "Subject", "Body")
    
    @patch('myapp.services.datetime')
    def test_send_email_logs_timestamp_correctly(self, mock_datetime):
        # Arrange
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        smtp_gateway = Mock()
        email_service = EmailService(smtp_gateway)
        
        # Act
        email_service.send_email("test@example.com", "Subject", "Body")
        
        # Assert
        mock_datetime.now.assert_called_once()
        # Additional assertions for logging behavior
```

#### Java with Mockito
```java
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

class EmailServiceTest {
    
    @Mock
    private SmtpGateway smtpGateway;
    
    @InjectMocks
    private EmailService emailService;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    @Test
    void sendEmail_CallsSmtpGatewayWithCorrectParameters() {
        // Arrange
        String recipient = "test@example.com";
        String subject = "Test Subject";
        String body = "Test Body";
        
        // Act
        emailService.sendEmail(recipient, subject, body);
        
        // Assert
        verify(smtpGateway).send(
            argThat(email -> 
                email.getTo().equals(recipient) &&
                email.getSubject().equals(subject) &&
                email.getBody().equals(body)
            )
        );
    }
    
    @Test
    void sendEmail_HandlesSmtpExceptionGracefully() {
        // Arrange
        when(smtpGateway.send(any(Email.class)))
            .thenThrow(new SmtpException("Connection failed"));
        
        // Act & Assert
        assertThrows(EmailDeliveryException.class, () -> 
            emailService.sendEmail("test@example.com", "Subject", "Body")
        );
    }
    
    @Test
    void sendEmail_RetriesOnFailure() {
        // Arrange
        when(smtpGateway.send(any(Email.class)))
            .thenThrow(new SmtpException("Temporary failure"))
            .thenReturn(new SendResult(true, "123"));
        
        // Act
        boolean result = emailService.sendEmail("test@example.com", "Subject", "Body");
        
        // Assert
        assertTrue(result);
        verify(smtpGateway, times(2)).send(any(Email.class));
    }
}
```

#### C# with Moq
```csharp
using Moq;
using Microsoft.VisualStudio.TestTools.UnitTesting;

[TestClass]
public class EmailServiceTests
{
    private Mock<ISmtpGateway> _smtpGatewayMock;
    private EmailService _emailService;
    
    [TestInitialize]
    public void Setup()
    {
        _smtpGatewayMock = new Mock<ISmtpGateway>();
        _emailService = new EmailService(_smtpGatewayMock.Object);
    }
    
    [TestMethod]
    public void SendEmail_CallsSmtpGatewayWithCorrectParameters()
    {
        // Arrange
        var recipient = "test@example.com";
        var subject = "Test Subject";
        var body = "Test Body";
        
        // Act
        _emailService.SendEmail(recipient, subject, body);
        
        // Assert
        _smtpGatewayMock.Verify(x => x.Send(
            It.Is<Email>(e => 
                e.To == recipient && 
                e.Subject == subject && 
                e.Body == body
            )
        ), Times.Once);
    }
    
    [TestMethod]
    public void SendEmail_HandlesSmtpExceptionGracefully()
    {
        // Arrange
        _smtpGatewayMock
            .Setup(x => x.Send(It.IsAny<Email>()))
            .Throws(new SmtpException("Connection failed"));
        
        // Act & Assert
        Assert.ThrowsException<EmailDeliveryException>(() =>
            _emailService.SendEmail("test@example.com", "Subject", "Body")
        );
    }
    
    [TestMethod]
    public void SendEmail_RetriesOnFailure()
    {
        // Arrange
        _smtpGatewayMock
            .SetupSequence(x => x.Send(It.IsAny<Email>()))
            .Throws(new SmtpException("Temporary failure"))
            .Returns(new SendResult(true, "123"));
        
        // Act
        var result = _emailService.SendEmail("test@example.com", "Subject", "Body");
        
        // Assert
        Assert.IsTrue(result);
        _smtpGatewayMock.Verify(x => x.Send(It.IsAny<Email>()), Times.Exactly(2));
    }
}
```

### Mocking Guidelines

#### Mock Interfaces, Not Concrete Classes
```python
# Good: Mock the interface/protocol
class PaymentGateway(Protocol):
    def charge(self, amount: float, customer_email: str) -> PaymentResult:
        ...

def test_payment_processing():
    payment_gateway = Mock(spec=PaymentGateway)
    # Test implementation

# Bad: Mock concrete implementation
def test_payment_processing():
    payment_gateway = Mock(spec=StripePaymentGateway)  # Too specific
    # Test implementation
```

#### Don't Mock What You Don't Own
```python
# Good: Create a wrapper for external dependencies
class DatabaseAdapter:
    def __init__(self, db_connection):
        self._connection = db_connection
    
    def get_user(self, user_id: int) -> Optional[User]:
        # Wrapper around third-party DB library
        pass

def test_user_service():
    db_adapter = Mock(spec=DatabaseAdapter)  # Mock your wrapper
    db_adapter.get_user.return_value = User(id=1, name="John")
    # Test implementation

# Bad: Mock third-party library directly
def test_user_service():
    db_connection = Mock(spec=psycopg2.connection)  # Don't mock external libs
    # Test implementation
```

## Test Categories and Scope

### Unit Tests
- Test individual components in isolation
- Fast execution (milliseconds)
- No external dependencies (database, network, file system)
- High code coverage

### Integration Tests
- Test interaction between components
- Moderate execution time (seconds)
- May use external dependencies
- Focus on integration points

### End-to-End Tests
- Test complete user scenarios
- Slower execution (minutes)
- Use real external dependencies
- Focus on business workflows

### Test Scope Guidelines

#### What to Unit Test
```python
# Good: Test business logic
def test_calculate_shipping_cost_for_domestic_delivery():
    # Test pure business logic
    pass

def test_validate_email_format_returns_false_for_invalid_email():
    # Test validation logic
    pass

def test_apply_discount_reduces_total_by_correct_percentage():
    # Test calculation logic
    pass
```

#### What NOT to Unit Test
```python
# Don't test: Framework code, getters/setters, trivial logic
def test_get_name_returns_name(self):  # Don't test simple getters
    user = User("John")
    assert user.get_name() == "John"  # Trivial test

def test_django_orm_save_method(self):  # Don't test framework code
    user = User.objects.create(name="John")  # Testing Django, not your code
    assert user.id is not None
```## Common Anti-Patterns to Avoid

### The Ice Cream Cone Anti-Pattern
Avoid having more UI tests than integration tests, and more integration tests than unit tests.

```
     /\      
    /  \     UI Tests (Avoid having too many)
   /____\    
  /      \   Integration Tests (Some)
 /        \  
/__________\ Unit Tests (Many - The foundation)
```

### Testing Implementation Details
```python
# Bad: Testing internal implementation
def test_user_service_calls_repository_save_method(self):
    repository = Mock()
    user_service = UserService(repository)
    user = User(name="John")
    
    user_service.create_user(user)
    
    # Bad: Testing that specific method was called
    repository.save.assert_called_once_with(user)

# Good: Testing behavior/outcome
def test_user_service_creates_user_successfully(self):
    repository = Mock()
    repository.save.return_value = User(id=1, name="John")
    user_service = UserService(repository)
    user = User(name="John")
    
    result = user_service.create_user(user)
    
    # Good: Testing the outcome
    self.assertIsNotNone(result.id)
    self.assertEqual(result.name, "John")
```

### Over-Mocking
```python
# Bad: Mocking everything
def test_order_total_calculation(self):
    item1 = Mock()
    item1.price = 10.00
    item2 = Mock()
    item2.price = 20.00
    order = Mock()
    order.items = [item1, item2]
    
    calculator = OrderCalculator()
    total = calculator.calculate_total(order)
    
    self.assertEqual(total, 30.00)

# Good: Use real objects for simple data
def test_order_total_calculation(self):
    item1 = OrderItem(name="Item 1", price=10.00)
    item2 = OrderItem(name="Item 2", price=20.00)
    order = Order(items=[item1, item2])
    
    calculator = OrderCalculator()
    total = calculator.calculate_total(order)
    
    self.assertEqual(total, 30.00)
```

### Test Interdependence
```python
# Bad: Tests that depend on each other
class TestUserManagement(unittest.TestCase):
    
    def test_01_create_user(self):
        global created_user
        created_user = create_user("john@example.com")
        self.assertIsNotNone(created_user.id)
    
    def test_02_update_user(self):
        global created_user
        updated_user = update_user(created_user.id, name="John Updated")
        self.assertEqual(updated_user.name, "John Updated")

# Good: Independent tests
class TestUserManagement(unittest.TestCase):
    
    def test_create_user_returns_user_with_id(self):
        user = create_user("john@example.com")
        self.assertIsNotNone(user.id)
    
    def test_update_user_changes_user_name(self):
        # Arrange: Create test data independently
        user = create_user("john@example.com")
        
        # Act
        updated_user = update_user(user.id, name="John Updated")
        
        # Assert
        self.assertEqual(updated_user.name, "John Updated")
```

### Testing Multiple Concerns in One Test
```python
# Bad: Testing multiple concerns
def test_user_registration_and_email_sending(self):
    email_service = Mock()
    user_service = UserService(email_service)
    
    user = user_service.register("john@example.com", "password123")
    
    # Testing user creation AND email sending
    self.assertIsNotNone(user.id)
    self.assertEqual(user.email, "john@example.com")
    self.assertFalse(user.email_verified)
    email_service.send_verification_email.assert_called_once()

# Good: Separate concerns
def test_user_registration_creates_unverified_user(self):
    email_service = Mock()
    user_service = UserService(email_service)
    
    user = user_service.register("john@example.com", "password123")
    
    # Only testing user creation
    self.assertIsNotNone(user.id)
    self.assertEqual(user.email, "john@example.com")
    self.assertFalse(user.email_verified)

def test_user_registration_sends_verification_email(self):
    email_service = Mock()
    user_service = UserService(email_service)
    
    user_service.register("john@example.com", "password123")
    
    # Only testing email sending
    email_service.send_verification_email.assert_called_once_with("john@example.com")
```

### Magic Numbers and Strings
```python
# Bad: Magic values without explanation
def test_calculate_discount(self):
    customer = Customer(membership_type="premium")
    order = Order(total=100.00)
    
    discount = calculate_discount(customer, order)
    
    self.assertEqual(discount, 20.00)  # Why 20.00?

# Good: Named constants with clear meaning
def test_calculate_discount_for_premium_customer(self):
    PREMIUM_DISCOUNT_RATE = 0.20
    ORDER_TOTAL = 100.00
    EXPECTED_DISCOUNT = ORDER_TOTAL * PREMIUM_DISCOUNT_RATE
    
    customer = Customer(membership_type="premium")
    order = Order(total=ORDER_TOTAL)
    
    discount = calculate_discount(customer, order)
    
    self.assertEqual(discount, EXPECTED_DISCOUNT)
```

## Language-Specific Examples

### Python Testing Frameworks and Tools

#### pytest (Recommended)
```python
import pytest
from unittest.mock import Mock, patch

class TestUserService:
    
    @pytest.fixture
    def user_repository(self):
        return Mock()
    
    @pytest.fixture
    def email_service(self):
        return Mock()
    
    @pytest.fixture
    def user_service(self, user_repository, email_service):
        return UserService(user_repository, email_service)
    
    def test_create_user_saves_to_repository(self, user_service, user_repository):
        # Arrange
        user_data = {"email": "test@example.com", "name": "Test User"}
        expected_user = User(id=1, **user_data)
        user_repository.save.return_value = expected_user
        
        # Act
        result = user_service.create_user(user_data)
        
        # Assert
        assert result.id == 1
        assert result.email == "test@example.com"
        user_repository.save.assert_called_once()
    
    @pytest.mark.parametrize("email,expected_valid", [
        ("valid@example.com", True),
        ("invalid-email", False),
        ("", False),
        ("no-at-symbol.com", False),
    ])
    def test_validate_email_format(self, email, expected_valid):
        result = validate_email(email)
        assert result == expected_valid
    
    def test_create_user_with_invalid_email_raises_exception(self, user_service):
        user_data = {"email": "invalid-email", "name": "Test User"}
        
        with pytest.raises(InvalidEmailException):
            user_service.create_user(user_data)
```

#### unittest (Built-in)
```python
import unittest
from unittest.mock import Mock, patch, MagicMock

class TestUserService(unittest.TestCase):
    
    def setUp(self):
        self.user_repository = Mock()
        self.email_service = Mock()
        self.user_service = UserService(self.user_repository, self.email_service)
    
    def test_create_user_saves_to_repository(self):
        # Arrange
        user_data = {"email": "test@example.com", "name": "Test User"}
        expected_user = User(id=1, **user_data)
        self.user_repository.save.return_value = expected_user
        
        # Act
        result = self.user_service.create_user(user_data)
        
        # Assert
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, "test@example.com")
        self.user_repository.save.assert_called_once()
    
    @patch('myapp.services.validate_email')
    def test_create_user_validates_email(self, mock_validate_email):
        # Arrange
        mock_validate_email.return_value = True
        user_data = {"email": "test@example.com", "name": "Test User"}
        
        # Act
        self.user_service.create_user(user_data)
        
        # Assert
        mock_validate_email.assert_called_once_with("test@example.com")
```

### Java Testing Frameworks and Tools

#### JUnit 5 with Mockito
```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@DisplayName("User Service Tests")
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private EmailService emailService;
    
    @InjectMocks
    private UserService userService;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    @Test
    @DisplayName("Should create user and save to repository")
    void createUser_SavesToRepository() {
        // Arrange
        UserData userData = new UserData("test@example.com", "Test User");
        User expectedUser = new User(1, "test@example.com", "Test User");
        when(userRepository.save(any(User.class))).thenReturn(expectedUser);
        
        // Act
        User result = userService.createUser(userData);
        
        // Assert
        assertEquals(1, result.getId());
        assertEquals("test@example.com", result.getEmail());
        verify(userRepository).save(any(User.class));
    }
    
    @ParameterizedTest
    @CsvSource({
        "valid@example.com, true",
        "invalid-email, false",
        "'', false",
        "no-at-symbol.com, false"
    })
    @DisplayName("Should validate email format correctly")
    void validateEmail_ReturnsCorrectResult(String email, boolean expectedValid) {
        boolean result = EmailValidator.isValid(email);
        assertEquals(expectedValid, result);
    }
    
    @Test
    @DisplayName("Should throw exception for invalid email")
    void createUser_WithInvalidEmail_ThrowsException() {
        UserData userData = new UserData("invalid-email", "Test User");
        
        assertThrows(InvalidEmailException.class, () -> 
            userService.createUser(userData)
        );
    }
    
    @Nested
    @DisplayName("Email notification tests")
    class EmailNotificationTests {
        
        @Test
        @DisplayName("Should send welcome email after user creation")
        void createUser_SendsWelcomeEmail() {
            // Arrange
            UserData userData = new UserData("test@example.com", "Test User");
            User savedUser = new User(1, "test@example.com", "Test User");
            when(userRepository.save(any(User.class))).thenReturn(savedUser);
            
            // Act
            userService.createUser(userData);
            
            // Assert
            verify(emailService).sendWelcomeEmail("test@example.com", "Test User");
        }
    }
}
```### C# Testing Frameworks and Tools

#### MSTest with Moq
```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using System.Threading.Tasks;

[TestClass]
public class UserServiceTests
{
    private Mock<IUserRepository> _userRepositoryMock;
    private Mock<IEmailService> _emailServiceMock;
    private UserService _userService;
    
    [TestInitialize]
    public void Setup()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _emailServiceMock = new Mock<IEmailService>();
        _userService = new UserService(_userRepositoryMock.Object, _emailServiceMock.Object);
    }
    
    [TestMethod]
    public async Task CreateUser_SavesToRepository()
    {
        // Arrange
        var userData = new UserData("test@example.com", "Test User");
        var expectedUser = new User(1, "test@example.com", "Test User");
        _userRepositoryMock
            .Setup(x => x.SaveAsync(It.IsAny<User>()))
            .ReturnsAsync(expectedUser);
        
        // Act
        var result = await _userService.CreateUserAsync(userData);
        
        // Assert
        Assert.AreEqual(1, result.Id);
        Assert.AreEqual("test@example.com", result.Email);
        _userRepositoryMock.Verify(x => x.SaveAsync(It.IsAny<User>()), Times.Once);
    }
    
    [DataTestMethod]
    [DataRow("valid@example.com", true)]
    [DataRow("invalid-email", false)]
    [DataRow("", false)]
    [DataRow("no-at-symbol.com", false)]
    public void ValidateEmail_ReturnsCorrectResult(string email, bool expectedValid)
    {
        var result = EmailValidator.IsValid(email);
        Assert.AreEqual(expectedValid, result);
    }
    
    [TestMethod]
    public async Task CreateUser_WithInvalidEmail_ThrowsException()
    {
        var userData = new UserData("invalid-email", "Test User");
        
        await Assert.ThrowsExceptionAsync<InvalidEmailException>(() =>
            _userService.CreateUserAsync(userData)
        );
    }
}
```

#### NUnit with Moq
```csharp
using NUnit.Framework;
using Moq;
using System.Threading.Tasks;

[TestFixture]
public class UserServiceTests
{
    private Mock<IUserRepository> _userRepositoryMock;
    private Mock<IEmailService> _emailServiceMock;
    private UserService _userService;
    
    [SetUp]
    public void Setup()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _emailServiceMock = new Mock<IEmailService>();
        _userService = new UserService(_userRepositoryMock.Object, _emailServiceMock.Object);
    }
    
    [Test]
    public async Task CreateUser_SavesToRepository()
    {
        // Arrange
        var userData = new UserData("test@example.com", "Test User");
        var expectedUser = new User(1, "test@example.com", "Test User");
        _userRepositoryMock
            .Setup(x => x.SaveAsync(It.IsAny<User>()))
            .ReturnsAsync(expectedUser);
        
        // Act
        var result = await _userService.CreateUserAsync(userData);
        
        // Assert
        Assert.That(result.Id, Is.EqualTo(1));
        Assert.That(result.Email, Is.EqualTo("test@example.com"));
        _userRepositoryMock.Verify(x => x.SaveAsync(It.IsAny<User>()), Times.Once);
    }
    
    [TestCase("valid@example.com", true)]
    [TestCase("invalid-email", false)]
    [TestCase("", false)]
    [TestCase("no-at-symbol.com", false)]
    public void ValidateEmail_ReturnsCorrectResult(string email, bool expectedValid)
    {
        var result = EmailValidator.IsValid(email);
        Assert.That(result, Is.EqualTo(expectedValid));
    }
    
    [Test]
    public void CreateUser_WithInvalidEmail_ThrowsException()
    {
        var userData = new UserData("invalid-email", "Test User");
        
        Assert.ThrowsAsync<InvalidEmailException>(() =>
            _userService.CreateUserAsync(userData)
        );
    }
}
```

#### xUnit with Moq
```csharp
using Xunit;
using Moq;
using System.Threading.Tasks;

public class UserServiceTests
{
    private readonly Mock<IUserRepository> _userRepositoryMock;
    private readonly Mock<IEmailService> _emailServiceMock;
    private readonly UserService _userService;
    
    public UserServiceTests()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _emailServiceMock = new Mock<IEmailService>();
        _userService = new UserService(_userRepositoryMock.Object, _emailServiceMock.Object);
    }
    
    [Fact]
    public async Task CreateUser_SavesToRepository()
    {
        // Arrange
        var userData = new UserData("test@example.com", "Test User");
        var expectedUser = new User(1, "test@example.com", "Test User");
        _userRepositoryMock
            .Setup(x => x.SaveAsync(It.IsAny<User>()))
            .ReturnsAsync(expectedUser);
        
        // Act
        var result = await _userService.CreateUserAsync(userData);
        
        // Assert
        Assert.Equal(1, result.Id);
        Assert.Equal("test@example.com", result.Email);
        _userRepositoryMock.Verify(x => x.SaveAsync(It.IsAny<User>()), Times.Once);
    }
    
    [Theory]
    [InlineData("valid@example.com", true)]
    [InlineData("invalid-email", false)]
    [InlineData("", false)]
    [InlineData("no-at-symbol.com", false)]
    public void ValidateEmail_ReturnsCorrectResult(string email, bool expectedValid)
    {
        var result = EmailValidator.IsValid(email);
        Assert.Equal(expectedValid, result);
    }
    
    [Fact]
    public async Task CreateUser_WithInvalidEmail_ThrowsException()
    {
        var userData = new UserData("invalid-email", "Test User");
        
        await Assert.ThrowsAsync<InvalidEmailException>(() =>
            _userService.CreateUserAsync(userData)
        );
    }
}
```

## CI/CD Integration

### Test Configuration Files

#### Python - pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=src
    --cov-report=html
    --cov-report=xml
    --cov-report=term-missing
    --cov-fail-under=80
    --junit-xml=test-results.xml
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

#### Python - setup.cfg
```ini
[coverage:run]
source = src
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */settings/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

#### Java - pom.xml (Maven)
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0-M9</version>
            <configuration>
                <includes>
                    <include>**/*Test.java</include>
                    <include>**/*Tests.java</include>
                </includes>
                <excludes>
                    <exclude>**/*IntegrationTest.java</exclude>
                </excludes>
                <systemPropertyVariables>
                    <junit.jupiter.execution.parallel.enabled>true</junit.jupiter.execution.parallel.enabled>
                    <junit.jupiter.execution.parallel.mode.default>concurrent</junit.jupiter.execution.parallel.mode.default>
                </systemPropertyVariables>
            </configuration>
        </plugin>
        
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.8</version>
            <executions>
                <execution>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>report</id>
                    <phase>test</phase>
                    <goals>
                        <goal>report</goal>
                    </goals>
                </execution>
            </executions>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>INSTRUCTION</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </plugin>
    </plugins>
</build>
```

#### C# - Directory.Build.props
```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <WarningsNotAsErrors>NU1701</WarningsNotAsErrors>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.3.2" />
    <PackageReference Include="coverlet.collector" Version="3.1.2" />
    <PackageReference Include="coverlet.msbuild" Version="3.1.2" />
  </ItemGroup>
</Project>
```

### CI/CD Pipeline Examples

#### GitHub Actions
```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run linting
      run: |
        flake8 src tests
        black --check src tests
        isort --check-only src tests
    
    - name: Run unit tests
      run: |
        pytest tests/unit --cov=src --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### Test Automation Best Practices

#### Fail Fast
```python
# Good: Use pytest-xvs for fail fast
# pytest -x -v tests/  # Stop on first failure

# Good: Organize tests by speed
pytest tests/unit  # Run fast tests first
pytest tests/integration  # Run slower tests after
```

#### Parallel Execution
```python
# pytest-xdist for parallel execution
# pytest -n 4 tests/  # Run with 4 workers

# pytest.ini configuration
[tool:pytest]
addopts = -n auto  # Use all available CPU cores
```

#### Test Categories
```python
# Mark tests for selective execution
@pytest.mark.unit
def test_calculate_discount():
    pass

@pytest.mark.integration
def test_payment_processing_integration():
    pass

@pytest.mark.slow
def test_large_data_processing():
    pass

# Run specific categories
# pytest -m unit  # Run only unit tests
# pytest -m "not slow"  # Skip slow tests
```## Quick Reference Checklist

### Test Writing Checklist

#### Before Writing Tests
- [ ] Identify the behavior to test (not implementation details)
- [ ] Determine test boundaries (unit vs integration)
- [ ] Plan test data and scenarios
- [ ] Consider edge cases and error conditions

#### Test Structure
- [ ] Use descriptive test names that explain intent
- [ ] Follow AAA pattern (Arrange, Act, Assert)
- [ ] Include only one logical assertion per test
- [ ] Use meaningful assertion messages
- [ ] Keep tests independent and isolated

#### Test Data Management
- [ ] Use test builders for complex objects
- [ ] Avoid hardcoded values (use constants)
- [ ] Use parameterized tests for multiple scenarios
- [ ] Clean up test data appropriately

#### Mocking and Dependencies
- [ ] Mock external dependencies only
- [ ] Verify behavior, not implementation
- [ ] Use appropriate test double type (mock, stub, fake)
- [ ] Don't over-mock (use real objects when simple)

#### Code Coverage
- [ ] Aim for high test coverage (80%+ for critical code)
- [ ] Focus on branch coverage, not just line coverage
- [ ] Don't test trivial code (getters, setters)
- [ ] Test edge cases and error paths

### Test Review Checklist

#### Readability
- [ ] Test intent is clear from the name
- [ ] Test is easy to understand without comments
- [ ] Test follows team conventions
- [ ] No unnecessary complexity

#### Reliability
- [ ] Test passes consistently
- [ ] Test doesn't depend on external state
- [ ] Test cleans up after itself
- [ ] No random or time-dependent behavior

#### Performance
- [ ] Test runs quickly (< 100ms for unit tests)
- [ ] No unnecessary setup or teardown
- [ ] Uses appropriate test scope
- [ ] Doesn't perform expensive operations

#### Maintenance
- [ ] Test will break when behavior changes
- [ ] Test won't break due to refactoring
- [ ] Test data is maintainable
- [ ] Test is not duplicate of existing test

### Common Testing Patterns

#### Boundary Value Testing
```python
@pytest.mark.parametrize("age,expected_category", [
    (0, "infant"),      # Lower boundary
    (1, "toddler"),     # Just above lower boundary
    (12, "child"),      # Just below upper boundary
    (13, "teenager"),   # Upper boundary
    (17, "teenager"),   # Just below next boundary
    (18, "adult"),      # Next boundary
    (64, "adult"),      # Just below next boundary
    (65, "senior"),     # Next boundary
])
def test_age_category_boundaries(age, expected_category):
    result = get_age_category(age)
    assert result == expected_category
```

#### Error Condition Testing
```python
def test_divide_by_zero_raises_exception():
    calculator = Calculator()
    
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calculator.divide(10, 0)

def test_invalid_input_raises_validation_error():
    validator = EmailValidator()
    
    with pytest.raises(ValidationError) as exc_info:
        validator.validate("invalid-email")
    
    assert "Invalid email format" in str(exc_info.value)
```

#### State-based Testing
```python
def test_shopping_cart_state_transitions():
    cart = ShoppingCart()
    
    # Initial state
    assert cart.is_empty()
    assert cart.total == 0.0
    
    # Add item
    cart.add_item(Item("Book", 10.00))
    assert not cart.is_empty()
    assert cart.total == 10.00
    
    # Remove item
    cart.remove_item("Book")
    assert cart.is_empty()
    assert cart.total == 0.0
```

#### Interaction-based Testing
```python
def test_order_service_sends_confirmation_email():
    email_service = Mock()
    order_service = OrderService(email_service)
    order = Order(customer_email="test@example.com", total=100.00)
    
    order_service.process_order(order)
    
    email_service.send_confirmation.assert_called_once_with(
        "test@example.com",
        order
    )
```

### Performance Testing Guidelines

#### Unit Test Performance Targets
- **Unit Tests**: < 100ms per test
- **Integration Tests**: < 5 seconds per test
- **End-to-End Tests**: < 30 seconds per test

#### Optimization Techniques
```python
# Use class-level fixtures for expensive setup
@pytest.fixture(scope="class")
def database_connection():
    connection = create_test_database()
    yield connection
    connection.close()

# Use session-level fixtures for one-time setup
@pytest.fixture(scope="session")
def test_data():
    return load_test_data_once()

# Use lazy loading for test data
@pytest.fixture
def user_data():
    return lambda: create_test_user()  # Only create when called
```

### Language-Specific Quick References

#### Python Testing Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_user_service.py

# Run specific test method
pytest tests/test_user_service.py::TestUserService::test_create_user

# Run tests matching pattern
pytest -k "test_create"

# Run tests with specific markers
pytest -m "unit"

# Run tests in parallel
pytest -n 4

# Stop on first failure
pytest -x

# Verbose output
pytest -v
```

#### Java Testing Commands
```bash
# Maven
mvn test                           # Run all tests
mvn test -Dtest=UserServiceTest    # Run specific test class
mvn test -Dtest=UserServiceTest#testCreateUser  # Run specific test method
mvn clean test                     # Clean and run tests
mvn test -DfailIfNoTests=false     # Don't fail if no tests

# Gradle
./gradlew test                     # Run all tests
./gradlew test --tests UserServiceTest  # Run specific test class
./gradlew test --tests "*UserService*"  # Run tests matching pattern
./gradlew clean test               # Clean and run tests
./gradlew test --continue          # Continue after test failures
```

#### C# Testing Commands
```bash
# .NET CLI
dotnet test                                    # Run all tests
dotnet test --filter "TestCategory=Unit"      # Run tests by category
dotnet test --filter "Name~UserService"       # Run tests matching name
dotnet test --logger "console;verbosity=detailed"  # Verbose output
dotnet test --collect:"XPlat Code Coverage"   # Run with coverage
dotnet test --no-build                        # Run without building

# Visual Studio Test Explorer
# Use Test Explorer in Visual Studio for GUI-based test running
# Right-click on test methods for context menu options
```

### Testing Anti-Pattern Quick Identification

#### Red Flags in Tests
- [ ] Test names like `test_method1()` or `test_user_service()`
- [ ] Tests longer than 20 lines
- [ ] Multiple assertions testing different concerns
- [ ] Tests that sleep or wait for time to pass
- [ ] Tests that depend on specific execution order
- [ ] Tests that modify global state
- [ ] Tests that require manual setup/cleanup
- [ ] Tests that test implementation details
- [ ] Tests with complex mock setups
- [ ] Tests that duplicate other tests

#### Good Test Indicators
- [ ] Clear, descriptive test names
- [ ] Single responsibility per test
- [ ] Fast execution (milliseconds for unit tests)
- [ ] No external dependencies
- [ ] Deterministic results
- [ ] Easy to understand and maintain
- [ ] Test behavior, not implementation
- [ ] Appropriate use of test doubles
- [ ] Good coverage of edge cases
- [ ] Tests act as documentation

### Testing Maturity Assessment

#### Level 1: Basic Testing
- [ ] Some unit tests exist
- [ ] Tests run manually
- [ ] Basic assertions
- [ ] Limited coverage

#### Level 2: Systematic Testing
- [ ] Consistent test structure
- [ ] Automated test execution
- [ ] Mocking framework usage
- [ ] Coverage measurement

#### Level 3: Advanced Testing
- [ ] Test-driven development
- [ ] Comprehensive test suite
- [ ] CI/CD integration
- [ ] Performance testing

#### Level 4: Testing Excellence
- [ ] Mutation testing
- [ ] Property-based testing
- [ ] Test automation everywhere
- [ ] Continuous testing feedback

---

## Summary

This guide provides comprehensive unit testing best practices that apply across programming languages. Key takeaways for AI assistants:

1. **Write Clear, Descriptive Tests**: Test names should explain the scenario and expected outcome
2. **Follow the AAA Pattern**: Arrange, Act, Assert for consistent test structure
3. **Test Behavior, Not Implementation**: Focus on what the code does, not how it does it
4. **Use Appropriate Test Doubles**: Mock external dependencies, use real objects for simple data
5. **Maintain Test Independence**: Each test should run in isolation
6. **Optimize for Readability**: Tests serve as documentation for the codebase
7. **Automate Everything**: Use CI/CD pipelines for consistent test execution
8. **Measure and Improve**: Use coverage tools and regular reviews to maintain quality

Remember: Good tests are fast, isolated, repeatable, self-validating, and timely. They should make you confident in your code changes and serve as documentation for how your system behaves.