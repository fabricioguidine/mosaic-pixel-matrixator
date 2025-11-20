"""Tests for color mixing operations."""

import unittest
from src.quantization.color_mixer import ColorMixer


class TestColorMixer(unittest.TestCase):
    """Test color mixing functions."""
    
    def test_get_primary_mix(self):
        """Test getting primary color mix information."""
        mix = ColorMixer.get_primary_mix(200, 100, 50)
        
        self.assertEqual(mix['rgb'], [200, 100, 50])
        self.assertEqual(mix['red'], 200)
        self.assertEqual(mix['green'], 100)
        self.assertEqual(mix['blue'], 50)
        self.assertIn('red_pct', mix)
        self.assertIn('green_pct', mix)
        self.assertIn('blue_pct', mix)
    
    def test_format_primary_mix_text(self):
        """Test formatting primary mix as text."""
        formatted = ColorMixer.format_primary_mix_text(200, 100, 50)
        
        self.assertIn('200,100,50', formatted)
        self.assertIn('R:', formatted)
        self.assertIn('G:', formatted)
        self.assertIn('B:', formatted)
        self.assertIn('%', formatted)
    
    def test_format_primary_mix_compact(self):
        """Test compact formatting of primary mix."""
        formatted = ColorMixer.format_primary_mix_compact(200, 100, 50)
        
        self.assertIn('200,100,50', formatted)
        self.assertIn('R:200', formatted)
        self.assertIn('G:100', formatted)
        self.assertIn('B:50', formatted)
    
    def test_primary_mix_percentages(self):
        """Test that percentages are calculated correctly."""
        mix = ColorMixer.get_primary_mix(255, 128, 0)
        
        # White should be 100%
        self.assertAlmostEqual(mix['red_pct'], 100.0, places=1)
        self.assertAlmostEqual(mix['green_pct'], 50.2, places=1)
        self.assertAlmostEqual(mix['blue_pct'], 0.0, places=1)
    
    def test_primary_mix_clamping(self):
        """Test that values are clamped to valid range."""
        mix = ColorMixer.get_primary_mix(300, -10, 128)
        
        self.assertEqual(mix['red'], 255)
        self.assertEqual(mix['green'], 0)
        self.assertEqual(mix['blue'], 128)


if __name__ == '__main__':
    unittest.main()

