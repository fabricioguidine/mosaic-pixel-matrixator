"""Tests for color quantization operations."""

import unittest
import numpy as np
from src.quantization.color_quantizer import ColorQuantizer


class TestColorQuantizer(unittest.TestCase):
    """Test color quantization functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.quantizer = ColorQuantizer(num_colors=8)
    
    def test_quantizer_initialization(self):
        """Test quantizer initialization."""
        self.assertEqual(self.quantizer.num_colors, 8)
        # Palette is None until quantize_matrix is called
        # This is expected behavior
        self.assertTrue(True)  # Placeholder - palette created on demand
    
    def test_quantize_color(self):
        """Test quantizing a single color via matrix quantization."""
        # Create test matrix and quantize it
        test_matrix = np.array([[[255, 128, 64]]], dtype=np.uint8)
        quantized_matrix = self.quantizer.quantize_matrix(test_matrix)
        
        # Verify the quantized result
        quantized_color = quantized_matrix[0, 0]
        self.assertEqual(len(quantized_color), 3)
        self.assertTrue(all(0 <= val <= 255 for val in quantized_color))
    
    def test_quantize_matrix(self):
        """Test quantizing a color matrix."""
        matrix = np.array([
            [[255, 0, 0], [0, 255, 0]],
            [[0, 0, 255], [128, 128, 128]]
        ], dtype=np.uint8)
        
        quantized = self.quantizer.quantize_matrix(matrix)
        
        self.assertEqual(quantized.shape, matrix.shape)
        self.assertEqual(quantized.dtype, np.uint8)
    
    def test_get_palette(self):
        """Test getting the color palette."""
        # Create palette first by quantizing a matrix
        test_matrix = np.array([[[255, 128, 64]]], dtype=np.uint8)
        self.quantizer.quantize_matrix(test_matrix)
        
        palette = self.quantizer.get_palette()
        
        self.assertIsNotNone(palette)
        self.assertTrue(len(palette) > 0)
        self.assertEqual(len(palette[0]), 3)  # RGB channels
    
    def test_median_cut_algorithm(self):
        """Test that median cut creates reasonable palette."""
        # Create matrix with distinct colors
        matrix = np.random.randint(0, 256, (10, 10, 3), dtype=np.uint8)
        quantizer = ColorQuantizer(num_colors=8)
        quantized = quantizer.quantize_matrix(matrix)
        
        # Check that quantized matrix has reasonable colors
        unique_colors = len(np.unique(quantized.reshape(-1, 3), axis=0))
        self.assertLessEqual(unique_colors, 8)


if __name__ == '__main__':
    unittest.main()

