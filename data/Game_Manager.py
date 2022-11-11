import pygame
import data.Block as Block
import random
import data.Audio_Manager as Audio_Manager

GAME_STATES = ["MENU", "GAME", "LOSE", "TUTORIAL"]

class Game_Manager():
    """Class that manages all the logic of the game."""

    def __init__(self) -> None:
        pygame.init()
        self.__game_state = GAME_STATES[0]
        self.__blocks = []
        self.__current_block = None
        self.__total_blocks_spawned = 0
        self.__pygame_clock = pygame.time.Clock()
        self.__score = 0
        self.__audio_manager = None

    #Function that handles events for player controls. Called from main game loop.
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.__game_state == "MENU":
                    self.__tutorial()
                    self.__audio_manager.continue_sound()
                elif self.__game_state == "TUTORIAL":
                    self.__start_game()
                    self.__audio_manager.continue_sound()
                elif self.__game_state == "GAME":
                    self.__current_block.drop()
                    self.__audio_manager.continue_sound()
                elif self.__game_state == "LOSE":
                    self.__main_menu()
                    self.__audio_manager.continue_sound()

    #Spawns a new block, increases total_blocks_spawned by 1, and adds the block to blocks list.
    def __spawn_block(self):
        self.__total_blocks_spawned += 1
        self.__current_block = Block.Block((random.randint(25, 430), 80), self.__randomize_block_direction_and_increase_speed())
        self.__blocks.append(self.__current_block)

    #Randomizes the direction of block movement when spawned, and increases block speed depending on how many blocks have been totally spawned.
    def __randomize_block_direction_and_increase_speed(self):
        starting_direction = random.choice([-1, 1])
        return (3 + self.__total_blocks_spawned / 2) * starting_direction
    
    #Removes block at index 0 from the blocks list, so the game doesn't do unnecessary draws for blocks that are no more visible (= out of screen). This function is called from the Graphics_Manager.
    def remove_first_block_not_visible_for_memory_saving(self):
        if self.__blocks[0] != None:
            self.__blocks.pop(0)
    
    #Spawns new block if current block is None, or if last dropped block has stopped moving.
    def check_if_new_block_needs_to_be_spawned(self):
        if self.__current_block == None:
            self.__spawn_block()
        if not self.__current_block.moving_horizontal and not self.__current_block.falling:
            self.__spawn_block()
    
    #After first block dropped, check if blocks are colliding. 
    def check_block_collision(self):
        if len(self.__blocks) > 1:
            if self.__current_block.falling:
                if self.__current_block.is_colliding(self.__blocks[-2]):
                    #If colliding, update score.
                    self.__update_score()
                    #If colliding, but three_bad_alignments_in_row() == True, lose game.
                    if self.__three_bad_alignments_in_row():
                        self.__lose_game()
            #If first has been dropped, but a block after that doesnt collide with the block before itself (=missed block), lose game.
            elif self.__current_block.is_colliding(self.__blocks[-2]) == False and self.__current_block.falling == False and self.__current_block.moving_horizontal == False:         
                self.__lose_game()
    
    #Update the score by adding return value of calculate_score() to score.
    def __update_score(self):
        self.__score += self.__calculate_score()
    
    #Calculate the condition of the alignment using the difference of block x-axis position. Depending on the difference, call block.change_block_art() and return score amount.
    def __calculate_score(self):
        if len(self.__blocks) > 1:
            new_block_pos = self.__blocks[-1].rect.x
            old_block_pos = self.__blocks[-2].rect.x
            pos_difference = abs(new_block_pos - old_block_pos)
            if pos_difference == 0:
                self.__current_block.change_block_art("PERFECT")
                return 10
            elif pos_difference < 15:
                self.__current_block.change_block_art("GOOD")
                return 5
            elif pos_difference < 30:
                self.__current_block.change_block_art("FAIR")
                return 1
            elif pos_difference < 50:
                self.__current_block.change_block_art("BAD")
                return 0
        else:
            return 0

    #Check if 3 last three block alignments has been "BAD", return bool. (This simulates block tower falling without physics modeling!) 
    def __three_bad_alignments_in_row(self):
        bad_blocks_count = 0
        if len(self.__blocks) >= 3:
            last_three_blocks = self.__blocks[-3:]
            for block in last_three_blocks:
                if block.bad_alignment:
                    bad_blocks_count += 1      
        return bad_blocks_count >= 3  

    #Change game state to "MENU"     
    def __main_menu(self):
        self.__game_state = GAME_STATES[0]

    #Change game state to "TUTORIAL"  
    def __tutorial(self):
        self.__game_state = GAME_STATES[3]

    #Change game state to "GAME" 
    def __start_game(self):
        self.__reset()
        self.__spawn_block()
        self.__game_state = GAME_STATES[1]

    #Change game state to "LOSE"
    def __lose_game(self):
        self.__game_state = GAME_STATES[2]

    #Empty the blocks list, reset the total_blocks_spawned and score to 0, so every times starting new game its fresh.
    def __reset(self):
        self.__blocks = []
        self.__total_blocks_spawned = 0
        self.__score = 0

    #Getter function for the blocks list. Called at Graphics_Manager.
    def get_blocks(self):
        return self.__blocks

    #Setter for the Audio_Manager. Called at main on launch.
    def set_audio_manager(self, audio_manager: Audio_Manager.Audio_Manager):
        self.__audio_manager = audio_manager

    #Returns reference to pygame_clock.
    @property
    def clock(self):
        return self.__pygame_clock

    #Returns reference to current game_state.
    @property
    def game_state(self):
        return self.__game_state

    #Returns reference to score.
    @property
    def score(self):
        return self.__score
