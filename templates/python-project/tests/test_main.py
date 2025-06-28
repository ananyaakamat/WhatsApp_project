"""
Comprehensive test suite for the main module.

This module demonstrates best practices for writing unit tests including:
- Clear test organization and naming
- Use of fixtures for setup and teardown
- Comprehensive test coverage
- Testing both success and failure scenarios
- Proper use of mocking and assertions
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from typing import List, Any

from src.main import (
    Config,
    ApplicationError,
    DataProcessor,
    create_default_processor
)


class TestConfig:
    """Test suite for the Config dataclass."""

    def test_config_default_values(self):
        """Test that Config initializes with correct default values."""
        config = Config()

        assert config.app_name == "Reference Project"
        assert config.debug is False
        assert config.max_retries == 3
        assert config.timeout == 30.0
        assert isinstance(config.created_at, datetime)

    def test_config_custom_values(self):
        """Test that Config accepts custom values."""
        custom_time = datetime.now()
        config = Config(
            app_name="Custom App",
            debug=True,
            max_retries=5,
            timeout=60.0,
            created_at=custom_time
        )

        assert config.app_name == "Custom App"
        assert config.debug is True
        assert config.max_retries == 5
        assert config.timeout == 60.0
        assert config.created_at == custom_time

    def test_config_post_init(self):
        """Test that __post_init__ sets created_at when None."""
        with patch('src.main.datetime') as mock_datetime:
            mock_now = Mock()
            mock_datetime.now.return_value = mock_now

            config = Config(created_at=None)

            assert config.created_at == mock_now
            mock_datetime.now.assert_called_once()


class TestApplicationError:
    """Test suite for the ApplicationError exception class."""

    def test_application_error_basic(self):
        """Test basic ApplicationError creation."""
        error = ApplicationError("Test error")

        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.error_code is None
        assert error.details == {}

    def test_application_error_with_code_and_details(self):
        """Test ApplicationError with error code and details."""
        details = {"field": "username", "value": "invalid"}
        error = ApplicationError(
            "Validation failed",
            error_code="VALIDATION_ERROR",
            details=details
        )

        assert error.message == "Validation failed"
        assert error.error_code == "VALIDATION_ERROR"
        assert error.details == details

    def test_application_error_inheritance(self):
        """Test that ApplicationError is properly inherited from Exception."""
        error = ApplicationError("Test")
        assert isinstance(error, Exception)


class TestDataProcessor:
    """Test suite for the DataProcessor class."""

    @pytest.fixture
    def config(self):
        """Provide a test configuration."""
        return Config(app_name="Test App", debug=True)

    @pytest.fixture
    def processor(self, config):
        """Provide a DataProcessor instance for testing."""
        return DataProcessor(config)

    def test_data_processor_initialization(self, config):
        """Test DataProcessor initialization with valid config."""
        processor = DataProcessor(config)

        assert processor.config == config
        assert processor.total_processed == 0

    def test_data_processor_invalid_config(self):
        """Test DataProcessor initialization with invalid config."""
        with pytest.raises(TypeError, match="config must be a Config instance"):
            DataProcessor("invalid_config")

    def test_process_items_empty_list(self, processor):
        """Test processing empty list raises ApplicationError."""
        with pytest.raises(ApplicationError) as exc_info:
            processor.process_items([])

        assert exc_info.value.error_code == "INVALID_INPUT"
        assert "cannot be empty" in exc_info.value.message

    def test_process_items_none(self, processor):
        """Test processing None raises ApplicationError."""
        with pytest.raises(ApplicationError) as exc_info:
            processor.process_items(None)

        assert exc_info.value.error_code == "INVALID_INPUT"

    def test_process_items_valid_numbers(self, processor):
        """Test processing list of valid numbers."""
        items = [1, 2, 3, 4, 5]
        result = processor.process_items(items)

        assert result['total'] == 15.0
        assert result['count'] == 5
        assert result['valid_items'] == [1.0, 2.0, 3.0, 4.0, 5.0]
        assert result['errors'] == []
        assert 'processed_timestamp' in result

    def test_process_items_mixed_types(self, processor):
        """Test processing list with mixed valid and invalid types."""
        items = [1, "2", 3.5, "invalid", None]
        result = processor.process_items(items)

        assert result['total'] == 6.5  # 1 + 2 + 3.5
        assert result['count'] == 3
        assert result['valid_items'] == [1.0, 2.0, 3.5]
        assert len(result['errors']) == 1  # "invalid" should cause error

        # Check error details
        error = result['errors'][0]
        assert error['index'] == 3
        assert error['item'] == "invalid"
        assert "Cannot convert string" in error['error']

    def test_process_items_all_invalid(self, processor):
        """Test processing list with all invalid items."""
        items = ["invalid1", "invalid2", object()]
        result = processor.process_items(items)

        assert result['total'] == 0.0
        assert result['count'] == 0
        assert result['valid_items'] == []
        assert len(result['errors']) == 3

    def test_process_single_item_numeric(self, processor):
        """Test _process_single_item with numeric values."""
        assert processor._process_single_item(42) == 42.0
        assert processor._process_single_item(3.14) == 3.14
        assert processor._process_single_item("123") == 123.0
        assert processor._process_single_item("45.67") == 45.67
        assert processor._process_single_item(None) is None

    def test_process_single_item_invalid_string(self, processor):
        """Test _process_single_item with invalid string."""
        with pytest.raises(ValueError, match="Cannot convert string"):
            processor._process_single_item("not_a_number")

    def test_process_single_item_unsupported_type(self, processor):
        """Test _process_single_item with unsupported type."""
        with pytest.raises(TypeError, match="Unsupported item type"):
            processor._process_single_item(object())

    def test_total_processed_counter(self, processor):
        """Test that total_processed counter works correctly."""
        assert processor.total_processed == 0

        processor.process_items([1, 2, 3])
        assert processor.total_processed == 3

        processor.process_items([4, 5])
        assert processor.total_processed == 5

    def test_reset_counter(self, processor):
        """Test reset_counter functionality."""
        processor.process_items([1, 2, 3])
        assert processor.total_processed == 3

        processor.reset_counter()
        assert processor.total_processed == 0

    @patch('src.main.logger')
    def test_logging_calls(self, mock_logger, processor):
        """Test that appropriate logging calls are made."""
        items = [1, 2, "invalid"]
        processor.process_items(items)

        # Verify logging calls were made
        mock_logger.info.assert_called()
        mock_logger.warning.assert_called()  # Due to debug=True in config


class TestCreateDefaultProcessor:
    """Test suite for the create_default_processor factory function."""

    def test_create_default_processor(self):
        """Test that create_default_processor returns properly configured instance."""
        processor = create_default_processor()

        assert isinstance(processor, DataProcessor)
        assert processor.config.app_name == "Default Reference Project"
        assert processor.config.debug is False
        assert processor.config.max_retries == 3
        assert processor.config.timeout == 30.0
        assert processor.total_processed == 0

    def test_create_default_processor_independence(self):
        """Test that multiple calls create independent instances."""
        processor1 = create_default_processor()
        processor2 = create_default_processor()

        # Process items with first processor
        processor1.process_items([1, 2, 3])

        # Second processor should be unaffected
        assert processor1.total_processed == 3
        assert processor2.total_processed == 0
        assert processor1 is not processor2


class TestIntegration:
    """Integration tests for the entire module."""

    def test_end_to_end_processing(self):
        """Test complete end-to-end data processing workflow."""
        # Create processor
        processor = create_default_processor()

        # Process multiple batches
        batch1 = [1, 2, 3, "4", 5.5]
        batch2 = ["invalid", 6, 7, None, 8.5]

        result1 = processor.process_items(batch1)
        result2 = processor.process_items(batch2)

        # Verify first batch results
        assert result1['total'] == 15.5  # 1+2+3+4+5.5
        assert result1['count'] == 5
        assert len(result1['errors']) == 0

        # Verify second batch results
        assert result2['total'] == 21.5  # 6+7+8.5
        assert result2['count'] == 3
        assert len(result2['errors']) == 1  # "invalid"

        # Verify cumulative counter
        assert processor.total_processed == 8  # 5 + 3

    @patch('src.main.logger')
    def test_main_function_success_path(self, mock_logger):
        """Test main function success path."""
        # This would normally test the main() function
        # For this example, we'll test the key components it uses
        processor = create_default_processor()
        sample_data = [1, 2, 3, "4", 5.5, "invalid", None, 7]

        result = processor.process_items(sample_data)

        # Verify expected results
        assert result['total'] > 0
        assert result['count'] > 0
        assert len(result['errors']) > 0  # "invalid" should cause an error

    def test_error_handling_chain(self):
        """Test error handling throughout the processing chain."""
        config = Config(debug=False)  # Disable debug for cleaner error handling
        processor = DataProcessor(config)

        # Test with problematic data
        problematic_data = [object(), {}, []]
        result = processor.process_items(problematic_data)

        # Should handle all errors gracefully
        assert result['total'] == 0.0
        assert result['count'] == 0
        assert len(result['errors']) == 3
        assert processor.total_processed == 0


# Performance and stress tests
class TestPerformance:
    """Performance and stress tests."""

    def test_large_dataset_processing(self):
        """Test processing performance with large dataset."""
        processor = create_default_processor()

        # Create large dataset
        large_dataset = list(range(10000))

        result = processor.process_items(large_dataset)

        assert result['count'] == 10000
        assert result['total'] == sum(range(10000))
        assert len(result['errors']) == 0

    def test_mixed_large_dataset(self):
        """Test processing performance with large mixed dataset."""
        processor = create_default_processor()

        # Create mixed dataset with some invalid items
        mixed_dataset = []
        for i in range(1000):
            if i % 100 == 0:
                mixed_dataset.append("invalid")  # 1% invalid items
            else:
                mixed_dataset.append(i)

        result = processor.process_items(mixed_dataset)

        assert result['count'] == 990  # 1000 - 10 invalid
        assert len(result['errors']) == 10
        assert processor.total_processed == 990


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
