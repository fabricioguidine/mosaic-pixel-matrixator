"""Tests for image visualization operations."""

import unittest
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from src.visualization.image_recreator import recreate_image_from_matrix


class TestVisualization(unittest.TestCase):
    """Test visualization functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        # Create a small test matrix (5x5x3)
        self.test_matrix = np.array([
            [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255]],
            [[0, 255, 255], [128, 128, 128], [255, 128, 0], [128, 0, 255], [0, 128, 255]],
            [[255, 255, 255], [0, 0, 0], [128, 128, 0], [128, 0, 128], [0, 128, 128]],
            [[200, 100, 50], [50, 200, 100], [100, 50, 200], [150, 150, 150], [75, 75, 75]],
            [[255, 200, 150], [150, 255, 200], [200, 150, 255], [180, 180, 180], [90, 90, 90]]
        ], dtype=np.uint8)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_recreate_image_from_matrix(self):
        """Test recreating image from matrix."""
        output_path = Path(self.test_dir) / 'test_preview.png'
        recreate_image_from_matrix(self.test_matrix, str(output_path))
        
        self.assertTrue(output_path.exists())
        
        # Load the saved image and verify it
        img = Image.open(output_path)
        self.assertEqual(img.mode, 'RGB')
    
    def test_recreate_image_with_scale_factor(self):
        """Test recreating image with scale factor."""
        output_path = Path(self.test_dir) / 'test_preview_scaled.png'
        recreate_image_from_matrix(self.test_matrix, str(output_path), scale_factor=10)
        
        self.assertTrue(output_path.exists())
        
        img = Image.open(output_path)
        # Original matrix is 5x5, scaled by 10 should be 50x50
        self.assertEqual(img.size, (50, 50))
    
    def test_recreate_image_without_scale(self):
        """Test recreating image without scaling."""
        output_path = Path(self.test_dir) / 'test_preview_no_scale.png'
        recreate_image_from_matrix(self.test_matrix, str(output_path), scale_factor=1)
        
        self.assertTrue(output_path.exists())
        
        img = Image.open(output_path)
        # Should be original matrix size
        self.assertEqual(img.size, (5, 5))


if __name__ == '__main__':
    unittest.main()

