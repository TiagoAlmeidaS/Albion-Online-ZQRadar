"""
Player model for Albion Radar
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class PlayerFlag(Enum):
    """Player flag types"""
    PASSIVE = 0
    FACTION_1 = 1
    FACTION_2 = 2
    FACTION_3 = 3
    FACTION_4 = 4
    FACTION_5 = 5
    FACTION_6 = 6
    DANGEROUS = 255

@dataclass
class Player:
    """
    Represents a player detected by the radar.
    
    Based on the original JavaScript Player class from PlayersHandler.js
    """
    
    # Basic info
    id: int
    nickname: str
    guild_name: str = ""
    alliance_name: str = ""
    
    # Position
    pos_x: float = 0.0
    pos_y: float = 0.0
    old_pos_x: float = 0.0
    old_pos_y: float = 0.0
    
    # Health
    current_health: int = 0
    initial_health: int = 0
    
    # Equipment and status
    items: List = field(default_factory=list)
    flag_id: int = 0
    mounted: bool = False
    
    # Movement
    h_x: float = 0.0
    h_y: float = 0.0
    
    # Distance tracking
    distance: int = 0
    
    # Timestamps
    detected_at: float = field(default_factory=lambda: __import__('time').time())
    last_update: float = field(default_factory=lambda: __import__('time').time())
    
    def __post_init__(self):
        """Post-initialization setup"""
        self.old_pos_x = self.pos_x
        self.old_pos_y = self.pos_y
    
    @property
    def flag_type(self) -> PlayerFlag:
        """Get the player flag type"""
        try:
            return PlayerFlag(self.flag_id)
        except ValueError:
            return PlayerFlag.PASSIVE
    
    @property
    def is_passive(self) -> bool:
        """Check if player is passive"""
        return self.flag_id == 0
    
    @property
    def is_faction(self) -> bool:
        """Check if player is faction"""
        return 1 <= self.flag_id <= 6
    
    @property
    def is_dangerous(self) -> bool:
        """Check if player is dangerous"""
        return self.flag_id == 255
    
    @property
    def health_percentage(self) -> float:
        """Get health as percentage"""
        if self.initial_health == 0:
            return 0.0
        return (self.current_health / self.initial_health) * 100
    
    @property
    def is_alive(self) -> bool:
        """Check if player is alive"""
        return self.current_health > 0
    
    def update_position(self, new_x: float, new_y: float):
        """Update player position"""
        self.old_pos_x = self.pos_x
        self.old_pos_y = self.pos_y
        self.pos_x = new_x
        self.pos_y = new_y
        self.last_update = __import__('time').time()
    
    def update_health(self, current: int, initial: Optional[int] = None):
        """Update player health"""
        self.current_health = current
        if initial is not None:
            self.initial_health = initial
        self.last_update = __import__('time').time()
    
    def update_items(self, items: List):
        """Update player items"""
        self.items = items
        self.last_update = __import__('time').time()
    
    def set_mounted(self, mounted: bool):
        """Set mounted status"""
        self.mounted = mounted
        self.last_update = __import__('time').time()
    
    def get_distance_to(self, x: float, y: float) -> float:
        """Calculate distance to a point"""
        return ((self.pos_x - x) ** 2 + (self.pos_y - y) ** 2) ** 0.5
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'nickname': self.nickname,
            'guild_name': self.guild_name,
            'alliance_name': self.alliance_name,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'current_health': self.current_health,
            'initial_health': self.initial_health,
            'health_percentage': self.health_percentage,
            'flag_id': self.flag_id,
            'flag_type': self.flag_type.name,
            'mounted': self.mounted,
            'items': self.items,
            'detected_at': self.detected_at,
            'last_update': self.last_update
        }
    
    def __str__(self) -> str:
        """String representation"""
        return f"Player({self.nickname}, ID: {self.id}, Guild: {self.guild_name})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"Player(id={self.id}, nickname='{self.nickname}', "
                f"guild='{self.guild_name}', pos=({self.pos_x:.2f}, {self.pos_y:.2f}), "
                f"health={self.current_health}/{self.initial_health}, "
                f"flag={self.flag_type.name}, mounted={self.mounted})") 