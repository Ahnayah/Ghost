import pygame, sys
from Player import Player

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Initialize player at the center of the screen
        player_sprite = Player((self.screen_width / 2, self.screen_height / 2))
        self.player = pygame.sprite.GroupSingle(player_sprite)
    
    image = pygame.image.load("assets/background.png")
    def draw_background(self):
        """Blit the background image to the screen."""
        size = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
        self.screen.blit(size, (0, 0))

    def draw(self):
        """Render everything to the screen."""
        self.draw_background()
        
        self.player.sprite.arrows.draw(self.screen)    
        self.player.draw(self.screen)
        pygame.display.update()
        
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.player.update()   


    def draw(self):
        """Render everything to the screen."""
        self.draw_background()  
        self.player.sprite.arrows.draw(self.screen)      
        self.player.draw(self.screen)
        pygame.display.update()
        
if __name__ == "__main__":
    # Pygame setup
    pygame.init()
    screen_width = 600
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Malware Mayhem")
    clock = pygame.time.Clock()
    

    # Create and run the game
    game = Game(screen, clock)
    game.run()
