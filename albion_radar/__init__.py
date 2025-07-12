"""
Albion Radar - Módulo Python para captura e processamento de dados do Albion Online

Este módulo fornece uma interface Python para capturar e processar dados de rede
do jogo Albion Online, permitindo detectar jogadores, recursos, mobs e outros objetos.

Exemplo de uso:
    from albion_radar import AlbionRadar
    
    radar = AlbionRadar()
    radar.on_player_detected(lambda player: print(f"Jogador: {player.nickname}"))
    await radar.start()
"""

from .core.radar import AlbionRadar
from .core.network_adapter import NetworkAdapterSelector, NetworkAdapter, select_adapter_for_capture
from .models.player import Player
from .models.resource import Resource
from .models.mob import Mob
from .models.chest import Chest
from .config.event_codes import EventCodes

__version__ = "1.0.0"
__author__ = "Zeldruck"
__license__ = "ISC"

__all__ = [
    "AlbionRadar",
    "NetworkAdapterSelector",
    "NetworkAdapter", 
    "select_adapter_for_capture",
    "Player", 
    "Resource",
    "Mob",
    "Chest",
    "EventCodes"
] 