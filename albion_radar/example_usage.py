"""
Example usage of Albion Radar module

This demonstrates how to use the albion_radar module in your own projects.
"""

import asyncio
import time
from albion_radar import AlbionRadar
from albion_radar.config.settings import Settings


async def main():
    """Example usage of AlbionRadar"""
    
    # Create settings
    settings = Settings()
    
    # Create radar instance
    radar = AlbionRadar(settings)
    
    # Add event callbacks
    def on_player_detected(player_data):
        print(f"Player detected: {player_data}")
    
    def on_resource_detected(resource_data):
        print(f"Resource detected: {resource_data}")
    
    def on_mob_detected(mob_data):
        print(f"Mob detected: {mob_data}")
    
    radar.on_player_detected(on_player_detected)
    radar.on_resource_detected(on_resource_detected)
    radar.on_mob_detected(on_mob_detected)
    
    # Start the radar
    print("Starting Albion Radar...")
    await radar.start()
    
    try:
        # Keep running for a while
        print("Radar is running. Press Ctrl+C to stop.")
        await asyncio.sleep(30)  # Run for 30 seconds
        
    except KeyboardInterrupt:
        print("\nStopping radar...")
    
    finally:
        # Stop the radar
        await radar.stop()
        print("Radar stopped.")


def example_integration():
    """Example of integrating radar into another project"""
    
    # Create settings
    settings = Settings()
    
    # Create radar instance
    radar = AlbionRadar(settings)
    
    # Custom callback for your project
    def my_custom_handler(data):
        """Your custom data processing"""
        # Process the radar data for your specific needs
        players = data.get('players', [])
        resources = data.get('resources', [])
        
        # Do something with the data
        print(f"Found {len(players)} players and {len(resources)} resources")
        
        # Example: Save to database, send to API, etc.
        # save_to_database(data)
        # send_to_api(data)
    
    # Register your custom handler
    # radar.add_callback('data_updated', my_custom_handler)  # TODO: Implement this method
    
    return radar


if __name__ == "__main__":
    # Run the example
    asyncio.run(main()) 