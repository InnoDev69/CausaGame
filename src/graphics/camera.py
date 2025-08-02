import pygame
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.target = None

    def set_target(self, target):
        self.target = target
    
    def update(self):
        if self.target:
            player_rect = self.target.get_rect()
            self.x = player_rect.centerx - self.width / 2

    def apply(self, rect):
        scaled_x = (rect.x - self.x) * self.zoom
        scaled_y = (rect.y - self.y) * self.zoom

        return pygame.Rect(scaled_x, scaled_y, rect.width * self.zoom, rect.height * self.zoom)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  
            self.zoom *= 1.1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: 
            self.zoom /= 1.1

class FreeCamera(Camera):
    def update(self):
        keys = pygame.key.get_pressed()
        speed = 5

        if keys[pygame.K_LEFT]:
            self.x -= speed
        if keys[pygame.K_RIGHT]:
            self.x += speed
        if keys[pygame.K_UP]:
            self.y -= speed
        if keys[pygame.K_DOWN]:
            self.y += speed


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  
                self.zoom *= 1.1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  
                self.zoom /= 1.1
    def apply(self, rect):
        scaled_x = (rect.x - self.x) * self.zoom
        scaled_y = (rect.y - self.y) * self.zoom

        return pygame.Rect(scaled_x, scaled_y, rect.width * self.zoom, rect.height * self.zoom)