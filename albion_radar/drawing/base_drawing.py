"""
Base Drawing Class for Albion Radar

This module provides the base drawing functionality for radar visualization.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple, Optional
import math


class BaseDrawing(ABC):
    """Base class for all drawing components."""
    
    def __init__(self, canvas_width: int = 500, canvas_height: int = 500):
        """Initialize the drawing component."""
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.center_x = canvas_width // 2
        self.center_y = canvas_height // 2
        self.scale = 4.0
        self.data = []
        self.settings = {}
    
    @abstractmethod
    def draw(self, ctx: Any) -> None:
        """Draw the component on the canvas."""
        pass
    
    def update_data(self, data: List[Dict[str, Any]]) -> None:
        """Update the data to be drawn."""
        self.data = data
    
    def update_settings(self, settings: Dict[str, Any]) -> None:
        """Update drawing settings."""
        self.settings.update(settings)
    
    def world_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates."""
        screen_x = int(self.center_x + (x * self.scale))
        screen_y = int(self.center_y - (y * self.scale))  # Invert Y axis
        return screen_x, screen_y
    
    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[float, float]:
        """Convert screen coordinates to world coordinates."""
        world_x = (screen_x - self.center_x) / self.scale
        world_y = (self.center_y - screen_y) / self.scale  # Invert Y axis
        return world_x, world_y
    
    def calculate_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate distance between two points."""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def is_in_range(self, x: float, y: float, max_distance: float = 80.0) -> bool:
        """Check if a point is within the radar range."""
        distance = self.calculate_distance(0, 0, x, y)
        return distance <= max_distance
    
    def get_color_by_faction(self, faction: str) -> str:
        """Get color based on faction."""
        faction_colors = {
            'FRIENDLY': '#00ff00',  # Green
            'HOSTILE': '#ff0000',   # Red
            'NEUTRAL': '#ffff00',   # Yellow
            'CAERLEON': '#ff6600',  # Orange
            'BRIDGEWATCH': '#0066ff', # Blue
            'FORTSTERLING': '#9900ff', # Purple
            'LYMHURST': '#00ff66',  # Light Green
            'MARTLOCK': '#ff0066',  # Pink
            'THETFORD': '#ff9900',  # Dark Orange
        }
        return faction_colors.get(faction, '#ffffff')  # Default white
    
    def get_color_by_rarity(self, rarity: str) -> str:
        """Get color based on item rarity."""
        rarity_colors = {
            'common': '#ffffff',     # White
            'uncommon': '#00ff00',   # Green
            'rare': '#0066ff',       # Blue
            'epic': '#9900ff',       # Purple
            'legendary': '#ff6600',  # Orange
        }
        return rarity_colors.get(rarity.lower(), '#ffffff')
    
    def draw_circle(self, ctx: Any, x: int, y: int, radius: int, 
                   color: str = '#ffffff', fill: bool = False) -> None:
        """Draw a circle on the canvas."""
        if hasattr(ctx, 'arc'):
            # HTML5 Canvas
            ctx.beginPath()
            ctx.arc(x, y, radius, 0, 2 * math.pi)
            ctx.strokeStyle = color
            ctx.fillStyle = color
            if fill:
                ctx.fill()
            else:
                ctx.stroke()
        else:
            # Generic drawing interface
            self._draw_circle_generic(ctx, x, y, radius, color, fill)
    
    def draw_text(self, ctx: Any, text: str, x: int, y: int, 
                 color: str = '#ffffff', font: str = '12px Arial') -> None:
        """Draw text on the canvas."""
        if hasattr(ctx, 'fillText'):
            # HTML5 Canvas
            ctx.fillStyle = color
            ctx.font = font
            ctx.fillText(text, x, y)
        else:
            # Generic drawing interface
            self._draw_text_generic(ctx, text, x, y, color, font)
    
    def draw_line(self, ctx: Any, x1: int, y1: int, x2: int, y2: int, 
                 color: str = '#ffffff', width: int = 1) -> None:
        """Draw a line on the canvas."""
        if hasattr(ctx, 'beginPath'):
            # HTML5 Canvas
            ctx.beginPath()
            ctx.moveTo(x1, y1)
            ctx.lineTo(x2, y2)
            ctx.strokeStyle = color
            ctx.lineWidth = width
            ctx.stroke()
        else:
            # Generic drawing interface
            self._draw_line_generic(ctx, x1, y1, x2, y2, color, width)
    
    def _draw_circle_generic(self, ctx: Any, x: int, y: int, radius: int, 
                            color: str, fill: bool) -> None:
        """Generic circle drawing implementation."""
        # Override in subclasses for specific drawing backends
        pass
    
    def _draw_text_generic(self, ctx: Any, text: str, x: int, y: int, 
                          color: str, font: str) -> None:
        """Generic text drawing implementation."""
        # Override in subclasses for specific drawing backends
        pass
    
    def _draw_line_generic(self, ctx: Any, x1: int, y1: int, x2: int, y2: int, 
                          color: str, width: int) -> None:
        """Generic line drawing implementation."""
        # Override in subclasses for specific drawing backends
        pass
    
    def clear(self, ctx: Any) -> None:
        """Clear the canvas."""
        if hasattr(ctx, 'clearRect'):
            # HTML5 Canvas
            ctx.clearRect(0, 0, self.canvas_width, self.canvas_height)
        else:
            # Generic drawing interface
            self._clear_generic(ctx)
    
    def _clear_generic(self, ctx: Any) -> None:
        """Generic clear implementation."""
        # Override in subclasses for specific drawing backends
        pass 