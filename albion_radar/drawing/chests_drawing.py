"""
Chests Drawing Component for Albion Radar

This module handles the drawing of chests on the radar,
based on the original ChestsDrawing.js.
"""

from typing import Dict, Any, List, Optional
from .base_drawing import BaseDrawing
import math


class ChestsDrawing(BaseDrawing):
    """Drawing component for chests on the radar."""
    
    def __init__(self, canvas_width: int = 500, canvas_height: int = 500):
        """Initialize chests drawing component."""
        super().__init__(canvas_width, canvas_height)
        self.chest_colors = {
            'green': '#00ff00',   # Green
            'blue': '#0066ff',    # Blue
            'purple': '#9900ff',  # Purple
            'yellow': '#ffff00',  # Yellow
            'legendary': '#ff6600', # Orange
        }
        
        self.chest_symbols = {
            'green': '📦',
            'blue': '📦',
            'purple': '📦',
            'yellow': '📦',
            'legendary': '📦',
        }
    
    def draw(self, ctx: Any) -> None:
        """Draw all chests on the radar."""
        if not self.data:
            return
        
        for chest in self.data:
            self._draw_chest(ctx, chest)
    
    def _draw_chest(self, ctx: Any, chest: Dict[str, Any]) -> None:
        """Draw a single chest on the radar."""
        # Extract chest data
        x = chest.get('x', 0)
        y = chest.get('y', 0)
        chest_type = chest.get('type', 'green')
        tier = chest.get('tier', 1)
        enchant = chest.get('enchant', 0)
        name = chest.get('name', 'Chest')
        
        # Check if chest should be shown based on settings
        if not self._should_show_chest(chest):
            return
        
        # Convert world coordinates to screen coordinates
        screen_x, screen_y = self.world_to_screen(x, y)
        
        # Check if chest is in range
        if not self.is_in_range(x, y):
            return
        
        # Get chest color and symbol
        color = self.chest_colors.get(chest_type.lower(), '#ffffff')
        symbol = self.chest_symbols.get(chest_type.lower(), '📦')
        
        # Draw chest
        self._draw_chest_marker(ctx, screen_x, screen_y, color, symbol, tier, enchant)
        
        # Draw chest name
        self._draw_chest_name(ctx, screen_x, screen_y, name, color)
    
    def _should_show_chest(self, chest: Dict[str, Any]) -> bool:
        """Check if chest should be shown based on settings."""
        chest_type = chest.get('type', 'green').lower()
        
        # Check chest type settings
        if chest_type == 'green' and not self.settings.get('chest_green', False):
            return False
        if chest_type == 'blue' and not self.settings.get('chest_blue', False):
            return False
        if chest_type == 'purple' and not self.settings.get('chest_purple', False):
            return False
        if chest_type == 'yellow' and not self.settings.get('chest_yellow', False):
            return False
        
        return True
    
    def _draw_chest_marker(self, ctx: Any, x: int, y: int, color: str, 
                          symbol: str, tier: int, enchant: int) -> None:
        """Draw chest marker on radar."""
        # Draw chest symbol
        self.draw_text(ctx, symbol, x, y, color, '16px Arial')
        
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
        self.draw_text(ctx, tier_text, tier_x, tier_y, color, '8px Arial')
    
    def _draw_chest_name(self, ctx: Any, x: int, y: int, name: str, color: str) -> None:
        """Draw chest name."""
        # Position text above chest symbol
        text_x = x
        text_y = y - 15
        
        # Truncate name if too long
        display_name = name[:10] if len(name) > 10 else name
        
        # Draw background for better visibility
        self._draw_text_background(ctx, text_x, text_y, display_name)
        
        # Draw text
        self.draw_text(ctx, display_name, text_x, text_y, color, '8px Arial')
    
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