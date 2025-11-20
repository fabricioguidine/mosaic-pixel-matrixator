"""Primary color mix representation with industry-standard formats."""

from .color_converter import ColorConverter


class ColorMixer:
    """Represents RGB colors with industry-standard color systems for paint purchasing."""
    
    # Primary colors in RGB space
    PRIMARY_RED = np.array([255, 0, 0], dtype=np.uint8)
    PRIMARY_GREEN = np.array([0, 255, 0], dtype=np.uint8)
    PRIMARY_BLUE = np.array([0, 0, 255], dtype=np.uint8)
    
    @classmethod
    def get_primary_mix(cls, r: int, g: int, b: int) -> dict:
        """
        Get industry-standard color information for an RGB color.
        Includes CMYK (for paint/printing) and Hex (for digital reference).
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        
        Returns:
            Dictionary with industry-standard color information:
            {
                'rgb': [r, g, b],
                'hex': '#RRGGBB' (hexadecimal code),
                'cmyk': {'c': cyan%, 'm': magenta%, 'y': yellow%, 'k': black%},
                'hsl': {'h': hue, 's': saturation%, 'l': lightness%}
            }
        """
        # Get all industry standards
        standards = ColorConverter.get_industry_standards(r, g, b)
        
        return standards
    
    @classmethod
    def format_primary_mix_text(cls, r: int, g: int, b: int) -> str:
        """
        Format RGB with CMYK paint mixing information.
        
        Args:
            r: Red value
            g: Green value
            b: Blue value
        
        Returns:
            Formatted string: "R,G,B[C:c%,M:m%,Y:y%,K:k%] #HEX"
        """
        mix = cls.get_primary_mix(r, g, b)
        cmyk = mix['cmyk']
        hex_code = mix['hex']
        return f"{int(r)},{int(g)},{int(b)}[C:{cmyk['c']:.1f}%,M:{cmyk['m']:.1f}%,Y:{cmyk['y']:.1f}%,K:{cmyk['k']:.1f}%] {hex_code}"
    
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

