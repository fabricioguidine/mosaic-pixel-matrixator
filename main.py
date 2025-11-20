"""Main entry point for Mosaic Pixel Matrixator."""

import sys
import argparse
from pathlib import Path
from datetime import datetime

from src.io import get_image_files, load_image, save_matrix_to_file, save_matrix_to_json
from src.generation import MatrixGenerator
from src.visualization import recreate_image_from_matrix
from src.config import TILE_SIZE_CM


def get_user_input(
    width_cm: float = None, 
    height_cm: float = None, 
    tile_size_cm: float = None
) -> tuple:
    """
    Get user input for dimensions and tile size.
    
    Args:
        width_cm: Optional width in centimeters (from command line)
        height_cm: Optional height in centimeters (from command line)
        tile_size_cm: Optional tile size in centimeters (from command line)
    
    Returns:
        Tuple of (width, height, tile_size) in centimeters
    """
    print("\n=== Mosaic Pixel Matrixator ===\n")
    
    if width_cm is not None and height_cm is not None:
        if width_cm <= 0 or height_cm <= 0:
            print("Error: Dimensions must be positive numbers.")
            sys.exit(1)
        # Use provided tile size or default
        tile_size = tile_size_cm if tile_size_cm is not None and tile_size_cm > 0 else TILE_SIZE_CM
        return width_cm, height_cm, tile_size
    
    try:
        width = float(input("Enter output width in centimeters: "))
        height = float(input("Enter output height in centimeters: "))
        tile_size_input = input(f"Enter tile size in centimeters (default: {TILE_SIZE_CM}cm): ").strip()
        
        if width <= 0 or height <= 0:
            print("Error: Dimensions must be positive numbers.")
            sys.exit(1)
        
        if tile_size_input:
            tile_size = float(tile_size_input)
            if tile_size <= 0:
                print("Error: Tile size must be a positive number.")
                sys.exit(1)
        else:
            tile_size = TILE_SIZE_CM
        
        return width, height, tile_size
    except ValueError:
        print("Error: Please enter valid numbers.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)


def main():
    """
    Main function to process images.
    
    Orchestrates the complete processing pipeline:
    1. Checks input directory and finds images
    2. Loads the first image found
    3. Gets dimensions from user (CLI args or interactive input)
    4. Generates RGB matrix with aspect ratio preservation
    5. Saves outputs (TXT, JSON, PNG preview)
    6. Displays processing results
    """
    parser = argparse.ArgumentParser(
        description='Mosaic Pixel Matrixator - Convert images to ceramic tile color matrices'
    )
    parser.add_argument('--width', type=float, help='Output width in centimeters')
    parser.add_argument('--height', type=float, help='Output height in centimeters')
    parser.add_argument(
        '--tile-size', 
        type=float, 
        default=TILE_SIZE_CM,
        help=f'Tile size in centimeters (default: {TILE_SIZE_CM}cm)'
    )
    args = parser.parse_args()
    
    # Validate tile size
    if args.tile_size <= 0:
        print("Error: Tile size must be a positive number.")
        sys.exit(1)
    
    # Check input directory
    input_dir = Path("input")
    if not input_dir.exists():
        input_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created input directory: {input_dir}")
        print("Please place image files in the 'input' directory and run again.")
        return
    
    # Get image files
    image_files = get_image_files("input")
    
    if not image_files:
        print("No image files found in the 'input' directory.")
        print("Supported formats: JPG, JPEG, PNG, BMP, GIF, TIFF, WEBP")
        return
    
    # Process one image at a time
    print(f"\nFound {len(image_files)} image file(s) in input directory:")
    for i, img_file in enumerate(image_files, 1):
        print(f"  {i}. {Path(img_file).name}")
    
    # Process the first image
    image_path = image_files[0]
    print(f"\nProcessing: {Path(image_path).name}")
    
    # Load image
    image = load_image(image_path)
    if image is None:
        print("Failed to load image.")
        return
    
    # Get user input for dimensions and tile size
    width_cm, height_cm, tile_size_cm = get_user_input(
        args.width, 
        args.height, 
        args.tile_size
    )
    
    # Initialize matrix generator with specified tile size
    generator = MatrixGenerator(tile_size_cm=tile_size_cm)
    
    print("\nProcessing image...")
    
    # Generate matrix
    try:
        # Get original image dimensions for reference
        orig_width, orig_height = image.size
        orig_aspect_ratio = orig_width / orig_height
        print(f"Original image: {orig_width}x{orig_height} (aspect ratio: {orig_aspect_ratio:.2f})")
        print(f"Requested dimensions: {width_cm}cm x {height_cm}cm")
        print(f"Tile size: {tile_size_cm:.2f}cm x {tile_size_cm:.2f}cm")
        
        matrix, (rows, cols), (actual_width_cm, actual_height_cm) = generator.generate_matrix(
            image, width_cm, height_cm, preserve_aspect_ratio=True
        )
        
        # Get matrix information
        info = generator.get_matrix_info(matrix)
        
        print("\n=== Processing Complete ===")
        print(f"Matrix dimensions: {rows} rows x {cols} columns")
        print(f"Total tiles: {info['total_tiles']}")
        print(f"Tile size: {info['tile_size_cm']:.2f}cm x {info['tile_size_cm']:.2f}cm")
        print(f"Output dimensions: {actual_width_cm:.2f}cm x {actual_height_cm:.2f}cm")
        
        # Show if dimensions were adjusted
        if abs(actual_width_cm - width_cm) > 0.01 or abs(actual_height_cm - height_cm) > 0.01:
            print(f"Note: Dimensions adjusted to preserve aspect ratio (maintained at {orig_aspect_ratio:.2f})")
        
        # Generate output filenames with image name and timestamp
        input_name = Path(image_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save as text file
        txt_output = output_dir / f"{input_name}-{timestamp}_matrix.txt"
        save_matrix_to_file(matrix, txt_output)
        print(f"\nMatrix saved to: {txt_output}")
        
        # Save as JSON file
        json_output = output_dir / f"{input_name}-{timestamp}_matrix.json"
        save_matrix_to_json(matrix, json_output)
        print(f"Matrix saved to: {json_output}")
        
        # Recreate image from matrix for visualization
        preview_output = output_dir / f"{input_name}-{timestamp}.png"
        recreate_image_from_matrix(matrix, preview_output, scale_factor=10)
        print(f"Preview image saved to: {preview_output}")
        
        print("\nProcessing completed successfully!")
        
    except Exception as e:
        print(f"\nError during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
