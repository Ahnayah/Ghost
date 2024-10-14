import pygame
from Arrow import Arrow

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/mainc.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 5
        self.ready = True
        self.shoot_time = 0
        self.shoot_cooldown = 600
        self.arrows = pygame.sprite.Group()
        self.facing_right = True  # Track the direction the player is facing
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing_right = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing_right = False
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_arrow()
            self.ready = False
            self.shoot_time = pygame.time.get_ticks()
        
        # Constrain player within window sides
        screen_rect = pygame.display.get_surface().get_rect()
        if self.rect.left < screen_rect.left:
            self.rect.left = screen_rect.left
        if self.rect.right > screen_rect.right:
            self.rect.right = screen_rect.right
        if self.rect.top < screen_rect.top:
            self.rect.top = screen_rect.top
        if self.rect.bottom > screen_rect.bottom:
            self.rect.bottom = screen_rect.bottom
            
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.ready = True
    
    def shoot_arrow(self):
        self.arrows.add(Arrow(self.rect.center, -8, self.rect.bottom)) 
    
    def update(self, arrows):        
        self.get_input()
        self.recharge()
        self.arrows.update()
