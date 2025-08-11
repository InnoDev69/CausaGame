"""Un elemento de interfaz que sirve como campo de texto editable."""
import pygame
from typing import Optional
from .ui_element import UIElement
from ...core.event_manager import Event, EventType

class TextField(UIElement):
    def __init__(self, position, size, placeholder="", max_length=20, color=(255, 255, 255), font_size=24):
        super().__init__(position, size, z_index=100)
        self.placeholder = placeholder
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.text = ""
        self.active = False
        self.cursor_visible = False
        self.cursor_timer = 0
        self.max_length = max_length
        self.on_text_changed = None
        self.on_submit = None

    def _handle_self_event(self, event: pygame.event.Event) -> Optional[Event]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            was_active = self.active
            self.active = self.rect.collidepoint(event.pos)
            
            if self.active and not was_active:
                return Event(EventType.TEXT_FIELD_FOCUSED, {"field": self})
            elif not self.active and was_active:
                if self.on_submit:
                    self.on_submit(self.text)
                return Event(EventType.TEXT_FIELD_UNFOCUSED, {"field": self, "text": self.text})
                
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                if self.on_submit:
                    self.on_submit(self.text)
                return Event(EventType.TEXT_SUBMITTED, {
                    "field": self,
                    "text": self.text
                })
                
            elif event.key == pygame.K_BACKSPACE:
                old_text = self.text
                self.text = self.text[:-1]
                if self.on_text_changed and old_text != self.text:
                    self.on_text_changed(self.text)
                return Event(EventType.TEXT_CHANGED, {
                    "field": self,
                    "text": self.text
                })
                
            elif event.unicode.isprintable():
                if len(self.text) < self.max_length:
                    old_text = self.text
                    self.text += event.unicode
                    if self.on_text_changed and old_text != self.text:
                        self.on_text_changed(self.text)
                    return Event(EventType.TEXT_CHANGED, {
                        "field": self,
                        "text": self.text
                    })
                
        return None

    def set_on_text_changed(self, callback):
        """Establece el callback para cuando el texto cambia"""
        self.on_text_changed = callback

    def set_on_submit(self, callback):
        """Establece el callback para cuando se envía el texto"""
        self.on_submit = callback

    def _render_self(self, surface):
        # Dibuja el fondo
        border_color = (0, 255, 0) if self.active else (128, 128, 128)
        pygame.draw.rect(surface, border_color, self.rect, 2)
        pygame.draw.rect(surface, (255, 255, 255), self.rect.inflate(-4, -4))

        # Renderiza el texto o placeholder
        display_text = self.text or self.placeholder
        text_color = (0, 0, 0) if self.text else (128, 128, 128)
        text_surface = self.font.render(display_text, True, text_color)
        
        # Centra el texto verticalmente y alinea a la izquierda
        text_rect = text_surface.get_rect(
            midleft=(self.rect.left + 5, self.rect.centery)
        )
        surface.blit(text_surface, text_rect)

        # Dibuja el cursor si está activo
        if self.active:
            cursor_x = text_rect.right + 2
            if pygame.time.get_ticks() % 1000 < 500:  # Parpadeo del cursor
                pygame.draw.line(surface, (0, 0, 0),
                               (cursor_x, self.rect.top + 5),
                               (cursor_x, self.rect.bottom - 5))