"""
Maps Drawing Component for Albion Radar

This module handles the drawing of map backgrounds and grid on the radar,
based on the original MapsDrawing.js.
"""

from typing import Dict, Any, List, Optional
from .base_drawing import BaseDrawing
import math


class MapsDrawing(BaseDrawing):
    """Drawing component for maps on the radar."""
    
    def __init__(self, canvas_width: int = 500, canvas_height: int = 500):
        """Initialize maps drawing component."""
        super().__init__(canvas_width, canvas_height)
        self.grid_color = '#333333'
        self.grid_spacing = 20
        self.map_images = {}
    
    def draw(self, ctx: Any) -> None:
        """Draw map background and grid on the radar."""
        # Draw map background if enabled
        if self.settings.get('show_map_background', False):
            self._draw_map_background(ctx)
        
        # Draw grid
        self._draw_grid(ctx)
        
        # Draw center marker
        self._draw_center_marker(ctx)
    
    def _draw_map_background(self, ctx: Any) -> None:
        """Draw map background image."""
        # This would load and draw a map image
        # For now, we'll just draw a placeholder
        if hasattr(ctx, 'fillRect'):
            # HTML5 Canvas
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)'
            ctx.fillRect(0, 0, self.canvas_width, self.canvas_height)
        else:
            # Generic drawing interface
            self._draw_rect_generic(ctx, 0, 0, self.canvas_width, self.canvas_height, 'rgba(0, 0, 0, 0.1)')
    
    def _draw_grid(self, ctx: Any) -> None:
        """Draw grid lines on the radar."""
        # Draw vertical lines
        for x in range(0, self.canvas_width, self.grid_spacing):
            self.draw_line(ctx, x, 0, x, self.canvas_height, self.grid_color, 1)
        
        # Draw horizontal lines
        for y in range(0, self.canvas_height, self.grid_spacing):
            self.draw_line(ctx, 0, y, self.canvas_width, y, self.grid_color, 1)
    
    def _draw_center_marker(self, ctx: Any) -> None:
        """Draw center marker (player position)."""
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2
        
        # Draw center cross
        cross_size = 10
        self.draw_line(ctx, center_x - cross_size, center_y, center_x + cross_size, center_y, '#ffffff', 2)
        self.draw_line(ctx, center_x, center_y - cross_size, center_x, center_y + cross_size, '#ffffff', 2)
        
        # Draw center circle
        self.draw_circle(ctx, center_x, center_y, 3, '#ffffff', fill=True)
    
    def _draw_rect_generic(self, ctx: Any, x: int, y: int, width: int, height: int, color: str) -> None:
        """Generic rectangle drawing implementation."""
        # Override in subclasses for specific drawing backends
        pass 