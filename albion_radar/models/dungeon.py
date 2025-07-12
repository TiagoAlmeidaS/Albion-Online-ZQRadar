"""
Dungeon model for Albion Radar
"""

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Dungeon:
    """
    Represents a dungeon detected by the radar.
    """
    id: int
    dungeon_type: str
    pos_x: float = 0.0
    pos_y: float = 0.0
    detected_at: float = field(default_factory=lambda: __import__('time').time())
    last_update: float = field(default_factory=lambda: __import__('time').time())

    def update_position(self, new_x: float, new_y: float):
        self.pos_x = new_x
        self.pos_y = new_y
        self.last_update = __import__('time').time()

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'dungeon_type': self.dungeon_type,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'detected_at': self.detected_at,
            'last_update': self.last_update
        }

    def __str__(self) -> str:
        return f"Dungeon({self.dungeon_type}, ID: {self.id})"

    def __repr__(self) -> str:
        return (f"Dungeon(id={self.id}, dungeon_type='{self.dungeon_type}', "
                f"pos=({self.pos_x:.2f}, {self.pos_y:.2f}))") 