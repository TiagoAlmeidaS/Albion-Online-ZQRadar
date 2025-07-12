"""
Dungeons Drawing Component for Albion Radar

This module handles the drawing of dungeons on the radar,
based on the original DungeonsDrawing.js.
"""

from typing import Dict, Any, List, Optional
from .base_drawing import BaseDrawing
import math


class DungeonsDrawing(BaseDrawing):
    """Drawing component for dungeons on the radar."""
    
    def __init__(self, canvas_width: int = 500, canvas_height: int = 500):
        """Initialize dungeons drawing component."""
        super().__init__(canvas_width, canvas_height)
        self.dungeon_colors = {
            'solo': '#00ff00',      # Green
            'group': '#ff6600',     # Orange
            'corrupted': '#ff0000',  # Red
            'hellgate': '#9900ff',   # Purple
        }
        
        self.dungeon_symbols = {
            'solo': '🏰',
            'group': '🏰',
            'corrupted': '🏰',
            'hellgate': '🏰',
        }
    
    def draw(self, ctx: Any) -> None:
        """Draw all dungeons on the radar."""
        if not self.data:
            return
        
        for dungeon in self.data:
            self._draw_dungeon(ctx, dungeon)
    
    def _draw_dungeon(self, ctx: Any, dungeon: Dict[str, Any]) -> None:
        """Draw a single dungeon on the radar."""
        # Extract dungeon data
        x = dungeon.get('x', 0)
        y = dungeon.get('y', 0)
        dungeon_type = dungeon.get('type', 'solo')
        tier = dungeon.get('tier', 1)
        enchant = dungeon.get('enchant', 0)
        name = dungeon.get('name', 'Dungeon')
        
        # Check if dungeon should be shown based on settings
        if not self._should_show_dungeon(dungeon):
            return
        
        # Convert world coordinates to screen coordinates
        screen_x, screen_y = self.world_to_screen(x, y)
        
        # Check if dungeon is in range
        if not self.is_in_range(x, y):
            return
        
        # Get dungeon color and symbol
        color = self.dungeon_colors.get(dungeon_type.lower(), '#ffffff')
        symbol = self.dungeon_symbols.get(dungeon_type.lower(), '🏰')
        
        # Draw dungeon
        self._draw_dungeon_marker(ctx, screen_x, screen_y, color, symbol, tier, enchant)
        
        # Draw dungeon name
        self._draw_dungeon_name(ctx, screen_x, screen_y, name, color)
    
    def _should_show_dungeon(self, dungeon: Dict[str, Any]) -> bool:
        """Check if dungeon should be shown based on settings."""
        dungeon_type = dungeon.get('type', 'solo').lower()
        enchant = dungeon.get('enchant', 0)
        
        # Check dungeon type settings
        if dungeon_type == 'solo' and not self.settings.get('dungeon_solo', False):
            return False
        if dungeon_type == 'group' and not self.settings.get('dungeon_group', False):
            return False
        if dungeon_type == 'corrupted' and not self.settings.get('dungeon_corrupted', False):
            return False
        if dungeon_type == 'hellgate' and not self.settings.get('dungeon_hellgate', False):
            return False
        
        # Check enchant settings
        dungeon_enchants = self.settings.get('dungeon_enchants', [False] * 5)
        if 0 <= enchant < len(dungeon_enchants) and not dungeon_enchants[enchant]:
            return False
        
        return True
    
    def _draw_dungeon_marker(self, ctx: Any, x: int, y: int, color: str, 
                            symbol: str, tier: int, enchant: int) -> None:
        """Draw dungeon marker on radar."""
        # Draw dungeon symbol
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
    
    def _draw_dungeon_name(self, ctx: Any, x: int, y: int, name: str, color: str) -> None:
        """Draw dungeon name."""
        # Position text above dungeon symbol
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