from enum import Enum
from typing import Callable, Dict, List

class EventType(Enum):
    PLAYER_MOVE = "player_move"
    PLAYER_JUMP = "player_jump"
    COLLISION = "collision"
    GAME_OVER = "game_over"
    LEVEL_COMPLETE = "level_complete"
    GAME_START = "game_start"
    GAME_QUIT = "game_quit"
    BUTTON_CLICK = "button_click"
    TEXT_INPUT = "text_input"
    MENU_OPEN = "menu_open"
    MENU_CLOSE = "menu_close"
    TEXT_FIELD_FOCUSED = "text_field_focused"
    TEXT_FIELD_UNFOCUSED = "text_field_unfocused"
    TEXT_CHANGED = "text_changed"
    TEXT_SUBMITTED = "text_submitted"
    # Añade más tipos de eventos según necesites

class Event:
    def __init__(self, event_type: EventType, data: dict = None):
        self.type = event_type
        self.data = data or {}

class EventManager:
    def __init__(self):
        self._listeners: Dict[EventType, List[Callable]] = {}
        
    def subscribe(self, event_type: EventType, listener: Callable) -> None:
        """Suscribe un listener a un tipo de evento específico"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
        
    def unsubscribe(self, event_type: EventType, listener: Callable) -> None:
        """Desuscribe un listener de un tipo de evento específico"""
        if event_type in self._listeners and listener in self._listeners[event_type]:
            self._listeners[event_type].remove(listener)
            
    def dispatch(self, event: Event) -> None:
        """Dispara un evento y notifica a todos los listeners suscritos"""
        if event.type in self._listeners:
            for listener in self._listeners[event.type]:
                listener(event)