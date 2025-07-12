"""
Example usage of Network Adapter Selector

This demonstrates how to use the network adapter selection functionality.
"""

import asyncio
from albion_radar import NetworkAdapterSelector, select_adapter_for_capture
from albion_radar.core.packet_capture import PacketCapture
from albion_radar.config.settings import Settings


def example_adapter_selection():
    """Example of network adapter selection"""
    
    print("=== Network Adapter Selection Example ===\n")
    
    # Create adapter selector
    selector = NetworkAdapterSelector()
    
    # List all available adapters
    adapters = selector.list_adapters()
    print(f"Found {len(adapters)} network adapters:")
    
    for i, adapter in enumerate(adapters, 1):
        print(f"  {i}. {adapter.name} - {adapter.ip_address}")
    
    print()
    
    # Try to load saved adapter
    saved_adapter = selector.load_saved_adapter()
    if saved_adapter:
        print(f"Loaded saved adapter: {saved_adapter.name} ({saved_adapter.ip_address})")
    else:
        print("No saved adapter found.")
    
    print()
    
    # Interactive selection
    print("Starting interactive selection...")
    selected = selector.select_adapter_interactive()
    
    if selected:
        print(f"Selected adapter: {selected.name} ({selected.ip_address})")
        
        # Validate the adapter
        if selector.validate_adapter(selected):
            print("✅ Adapter is suitable for packet capture")
        else:
            print("❌ Adapter may not be suitable for packet capture")
    else:
        print("No adapter selected.")
    
    return selected


def example_automatic_selection():
    """Example of automatic adapter selection"""
    
    print("=== Automatic Adapter Selection ===\n")
    
    # Use convenience function
    adapter = select_adapter_for_capture()
    
    if adapter:
        print(f"Automatically selected: {adapter.name} ({adapter.ip_address})")
        return adapter
    else:
        print("No suitable adapter found automatically.")
        return None


def example_with_packet_capture():
    """Example integrating adapter selection with packet capture"""
    
    print("=== Adapter Selection with Packet Capture ===\n")
    
    # Create settings
    settings = Settings()
    
    # Select adapter
    adapter = select_adapter_for_capture()
    
    if not adapter:
        print("No adapter selected. Cannot start packet capture.")
        return
    
    print(f"Using adapter: {adapter.name} ({adapter.ip_address})")
    
    # Create packet capture with selected adapter
    packet_capture = PacketCapture(settings)
    
    # Add callback for packet processing
    def on_packet_received(packet_data):
        print(f"Packet received from {adapter.name}: {len(packet_data)} bytes")
    
    packet_capture.add_callback('packet', on_packet_received)
    
    print("Packet capture configured with selected adapter.")
    print("Note: Actual packet capture requires additional setup.")
    
    return packet_capture


def example_adapter_validation():
    """Example of adapter validation"""
    
    print("=== Adapter Validation Example ===\n")
    
    selector = NetworkAdapterSelector()
    adapters = selector.list_adapters()
    
    print("Validating adapters for packet capture:")
    
    for adapter in adapters:
        is_valid = selector.validate_adapter(adapter)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        print(f"  {adapter.name} ({adapter.ip_address}): {status}")
    
    print()
    
    # Find best adapter
    best_adapter = selector.get_best_adapter()
    if best_adapter:
        print(f"Best adapter for packet capture: {best_adapter.name} ({best_adapter.ip_address})")
    else:
        print("No suitable adapter found for packet capture.")


async def main():
    """Main example function"""
    
    print("Albion Radar - Network Adapter Selection Examples")
    print("=" * 50)
    
    # Example 1: Manual adapter selection
    print("\n1. Manual Adapter Selection")
    example_adapter_selection()
    
    print("\n" + "-" * 30)
    
    # Example 2: Automatic selection
    print("\n2. Automatic Adapter Selection")
    example_automatic_selection()
    
    print("\n" + "-" * 30)
    
    # Example 3: Adapter validation
    print("\n3. Adapter Validation")
    example_adapter_validation()
    
    print("\n" + "-" * 30)
    
    # Example 4: Integration with packet capture
    print("\n4. Integration with Packet Capture")
    example_with_packet_capture()
    
    print("\n" + "=" * 50)
    print("Examples completed!")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 