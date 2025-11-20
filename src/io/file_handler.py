"""File handling operations for saving matrices."""

import json
from pathlib import Path
import numpy as np
from src.quantization.color_namer import ColorNamer


def save_matrix_to_file(matrix: np.ndarray, output_path: str):
    """
    Save the color matrix to a file in a readable text format.
    
    Args:
        matrix: RGB matrix numpy array of shape (rows, cols, 3)
        output_path: Path where the file will be saved
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("# RGB Color Matrix\n")
        f.write(f"# Matrix dimensions: {matrix.shape[0]} rows x {matrix.shape[1]} columns\n")
        f.write("# Format: R,G,B[color-name] for each tile\n\n")
        
        for i, row in enumerate(matrix):
            f.write(f"# Row {i+1}\n")
            for j, pixel in enumerate(row):
                r, g, b = pixel
                color_str = ColorNamer.add_color_name_to_rgb(r, g, b)
                f.write(color_str)
                if j < len(row) - 1:
                    f.write(" ")
            f.write("\n")


def save_matrix_to_json(matrix: np.ndarray, output_path: str):
    """
    Save the color matrix to a JSON file.
    
    Args:
        matrix: RGB matrix numpy array of shape (rows, cols, 3)
        output_path: Path where the JSON file will be saved
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert numpy array to list of lists with color names
    matrix_list = []
    for row in matrix:
        row_list = []
        for r, g, b in row:
            color_name = ColorNamer.get_color_name(int(r), int(g), int(b))
            row_list.append({
                "rgb": [int(r), int(g), int(b)],
                "color_name": color_name
            })
        matrix_list.append(row_list)
    
    data = {
        "dimensions": {
            "rows": matrix.shape[0],
            "columns": matrix.shape[1]
        },
        "matrix": matrix_list
    }
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

