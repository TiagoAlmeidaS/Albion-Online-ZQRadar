"""
Data Manager for Albion Radar

Manages data flow and coordination between handlers.
"""

import asyncio
import time
from typing import Dict, List, Optional, Callable
from ..handlers.players_handler import PlayersHandler
from ..handlers.harvestables_handler import HarvestablesHandler
from ..handlers.mobs_handler import MobsHandler
from ..handlers.chests_handler import ChestsHandler
from ..handlers.dungeons_handler import DungeonsHandler
from ..handlers.fishing_handler import FishingHandler
from ..handlers.wisp_cage_handler import WispCageHandler
from ..handlers.items_info import ItemsInfo
from ..handlers.mobs_info import MobsInfo
from ..config.settings import Settings


class DataManager:
    """
    Manages data flow and coordination between handlers.
    
    Acts as a central coordinator for all radar data processing.
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        
        # Initialize handlers
        self.players_handler = PlayersHandler(settings)
        self.harvestables_handler = HarvestablesHandler(settings)
        self.mobs_handler = MobsHandler(settings)
        self.chests_handler = ChestsHandler(settings)
        self.dungeons_handler = DungeonsHandler(settings)
        self.fishing_handler = FishingHandler(settings)
        self.wisp_cage_handler = WispCageHandler(settings)
        self.items_info = ItemsInfo()
        self.mobs_info = MobsInfo()
        
        # Event callbacks
        self.callbacks: Dict[str, List[Callable]] = {
            'player_detected': [],
            'resource_detected': [],
            'mob_detected': [],
            'chest_detected': [],
            'dungeon_detected': [],
            'fish_detected': [],
            'cage_detected': [],
            'data_updated': []
        }
        
        self._last_update = time.time()
    
    def add_callback(self, event_type: str, callback: Callable) -> None:
        """Add event callback"""
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
    
    def remove_callback(self, event_type: str, callback: Callable) -> None:
        """Remove event callback"""
        if event_type in self.callbacks:
            try:
                self.callbacks[event_type].remove(callback)
            except ValueError:
                pass
    
    def _emit_event(self, event_type: str, data: Dict) -> None:
        """Emit event to all callbacks"""
        if event_type in self.callbacks:
            for callback in self.callbacks[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in callback for {event_type}: {e}")
    
    def process_packet_data(self, packet_data: Dict) -> None:
        """Process packet data and route to appropriate handlers"""
        try:
            event_type = packet_data.get('type')
            event_code = packet_data.get('code', 0)
            parameters = packet_data.get('parameters', {})
            
            if event_type == 'event':
                self._process_event(event_code, parameters)
            elif event_type == 'request':
                self._process_request(event_code, parameters)
            elif event_type == 'response':
                self._process_response(event_code, parameters)
                
        except Exception as e:
            print(f"Error processing packet data: {e}")
    
    def _process_event(self, event_code: int, parameters: Dict) -> None:
        """Process event data"""
        try:
            if event_code == 1:  # Player event
                self.players_handler.handle_new_player_event(parameters)
                self._emit_event('player_detected', parameters)
                
            elif event_code == 2:  # Resource event
                self.harvestables_handler.handle_new_harvestable_object(
                    parameters.get(0, 0), parameters
                )
                self._emit_event('resource_detected', parameters)
                
            elif event_code == 3:  # Mob event
                self.mobs_handler.handle_new_mob_event(parameters)
                self._emit_event('mob_detected', parameters)
                
            elif event_code == 4:  # Chest event
                self.chests_handler.handle_chest_event(parameters)
                self._emit_event('chest_detected', parameters)
                
            elif event_code == 5:  # Dungeon event
                self.dungeons_handler.handle_dungeon_event(parameters)
                self._emit_event('dungeon_detected', parameters)
                
            elif event_code == 6:  # Fish event
                self.fishing_handler.handle_new_fish_event(parameters)
                self._emit_event('fish_detected', parameters)
                
            elif event_code == 7:  # Cage event
                self.wisp_cage_handler.handle_new_cage_event(parameters)
                self._emit_event('cage_detected', parameters)
            
            # Emit general data update
            self._emit_event('data_updated', {
                'timestamp': time.time(),
                'event_code': event_code
            })
            
        except Exception as e:
            print(f"Error processing event {event_code}: {e}")
    
    def _process_request(self, operation_code: int, parameters: Dict) -> None:
        """Process operation request"""
        # TODO: Implement request processing
        pass
    
    def _process_response(self, operation_code: int, parameters: Dict) -> None:
        """Process operation response"""
        # TODO: Implement response processing
        pass
    
    def get_all_data(self) -> Dict:
        """Get all current radar data"""
        return {
            'players': self.players_handler.get_players_in_range(),
            'resources': self.harvestables_handler.get_harvestable_list(),
            'mobs': self.mobs_handler.get_mob_list(),
            'mists': self.mobs_handler.get_mist_list(),
            'chests': self.chests_handler.get_chests_list(),
            'dungeons': self.dungeons_handler.get_dungeon_list(),
            'fishes': self.fishing_handler.get_fishes_list(),
            'cages': self.wisp_cage_handler.get_cages_list(),
            'timestamp': time.time()
        }
    
    def clear_all_data(self) -> None:
        """Clear all data from all handlers"""
        self.players_handler.clear()
        self.harvestables_handler.clear()
        self.mobs_handler.clear()
        self.chests_handler.clear()
        self.dungeons_handler.clear()
        self.fishing_handler.clear()
        self.wisp_cage_handler.clear()
    
    def update_local_player_position(self, pos_x: float, pos_y: float) -> None:
        """Update local player position"""
        self.players_handler.update_local_player_position(pos_x, pos_y)
    
    def get_players_in_range(self, max_distance: float = 80.0) -> List:
        """Get players in range"""
        return self.players_handler.get_players_in_range(max_distance)
    
    def get_resources_in_range(self, local_pos_x: float, local_pos_y: float, 
                              max_distance: float = 80.0) -> List:
        """Get resources in range"""
        self.harvestables_handler.remove_not_in_range(local_pos_x, local_pos_y, max_distance)
        return self.harvestables_handler.get_harvestable_list() 