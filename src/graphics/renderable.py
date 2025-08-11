from abc import ABC, abstractmethod
import pygame
from typing import Tuple

class Renderable(ABC):
    def __init__(self, position: Tuple[float, float], z_index: int = 0):
        self.position = position
        self.z_index = z_index  # Para controlar el orden de renderizado
        self.visible = True

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        pass