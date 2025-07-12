"""
Packet Capture for Albion Radar

Handles network packet capture and parsing.
"""

import asyncio
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from .photon_parser import PhotonParser
from ..config.settings import Settings


@dataclass
class PacketInfo:
    """Information about a captured packet"""
    timestamp: float
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    data: bytes
    size: int


class PacketCapture:
    """
    Handles network packet capture and parsing.
    
    Based on the original JavaScript packet parsing classes
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.parser = PhotonParser()
        self.is_capturing = False
        self.callbacks: Dict[str, List[Callable]] = {
            'packet': [],
            'player': [],
            'resource': [],
            'mob': [],
            'chest': [],
            'dungeon': [],
            'fish': [],
            'cage': []
        }
    
    async def start_capture(self) -> None:
        """Start packet capture"""
        if self.is_capturing:
            return
            
        self.is_capturing = True
        print("Starting packet capture...")
        
        try:
            # TODO: Implement actual packet capture
            # For now, simulate packet capture
            await self._simulate_capture()
        except Exception as e:
            print(f"Error starting packet capture: {e}")
            self.is_capturing = False
    
    async def stop_capture(self) -> None:
        """Stop packet capture"""
        self.is_capturing = False
        print("Stopping packet capture...")
    
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
    
    async def _simulate_capture(self) -> None:
        """Simulate packet capture for testing"""
        while self.is_capturing:
            # Simulate packet processing
            await asyncio.sleep(0.1)
            
            # TODO: Replace with actual packet capture
            # This is just for demonstration
            pass
    
    def process_packet(self, packet_data: bytes) -> None:
        """Process a captured packet"""
        try:
            # Parse the packet using PhotonParser
            parsed_data = self.parser.parse_packet(packet_data)
            
            if parsed_data:
                # Emit the parsed data
                self._emit_event('packet', parsed_data)
                
                # Process specific event types
                self._process_event_data(parsed_data)
                
        except Exception as e:
            print(f"Error processing packet: {e}")
    
    def _process_event_data(self, data: Dict) -> None:
        """Process specific event types"""
        event_code = data.get('code')
        
        if event_code == 1:  # Player event
            self._emit_event('player', data)
        elif event_code == 2:  # Resource event
            self._emit_event('resource', data)
        elif event_code == 3:  # Mob event
            self._emit_event('mob', data)
        elif event_code == 4:  # Chest event
            self._emit_event('chest', data)
        elif event_code == 5:  # Dungeon event
            self._emit_event('dungeon', data)
        elif event_code == 6:  # Fish event
            self._emit_event('fish', data)
        elif event_code == 7:  # Cage event
            self._emit_event('cage', data) 