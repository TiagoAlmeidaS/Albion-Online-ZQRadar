"""
Players Drawing Component for Albion Radar

This module handles the drawing of players on the radar,
based on the original PlayersDrawing.js.
"""

from typing import Dict, Any, List, Optional
from .base_drawing import BaseDrawing
import math


class PlayersDrawing(BaseDrawing):
    """Drawing component for players on the radar."""
    
    def __init__(self, canvas_width: int = 500, canvas_height: int = 500):
        """Initialize players drawing component."""
        super().__init__(canvas_width, canvas_height)
        self.player_colors = {
            'FRIENDLY': '#00ff00',    # Green
            'HOSTILE': '#ff0000',     # Red
            'NEUTRAL': '#ffff00',     # Yellow
            'CAERLEON': '#ff6600',    # Orange
            'BRIDGEWATCH': '#0066ff', # Blue
            'FORTSTERLING': '#9900ff', # Purple
            'LYMHURST': '#00ff66',    # Light Green
            'MARTLOCK': '#ff0066',    # Pink
            'THETFORD': '#ff9900',    # Dark Orange
        }
    
    def draw(self, ctx: Any) -> None:
        """Draw all players on the radar."""
        if not self.data:
            return
        
        for player in self.data:
            self._draw_player(ctx, player)
    
    def _draw_player(self, ctx: Any, player: Dict[str, Any]) -> None:
        """Draw a single player on the radar."""
        # Extract player data
        x = player.get('x', 0)
        y = player.get('y', 0)
        name = player.get('name', 'Unknown')
        health = player.get('health', 100)
        max_health = player.get('max_health', 100)
        faction = player.get('faction', 'NEUTRAL')
        guild = player.get('guild', '')
        mounted = player.get('mounted', False)
        distance = player.get('distance', 0)
        items = player.get('items', [])
        
        # Check if player should be shown based on settings
        if not self._should_show_player(player):
            return
        
        # Convert world coordinates to screen coordinates
        screen_x, screen_y = self.world_to_screen(x, y)
        
        # Check if player is in range
        if not self.is_in_range(x, y):
            return
        
        # Get player color based on faction
        color = self.get_color_by_faction(faction)
        
        # Draw player dot
        self._draw_player_dot(ctx, screen_x, screen_y, color, mounted)
        
        # Draw player name
        if self.settings.get('setting_nickname', False):
            self._draw_player_name(ctx, screen_x, screen_y, name, color)
        
        # Draw player health
        if self.settings.get('setting_health', False):
            self._draw_player_health(ctx, screen_x, screen_y, health, max_health)
        
        # Draw player guild
        if self.settings.get('setting_guild', False) and guild:
            self._draw_player_guild(ctx, screen_x, screen_y, guild, color)
        
        # Draw player distance
        if self.settings.get('setting_distance', False):
            self._draw_player_distance(ctx, screen_x, screen_y, distance)
        
        # Draw player items
        if self.settings.get('setting_items', False):
            self._draw_player_items(ctx, screen_x, screen_y, items)
        
        # Draw player items (dev mode)
        if self.settings.get('setting_items_dev', False):
            self._draw_player_items_dev(ctx, screen_x, screen_y, items)
    
    def _should_show_player(self, player: Dict[str, Any]) -> bool:
        """Check if player should be shown based on settings."""
        # Check ignore list
        name = player.get('name', '')
        if name in self.settings.get('ignore_list', []):
            return False
        
        # Check player type settings
        player_type = player.get('type', 'NEUTRAL')
        
        if player_type == 'PASSIVE' and not self.settings.get('setting_passive_players', False):
            return False
        
        if player_type == 'FACTION' and not self.settings.get('setting_faction_players', False):
            return False
        
        if player_type == 'DANGEROUS' and not self.settings.get('setting_dangerous_players', False):
            return False
        
        return True
    
    def _draw_player_dot(self, ctx: Any, x: int, y: int, color: str, mounted: bool) -> None:
        """Draw player dot on radar."""
        radius = 3 if not mounted else 5
        
        # Draw main dot
        self.draw_circle(ctx, x, y, radius, color, fill=True)
        
        # Draw border
        self.draw_circle(ctx, x, y, radius, '#000000', fill=False)
        
        # Draw mount indicator
        if mounted:
            self.draw_circle(ctx, x, y, radius + 2, color, fill=False)
    
    def _draw_player_name(self, ctx: Any, x: int, y: int, name: str, color: str) -> None:
        """Draw player name."""
        # Position text above player dot
        text_x = x
        text_y = y - 15
        
        # Draw background for better visibility
        self._draw_text_background(ctx, text_x, text_y, name)
        
        # Draw text
        self.draw_text(ctx, name, text_x, text_y, color, '10px Arial')
    
    def _draw_player_health(self, ctx: Any, x: int, y: int, health: int, max_health: int) -> None:
        """Draw player health bar."""
        if max_health <= 0:
            return
        
        health_percentage = health / max_health
        bar_width = 20
        bar_height = 3
        
        # Position health bar below player dot
        bar_x = x - bar_width // 2
        bar_y = y + 8
        
        # Draw background
        self.draw_line(ctx, bar_x, bar_y, bar_x + bar_width, bar_y, '#000000', bar_height)
        
        # Draw health
        health_width = int(bar_width * health_percentage)
        health_color = self._get_health_color(health_percentage)
        self.draw_line(ctx, bar_x, bar_y, bar_x + health_width, bar_y, health_color, bar_height)
    
    def _draw_player_guild(self, ctx: Any, x: int, y: int, guild: str, color: str) -> None:
        """Draw player guild name."""
        # Position text below health bar
        text_x = x
        text_y = y + 25
        
        # Draw background for better visibility
        self._draw_text_background(ctx, text_x, text_y, guild)
        
        # Draw text
        self.draw_text(ctx, guild, text_x, text_y, color, '8px Arial')
    
    def _draw_player_distance(self, ctx: Any, x: int, y: int, distance: float) -> None:
        """Draw player distance."""
        # Position text to the right of player dot
        text_x = x + 15
        text_y = y
        
        distance_text = f"{distance:.1f}m"
        
        # Draw background for better visibility
        self._draw_text_background(ctx, text_x, text_y, distance_text)
        
        # Draw text
        self.draw_text(ctx, distance_text, text_x, text_y, '#ffffff', '8px Arial')
    
    def _draw_player_items(self, ctx: Any, x: int, y: int, items: List[Dict[str, Any]]) -> None:
        """Draw player items."""
        if not items:
            return
        
        # Position items to the left of player dot
        item_x = x - 30
        item_y = y
        
        for i, item in enumerate(items[:3]):  # Show only first 3 items
            item_name = item.get('name', 'Unknown')
            item_rarity = item.get('rarity', 'common')
            
            # Draw item background
            self._draw_text_background(ctx, item_x, item_y + i * 12, item_name)
            
            # Draw item name with rarity color
            rarity_color = self.get_color_by_rarity(item_rarity)
            self.draw_text(ctx, item_name, item_x, item_y + i * 12, rarity_color, '8px Arial')
    
    def _draw_player_items_dev(self, ctx: Any, x: int, y: int, items: List[Dict[str, Any]]) -> None:
        """Draw player items in development mode."""
        if not items:
            return
        
        # Position items to the right of player dot
        item_x = x + 15
        item_y = y + 15
        
        for i, item in enumerate(items):
            item_name = item.get('name', 'Unknown')
            item_tier = item.get('tier', 0)
            item_enchant = item.get('enchant', 0)
            
            # Format item display
            item_display = f"{item_name} T{item_tier}"
            if item_enchant > 0:
                item_display += f".{item_enchant}"
            
            # Draw item background
            self._draw_text_background(ctx, item_x, item_y + i * 10, item_display)
            
            # Draw item
            self.draw_text(ctx, item_display, item_x, item_y + i * 10, '#ffffff', '7px Arial')
    
    def _draw_text_background(self, ctx: Any, x: int, y: int, text: str) -> None:
        """Draw background for text to improve visibility."""
        # Estimate text width (rough calculation)
        text_width = len(text) * 6  # Approximate width per character
        text_height = 12
        
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