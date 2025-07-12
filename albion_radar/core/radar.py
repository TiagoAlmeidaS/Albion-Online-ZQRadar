"""
Main AlbionRadar class that orchestrates packet capture, parsing, and event handling.
"""

import asyncio
import threading
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass
from enum import Enum

from .packet_capture import PacketCapture
from .photon_parser import PhotonParser
from .data_manager import DataManager
from ..handlers.players_handler import PlayersHandler
from ..handlers.harvestables_handler import HarvestablesHandler
from ..handlers.mobs_handler import MobsHandler
from ..handlers.chests_handler import ChestsHandler
from ..handlers.dungeons_handler import DungeonsHandler
from ..config.settings import Settings
from ..config.event_codes import EventCodes

class ObjectType(Enum):
    """Types of objects that can be detected"""
    PLAYER = "player"
    RESOURCE = "resource"
    MOB = "mob"
    CHEST = "chest"
    DUNGEON = "dungeon"

@dataclass
class RadarEvent:
    """Represents a radar event"""
    event_type: ObjectType
    object_id: int
    data: Dict
    timestamp: float

class AlbionRadar:
    """
    Main class for Albion Radar functionality.
    
    This class provides a high-level interface for capturing and processing
    Albion Online network data.
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize AlbionRadar.
        
        Args:
            settings: Optional settings object. If None, default settings will be used.
        """
        self.settings = settings or Settings()
        self.data_manager = DataManager()
        
        # Core components
        self.packet_capture = PacketCapture()
        self.photon_parser = PhotonParser()
        
        # Handlers
        self.players_handler = PlayersHandler(self.settings)
        self.harvestables_handler = HarvestablesHandler(self.settings)
        self.mobs_handler = MobsHandler(self.settings)
        self.chests_handler = ChestsHandler(self.settings)
        self.dungeons_handler = DungeonsHandler(self.settings)
        
        # Event callbacks
        self._callbacks: Dict[ObjectType, List[Callable]] = {
            ObjectType.PLAYER: [],
            ObjectType.RESOURCE: [],
            ObjectType.MOB: [],
            ObjectType.CHEST: [],
            ObjectType.DUNGEON: []
        }
        
        # State
        self._running = False
        self._lock = threading.Lock()
        
        # Setup event handlers
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Setup internal event handlers"""
        # Players
        self.players_handler.on_player_added(self._on_player_detected)
        self.players_handler.on_player_removed(self._on_player_removed)
        
        # Resources
        self.harvestables_handler.on_resource_added(self._on_resource_detected)
        self.harvestables_handler.on_resource_removed(self._on_resource_removed)
        
        # Mobs
        self.mobs_handler.on_mob_added(self._on_mob_detected)
        self.mobs_handler.on_mob_removed(self._on_mob_removed)
        
        # Chests
        self.chests_handler.on_chest_added(self._on_chest_detected)
        self.chests_handler.on_chest_removed(self._on_chest_removed)
        
        # Dungeons
        self.dungeons_handler.on_dungeon_added(self._on_dungeon_detected)
        self.dungeons_handler.on_dungeon_removed(self._on_dungeon_removed)
    
    async def start(self):
        """
        Start the radar system.
        
        This will begin packet capture and processing.
        """
        if self._running:
            print("Radar already running!")
            return
        
        self._running = True
        print("Starting Albion Radar...")
        
        try:
            # Start packet capture
            await self.packet_capture.start(self._on_packet_received)
            print("Albion Radar started successfully!")
            
        except Exception as e:
            self._running = False
            print(f"Failed to start radar: {e}")
            raise
    
    async def stop(self):
        """
        Stop the radar system.
        """
        if not self._running:
            return
        
        print("Stopping Albion Radar...")
        self._running = False
        
        try:
            await self.packet_capture.stop()
            print("Albion Radar stopped successfully!")
        except Exception as e:
            print(f"Error stopping radar: {e}")
    
    async def _on_packet_received(self, payload: bytes):
        """
        Handle received packet data.
        
        Args:
            payload: Raw packet data
        """
        if not self._running:
            return
        
        try:
            # Parse the packet
            parsed_data = self.photon_parser.parse(payload)
            
            # Process the parsed data
            await self._process_parsed_data(parsed_data)
            
        except Exception as e:
            print(f"Error processing packet: {e}")
    
    async def _process_parsed_data(self, data: Dict):
        """
        Process parsed packet data.
        
        Args:
            data: Parsed packet data
        """
        event_code = data.get("event_code")
        
        if event_code == EventCodes.NewCharacter:
            await self._handle_new_player(data)
        elif event_code == EventCodes.NewSimpleHarvestableObjectList:
            await self._handle_new_resource(data)
        elif event_code == EventCodes.NewMob:
            await self._handle_new_mob(data)
        elif event_code == EventCodes.NewLootChest:
            await self._handle_new_chest(data)
        elif event_code == EventCodes.NewRandomDungeonExit:
            await self._handle_new_dungeon(data)
        elif event_code == EventCodes.Leave:
            await self._handle_object_leave(data)
    
    async def _handle_new_player(self, data: Dict):
        """Handle new player event"""
        try:
            await self.players_handler.handle_new_player(data)
        except Exception as e:
            print(f"Error handling new player: {e}")
    
    async def _handle_new_resource(self, data: Dict):
        """Handle new resource event"""
        try:
            await self.harvestables_handler.handle_new_resource(data)
        except Exception as e:
            print(f"Error handling new resource: {e}")
    
    async def _handle_new_mob(self, data: Dict):
        """Handle new mob event"""
        try:
            await self.mobs_handler.handle_new_mob(data)
        except Exception as e:
            print(f"Error handling new mob: {e}")
    
    async def _handle_new_chest(self, data: Dict):
        """Handle new chest event"""
        try:
            await self.chests_handler.handle_new_chest(data)
        except Exception as e:
            print(f"Error handling new chest: {e}")
    
    async def _handle_new_dungeon(self, data: Dict):
        """Handle new dungeon event"""
        try:
            await self.dungeons_handler.handle_new_dungeon(data)
        except Exception as e:
            print(f"Error handling new dungeon: {e}")
    
    async def _handle_object_leave(self, data: Dict):
        """Handle object leave event"""
        object_id = data.get("object_id")
        if object_id:
            self.players_handler.remove_player(object_id)
            self.harvestables_handler.remove_resource(object_id)
            self.mobs_handler.remove_mob(object_id)
            self.chests_handler.remove_chest(object_id)
            self.dungeons_handler.remove_dungeon(object_id)
    
    # Event callback registration methods
    def on_player_detected(self, callback: Callable):
        """Register callback for player detection"""
        self._callbacks[ObjectType.PLAYER].append(callback)
    
    def on_resource_detected(self, callback: Callable):
        """Register callback for resource detection"""
        self._callbacks[ObjectType.RESOURCE].append(callback)
    
    def on_mob_detected(self, callback: Callable):
        """Register callback for mob detection"""
        self._callbacks[ObjectType.MOB].append(callback)
    
    def on_chest_detected(self, callback: Callable):
        """Register callback for chest detection"""
        self._callbacks[ObjectType.CHEST].append(callback)
    
    def on_dungeon_detected(self, callback: Callable):
        """Register callback for dungeon detection"""
        self._callbacks[ObjectType.DUNGEON].append(callback)
    
    # Internal event handlers
    def _on_player_detected(self, player):
        """Internal player detection handler"""
        for callback in self._callbacks[ObjectType.PLAYER]:
            try:
                callback(player)
            except Exception as e:
                print(f"Error in player callback: {e}")
    
    def _on_player_removed(self, player_id: int):
        """Internal player removal handler"""
        # Handle player removal if needed
        pass
    
    def _on_resource_detected(self, resource):
        """Internal resource detection handler"""
        for callback in self._callbacks[ObjectType.RESOURCE]:
            try:
                callback(resource)
            except Exception as e:
                print(f"Error in resource callback: {e}")
    
    def _on_resource_removed(self, resource_id: int):
        """Internal resource removal handler"""
        pass
    
    def _on_mob_detected(self, mob):
        """Internal mob detection handler"""
        for callback in self._callbacks[ObjectType.MOB]:
            try:
                callback(mob)
            except Exception as e:
                print(f"Error in mob callback: {e}")
    
    def _on_mob_removed(self, mob_id: int):
        """Internal mob removal handler"""
        pass
    
    def _on_chest_detected(self, chest):
        """Internal chest detection handler"""
        for callback in self._callbacks[ObjectType.CHEST]:
            try:
                callback(chest)
            except Exception as e:
                print(f"Error in chest callback: {e}")
    
    def _on_chest_removed(self, chest_id: int):
        """Internal chest removal handler"""
        pass
    
    def _on_dungeon_detected(self, dungeon):
        """Internal dungeon detection handler"""
        for callback in self._callbacks[ObjectType.DUNGEON]:
            try:
                callback(dungeon)
            except Exception as e:
                print(f"Error in dungeon callback: {e}")
    
    def _on_dungeon_removed(self, dungeon_id: int):
        """Internal dungeon removal handler"""
        pass
    
    # Data access methods
    def get_players(self) -> List:
        """Get all detected players"""
        return self.players_handler.get_players()
    
    def get_resources(self) -> List:
        """Get all detected resources"""
        return self.harvestables_handler.get_resources()
    
    def get_mobs(self) -> List:
        """Get all detected mobs"""
        return self.mobs_handler.get_mobs()
    
    def get_chests(self) -> List:
        """Get all detected chests"""
        return self.chests_handler.get_chests()
    
    def get_dungeons(self) -> List:
        """Get all detected dungeons"""
        return self.dungeons_handler.get_dungeons()
    
    def get_objects_in_range(self, center_x: float, center_y: float, radius: float) -> Dict[ObjectType, List]:
        """Get all objects within a specific radius"""
        objects = {
            ObjectType.PLAYER: [],
            ObjectType.RESOURCE: [],
            ObjectType.MOB: [],
            ObjectType.CHEST: [],
            ObjectType.DUNGEON: []
        }
        
        # Check players
        for player in self.get_players():
            distance = ((player.pos_x - center_x) ** 2 + (player.pos_y - center_y) ** 2) ** 0.5
            if distance <= radius:
                objects[ObjectType.PLAYER].append(player)
        
        # Check resources
        for resource in self.get_resources():
            distance = ((resource.pos_x - center_x) ** 2 + (resource.pos_y - center_y) ** 2) ** 0.5
            if distance <= radius:
                objects[ObjectType.RESOURCE].append(resource)
        
        # Check mobs
        for mob in self.get_mobs():
            distance = ((mob.pos_x - center_x) ** 2 + (mob.pos_y - center_y) ** 2) ** 0.5
            if distance <= radius:
                objects[ObjectType.MOB].append(mob)
        
        # Check chests
        for chest in self.get_chests():
            distance = ((chest.pos_x - center_x) ** 2 + (chest.pos_y - center_y) ** 2) ** 0.5
            if distance <= radius:
                objects[ObjectType.CHEST].append(chest)
        
        # Check dungeons
        for dungeon in self.get_dungeons():
            distance = ((dungeon.pos_x - center_x) ** 2 + (dungeon.pos_y - center_y) ** 2) ** 0.5
            if distance <= radius:
                objects[ObjectType.DUNGEON].append(dungeon)
        
        return objects
    
    def is_running(self) -> bool:
        """Check if radar is running"""
        return self._running
    
    def clear_data(self):
        """Clear all stored data"""
        self.players_handler.clear()
        self.harvestables_handler.clear()
        self.mobs_handler.clear()
        self.chests_handler.clear()
        self.dungeons_handler.clear() 