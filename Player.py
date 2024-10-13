import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/mainc.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 5
        self.ready = True
        self.shoot_time = 0
        self.shoot_cooldown = 600
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        
        if keys[pygame.K_SPACE]:
            self.shoot_arrow()
            self.ready = False
            self.shoot_time = pygame.time.get_ticks()
            
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
    def shoot_arrow(self):
        print("shoot")   
    
    def update(self):
        self.get_input()