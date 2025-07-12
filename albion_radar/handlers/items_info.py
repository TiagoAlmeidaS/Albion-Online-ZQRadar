"""
Items Info Handler for Albion Radar

Handles item information and lookup.
"""

import json
import os
from typing import Dict, Optional
from ..config.settings import Settings


class ItemsInfo:
    """
    Handles item information and lookup.
    
    Based on the original JavaScript ItemsInfo.js
    """
    
    def __init__(self):
        self.items: Dict[str, str] = {}
        self._load_items()
    
    def add_item(self, item_id: str, name: str, value: str) -> None:
        """Add item information"""
        self.items[item_id] = name
    
    def get_item_name(self, item_id: str) -> Optional[str]:
        """Get item name by ID"""
        return self.items.get(item_id)
    
    def _load_items(self) -> None:
        """Load items from file"""
        try:
            # TODO: Load from actual items.txt file
            # For now, create some sample items
            sample_items = {
                "T4_BAG": "Adept's Bag",
                "T5_BAG": "Expert's Bag",
                "T6_BAG": "Master's Bag",
                "T7_BAG": "Grandmaster's Bag",
                "T8_BAG": "Elder's Bag"
            }
            self.items.update(sample_items)
        except Exception as e:
            print(f"Error loading items: {e}")
    
    def get_all_items(self) -> Dict[str, str]:
        """Get all items"""
        return self.items.copy() 