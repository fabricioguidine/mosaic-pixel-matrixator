"""Tests for configuration constants."""

import unittest
from src.config.constants import TILE_SIZE_CM, SUPPORTED_IMAGE_FORMATS


class TestConfig(unittest.TestCase):
    """Test configuration constants."""
    
    def test_tile_size_cm_default(self):
        """Test that default tile size is 2.2cm."""
        self.assertEqual(TILE_SIZE_CM, 2.2)
    
    def test_tile_size_cm_is_positive(self):
        """Test that tile size is a positive number."""
        self.assertGreater(TILE_SIZE_CM, 0)
    
    def test_supported_formats_is_set(self):
        """Test that supported formats is a set."""
        self.assertIsInstance(SUPPORTED_IMAGE_FORMATS, set)
    
    def test_supported_formats_includes_common_formats(self):
        """Test that common image formats are supported."""
        expected_formats = {'.jpg', '.jpeg', '.png'}
        self.assertTrue(expected_formats.issubset(SUPPORTED_IMAGE_FORMATS))
    
    def test_supported_formats_case_insensitive(self):
        """Test that format extensions are in lowercase."""
        for fmt in SUPPORTED_IMAGE_FORMATS:
            self.assertEqual(fmt, fmt.lower())


if __name__ == '__main__':
    unittest.main()

