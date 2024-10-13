import pygame
import sys
import random
from Player import Player
from Enemy import Malware, Spyware, AssetItem

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        self.spawn_malware_event = pygame.USEREVENT + 1
        self.spawn_spyware_event = pygame.USEREVENT + 2
        self.spawn_asset_event = pygame.USEREVENT + 3
        pygame.time.set_timer(self.spawn_malware_event, 2000)
        pygame.time.set_timer(self.spawn_spyware_event, 3000)
        pygame.time.set_timer(self.spawn_asset_event, 5000)
        
        self.malware = pygame.sprite.Group()
        self.spyware = pygame.sprite.Group()
        self.asset_group = pygame.sprite.Group()

        # Initialize player at the center of the screen
        player_sprite = Player((self.screen_width / 2, self.screen_height / 2))
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        self.image = pygame.image.load("assets/background.png")
        self.clock = pygame.time.Clock()
        self.game_over = False

    def draw_background(self):
        """Blit the background image to the screen."""
        size = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
        self.screen.blit(size, (0, 0))
        
    def draw(self):
        """Draw all game elements."""
        self.draw_background()
        self.player.draw(self.screen)
        self.player.sprite.arrows.draw(self.screen)
        self.malware.draw(self.screen)
        self.spyware.draw(self.screen)
        self.asset_group.draw(self.screen)
        if self.game_over:
            self.draw_game_over()
        pygame.display.flip()
        
    def draw_game_over(self):
        """Draw the game over screen."""
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.screen.blit(text, text_rect)
        
    def update(self):
        """Update all game elements."""
        self.player.update(self.malware)
        self.malware.update(self.player.sprite.arrows, self.player.sprite)
        self.spyware.update(self.player.sprite.arrows, self.player.sprite, self.asset_group)
        self.asset_group.update()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == self.spawn_malware_event:
                malware = Malware((random.randint(0, self.screen_width), 0))
                self.malware.add(malware)
            elif event.type == self.spawn_spyware_event:
                spyware = Spyware((random.randint(0, self.screen_width), 0))
                self.spyware.add(spyware)
            elif event.type == self.spawn_asset_event:
                if self.spyware:
                    spyware = random.choice(self.spyware.sprites())
                    asset_item = AssetItem(spyware.rect.center)
                    self.asset_group.add(asset_item)
        
    def run(self):
        while True:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    # Pygame setup
    pygame.init()
    screen_width = 600
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Malware Mayhem")
    
    # Create and run the game
    game = Game(screen)
    game.run()
