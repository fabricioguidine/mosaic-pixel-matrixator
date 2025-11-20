"""Paint color inventory with industry-standard color codes."""

import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
from .color_converter import ColorConverter


class PaintColorInventory:
    """Manages paint color requirements for the mosaic."""
    
    def __init__(self):
        """Initialize the paint color inventory."""
        self.color_counts: Dict[Tuple[int, int, int], int] = defaultdict(int)
    
    def add_color(self, r: int, g: int, b: int):
        """Add a color to the inventory."""
        color_key = (int(r), int(g), int(b))
        self.color_counts[color_key] += 1
    
    def get_required_paints(self) -> List[Dict]:
        """
        Get the list of required paint colors with industry-standard color codes.
        
        Returns:
            List of dictionaries with paint color information:
            [
                {
                    'rgb': [r, g, b],
                    'hex': '#RRGGBB' (hexadecimal code for reference),
                    'cmyk': {'c': cyan%, 'm': magenta%, 'y': yellow%, 'k': black%},
                    'hsl': {'h': hue, 's': saturation%, 'l': lightness%},
                    'count': usage_count
                },
                ...
            ]
            Sorted by usage count (most used first)
        """
        paints = []
        for (r, g, b), count in self.color_counts.items():
            # Get industry-standard color information
            color_info = ColorConverter.get_industry_standards(r, g, b)
            
            # Add usage count
            color_info['count'] = count
            
            paints.append(color_info)
        
        # Sort by count (most used first), then by RGB values
        paints.sort(key=lambda x: (-x['count'], x['rgb']))
        
        return paints
    
    def get_unique_colors_count(self) -> int:
        """Get the number of unique paint colors needed."""
        return len(self.color_counts)
    
    def get_total_tiles(self) -> int:
        """Get the total number of tiles."""
        return sum(self.color_counts.values())
    
    @classmethod
    def from_matrix(cls, matrix: np.ndarray) -> 'PaintColorInventory':
        """
        Create inventory from a color matrix.
        
        Args:
            matrix: RGB matrix of shape (rows, cols, 3)
        
        Returns:
            PaintColorInventory instance
        """
        inventory = cls()
        for row in matrix:
            for r, g, b in row:
                inventory.add_color(int(r), int(g), int(b))
        return inventory

