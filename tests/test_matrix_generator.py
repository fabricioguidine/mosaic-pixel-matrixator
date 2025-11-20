"""Tests for matrix generation operations."""

import unittest
import numpy as np
from PIL import Image
from src.generation.matrix_generator import MatrixGenerator
from src.config.constants import TILE_SIZE_CM


class TestMatrixGenerator(unittest.TestCase):
    """Test matrix generation functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = MatrixGenerator(tile_size_cm=2.2)
        self.test_image = Image.new('RGB', (200, 100), color='green')
    
    def test_generator_initialization(self):
        """Test generator initialization with default tile size."""
        generator = MatrixGenerator()
        self.assertEqual(generator.tile_size_cm, TILE_SIZE_CM)
    
    def test_calculate_matrix_dimensions(self):
        """Test matrix dimension calculation."""
        rows, cols = self.generator.calculate_matrix_dimensions(220, 110)
        # 220cm / 2.2cm ≈ 100 columns, 110cm / 2.2cm ≈ 50 rows
        # Using approximate values due to floating point precision
        self.assertAlmostEqual(cols, 100, delta=1)
        self.assertAlmostEqual(rows, 50, delta=1)
    
    def test_calculate_dimensions_preserving_aspect_ratio(self):
        """Test dimension calculation preserving aspect ratio."""
        # Image is 200x100, aspect ratio = 2.0
        # Request 200x150 -> Option 1: 200x100, Option 2: 300x150
        # Option 1 total diff: 0 + 50 = 50
        # Option 2 total diff: 100 + 0 = 100
        # Should choose Option 1 (fit to width)
        width, height, width_diff, height_diff = self.generator.calculate_dimensions_preserving_aspect_ratio(
            self.test_image, 200, 150
        )
        self.assertEqual(width, 200)
        self.assertEqual(height, 100)
        self.assertEqual(width_diff, 0)
        self.assertEqual(height_diff, 50)
    
    def test_calculate_dimensions_fit_to_height(self):
        """Test dimension calculation when fitting to height is better."""
        # Image is 200x100, aspect ratio = 2.0
        # Request 100x50 -> Option 1: 100x50, Option 2: 100x50 (both same)
        # But if request 50x50 -> Option 1: 50x25, Option 2: 100x50
        # Option 1 total diff: 0 + 25 = 25
        # Option 2 total diff: 50 + 0 = 50
        # Should choose Option 1
        width, height, width_diff, height_diff = self.generator.calculate_dimensions_preserving_aspect_ratio(
            self.test_image, 50, 50
        )
        # Should fit to width (50), so height becomes 25
        self.assertEqual(width, 50)
        self.assertEqual(height, 25)
    
    def test_generate_matrix(self):
        """Test matrix generation."""
        matrix, (rows, cols), (width, height), (width_diff, height_diff) = self.generator.generate_matrix(
            self.test_image, 200, 100, preserve_aspect_ratio=True
        )
        self.assertEqual(matrix.shape[:2], (rows, cols))
        self.assertEqual(matrix.shape[2], 3)  # RGB channels
    
    def test_get_matrix_info(self):
        """Test getting matrix information."""
        matrix, (rows, cols), _, _ = self.generator.generate_matrix(
            self.test_image, 220, 110, preserve_aspect_ratio=False
        )
        info = self.generator.get_matrix_info(matrix)
        
        self.assertEqual(info['matrix_rows'], rows)
        self.assertEqual(info['matrix_columns'], cols)
        self.assertEqual(info['total_tiles'], rows * cols)
        self.assertEqual(info['tile_size_cm'], 2.2)
        self.assertEqual(info['color_format'], 'RGB')


if __name__ == '__main__':
    unittest.main()

