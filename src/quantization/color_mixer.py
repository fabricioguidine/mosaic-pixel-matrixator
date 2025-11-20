"""Primary color mix representation for RGB values."""

import numpy as np
from typing import Tuple


class ColorMixer:
    """Represents RGB colors as a mix of three primary colors (Red, Green, Blue)."""
    
    # Primary colors in RGB space
    PRIMARY_RED = np.array([255, 0, 0], dtype=np.uint8)
    PRIMARY_GREEN = np.array([0, 255, 0], dtype=np.uint8)
    PRIMARY_BLUE = np.array([0, 0, 255], dtype=np.uint8)
    
    @classmethod
    def get_primary_mix(cls, r: int, g: int, b: int) -> dict:
        """
        Get the primary color mix information for an RGB color.
        Returns the amount of Red, Green, and Blue primaries needed.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        
        Returns:
            Dictionary with primary color mix information:
            {
                'rgb': [r, g, b],
                'red': r_value (0-255),
                'green': g_value (0-255),
                'blue': b_value (0-255),
                'red_pct': red_percentage (0-100),
                'green_pct': green_percentage (0-100),
                'blue_pct': blue_percentage (0-100)
            }
        """
        # Clamp values to valid range
        r = int(max(0, min(255, r)))
        g = int(max(0, min(255, g)))
        b = int(max(0, min(255, b)))
        
        # Calculate percentages (how much of each primary color)
        red_pct = round((r / 255.0) * 100, 1)
        green_pct = round((g / 255.0) * 100, 1)
        blue_pct = round((b / 255.0) * 100, 1)
        
        return {
            'rgb': [r, g, b],
            'red': r,
            'green': g,
            'blue': b,
            'red_pct': red_pct,
            'green_pct': green_pct,
            'blue_pct': blue_pct
        }
    
    @classmethod
    def format_primary_mix_text(cls, r: int, g: int, b: int) -> str:
        """
        Format RGB with primary color mix information.
        
        Args:
            r: Red value
            g: Green value
            b: Blue value
        
        Returns:
            Formatted string: "R,G,B[R:r%,G:g%,B:b%]"
        """
        mix = cls.get_primary_mix(r, g, b)
        return f"{int(r)},{int(g)},{int(b)}[R:{mix['red_pct']:.1f}%,G:{mix['green_pct']:.1f}%,B:{mix['blue_pct']:.1f}%]"
    
    @classmethod
    def format_primary_mix_compact(cls, r: int, g: int, b: int) -> str:
        """
        Format RGB with compact primary color mix information.
        
        Args:
            r: Red value
            g: Green value
            b: Blue value
        
        Returns:
            Formatted string: "R,G,B[R:r,G:g,B:b]"
        """
        return f"{int(r)},{int(g)},{int(b)}[R:{int(r)},G:{int(g)},B:{int(b)}]"

