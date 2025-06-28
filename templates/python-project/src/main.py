"""
Main module for the application.

This module serves as the entry point and contains the core functionality
of the application. It demonstrates best practices for Python code organization,
documentation, and type hinting.
"""

from __future__ import annotations

import logging
from typing import Optional, Any, Dict, List
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Config:
    """
    Configuration class for application settings.

    This class encapsulates all configuration parameters needed
    for the application to run properly.

    Attributes:
        app_name: Name of the application
        debug: Whether debug mode is enabled
        max_retries: Maximum number of retry attempts
        timeout: Request timeout in seconds
        created_at: When the configuration was created
    """
    app_name: str = "Reference Project"
    debug: bool = False
    max_retries: int = 3
    timeout: float = 30.0
    created_at: datetime = None

    def __post_init__(self) -> None:
        """Initialize computed fields after dataclass creation."""
        if self.created_at is None:
            self.created_at = datetime.now()


class ApplicationError(Exception):
    """
    Base exception for application-specific errors.

    This exception provides a foundation for creating more specific
    error types with consistent error handling across the application.

    Attributes:
        message: Human-readable error message
        error_code: Application-specific error code
        details: Additional error details
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize application error.

        Args:
            message: Error message
            error_code: Optional error code for categorization
            details: Optional additional error information
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class DataProcessor:
    """
    Processes and validates data according to business rules.

    This class demonstrates clean code principles including:
    - Single responsibility (data processing only)
    - Dependency injection (config is injected)
    - Proper error handling
    - Comprehensive documentation

    Example:
        >>> config = Config(debug=True)
        >>> processor = DataProcessor(config)
        >>> result = processor.process_items([1, 2, 3, 4, 5])
        >>> print(result['total'])
        15
    """

    def __init__(self, config: Config):
        """
        Initialize data processor with configuration.

        Args:
            config: Application configuration object

        Raises:
            TypeError: If config is not a Config instance
        """
        if not isinstance(config, Config):
            raise TypeError("config must be a Config instance")

        self.config = config
        self._processed_count = 0

        logger.info(
            "DataProcessor initialized with config: %s",
            self.config.app_name
        )

    def process_items(self, items: List[Any]) -> Dict[str, Any]:
        """
        Process a list of items and return summary statistics.

        This method validates input, processes each item, and returns
        comprehensive statistics about the processing results.

        Args:
            items: List of items to process

        Returns:
            Dictionary containing:
                - total: Sum of all numeric items
                - count: Number of items processed
                - valid_items: List of successfully processed items
                - errors: List of any errors encountered

        Raises:
            ApplicationError: If items list is empty or None

        Example:
            >>> processor = DataProcessor(Config())
            >>> result = processor.process_items([1, "2", 3.5, "invalid"])
            >>> result['total']
            6.5
            >>> result['count']
            3
        """
        if not items:
            raise ApplicationError(
                "Items list cannot be empty or None",
                error_code="INVALID_INPUT",
                details={"items_length": len(items) if items else 0}
            )

        logger.info("Processing %d items", len(items))

        total = 0.0
        valid_items = []
        errors = []

        for i, item in enumerate(items):
            try:
                processed_item = self._process_single_item(item)
                if processed_item is not None:
                    total += processed_item
                    valid_items.append(processed_item)

            except (ValueError, TypeError) as e:
                error_details = {
                    "index": i,
                    "item": item,
                    "error": str(e)
                }
                errors.append(error_details)

                if self.config.debug:
                    logger.warning("Error processing item at index %d: %s", i, e)

        self._processed_count += len(valid_items)

        result = {
            "total": total,
            "count": len(valid_items),
            "valid_items": valid_items,
            "errors": errors,
            "processed_timestamp": datetime.now().isoformat()
        }

        logger.info(
            "Processing complete. Valid items: %d, Errors: %d, Total: %.2f",
            len(valid_items), len(errors), total
        )

        return result

    def _process_single_item(self, item: Any) -> Optional[float]:
        """
        Process a single item and convert it to a numeric value.

        This private method handles the conversion of individual items
        to numeric values, with appropriate error handling.

        Args:
            item: Single item to process

        Returns:
            Numeric value of the item, or None if item is None

        Raises:
            ValueError: If item cannot be converted to a number
            TypeError: If item type is not supported
        """
        if item is None:
            return None

        if isinstance(item, (int, float)):
            return float(item)

        if isinstance(item, str):
            try:
                return float(item)
            except ValueError:
                raise ValueError(f"Cannot convert string '{item}' to number")

        raise TypeError(f"Unsupported item type: {type(item)}")

    @property
    def total_processed(self) -> int:
        """Get the total number of items processed by this instance."""
        return self._processed_count

    def reset_counter(self) -> None:
        """Reset the processed items counter."""
        self._processed_count = 0
        logger.info("Processed items counter reset")


def create_default_processor() -> DataProcessor:
    """
    Factory function to create a DataProcessor with default configuration.

    This function demonstrates the factory pattern and provides a convenient
    way to create processor instances with sensible defaults.

    Returns:
        DataProcessor instance with default configuration

    Example:
        >>> processor = create_default_processor()
        >>> result = processor.process_items([1, 2, 3])
        >>> result['count']
        3
    """
    config = Config(
        app_name="Default Reference Project",
        debug=False,
        max_retries=3,
        timeout=30.0
    )

    return DataProcessor(config)


def main() -> None:
    """
    Main entry point for the application.

    This function demonstrates how to structure a main function with
    proper error handling and logging.
    """
    try:
        logger.info("Starting Reference Project application")

        # Create processor with default configuration
        processor = create_default_processor()

        # Example data processing
        sample_data = [1, 2, 3, "4", 5.5, "invalid", None, 7]
        result = processor.process_items(sample_data)

        print("Processing Results:")
        print(f"  Total: {result['total']}")
        print(f"  Valid items: {result['count']}")
        print(f"  Errors: {len(result['errors'])}")

        if result['errors']:
            print("  Error details:")
            for error in result['errors']:
                print(f"    Index {error['index']}: {error['error']}")

        logger.info("Application completed successfully")

    except ApplicationError as e:
        logger.error("Application error: %s (Code: %s)", e.message, e.error_code)
        if e.details:
            logger.debug("Error details: %s", e.details)

    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)


if __name__ == "__main__":
    main()
