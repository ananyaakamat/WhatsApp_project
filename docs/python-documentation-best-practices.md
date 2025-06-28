# Python Documentation Best Practices Guide for AI Assistants

## Table of Contents
1. [Introduction](#introduction)
2. [Comments vs Documentation](#comments-vs-documentation)
3. [Type Hinting Best Practices](#type-hinting-best-practices)
4. [Docstring Standards](#docstring-standards)
5. [Sphinx Documentation Generation](#sphinx-documentation-generation)
6. [Code Examples and Patterns](#code-examples-and-patterns)
7. [Documentation Automation](#documentation-automation)
8. [Quality Assurance](#quality-assurance)
9. [Quick Reference Checklist](#quick-reference-checklist)

## Introduction

This guide provides comprehensive Python documentation best practices specifically designed for AI assistants to understand and apply. It covers type hinting, docstring conventions, automated documentation generation with Sphinx, and modern Python documentation standards.

### Key Principles for AI Documentation Generation
- **Clarity**: Documentation should be self-explanatory and unambiguous
- **Consistency**: Follow established patterns and conventions
- **Completeness**: Cover all public APIs with proper documentation
- **Maintainability**: Documentation should be easy to update and maintain
- **Automation**: Use tools to generate and validate documentation

## Comments vs Documentation

### Understanding the Difference

```python
# Good: Comments explain WHY (for developers)
def calculate_tax(income: float, tax_rate: float) -> float:
    """
    Calculate tax amount based on income and tax rate.
    
    Args:
        income: Annual income in dollars
        tax_rate: Tax rate as a decimal (e.g., 0.25 for 25%)
        
    Returns:
        Tax amount in dollars
    """
    # Use ceiling to round up to nearest cent for tax compliance
    return math.ceil(income * tax_rate * 100) / 100

# Bad: Comments that just repeat the code
def calculate_tax(income: float, tax_rate: float) -> float:
    # Multiply income by tax rate  # This is obvious from the code
    return income * tax_rate
```

### When to Use Comments vs Docstrings

```python
# Good: Strategic use of comments and docstrings
class PaymentProcessor:
    """
    Handles payment processing with multiple payment methods.
    
    This class provides a unified interface for processing payments
    through various payment gateways while handling failures gracefully.
    """
    
    def __init__(self, api_key: str, sandbox: bool = False):
        """
        Initialize payment processor.
        
        Args:
            api_key: API key for payment gateway
            sandbox: Whether to use sandbox mode for testing
        """
        self.api_key = api_key
        self.sandbox = sandbox
        # Cache successful payment methods to optimize retry logic
        self._successful_methods = set()
    
    def process_payment(self, amount: float, method: str) -> bool:
        """
        Process a payment using specified method.
        
        Args:
            amount: Payment amount in dollars
            method: Payment method ('credit_card', 'paypal', 'bank_transfer')
            
        Returns:
            True if payment successful, False otherwise
            
        Raises:
            ValueError: If amount is negative or method is invalid
            PaymentGatewayError: If payment gateway is unavailable
        """
        if amount < 0:
            raise ValueError("Payment amount cannot be negative")
        
        # Try cached successful method first to reduce latency
        if method in self._successful_methods:
            return self._attempt_payment(amount, method)
        
        return self._attempt_payment(amount, method)

# Bad: Mixing concerns and poor documentation
class PaymentProcessor:
    # This class processes payments  # Should be in docstring
    def __init__(self, api_key, sandbox=False):
        self.api_key = api_key  # Store API key
        self.sandbox = sandbox  # Set sandbox mode
        
    def process_payment(self, amount, method):
        # Process payment  # No useful information
        if amount < 0:  # Check if negative
            return False  # Return false if negative
        return True  # Return true otherwise
```

## Type Hinting Best Practices

### Basic Type Hints

```python
# Good: Comprehensive type hints with modern syntax (Python 3.9+)
from __future__ import annotations  # Enable forward references
from typing import Optional, Union, List, Dict, Callable, Any
from dataclasses import dataclass
from datetime import datetime

def process_user_data(
    user_id: int,
    username: str,
    email: Optional[str] = None,
    tags: list[str] | None = None,  # Python 3.10+ union syntax
    metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Process user data and return formatted result.
    
    Args:
        user_id: Unique identifier for the user
        username: Username string (must be unique)
        email: Optional email address
        tags: Optional list of user tags
        metadata: Optional dictionary of additional user data
        
    Returns:
        Dictionary containing processed user information
    """
    result = {
        'id': user_id,
        'username': username,
        'created_at': datetime.now().isoformat()
    }
    
    if email:
        result['email'] = email
    if tags:
        result['tags'] = tags
    if metadata:
        result['metadata'] = metadata
        
    return result

# Good: Complex type hints for advanced scenarios
from typing import Protocol, TypeVar, Generic

T = TypeVar('T')

class Serializable(Protocol):
    """Protocol for objects that can be serialized."""
    def to_dict(self) -> dict[str, Any]: ...

class Repository(Generic[T]):
    """
    Generic repository pattern for data storage.
    
    Type Parameters:
        T: Type of objects stored in this repository
    """
    
    def save(self, item: T) -> T:
        """Save an item to the repository."""
        ...
    
    def find_by_id(self, id: int) -> Optional[T]:
        """Find an item by its ID."""
        ...
    
    def find_all(self) -> list[T]:
        """Retrieve all items from the repository."""
        ...

@dataclass
class User:
    """User data model with comprehensive type hints."""
    id: int
    username: str
    email: str
    is_active: bool = True
    created_at: datetime = None
    tags: list[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.tags is None:
            self.tags = []

# Bad: Missing or inadequate type hints
def process_user_data(user_id, username, email=None, tags=None):  # No type hints
    # Function behavior unclear without types
    return {'id': user_id, 'username': username}

def bad_function(data):  # Too generic
    return data  # What type is returned?
```

### Type Validation with mypy

```python
# Good: Code that passes mypy validation
from typing import NewType, Final

# Create distinct types for better type safety
UserId = NewType('UserId', int)
Email = NewType('Email', str)

# Use Final for constants
MAX_USERNAME_LENGTH: Final = 50
DEFAULT_USER_ROLE: Final = 'user'

class UserService:
    """Service for user management operations."""
    
    def create_user(
        self, 
        username: str, 
        email: Email,
        role: str = DEFAULT_USER_ROLE
    ) -> UserId:
        """
        Create a new user account.
        
        Args:
            username: Unique username (max 50 characters)
            email: Valid email address
            role: User role (default: 'user')
            
        Returns:
            Newly created user ID
            
        Raises:
            ValueError: If username is too long or email is invalid
        """
        if len(username) > MAX_USERNAME_LENGTH:
            raise ValueError(f"Username too long (max {MAX_USERNAME_LENGTH})")
        
        # Implementation would go here
        return UserId(12345)
    
    def get_user(self, user_id: UserId) -> Optional[dict[str, Any]]:
        """Retrieve user by ID."""
        # Implementation would go here
        return None

# Usage with proper types
service = UserService()
email = Email("user@example.com")
user_id = service.create_user("john_doe", email)
user_data = service.get_user(user_id)

# Bad: Type errors that mypy would catch
def create_user(username, email):  # Missing types
    return username + email  # Type error: might not be strings

def get_user(user_id: int) -> str:  # Inconsistent return type
    return {'id': user_id}  # Returns dict, not str
```

## Docstring Standards

### Function Docstrings (Sphinx/reStructuredText Format)

```python
# Good: Comprehensive function documentation
import math
from typing import Optional

def calculate_compound_interest(
    principal: float,
    rate: float,
    time: int,
    compound_frequency: int = 1,
    additional_payment: Optional[float] = None
) -> dict[str, float]:
    """
    Calculate compound interest with optional additional payments.
    
    This function computes compound interest using the standard formula
    and optionally includes regular additional payments to the principal.
    
    Args:
        principal: Initial principal amount in dollars
        rate: Annual interest rate as a decimal (e.g., 0.05 for 5%)
        time: Number of years to compound
        compound_frequency: Number of times interest compounds per year (default: 1)
        additional_payment: Optional additional payment made each compounding period
        
    Returns:
        Dictionary containing:
            - 'final_amount': Total amount after interest
            - 'total_interest': Interest earned
            - 'total_payments': Sum of additional payments made
            
    Raises:
        ValueError: If principal, rate, or time is negative
        ValueError: If compound_frequency is less than 1
        
    Example:
        >>> result = calculate_compound_interest(1000, 0.05, 10, 12, 100)
        >>> print(f"Final amount: ${result['final_amount']:.2f}")
        Final amount: $3737.35
        
    Note:
        The formula used is: A = P(1 + r/n)^(nt) + PMT * [((1 + r/n)^(nt) - 1) / (r/n)]
        where PMT is the additional payment amount.
        
    See Also:
        simple_interest: For simple interest calculations
        investment_growth: For more complex investment scenarios
    """
    if principal < 0 or rate < 0 or time < 0:
        raise ValueError("Principal, rate, and time must be non-negative")
    if compound_frequency < 1:
        raise ValueError("Compound frequency must be at least 1")
    
    # Standard compound interest calculation
    compound_amount = principal * (1 + rate / compound_frequency) ** (compound_frequency * time)
    
    # Add additional payments if specified
    total_additional = 0.0
    if additional_payment and additional_payment > 0:
        # Future value of annuity formula
        periods = compound_frequency * time
        period_rate = rate / compound_frequency
        if period_rate > 0:
            additional_growth = additional_payment * (
                ((1 + period_rate) ** periods - 1) / period_rate
            )
            compound_amount += additional_growth
            total_additional = additional_payment * periods
    
    total_interest = compound_amount - principal - total_additional
    
    return {
        'final_amount': round(compound_amount, 2),
        'total_interest': round(total_interest, 2),
        'total_payments': round(total_additional, 2)
    }

# Bad: Minimal or missing documentation
def calc_interest(p, r, t, n=1):  # Unclear parameter names
    """Calculate interest."""  # Too brief
    return p * (1 + r/n) ** (n*t)  # No explanation of formula or parameters
```

### Class Docstrings

```python
# Good: Comprehensive class documentation
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    """Protocol for objects that can be drawn on a canvas."""
    def draw(self, canvas: 'Canvas') -> None: ...

class Shape(ABC):
    """
    Abstract base class for geometric shapes.
    
    This class provides a common interface for all geometric shapes
    and implements shared functionality like area calculation validation.
    
    Attributes:
        name: Human-readable name of the shape
        color: RGB color tuple (default: black)
        filled: Whether the shape should be filled when drawn
        
    Class Attributes:
        PI: Mathematical constant pi for circular calculations
        
    Example:
        >>> class Circle(Shape):
        ...     def __init__(self, radius):
        ...         super().__init__("Circle")
        ...         self.radius = radius
        ...     def area(self):
        ...         return Shape.PI * self.radius ** 2
        >>> circle = Circle(5)
        >>> print(f"Area: {circle.area():.2f}")
        Area: 78.54
        
    Note:
        Subclasses must implement the abstract methods: area() and perimeter()
    """
    
    PI: float = 3.14159265359
    
    def __init__(self, name: str, color: tuple[int, int, int] = (0, 0, 0)):
        """
        Initialize a shape with basic properties.
        
        Args:
            name: Descriptive name of the shape
            color: RGB color tuple (values 0-255)
            
        Raises:
            ValueError: If color values are outside 0-255 range
        """
        if any(c < 0 or c > 255 for c in color):
            raise ValueError("Color values must be between 0 and 255")
            
        self.name = name
        self.color = color
        self.filled = False
    
    @abstractmethod
    def area(self) -> float:
        """
        Calculate the area of the shape.
        
        Returns:
            Area in square units
        """
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """
        Calculate the perimeter of the shape.
        
        Returns:
            Perimeter in linear units
        """
        pass
    
    def is_larger_than(self, other: 'Shape') -> bool:
        """
        Compare this shape's area with another shape.
        
        Args:
            other: Another shape to compare against
            
        Returns:
            True if this shape has a larger area
            
        Example:
            >>> circle = Circle(5)
            >>> square = Square(8)
            >>> circle.is_larger_than(square)
            True
        """
        return self.area() > other.area()

class Rectangle(Shape):
    """
    Rectangle shape implementation.
    
    A rectangle is defined by its width and height dimensions.
    
    Args:
        width: Width of the rectangle
        height: Height of the rectangle
        color: Optional RGB color (default: black)
        
    Attributes:
        width: Rectangle width
        height: Rectangle height
        
    Example:
        >>> rect = Rectangle(10, 5)
        >>> print(f"Area: {rect.area()}")
        Area: 50
        >>> print(f"Perimeter: {rect.perimeter()}")
        Perimeter: 30
    """
    
    def __init__(self, width: float, height: float, color: tuple[int, int, int] = (0, 0, 0)):
        super().__init__("Rectangle", color)
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        """Calculate rectangle area (width × height)."""
        return self.width * self.height
    
    def perimeter(self) -> float:
        """Calculate rectangle perimeter (2 × (width + height))."""
        return 2 * (self.width + self.height)

# Bad: Poor class documentation
class Rectangle:
    """A rectangle."""  # Too brief
    
    def __init__(self, w, h):  # No docstring, unclear parameters
        self.w = w
        self.h = h
    
    def area(self):  # No documentation
        return self.w * self.h
```

### Module Docstrings

```python
# Good: Comprehensive module documentation
"""
Geometric Shapes Library
========================

This module provides classes and functions for working with geometric shapes.
It includes implementations for basic shapes like rectangles, circles, and triangles,
as well as utility functions for shape manipulation and analysis.

Classes:
    Shape: Abstract base class for all geometric shapes
    Rectangle: Rectangle implementation with width and height
    Circle: Circle implementation with radius
    Triangle: Triangle implementation with three sides
    Canvas: Drawing surface for rendering shapes

Functions:
    calculate_total_area: Sum areas of multiple shapes
    find_largest_shape: Find shape with maximum area
    shapes_overlap: Check if two shapes overlap

Constants:
    DEFAULT_COLOR: Default RGB color for shapes (black)
    MAX_CANVAS_SIZE: Maximum allowed canvas dimensions

Examples:
    Basic shape creation and manipulation:
    
    >>> from shapes import Rectangle, Circle
    >>> rect = Rectangle(10, 5)
    >>> circle = Circle(3)
    >>> print(f"Rectangle area: {rect.area()}")
    Rectangle area: 50
    >>> print(f"Circle area: {circle.area():.2f}")
    Circle area: 28.27

    Using utility functions:
    
    >>> from shapes import calculate_total_area
    >>> total = calculate_total_area([rect, circle])
    >>> print(f"Total area: {total:.2f}")
    Total area: 78.27

Author:
    Development Team <dev@company.com>

Version:
    2.1.0

License:
    MIT License - see LICENSE file for details

See Also:
    - geometry.utils: Additional geometric utility functions
    - graphics.canvas: Advanced canvas rendering capabilities
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union
import math

# Module constants with documentation
DEFAULT_COLOR: tuple[int, int, int] = (0, 0, 0)
"""Default RGB color for shapes (black)."""

MAX_CANVAS_SIZE: int = 10000
"""Maximum allowed canvas dimension in pixels."""

# Rest of module implementation...

# Bad: Missing or inadequate module documentation
"""
shapes.py - some shape classes
"""
# No description of what the module does
# No examples or usage information
# No author or version information
```

## Sphinx Documentation Generation

### Project Setup for Sphinx

```python
# docs/conf.py - Sphinx configuration
"""Sphinx configuration for automatic documentation generation."""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'My Python Project'
copyright = '2025, Development Team'
author = 'Development Team'
version = '1.0.0'
release = '1.0.0'

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',        # Automatic documentation from docstrings
    'sphinx.ext.viewcode',       # Add source code links
    'sphinx.ext.napoleon',       # Google/NumPy docstring support
    'sphinx.ext.intersphinx',    # Link to other projects' documentation
    'sphinx.ext.doctest',        # Test code examples in docstrings
    'sphinx.ext.coverage',       # Documentation coverage reports
    'sphinx.ext.githubpages',    # GitHub Pages support
]

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'pandas': ('https://pandas.pydata.org/docs', None),
}

# HTML theme and options
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False
}

# Static files
html_static_path = ['_static']
html_css_files = ['custom.css']

# Output options
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True
```

### Automatic API Documentation

```rst
.. Good: Comprehensive API documentation structure
.. docs/source/api.rst

API Reference
=============

This section contains the complete API reference for all modules,
classes, and functions in the project.

Core Modules
------------

shapes module
~~~~~~~~~~~~~

.. automodule:: shapes
   :members:
   :undoc-members:
   :show-inheritance:

utils module
~~~~~~~~~~~~

.. automodule:: utils
   :members:
   :undoc-members:
   :show-inheritance:

Classes
-------

Shape Classes
~~~~~~~~~~~~~

.. autoclass:: shapes.Shape
   :members:
   :special-members: __init__
   :show-inheritance:

.. autoclass:: shapes.Rectangle
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: shapes.Circle
   :members:
   :inherited-members:
   :show-inheritance:

Functions
---------

Utility Functions
~~~~~~~~~~~~~~~~~

.. autofunction:: utils.calculate_total_area

.. autofunction:: utils.find_largest_shape

.. autofunction:: utils.shapes_overlap

Exceptions
----------

.. autoexception:: shapes.ShapeError
   :members:

.. autoexception:: shapes.InvalidDimensionError
   :members:
```

### Documentation Build Automation

```python
# build_docs.py - Automated documentation building
"""Script for automated documentation generation and validation."""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command: list[str], cwd: str = None) -> bool:
    """
    Run a shell command and return success status.
    
    Args:
        command: Command and arguments as list
        cwd: Working directory for command
        
    Returns:
        True if command succeeded, False otherwise
    """
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✓ {' '.join(command)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {' '.join(command)}")
        print(f"Error: {e.stderr}")
        return False

def generate_api_docs() -> bool:
    """Generate API documentation using sphinx-apidoc."""
    docs_dir = Path("docs")
    source_dir = docs_dir / "source"
    
    # Create docs directory if it doesn't exist
    source_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate API documentation
    command = [
        "sphinx-apidoc",
        "-f",  # Force overwrite
        "-o", str(source_dir),  # Output directory
        ".",  # Source directory
        "tests/",  # Exclude tests
        "setup.py",  # Exclude setup.py
    ]
    
    return run_command(command)

def build_html_docs() -> bool:
    """Build HTML documentation."""
    return run_command(["make", "html"], cwd="docs")

def validate_docs() -> bool:
    """Validate documentation for common issues."""
    # Check for broken links
    link_check = run_command(["make", "linkcheck"], cwd="docs")
    
    # Run doctests
    doctest_check = run_command(["make", "doctest"], cwd="docs")
    
    return link_check and doctest_check

def main():
    """Main documentation build process."""
    print("🏗️  Building documentation...")
    
    steps = [
        ("Generating API docs", generate_api_docs),
        ("Building HTML", build_html_docs),
        ("Validating docs", validate_docs),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ {step_name} failed!")
            sys.exit(1)
    
    print("\n✅ Documentation build completed successfully!")
    print("📂 Documentation available at: docs/_build/html/index.html")

if __name__ == "__main__":
    main()
```

## Code Examples and Patterns

### Documented Design Patterns

```python
# Good: Well-documented design pattern implementation
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class Observer(ABC):
    """
    Abstract base class for observers in the Observer pattern.
    
    Observers are notified when the subject's state changes.
    """
    
    @abstractmethod
    def update(self, subject: 'Subject', event_type: str, data: Any = None) -> None:
        """
        Handle notification from subject.
        
        Args:
            subject: The subject that triggered the notification
            event_type: Type of event that occurred
            data: Optional event data
        """
        pass

class Subject:
    """
    Subject class for the Observer pattern.
    
    Maintains a list of observers and notifies them of state changes.
    
    Example:
        >>> class UserAccount(Subject):
        ...     def __init__(self, username):
        ...         super().__init__()
        ...         self.username = username
        ...         self.balance = 0
        ...     
        ...     def deposit(self, amount):
        ...         self.balance += amount
        ...         self.notify_observers('deposit', {'amount': amount})
        
        >>> class EmailNotifier(Observer):
        ...     def update(self, subject, event_type, data=None):
        ...         print(f"Email: {subject.username} made a {event_type}")
        
        >>> account = UserAccount("john_doe")
        >>> notifier = EmailNotifier()
        >>> account.add_observer(notifier)
        >>> account.deposit(100)
        Email: john_doe made a deposit
    """
    
    def __init__(self):
        """Initialize subject with empty observer list."""
        self._observers: List[Observer] = []
    
    def add_observer(self, observer: Observer) -> None:
        """
        Add an observer to the notification list.
        
        Args:
            observer: Observer to add
            
        Raises:
            ValueError: If observer is already registered
        """
        if observer in self._observers:
            raise ValueError("Observer already registered")
        self._observers.append(observer)
    
    def remove_observer(self, observer: Observer) -> None:
        """
        Remove an observer from the notification list.
        
        Args:
            observer: Observer to remove
            
        Raises:
            ValueError: If observer is not registered
        """
        if observer not in self._observers:
            raise ValueError("Observer not registered")
        self._observers.remove(observer)
    
    def notify_observers(self, event_type: str, data: Any = None) -> None:
        """
        Notify all registered observers of an event.
        
        Args:
            event_type: Type of event that occurred
            data: Optional event data to pass to observers
        """
        for observer in self._observers:
            try:
                observer.update(self, event_type, data)
            except Exception as e:
                # Log error but continue notifying other observers
                print(f"Error notifying observer {observer}: {e}")

# Factory Pattern with comprehensive documentation
class ShapeFactory:
    """
    Factory class for creating geometric shapes.
    
    This factory provides a centralized way to create shape instances
    based on string identifiers, making it easy to extend with new shapes.
    
    Attributes:
        _creators: Dictionary mapping shape names to creator functions
        
    Example:
        >>> factory = ShapeFactory()
        >>> rectangle = factory.create_shape('rectangle', width=10, height=5)
        >>> circle = factory.create_shape('circle', radius=3)
        >>> print(f"Rectangle area: {rectangle.area()}")
        Rectangle area: 50
        
    Note:
        New shape types can be registered using the register_shape method.
    """
    
    def __init__(self):
        """Initialize factory with default shape creators."""
        self._creators: Dict[str, callable] = {
            'rectangle': self._create_rectangle,
            'circle': self._create_circle,
            'triangle': self._create_triangle,
        }
    
    def register_shape(self, name: str, creator: callable) -> None:
        """
        Register a new shape type with the factory.
        
        Args:
            name: Unique name for the shape type
            creator: Function that creates the shape instance
            
        Raises:
            ValueError: If shape name is already registered
            
        Example:
            >>> def create_hexagon(**kwargs):
            ...     return Hexagon(kwargs['side_length'])
            >>> factory.register_shape('hexagon', create_hexagon)
        """
        if name in self._creators:
            raise ValueError(f"Shape type '{name}' already registered")
        self._creators[name] = creator
    
    def create_shape(self, shape_type: str, **kwargs) -> 'Shape':
        """
        Create a shape instance of the specified type.
        
        Args:
            shape_type: Type of shape to create
            **kwargs: Shape-specific parameters
            
        Returns:
            Shape instance of the requested type
            
        Raises:
            ValueError: If shape_type is not registered
            TypeError: If required parameters are missing
            
        Example:
            >>> rectangle = factory.create_shape('rectangle', width=10, height=5)
            >>> circle = factory.create_shape('circle', radius=3)
        """
        if shape_type not in self._creators:
            available_types = ', '.join(self._creators.keys())
            raise ValueError(
                f"Unknown shape type '{shape_type}'. "
                f"Available types: {available_types}"
            )
        
        try:
            return self._creators[shape_type](**kwargs)
        except TypeError as e:
            raise TypeError(
                f"Invalid parameters for {shape_type}: {e}"
            ) from e
    
    def _create_rectangle(self, width: float, height: float, **kwargs) -> 'Rectangle':
        """Create Rectangle instance with validation."""
        return Rectangle(width, height)
    
    def _create_circle(self, radius: float, **kwargs) -> 'Circle':
        """Create Circle instance with validation."""
        return Circle(radius)
    
    def _create_triangle(self, side_a: float, side_b: float, side_c: float, **kwargs) -> 'Triangle':
        """Create Triangle instance with validation."""
        return Triangle(side_a, side_b, side_c)

# Bad: Poorly documented design pattern
class Factory:  # Generic name, no docstring
    def __init__(self):
        self.things = {}  # Unclear what 'things' are
    
    def make(self, type, **args):  # No documentation, unclear parameters
        return self.things[type](**args)  # No error handling
```

### Documented Error Handling

```python
# Good: Comprehensive error handling with documentation
class ValidationError(Exception):
    """
    Raised when data validation fails.
    
    This exception includes detailed information about what validation
    failed and provides suggestions for fixing the issue.
    
    Attributes:
        field: Name of the field that failed validation
        value: The invalid value that was provided
        message: Human-readable error message
        suggestions: List of suggested fixes
    """
    
    def __init__(
        self, 
        field: str, 
        value: Any, 
        message: str, 
        suggestions: Optional[List[str]] = None
    ):
        """
        Initialize validation error with detailed information.
        
        Args:
            field: Name of the field that failed validation
            value: The invalid value
            message: Description of the validation failure
            suggestions: Optional list of suggested fixes
        """
        self.field = field
        self.value = value
        self.message = message
        self.suggestions = suggestions or []
        
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """Format comprehensive error message."""
        msg = f"Validation failed for field '{self.field}': {self.message}"
        msg += f"\nProvided value: {self.value}"
        
        if self.suggestions:
            msg += "\nSuggestions:"
            for suggestion in self.suggestions:
                msg += f"\n  - {suggestion}"
        
        return msg

def validate_user_data(data: Dict[str, Any]) -> None:
    """
    Validate user registration data.
    
    Args:
        data: Dictionary containing user data to validate
        
    Raises:
        ValidationError: If any validation rules fail
        TypeError: If data is not a dictionary
        
    Example:
        >>> user_data = {
        ...     'username': 'john_doe',
        ...     'email': 'john@example.com',
        ...     'age': 25
        ... }
        >>> validate_user_data(user_data)  # No exception raised
        
        >>> invalid_data = {'username': 'j', 'email': 'invalid'}
        >>> validate_user_data(invalid_data)
        ValidationError: Validation failed for field 'username': Must be at least 3 characters
    """
    if not isinstance(data, dict):
        raise TypeError("User data must be a dictionary")
    
    # Username validation
    username = data.get('username', '')
    if not username:
        raise ValidationError(
            'username', 
            username, 
            'Username is required',
            ['Provide a username between 3-50 characters']
        )
    elif len(username) < 3:
        raise ValidationError(
            'username',
            username,
            'Must be at least 3 characters',
            [
                'Use a longer username',
                'Username should be 3-50 characters long'
            ]
        )
    elif len(username) > 50:
        raise ValidationError(
            'username',
            username,
            'Must be no more than 50 characters',
            ['Shorten the username to 50 characters or less']
        )
    
    # Email validation
    email = data.get('email', '')
    if not email:
        raise ValidationError(
            'email',
            email,
            'Email address is required',
            ['Provide a valid email address like user@example.com']
        )
    elif '@' not in email or '.' not in email:
        raise ValidationError(
            'email',
            email,
            'Invalid email format',
            [
                'Use format: username@domain.com',
                'Include both @ symbol and domain extension'
            ]
        )
    
    # Age validation
    age = data.get('age')
    if age is not None:
        if not isinstance(age, int):
            raise ValidationError(
                'age',
                age,
                'Age must be an integer',
                ['Provide age as a whole number']
            )
        elif age < 13:
            raise ValidationError(
                'age',
                age,
                'Must be at least 13 years old',
                ['Users must be 13 or older to register']
            )
        elif age > 120:
            raise ValidationError(
                'age',
                age,
                'Age seems unrealistic',
                ['Please verify the age is correct']
            )

# Bad: Poor error handling documentation
def validate_data(data):  # No type hints or docstring
    if not data['username']:  # KeyError if 'username' missing
        raise Exception("Bad username")  # Generic exception
    # No comprehensive validation
    # No helpful error messages
```

## Documentation Automation

### Pre-commit Hooks for Documentation

```python
# .pre-commit-config.yaml
"""Pre-commit configuration for documentation quality assurance."""

repos:
  - repo: local
    hooks:
      - id: doc-style-check
        name: Documentation Style Check
        entry: python scripts/check_docs.py
        language: python
        files: \.py$
        pass_filenames: true
        
      - id: type-check
        name: Type Checking with mypy
        entry: mypy
        language: python
        files: \.py$
        additional_dependencies: [mypy]
        
      - id: docstring-coverage
        name: Docstring Coverage Check
        entry: python scripts/docstring_coverage.py
        language: python
        files: \.py$

# scripts/check_docs.py
"""Documentation quality checker script."""

import ast
import sys
from pathlib import Path
from typing import List, Tuple

class DocChecker:
    """
    Checker for Python documentation quality.
    
    Validates docstring presence, type hints, and documentation standards.
    """
    
    def __init__(self):
        """Initialize documentation checker."""
        self.errors: List[Tuple[str, int, str]] = []
    
    def check_file(self, filepath: Path) -> bool:
        """
        Check a Python file for documentation issues.
        
        Args:
            filepath: Path to Python file to check
            
        Returns:
            True if no issues found, False otherwise
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            self._check_node(tree, filepath)
            
            return len(self.errors) == 0
            
        except SyntaxError as e:
            self.errors.append((str(filepath), e.lineno, f"Syntax error: {e.msg}"))
            return False
    
    def _check_node(self, node: ast.AST, filepath: Path) -> None:
        """Recursively check AST nodes for documentation issues."""
        if isinstance(node, ast.FunctionDef):
            self._check_function(node, filepath)
        elif isinstance(node, ast.ClassDef):
            self._check_class(node, filepath)
        
        for child in ast.iter_child_nodes(node):
            self._check_node(child, filepath)
    
    def _check_function(self, node: ast.FunctionDef, filepath: Path) -> None:
        """Check function for proper documentation."""
        # Skip private functions
        if node.name.startswith('_') and not node.name.startswith('__'):
            return
        
        # Check for docstring
        if not ast.get_docstring(node):
            self.errors.append((
                str(filepath), 
                node.lineno, 
                f"Function '{node.name}' missing docstring"
            ))
        
        # Check for type hints
        if node.returns is None and node.name != '__init__':
            self.errors.append((
                str(filepath),
                node.lineno,
                f"Function '{node.name}' missing return type hint"
            ))
        
        # Check parameter type hints
        for arg in node.args.args:
            if arg.annotation is None and arg.arg != 'self':
                self.errors.append((
                    str(filepath),
                    node.lineno,
                    f"Parameter '{arg.arg}' in '{node.name}' missing type hint"
                ))
    
    def _check_class(self, node: ast.ClassDef, filepath: Path) -> None:
        """Check class for proper documentation."""
        if not ast.get_docstring(node):
            self.errors.append((
                str(filepath),
                node.lineno,
                f"Class '{node.name}' missing docstring"
            ))
    
    def print_errors(self) -> None:
        """Print all documentation errors found."""
        for filepath, lineno, message in self.errors:
            print(f"{filepath}:{lineno}: {message}")

def main():
    """Main function for documentation checking."""
    if len(sys.argv) < 2:
        print("Usage: python check_docs.py <file1.py> [file2.py ...]")
        sys.exit(1)
    
    checker = DocChecker()
    all_good = True
    
    for filepath in sys.argv[1:]:
        path = Path(filepath)
        if path.suffix == '.py':
            if not checker.check_file(path):
                all_good = False
    
    if not all_good:
        print("\n📋 Documentation issues found:")
        checker.print_errors()
        sys.exit(1)
    else:
        print("✅ All documentation checks passed!")

if __name__ == "__main__":
    main()
```

### Continuous Integration for Documentation

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install sphinx sphinx_rtd_theme mypy
    
    - name: Type checking with mypy
      run: |
        mypy --config-file=mypy.ini src/
    
    - name: Check docstring coverage
      run: |
        python scripts/docstring_coverage.py src/
    
    - name: Build documentation
      run: |
        cd docs
        make html
    
    - name: Test documentation examples
      run: |
        cd docs
        make doctest
    
    - name: Check for broken links
      run: |
        cd docs
        make linkcheck
    
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/_build/html
```

## Quality Assurance

### Documentation Testing

```python
# Good: Comprehensive doctest examples
def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    
    The Fibonacci sequence starts with 0, 1, and each subsequent number
    is the sum of the two preceding ones.
    
    Args:
        n: Position in the Fibonacci sequence (0-indexed)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        Basic usage:
        
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(5)
        5
        >>> fibonacci(10)
        55
        
        Edge cases:
        
        >>> fibonacci(-1)
        Traceback (most recent call last):
            ...
        ValueError: n must be non-negative
        
        Large numbers:
        
        >>> fibonacci(20)
        6765
        
    Note:
        This implementation uses recursion and may be slow for large values.
        Consider using the iterative version for better performance.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def parse_config(config_str: str) -> dict[str, str]:
    """
    Parse configuration string into dictionary.
    
    Args:
        config_str: Configuration in key=value format, one per line
        
    Returns:
        Dictionary of configuration key-value pairs
        
    Examples:
        Simple configuration:
        
        >>> config = '''
        ... host=localhost
        ... port=8080
        ... debug=true
        ... '''
        >>> result = parse_config(config)
        >>> sorted(result.items())
        [('debug', 'true'), ('host', 'localhost'), ('port', '8080')]
        
        Empty and whitespace handling:
        
        >>> parse_config('')
        {}
        >>> parse_config('   \\n  \\n  ')
        {}
        
        Comments and invalid lines:
        
        >>> config_with_comments = '''
        ... # This is a comment
        ... host=localhost
        ... # Another comment
        ... port=8080
        ... invalid_line_without_equals
        ... debug=true
        ... '''
        >>> result = parse_config(config_with_comments)
        >>> len(result)
        3
        >>> result['host']
        'localhost'
    """
    result = {}
    
    for line in config_str.strip().split('\n'):
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Skip lines without equals sign
        if '=' not in line:
            continue
        
        key, value = line.split('=', 1)
        result[key.strip()] = value.strip()
    
    return result

# Bad: Poor or missing doctests
def calculate(a, b):
    """Calculate something."""  # No examples
    return a + b

def process_data(data):
    """
    Process data.
    
    Example:
        >>> process_data([1, 2, 3])  # No expected output
    """
    return [x * 2 for x in data]
```

### Documentation Coverage Measurement

```python
# scripts/docstring_coverage.py
"""Script to measure and report docstring coverage."""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class DocstringCoverage:
    """
    Measures docstring coverage for Python modules.
    
    Analyzes Python files to determine what percentage of functions,
    classes, and modules have proper docstring documentation.
    """
    
    def __init__(self):
        """Initialize coverage tracker."""
        self.stats = {
            'modules': {'total': 0, 'documented': 0},
            'classes': {'total': 0, 'documented': 0},
            'functions': {'total': 0, 'documented': 0},
        }
        self.missing_docs: List[Tuple[str, str, str]] = []
    
    def analyze_file(self, filepath: Path) -> None:
        """
        Analyze a Python file for docstring coverage.
        
        Args:
            filepath: Path to Python file to analyze
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Check module docstring
            self.stats['modules']['total'] += 1
            if ast.get_docstring(tree):
                self.stats['modules']['documented'] += 1
            else:
                self.missing_docs.append((str(filepath), 'module', str(filepath)))
            
            self._analyze_node(tree, filepath)
            
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Error analyzing {filepath}: {e}")
    
    def _analyze_node(self, node: ast.AST, filepath: Path) -> None:
        """Recursively analyze AST nodes."""
        if isinstance(node, ast.ClassDef):
            self._check_class(node, filepath)
        elif isinstance(node, ast.FunctionDef):
            self._check_function(node, filepath)
        
        for child in ast.iter_child_nodes(node):
            self._analyze_node(child, filepath)
    
    def _check_class(self, node: ast.ClassDef, filepath: Path) -> None:
        """Check class for docstring."""
        self.stats['classes']['total'] += 1
        if ast.get_docstring(node):
            self.stats['classes']['documented'] += 1
        else:
            self.missing_docs.append((str(filepath), 'class', node.name))
    
    def _check_function(self, node: ast.FunctionDef, filepath: Path) -> None:
        """Check function for docstring."""
        # Skip private functions (but include special methods)
        if node.name.startswith('_') and not node.name.startswith('__'):
            return
        
        self.stats['functions']['total'] += 1
        if ast.get_docstring(node):
            self.stats['functions']['documented'] += 1
        else:
            self.missing_docs.append((str(filepath), 'function', node.name))
    
    def calculate_coverage(self) -> Dict[str, float]:
        """Calculate coverage percentages."""
        coverage = {}
        for category, counts in self.stats.items():
            if counts['total'] > 0:
                coverage[category] = (counts['documented'] / counts['total']) * 100
            else:
                coverage[category] = 100.0
        
        # Calculate overall coverage
        total_items = sum(counts['total'] for counts in self.stats.values())
        total_documented = sum(counts['documented'] for counts in self.stats.values())
        
        if total_items > 0:
            coverage['overall'] = (total_documented / total_items) * 100
        else:
            coverage['overall'] = 100.0
        
        return coverage
    
    def print_report(self, minimum_coverage: float = 80.0) -> bool:
        """
        Print coverage report.
        
        Args:
            minimum_coverage: Minimum acceptable coverage percentage
            
        Returns:
            True if coverage meets minimum threshold
        """
        coverage = self.calculate_coverage()
        
        print("📊 Docstring Coverage Report")
        print("=" * 50)
        
        for category, percentage in coverage.items():
            if category == 'overall':
                continue
            
            counts = self.stats[category]
            status = "✅" if percentage >= minimum_coverage else "❌"
            print(f"{status} {category.capitalize()}: {counts['documented']}/{counts['total']} ({percentage:.1f}%)")
        
        print("-" * 50)
        overall_status = "✅" if coverage['overall'] >= minimum_coverage else "❌"
        print(f"{overall_status} Overall: {coverage['overall']:.1f}%")
        
        if self.missing_docs:
            print(f"\n📝 Missing Documentation ({len(self.missing_docs)} items):")
            for filepath, item_type, name in self.missing_docs:
                print(f"  - {filepath}: {item_type} '{name}'")
        
        return coverage['overall'] >= minimum_coverage

def main():
    """Main function for docstring coverage analysis."""
    if len(sys.argv) < 2:
        print("Usage: python docstring_coverage.py <directory>")
        sys.exit(1)
    
    directory = Path(sys.argv[1])
    minimum_coverage = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0
    
    coverage = DocstringCoverage()
    
    # Analyze all Python files in directory
    for py_file in directory.rglob("*.py"):
        if py_file.name.startswith('.'):
            continue
        coverage.analyze_file(py_file)
    
    # Print report and exit with appropriate code
    meets_threshold = coverage.print_report(minimum_coverage)
    sys.exit(0 if meets_threshold else 1)

if __name__ == "__main__":
    main()
```

## Quick Reference Checklist

### Docstring Standards ✅
- [ ] All public modules have module docstrings
- [ ] All public classes have comprehensive docstrings
- [ ] All public functions have docstrings with Args/Returns/Raises
- [ ] Docstrings include practical examples
- [ ] Complex algorithms include implementation notes
- [ ] Docstrings are in reStructuredText or Google/NumPy format

### Type Hinting ✅
- [ ] All function parameters have type hints
- [ ] All function return types are specified
- [ ] Complex types use proper typing imports
- [ ] Type hints are validated with mypy
- [ ] Generic types are used appropriately
- [ ] Optional and Union types are used correctly

### Code Examples ✅
- [ ] Docstrings include working code examples
- [ ] Examples cover common use cases
- [ ] Edge cases are documented with examples
- [ ] Examples are tested with doctest
- [ ] Error conditions are demonstrated
- [ ] Examples show expected output

### Sphinx Documentation ✅
- [ ] Project configured with sphinx-quickstart
- [ ] conf.py includes necessary extensions
- [ ] API documentation auto-generated
- [ ] Documentation builds without errors
- [ ] Cross-references work correctly
- [ ] External links are validated

### Automation ✅
- [ ] Pre-commit hooks check documentation quality
- [ ] CI/CD pipeline builds and validates docs
- [ ] Docstring coverage is measured and enforced
- [ ] Documentation is automatically deployed
- [ ] Broken links are detected automatically
- [ ] Type checking is integrated into workflow

### Quality Assurance ✅
- [ ] Doctests are comprehensive and pass
- [ ] Documentation coverage meets project standards
- [ ] Examples are kept up-to-date with code changes
- [ ] Documentation is reviewed in pull requests
- [ ] Style guide is consistently followed
- [ ] Performance implications are documented

This guide provides a comprehensive foundation for creating high-quality Python documentation that is easily understood and applied by both humans and AI assistants. It emphasizes automation, consistency, and practical examples to ensure documentation remains valuable and maintainable over time.