"""Tests for color conversion operations."""

import unittest
from src.quantization.color_converter import ColorConverter


class TestColorConverter(unittest.TestCase):
    """Test color conversion functions."""
    
    def test_rgb_to_hex(self):
        """Test RGB to hexadecimal conversion."""
        hex_code = ColorConverter.rgb_to_hex(255, 255, 255)
        self.assertEqual(hex_code, '#FFFFFF')
        
        hex_code = ColorConverter.rgb_to_hex(0, 0, 0)
        self.assertEqual(hex_code, '#000000')
        
        hex_code = ColorConverter.rgb_to_hex(255, 0, 128)
        self.assertEqual(hex_code, '#FF0080')
    
    def test_rgb_to_hex_clamping(self):
        """Test that values are clamped to valid range."""
        hex_code = ColorConverter.rgb_to_hex(300, -10, 128)
        self.assertEqual(hex_code, '#FF0080')
    
    def test_rgb_to_cmyk_white(self):
        """Test RGB to CMYK conversion for white."""
        cmyk = ColorConverter.rgb_to_cmyk(255, 255, 255)
        self.assertEqual(cmyk['c'], 0.0)
        self.assertEqual(cmyk['m'], 0.0)
        self.assertEqual(cmyk['y'], 0.0)
        self.assertEqual(cmyk['k'], 0.0)
    
    def test_rgb_to_cmyk_black(self):
        """Test RGB to CMYK conversion for black."""
        cmyk = ColorConverter.rgb_to_cmyk(0, 0, 0)
        self.assertEqual(cmyk['k'], 100.0)
    
    def test_rgb_to_cmyk_red(self):
        """Test RGB to CMYK conversion for red."""
        cmyk = ColorConverter.rgb_to_cmyk(255, 0, 0)
        self.assertEqual(cmyk['c'], 0.0)
        self.assertEqual(cmyk['m'], 100.0)
        self.assertEqual(cmyk['y'], 100.0)
        self.assertGreater(cmyk['k'], 0.0)
    
    def test_rgb_to_hsl(self):
        """Test RGB to HSL conversion."""
        hsl = ColorConverter.rgb_to_hsl(255, 255, 255)
        self.assertEqual(hsl['s'], 0.0)
        self.assertEqual(hsl['l'], 100.0)
        
        hsl = ColorConverter.rgb_to_hsl(0, 0, 0)
        self.assertEqual(hsl['l'], 0.0)
    
    def test_get_industry_standards(self):
        """Test getting all industry-standard color representations."""
        standards = ColorConverter.get_industry_standards(255, 255, 255)
        
        self.assertIn('rgb', standards)
        self.assertIn('hex', standards)
        self.assertIn('cmyk', standards)
        self.assertIn('hsl', standards)
        self.assertEqual(standards['hex'], '#FFFFFF')
        self.assertEqual(standards['cmyk']['k'], 0.0)


if __name__ == '__main__':
    unittest.main()

