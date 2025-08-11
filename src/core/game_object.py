import pygame
from ..graphics.renderable import Renderable
from typing import Tuple, Optional, Union

class GameObject(Renderable):
    def __init__(self, position: Tuple[float, float], 
                 visual: Union[pygame.Surface, Tuple[int, int, int], Tuple[int, int, int, int]] = None, 
                 size: Tuple[int, int] = (50, 50),
                 z_index: int = 0,
                 keep_aspect_ratio: bool = True):
        super().__init__(position, z_index)
        self.sprite = None
        self.color = None
        self.original_sprite = None  # Guardamos la sprite original
        self.size = size
        self.scale = (1.0, 1.0)
        self.rotation = 0.0
        self.keep_aspect_ratio = keep_aspect_ratio
        
        # Determinar si es un sprite o un color
        if isinstance(visual, pygame.Surface):
            self.set_sprite(visual)
        elif isinstance(visual, tuple):
            self.set_color(visual)

    def set_sprite(self, sprite: pygame.Surface) -> None:
        """Establece un sprite como visual del objeto y lo ajusta al tamaño"""
        self.original_sprite = sprite
        self._update_sprite()

    def set_size(self, size: Tuple[int, int]) -> None:
        """Actualiza el tamaño del objeto y ajusta el sprite si existe"""
        self.size = size
        self._update_sprite()

    def _update_sprite(self) -> None:
        """Actualiza el sprite aplicando el tamaño y la escala"""
        if self.original_sprite is None:
            return

        target_width = int(self.size[0] * self.scale[0])
        target_height = int(self.size[1] * self.scale[1])

        if self.keep_aspect_ratio:
            # Mantener aspect ratio
            original_ratio = self.original_sprite.get_width() / self.original_sprite.get_height()
            target_ratio = target_width / target_height

            if target_ratio > original_ratio:
                # Ajustar por altura
                target_width = int(target_height * original_ratio)
            else:
                # Ajustar por ancho
                target_height = int(target_width / original_ratio)

        try:
            self.sprite = pygame.transform.smoothscale(
                self.original_sprite, 
                (target_width, target_height)
            )
        except ValueError:
            # Fallback a scale normal si smoothscale falla
            self.sprite = pygame.transform.scale(
                self.original_sprite, 
                (target_width, target_height)
            )

    def render(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return

        if self.sprite is not None:
            # Aplicar rotación si es necesario
            if self.rotation != 0:
                rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
                rect = rotated_sprite.get_rect(center=self.position)
                surface.blit(rotated_sprite, rect)
            else:
                rect = self.sprite.get_rect(center=self.position)
                surface.blit(self.sprite, rect)
        
        elif self.color is not None:
            # Renderizado de forma coloreada
            scaled_size = (int(self.size[0] * self.scale[0]), 
                         int(self.size[1] * self.scale[1]))
            rect = pygame.Rect(0, 0, *scaled_size)
            rect.center = self.position
            
            if self.rotation != 0:
                surf = pygame.Surface(scaled_size, pygame.SRCALPHA)
                pygame.draw.rect(surf, self.color, surf.get_rect())
                rotated = pygame.transform.rotate(surf, self.rotation)
                rot_rect = rotated.get_rect(center=self.position)
                surface.blit(rotated, rot_rect)
            else:
                pygame.draw.rect(surface, self.color, rect)