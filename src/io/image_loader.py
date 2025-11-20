"""Image loading utilities."""

from pathlib import Path
from typing import List, Optional
from PIL import Image
from src.config.constants import SUPPORTED_IMAGE_FORMATS


def get_image_files(directory: str) -> List[str]:
    """
    Get all supported image files from a directory.
    
    Args:
        directory: Path to the directory to search
    
    Returns:
        List of image file paths
    """
    directory_path = Path(directory)
    if not directory_path.exists():
        return []
    
    image_files = []
    for file_path in directory_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_IMAGE_FORMATS:
            image_files.append(str(file_path))
    
    return sorted(image_files)


def load_image(image_path: str) -> Optional[Image.Image]:
    """
    Load an image file.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        PIL Image object or None if loading fails
    """
    try:
        return Image.open(image_path)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

