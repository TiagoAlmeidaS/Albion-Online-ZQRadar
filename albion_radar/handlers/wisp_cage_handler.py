"""
Wisp Cage Handler for Albion Radar

Handles wisp cage detection and management.
"""

import time
from typing import Dict, List
from dataclasses import dataclass, field
from ..config.settings import Settings


@dataclass
class Cage:
    """Represents a wisp cage"""
    id: int
    pos_x: float
    pos_y: float
    name: str
    h_x: float = 0.0
    h_y: float = 0.0


class WispCageHandler:
    """
    Handles wisp cage detection and management.
    
    Based on the original JavaScript WispCageHandler.js
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.cages: List[Cage] = []
    
    def add_cage(self, cage_id: int, pos_x: float, pos_y: float, name: str) -> None:
        """Add a new wisp cage"""
        cage = Cage(id=cage_id, pos_x=pos_x, pos_y=pos_y, name=name)
        
        # Check if cage already exists
        if not any(c.id == cage_id for c in self.cages):
            self.cages.append(cage)
    
    def remove_cage(self, cage_id: int) -> None:
        """Remove a wisp cage"""
        self.cages = [c for c in self.cages if c.id != cage_id]
    
    def handle_new_cage_event(self, parameters: Dict) -> None:
        """Handle new cage event"""
        try:
            cage_id = parameters.get(0)
            position = parameters.get(1, [0, 0])
            name = parameters.get(2, "")
            
            if not cage_id or not position:
                return
                
            pos_x, pos_y = position[0], position[1]
            
            self.add_cage(cage_id, pos_x, pos_y, name)
            
        except Exception as e:
            print(f"Error handling new cage event: {e}")
    
    def handle_cage_opened_event(self, parameters: Dict) -> None:
        """Handle cage opened event"""
        try:
            cage_id = parameters.get(0)
            if cage_id:
                self.remove_cage(cage_id)
        except Exception as e:
            print(f"Error handling cage opened event: {e}")
    
    def get_cages_list(self) -> List[Cage]:
        """Get all wisp cages"""
        return self.cages.copy()
    
    def clear(self) -> None:
        """Clear all wisp cages"""
        self.cages.clear() 