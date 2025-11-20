"""Matrix generation and dimension calculations."""

import numpy as np
from typing import Tuple, Dict
from PIL import Image
from src.config.constants import TILE_SIZE_CM
from src.processing.image_processor import ImageProcessor


class MatrixGenerator:
    """Generates color matrices from images based on tile dimensions."""
    
    def __init__(self, tile_size_cm: float = TILE_SIZE_CM):
        """
        Initialize the matrix generator.
        
        Args:
            tile_size_cm: Size of each tile in centimeters (default: 2.0cm)
        """
        self.tile_size_cm = tile_size_cm
        self.processor = ImageProcessor(tile_size_cm=tile_size_cm)
    
    def calculate_matrix_dimensions(
        self, 
        output_width_cm: float, 
        output_height_cm: float
    ) -> Tuple[int, int]:
        """
        Calculate the matrix dimensions based on output size and tile size.
        
        Args:
            output_width_cm: Desired output width in centimeters
            output_height_cm: Desired output height in centimeters
        
        Returns:
            Tuple of (rows, columns) for the matrix
        """
        columns = int(output_width_cm / self.tile_size_cm)
        rows = int(output_height_cm / self.tile_size_cm)
        
        return rows, columns
    
    def calculate_dimensions_preserving_aspect_ratio(
        self,
        image: Image.Image,
        max_width_cm: float,
        max_height_cm: float
    ) -> Tuple[float, float]:
        """
        Calculate output dimensions that preserve image aspect ratio.
        The dimensions will fit within the specified maximum bounds.
        
        Args:
            image: Input PIL Image
            max_width_cm: Maximum allowed width in centimeters
            max_height_cm: Maximum allowed height in centimeters
        
        Returns:
            Tuple of (actual_width_cm, actual_height_cm) that preserves aspect ratio
        """
        # Get original image dimensions
        orig_width, orig_height = image.size
        orig_aspect_ratio = orig_width / orig_height
        
        # Calculate what dimensions would be if we fit to width
        width_fit_height = max_width_cm / orig_aspect_ratio
        width_fits = width_fit_height <= max_height_cm
        
        # Calculate what dimensions would be if we fit to height
        height_fit_width = max_height_cm * orig_aspect_ratio
        height_fits = height_fit_width <= max_width_cm
        
        # Choose the best fit (prefer fitting to the constraint that results in larger size)
        if width_fits and height_fits:
            # Both fit, choose the one that uses more space
            if width_fit_height > max_height_cm * 0.95:
                # Width fit is close to max height, use it
                return max_width_cm, width_fit_height
            else:
                # Height fit uses more space
                return height_fit_width, max_height_cm
        elif width_fits:
            # Only width fits
            return max_width_cm, width_fit_height
        elif height_fits:
            # Only height fits
            return height_fit_width, max_height_cm
        else:
            # This shouldn't happen, but if it does, fit to the smaller constraint
            # Calculate scale factors for both dimensions
            width_scale = max_width_cm / orig_aspect_ratio / max_height_cm
            height_scale = max_height_cm * orig_aspect_ratio / max_width_cm
            
            if width_scale < height_scale:
                return max_width_cm, max_width_cm / orig_aspect_ratio
            else:
                return max_height_cm * orig_aspect_ratio, max_height_cm
    
    def generate_matrix(
        self, 
        image: Image.Image, 
        output_width_cm: float, 
        output_height_cm: float,
        preserve_aspect_ratio: bool = True
    ) -> Tuple[np.ndarray, Tuple[int, int], Tuple[float, float]]:
        """
        Generate a color matrix from an image.
        
        Args:
            image: Input PIL Image
            output_width_cm: Desired output width in centimeters (max if preserve_aspect_ratio=True)
            output_height_cm: Desired output height in centimeters (max if preserve_aspect_ratio=True)
            preserve_aspect_ratio: If True, maintain image aspect ratio (default: True)
        
        Returns:
            Tuple of (color_matrix, (rows, cols), (actual_width_cm, actual_height_cm))
        """
        if preserve_aspect_ratio:
            # Calculate dimensions that preserve aspect ratio
            actual_width_cm, actual_height_cm = self.calculate_dimensions_preserving_aspect_ratio(
                image, output_width_cm, output_height_cm
            )
        else:
            # Use exact dimensions (may distort image)
            actual_width_cm = output_width_cm
            actual_height_cm = output_height_cm
        
        # Calculate matrix dimensions
        rows, cols = self.calculate_matrix_dimensions(actual_width_cm, actual_height_cm)
        
        # Convert image to matrix
        matrix = self.processor.image_to_array(image, rows, cols)
        
        return matrix, (rows, cols), (actual_width_cm, actual_height_cm)
    
    def get_matrix_info(self, matrix: np.ndarray) -> Dict:
        """
        Get information about the generated matrix.
        
        Args:
            matrix: Color matrix numpy array
        
        Returns:
            Dictionary with matrix information
        """
        rows, cols = matrix.shape[:2]
        
        # Calculate actual output dimensions
        actual_width_cm = cols * self.tile_size_cm
        actual_height_cm = rows * self.tile_size_cm
        
        return {
            "matrix_rows": rows,
            "matrix_columns": cols,
            "total_tiles": rows * cols,
            "tile_size_cm": self.tile_size_cm,
            "output_width_cm": actual_width_cm,
            "output_height_cm": actual_height_cm,
            "color_format": "RGB"
        }

