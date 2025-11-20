"""File handling operations for saving matrices."""

import json
from pathlib import Path
from typing import List, Dict
import numpy as np
from src.quantization.color_mixer import ColorMixer
from src.quantization.color_base_selector import ColorBaseSelector


def save_matrix_to_file(matrix: np.ndarray, output_path: str, base_colors: List[Dict] = None):
    """
    Save the color matrix to a file with paint mixing instructions.
    
    Args:
        matrix: RGB matrix numpy array of shape (rows, cols, 3)
        output_path: Path where the file will be saved
        base_colors: List of base colors to purchase (if None, will be calculated)
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Get base colors if not provided
    if base_colors is None:
        base_colors = ColorBaseSelector.select_base_colors(matrix)
    
    with open(output_file, 'w') as f:
        f.write("# RGB Color Matrix with Paint Mixing Instructions\n")
        f.write(f"# Matrix dimensions: {matrix.shape[0]} rows x {matrix.shape[1]} columns\n")
        f.write("# Format: R,G,B[CMYK] #HEX {mix_instruction}\n\n")
        
        # Write base colors to purchase
        f.write("# BASE COLORS TO PURCHASE:\n")
        for base in base_colors:
            if base.get('purchase', False):
                f.write(f"# - {base['name'].upper()}: RGB{base['rgb']} {base['hex']} ")
                f.write(f"CMYK({base['cmyk']['c']:.1f}%,{base['cmyk']['m']:.1f}%,{base['cmyk']['y']:.1f}%,{base['cmyk']['k']:.1f}%)\n")
        f.write("\n")
        
        # Write matrix with mixing instructions
        for i, row in enumerate(matrix):
            f.write(f"# Row {i+1}\n")
            for j, pixel in enumerate(row):
                r, g, b = pixel
                color_info = ColorMixer.get_primary_mix(int(r), int(g), int(b))
                cmyk = color_info['cmyk']
                hex_code = color_info['hex']
                
                # Calculate mix instructions
                mix_info = ColorBaseSelector.calculate_mix_instructions(cmyk, base_colors)
                
                # Format: R,G,B[C:c%,M:m%,Y:y%,K:k%] #HEX {Mix: X% color1, Y% color2}
                f.write(f"{int(r)},{int(g)},{int(b)}[C:{cmyk['c']:.1f}%,M:{cmyk['m']:.1f}%,Y:{cmyk['y']:.1f}%,K:{cmyk['k']:.1f}%] {hex_code} {{{mix_info['instruction']}}}")
                
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
    
    # Convert numpy array to list of lists with primary color mix information
    matrix_list = []
    for row in matrix:
        row_list = []
        for r, g, b in row:
            mix_info = ColorMixer.get_primary_mix(int(r), int(g), int(b))
            row_list.append(mix_info)
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

