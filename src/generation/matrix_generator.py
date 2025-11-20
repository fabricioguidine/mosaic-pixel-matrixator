"""Matrix generation and dimension calculations."""

import numpy as np
from typing import Tuple, Dict, Optional
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
        requested_width_cm: float,
        requested_height_cm: float
    ) -> Tuple[float, float, float, float]:
        """
        Calculate output dimensions that preserve image aspect ratio.
        Chooses the option that is closest to the requested dimensions.
        
        Args:
            image: Input PIL Image
            requested_width_cm: Requested width in centimeters
            requested_height_cm: Requested height in centimeters
        
        Returns:
            Tuple of (actual_width_cm, actual_height_cm, width_diff, height_diff)
            where width_diff and height_diff are the differences from requested values
        """
        # Get original image dimensions
        orig_width, orig_height = image.size
        orig_aspect_ratio = orig_width / orig_height
        
        # Calculate option 1: Fit to requested width
        option1_width = requested_width_cm
        option1_height = requested_width_cm / orig_aspect_ratio
        option1_width_diff = abs(option1_width - requested_width_cm)  # Should be 0
        option1_height_diff = abs(option1_height - requested_height_cm)
        option1_total_diff = option1_width_diff + option1_height_diff
        
        # Calculate option 2: Fit to requested height
        option2_width = requested_height_cm * orig_aspect_ratio
        option2_height = requested_height_cm
        option2_width_diff = abs(option2_width - requested_width_cm)
        option2_height_diff = abs(option2_height - requested_height_cm)  # Should be 0
        option2_total_diff = option2_width_diff + option2_height_diff
        
        # Choose the option with the smallest total difference
        if option1_total_diff <= option2_total_diff:
            return option1_width, option1_height, option1_width_diff, option1_height_diff
        else:
            return option2_width, option2_height, option2_width_diff, option2_height_diff
    
    def generate_matrix(
        self, 
        image: Image.Image, 
        output_width_cm: float, 
        output_height_cm: float,
        preserve_aspect_ratio: bool = True,
        quantize_colors: bool = True,
        num_colors: Optional[int] = None
    ) -> Tuple[np.ndarray, Tuple[int, int], Tuple[float, float], Tuple[float, float]]:
        """
        Generate a color matrix from an image.
        
        Args:
            image: Input PIL Image
            output_width_cm: Requested output width in centimeters
            output_height_cm: Requested output height in centimeters
            preserve_aspect_ratio: If True, maintain image aspect ratio (default: True)
            quantize_colors: If True, reduce color palette to mixable colors (default: True)
            num_colors: Number of colors in reduced palette (default: None, uses default from quantizer)
        
        Returns:
            Tuple of (color_matrix, (rows, cols), (actual_width_cm, actual_height_cm), (width_diff, height_diff))
        """
        if preserve_aspect_ratio:
            # Calculate dimensions that preserve aspect ratio and are closest to requested
            actual_width_cm, actual_height_cm, width_diff, height_diff = self.calculate_dimensions_preserving_aspect_ratio(
                image, output_width_cm, output_height_cm
            )
        else:
            # Use exact dimensions (may distort image)
            actual_width_cm = output_width_cm
            actual_height_cm = output_height_cm
            width_diff = 0.0
            height_diff = 0.0
        
        # Calculate matrix dimensions
        rows, cols = self.calculate_matrix_dimensions(actual_width_cm, actual_height_cm)
        
        # Convert image to matrix
        matrix = self.processor.image_to_array(image, rows, cols)
        
        # Quantize colors if requested
        if quantize_colors:
            from src.quantization.color_quantizer import ColorQuantizer
            quantizer = ColorQuantizer(num_colors=num_colors or 32)
            matrix = quantizer.quantize_matrix(matrix)
        
        return matrix, (rows, cols), (actual_width_cm, actual_height_cm), (width_diff, height_diff)
    
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

