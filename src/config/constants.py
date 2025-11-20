"""
Configuration constants.

This module contains all configuration constants used throughout the application.
Modify these values to change default behavior (e.g., tile size, supported formats).
"""

# Standard ceramic tile size in centimeters
# This value determines the size of each tile in the output matrix
TILE_SIZE_CM = 2.0

# Supported image file formats (case-insensitive)
# Files with these extensions will be recognized as valid input images
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

