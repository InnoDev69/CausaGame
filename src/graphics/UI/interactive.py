from abc import ABC, abstractmethod
import pygame
from typing import Optional
from ...core.event_manager import Event

class Interactive(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Optional[Event]:
        """
        Maneja un evento de pygame y retorna un evento del sistema si es necesario
        Retorna None si el evento no fue manejado o no generó un evento del sistema
        """
        pass

    @abstractmethod
    def is_interactable(self) -> bool:
        """Determina si el elemento puede interactuar en este momento"""
        pass