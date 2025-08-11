import pygame
from ..renderable import Renderable
from .interactive import Interactive
from typing import Tuple, Optional
from ...core.event_manager import Event

class UIElement(Renderable, Interactive):
    def __init__(self, position: Tuple[float, float], size: Tuple[int, int], z_index: int = 100):
        super().__init__(position, z_index)
        self.size = size
        self.rect = pygame.Rect(*position, *size)
        self.enabled = True
        self.parent = None
        self.children = []

    def is_interactable(self) -> bool:
        return self.enabled and self.visible

    def handle_event(self, event: pygame.event.Event) -> Optional[Event]:
        if not self.is_interactable():
            return None
            
        # Manejar eventos en los hijos primero
        for child in self.children:
            result = child.handle_event(event)
            if result is not None:
                return result
                
        return self._handle_self_event(event)

    def _handle_self_event(self, event: pygame.event.Event) -> Optional[Event]:
        """Implementado por las subclases para manejar sus propios eventos"""
        return None

    def update_rect(self):
        """Actualiza el rectángulo de colisión cuando la posición cambia"""
        self.rect.topleft = self.get_absolute_position()

    def add_child(self, child: 'UIElement') -> None:
        child.parent = self
        self.children.append(child)

    def get_absolute_position(self) -> Tuple[float, float]:
        if self.parent is None:
            return self.position
        parent_pos = self.parent.get_absolute_position()
        return (parent_pos[0] + self.position[0], 
                parent_pos[1] + self.position[1])

    def render(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        # Renderiza primero este elemento
        self._render_self(surface)
        # Luego renderiza los hijos
        for child in self.children:
            child.render(surface)

    def _render_self(self, surface: pygame.Surface) -> None:
        pass  # Implementado por las subclases