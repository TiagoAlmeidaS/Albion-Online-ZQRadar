"""
Network Adapter Selector for Albion Radar

Handles network adapter detection and selection for packet capture.
"""

import socket
import netifaces
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class NetworkAdapter:
    """Represents a network adapter"""
    name: str
    ip_address: str
    interface_name: str
    is_active: bool = True


class NetworkAdapterSelector:
    """
    Handles network adapter detection and selection.
    
    Based on the original JavaScript adapter-selector.js
    """
    
    def __init__(self):
        self.adapters: List[NetworkAdapter] = []
        self.selected_adapter: Optional[NetworkAdapter] = None
        self._load_adapters()
    
    def _load_adapters(self) -> None:
        """Load available network adapters"""
        try:
            # Get all network interfaces
            interfaces = netifaces.interfaces()
            
            for interface_name in interfaces:
                try:
                    # Get interface addresses
                    addrs = netifaces.ifaddresses(interface_name)
                    
                    # Look for IPv4 addresses
                    if netifaces.AF_INET in addrs:
                        for addr_info in addrs[netifaces.AF_INET]:
                            ip_address = addr_info['addr']
                            
                            # Skip loopback and internal addresses
                            if not ip_address.startswith('127.') and not ip_address.startswith('169.254.'):
                                adapter = NetworkAdapter(
                                    name=interface_name,
                                    ip_address=ip_address,
                                    interface_name=interface_name
                                )
                                self.adapters.append(adapter)
                                
                except Exception as e:
                    print(f"Error loading adapter {interface_name}: {e}")
                    continue
                    
        except ImportError:
            print("netifaces module not available. Using fallback method.")
            self._load_adapters_fallback()
        except Exception as e:
            print(f"Error loading network adapters: {e}")
    
    def _load_adapters_fallback(self) -> None:
        """Fallback method using socket module"""
        try:
            # Get hostname to find local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            adapter = NetworkAdapter(
                name="Default Interface",
                ip_address=local_ip,
                interface_name="default"
            )
            self.adapters.append(adapter)
            
        except Exception as e:
            print(f"Error in fallback adapter loading: {e}")
    
    def list_adapters(self) -> List[NetworkAdapter]:
        """Get list of available adapters"""
        return self.adapters.copy()
    
    def select_adapter_interactive(self) -> Optional[NetworkAdapter]:
        """Interactive adapter selection"""
        if not self.adapters:
            print("No network adapters found!")
            return None
        
        print("\nAvailable network adapters:")
        print("Please select the adapter you use to connect to the internet:")
        
        for i, adapter in enumerate(self.adapters, 1):
            print(f"  {i}. {adapter.name}\t IP: {adapter.ip_address}")
        
        while True:
            try:
                print()
                user_input = input("Enter the number here: ").strip()
                selection = int(user_input)
                
                if 1 <= selection <= len(self.adapters):
                    selected = self.adapters[selection - 1]
                    self.selected_adapter = selected
                    
                    print(f"\nYou have selected: {selected.name} - {selected.ip_address}")
                    self._save_selected_adapter(selected)
                    
                    return selected
                else:
                    print("Invalid selection. Please try again.")
                    
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nSelection cancelled.")
                return None
    
    def select_adapter_by_ip(self, ip_address: str) -> Optional[NetworkAdapter]:
        """Select adapter by IP address"""
        for adapter in self.adapters:
            if adapter.ip_address == ip_address:
                self.selected_adapter = adapter
                return adapter
        return None
    
    def select_adapter_by_name(self, interface_name: str) -> Optional[NetworkAdapter]:
        """Select adapter by interface name"""
        for adapter in self.adapters:
            if adapter.interface_name == interface_name:
                self.selected_adapter = adapter
                return adapter
        return None
    
    def get_selected_adapter(self) -> Optional[NetworkAdapter]:
        """Get currently selected adapter"""
        return self.selected_adapter
    
    def _save_selected_adapter(self, adapter: NetworkAdapter) -> None:
        """Save selected adapter to file"""
        try:
            with open('ip.txt', 'w') as f:
                f.write(adapter.ip_address)
            print("Selected IP saved to ip.txt")
        except Exception as e:
            print(f"Error saving IP: {e}")
    
    def load_saved_adapter(self) -> Optional[NetworkAdapter]:
        """Load previously saved adapter"""
        try:
            if os.path.exists('ip.txt'):
                with open('ip.txt', 'r') as f:
                    saved_ip = f.read().strip()
                
                return self.select_adapter_by_ip(saved_ip)
        except Exception as e:
            print(f"Error loading saved adapter: {e}")
        
        return None
    
    def get_adapter_info(self, adapter: NetworkAdapter) -> Dict:
        """Get detailed information about an adapter"""
        return {
            'name': adapter.name,
            'ip_address': adapter.ip_address,
            'interface_name': adapter.interface_name,
            'is_active': adapter.is_active
        }
    
    def validate_adapter(self, adapter: NetworkAdapter) -> bool:
        """Validate if adapter is suitable for packet capture"""
        try:
            # Test if we can bind to the interface
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            test_socket.bind((adapter.ip_address, 0))
            test_socket.close()
            return True
        except Exception:
            return False
    
    def get_best_adapter(self) -> Optional[NetworkAdapter]:
        """Automatically select the best adapter for packet capture"""
        # Try to load saved adapter first
        saved = self.load_saved_adapter()
        if saved and self.validate_adapter(saved):
            return saved
        
        # Try to find a suitable adapter
        for adapter in self.adapters:
            if self.validate_adapter(adapter):
                return adapter
        
        return None


def create_adapter_selector() -> NetworkAdapterSelector:
    """Factory function to create adapter selector"""
    return NetworkAdapterSelector()


def select_adapter_for_capture() -> Optional[NetworkAdapter]:
    """Convenience function to select adapter for packet capture"""
    selector = create_adapter_selector()
    
    # Try to load saved adapter
    adapter = selector.load_saved_adapter()
    if adapter:
        print(f"Using saved adapter: {adapter.name} ({adapter.ip_address})")
        return adapter
    
    # Interactive selection
    return selector.select_adapter_interactive() 