"""Image processing operations for resizing and converting images."""

import numpy as np
from PIL import Image
from typing import Tuple
from src.config.constants import TILE_SIZE_CM


class ImageProcessor:
    """Processes images for tile matrix conversion."""
    
    def __init__(self, tile_size_cm: float = TILE_SIZE_CM):
        """
        Initialize the image processor.
        
        Args:
            tile_size_cm: Size of each tile in centimeters (default: 2.0cm)
        """
        self.tile_size_cm = tile_size_cm
    
    def resize_image(self, image: Image.Image, target_rows: int, target_cols: int) -> Image.Image:
        """
        Resize image to match the target matrix dimensions.
        
        Args:
            image: Input PIL Image
            target_rows: Number of rows in the output matrix
            target_cols: Number of columns in the output matrix
        
        Returns:
            Resized PIL Image
        """
        return image.resize((target_cols, target_rows), Image.Resampling.LANCZOS)
    
    def convert_to_rgb(self, image: Image.Image) -> Image.Image:
        """
        Convert image to RGB mode if not already.
        
        Args:
            image: Input PIL Image
        
        Returns:
            RGB mode PIL Image
        """
        if image.mode != 'RGB':
            return image.convert('RGB')
        return image
    
    def image_to_array(self, image: Image.Image, rows: int, cols: int) -> np.ndarray:
        """
        Convert an image to a numpy array with specified dimensions.
        
        Args:
            image: Input PIL Image
            rows: Number of rows in the output array
            cols: Number of columns in the output array
        
        Returns:
            Numpy array of shape (rows, cols, 3) with RGB values
        """
        # Convert to RGB if not already
        rgb_image = self.convert_to_rgb(image)
        
        # Resize image to match matrix dimensions
        resized_image = self.resize_image(rgb_image, rows, cols)
        
        # Convert to numpy array
        image_array = np.array(resized_image)
        
        # Ensure the array has the correct shape (rows, cols, 3)
        if image_array.shape != (rows, cols, 3):
            image_array = image_array[:rows, :cols, :3]
        
        return image_array

