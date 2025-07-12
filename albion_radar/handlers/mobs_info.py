"""
Mobs Info Handler for Albion Radar

Handles mob information and lookup.
"""

import json
import os
from typing import Dict, Optional
from ..config.settings import Settings


class MobsInfo:
    """
    Handles mob information and lookup.
    
    Based on the original JavaScript MobsInfo.js
    """
    
    def __init__(self):
        self.mobs: Dict[str, Dict] = {}
        self._load_mobs()
    
    def add_mob(self, mob_id: str, tier: int, mob_type: str, location: str) -> None:
        """Add mob information"""
        self.mobs[mob_id] = {
            'tier': tier,
            'type': mob_type,
            'location': location
        }
    
    def get_mob_info(self, mob_id: str) -> Optional[Dict]:
        """Get mob information by ID"""
        return self.mobs.get(mob_id)
    
    def _load_mobs(self) -> None:
        """Load mobs from file"""
        try:
            # TODO: Load from actual mobs data file
            # For now, create some sample mobs
            sample_mobs = {
                "Mob_1": {'tier': 1, 'type': 'Enemy', 'location': 'Forest'},
                "Mob_2": {'tier': 2, 'type': 'Boss', 'location': 'Dungeon'},
                "Mob_3": {'tier': 3, 'type': 'Living', 'location': 'Mountain'}
            }
            self.mobs.update(sample_mobs)
        except Exception as e:
            print(f"Error loading mobs: {e}")
    
    def get_all_mobs(self) -> Dict[str, Dict]:
        """Get all mobs"""
        return self.mobs.copy() 