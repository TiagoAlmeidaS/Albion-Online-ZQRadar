"""
Resource model for Albion Radar
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum

class ResourceType(Enum):
    """Resource types"""
    FIBER = "fiber"
    WOOD = "wood"
    HIDE = "hide"
    ORE = "ore"
    ROCK = "rock"
    FISH = "fish"
    UNKNOWN = "unknown"

class ResourceEnchant(Enum):
    """Resource enchantment levels"""
    NONE = 0
    UNCOMMON = 1
    RARE = 2
    EXCEPTIONAL = 3
    MASTERWORK = 4

@dataclass
class Resource:
    """
    Represents a resource detected by the radar.
    
    Based on the original JavaScript resource handling from HarvestablesHandler.js
    """
    
    # Basic info
    id: int
    type: ResourceType
    tier: int
    
    # Position
    pos_x: float
    pos_y: float
    
    # Properties
    enchant: ResourceEnchant = ResourceEnchant.NONE
    is_living: bool = False
    is_static: bool = True
    
    # State
    is_harvested: bool = False
    health: Optional[int] = None
    max_health: Optional[int] = None
    
    # Timestamps
    detected_at: float = field(default_factory=lambda: __import__('time').time())
    last_update: float = field(default_factory=lambda: __import__('time').time())
    
    @property
    def is_alive(self) -> bool:
        """Check if resource is alive (for living resources)"""
        if self.health is None or self.max_health is None:
            return True
        return self.health > 0
    
    @property
    def health_percentage(self) -> float:
        """Get health as percentage (for living resources)"""
        if self.max_health is None or self.max_health == 0:
            return 100.0
        return (self.health or 0) / self.max_health * 100
    
    @property
    def full_name(self) -> str:
        """Get full resource name with tier and enchant"""
        enchant_suffix = f"_{self.enchant.value}" if self.enchant != ResourceEnchant.NONE else ""
        return f"{self.type.value}_{self.tier}{enchant_suffix}"
    
    @property
    def display_name(self) -> str:
        """Get display name for UI"""
        enchant_name = f" ({self.enchant.name})" if self.enchant != ResourceEnchant.NONE else ""
        return f"{self.type.value.title()} T{self.tier}{enchant_name}"
    
    def update_position(self, new_x: float, new_y: float):
        """Update resource position"""
        self.pos_x = new_x
        self.pos_y = new_y
        self.last_update = __import__('time').time()
    
    def update_health(self, health: int, max_health: Optional[int] = None):
        """Update resource health (for living resources)"""
        self.health = health
        if max_health is not None:
            self.max_health = max_health
        self.last_update = __import__('time').time()
    
    def mark_harvested(self):
        """Mark resource as harvested"""
        self.is_harvested = True
        self.last_update = __import__('time').time()
    
    def get_distance_to(self, x: float, y: float) -> float:
        """Calculate distance to a point"""
        return ((self.pos_x - x) ** 2 + (self.pos_y - y) ** 2) ** 0.5
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'type': self.type.value,
            'tier': self.tier,
            'enchant': self.enchant.value,
            'enchant_name': self.enchant.name,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'is_living': self.is_living,
            'is_static': self.is_static,
            'is_harvested': self.is_harvested,
            'health': self.health,
            'max_health': self.max_health,
            'health_percentage': self.health_percentage,
            'full_name': self.full_name,
            'display_name': self.display_name,
            'detected_at': self.detected_at,
            'last_update': self.last_update
        }
    
    def __str__(self) -> str:
        """String representation"""
        return f"Resource({self.display_name}, ID: {self.id})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"Resource(id={self.id}, type={self.type.value}, "
                f"tier={self.tier}, enchant={self.enchant.name}, "
                f"pos=({self.pos_x:.2f}, {self.pos_y:.2f}), "
                f"living={self.is_living}, harvested={self.is_harvested})") 