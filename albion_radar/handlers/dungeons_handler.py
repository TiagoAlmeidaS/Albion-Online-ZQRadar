"""
Dungeons Handler for Albion Radar

Handles dungeon detection and management.
"""

import time
from typing import Dict, List
from dataclasses import dataclass, field
from enum import Enum
from ..models.dungeon import Dungeon
from ..config.settings import Settings


class DungeonType(Enum):
    """Dungeon types"""
    SOLO = 0
    GROUP = 1
    CORRUPTED = 2
    HELLGATE = 3


@dataclass
class DungeonData:
    """Represents a dungeon"""
    id: int
    pos_x: float
    pos_y: float
    name: str
    enchant: int
    type: DungeonType
    draw_name: str = ""
    h_x: float = 0.0
    h_y: float = 0.0
    
    def __post_init__(self):
        """Set draw name based on type"""
        if self.type == DungeonType.SOLO:
            self.draw_name = f"dungeon_{self.enchant}"
        elif self.type == DungeonType.GROUP:
            self.draw_name = f"group_{self.enchant}"
        elif self.type == DungeonType.CORRUPTED:
            self.draw_name = "corrupt"
        elif self.type == DungeonType.HELLGATE:
            self.draw_name = "hellgate"


class DungeonsHandler:
    """
    Handles dungeon detection and management.
    
    Based on the original JavaScript DungeonsHandler.js
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.dungeon_list: List[DungeonData] = []
    
    def add_dungeon(self, dungeon_id: int, pos_x: float, pos_y: float, 
                    name: str, enchant: int) -> None:
        """Add a new dungeon"""
        
        # Determine dungeon type from name
        dungeon_type = self._get_dungeon_type(name, enchant)
        if dungeon_type is None:
            return
        
        # Check if dungeon already exists
        if any(d.id == dungeon_id for d in self.dungeon_list):
            return
        
        dungeon = DungeonData(
            id=dungeon_id,
            pos_x=pos_x,
            pos_y=pos_y,
            name=name,
            enchant=enchant,
            type=dungeon_type
        )
        
        self.dungeon_list.append(dungeon)
    
    def remove_dungeon(self, dungeon_id: int) -> None:
        """Remove a dungeon"""
        self.dungeon_list = [d for d in self.dungeon_list if d.id != dungeon_id]
    
    def handle_dungeon_event(self, parameters: Dict) -> None:
        """Handle dungeon event"""
        try:
            dungeon_id = parameters.get(0)
            position = parameters.get(1, [0, 0])
            name = parameters.get(3, "")
            enchant = parameters.get(6, 0)
            
            if not dungeon_id or not position:
                return
                
            pos_x, pos_y = position[0], position[1]
            
            self.add_dungeon(dungeon_id, pos_x, pos_y, name, enchant)
            
        except Exception as e:
            print(f"Error handling dungeon event: {e}")
    
    def get_dungeon_list(self) -> List[DungeonData]:
        """Get all dungeons"""
        return self.dungeon_list.copy()
    
    def clear(self) -> None:
        """Clear all dungeons"""
        self.dungeon_list.clear()
    
    def _get_dungeon_type(self, name: str, enchant: int) -> DungeonType:
        """Get dungeon type from name and settings"""
        name_lower = name.lower()
        
        # Check corrupted first (has "solo" in name)
        if "corrupted" in name_lower:
            if not self.settings.show_dungeons:
                return DungeonType.SOLO  # Default return
            return DungeonType.CORRUPTED
        
        # Check solo dungeons
        elif "solo" in name_lower:
            if not self.settings.show_dungeons:
                return DungeonType.SOLO  # Default return
            return DungeonType.SOLO
        
        # Check hellgate
        elif "hellgate" in name_lower:
            if not self.settings.show_dungeons:
                return DungeonType.SOLO  # Default return
            return DungeonType.HELLGATE
        
        # Default to group
        else:
            if not self.settings.show_dungeons:
                return DungeonType.SOLO  # Default return
            return DungeonType.GROUP 