"""
Harvestables Handler for Albion Radar

Handles resource detection, tracking, and management.
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from ..models.resource import Resource, ResourceType, ResourceEnchant
from ..config.settings import Settings


class HarvestableType(Enum):
    """Harvestable resource types"""
    FIBER = 'Fiber'
    HIDE = 'Hide'
    LOG = 'Log'
    ORE = 'Ore'
    ROCK = 'Rock'


@dataclass
class Harvestable:
    """Represents a harvestable resource"""
    id: int
    type: int
    tier: int
    pos_x: float
    pos_y: float
    charges: int = 0
    size: int = 0
    h_x: float = 0.0
    h_y: float = 0.0
    
    def set_charges(self, charges: int) -> None:
        """Update resource charges"""
        self.charges = charges


class HarvestablesHandler:
    """
    Handles harvestable resource detection and management.
    
    Based on the original JavaScript HarvestablesHandler.js
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.harvestable_list: List[Harvestable] = []
        self._last_update = time.time()
    
    def add_harvestable(self, resource_id: int, resource_type: int, tier: int,
                        pos_x: float, pos_y: float, charges: int = 0, size: int = 0) -> None:
        """Add a new harvestable resource"""
        
        # Check if this resource type should be shown based on settings
        if not self._should_show_resource(resource_type, charges, tier):
            return
        
        # Check if resource already exists
        existing = self._find_harvestable(resource_id)
        if existing:
            existing.set_charges(charges)
            return
        
        # Create new harvestable
        harvestable = Harvestable(
            id=resource_id,
            type=resource_type,
            tier=tier,
            pos_x=pos_x,
            pos_y=pos_y,
            charges=charges,
            size=size
        )
        
        self.harvestable_list.append(harvestable)
    
    def update_harvestable(self, resource_id: int, resource_type: int, tier: int,
                          pos_x: float, pos_y: float, charges: int = 0, size: int = 0) -> None:
        """Update an existing harvestable resource"""
        
        # Check if this resource type should be shown based on settings
        if not self._should_show_resource(resource_type, charges, tier):
            return
        
        existing = self._find_harvestable(resource_id)
        if existing:
            existing.charges = charges
            existing.size = size
        else:
            self.add_harvestable(resource_id, resource_type, tier, pos_x, pos_y, charges, size)
    
    def remove_harvestable(self, resource_id: int) -> None:
        """Remove a harvestable resource"""
        self.harvestable_list = [h for h in self.harvestable_list if h.id != resource_id]
    
    def remove_not_in_range(self, local_pos_x: float, local_pos_y: float, max_distance: float = 80.0) -> None:
        """Remove resources that are too far from local player"""
        self.harvestable_list = [
            h for h in self.harvestable_list 
            if self._calculate_distance(local_pos_x, local_pos_y, h.pos_x, h.pos_y) <= max_distance
            and h.size is not None
        ]
    
    def update_harvestable_size(self, resource_id: int, new_size: int) -> None:
        """Update resource size after harvesting"""
        harvestable = self._find_harvestable(resource_id)
        if harvestable:
            harvestable.size = new_size
    
    def harvest_finished(self, resource_id: int, count: int) -> None:
        """Handle harvest completion"""
        harvestable = self._find_harvestable(resource_id)
        if harvestable:
            harvestable.size = max(0, harvestable.size - count)
    
    def handle_new_harvestable_object(self, resource_id: int, parameters: Dict) -> None:
        """Handle new harvestable object event"""
        try:
            resource_type = parameters.get(5)
            tier = parameters.get(7)
            location = parameters.get(8, [0, 0])
            enchant = parameters.get(11, 0)
            size = parameters.get(10, 0)
            
            if not location:
                return
                
            pos_x, pos_y = location[0], location[1]
            
            if resource_type is not None and tier is not None:
                self.update_harvestable(
                    resource_id, resource_type, tier, pos_x, pos_y, enchant, size
                )
            
        except Exception as e:
            print(f"Error handling new harvestable object: {e}")
    
    def handle_simple_harvestable_object(self, parameters: Dict) -> None:
        """Handle simple harvestable object event"""
        try:
            data_0 = parameters.get(0, {}).get('data', parameters.get(0, []))
            data_1 = parameters.get(1, {}).get('data', [])
            data_2 = parameters.get(2, {}).get('data', [])
            data_3 = parameters.get(3, [])
            data_4 = parameters.get(4, {}).get('data', [])
            
            if not data_0:
                return
            
            for i in range(len(data_0)):
                resource_id = data_0[i]
                resource_type = data_1[i] if i < len(data_1) else 0
                tier = data_2[i] if i < len(data_2) else 1
                pos_x = data_3[i * 2] if i * 2 < len(data_3) else 0
                pos_y = data_3[i * 2 + 1] if i * 2 + 1 < len(data_3) else 0
                count = data_4[i] if i < len(data_4) else 0
                
                self.add_harvestable(resource_id, resource_type, tier, pos_x, pos_y, 0, count)
                
        except Exception as e:
            print(f"Error handling simple harvestable object: {e}")
    
    def get_harvestable_list(self) -> List[Harvestable]:
        """Get all harvestable resources"""
        return self.harvestable_list.copy()
    
    def clear(self) -> None:
        """Clear all harvestable resources"""
        self.harvestable_list.clear()
    
    def _find_harvestable(self, resource_id: int) -> Optional[Harvestable]:
        """Find a harvestable by ID"""
        for harvestable in self.harvestable_list:
            if harvestable.id == resource_id:
                return harvestable
        return None
    
    def _should_show_resource(self, resource_type: int, charges: int, tier: int) -> bool:
        """Check if resource should be shown based on settings"""
        resource_type_str = self._get_string_type(resource_type)
        
        # TODO: Implement proper settings checking
        # For now, show all resources
        return True
    
    def _get_string_type(self, type_number: int) -> str:
        """Convert type number to string type"""
        if 0 <= type_number <= 5:
            return HarvestableType.LOG.value
        elif 6 <= type_number <= 10:
            return HarvestableType.ROCK.value
        elif 11 <= type_number <= 15:
            return HarvestableType.FIBER.value
        elif 16 <= type_number <= 22:
            return HarvestableType.HIDE.value
        elif 23 <= type_number <= 27:
            return HarvestableType.ORE.value
        else:
            return ''
    
    def _calculate_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate distance between two points"""
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 