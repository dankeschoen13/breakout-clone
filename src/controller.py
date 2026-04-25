from src import GameView, BrickManager, Player, Ball, Paddle, Rules, Config
import math

class GameController:
    """
    The orchestrator of the Breakout game.

    This class implements the Controller logic of the MVC pattern, mediating
    communication between the data models and the user interface. It manages
    the high-level game state and the execution of the main game loop.
    """

    def __init__(self) -> None:
        """
        Initializes the game application and its core components.

        Sets up the primary View and Model instances required to run the game.
        """
        self.view = GameView()
        self.bricks = BrickManager()
        self.player = Player()
        self.paddle = Paddle(*Config.Paddle.INIT_POS)
        self.ball = Ball(*Config.Ball.init_pos())

    def _bind_keys(self) -> None:
        """
        Hooks up the physical keyboard to the Paddle Model's state,
        """
        self.view.window.listen()
        self.view.window.onkeypress(self.paddle.press_left, "Left")
        self.view.window.onkeyrelease(self.paddle.release_left, "Left")
        self.view.window.onkeypress(self.paddle.press_right, "Right")
        self.view.window.onkeyrelease(self.paddle.release_right, "Right")
        self.view.window.onkeypress(self.launch_ball, "space")

    def launch_ball(self) -> None:
        """
        Controller logic to launch the ball if it isn't already in play.
        """
        if not self.ball.in_play:
            self.ball.in_play = True

            paddle_half = Config.Paddle.half_width()
            speed = Config.Ball.SPEED

            ratio = (self.view.ball_pen.xcor() - self.view.paddle_pen.xcor()) / paddle_half
            if self.paddle.is_moving_right:
                ratio += Config.Physics.PADDLE_PUSH
            elif self.paddle.is_moving_left:
                ratio -= Config.Physics.PADDLE_PUSH
            ratio = max(-Config.Physics.MAX_RATIO,
                        min(ratio, Config.Physics.MAX_RATIO))

            self.ball.x_move = ratio * speed
            self.ball.y_move = math.sqrt(max(speed ** 2 - self.ball.x_move ** 2, 0))


    def run(self) -> None:
        """
        Starts the game initialization process and enters the main loop.
        """
        self.view.draw_bricks(self.bricks)
        self.view.draw_hud(self.player)
        self._bind_keys()

        self._game_loop()
        self.view.hold_window()


    def _game_loop(self) -> None:
        """
        The core execution loop of the game. Runs at 60 FPS.
        """
        self.paddle.move()

        if self.ball.in_play:
            self.ball.move()
        else:
            self.ball.x = self.paddle.x

        self.view.draw_paddle(self.paddle)
        self.view.draw_ball(self.ball)

        self.view.update_window()

        self.view.refresh_window(self._game_loop, Config.Screen.FPS)
