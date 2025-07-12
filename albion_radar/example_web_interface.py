#!/usr/bin/env python3
"""
Example script demonstrating how to use the Albion Radar Web Interface.

This script shows how to start the web interface and configure it for use.
"""

import sys
import os
import logging
from pathlib import Path

# Add the parent directory to the path so we can import albion_radar
sys.path.insert(0, str(Path(__file__).parent.parent))

from albion_radar.web_interface import create_web_interface

def main():
    """Main function to run the web interface."""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("Albion Radar Web Interface")
    print("=" * 40)
    print()
    print("Starting web interface...")
    print("The interface will be available at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        # Create and run the web interface
        interface = create_web_interface()
        
        # Run the interface
        interface.run(
            host='127.0.0.1',
            port=5000,
            debug=True
        )
        
    except KeyboardInterrupt:
        print("\nShutting down web interface...")
    except Exception as e:
        print(f"Error running web interface: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 