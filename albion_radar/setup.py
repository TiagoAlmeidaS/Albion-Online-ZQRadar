#!/usr/bin/env python3
"""
Setup script for Albion Radar Python Module

This script installs the albion_radar module and its dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements(requirements_file):
    """Install requirements from file."""
    if not os.path.exists(requirements_file):
        print(f"Warning: {requirements_file} not found")
        return False
    
    print(f"Installing requirements from {requirements_file}...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ])
        print(f"✓ Successfully installed requirements from {requirements_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False

def check_administrative_privileges():
    """Check if running with administrative privileges."""
    if platform.system() == "Windows":
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0

def main():
    """Main setup function."""
    print("Albion Radar Python Module Setup")
    print("=" * 40)
    print()
    
    # Check Python version
    check_python_version()
    
    # Check administrative privileges
    if not check_administrative_privileges():
        print("⚠ Warning: Administrative privileges may be required for packet capture")
        print("  Run this script as administrator if you encounter permission issues")
    else:
        print("✓ Administrative privileges detected")
    
    print()
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Install core requirements
    core_requirements = "requirements.txt"
    if os.path.exists(core_requirements):
        if not install_requirements(core_requirements):
            print("Failed to install core requirements")
            sys.exit(1)
    else:
        print("Warning: requirements.txt not found")
    
    # Install web interface requirements (optional)
    web_requirements = "requirements_web.txt"
    if os.path.exists(web_requirements):
        print("\nInstalling web interface dependencies (optional)...")
        install_requirements(web_requirements)
    else:
        print("\nWeb interface requirements not found, skipping...")
    
    print()
    print("Setup completed!")
    print()
    print("Usage examples:")
    print("  python albion_radar/example_usage.py")
    print("  python albion_radar/example_web_interface.py")
    print()
    print("For more information, see README.md")

if __name__ == '__main__':
    main() 