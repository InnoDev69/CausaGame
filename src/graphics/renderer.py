import pygame
from typing import List, Dict, Tuple, Optional
from .renderable import Renderable
from .UI.ui_element import UIElement
from ..core.game_object import GameObject
from ..core.event_manager import Event

class Renderer:
    def __init__(self, screen: pygame.Surface, virtual_size: Tuple[int, int] = (800, 600)):
        self.screen = screen
        self.virtual_size = virtual_size
        # Superficie virtual con resolución base
        self.virtual_surface = pygame.Surface(virtual_size, pygame.SRCALPHA)
        self.renderables: Dict[int, List[Renderable]] = {}
        self.ui_layer = pygame.Surface(virtual_size, pygame.SRCALPHA)
        self.game_layer = pygame.Surface(virtual_size, pygame.SRCALPHA)

    def add(self, renderable: Renderable) -> None:
        """Añade un elemento para ser renderizado"""
        if renderable.z_index not in self.renderables:
            self.renderables[renderable.z_index] = []
        self.renderables[renderable.z_index].append(renderable)

    def remove(self, renderable: Renderable) -> None:
        """Elimina un elemento del renderizador"""
        if renderable.z_index in self.renderables:
            self.renderables[renderable.z_index].remove(renderable)

    def render(self) -> None:
        """Renderiza todos los elementos manteniendo el aspect ratio"""
        # Limpia las capas
        self.virtual_surface.fill((0, 0, 0, 0))
        self.ui_layer.fill((0, 0, 0, 0))
        self.game_layer.fill((0, 0, 0, 0))

        # Renderiza en orden por z-index
        for z_index in sorted(self.renderables.keys()):
            for renderable in self.renderables[z_index]:
                if isinstance(renderable, UIElement):
                    renderable.render(self.ui_layer)
                else:
                    renderable.render(self.game_layer)

        # Combina las capas en la superficie virtual
        self.virtual_surface.blit(self.game_layer, (0, 0))
        self.virtual_surface.blit(self.ui_layer, (0, 0))

        # Escala y centra en la pantalla real
        scale, offset = self.get_scale_and_offset()
        scaled_surface = pygame.transform.smoothscale(
            self.virtual_surface,
            (int(self.virtual_size[0] * scale),
             int(self.virtual_size[1] * scale))
        )
        
        self.screen.fill((0, 0, 0))
        self.screen.blit(scaled_surface, offset)
        
    def get_scale_and_offset(self) -> Tuple[float, Tuple[int, int]]:
        """Calcula la escala y el offset para mantener el aspect ratio"""
        screen_rect = self.screen.get_rect()
        virtual_rect = pygame.Rect((0, 0), self.virtual_size)
        
        scale_x = screen_rect.width / virtual_rect.width
        scale_y = screen_rect.height / virtual_rect.height
        scale = min(scale_x, scale_y)
        
        scaled_size = (int(virtual_rect.width * scale), 
                      int(virtual_rect.height * scale))
        offset = ((screen_rect.width - scaled_size[0]) // 2,
                 (screen_rect.height - scaled_size[1]) // 2)
                 
        return scale, offset

    def handle_ui_event(self, event: pygame.event.Event) -> Optional[Event]:
        """Propaga el evento a través de todos los elementos UI en orden inverso de z-index"""
        # Ordenar z-indices en orden inverso para que los elementos superiores reciban eventos primero
        for z_index in sorted(self.renderables.keys(), reverse=True):
            for renderable in self.renderables[z_index]:
                if isinstance(renderable, UIElement):
                    result = renderable.handle_event(event)
                    if result is not None:
                        return result
                if hasattr(renderable, 'update'):
                    renderable.update()
        return None