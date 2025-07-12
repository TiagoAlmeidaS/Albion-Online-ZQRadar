"""
Mob model for Albion Radar
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Mob:
    """
    Represents a mob detected by the radar.
    """
    id: int
    name: str
    level: int = 0
    pos_x: float = 0.0
    pos_y: float = 0.0
    health: Optional[int] = None
    max_health: Optional[int] = None
    detected_at: float = field(default_factory=lambda: __import__('time').time())
    last_update: float = field(default_factory=lambda: __import__('time').time())

    @property
    def is_alive(self) -> bool:
        if self.health is None or self.max_health is None:
            return True
        return self.health > 0

    @property
    def health_percentage(self) -> float:
        if self.max_health is None or self.max_health == 0:
            return 100.0
        return (self.health or 0) / self.max_health * 100

    def update_position(self, new_x: float, new_y: float):
        self.pos_x = new_x
        self.pos_y = new_y
        self.last_update = __import__('time').time()

    def update_health(self, health: int, max_health: Optional[int] = None):
        self.health = health
        if max_health is not None:
            self.max_health = max_health
        self.last_update = __import__('time').time()

    def get_distance_to(self, x: float, y: float) -> float:
        return ((self.pos_x - x) ** 2 + (self.pos_y - y) ** 2) ** 0.5

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'health': self.health,
            'max_health': self.max_health,
            'health_percentage': self.health_percentage,
            'detected_at': self.detected_at,
            'last_update': self.last_update
        }

    def __str__(self) -> str:
        return f"Mob({self.name}, ID: {self.id}, Level: {self.level})"

    def __repr__(self) -> str:
        return (f"Mob(id={self.id}, name='{self.name}', level={self.level}, "
                f"pos=({self.pos_x:.2f}, {self.pos_y:.2f}), health={self.health}/{self.max_health})") 