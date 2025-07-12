"""
Web Interface for Albion Radar Python Module

This module provides a Flask-based web interface for the albion_radar module,
similar to the original Node.js views but adapted for Python.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
import time
from datetime import datetime

from .core.network_adapter import NetworkAdapterSelector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'albion_radar_secret_key_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Settings file path
SETTINGS_FILE = 'radar_settings.json'

def load_settings():
    """Load settings from JSON file"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_settings(settings):
    """Save settings to JSON file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except:
        return False

# Ignore list file path
IGNORE_LIST_FILE = 'ignore_list.json'

def load_ignore_list():
    """Load ignore list from JSON file"""
    if os.path.exists(IGNORE_LIST_FILE):
        try:
            with open(IGNORE_LIST_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'players': [], 'guilds': []}

def save_ignore_list(ignore_list):
    """Save ignore list to JSON file"""
    try:
        with open(IGNORE_LIST_FILE, 'w') as f:
            json.dump(ignore_list, f, indent=2)
        return True
    except:
        return False

@app.route('/')
def index():
    """Main radar page"""
    return render_template('index.html')

@app.route('/home')
def home():
    """Players settings page"""
    return render_template('home.html')

@app.route('/resources')
def resources():
    """Resources settings page"""
    return render_template('resources.html')

@app.route('/enemies')
def enemies():
    """Enemies settings page"""
    return render_template('enemies.html')

@app.route('/chests')
def chests():
    """Chests and dungeons settings page"""
    return render_template('chests.html')

@app.route('/settings')
def settings():
    """General settings page"""
    return render_template('settings.html')

@app.route('/map')
def map():
    """Map settings page"""
    return render_template('map.html')

@app.route('/ignorelist')
def ignorelist():
    """Ignore list management page"""
    return render_template('ignorelist.html')

@app.route('/drawing-items')
def drawing_items():
    """Drawing items settings page"""
    return render_template('drawing-items.html')

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get all settings"""
    return jsonify(load_settings())

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update settings"""
    settings = request.json
    if save_settings(settings):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 500

@app.route('/api/ignore-list', methods=['GET'])
def get_ignore_list():
    """Get ignore list"""
    return jsonify(load_ignore_list())

@app.route('/api/ignore-list', methods=['POST'])
def add_to_ignore_list():
    """Add item to ignore list"""
    data = request.json
    ignore_list = load_ignore_list()
    
    if data['type'] == 'player':
        if data['name'] not in ignore_list['players']:
            ignore_list['players'].append(data['name'])
    elif data['type'] == 'guild':
        if data['name'] not in ignore_list['guilds']:
            ignore_list['guilds'].append(data['name'])
    
    if save_ignore_list(ignore_list):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 500

@app.route('/api/ignore-list', methods=['DELETE'])
def remove_from_ignore_list():
    """Remove item from ignore list"""
    data = request.json
    ignore_list = load_ignore_list()
    
    if data['type'] == 'player':
        if data['index'] < len(ignore_list['players']):
            ignore_list['players'].pop(data['index'])
    elif data['type'] == 'guild':
        if data['index'] < len(ignore_list['guilds']):
            ignore_list['guilds'].pop(data['index'])
    
    if save_ignore_list(ignore_list):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 500

@app.route('/api/radar-data')
def get_radar_data():
    """Get current radar data"""
    # This would be connected to the actual radar data
    # For now, return sample data
    return jsonify({
        'players': [],
        'mobs': [],
        'resources': [],
        'chests': [],
        'dungeons': [],
        'fishing_spots': [],
        'wisp_cages': [],
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('status', {'message': 'Connected to Albion Radar'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('request_data')
def handle_data_request():
    """Handle data request from client"""
    # This would send actual radar data
    emit('radar_data', {
        'players': [],
        'mobs': [],
        'resources': [],
        'chests': [],
        'dungeons': [],
        'fishing_spots': [],
        'wisp_cages': [],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Albion Radar Web Interface...")
    print("📡 Web interface will be available at: http://localhost:5000")
    print("🎮 Radar data will be available at: http://localhost:5000")
    print("⚙️  Settings can be configured at: http://localhost:5000/settings")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 