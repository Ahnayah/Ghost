import pygame

class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos, speed=-8, screen_height=400):
        super().__init__()
        self.image = pygame.image.load("assets/arrow.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.height_y_constraint = screen_height
    
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()
            
    def update(self):
        self.rect.y += self.speed
        self.destroy()