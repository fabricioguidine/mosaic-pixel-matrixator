"""Color conversion utilities for industry-standard color systems."""

from typing import Dict


class ColorConverter:
    """Converts RGB colors to industry-standard color systems."""
    
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """
        Convert RGB to hexadecimal color code.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        
        Returns:
            Hexadecimal color code (e.g., '#FFFFFF')
        """
        r = max(0, min(255, int(r)))
        g = max(0, min(255, int(g)))
        b = max(0, min(255, int(b)))
        return f"#{r:02X}{g:02X}{b:02X}"
    
    @staticmethod
    def rgb_to_cmyk(r: int, g: int, b: int) -> Dict[str, float]:
        """
        Convert RGB to CMYK color space.
        CMYK is used in printing and paint mixing.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        
        Returns:
            Dictionary with CMYK values as percentages (0-100):
            {
                'c': cyan percentage,
                'm': magenta percentage,
                'y': yellow percentage,
                'k': black (key) percentage
            }
        """
        # Normalize RGB to 0-1
        r_norm = max(0, min(255, int(r))) / 255.0
        g_norm = max(0, min(255, int(g))) / 255.0
        b_norm = max(0, min(255, int(b))) / 255.0
        
        # Calculate CMYK
        # K (black) is 1 minus the maximum of R, G, B
        k = 1.0 - max(r_norm, g_norm, b_norm)
        
        if k == 1.0:
            # Pure black
            return {'c': 0.0, 'm': 0.0, 'y': 0.0, 'k': 100.0}
        
        # Calculate C, M, Y when K < 1.0
        # Formula: component = (1 - rgb_norm - k) / (1 - k)
        c = (1.0 - r_norm - k) / (1.0 - k) if (1.0 - k) > 0 else 0.0
        m = (1.0 - g_norm - k) / (1.0 - k) if (1.0 - k) > 0 else 0.0
        y = (1.0 - b_norm - k) / (1.0 - k) if (1.0 - k) > 0 else 0.0
        
        # Ensure values are in valid range [0, 1]
        c = max(0.0, min(1.0, c))
        m = max(0.0, min(1.0, m))
        y = max(0.0, min(1.0, y))
        
        # Convert to percentages and round
        return {
            'c': round(c * 100.0, 1),
            'm': round(m * 100.0, 1),
            'y': round(y * 100.0, 1),
            'k': round(k * 100.0, 1)
        }
    
    @staticmethod
    def rgb_to_hsl(r: int, g: int, b: int) -> Dict[str, float]:
        """
        Convert RGB to HSL color space.
        HSL (Hue, Saturation, Lightness) is intuitive for color mixing.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        
        Returns:
            Dictionary with HSL values:
            {
                'h': hue (0-360 degrees),
                's': saturation (0-100%),
                'l': lightness (0-100%)
            }
        """
        # Normalize RGB to 0-1
        r_norm = max(0, min(255, int(r))) / 255.0
        g_norm = max(0, min(255, int(g))) / 255.0
        b_norm = max(0, min(255, int(b))) / 255.0
        
        max_val = max(r_norm, g_norm, b_norm)
        min_val = min(r_norm, g_norm, b_norm)
        delta = max_val - min_val
        
        # Lightness
        l = (max_val + min_val) / 2.0
        
        # Saturation
        if delta == 0:
            s = 0.0
        else:
            s = delta / (1.0 - abs(2.0 * l - 1.0))
        
        # Hue
        if delta == 0:
            h = 0.0
        elif max_val == r_norm:
            h = 60.0 * (((g_norm - b_norm) / delta) % 6)
        elif max_val == g_norm:
            h = 60.0 * (((b_norm - r_norm) / delta) + 2)
        else:  # max_val == b_norm
            h = 60.0 * (((r_norm - g_norm) / delta) + 4)
        
        # Ensure hue is positive
        if h < 0:
            h += 360.0
        
        return {
            'h': round(h, 1),
            's': round(s * 100.0, 1),
            'l': round(l * 100.0, 1)
        }
    
    @staticmethod
    def get_industry_standards(r: int, g: int, b: int) -> Dict:
        """
        Get all industry-standard color representations for a given RGB color.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        
        Returns:
            Dictionary with all color system representations:
            {
                'rgb': [r, g, b],
                'hex': '#RRGGBB',
                'cmyk': {'c': %, 'm': %, 'y': %, 'k': %},
                'hsl': {'h': degrees, 's': %, 'l': %},
                'rgb_pct': {'r': %, 'g': %, 'b': %}  # For digital reference
            }
        """
        cmyk = ColorConverter.rgb_to_cmyk(r, g, b)
        hsl = ColorConverter.rgb_to_hsl(r, g, b)
        hex_code = ColorConverter.rgb_to_hex(r, g, b)
        
        # RGB percentages (for digital reference)
        rgb_pct = {
            'r': round((r / 255.0) * 100.0, 1),
            'g': round((g / 255.0) * 100.0, 1),
            'b': round((b / 255.0) * 100.0, 1)
        }
        
        return {
            'rgb': [int(r), int(g), int(b)],
            'hex': hex_code,
            'cmyk': cmyk,
            'hsl': hsl,
            'rgb_pct': rgb_pct  # Keep for backward compatibility
        }

