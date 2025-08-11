import pygame
from src.graphics.UI.ui_element import UIElement
from typing import Tuple, Optional, Any, Callable, Union

class Label(UIElement):
    def __init__(self, 
                 text: str = "", 
                 position: Tuple[float, float] = (0, 0), 
                 font_size: int = 36, 
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 background_color: Optional[Tuple[int, int, int]] = None, 
                 font_name: Optional[str] = None,
                 z_index: int = 100,
                 variable: Union[Any, Callable[[], Any]] = None,
                 format_func: Callable[[Any], str] = str,
                 update_interval: float = 1.0):  # Intervalo en segundos
        # Inicializar el tamaño en 0,0 - se actualizará en _render
        super().__init__(position, (0, 0), z_index)
        
        self.base_text = text
        self.text = text
        self.font = pygame.font.Font(font_name, font_size)
        self.text_color = text_color
        self.background_color = background_color
        self.variable = variable
        self.format_func = format_func
        self._last_value = None
        self.update_interval = update_interval
        self._last_update_time = 0
        self._render()

    def update(self) -> None:
        """Actualiza el texto si la variable ha cambiado y ha pasado el intervalo"""
        current_time = pygame.time.get_ticks() / 1000  # Convertir a segundos
        
        if (current_time - self._last_update_time) >= self.update_interval:
            if self.variable is not None:
                # Si es una función, llamarla para obtener el valor
                current_value = self.variable() if callable(self.variable) else self.variable
                
                if current_value != self._last_value:
                    self._last_value = current_value
                    formatted_value = self.format_func(current_value)
                    self.text = f"{self.base_text}{formatted_value}"
                    self._render()
            
            self._last_update_time = current_time

    def set_variable(self, variable: Any, format_func: Callable[[Any], str] = str) -> None:
        """Establece la variable a observar y su función de formato"""
        self.variable = variable
        self.format_func = format_func
        self.update()

    def _render(self):
        """Render the text to a surface"""
        self.surface = self.font.render(self.text, True, self.text_color, self.background_color)
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.position
        # Actualizar el tamaño basado en la superficie renderizada
        self.size = self.surface.get_size()

    def set_text(self, new_text: str) -> None:
        """Update the text content"""
        if self.text != new_text:
            self.text = new_text
            self._render()

    def _render_self(self, surface: pygame.Surface) -> None:
        """Implementación del método abstracto de UIElement"""
        if not self.visible:
            return
        surface.blit(self.surface, self.rect)

    def is_interactable(self) -> bool:
        """Implementación del método abstracto de Interactive"""
        return False  # Los labels no son interactivos por defecto

    def handle_event(self, event: pygame.event.Event) -> None:
        """Implementación del método abstracto de Interactive"""
        return None  # Los labels no manejan eventos