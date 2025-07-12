"""
Chest model for Albion Radar
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Chest:
    """
    Represents a chest detected by the radar.
    """
    id: int
    chest_type: str
    rarity: str = "common"
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
            'chest_type': self.chest_type,
            'rarity': self.rarity,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'detected_at': self.detected_at,
            'last_update': self.last_update
        }

    def __str__(self) -> str:
        return f"Chest({self.chest_type}, ID: {self.id}, Rarity: {self.rarity})"

    def __repr__(self) -> str:
        return (f"Chest(id={self.id}, chest_type='{self.chest_type}', rarity='{self.rarity}', "
                f"pos=({self.pos_x:.2f}, {self.pos_y:.2f}))") 