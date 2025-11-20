"""Color naming system for RGB values."""

import numpy as np
from typing import Tuple


class ColorNamer:
    """Maps RGB values to color names based on color ranges."""
    
    # Color thresholds and names
    COLOR_RANGES = {
        'red': {'r_min': 128, 'g_max': 100, 'b_max': 100, 'priority': 1},
        'dark-red': {'r_min': 50, 'r_max': 128, 'g_max': 50, 'b_max': 50, 'priority': 2},
        'light-red': {'r_min': 200, 'g_max': 150, 'b_max': 150, 'priority': 3},
        
        'green': {'g_min': 128, 'r_max': 100, 'b_max': 100, 'priority': 1},
        'dark-green': {'g_min': 50, 'g_max': 128, 'r_max': 50, 'b_max': 50, 'priority': 2},
        'light-green': {'g_min': 200, 'r_max': 150, 'b_max': 150, 'priority': 3},
        
        'blue': {'b_min': 128, 'r_max': 100, 'g_max': 100, 'priority': 1},
        'dark-blue': {'b_min': 50, 'b_max': 128, 'r_max': 50, 'g_max': 50, 'priority': 2},
        'light-blue': {'b_min': 200, 'r_max': 150, 'g_max': 150, 'priority': 3},
        
        'yellow': {'r_min': 180, 'g_min': 180, 'b_max': 100, 'priority': 1},
        'orange': {'r_min': 200, 'g_min': 100, 'g_max': 200, 'b_max': 50, 'priority': 1},
        'purple': {'r_min': 100, 'g_max': 100, 'b_min': 150, 'priority': 1},
        
        'white': {'r_min': 220, 'g_min': 220, 'b_min': 220, 'priority': 1},
        'light-gray': {'r_min': 180, 'g_min': 180, 'b_min': 180, 'r_max': 219, 'g_max': 219, 'b_max': 219, 'priority': 2},
        'gray': {'r_min': 100, 'g_min': 100, 'b_min': 100, 'r_max': 179, 'g_max': 179, 'b_max': 179, 'priority': 3},
        'dark-gray': {'r_min': 50, 'g_min': 50, 'b_min': 50, 'r_max': 99, 'g_max': 99, 'b_max': 99, 'priority': 4},
        'black': {'r_max': 49, 'g_max': 49, 'b_max': 49, 'priority': 5},
        
        'brown': {'r_min': 100, 'r_max': 180, 'g_min': 50, 'g_max': 150, 'b_max': 100, 'priority': 1},
        'pink': {'r_min': 200, 'g_min': 100, 'g_max': 200, 'b_min': 150, 'b_max': 200, 'priority': 1},
        'cyan': {'g_min': 150, 'b_min': 150, 'r_max': 100, 'priority': 1},
    }
    
    @classmethod
    def get_color_name(cls, r: int, g: int, b: int) -> str:
        """
        Get color name for RGB values.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        
        Returns:
            Color name string
        """
        # Check each color range in priority order
        matches = []
        for color_name, criteria in cls.COLOR_RANGES.items():
            match = True
            priority = criteria.get('priority', 999)
            
            # Check min/max conditions
            if 'r_min' in criteria and r < criteria['r_min']:
                match = False
            if 'r_max' in criteria and r > criteria['r_max']:
                match = False
            if 'g_min' in criteria and g < criteria['g_min']:
                match = False
            if 'g_max' in criteria and g > criteria['g_max']:
                match = False
            if 'b_min' in criteria and b < criteria['b_min']:
                match = False
            if 'b_max' in criteria and b > criteria['b_max']:
                match = False
            
            if match:
                matches.append((priority, color_name))
        
        # Return highest priority match, or default to RGB description
        if matches:
            matches.sort(key=lambda x: x[0])
            return matches[0][1]
        
        # Default: describe by dominant channel
        max_val = max(r, g, b)
        if max_val < 50:
            return 'black'
        elif max_val > 200:
            if abs(r - g) < 30 and abs(g - b) < 30:
                return 'white'
            elif r > g and r > b:
                return 'light-red' if r > 200 else 'red'
            elif g > r and g > b:
                return 'light-green' if g > 200 else 'green'
            else:
                return 'light-blue' if b > 200 else 'blue'
        else:
            if r > g and r > b:
                return 'red'
            elif g > r and g > b:
                return 'green'
            else:
                return 'blue'
    
    @classmethod
    def add_color_name_to_rgb(cls, r: int, g: int, b: int) -> str:
        """
        Format RGB with color name.
        
        Args:
            r: Red value
            g: Green value
            b: Blue value
        
        Returns:
            Formatted string: "R,G,B[color-name]"
        """
        color_name = cls.get_color_name(int(r), int(g), int(b))
        return f"{int(r)},{int(g)},{int(b)}[{color_name}]"

