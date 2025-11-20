"""Image recreation from RGB matrices for visualization."""

from pathlib import Path
import numpy as np
from PIL import Image


def recreate_image_from_matrix(matrix: np.ndarray, output_path: str, scale_factor: int = 10):
    """
    Recreate an image from the RGB matrix for visualization.
    
    This function takes the RGB matrix generated from an image and recreates
    a visual representation that can be previewed before assembling the actual
    ceramic tile mosaic.
    
    Args:
        matrix: RGB matrix numpy array of shape (rows, cols, 3)
        output_path: Path where the recreated image will be saved
        scale_factor: Factor to upscale the image for better visibility (default: 10)
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Ensure matrix values are integers and in valid range
    matrix_int = np.clip(matrix.astype(np.uint8), 0, 255)
    
    # Convert numpy array to PIL Image
    image = Image.fromarray(matrix_int, mode='RGB')
    
    # Upscale the image for better visualization (since matrix might be small)
    if scale_factor > 1:
        new_size = (matrix.shape[1] * scale_factor, matrix.shape[0] * scale_factor)
        image = image.resize(new_size, Image.Resampling.NEAREST)
    
    # Save the image
    image.save(output_file, quality=95)

