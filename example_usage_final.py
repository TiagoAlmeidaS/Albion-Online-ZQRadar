#!/usr/bin/env python3
"""
Example usage of the Albion Radar Python module.

This demonstrates how to use the radar module programmatically
and integrate it with the web interface.
"""

import asyncio
import logging
from albion_radar.core.radar import Radar
from albion_radar.core.network_adapter import NetworkAdapterSelector
from albion_radar.web_interface import app, socketio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlbionRadarExample:
    """Example implementation of Albion Radar."""
    
    def __init__(self):
        """Initialize the radar example."""
        self.radar = None
        self.network_adapter = NetworkAdapterSelector()
        self.is_running = False
        
    def setup_radar(self):
        """Setup the radar with default configuration."""
        try:
            # Initialize radar
            self.radar = Radar()
            
            # List available network adapters
            adapters = self.network_adapter.list_adapters()
            logger.info(f"Available network adapters: {adapters}")
            
            # Auto-select the first available adapter
            if adapters:
                selected = self.network_adapter.select_adapter(adapters[0])
                logger.info(f"Selected adapter: {selected}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up radar: {e}")
            return False
    
    def start_radar(self):
        """Start the radar capture."""
        if not self.radar:
            logger.error("Radar not initialized")
            return False
        
        try:
            self.is_running = True
            self.radar.start()
            logger.info("Radar started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting radar: {e}")
            return False
    
    def stop_radar(self):
        """Stop the radar capture."""
        if self.radar:
            self.is_running = False
            self.radar.stop()
            logger.info("Radar stopped")
    
    def get_radar_data(self):
        """Get current radar data."""
        if not self.radar:
            return {}
        
        try:
            return {
                'players': self.radar.get_players(),
                'mobs': self.radar.get_mobs(),
                'resources': self.radar.get_resources(),
                'chests': self.radar.get_chests(),
                'dungeons': self.radar.get_dungeons(),
                'fishing_spots': self.radar.get_fishing_spots(),
                'wisp_cages': self.radar.get_wisp_cages()
            }
        except Exception as e:
            logger.error(f"Error getting radar data: {e}")
            return {}

def run_web_interface():
    """Run the web interface."""
    print("🚀 Starting Albion Radar Web Interface...")
    print("📡 Web interface will be available at: http://localhost:5000")
    print("🎮 Radar data will be available at: http://localhost:5000/api/radar-data")
    print("⚙️  Settings can be configured at: http://localhost:5000/settings")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    # Run the Flask app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

def run_radar_example():
    """Run the radar example."""
    print("🎯 Albion Radar Python Example")
    print("=" * 40)
    
    # Create radar instance
    radar_example = AlbionRadarExample()
    
    # Setup radar
    if not radar_example.setup_radar():
        print("❌ Failed to setup radar")
        return
    
    print("✅ Radar setup complete")
    
    # Start radar
    if not radar_example.start_radar():
        print("❌ Failed to start radar")
        return
    
    print("✅ Radar started")
    
    try:
        # Run for a few seconds to demonstrate
        import time
        for i in range(10):
            data = radar_example.get_radar_data()
            print(f"📊 Data update {i+1}: {len(data.get('players', []))} players detected")
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n⏹️  Stopping radar...")
    
    finally:
        radar_example.stop_radar()
        print("✅ Radar stopped")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        # Run web interface
        run_web_interface()
    else:
        # Run radar example
        run_radar_example() 