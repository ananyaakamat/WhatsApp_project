# Python Best Practices Guide for AI Assistants

## Table of Contents
1. [Introduction](#introduction)
2. [PEP8 Style Guidelines](#pep8-style-guidelines)
3. [Clean Code Principles](#clean-code-principles)
4. [SOLID Principles in Python](#solid-principles-in-python)
5. [Modern Python Best Practices](#modern-python-best-practices)
6. [Quick Reference Checklist](#quick-reference-checklist)

## Introduction

This guide provides comprehensive Python coding best practices specifically designed for AI assistants to understand and apply. It covers PEP8 style guidelines, clean code principles, SOLID principles, and modern Python development practices.

### Key Principles for AI Code Generation
- **Consistency**: Follow established patterns throughout the codebase
- **Readability**: Code should be self-documenting and easy to understand
- **Maintainability**: Write code that can be easily modified and extended
- **Pythonic**: Embrace Python's idioms and conventions

## PEP8 Style Guidelines

### Naming Conventions

#### Variables and Functions
```python
# Good: Use snake_case for variables and functions
user_name = "john_doe"
total_count = 42

def calculate_total_price(items):
    return sum(item.price for item in items)

# Bad: Don't use camelCase or PascalCase for variables/functions
userName = "john_doe"  # Bad
totalCount = 42        # Bad
```

#### Classes
```python
# Good: Use PascalCase for class names
class UserAccount:
    pass

class PaymentProcessor:
    pass

# Bad: Don't use snake_case for classes
class user_account:  # Bad
    pass
```

#### Constants
```python
# Good: Use UPPER_CASE for constants
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"

# Bad: Don't use lowercase for constants
max_retry_count = 3  # Bad
```

### Code Layout

#### Indentation
```python
# Good: Use 4 spaces for indentation
def process_data(data):
    if data:
        for item in data:
            if item.is_valid():
                process_item(item)
    return True

# Bad: Don't use tabs or inconsistent spacing
def process_data(data):
	if data:  # Tab used (bad)
		for item in data:
		    if item.is_valid():  # Mixed tabs and spaces (very bad)
		        process_item(item)
	return True
```

#### Line Length
```python
# Good: Keep lines under 79 characters
def create_user_profile(username, email, first_name, last_name, 
                       date_of_birth, preferred_language="en"):
    return UserProfile(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        preferred_language=preferred_language
    )

# Bad: Lines too long
def create_user_profile(username, email, first_name, last_name, date_of_birth, preferred_language="en"):  # Too long
    return UserProfile(username=username, email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, preferred_language=preferred_language)  # Way too long
```

#### Imports
```python
# Good: Imports at the top, grouped and sorted
import os
import sys
from pathlib import Path

import requests
import numpy as np

from myproject.models import User
from myproject.utils import logger

# Bad: Mixed import styles and locations
from pathlib import Path
import os, sys  # Don't combine imports on one line
import requests
def some_function():
    import numpy as np  # Don't import inside functions unless necessary
```

### Whitespace

#### Function and Method Definitions
```python
# Good: Two blank lines before top-level functions/classes
class MyClass:
    pass


def my_function():
    pass


class AnotherClass:
    pass

# Good: One blank line before methods inside classes
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, value):
        self.result += value
        return self
    
    def multiply(self, value):
        self.result *= value
        return self
```

## Clean Code Principles

### Meaningful Names

#### Use Intention-Revealing Names
```python
# Good: Names that reveal intent
def get_active_users_count():
    return User.objects.filter(is_active=True).count()

elapsed_time_in_seconds = time.time() - start_time
user_settings = load_user_preferences(user_id)

# Bad: Unclear or abbreviated names
def getUsrCnt():  # What does this do?
    return User.objects.filter(is_active=True).count()

t = time.time() - s  # What do t and s represent?
d = load_user_preferences(user_id)  # What is d?
```

#### Use Searchable Names
```python
# Good: Use named constants instead of magic numbers
SECONDS_PER_DAY = 86400
MAX_RETRY_ATTEMPTS = 3
DEFAULT_PAGE_SIZE = 20

def calculate_days_between(start_date, end_date):
    seconds_diff = (end_date - start_date).total_seconds()
    return int(seconds_diff / SECONDS_PER_DAY)

# Bad: Magic numbers without context
def calculate_days_between(start_date, end_date):
    seconds_diff = (end_date - start_date).total_seconds()
    return int(seconds_diff / 86400)  # What is 86400?
```

### Functions

#### Keep Functions Small
```python
# Good: Small, focused functions
def validate_user_input(user_data):
    if not user_data.get('email'):
        raise ValueError("Email is required")
    if not user_data.get('username'):
        raise ValueError("Username is required")
    if len(user_data['username']) < 3:
        raise ValueError("Username must be at least 3 characters")

def create_user_account(user_data):
    validate_user_input(user_data)
    user = User.objects.create(**user_data)
    send_welcome_email(user.email)
    return user

# Bad: Large function doing too much
def create_user_account(user_data):
    # Validation
    if not user_data.get('email'):
        raise ValueError("Email is required")
    if not user_data.get('username'):
        raise ValueError("Username is required")
    if len(user_data['username']) < 3:
        raise ValueError("Username must be at least 3 characters")
    
    # Creation
    user = User.objects.create(**user_data)
    
    # Email sending
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(EMAIL_USER, EMAIL_PASS)
    message = f"Welcome {user.username}!"
    smtp_server.send_message(message)
    smtp_server.quit()
    
    return user
```

#### Function Arguments
```python
# Good: Minimize the number of arguments
class EmailService:
    def __init__(self, smtp_server, username, password):
        self.smtp_server = smtp_server
        self.username = username
        self.password = password
    
    def send_welcome_email(self, recipient_email, username):
        message = self._create_welcome_message(username)
        self._send_email(recipient_email, "Welcome!", message)

# Good: Use dataclasses for multiple related arguments
from dataclasses import dataclass

@dataclass
class UserRegistrationData:
    username: str
    email: str
    first_name: str
    last_name: str
    age: int

def register_user(registration_data: UserRegistrationData):
    # Process registration
    pass

# Bad: Too many function arguments
def register_user(username, email, first_name, last_name, age, 
                 phone, address, city, state, zip_code, country):
    # Too many parameters make this hard to use and maintain
    pass
```

### Comments and Documentation

#### Use Docstrings for Documentation
```python
# Good: Clear docstrings with type hints
def calculate_compound_interest(principal: float, rate: float, 
                              time: int, compounds_per_year: int = 1) -> float:
    """
    Calculate compound interest.
    
    Args:
        principal: The initial amount of money
        rate: Annual interest rate (as a decimal, e.g., 0.05 for 5%)
        time: Number of years
        compounds_per_year: Number of times interest is compounded per year
        
    Returns:
        The final amount after compound interest
        
    Raises:
        ValueError: If any of the numeric arguments are negative
        
    Example:
        >>> calculate_compound_interest(1000, 0.05, 10, 12)
        1643.62
    """
    if principal < 0 or rate < 0 or time < 0 or compounds_per_year < 0:
        raise ValueError("All arguments must be non-negative")
    
    return principal * (1 + rate / compounds_per_year) ** (compounds_per_year * time)
```

#### Use Comments to Explain Why, Not What
```python
# Good: Comments explain the reasoning
def process_payment(amount, currency="USD"):
    # Convert to cents to avoid floating point precision issues
    amount_in_cents = int(amount * 100)
    
    # Use exponential backoff for payment gateway retries
    # to handle temporary network issues gracefully
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return payment_gateway.charge(amount_in_cents, currency)
        except NetworkError:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    
    raise PaymentProcessingError("Failed to process payment after retries")

# Bad: Comments that just repeat the code
def process_payment(amount, currency="USD"):
    # Convert amount to cents
    amount_in_cents = int(amount * 100)
    
    # Set max retries to 3
    max_retries = 3
    
    # Loop through retries
    for attempt in range(max_retries):
        # Try to charge payment
        try:
            return payment_gateway.charge(amount_in_cents, currency)
        # Catch network error
        except NetworkError:
            # Calculate wait time
            wait_time = 2 ** attempt
            # Sleep for wait time
            time.sleep(wait_time)
```

## SOLID Principles in Python

### Single Responsibility Principle (SRP)

```python
# Good: Each class has a single responsibility
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

class UserRepository:
    def save(self, user: User):
        # Save user to database
        pass
    
    def find_by_email(self, email: str) -> User:
        # Find user by email
        pass

class EmailService:
    def send_welcome_email(self, user: User):
        # Send welcome email
        pass

class UserRegistrationService:
    def __init__(self, user_repo: UserRepository, email_service: EmailService):
        self.user_repo = user_repo
        self.email_service = email_service
    
    def register_user(self, username: str, email: str) -> User:
        user = User(username, email)
        self.user_repo.save(user)
        self.email_service.send_welcome_email(user)
        return user

# Bad: User class doing too much
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def save_to_database(self):
        # Database logic mixed with user logic
        pass
    
    def send_welcome_email(self):
        # Email logic mixed with user logic
        pass
    
    def validate_email_format(self):
        # Validation logic mixed with user logic
        pass
```

### Open/Closed Principle (OCP)

```python
# Good: Open for extension, closed for modification
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        # Credit card processing logic
        return True

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        # PayPal processing logic
        return True

class BitcoinProcessor(PaymentProcessor):  # New processor added without modifying existing code
    def process_payment(self, amount: float) -> bool:
        # Bitcoin processing logic
        return True

class PaymentService:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor
    
    def make_payment(self, amount: float) -> bool:
        return self.processor.process_payment(amount)

# Bad: Need to modify existing code to add new payment methods
class PaymentService:
    def process_payment(self, amount: float, payment_type: str) -> bool:
        if payment_type == "credit_card":
            # Credit card logic
            return True
        elif payment_type == "paypal":
            # PayPal logic
            return True
        # Need to modify this method every time we add a new payment type
        elif payment_type == "bitcoin":  # This violates OCP
            # Bitcoin logic
            return True
```

### Liskov Substitution Principle (LSP)

```python
# Good: Subclasses can replace base classes without breaking functionality
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Square(Shape):  # Separate class, doesn't inherit problematic behavior
    def __init__(self, side: float):
        self.side = side
    
    def area(self) -> float:
        return self.side * self.side

def calculate_total_area(shapes: list[Shape]) -> float:
    return sum(shape.area() for shape in shapes)

# This works correctly with any Shape subclass
shapes = [Rectangle(5, 10), Square(4), Rectangle(3, 7)]
total = calculate_total_area(shapes)  # Works correctly

# Bad: Square inheriting from Rectangle violates LSP
class Rectangle:
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height
    
    def set_width(self, width: float):
        self._width = width
    
    def set_height(self, height: float):
        self._height = height
    
    def area(self) -> float:
        return self._width * self._height

class Square(Rectangle):  # Problematic inheritance
    def set_width(self, width: float):
        self._width = width
        self._height = width  # Violates expected behavior
    
    def set_height(self, height: float):
        self._width = height
        self._height = height  # Violates expected behavior

# This breaks the expectation that setting width doesn't affect height
rectangle = Square(5)
rectangle.set_width(10)
rectangle.set_height(5)  # Both width and height become 5, unexpected!
```

### Interface Segregation Principle (ISP)

```python
# Good: Specific, focused interfaces
from abc import ABC, abstractmethod

class Readable(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

class Writable(ABC):
    @abstractmethod
    def write(self, data: str) -> None:
        pass

class Seekable(ABC):
    @abstractmethod
    def seek(self, position: int) -> None:
        pass

class FileReader(Readable):
    def read(self) -> str:
        # Only implements what it needs
        return "file content"

class FileWriter(Writable):
    def write(self, data: str) -> None:
        # Only implements what it needs
        pass

class RandomAccessFile(Readable, Writable, Seekable):
    def read(self) -> str:
        return "content"
    
    def write(self, data: str) -> None:
        pass
    
    def seek(self, position: int) -> None:
        pass

# Bad: Fat interface forcing unnecessary implementation
class FileHandler(ABC):
    @abstractmethod
    def read(self) -> str:
        pass
    
    @abstractmethod
    def write(self, data: str) -> None:
        pass
    
    @abstractmethod
    def seek(self, position: int) -> None:
        pass

class ReadOnlyFile(FileHandler):  # Forced to implement methods it doesn't need
    def read(self) -> str:
        return "content"
    
    def write(self, data: str) -> None:
        raise NotImplementedError("Read-only file cannot write")  # Bad!
    
    def seek(self, position: int) -> None:
        raise NotImplementedError("Read-only file cannot seek")  # Bad!
```

### Dependency Inversion Principle (DIP)

```python
# Good: Depend on abstractions, not concretions
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def save(self, data: dict) -> None:
        pass
    
    @abstractmethod
    def find(self, id: str) -> dict:
        pass

class PostgreSQLDatabase(DatabaseInterface):
    def save(self, data: dict) -> None:
        # PostgreSQL specific implementation
        pass
    
    def find(self, id: str) -> dict:
        # PostgreSQL specific implementation
        return {}

class MongoDatabase(DatabaseInterface):
    def save(self, data: dict) -> None:
        # MongoDB specific implementation
        pass
    
    def find(self, id: str) -> dict:
        # MongoDB specific implementation
        return {}

class UserService:
    def __init__(self, database: DatabaseInterface):  # Depends on abstraction
        self.database = database
    
    def create_user(self, user_data: dict) -> None:
        self.database.save(user_data)
    
    def get_user(self, user_id: str) -> dict:
        return self.database.find(user_id)

# Can easily switch database implementations
postgres_db = PostgreSQLDatabase()
mongo_db = MongoDatabase()

user_service_postgres = UserService(postgres_db)
user_service_mongo = UserService(mongo_db)

# Bad: Depending on concrete implementation
class UserService:
    def __init__(self):
        self.database = PostgreSQLDatabase()  # Tightly coupled to specific implementation
    
    def create_user(self, user_data: dict) -> None:
        self.database.save(user_data)  # Can't easily change database type
```

## Modern Python Best Practices

### Type Hints

```python
# Good: Use type hints for better code documentation and IDE support
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    email: str
    is_active: bool = True

def get_user_by_id(user_id: int) -> Optional[User]:
    # Return User or None if not found
    pass

def get_users_by_status(is_active: bool) -> List[User]:
    # Return list of users
    pass

def update_user_data(user_id: int, updates: Dict[str, Union[str, bool]]) -> User:
    # Update user and return updated user
    pass

# Bad: No type hints, unclear what the function expects/returns
def get_user_by_id(user_id):
    # What type is user_id? What does this return?
    pass

def update_user_data(user_id, updates):
    # What type are these parameters? What's returned?
    pass
```

### Use Context Managers

```python
# Good: Use context managers for resource management
def read_config_file(filename: str) -> dict:
    with open(filename, 'r') as file:
        return json.load(file)

def write_to_database(data: dict):
    with database_connection() as conn:
        conn.execute("INSERT INTO table VALUES (%s)", data)
        # Connection automatically closed even if exception occurs

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"Execution time: {end - start:.2f} seconds")

# Usage
with timer():
    # Some time-consuming operation
    process_large_dataset()

# Bad: Manual resource management
def read_config_file(filename: str) -> dict:
    file = open(filename, 'r')  # Could leak file handle if exception occurs
    data = json.load(file)
    file.close()  # Might not be reached if exception occurs
    return data
```

### Exception Handling

```python
# Good: Specific exception handling
def divide_numbers(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")
    except TypeError:
        raise ValueError("Both arguments must be numbers")

def load_user_data(user_id: int) -> User:
    try:
        return database.get_user(user_id)
    except DatabaseConnectionError:
        logger.error("Database connection failed")
        raise ServiceUnavailableError("User service temporarily unavailable")
    except UserNotFoundError:
        logger.info(f"User {user_id} not found")
        raise

# Custom exceptions for better error handling
class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

def validate_email(email: str) -> None:
    if "@" not in email:
        raise ValidationError("email", "Must contain @ symbol")

# Bad: Catching all exceptions
def divide_numbers(a, b):
    try:
        return a / b
    except Exception:  # Too broad
        return None  # Lost information about what went wrong

def load_user_data(user_id):
    try:
        return database.get_user(user_id)
    except:  # Even worse - catches everything including KeyboardInterrupt
        pass  # Silent failure is dangerous
```

### Use List Comprehensions and Generator Expressions

```python
# Good: List comprehensions for simple transformations
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers if x % 2 == 0]  # [4, 16]

# Good: Generator expressions for memory efficiency
def process_large_file(filename: str):
    with open(filename) as file:
        # Process one line at a time, memory efficient
        valid_lines = (line.strip() for line in file if line.strip())
        for line in valid_lines:
            yield process_line(line)

# Good: Dictionary comprehensions
user_emails = {"john": "john@example.com", "jane": "jane@example.com"}
email_domains = {user: email.split("@")[1] for user, email in user_emails.items()}

# Bad: Unnecessary loops
squares = []
for x in numbers:
    if x % 2 == 0:
        squares.append(x**2)

# Bad: Loading everything into memory
def process_large_file(filename: str):
    with open(filename) as file:
        all_lines = file.readlines()  # Loads entire file into memory
        valid_lines = []
        for line in all_lines:
            if line.strip():
                valid_lines.append(line.strip())
        return [process_line(line) for line in valid_lines]
```

### Use Dataclasses and Named Tuples

```python
# Good: Use dataclasses for data containers
from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    id: int
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")

@dataclass(frozen=True)  # Immutable
class Point:
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        return (self.x**2 + self.y**2)**0.5

# Good: Use named tuples for simple immutable data
from typing import NamedTuple

class Coordinate(NamedTuple):
    latitude: float
    longitude: float
    
    def to_string(self) -> str:
        return f"({self.latitude}, {self.longitude})"

# Bad: Using regular classes for simple data containers
class Product:
    def __init__(self, id, name, price, tags=None):
        self.id = id
        self.name = name
        self.price = price
        self.tags = tags or []  # Mutable default argument issue
    
    def __eq__(self, other):  # Need to implement all comparison methods
        return (self.id == other.id and 
                self.name == other.name and 
                self.price == other.price and 
                self.tags == other.tags)
    
    def __repr__(self):  # Need to implement string representation
        return f"Product(id={self.id}, name={self.name}, price={self.price}, tags={self.tags})"
```

## Quick Reference Checklist

### Code Style ✅
- [ ] Use snake_case for variables and functions
- [ ] Use PascalCase for classes  
- [ ] Use UPPER_CASE for constants
- [ ] Keep lines under 79 characters
- [ ] Use 4 spaces for indentation
- [ ] Group imports (standard library, third-party, local)
- [ ] Two blank lines before top-level functions/classes
- [ ] One blank line before methods in classes

### Function Design ✅
- [ ] Functions do one thing well (Single Responsibility)
- [ ] Function names are descriptive and verb-based
- [ ] Functions have type hints
- [ ] Functions have docstrings with examples
- [ ] Minimize function arguments (prefer dataclasses for many args)
- [ ] No side effects unless clearly indicated

### Error Handling ✅
- [ ] Use specific exception types
- [ ] Create custom exceptions when appropriate
- [ ] Don't catch generic Exception unless necessary
- [ ] Log errors appropriately
- [ ] Use context managers for resource management

### SOLID Principles ✅
- [ ] Each class has a single responsibility
- [ ] Use inheritance/composition properly (Open/Closed)
- [ ] Subclasses can replace base classes (Liskov Substitution)
- [ ] Interfaces are focused and specific (Interface Segregation)
- [ ] Depend on abstractions, not concretions (Dependency Inversion)

### Modern Python Features ✅
- [ ] Use type hints consistently
- [ ] Use dataclasses for data containers
- [ ] Use list/dict comprehensions appropriately
- [ ] Use generator expressions for memory efficiency
- [ ] Use context managers for resource management
- [ ] Use pathlib for file paths
- [ ] Use f-strings for string formatting

### Testing Considerations ✅
- [ ] Functions are testable (pure when possible)
- [ ] Dependencies can be mocked/stubbed
- [ ] Edge cases are considered
- [ ] Error conditions are testable

This guide provides a foundation for writing clean, maintainable Python code that follows industry best practices and is easily understood by both humans and AI assistants.