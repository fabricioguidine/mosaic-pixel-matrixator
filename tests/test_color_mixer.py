"""Tests for color mixing operations."""

import unittest
from src.quantization.color_mixer import ColorMixer


class TestColorMixer(unittest.TestCase):
    """Test color mixing functions."""
    
    def test_get_primary_mix(self):
        """Test getting primary color mix information."""
        mix = ColorMixer.get_primary_mix(200, 100, 50)
        
        self.assertEqual(mix['rgb'], [200, 100, 50])
        self.assertIn('hex', mix)
        self.assertIn('cmyk', mix)
        self.assertIn('hsl', mix)
        self.assertEqual(mix['hex'], '#C86432')
    
    def test_format_primary_mix_text(self):
        """Test formatting primary mix as text with CMYK."""
        formatted = ColorMixer.format_primary_mix_text(200, 100, 50)
        
        self.assertIn('200,100,50', formatted)
        self.assertIn('C:', formatted)
        self.assertIn('M:', formatted)
        self.assertIn('Y:', formatted)
        self.assertIn('K:', formatted)
        self.assertIn('#', formatted)  # Hex code
    
    def test_format_primary_mix_compact(self):
        """Test compact formatting of primary mix."""
        formatted = ColorMixer.format_primary_mix_compact(200, 100, 50)
        
        self.assertIn('200,100,50', formatted)
        self.assertIn('R:200', formatted)
        self.assertIn('G:100', formatted)
        self.assertIn('B:50', formatted)
    
    def test_primary_mix_cmyk(self):
        """Test that CMYK values are calculated correctly."""
        mix = ColorMixer.get_primary_mix(255, 255, 255)  # White
        
        # White should have all CMYK at 0%
        self.assertEqual(mix['cmyk']['c'], 0.0)
        self.assertEqual(mix['cmyk']['m'], 0.0)
        self.assertEqual(mix['cmyk']['y'], 0.0)
        self.assertEqual(mix['cmyk']['k'], 0.0)
    
    def test_primary_mix_clamping(self):
        """Test that RGB values are clamped to valid range."""
        mix = ColorMixer.get_primary_mix(300, -10, 128)
        
        # Values should be clamped to 0-255
        self.assertEqual(mix['rgb'][0], 255)
        self.assertEqual(mix['rgb'][1], 0)
        self.assertEqual(mix['rgb'][2], 128)


if __name__ == '__main__':
    unittest.main()

