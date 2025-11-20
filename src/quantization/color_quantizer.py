"""Color quantization to reduce palette to mixable ceramic tile colors."""

import numpy as np
from typing import Optional


class ColorQuantizer:
    """
    Quantizes RGB colors to a limited palette.
    Maps each color to the closest available color in the palette,
    ensuring colors are similar and easy to obtain for ceramic tiles.
    """
    
    def __init__(self, num_colors: int = 32):
        """
        Initialize the color quantizer.
        
        Args:
            num_colors: Number of colors in the reduced palette (default: 32)
                       Lower values mean fewer colors, more mixable tiles
        """
        self.num_colors = num_colors
        self.palette: Optional[np.ndarray] = None
        self._create_palette()
    
    def _create_palette(self):
        """
        Create a palette of easily obtainable colors.
        Uses a grid-based approach with colors evenly distributed in RGB space.
        """
        # Calculate levels for each channel to create a grid
        levels = max(2, int(np.cbrt(self.num_colors)))  # At least 2 levels
        step = 255 / (levels - 1)
        
        palette = []
        for r_level in range(levels):
            for g_level in range(levels):
                for b_level in range(levels):
                    r = int(r_level * step)
                    g = int(g_level * step)
                    b = int(b_level * step)
                    # Clamp to valid RGB range
                    r = min(255, max(0, r))
                    g = min(255, max(0, g))
                    b = min(255, max(0, b))
                    palette.append([r, g, b])
        
        # Limit to requested number of colors
        self.palette = np.array(palette[:self.num_colors], dtype=np.float32)
    
    def _find_closest_color(self, color: np.ndarray) -> np.ndarray:
        """
        Find the closest color in the palette using Euclidean distance in RGB space.
        
        Args:
            color: RGB color array of shape (3,)
        
        Returns:
            Closest color from palette
        """
        # Calculate Euclidean distance to all colors in palette
        distances = np.sqrt(np.sum((self.palette - color) ** 2, axis=1))
        
        # Find index of closest color
        closest_idx = np.argmin(distances)
        
        return self.palette[closest_idx]
    
    def quantize_color(self, color: np.ndarray) -> np.ndarray:
        """
        Quantize a single color to the closest palette color.
        
        Args:
            color: RGB color array of shape (3,)
        
        Returns:
            Quantized color from palette
        """
        return self._find_closest_color(color)
    
    def quantize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """
        Quantize a color matrix to reduce color variations.
        Maps each pixel's color to the closest color in the palette.
        
        Args:
            matrix: RGB matrix of shape (rows, cols, 3)
        
        Returns:
            Quantized matrix with reduced color palette
        """
        # Get shape
        rows, cols, channels = matrix.shape
        
        # Reshape to 2D array (pixels, channels)
        pixels = matrix.reshape(-1, 3).astype(np.float32)
        
        # Find closest color for each pixel
        quantized_pixels = np.array([
            self._find_closest_color(pixel) for pixel in pixels
        ])
        
        # Reshape back to original shape
        quantized_matrix = quantized_pixels.reshape(rows, cols, channels)
        
        return quantized_matrix.astype(np.uint8)
    
    def get_palette(self) -> np.ndarray:
        """
        Get the current color palette.
        
        Returns:
            Array of palette colors (num_colors, 3)
        """
        return self.palette.astype(np.uint8)
