"""
Players Handler for Albion Radar

Handles player detection, tracking, and management.
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from ..models.player import Player, PlayerFlag
from ..config.settings import Settings


@dataclass
class LocalPlayer:
    """Local player data"""
    pos_x: float = 0.0
    pos_y: float = 0.0
    next_pos_x: float = 0.0
    next_pos_y: float = 0.0


class PlayersHandler:
    """
    Handles player detection and management.
    
    Based on the original JavaScript PlayersHandler.js
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.players: Dict[int, Player] = {}
        self.local_player = LocalPlayer()
        self._last_update = time.time()
    
    def add_player(self, pos_x: float, pos_y: float, player_id: int, 
                   nickname: str, guild_name: str = "", current_health: int = 0,
                   initial_health: int = 0, items: Optional[List] = None, 
                   sound: bool = False, flag_id: int = 0) -> None:
        """Add a new player to the tracking list"""
        
        if player_id in self.players:
            return  # Player already exists
            
        player = Player(
            id=player_id,
            nickname=nickname,
            guild_name=guild_name,
            pos_x=pos_x,
            pos_y=pos_y,
            current_health=current_health,
            initial_health=initial_health,
            items=items or [],
            flag_id=flag_id
        )
        
        self.players[player_id] = player
        
        if sound and self.settings.player_sound:
            # TODO: Implement sound notification
            pass
    
    def remove_player(self, player_id: int) -> None:
        """Remove a player from tracking"""
        if player_id in self.players:
            del self.players[player_id]
    
    def update_player_position(self, player_id: int, pos_x: float, pos_y: float) -> None:
        """Update player position"""
        if player_id in self.players:
            player = self.players[player_id]
            player.old_pos_x = player.pos_x
            player.old_pos_y = player.pos_y
            player.pos_x = pos_x
            player.pos_y = pos_y
            player.last_update = time.time()
    
    def update_player_health(self, player_id: int, current_health: int, initial_health: int) -> None:
        """Update player health"""
        if player_id in self.players:
            player = self.players[player_id]
            player.current_health = current_health
            player.initial_health = initial_health
    
    def update_player_items(self, player_id: int, items: List) -> None:
        """Update player items"""
        if player_id in self.players:
            player = self.players[player_id]
            player.items = items
    
    def update_player_mounted(self, player_id: int, mounted: bool) -> None:
        """Update player mounted status"""
        if player_id in self.players:
            player = self.players[player_id]
            player.mounted = mounted
    
    def update_local_player_position(self, pos_x: float, pos_y: float) -> None:
        """Update local player position"""
        self.local_player.pos_x = pos_x
        self.local_player.pos_y = pos_y
    
    def update_local_player_next_position(self, pos_x: float, pos_y: float) -> None:
        """Update local player next position for interpolation"""
        self.local_player.next_pos_x = pos_x
        self.local_player.next_pos_y = pos_y
    
    def get_players_in_range(self, max_distance: float = 80.0) -> List[Player]:
        """Get all players within range of local player"""
        players_in_range = []
        
        for player in self.players.values():
            distance = self._calculate_distance(
                self.local_player.pos_x, self.local_player.pos_y,
                player.pos_x, player.pos_y
            )
            if distance <= max_distance:
                player.distance = int(distance)
                players_in_range.append(player)
        
        return players_in_range
    
    def handle_new_player_event(self, parameters: Dict, is_bz: bool = False) -> None:
        """Handle new player event from packet data"""
        try:
            player_id = parameters.get(0)
            position = parameters.get(1, [0, 0])
            nickname = parameters.get(2, "")
            guild_name = parameters.get(3, "")
            alliance_name = parameters.get(4, "")
            current_health = parameters.get(5, 0)
            initial_health = parameters.get(6, 0)
            items = parameters.get(7, [])
            flag_id = parameters.get(8, 0)
            
            if not player_id or not position:
                return
                
            pos_x, pos_y = position[0], position[1]
            
            self.add_player(
                pos_x=pos_x,
                pos_y=pos_y,
                player_id=player_id,
                nickname=nickname,
                guild_name=guild_name,
                current_health=current_health,
                initial_health=initial_health,
                items=items,
                flag_id=flag_id
            )
            
        except Exception as e:
            print(f"Error handling new player event: {e}")
    
    def handle_mounted_player_event(self, player_id: int, parameters: Dict) -> None:
        """Handle player mounted event"""
        try:
            mounted = parameters.get(0, False)
            self.update_player_mounted(player_id, mounted)
        except Exception as e:
            print(f"Error handling mounted player event: {e}")
    
    def clear(self) -> None:
        """Clear all players"""
        self.players.clear()
    
    def _calculate_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate distance between two points"""
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 