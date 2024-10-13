import pygame
import random
from Arrow import Arrow
from Player import Player

# Define screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

class AssetItem(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("assets/Item.png").convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.spawn_time = pygame.time.get_ticks() 
        

    def update(self):
        # Remove the asset item after 1 second
        if pygame.time.get_ticks() - self.spawn_time > 1000:
            self.kill()

class Malware(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        position = (random.randint(0, SCREEN_WIDTH), 0)  # Random x-coordinate at the top
        self.image = pygame.image.load("assets/Virus.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 1  # Initial speed
        self.start_time = pygame.time.get_ticks()  # Record the time when the malware is created

    def update(self, arrows, player):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
        # Increase speed over time
        if elapsed_time > 10:
            self.speed = 2  # Increase speed after 10 seconds
        self.rect.y += self.speed * (1.0 + elapsed_time / 10.0)

        # Check for collision with arrows
        arrows = pygame.sprite.spritecollide(self, arrows, True)
        if pygame.sprite.spritecollideany(self, arrows):
            self.kill()

    def hit(self):
        # Drop an asset item when hit
        return AssetItem(self.rect.center)

class Spyware(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        position = (random.randint(0, SCREEN_WIDTH), 0)  # Random x-coordinate at the top
        self.image = pygame.image.load("assets/Spyware.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 1  # Initial speed
        self.start_time = pygame.time.get_ticks()  # Record the time when the spyware is created

    def update(self, arrows, player, asset_group):
        # Calculate elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
        # Increase speed over time
        self.rect.y += self.speed * (1.0 + elapsed_time / 5.0)  # Increase speed faster
        # Check for collision with arrows
        collided_arrows = pygame.sprite.spritecollide(self, arrows, True)
        if collided_arrows:
            self.kill()
            # Drop asset item when hit
            asset_item = AssetItem(self.rect.center)
            asset_group.add(asset_item)

    def hit(self):
        # Drop an asset item when hit
        return AssetItem(self.rect.center)
