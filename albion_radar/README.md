# Albion Radar Python Module

A Python implementation of the Albion Online radar system, providing packet capture, parsing, and real-time game data analysis.

## Features

- **Packet Capture**: Network adapter selection and packet capture for Albion Online traffic
- **Photon Protocol Parsing**: Decode and parse Photon protocol packets
- **Real-time Data Processing**: Handle various game entities (players, resources, mobs, etc.)
- **Modular Architecture**: Extensible handler system for different game objects
- **Web Interface**: Modern web-based control interface
- **Cross-platform**: Works on Windows, Linux, and macOS

## Installation

### Prerequisites

- Python 3.8 or higher
- Administrative privileges (for packet capture)
- Network adapter with Albion Online traffic

### Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Web interface dependencies (optional)
pip install -r requirements_web.txt
```

## Usage

### Command Line Interface

```python
from albion_radar import Radar, NetworkAdapterSelector

# Select network adapter
selector = NetworkAdapterSelector()
adapter = selector.select_adapter_interactive()

# Start radar
radar = Radar(adapter)
radar.start()
```

### Web Interface

Start the web interface for a graphical control panel:

```bash
python albion_radar/example_web_interface.py
```

Then open your browser to `http://127.0.0.1:5000`

### Network Adapter Selection

```python
from albion_radar.core.network_adapter import NetworkAdapterSelector

selector = NetworkAdapterSelector()

# List available adapters
adapters = selector.list_adapters()
print("Available adapters:", adapters)

# Select adapter automatically
adapter = selector.select_adapter_auto()

# Select adapter interactively
adapter = selector.select_adapter_interactive()

# Select specific adapter
selector.select_adapter("Ethernet")
```

## Architecture

### Core Components

- **`core/radar.py`**: Main radar system orchestrator
- **`core/packet_capture.py`**: Network packet capture functionality
- **`core/photon_parser.py`**: Photon protocol packet parsing
- **`core/network_adapter.py`**: Network adapter selection and management
- **`core/data_manager.py`**: Data management and storage

### Handlers

- **`handlers/players_handler.py`**: Player detection and tracking
- **`handlers/harvestables_handler.py`**: Resource detection
- **`handlers/mobs_handler.py`**: Enemy mob detection
- **`handlers/chests_handler.py`**: Chest and dungeon detection
- **`handlers/dungeons_handler.py`**: Dungeon entrance detection
- **`handlers/fishing_handler.py`**: Fishing spot detection
- **`handlers/wisp_cage_handler.py`**: Wisp cage detection

### Models

- **`models/player.py`**: Player data model
- **`models/resource.py`**: Resource data model
- **`models/mob.py`**: Mob data model
- **`models/chest.py`**: Chest data model
- **`models/dungeon.py`**: Dungeon data model

### Web Interface

- **`web_interface.py`**: Flask-based web server
- **`templates/`**: HTML templates for the web interface
- **`static/`**: Static assets (CSS, JS, images)

## Configuration

### Event Codes

Configure event codes in `config/event_codes.py`:

```python
EVENT_CODES = {
    'PLAYER_JOIN': 1,
    'PLAYER_LEAVE': 2,
    'RESOURCE_SPAWN': 3,
    # ... more codes
}
```

### Settings

Settings are stored in JSON format and can be managed through the web interface or programmatically:

```python
from albion_radar.web_interface import AlbionRadarWebInterface

interface = AlbionRadarWebInterface()
settings = interface._load_settings()
```

## Development

### Project Structure

```
albion_radar/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── radar.py
│   ├── packet_capture.py
│   ├── photon_parser.py
│   ├── network_adapter.py
│   └── data_manager.py
├── handlers/
│   ├── __init__.py
│   ├── players_handler.py
│   ├── harvestables_handler.py
│   ├── mobs_handler.py
│   ├── chests_handler.py
│   ├── dungeons_handler.py
│   ├── fishing_handler.py
│   └── wisp_cage_handler.py
├── models/
│   ├── __init__.py
│   ├── player.py
│   ├── resource.py
│   ├── mob.py
│   ├── chest.py
│   └── dungeon.py
├── config/
│   ├── __init__.py
│   └── event_codes.py
├── web_interface.py
├── templates/
│   ├── base.html
│   └── index.html
├── example_usage.py
├── example_network_adapter.py
├── example_web_interface.py
├── requirements.txt
├── requirements_web.txt
└── README.md
```

### Adding New Handlers

1. Create a new handler in `handlers/`:
```python
from .base_handler import BaseHandler

class NewEntityHandler(BaseHandler):
    def __init__(self):
        super().__init__()
    
    def handle_packet(self, packet):
        # Process packet and extract data
        pass
    
    def get_data(self):
        # Return processed data
        return self.data
```

2. Register the handler in the radar system:
```python
from .handlers.new_entity_handler import NewEntityHandler

radar = Radar(adapter)
radar.register_handler(NewEntityHandler())
```

### Web Interface Customization

The web interface uses Flask with Socket.IO for real-time communication. Templates are in `templates/` and can be customized for your needs.

## Examples

### Basic Usage

```python
from albion_radar import Radar, NetworkAdapterSelector

# Setup
selector = NetworkAdapterSelector()
adapter = selector.select_adapter_auto()

# Start radar
radar = Radar(adapter)
radar.start()

# Access data
players = radar.get_players()
resources = radar.get_resources()
```

### Web Interface

```python
from albion_radar.web_interface import create_web_interface

# Create and run web interface
interface = create_web_interface()
interface.run(host='127.0.0.1', port=5000)
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Run with administrative privileges
2. **No Network Adapters**: Ensure Albion Online is running
3. **No Packets Captured**: Check firewall settings and adapter selection

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

This project is for educational purposes. Please respect game terms of service.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for complying with Albion Online's terms of service and applicable laws. 