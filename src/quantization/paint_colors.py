"""Paint color inventory and requirements."""

import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict


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
        Get the list of required paint colors with usage counts.
        
        Returns:
            List of dictionaries with paint color information:
            [
                {
                    'rgb': [r, g, b],
                    'red': r,
                    'green': g,
                    'blue': b,
                    'count': usage_count,
                    'red_pct': r_percentage,
                    'green_pct': g_percentage,
                    'blue_pct': b_percentage
                },
                ...
            ]
            Sorted by usage count (most used first)
        """
        paints = []
        for (r, g, b), count in self.color_counts.items():
            total = r + g + b
            red_pct = round((r / 255.0) * 100, 1) if total > 0 else 0
            green_pct = round((g / 255.0) * 100, 1) if total > 0 else 0
            blue_pct = round((b / 255.0) * 100, 1) if total > 0 else 0
            
            paints.append({
                'rgb': [r, g, b],
                'red': r,
                'green': g,
                'blue': b,
                'count': count,
                'red_pct': red_pct,
                'green_pct': green_pct,
                'blue_pct': blue_pct
            })
        
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

