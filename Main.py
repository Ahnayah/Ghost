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
        pygame.time.set_timer(self.spawn_malware_event, 2000)
        pygame.time.set_timer(self.spawn_spyware_event, 3000)
        
        self.malware = pygame.sprite.Group()
        self.spyware = pygame.sprite.Group()
        self.asset_group = pygame.sprite.Group()

        # Initialize player at the center of the screen
        player_sprite = Player((self.screen_width / 2, self.screen_height / 2))
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        self.image = pygame.image.load("assets/background.png")
        self.clock = pygame.time.Clock()
        self.game_over = False

        # Counters for malwares and spywares that passed through
        self.malwares_passed = 0
        self.spywares_passed = 0
    
        self.show_start_menu()

    def show_start_menu(self):
        # Check for null pointer references
        if not self.screen:
            raise RuntimeError("Screen is null")
            
        font = pygame.font.Font(None, 74)
        text = font.render("Defend your firewall!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
            
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        
    def reset_game(self):
        self.malware.empty()
        self.spyware.empty()
        self.asset_group.empty()
        self.player.sprite.rect.center = (self.screen_width / 2, self.screen_height / 2)
        self.game_over = False
        self.malwares_passed = 0
        self.spywares_passed = 0

    def draw_background(self):
        size = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
        self.screen.blit(size, (0, 0))
        
    def draw(self):
        self.draw_background()
        self.player.draw(self.screen)
        self.player.sprite.arrows.draw(self.screen)
        self.malware.draw(self.screen)
        self.spyware.draw(self.screen)
        self.asset_group.draw(self.screen)
        self.draw_counter()
        if self.game_over:
            self.draw_game_over()
        pygame.display.flip()
        
    def draw_game_over(self):
        font = pygame.font.Font(None, 55)
        text = font.render("Game Over. Press 'R' to restart.", True, ('white'))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.screen.blit(text, text_rect)
        
    def draw_counter(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Malware Passed: {self.malwares_passed}/4", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        text = font.render(f"Spyware Passed: {self.spywares_passed}/4", True, (255, 255, 255))
        self.screen.blit(text, (10, 50))
        
    def update(self):
        self.player.update(self.malware)
        self.malware.update(self.player.sprite.arrows, self.player.sprite)
        self.spyware.update(self.player.sprite.arrows, self.player.sprite, self.asset_group)
        self.asset_group.update()

        # Check for collisions between arrows and malware
        for arrow in self.player.sprite.arrows:
            collided_malware = pygame.sprite.spritecollide(arrow, self.malware, True)
            for malware in collided_malware:
                asset_item = AssetItem(malware.rect.center)
                self.asset_group.add(asset_item)
                arrow.kill()

        # Check if any malware has passed the bottom of the screen
        for malware in self.malware:
            if malware.rect.top > self.screen_height:
                self.malwares_passed += 1
                malware.kill()
                if self.malwares_passed >= 4:
                    self.game_over = True

        # Check if any spyware has passed the bottom of the screen
        for spyware in self.spyware:
            if spyware.rect.top > self.screen_height:
                self.spywares_passed += 1
                spyware.kill()
                if self.spywares_passed >= 8:
                    self.game_over = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            elif event.type == self.spawn_malware_event:
                malware = Malware((random.randint(0, self.screen_width), 0))
                self.malware.add(malware)
            elif event.type == self.spawn_spyware_event:
                spyware = Spyware((random.randint(0, self.screen_width), 0))
                self.spyware.add(spyware)
        
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
    pygame.display.set_caption("Defend the Firewall : Malware Mayhem")
    
    # Create and run the game
    game = Game(screen)
    game.run()
