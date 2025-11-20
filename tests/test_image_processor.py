"""Tests for image processing operations."""

import unittest
import numpy as np
from PIL import Image
from src.processing.image_processor import ImageProcessor
from src.config.constants import TILE_SIZE_CM


class TestImageProcessor(unittest.TestCase):
    """Test image processing functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = ImageProcessor(tile_size_cm=2.2)
        self.test_image = Image.new('RGB', (200, 100), color='blue')
    
    def test_processor_initialization(self):
        """Test processor initialization with default tile size."""
        processor = ImageProcessor()
        self.assertEqual(processor.tile_size_cm, TILE_SIZE_CM)
    
    def test_processor_custom_tile_size(self):
        """Test processor initialization with custom tile size."""
        processor = ImageProcessor(tile_size_cm=3.0)
        self.assertEqual(processor.tile_size_cm, 3.0)
    
    def test_convert_to_rgb_already_rgb(self):
        """Test converting RGB image to RGB (should return same)."""
        rgb_image = Image.new('RGB', (100, 100), color='red')
        result = self.processor.convert_to_rgb(rgb_image)
        self.assertEqual(result.mode, 'RGB')
    
    def test_resize_image(self):
        """Test image resizing."""
        resized = self.processor.resize_image(self.test_image, 50, 100)
        self.assertEqual(resized.size, (100, 50))  # (width, height)
    
    def test_image_to_array_correct_shape(self):
        """Test image to array conversion produces correct shape."""
        rows, cols = 10, 20
        array = self.processor.image_to_array(self.test_image, rows, cols)
        self.assertEqual(array.shape, (rows, cols, 3))
    
    def test_image_to_array_rgb_values(self):
        """Test that array contains valid RGB values."""
        rows, cols = 5, 5
        array = self.processor.image_to_array(self.test_image, rows, cols)
        # Check that all values are in valid RGB range (0-255)
        self.assertTrue(np.all(array >= 0))
        self.assertTrue(np.all(array <= 255))
    
    def test_image_to_array_dtype(self):
        """Test that array has correct dtype."""
        rows, cols = 5, 5
        array = self.processor.image_to_array(self.test_image, rows, cols)
        # Should be uint8 for RGB values
        self.assertIn(array.dtype, [np.uint8, np.int64, np.int32])


if __name__ == '__main__':
    unittest.main()

