"""Color base selection algorithm to find minimum purchase colors."""

import numpy as np
from typing import List, Dict, Tuple, Set
from collections import defaultdict


class ColorBaseSelector:
    """Selects minimum set of base colors that can be mixed to achieve all required colors."""
    
    # Primary CMYK colors (base paints to buy)
    PRIMARY_COLORS = {
        'cyan': {'c': 100, 'm': 0, 'y': 0, 'k': 0},
        'magenta': {'c': 0, 'm': 100, 'y': 0, 'k': 0},
        'yellow': {'c': 0, 'm': 0, 'y': 100, 'k': 0},
        'black': {'c': 0, 'm': 0, 'y': 0, 'k': 100},
        'white': {'c': 0, 'm': 0, 'y': 0, 'k': 0}
    }
    
    @staticmethod
    def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> Tuple[int, int, int]:
        """Convert CMYK to RGB."""
        c_norm = c / 100.0
        m_norm = m / 100.0
        y_norm = y / 100.0
        k_norm = k / 100.0
        
        r = int(255 * (1 - min(1, c_norm + k_norm)))
        g = int(255 * (1 - min(1, m_norm + k_norm)))
        b = int(255 * (1 - min(1, y_norm + k_norm)))
        
        return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
    
    @staticmethod
    def select_base_colors(matrix: np.ndarray) -> List[Dict]:
        """
        Select minimum set of base colors (CMYK primaries + white).
        
        Args:
            matrix: RGB matrix of shape (rows, cols, 3)
        
        Returns:
            List of base colors to purchase with CMYK information
        """
        # Always use CMYK primaries (cyan, magenta, yellow, black, white)
        # These are the fundamental colors that can create any other color
        base_colors = []
        
        for color_name, cmyk in ColorBaseSelector.PRIMARY_COLORS.items():
            r, g, b = ColorBaseSelector.cmyk_to_rgb(
                cmyk['c'], cmyk['m'], cmyk['y'], cmyk['k']
            )
            
            from .color_converter import ColorConverter
            hex_code = ColorConverter.rgb_to_hex(r, g, b)
            
            base_colors.append({
                'name': color_name,
                'rgb': [r, g, b],
                'hex': hex_code,
                'cmyk': cmyk,
                'purchase': True  # These must be purchased
            })
        
        return base_colors
    
    @staticmethod
    def calculate_mix_instructions(target_cmyk: Dict[str, float], base_colors: List[Dict]) -> Dict:
        """
        Calculate how to mix base colors to achieve target CMYK color.
        
        Args:
            target_cmyk: Target CMYK values {'c': %, 'm': %, 'y': %, 'k': %}
            base_colors: List of available base colors
        
        Returns:
            Dictionary with mixing instructions:
            {
                'mix': [
                    {'color': 'cyan', 'percentage': 50.0},
                    {'color': 'magenta', 'percentage': 25.0},
                    ...
                ],
                'instruction': 'Mix 50% cyan, 25% magenta, ...'
            }
        """
        mix = []
        
        # Extract CMYK percentages from target
        c_target = target_cmyk.get('c', 0.0)
        m_target = target_cmyk.get('m', 0.0)
        y_target = target_cmyk.get('y', 0.0)
        k_target = target_cmyk.get('k', 0.0)
        
        # Calculate mixing percentages for each primary
        # CMYK colors are additive - we mix the percentages
        if c_target > 0:
            mix.append({'color': 'cyan', 'percentage': round(c_target, 1)})
        if m_target > 0:
            mix.append({'color': 'magenta', 'percentage': round(m_target, 1)})
        if y_target > 0:
            mix.append({'color': 'yellow', 'percentage': round(y_target, 1)})
        if k_target > 0:
            mix.append({'color': 'black', 'percentage': round(k_target, 1)})
        
        # If all CMYK are low, we need white as base
        if c_target < 10 and m_target < 10 and y_target < 10 and k_target < 10:
            # Light color - use white as base
            white_pct = 100.0 - max(c_target, m_target, y_target, k_target)
            if white_pct > 0:
                mix.append({'color': 'white', 'percentage': round(white_pct, 1)})
        else:
            # For darker colors, add white only if needed for lightness
            total_colored = c_target + m_target + y_target + k_target
            if total_colored < 100:
                white_pct = 100.0 - total_colored
                if white_pct > 5:  # Only if significant amount
                    mix.append({'color': 'white', 'percentage': round(white_pct, 1)})
        
        # Normalize percentages to sum to 100%
        total = sum(item['percentage'] for item in mix)
        if total > 0:
            scale = 100.0 / total
            for item in mix:
                item['percentage'] = round(item['percentage'] * scale, 1)
        
        # Create instruction text
        if not mix:
            instruction = "Use white (100%)"
        else:
            parts = [f"{item['percentage']:.1f}% {item['color']}" for item in mix]
            instruction = f"Mix: {', '.join(parts)}"
        
        return {
            'mix': mix,
            'instruction': instruction
        }

