import pygame
from typing import Optional
from .ui_element import UIElement
from ...core.event_manager import Event, EventType

class Button(UIElement):
    def __init__(self, position, size, text, color, on_click=None):
        super().__init__(position, size)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        self.hovered = False
        self.pressed = False
        self.on_click = on_click

    def _handle_self_event(self, event: pygame.event.Event) -> Optional[Event]:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.pressed = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed and self.hovered:
                self.pressed = False
                if self.on_click:
                    self.on_click()
                return Event(EventType.BUTTON_CLICK, {"button": self})
            self.pressed = False
            
        return None

    def set_on_click(self, callback):
        """Establece el callback para cuando se hace clic en el botón"""
        self.on_click = callback

    def _render_self(self, surface):
        # Calcular color basado en estado
        color = self.color
        if self.pressed:
            color = tuple(max(0, c - 40) for c in self.color)
        elif self.hovered:
            color = tuple(min(255, c + 20) for c in self.color)

        pygame.draw.rect(surface, color, self.rect)
        
        # Renderizar texto
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)