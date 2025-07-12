"""
Harvestables Drawing Component for Albion Radar

This module handles the drawing of harvestable resources on the radar,
based on the original HarvestablesDrawing.js.
"""

from typing import Dict, Any, List, Optional
from .base_drawing import BaseDrawing
import math


class HarvestablesDrawing(BaseDrawing):
    """Drawing component for harvestable resources on the radar."""
    
    def __init__(self, canvas_width: int = 500, canvas_height: int = 500):
        """Initialize harvestables drawing component."""
        super().__init__(canvas_width, canvas_height)
        self.resource_colors = {
            'fiber': '#00ff00',  # Green
            'wood': '#8b4513',   # Brown
            'hide': '#ffd700',   # Gold
            'ore': '#808080',    # Gray
            'rock': '#a0522d',   # Saddle Brown
            'fish': '#4169e1',   # Royal Blue
        }
        
        self.resource_symbols = {
            'fiber': '🌿',
            'wood': '🌳',
            'hide': '🦌',
            'ore': '⛏️',
            'rock': '🪨',
            'fish': '🐟',
        }
    
    def draw(self, ctx: Any) -> None:
        """Draw all harvestable resources on the radar."""
        if not self.data:
            return
        
        for resource in self.data:
            self._draw_resource(ctx, resource)
    
    def _draw_resource(self, ctx: Any, resource: Dict[str, Any]) -> None:
        """Draw a single resource on the radar."""
        # Extract resource data
        x = resource.get('x', 0)
        y = resource.get('y', 0)
        resource_type = resource.get('type', 'unknown')
        tier = resource.get('tier', 1)
        enchant = resource.get('enchant', 0)
        health = resource.get('health', 100)
        max_health = resource.get('max_health', 100)
        resource_id = resource.get('id', '')
        is_living = resource.get('is_living', False)
        
        # Check if resource should be shown based on settings
        if not self._should_show_resource(resource):
            return
        
        # Convert world coordinates to screen coordinates
        screen_x, screen_y = self.world_to_screen(x, y)
        
        # Check if resource is in range
        if not self.is_in_range(x, y):
            return
        
        # Get resource color and symbol
        color = self.resource_colors.get(resource_type.lower(), '#ffffff')
        symbol = self.resource_symbols.get(resource_type.lower(), '❓')
        
        # Draw resource
        self._draw_resource_marker(ctx, screen_x, screen_y, color, symbol, tier, enchant)
        
        # Draw resource info
        if self.settings.get('resource_size', False):
            self._draw_resource_size(ctx, screen_x, screen_y, resource)
        
        # Draw living resource health
        if is_living and self.settings.get('living_resources_hp', False):
            self._draw_resource_health(ctx, screen_x, screen_y, health, max_health)
        
        # Draw living resource ID
        if is_living and self.settings.get('living_resources_id', False):
            self._draw_resource_id(ctx, screen_x, screen_y, resource_id)
    
    def _should_show_resource(self, resource: Dict[str, Any]) -> bool:
        """Check if resource should be shown based on settings."""
        resource_type = resource.get('type', '').lower()
        tier = resource.get('tier', 1)
        enchant = resource.get('enchant', 0)
        is_living = resource.get('is_living', False)
        
        # Get settings for this resource type
        if is_living:
            settings_key = f"harvesting_living_{resource_type}"
        else:
            settings_key = f"harvesting_static_{resource_type}"
        
        resource_settings = self.settings.get(settings_key, {})
        
        # Check if this tier/enchant combination is enabled
        enchant_key = f"e{enchant}"
        if enchant_key in resource_settings:
            tier_index = tier - 1  # Convert tier to 0-based index
            if 0 <= tier_index < len(resource_settings[enchant_key]):
                return resource_settings[enchant_key][tier_index]
        
        return False
    
    def _draw_resource_marker(self, ctx: Any, x: int, y: int, color: str, 
                            symbol: str, tier: int, enchant: int) -> None:
        """Draw resource marker on radar."""
        # Draw resource symbol
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
    
    def _draw_resource_size(self, ctx: Any, x: int, y: int, resource: Dict[str, Any]) -> None:
        """Draw resource size information."""
        size = resource.get('size', 0)
        if size <= 0:
            return
        
        # Position size text to the right of resource
        size_x = x + 15
        size_y = y
        
        size_text = f"Size: {size}"
        
        # Draw background for size text
        self._draw_text_background(ctx, size_x, size_y, size_text)
        
        # Draw size text
        self.draw_text(ctx, size_text, size_x, size_y, '#ffffff', '8px Arial')
    
    def _draw_resource_health(self, ctx: Any, x: int, y: int, health: int, max_health: int) -> None:
        """Draw living resource health bar."""
        if max_health <= 0:
            return
        
        health_percentage = health / max_health
        bar_width = 15
        bar_height = 2
        
        # Position health bar above resource
        bar_x = x - bar_width // 2
        bar_y = y - 20
        
        # Draw background
        self.draw_line(ctx, bar_x, bar_y, bar_x + bar_width, bar_y, '#000000', bar_height)
        
        # Draw health
        health_width = int(bar_width * health_percentage)
        health_color = self._get_health_color(health_percentage)
        self.draw_line(ctx, bar_x, bar_y, bar_x + health_width, bar_y, health_color, bar_height)
    
    def _draw_resource_id(self, ctx: Any, x: int, y: int, resource_id: str) -> None:
        """Draw living resource ID."""
        if not resource_id:
            return
        
        # Position ID text to the left of resource
        id_x = x - 25
        id_y = y
        
        # Truncate ID if too long
        display_id = resource_id[:8] if len(resource_id) > 8 else resource_id
        
        # Draw background for ID text
        self._draw_text_background(ctx, id_x, id_y, display_id)
        
        # Draw ID text
        self.draw_text(ctx, display_id, id_x, id_y, '#ffffff', '7px Arial')
    
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
    
    def _get_health_color(self, health_percentage: float) -> str:
        """Get color based on health percentage."""
        if health_percentage > 0.6:
            return '#00ff00'  # Green
        elif health_percentage > 0.3:
            return '#ffff00'  # Yellow
        else:
            return '#ff0000'  # Red
    
    def _draw_rect_generic(self, ctx: Any, x: int, y: int, width: int, height: int, color: str) -> None:
        """Generic rectangle drawing implementation."""
        # Override in subclasses for specific drawing backends
        pass 