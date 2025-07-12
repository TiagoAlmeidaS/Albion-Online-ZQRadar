"""
Mobs Handler for Albion Radar

Handles mob detection, tracking, and management.
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from ..models.mob import Mob
from ..config.settings import Settings


class EnemyType(Enum):
    """Enemy types"""
    ENEMY = 0
    BOSS = 1
    LIVING_SKINNABLE = 2
    LIVING_HARVESTABLE = 3
    DRONE = 4
    MIST_BOSS = 5
    EVENTS = 6


@dataclass
class Mist:
    """Represents a mist portal"""
    id: int
    pos_x: float
    pos_y: float
    name: str
    enchant: int
    type: int = 0
    h_x: float = 0.0
    h_y: float = 0.0


class MobsHandler:
    """
    Handles mob detection and management.
    
    Based on the original JavaScript MobsHandler.js
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.mob_list: List[Mob] = []
        self.mist_list: List[Mist] = []
        self.mob_info: Dict = {}
        self._last_update = time.time()
    
    def add_mob(self, mob_id: int, type_id: int, pos_x: float, pos_y: float,
                health: int = 0, enchantment_level: int = 0, rarity: str = "common") -> None:
        """Add a new mob"""
        
        # Check if mob already exists
        if self._find_mob(mob_id):
            return
        
        mob = Mob(
            id=mob_id,
            name=self._get_mob_name(type_id),
            level=enchantment_level,
            pos_x=pos_x,
            pos_y=pos_y,
            health=health,
            max_health=health
        )
        
        self.mob_list.append(mob)
    
    def add_mist(self, mist_id: int, pos_x: float, pos_y: float, name: str, enchant: int) -> None:
        """Add a new mist portal"""
        
        # Check if mist already exists
        if self._find_mist(mist_id):
            return
        
        mist = Mist(
            id=mist_id,
            pos_x=pos_x,
            pos_y=pos_y,
            name=name,
            enchant=enchant
        )
        
        self.mist_list.append(mist)
    
    def remove_mob(self, mob_id: int) -> None:
        """Remove a mob"""
        self.mob_list = [m for m in self.mob_list if m.id != mob_id]
    
    def remove_mist(self, mist_id: int) -> None:
        """Remove a mist portal"""
        self.mist_list = [m for m in self.mist_list if m.id != mist_id]
    
    def update_mob_position(self, mob_id: int, pos_x: float, pos_y: float) -> None:
        """Update mob position"""
        mob = self._find_mob(mob_id)
        if mob:
            mob.pos_x = pos_x
            mob.pos_y = pos_y
            mob.last_update = time.time()
    
    def update_mist_position(self, mist_id: int, pos_x: float, pos_y: float) -> None:
        """Update mist position"""
        mist = self._find_mist(mist_id)
        if mist:
            mist.pos_x = pos_x
            mist.pos_y = pos_y
    
    def update_mob_health(self, mob_id: int, health: int) -> None:
        """Update mob health"""
        mob = self._find_mob(mob_id)
        if mob:
            mob.health = health
            mob.last_update = time.time()
    
    def update_mist_enchantment(self, mist_id: int, enchant: int) -> None:
        """Update mist enchantment level"""
        mist = self._find_mist(mist_id)
        if mist:
            mist.enchant = enchant
    
    def handle_new_mob_event(self, parameters: Dict) -> None:
        """Handle new mob event"""
        try:
            mob_id = parameters.get(0)
            position = parameters.get(1, [0, 0])
            type_id = parameters.get(2, 0)
            health = parameters.get(3, 0)
            enchant = parameters.get(4, 0)
            rarity = parameters.get(5, "common")
            
            if not mob_id or not position:
                return
                
            pos_x, pos_y = position[0], position[1]
            
            self.add_mob(mob_id, type_id, pos_x, pos_y, health, enchant, rarity)
            
        except Exception as e:
            print(f"Error handling new mob event: {e}")
    
    def handle_mist_event(self, parameters: Dict) -> None:
        """Handle mist event"""
        try:
            mist_id = parameters.get(0)
            position = parameters.get(1, [0, 0])
            name = parameters.get(2, "")
            enchant = parameters.get(3, 0)
            mist_type = parameters.get(4, 0)
            
            if not mist_id or not position:
                return
                
            pos_x, pos_y = position[0], position[1]
            
            mist = Mist(
                id=mist_id,
                pos_x=pos_x,
                pos_y=pos_y,
                name=name,
                enchant=enchant,
                type=mist_type
            )
            
            # Remove existing mist with same ID
            self.remove_mist(mist_id)
            self.mist_list.append(mist)
            
        except Exception as e:
            print(f"Error handling mist event: {e}")
    
    def get_mob_list(self) -> List[Mob]:
        """Get all mobs"""
        return self.mob_list.copy()
    
    def get_mist_list(self) -> List[Mist]:
        """Get all mist portals"""
        return self.mist_list.copy()
    
    def update_mob_info(self, new_data: Dict) -> None:
        """Update mob information database"""
        self.mob_info.update(new_data)
    
    def clear(self) -> None:
        """Clear all mobs and mists"""
        self.mob_list.clear()
        self.mist_list.clear()
    
    def _find_mob(self, mob_id: int) -> Optional[Mob]:
        """Find a mob by ID"""
        for mob in self.mob_list:
            if mob.id == mob_id:
                return mob
        return None
    
    def _find_mist(self, mist_id: int) -> Optional[Mist]:
        """Find a mist by ID"""
        for mist in self.mist_list:
            if mist.id == mist_id:
                return mist
        return None
    
    def _get_mob_name(self, type_id: int) -> str:
        """Get mob name from type ID"""
        # TODO: Implement proper mob name lookup
        return f"Mob_{type_id}" 