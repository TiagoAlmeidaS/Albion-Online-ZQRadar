"""
Fishing Drawing Component for Albion Radar

This module handles the drawing of fishing spots on the radar,
based on the original FishingDrawing.js.
"""

from typing import Dict, Any, List, Optional
from .base_drawing import BaseDrawing
import math


class FishingDrawing(BaseDrawing):
    """Drawing component for fishing spots on the radar."""
    
    def __init__(self, canvas_width: int = 500, canvas_height: int = 500):
        """Initialize fishing drawing component."""
        super().__init__(canvas_width, canvas_height)
        self.fishing_color = '#4169e1'  # Royal Blue
        self.fishing_symbol = '🐟'
    
    def draw(self, ctx: Any) -> None:
        """Draw all fishing spots on the radar."""
        if not self.data:
            return
        
        for fishing_spot in self.data:
            self._draw_fishing_spot(ctx, fishing_spot)
    
    def _draw_fishing_spot(self, ctx: Any, fishing_spot: Dict[str, Any]) -> None:
        """Draw a single fishing spot on the radar."""
        # Extract fishing spot data
        x = fishing_spot.get('x', 0)
        y = fishing_spot.get('y', 0)
        tier = fishing_spot.get('tier', 1)
        enchant = fishing_spot.get('enchant', 0)
        name = fishing_spot.get('name', 'Fishing Spot')
        
        # Check if fishing should be shown based on settings
        if not self.settings.get('show_fish', False):
            return
        
        # Convert world coordinates to screen coordinates
        screen_x, screen_y = self.world_to_screen(x, y)
        
        # Check if fishing spot is in range
        if not self.is_in_range(x, y):
            return
        
        # Draw fishing spot
        self._draw_fishing_marker(ctx, screen_x, screen_y, tier, enchant)
        
        # Draw fishing spot name
        self._draw_fishing_name(ctx, screen_x, screen_y, name)
    
    def _draw_fishing_marker(self, ctx: Any, x: int, y: int, tier: int, enchant: int) -> None:
        """Draw fishing marker on radar."""
        # Draw fishing symbol
        self.draw_text(ctx, self.fishing_symbol, x, y, self.fishing_color, '16px Arial')
        
        # Draw tier indicator
        tier_text = str(tier)
        if enchant > 0:
            tier_text += f".{enchant}"
        
        # Position tier text below symbol
        tier_x = x
        tier_y = y + 12
        
        # Draw background for tier text
        self._draw_text_background(ctx, tier_x, tier_y, tier_text)
        
        # Draw tier text
        self.draw_text(ctx, tier_text, tier_x, tier_y, self.fishing_color, '8px Arial')
    
    def _draw_fishing_name(self, ctx: Any, x: int, y: int, name: str) -> None:
        """Draw fishing spot name."""
        # Position text above fishing symbol
        text_x = x
        text_y = y - 15
        
        # Truncate name if too long
        display_name = name[:10] if len(name) > 10 else name
        
        # Draw background for better visibility
        self._draw_text_background(ctx, text_x, text_y, display_name)
        
        # Draw text
        self.draw_text(ctx, display_name, text_x, text_y, self.fishing_color, '8px Arial')
    
    def _draw_text_background(self, ctx: Any, x: int, y: int, text: str) -> None:
        """Draw background for text to improve visibility."""
        # Estimate text width (rough calculation)
        text_width = len(text) * 5  # Approximate width per character
        text_height = 10
        
        # Draw semi-transparent background
        if hasattr(ctx, 'fillRect'):
            # HTML5 Canvas
            ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'
            ctx.fillRect(x - 2, y - text_height + 2, text_width + 4, text_height)
        else:
            # Generic drawing interface
            self._draw_rect_generic(ctx, x - 2, y - text_height + 2, text_width + 4, text_height, 'rgba(0, 0, 0, 0.7)')
    
    def _draw_rect_generic(self, ctx: Any, x: int, y: int, width: int, height: int, color: str) -> None:
        """Generic rectangle drawing implementation."""
        # Override in subclasses for specific drawing backends
        pass 