"""
Mobs Drawing Component for Albion Radar

This module handles the drawing of mobs/enemies on the radar,
based on the original MobsDrawing.js.
"""

from typing import Dict, Any, List, Optional
from .base_drawing import BaseDrawing
import math


class MobsDrawing(BaseDrawing):
    """Drawing component for mobs/enemies on the radar."""
    
    def __init__(self, canvas_width: int = 500, canvas_height: int = 500):
        """Initialize mobs drawing component."""
        super().__init__(canvas_width, canvas_height)
        self.mob_colors = {
            'normal': '#ff0000',      # Red
            'elite': '#ff6600',       # Orange
            'boss': '#ff00ff',        # Magenta
            'event': '#00ffff',       # Cyan
            'avalone': '#4169e1',     # Royal Blue
            'crystal_spider': '#ff1493', # Deep Pink
            'fairy_dragon': '#00ff7f',   # Spring Green
            'veil_weaver': '#9370db',    # Medium Purple
            'griffin': '#ffd700',     # Gold
        }
        
        self.mob_symbols = {
            'normal': '👹',
            'elite': '👺',
            'boss': '👾',
            'event': '🎃',
            'avalone': '🤖',
            'crystal_spider': '🕷️',
            'fairy_dragon': '🐉',
            'veil_weaver': '🕸️',
            'griffin': '🦅',
        }
    
    def draw(self, ctx: Any) -> None:
        """Draw all mobs on the radar."""
        if not self.data:
            return
        
        for mob in self.data:
            self._draw_mob(ctx, mob)
    
    def _draw_mob(self, ctx: Any, mob: Dict[str, Any]) -> None:
        """Draw a single mob on the radar."""
        # Extract mob data
        x = mob.get('x', 0)
        y = mob.get('y', 0)
        name = mob.get('name', 'Unknown')
        health = mob.get('health', 100)
        max_health = mob.get('max_health', 100)
        level = mob.get('level', 1)
        mob_type = mob.get('type', 'normal')
        mob_id = mob.get('id', '')
        is_event = mob.get('is_event', False)
        is_avalone = mob.get('is_avalone', False)
        
        # Check if mob should be shown based on settings
        if not self._should_show_mob(mob):
            return
        
        # Convert world coordinates to screen coordinates
        screen_x, screen_y = self.world_to_screen(x, y)
        
        # Check if mob is in range
        if not self.is_in_range(x, y):
            return
        
        # Get mob color and symbol
        color = self._get_mob_color(mob_type, is_event, is_avalone)
        symbol = self._get_mob_symbol(mob_type, is_event, is_avalone)
        
        # Draw mob
        self._draw_mob_marker(ctx, screen_x, screen_y, color, symbol, level)
        
        # Draw mob name
        if self.settings.get('enemies_id', False):
            self._draw_mob_name(ctx, screen_x, screen_y, name, color)
        
        # Draw mob health
        if self.settings.get('enemies_hp', False):
            self._draw_mob_health(ctx, screen_x, screen_y, health, max_health)
        
        # Draw mob level
        self._draw_mob_level(ctx, screen_x, screen_y, level, color)
    
    def _should_show_mob(self, mob: Dict[str, Any]) -> bool:
        """Check if mob should be shown based on settings."""
        level = mob.get('level', 1)
        health = mob.get('health', 100)
        max_health = mob.get('max_health', 100)
        mob_type = mob.get('type', 'normal')
        is_event = mob.get('is_event', False)
        is_avalone = mob.get('is_avalone', False)
        
        # Check level settings
        enemy_levels = self.settings.get('enemy_levels', [False] * 5)
        level_index = min(level - 1, len(enemy_levels) - 1)
        if level_index >= 0 and not enemy_levels[level_index]:
            return False
        
        # Check minimum health setting
        if self.settings.get('show_minimum_health_enemies', False):
            minimum_health = self.settings.get('minimum_health_enemies', 2100)
            if health < minimum_health:
                return False
        
        # Check Avalone drones setting
        if is_avalone and not self.settings.get('avalone_drones', False):
            return False
        
        # Check unmanaged enemies setting
        if mob_type == 'unmanaged' and not self.settings.get('show_unmanaged_enemies', False):
            return False
        
        # Check event enemies setting
        if is_event and not self.settings.get('show_event_enemies', False):
            return False
        
        # Check specific boss settings
        if mob_type == 'crystal_spider' and not self.settings.get('boss_crystal_spider', False):
            return False
        if mob_type == 'fairy_dragon' and not self.settings.get('boss_fairy_dragon', False):
            return False
        if mob_type == 'veil_weaver' and not self.settings.get('boss_veil_weaver', False):
            return False
        if mob_type == 'griffin' and not self.settings.get('boss_griffin', False):
            return False
        
        return True
    
    def _get_mob_color(self, mob_type: str, is_event: bool, is_avalone: bool) -> str:
        """Get color for mob based on type."""
        if is_avalone:
            return self.mob_colors['avalone']
        elif is_event:
            return self.mob_colors['event']
        elif mob_type in self.mob_colors:
            return self.mob_colors[mob_type]
        else:
            return self.mob_colors['normal']
    
    def _get_mob_symbol(self, mob_type: str, is_event: bool, is_avalone: bool) -> str:
        """Get symbol for mob based on type."""
        if is_avalone:
            return self.mob_symbols['avalone']
        elif is_event:
            return self.mob_symbols['event']
        elif mob_type in self.mob_symbols:
            return self.mob_symbols[mob_type]
        else:
            return self.mob_symbols['normal']
    
    def _draw_mob_marker(self, ctx: Any, x: int, y: int, color: str, 
                         symbol: str, level: int) -> None:
        """Draw mob marker on radar."""
        # Draw mob symbol
        self.draw_text(ctx, symbol, x, y, color, '16px Arial')
        
        # Draw level indicator
        level_text = str(level)
        
        # Position level text below symbol
        level_x = x
        level_y = y + 12
        
        # Draw background for level text
        self._draw_text_background(ctx, level_x, level_y, level_text)
        
        # Draw level text
        self.draw_text(ctx, level_text, level_x, level_y, color, '8px Arial')
    
    def _draw_mob_name(self, ctx: Any, x: int, y: int, name: str, color: str) -> None:
        """Draw mob name."""
        # Position text above mob symbol
        text_x = x
        text_y = y - 15
        
        # Truncate name if too long
        display_name = name[:12] if len(name) > 12 else name
        
        # Draw background for better visibility
        self._draw_text_background(ctx, text_x, text_y, display_name)
        
        # Draw text
        self.draw_text(ctx, display_name, text_x, text_y, color, '8px Arial')
    
    def _draw_mob_health(self, ctx: Any, x: int, y: int, health: int, max_health: int) -> None:
        """Draw mob health bar."""
        if max_health <= 0:
            return
        
        health_percentage = health / max_health
        bar_width = 20
        bar_height = 3
        
        # Position health bar below mob symbol
        bar_x = x - bar_width // 2
        bar_y = y + 20
        
        # Draw background
        self.draw_line(ctx, bar_x, bar_y, bar_x + bar_width, bar_y, '#000000', bar_height)
        
        # Draw health
        health_width = int(bar_width * health_percentage)
        health_color = self._get_health_color(health_percentage)
        self.draw_line(ctx, bar_x, bar_y, bar_x + health_width, bar_y, health_color, bar_height)
    
    def _draw_mob_level(self, ctx: Any, x: int, y: int, level: int, color: str) -> None:
        """Draw mob level indicator."""
        # Position level text to the right of mob symbol
        level_x = x + 15
        level_y = y
        
        level_text = f"L{level}"
        
        # Draw background for level text
        self._draw_text_background(ctx, level_x, level_y, level_text)
        
        # Draw level text
        self.draw_text(ctx, level_text, level_x, level_y, color, '8px Arial')
    
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