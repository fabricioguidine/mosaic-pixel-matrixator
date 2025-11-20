"""Tests for color base selection operations."""

import unittest
import numpy as np
from src.quantization.color_base_selector import ColorBaseSelector


class TestColorBaseSelector(unittest.TestCase):
    """Test color base selection functions."""
    
    def test_select_base_colors(self):
        """Test selecting base colors."""
        matrix = np.array([
            [[255, 0, 0], [0, 255, 0]],
            [[0, 0, 255], [255, 255, 255]]
        ], dtype=np.uint8)
        
        base_colors = ColorBaseSelector.select_base_colors(matrix)
        
        # Should have 5 base colors: cyan, magenta, yellow, black, white
        self.assertEqual(len(base_colors), 5)
        
        # Check that all have required fields
        for base in base_colors:
            self.assertIn('name', base)
            self.assertIn('rgb', base)
            self.assertIn('hex', base)
            self.assertIn('cmyk', base)
            self.assertTrue(base.get('purchase', False))
    
    def test_calculate_mix_instructions(self):
        """Test calculating mix instructions."""
        base_colors = ColorBaseSelector.select_base_colors(
            np.array([[[255, 0, 0]]], dtype=np.uint8)
        )
        
        # Test mixing red (CMYK: 0, 100, 100, 0)
        target_cmyk = {'c': 0.0, 'm': 100.0, 'y': 100.0, 'k': 0.0}
        mix_info = ColorBaseSelector.calculate_mix_instructions(target_cmyk, base_colors)
        
        self.assertIn('mix', mix_info)
        self.assertIn('instruction', mix_info)
        self.assertIn('magenta', mix_info['instruction'].lower())
        self.assertIn('yellow', mix_info['instruction'].lower())
    
    def test_calculate_mix_instructions_white(self):
        """Test mixing white color."""
        base_colors = ColorBaseSelector.select_base_colors(
            np.array([[[255, 255, 255]]], dtype=np.uint8)
        )
        
        target_cmyk = {'c': 0.0, 'm': 0.0, 'y': 0.0, 'k': 0.0}
        mix_info = ColorBaseSelector.calculate_mix_instructions(target_cmyk, base_colors)
        
        self.assertIn('white', mix_info['instruction'].lower())


if __name__ == '__main__':
    unittest.main()

