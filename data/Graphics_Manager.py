import pygame
import data.Cloud as Cloud
from data.Game_Manager import Game_Manager

#Assign different const colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
VIOLET = (128, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, VIOLET]

#const list of game arts
GAME_ART = ["resources/images/mainmenu.png", "resources/images/Tutorial.png", "resources/images/background.png", "resources/images/Nosturi.png", "resources/images/koukku.png", "resources/images/game_over.png"]

class Graphics_Manager():
    """Class that manages all the graphics drawing of the game."""
    def __init__(self, screen_width, screen_height, game_manager: Game_Manager) -> None:
        self.__screen = pygame.display.set_mode((screen_width, screen_height))
        self.__blocks = pygame.sprite.Group()
        self.__game_manager = game_manager
        self.__art = GAME_ART
        self.__clouds_front = pygame.sprite.Group()
        self.__clouds_behind = pygame.sprite.Group()
        self.__background_image_y_pos = -1145

    #Draws the background image.
    def __draw_background(self):
        background_image = pygame.image.load(self.__art[2])
        self.__screen.blit(background_image, (0, self.__background_image_y_pos))

    #Draws the crane and hook images. If blocks have been spawned, hook image x-position = current block x-position.
    def __draw_crane(self):
        crane_image = pygame.image.load(self.__art[3])
        hook_image = pygame.image.load(self.__art[4])
        self.__screen.blit(crane_image, (0,0))
        if len(self.__blocks.sprites()) > 0:
            self.__screen.blit(hook_image, (self.__blocks.sprites()[-1].rect.x, 30))
    
    #Syncs blocks in sprite.Group() with Game_Manager blocks[], if they have different amount of items.
    def __sync_blocks_with_game_manager(self):
        if len(self.__blocks.sprites()) != len(self.__game_manager.get_blocks()):
            self.__blocks.empty()
            for block in self.__game_manager.get_blocks():
                self.__blocks.add(block)

    #This function handles the blocks collision, spawning, list syncing, moving and drawing.
    def __draw_blocks(self):
        #Check if block sprites are colliding.
        self.__game_manager.check_block_collision()
        #Check if need to spawn new block.
        self.__game_manager.check_if_new_block_needs_to_be_spawned()
        #Sync the blocks lists.
        self.__sync_blocks_with_game_manager()
        #Call the block.update methods (= move the blocks).
        self.__blocks.update()
        #Draw the blocks.
        self.__blocks.draw(self.__screen)

    #Draw clouds from the clouds_front sprite.Group().
    def __draw_clouds_front(self):
        #If there is cloud sprites in the group:
        if len(self.__clouds_front.sprites()) > 0:
            #Draw the sprites on screen.
            self.__clouds_front.draw(self.__screen)
            #Call cloud.update() functions. (Cloud.update() = Move and after past left edge of screen remove.) 
            self.__clouds_front.update()
        #If there is not any cloud sprites in the group to be drawn:
        else:
            #Assign a cloud generator, using Cloud modules cloud_generator function.
            cloud_generator = Cloud.cloud_generator(3,3)
            #Go through all the yielded Clouds and add them in the sprite.Group()
            for cloud in cloud_generator:
                self.__clouds_front.add(cloud)

    #Same functionality as __draw_clouds_front. Reason for duplicate function is to be able to draw different set of clouds on z-axis.
    def __draw_clouds_behind(self):
        if len(self.__clouds_behind.sprites()) > 0:
            self.__clouds_behind.draw(self.__screen)
            self.__clouds_behind.update()
        else:
            cloud_generator = Cloud.cloud_generator(3,2)
            for cloud in cloud_generator:
                self.__clouds_behind.add(cloud)

    #Draw the menu image and call reset()
    def __draw_menu(self):
        self.__reset()
        image = pygame.image.load(self.__art[0])
        self.__screen.blit(image, (0,0))

    #Draw the tutorial image on screen.
    def __draw_tutorial(self):
        image = pygame.image.load(self.__art[1])
        self.__screen.blit(image, (0,0))

    #Draw the game scene layer by layer in correct z-axis order.
    def __draw_game(self):
        self.__draw_background()
        self.__draw_clouds_behind()
        self.__draw_crane()
        self.__draw_blocks()
        self.__draw_clouds_front()
        self.__draw_score()
        self.__screen_scroll()

    #Draw lose image on screen.
    def __draw_lose(self):
        self.__draw_game()
        image = pygame.image.load(self.__art[5])
        self.__screen.blit(image, (self.__screen.get_width()/2 - image.get_width()/2, self.__screen.get_height()/2 - image.get_height()/2))

    #Draw score background rectangle, and draw text on the screen using draw_text() function.
    def __draw_score(self):
        pygame.draw.rect(self.__screen, (GRAY), (self.__screen.get_width()/2-240, 0, self.__screen.get_width(), 20))
        self.__draw_text(f"Score: {self.__game_manager.score}", 10, (self.__screen.get_width()/2, 10))
    
    #Draw scene depending on the current game state
    def draw_scene(self):
        if self.__game_manager.game_state == "MENU":
            self.__screen.fill(BLACK)
            self.__draw_menu()
        elif self.__game_manager.game_state == "TUTORIAL":
            self.__draw_tutorial()
        elif self.__game_manager.game_state == "GAME":
            self.__screen.fill(BLACK)
            self.__draw_game()  
        elif self.__game_manager.game_state == "LOSE":
            self.__draw_lose()
        pygame.display.flip()
    
    #Function draws text.
    def __draw_text(self, text_to_draw: str, font_size: int, pos: tuple):
        font = pygame.font.SysFont('arialblack', font_size)
        text = font.render(text_to_draw, True, WHITE)
        textRect = text.get_rect()
        textRect.center = (pos)
        self.__screen.blit(text, textRect)

    #Move blocks, clouds and background on the y-axis after over 5 blocks spawned and the most top block on the stack is past half of the screen. 
    #This is to create illusion of camera moving up when block tower getting higher.
    def __screen_scroll(self):
        if self.__game_manager.game_state == "GAME":
            if len(self.__blocks.sprites()) > 5 and self.__blocks.sprites()[-2].rect.y <= self.__screen.get_height()/2:
                    for block in self.__blocks.sprites():
                        if not block.falling and not block.moving_horizontal:
                            block.rect.y = block.rect.y + 50
                    #After background has been moved enough, no need to move it anymore.
                    if self.__background_image_y_pos < -800:
                        self.__background_image_y_pos += 50
                    if len(self.__clouds_front.sprites()) > 0:
                        for cloud in self.__clouds_front.sprites():
                            cloud.rect.y += 50  
            #Keep drawing only max 10 blocks. When there is over 10 blocks, call remove_first_block_not_visible_for_memory_saving() function.     
            if len(self.__blocks.sprites()) > 10:
                self.__game_manager.remove_first_block_not_visible_for_memory_saving()
    
    #Resets the position of background image and removes clouds so the game has fresh looking start.
    def __reset(self):
        self.__background_image_y_pos = -1145
        self.__clouds_front.empty()
    
