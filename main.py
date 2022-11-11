import pygame
import data.Game_Manager as Game_Manager
import data.Graphics_Manager as Graphics_Manager
import data.Audio_Manager as Audio_Manager

game_manager = Game_Manager.Game_Manager()
graphics_manager = Graphics_Manager.Graphics_Manager(480, 640, game_manager)
audio_manager = Audio_Manager.Audio_Manager()
game_manager.set_audio_manager(audio_manager)

pygame.init()
pygame.display.set_caption(f'Tower Builder')

#Main game loop
def game():
    audio_manager.background_music()

    while True:
        for event in pygame.event.get():
            game_manager.event_handler(event)
            
            if event.type == pygame.QUIT:
                        exit()

        graphics_manager.draw_scene()
        game_manager.clock.tick(60)
        
game()