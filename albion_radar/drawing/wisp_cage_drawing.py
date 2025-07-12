"""
Wisp Cage Drawing Component for Albion Radar

This module handles the drawing of wisp cages on the radar,
based on the original WispCageDrawing.js.
"""

from typing import Dict, Any, List, Optional
from .base_drawing import BaseDrawing
import math


class WispCageDrawing(BaseDrawing):
    """Drawing component for wisp cages on the radar."""
    
    def __init__(self, canvas_width: int = 500, canvas_height: int = 500):
        """Initialize wisp cage drawing component."""
        super().__init__(canvas_width, canvas_height)
        self.wisp_cage_color = '#ff00ff'  # Magenta
        self.wisp_cage_symbol = '✨'
    
    def draw(self, ctx: Any) -> None:
        """Draw all wisp cages on the radar."""
        if not self.data:
            return
        
        for wisp_cage in self.data:
            self._draw_wisp_cage(ctx, wisp_cage)
    
    def _draw_wisp_cage(self, ctx: Any, wisp_cage: Dict[str, Any]) -> None:
        """Draw a single wisp cage on the radar."""
        # Extract wisp cage data
        x = wisp_cage.get('x', 0)
        y = wisp_cage.get('y', 0)
        tier = wisp_cage.get('tier', 1)
        enchant = wisp_cage.get('enchant', 0)
        name = wisp_cage.get('name', 'Wisp Cage')
        
        # Check if wisp cage should be shown based on settings
        if not self.settings.get('wisp_cage', False):
            return
        
        # Convert world coordinates to screen coordinates
        screen_x, screen_y = self.world_to_screen(x, y)
        
        # Check if wisp cage is in range
        if not self.is_in_range(x, y):
            return
        
        # Draw wisp cage
        self._draw_wisp_cage_marker(ctx, screen_x, screen_y, tier, enchant)
        
        # Draw wisp cage name
        self._draw_wisp_cage_name(ctx, screen_x, screen_y, name)
    
    def _draw_wisp_cage_marker(self, ctx: Any, x: int, y: int, tier: int, enchant: int) -> None:
        """Draw wisp cage marker on radar."""
        # Draw wisp cage symbol
        self.draw_text(ctx, self.wisp_cage_symbol, x, y, self.wisp_cage_color, '16px Arial')
        
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
        self.draw_text(ctx, tier_text, tier_x, tier_y, self.wisp_cage_color, '8px Arial')
    
    def _draw_wisp_cage_name(self, ctx: Any, x: int, y: int, name: str) -> None:
        """Draw wisp cage name."""
        # Position text above wisp cage symbol
        text_x = x
        text_y = y - 15
        
        # Truncate name if too long
        display_name = name[:10] if len(name) > 10 else name
        
        # Draw background for better visibility
        self._draw_text_background(ctx, text_x, text_y, display_name)
        
        # Draw text
        self.draw_text(ctx, display_name, text_x, text_y, self.wisp_cage_color, '8px Arial')
    
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