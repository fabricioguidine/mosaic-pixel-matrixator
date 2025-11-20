"""Tests for paint color inventory operations."""

import unittest
import numpy as np
from src.quantization.paint_colors import PaintColorInventory


class TestPaintColorInventory(unittest.TestCase):
    """Test paint color inventory functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.inventory = PaintColorInventory()
    
    def test_add_color(self):
        """Test adding colors to inventory."""
        self.inventory.add_color(255, 0, 0)
        self.inventory.add_color(0, 255, 0)
        
        self.assertEqual(self.inventory.get_unique_colors_count(), 2)
    
    def test_add_duplicate_colors(self):
        """Test that duplicate colors increment count."""
        self.inventory.add_color(255, 0, 0)
        self.inventory.add_color(255, 0, 0)
        self.inventory.add_color(255, 0, 0)
        
        self.assertEqual(self.inventory.get_unique_colors_count(), 1)
        self.assertEqual(self.inventory.get_total_tiles(), 3)
    
    def test_get_required_paints(self):
        """Test getting required paints list with industry standards."""
        self.inventory.add_color(255, 0, 0)
        self.inventory.add_color(0, 255, 0)
        self.inventory.add_color(255, 0, 0)  # Duplicate
        
        paints = self.inventory.get_required_paints()
        
        self.assertEqual(len(paints), 2)
        self.assertEqual(paints[0]['count'], 2)  # Red is most used
        self.assertIn('rgb', paints[0])
        self.assertIn('hex', paints[0])
        self.assertIn('cmyk', paints[0])
        self.assertIn('hsl', paints[0])
        self.assertIn('count', paints[0])
    
    def test_from_matrix(self):
        """Test creating inventory from matrix."""
        matrix = np.array([
            [[255, 0, 0], [0, 255, 0]],
            [[255, 0, 0], [128, 128, 128]]
        ], dtype=np.uint8)
        
        inventory = PaintColorInventory.from_matrix(matrix)
        
        self.assertEqual(inventory.get_unique_colors_count(), 3)
        self.assertEqual(inventory.get_total_tiles(), 4)
    
    def test_paints_sorted_by_count(self):
        """Test that paints are sorted by usage count."""
        self.inventory.add_color(255, 0, 0)  # 3 times
        self.inventory.add_color(255, 0, 0)
        self.inventory.add_color(255, 0, 0)
        self.inventory.add_color(0, 255, 0)  # 1 time
        
        paints = self.inventory.get_required_paints()
        
        self.assertEqual(paints[0]['count'], 3)
        self.assertEqual(paints[1]['count'], 1)


if __name__ == '__main__':
    unittest.main()

