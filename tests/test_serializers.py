from django.test import TestCase
from django_logger_panel.core import get_all_loggers, LEVELS
from django_logger_panel.serializers import (
    logger_serializer,
    logger_list_serializer,
    logger_response_serializer,
    log_level_serializer,
)


class SerializerTestCase(TestCase):
    """Test suite for serializers."""

    def setUp(self):
        """Define the test variables."""
        self.loggers = get_all_loggers()

    def test_logger_serializer(self):
        """Test the logger_serializer() result schema."""
        serialized = logger_serializer(self.loggers.get("root"))
        expected = {
            "effectiveLevel": {"code": 30, "name": "WARNING"},
            "level": {"code": 30, "name": "WARNING"},
            "name": "root",
            "parent": None,
        }
        self.assertDictEqual(serialized, expected)

    def test_logger_list_serializer(self):
        """Test the logger_list_serializer() result schema."""
        serialized = logger_list_serializer(self.loggers)
        for logger in serialized:
            self.assertIsInstance(logger["effectiveLevel"], dict)
            self.assertIsInstance(logger["effectiveLevel"]["code"], int)
            self.assertIsInstance(logger["effectiveLevel"]["name"], str)
            self.assertIsInstance(logger["level"], dict)
            self.assertIsInstance(logger["level"]["code"], int)
            self.assertIsInstance(logger["level"]["name"], str)
            self.assertIsInstance(logger["name"], str)
            self.assertIsInstance(logger["parent"], (str, type(None)))

    def test_log_level_serializer(self):
        """Test the log_level_serializer() result schema."""
        serialized = log_level_serializer(LEVELS["DEBUG"])
        self.assertIsInstance(serialized["code"], int)
        self.assertIsInstance(serialized["name"], str)

    def test_logger_response_serializer(self):
        """Test the logger_response_serializer() result schema."""
        serialized = logger_response_serializer(LEVELS, self.loggers)
        self.assertIsInstance(serialized["log_levels"], dict)
        self.assertIsInstance(serialized["loggers"], list)
