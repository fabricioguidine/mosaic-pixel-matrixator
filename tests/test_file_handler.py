"""Tests for file handling operations."""

import unittest
import tempfile
import json
import os
from pathlib import Path
import numpy as np
from src.io.file_handler import save_matrix_to_file, save_matrix_to_json


class TestFileHandler(unittest.TestCase):
    """Test file handling functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_matrix = np.array([
            [[255, 128, 64], [200, 100, 50]],
            [[100, 50, 25], [75, 37, 18]]
        ], dtype=np.uint8)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_save_matrix_to_file(self):
        """Test saving matrix to text file with mixing instructions."""
        output_path = Path(self.test_dir) / 'test_matrix.txt'
        save_matrix_to_file(self.test_matrix, str(output_path))
        
        self.assertTrue(output_path.exists())
        
        content = output_path.read_text()
        self.assertIn('RGB Color Matrix with Paint Mixing Instructions', content)
        self.assertIn('2 rows x 2 columns', content)
        self.assertIn('255,128,64', content)
        self.assertIn('BASE COLORS TO PURCHASE', content)
        self.assertIn('Mix:', content)
    
    def test_save_matrix_to_json(self):
        """Test saving matrix to JSON file."""
        output_path = Path(self.test_dir) / 'test_matrix.json'
        save_matrix_to_json(self.test_matrix, str(output_path))
        
        self.assertTrue(output_path.exists())
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(data['dimensions']['rows'], 2)
        self.assertEqual(data['dimensions']['columns'], 2)
        self.assertEqual(len(data['matrix']), 2)
        self.assertEqual(len(data['matrix'][0]), 2)
        # Updated format includes industry-standard color info
        self.assertIn('rgb', data['matrix'][0][0])
        self.assertIn('hex', data['matrix'][0][0])
        self.assertIn('cmyk', data['matrix'][0][0])
        self.assertIn('hsl', data['matrix'][0][0])
        self.assertEqual(data['matrix'][0][0]['rgb'], [255, 128, 64])
    
    def test_save_matrix_creates_directory(self):
        """Test that save functions create directories if they don't exist."""
        nested_path = Path(self.test_dir) / 'nested' / 'deep' / 'matrix.txt'
        save_matrix_to_file(self.test_matrix, str(nested_path))
        
        self.assertTrue(nested_path.exists())
        self.assertTrue(nested_path.parent.exists())


if __name__ == '__main__':
    unittest.main()

