import pygame
from src.core.event_manager import EventManager, Event, EventType
from config.constants import *
from src.graphics.renderer import Renderer
from src.graphics.UI.button import Button
from src.graphics.UI.text_field import TextField
from src.core.game_object import GameObject
from src.world.world_manager import World
from src.graphics.UI.label import Label

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Game Title")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Inicializar el renderer
        self.renderer = Renderer(self.screen)
        
        # Crear botones con sus callbacks
        start_button = Button(
            (100, 100), 
            (200, 50), 
            "Start", 
            (0, 255, 0),
            on_click=self.start_game
        )
        quit_button = Button(
            (100, 200), 
            (200, 50), 
            "Quit", 
            (255, 0, 0),
            on_click=self.quit_game
        )
        
        self.renderer.add(start_button)
        self.renderer.add(quit_button)
        
        # Crear campo de texto con sus callbacks
        self.name_field = TextField(
            (300, 100),
            (200, 40),
            placeholder="Enter name...",
            max_length=20
        )
        self.name_field.set_on_text_changed(self.on_name_changed)
        self.name_field.set_on_submit(self.on_name_submitted)
        self.renderer.add(self.name_field)
        
        self.label = Label(
            text="FPS: ",
            position=(300, 200),
            font_size=24,
            text_color=(255, 255, 255),
            variable=self.clock.get_fps,  # Pasamos la función directamente
            format_func=lambda fps: f"{fps:.1f}",  # Formatear a 1 decimal
            update_interval=0.1  # Actualizar cada 0.1 segundos
        )
        self.renderer.add(self.label)
        
        # Inicializar el gestor de eventos
        self.event_manager = EventManager()
        self._setup_event_handlers()
        
        # Inicializar el gestor de mundos
        self.world_manager = World("E", "./src/world/map.txt")
        
    def build_world(self):
        for row, block in enumerate(self.world_manager.get_world_data()):
            for col, char in enumerate(block.strip()):
                if char != '0':
                    self.renderer.add(GameObject((col * 50, row * 50), 
                    pygame.image.load("./assets/textures/bricks.png"), z_index=0,
                    size=(50, 50)))
        
    def spawn_entity(self, entity):
        """Añade una entidad al juego y la renderiza"""
        self.renderer.add(entity)
        self.world_manager.add_entity(entity)

    def _setup_event_handlers(self):
        """Configura los manejadores de eventos básicos"""
        self.event_manager.subscribe(EventType.GAME_OVER, self._handle_game_over)
        self.event_manager.subscribe(EventType.LEVEL_COMPLETE, self._handle_level_complete)

    def _handle_game_over(self, event: Event):
        print("Game Over!")
        # Implementa la lógica de game over
        self.running = False

    def _handle_level_complete(self, event: Event):
        print(f"Level Complete! Score: {event.data.get('score', 0)}")
        # Implementa la lógica de nivel completado

    def _handle_text_submitted(self, event: Event):
        """Maneja cuando se envía el texto (presionar Enter)"""
        field = event.data["field"]
        if field == self.name_field:
            text = event.data["text"]

            print(f"Nombre enviado: {text}")
            # Aquí puedes hacer lo que necesites con el texto
            # Por ejemplo:
            self.player.set_name(text)
            # O:
            self.save_player_name(text)

    def _handle_text_changed(self, event: Event):
        """Maneja cambios en el texto mientras se escribe"""
        field = event.data["field"]
        text = event.data["text"]
        
        if field == self.name_field:
            # Validación en tiempo real
            if len(text) > 20:  # ejemplo: limitar longitud
                field.text = text[:20]
            # O actualizar UI en tiempo real
            self.update_character_preview(text)

    def _handle_field_focused(self, event: Event):
        """Maneja cuando un campo obtiene el foco"""
        field = event.data["field"]
        # Por ejemplo, pausar el juego cuando se está escribiendo
        if field == self.name_field:
            pass

    def _handle_pygame_events(self):
        """Maneja los eventos de Pygame y los convierte en eventos del sistema"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Propagar eventos a elementos UI
            self.renderer.handle_ui_event(event)

    def start_game(self):
        print("Juego iniciado!")
        # Implementa la lógica de inicio del juego

    def quit_game(self):
        print("Saliendo del juego...")
        self.running = False

    def on_name_changed(self, text):
        print(f"Nombre cambiando: {text}")
        # Implementa la lógica de validación o actualización en tiempo real

    def on_name_submitted(self, text):
        print(f"Nombre enviado: {text}")
        # Implementa la lógica cuando se envía el nombre

    def run(self):
        while self.running:
            self._handle_pygame_events()
            
            # Actualiza el estado del juego
            self.update()
            
            # Renderiza
            self.render()
            
            # Mantén el framerate constante
            self.clock.tick(CLOCK)

        pygame.quit()

    def update(self):
        # Actualiza la lógica del juego
        pass

    def render(self):
        self.screen.fill((0, 0, 0))
        self.renderer.render()
        pygame.display.flip()
