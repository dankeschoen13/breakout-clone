import os, sys, pygame

class SoundManager:

    def __init__(self) -> None:

        pygame.mixer.init(buffer=512)

        try:
            self.sfx_paddle = pygame.mixer.Sound(get_resource_path(os.path.join("assets", "paddle_hit.wav")))
            self.sfx_wall = pygame.mixer.Sound(get_resource_path(os.path.join("assets", "wall_hit.wav")))
            self.sfx_brick = pygame.mixer.Sound(get_resource_path(os.path.join("assets", "brick_hit.wav")))

            self.sfx_paddle.set_volume(0.5)
            self.sfx_wall.set_volume(0.4)
            self.sfx_brick.set_volume(0.7)
            self.audio_enabled = True

        except FileNotFoundError:
            print("WARNING: Audio assets not found. Running in silent mode.")
            self.audio_enabled = False

    def play_paddle(self) -> None:
        if self.audio_enabled:
            self.sfx_paddle.play()

    def play_wall(self) -> None:
        if self.audio_enabled:
            self.sfx_wall.play()

    def play_brick(self) -> None:
        if self.audio_enabled:
            self.sfx_brick.play()


def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to a resource.
    Works for standard development AND packaged PyInstaller executables.
    """
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = str(os.path.dirname(current_dir))

    return os.path.join(base_path, relative_path)
