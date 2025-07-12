# Albion Online ZQRadar - Python Version

A complete Python port of the original Node.js Albion Online radar tool, providing real-time game data visualization and analysis.

## 🚀 Features

### Core Functionality
- **Real-time packet capture** from Albion Online network traffic
- **Photon protocol parsing** for game data extraction
- **Multi-adapter network support** with automatic detection
- **Web-based interface** with real-time updates via WebSocket

### Radar Detection
- **Players**: Name, health, guild, equipment, distance, mounted status
- **Mobs & Bosses**: Health, level, type, special enemies (Crystal Spider, Fairy Dragon, etc.)
- **Resources**: All harvestable resources with tier/enchant filtering
- **Chests & Dungeons**: Green, blue, purple, yellow chests and various dungeon types
- **Fishing Spots**: Water-based resource locations
- **Wisp Cages**: Special mist content
- **Maps**: Interactive map with zoom and navigation

### Advanced Features
- **Ignore List Management**: Filter out specific players/guilds
- **Settings Management**: Comprehensive configuration system
- **Drawing Components**: Visual representation with color coding
- **Sound Alerts**: Audio notifications for important events
- **Dark Mode**: Modern UI with dark theme support

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (for network adapter access)
- Albion Online installed and running

### Quick Start (Windows)
1. **Download** the project files
2. **Run** `_INSTALL_FINAL.bat` as Administrator
3. **Run** `_RUN_FINAL.bat` to start the radar
4. **Open** http://localhost:5000 in your browser

### Manual Installation
```bash
# Install dependencies
pip install flask flask-socketio scapy psutil

# Run the web interface
python -m albion_radar.web_interface
```

## 🎮 Usage

### Starting the Radar
1. **Launch** Albion Online
2. **Run** the radar application
3. **Open** the web interface at http://localhost:5000
4. **Configure** settings in the web interface
5. **Start** packet capture from the main dashboard

### Web Interface Pages
- **Home** (`/home`): Player and PvP settings
- **Resources** (`/resources`): Harvestable resource filters
- **Enemies** (`/enemies`): Mob and boss detection settings
- **Chests** (`/chests`): Chest and dungeon filters
- **Settings** (`/settings`): General configuration
- **Map** (`/map`): Map display settings
- **Ignore List** (`/ignorelist`): Player/guild filtering
- **Drawing Items** (`/drawing-items`): Item display settings

## 🏗️ Architecture

### Core Modules
```
albion_radar/
├── core/
│   ├── radar.py              # Main radar engine
│   ├── packet_capture.py     # Network packet capture
│   ├── photon_parser.py      # Photon protocol parsing
│   ├── network_adapter.py    # Network adapter management
│   └── data_manager.py       # Data storage and management
├── handlers/
│   ├── players_handler.py    # Player data processing
│   ├── mobs_handler.py       # Mob data processing
│   ├── harvestables_handler.py # Resource processing
│   ├── chests_handler.py     # Chest processing
│   ├── dungeons_handler.py   # Dungeon processing
│   ├── fishing_handler.py    # Fishing spot processing
│   └── wisp_cage_handler.py # Wisp cage processing
├── drawing/
│   ├── base_drawing.py       # Base drawing functionality
│   ├── players_drawing.py    # Player visualization
│   ├── harvestables_drawing.py # Resource visualization
│   ├── mobs_drawing.py       # Mob visualization
│   ├── chests_drawing.py     # Chest visualization
│   ├── dungeons_drawing.py   # Dungeon visualization
│   ├── fishing_drawing.py    # Fishing visualization
│   ├── wisp_cage_drawing.py  # Wisp cage visualization
│   └── maps_drawing.py       # Map visualization
├── models/
│   ├── player.py             # Player data model
│   ├── mob.py                # Mob data model
│   ├── resource.py           # Resource data model
│   ├── chest.py              # Chest data model
│   └── dungeon.py            # Dungeon data model
├── templates/                # Web interface templates
├── web_interface.py          # Flask web application
└── __init__.py              # Package initialization
```

### Data Flow
1. **Packet Capture** → Network adapter captures Albion traffic
2. **Photon Parsing** → Protocol parser extracts game data
3. **Handler Processing** → Specialized handlers process data types
4. **Data Management** → Centralized data storage and retrieval
5. **Drawing Components** → Visual representation generation
6. **Web Interface** → Real-time display via WebSocket

## ⚙️ Configuration

### Settings Management
All settings are stored in `radar_settings.json` and managed through the web interface:

- **Player Settings**: Display options, filters, alerts
- **Resource Settings**: Tier/enchant filters, resource types
- **Enemy Settings**: Level filters, boss detection
- **Chest Settings**: Type filters, enchant levels
- **General Settings**: Performance, alerts, network
- **Map Settings**: Display options, zoom, style

### Ignore List
Manage ignored players and guilds in `ignore_list.json`:
- Add/remove individual players
- Add/remove entire guilds
- Automatic filtering during detection

## 🔧 Development

### Project Structure
```
Albion-Online-ZQRadar/
├── albion_radar/            # Python module
├── _INSTALL_FINAL.bat       # Windows installer
├── _RUN_FINAL.bat          # Windows launcher
├── README.md               # This file
└── requirements_web.txt    # Python dependencies
```

### Adding New Features
1. **Create Handler**: Add new handler in `handlers/`
2. **Create Model**: Add data model in `models/`
3. **Create Drawing**: Add visualization in `drawing/`
4. **Update Web Interface**: Add routes and templates
5. **Update Settings**: Add configuration options

### Testing
```bash
# Run web interface in debug mode
python -m albion_radar.web_interface

# Test specific components
python -c "from albion_radar.core.radar import Radar; print('Radar module loaded')"
```

## 🛡️ Security & Legal

### Important Notes
- **Educational Purpose**: This tool is for educational and research purposes
- **Game Terms**: Use at your own risk and in accordance with Albion Online's Terms of Service
- **Network Access**: Requires administrator privileges for packet capture
- **Privacy**: Only captures Albion Online network traffic

### Safety Features
- **Local Only**: All data processed locally, no external transmission
- **Configurable**: Full control over what data is captured and displayed
- **Transparent**: Open source code for full transparency

## 🤝 Contributing

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add comprehensive docstrings
- Include error handling
- Test with different network configurations
- Update documentation for new features

## 📄 License

This project is provided as-is for educational purposes. Use responsibly and in accordance with Albion Online's Terms of Service.

## 🆘 Support

### Common Issues
1. **"No network adapters found"**: Run as Administrator
2. **"Flask not found"**: Run `pip install flask flask-socketio`
3. **"Permission denied"**: Run installer as Administrator
4. **"No data detected"**: Ensure Albion Online is running

### Getting Help
- Check the web interface logs for error messages
- Verify network adapter selection
- Ensure Albion Online is actively running
- Test with different network configurations

---

**🎮 Happy Hunting in Albion Online! 🎯**