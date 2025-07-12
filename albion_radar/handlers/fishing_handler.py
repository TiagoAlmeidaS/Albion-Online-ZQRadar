"""
Fishing Handler for Albion Radar

Handles fishing spot detection and management.
"""

import time
from typing import Dict, List
from dataclasses import dataclass, field
from ..config.settings import Settings


@dataclass
class Fish:
    """Represents a fishing spot"""
    id: int
    pos_x: float
    pos_y: float
    type: str
    size_spawned: int = 0
    size_left_to_spawn: int = 0
    total_size: int = 0
    h_x: float = 0.0
    h_y: float = 0.0
    
    def __post_init__(self):
        """Calculate total size"""
        self.total_size = self.size_spawned + self.size_left_to_spawn


class FishingHandler:
    """
    Handles fishing spot detection and management.
    
    Based on the original JavaScript FishingHandler.js
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.fishes: List[Fish] = []
    
    def add_fish(self, fish_id: int, pos_x: float, pos_y: float, 
                 fish_type: str, size_spawned: int = 0, size_left_to_spawn: int = 0) -> None:
        """Add a new fishing spot"""
        fish = Fish(
            id=fish_id,
            pos_x=pos_x,
            pos_y=pos_y,
            type=fish_type,
            size_spawned=size_spawned,
            size_left_to_spawn=size_left_to_spawn
        )
        
        # Update existing fish or add new one
        existing_index = next((i for i, f in enumerate(self.fishes) if f.id == fish_id), -1)
        if existing_index != -1:
            self.fishes[existing_index] = fish
        else:
            self.fishes.append(fish)
    
    def remove_fish(self, fish_id: int) -> None:
        """Remove a fishing spot"""
        self.fishes = [f for f in self.fishes if f.id != fish_id]
    
    def handle_new_fish_event(self, parameters: Dict) -> None:
        """Handle new fish event"""
        if not self.settings.show_fish:
            return
            
        try:
            fish_id = parameters.get(0)
            position = parameters.get(1, [0, 0])
            size_spawned = parameters.get(2, 0)
            size_left_to_spawn = parameters.get(3, 0)
            fish_type = parameters.get(4, "")
            
            if not fish_id or not position or not fish_type:
                return
                
            pos_x, pos_y = position[0], position[1]
            
            self.add_fish(fish_id, pos_x, pos_y, fish_type, size_spawned, size_left_to_spawn)
            
        except Exception as e:
            print(f"Error handling new fish event: {e}")
    
    def handle_fishing_end_event(self, parameters: Dict) -> None:
        """Handle fishing end event"""
        if not self.settings.show_fish:
            return
            
        try:
            fish_id = parameters.get(0)
            if fish_id and any(f.id == fish_id for f in self.fishes):
                self.remove_fish(fish_id)
        except Exception as e:
            print(f"Error handling fishing end event: {e}")
    
    def get_fishes_list(self) -> List[Fish]:
        """Get all fishing spots"""
        return self.fishes.copy()
    
    def clear(self) -> None:
        """Clear all fishing spots"""
        self.fishes.clear() 