"""Tests for file handling operations."""

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.io.file_handler import save_matrix_to_file, save_matrix_to_json
from src.quantization.paint_colors import PaintColorInventory


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

        content = output_path.read_text(encoding='utf-8')
        self.assertIn('RGB Color Matrix with Paint Mixing Instructions', content)
        self.assertIn('2 rows x 2 columns', content)
        self.assertIn('255,128,64', content)
        self.assertIn('BASE COLORS TO PURCHASE', content)
        self.assertIn('Mix:', content)
        # Check for tile count summary
        self.assertIn('TILES TO PAINT', content)
        self.assertIn('Total tiles', content)
        self.assertIn('Tiles', content)

    def test_save_matrix_to_json(self):
        """Test saving matrix to JSON file."""
        output_path = Path(self.test_dir) / 'test_matrix.json'
        save_matrix_to_json(self.test_matrix, str(output_path))

        self.assertTrue(output_path.exists())

        with open(output_path, encoding='utf-8') as f:
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
        # Check for tile count information
        self.assertIn('total_tiles', data)
        self.assertIn('total_unique_colors', data)
        self.assertIn('tiles_to_paint', data)
        self.assertIsInstance(data['tiles_to_paint'], list)
        if len(data['tiles_to_paint']) > 0:
            self.assertIn('tile_count', data['tiles_to_paint'][0])
            self.assertIn('percentage', data['tiles_to_paint'][0])

    def test_save_matrix_creates_directory(self):
        """Test that save functions create directories if they don't exist."""
        nested_path = Path(self.test_dir) / 'nested' / 'deep' / 'matrix.txt'
        save_matrix_to_file(self.test_matrix, str(nested_path))

        self.assertTrue(nested_path.exists())
        self.assertTrue(nested_path.parent.exists())

    def test_save_matrix_with_paint_inventory(self):
        """Test saving matrix with provided paint inventory."""
        output_path = Path(self.test_dir) / 'test_matrix.txt'
        paint_inventory = PaintColorInventory.from_matrix(self.test_matrix)

        save_matrix_to_file(self.test_matrix, str(output_path), paint_inventory=paint_inventory)

        self.assertTrue(output_path.exists())
        content = output_path.read_text(encoding='utf-8')
        # Verify tile count information is present
        self.assertIn('TILES TO PAINT', content)
        self.assertIn('Total tiles', content)

        # Test JSON with paint inventory
        json_path = Path(self.test_dir) / 'test_matrix.json'
        save_matrix_to_json(self.test_matrix, str(json_path), paint_inventory=paint_inventory)

        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)

        self.assertIn('total_tiles', data)
        self.assertIn('tiles_to_paint', data)
        self.assertEqual(data['total_tiles'], 4)  # 2x2 matrix = 4 tiles


if __name__ == '__main__':
    unittest.main()

