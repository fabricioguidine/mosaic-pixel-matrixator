"""Color quantization using median cut algorithm for better image quality."""

import numpy as np
from typing import Optional


class ColorQuantizer:
    """
    Quantizes RGB colors using median cut algorithm.
    Creates a palette optimized for the image content, resulting in better quality.
    """
    
    def __init__(self, num_colors: int = 64):
        """
        Initialize the color quantizer.
        
        Args:
            num_colors: Number of colors in the reduced palette (default: 64)
                       Higher values preserve more color detail
        """
        self.num_colors = num_colors
        self.palette: Optional[np.ndarray] = None
    
    def _median_cut_quantize(self, pixels: np.ndarray) -> np.ndarray:
        """
        Perform median cut color quantization.
        Splits color space by the channel with greatest range, recursively.
        
        Args:
            pixels: Array of RGB pixels (N, 3)
        
        Returns:
            Palette of colors (num_colors, 3)
        """
        if len(pixels) == 0:
            return np.array([[0, 0, 0]], dtype=np.uint8)
        
        # Start with one box containing all pixels
        boxes = [pixels.copy()]
        
        # Split boxes until we have enough colors
        while len(boxes) < self.num_colors and len(boxes) > 0:
            # Find the box with the largest range
            largest_box_idx = 0
            largest_range = 0
            
            for i, box in enumerate(boxes):
                if len(box) == 0:
                    continue
                # Find the channel with the largest range
                ranges = box.max(axis=0) - box.min(axis=0)
                max_range = ranges.max()
                if max_range > largest_range:
                    largest_range = max_range
                    largest_box_idx = i
            
            # Split the largest box along the channel with the largest range
            box_to_split = boxes[largest_box_idx]
            if len(box_to_split) <= 1:
                break
            
            # Find channel with largest range
            ranges = box_to_split.max(axis=0) - box_to_split.min(axis=0)
            channel = np.argmax(ranges)
            
            # Sort by this channel
            sorted_indices = np.argsort(box_to_split[:, channel])
            sorted_box = box_to_split[sorted_indices]
            
            # Split at median
            median_idx = len(sorted_box) // 2
            box1 = sorted_box[:median_idx]
            box2 = sorted_box[median_idx:]
            
            # Replace original box with two new boxes
            boxes.pop(largest_box_idx)
            if len(box1) > 0:
                boxes.append(box1)
            if len(box2) > 0:
                boxes.append(box2)
        
        # Calculate average color for each box (this becomes our palette)
        palette = []
        for box in boxes:
            if len(box) > 0:
                avg_color = box.mean(axis=0).astype(np.uint8)
                palette.append(avg_color)
        
        # If we don't have enough colors, pad with black
        while len(palette) < self.num_colors:
            palette.append([0, 0, 0])
        
        return np.array(palette[:self.num_colors], dtype=np.uint8)
    
    def _find_closest_color(self, color: np.ndarray, palette: np.ndarray) -> np.ndarray:
        """
        Find the closest color in the palette using perceptual distance.
        Uses weighted Euclidean distance (favors perceptual similarity).
        
        Args:
            color: RGB color array of shape (3,)
            palette: Palette array of shape (N, 3)
        
        Returns:
            Closest color from palette
        """
        # Use perceptual weights (based on human eye sensitivity)
        weights = np.array([0.299, 0.587, 0.114])  # R, G, B weights for luminance
        
        # Calculate weighted squared distance
        color_float = color.astype(np.float32)
        palette_float = palette.astype(np.float32)
        
        diff = palette_float - color_float
        weighted_distances = np.sum((diff ** 2) * weights, axis=1)
        
        # Find index of closest color
        closest_idx = np.argmin(weighted_distances)
        
        return palette[closest_idx]
    
    def quantize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """
        Quantize a color matrix using median cut algorithm.
        First builds a palette optimized for the image, then maps each pixel.
        
        Args:
            matrix: RGB matrix of shape (rows, cols, 3)
        
        Returns:
            Quantized matrix with reduced color palette
        """
        # Get shape
        rows, cols, channels = matrix.shape
        
        # Reshape to 2D array (pixels, channels)
        pixels = matrix.reshape(-1, 3).astype(np.float32)
        
        # Build palette using median cut
        self.palette = self._median_cut_quantize(pixels)
        
        # Map each pixel to closest palette color
        quantized_pixels = np.array([
            self._find_closest_color(pixel, self.palette) for pixel in pixels
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
        if self.palette is None:
            return np.array([], dtype=np.uint8).reshape(0, 3)
        return self.palette.astype(np.uint8)
