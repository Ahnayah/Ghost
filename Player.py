import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/mainc.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 5
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.y += self.speed
        if keys[pygame.K_d]:
            self.rect.y += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
    
    def update(self):
        self.get_input()
