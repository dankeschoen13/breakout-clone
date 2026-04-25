from src import GameView, BrickManager, Player


class GameController:
    """
    The orchestrator of the Breakout game.

    This class implements the Controller logic of the MVC pattern, mediating
    communication between the data models (BrickManager) and the user
    interface (GameView). It manages the high-level game state and the
    execution of the main game loop.
    """

    def __init__(self) -> None:
        """
        Initializes the game application and its core components.

        Sets up the primary View and Model instances required to run the game.
        """
        self.view = GameView()
        self.bricks = BrickManager()
        self.player = Player()

    def run(self) -> None:
        """
        Starts the game initialization process and enters the main loop.

        This method performs the following sequence:
        1. Triggers the initial window configuration.
        2. Renders the starting brick grid.
        3. Maintains the active game state via a continuous update loop.
        4. Invokes the window hold logic upon game termination to prevent
           automatic exit.
        """
        game_is_on = True
        self.view.draw_bricks(self.bricks)
        self.view.draw_hud(self.player)

        while game_is_on:
            self.view.update_window()

        self.view.hold_window()
