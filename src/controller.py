from src import GameView

class GameController:
    def __init__(self):
        self.view = GameView()

    def run(self):
        game_is_on = True
        self.view.window_setup()

        while game_is_on:
            self.view.update_window()

        self.view.hold_window()
