"""
Chests Handler for Albion Radar

Handles chest detection and management.
"""

import time
from typing import Dict, List
from dataclasses import dataclass, field
from ..models.chest import Chest
from ..config.settings import Settings


@dataclass
class ChestData:
    """Represents a chest"""
    id: int
    pos_x: float
    pos_y: float
    chest_name: str
    h_x: float = 0.0
    h_y: float = 0.0


class ChestsHandler:
    """
    Handles chest detection and management.
    
    Based on the original JavaScript ChestsHandler.js
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.chests_list: List[ChestData] = []
    
    def add_chest(self, chest_id: int, pos_x: float, pos_y: float, name: str) -> None:
        """Add a new chest"""
        chest = ChestData(id=chest_id, pos_x=pos_x, pos_y=pos_y, chest_name=name)
        
        # Check if chest already exists
        if not any(c.id == chest_id for c in self.chests_list):
            self.chests_list.append(chest)
    
    def remove_chest(self, chest_id: int) -> None:
        """Remove a chest"""
        self.chests_list = [c for c in self.chests_list if c.id != chest_id]
    
    def handle_chest_event(self, parameters: Dict) -> None:
        """Handle chest event"""
        try:
            chest_id = parameters.get(0)
            position = parameters.get(1, [0, 0])
            chest_name = parameters.get(3, "")
            
            if not chest_id or not position:
                return
                
            pos_x, pos_y = position[0], position[1]
            
            # Handle mist chests
            if "mist" in chest_name.lower():
                chest_name = parameters.get(4, chest_name)
            
            self.add_chest(chest_id, pos_x, pos_y, chest_name)
            
        except Exception as e:
            print(f"Error handling chest event: {e}")
    
    def get_chests_list(self) -> List[ChestData]:
        """Get all chests"""
        return self.chests_list.copy()
    
    def clear(self) -> None:
        """Clear all chests"""
        self.chests_list.clear() 