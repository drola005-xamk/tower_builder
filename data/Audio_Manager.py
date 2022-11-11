from pygame import mixer

SOUND_FILES = ["resources/music/8bit Bossa.mp3", "resources/sounds/vgmenuhighlight.wav", "resources/sounds/vgmenuselect.wav"]

class Audio_Manager():
    """Class that manages audio in the game."""
    def __init__(self) -> None:
        self.__sound_files = SOUND_FILES

    def background_music(self):
        mixer.music.load(self.__sound_files[0])
        mixer.music.play(-1)

    def continue_sound(self):
        sound = mixer.Sound(self.__sound_files[1])
        sound.play()

    def collision_sound(self):
        sound = mixer.Sound(self.__sound_files[1])
        sound.play()
    
    def perfect_collision_sound(self):
        sound = mixer.Sound(self.__sound_files[2])
        sound.play()

