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
            self._apply_deflection(speed=Config.Ball.SPEED)

    def check_paddle_collision(self) -> None:
        """
        Detects paddle strikes and calculates the dynamic return trajectory.

        - Detects collision only when all conditions are true:
            1. Ball enters small collision zone between paddle and ball starting position
                    ( paddle < ball < ball starting position )
            2. Ball is inside the paddle length
                    ( paddle left edge < ball < paddle right edge )
            3. Ball is moving downwards (-y)
        - Otherwise:
            1. Reset ball position.
        """
        paddle_half = Config.Paddle.half_width()

        if (self.paddle.y < self.ball.y < Rules.ball_start_y() and
            self.paddle.x - paddle_half < self.ball.x < self.paddle.x + paddle_half and
            self.ball.y_move < 0):

            self.ball.bounce_y()
            current_speed = math.hypot(self.ball.x_move, self.ball.y_move)
            self._apply_deflection(speed=current_speed)

        elif self.ball.y < Config.Screen.BORDER_DIM[1] + Config.Ball.radius():
            self.ball.reset_position(*Config.Ball.init_pos())
            self.player.ball_dies()
            self.view.draw_hud(self.player)


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

            if self.ball.x > 265:
                self.ball.x = 265
                self.ball.bounce_x()

            elif self.ball.x < -265:
                self.ball.x = -265
                self.ball.bounce_x()

            if self.ball.y > 275:
                self.ball.y = 275
                self.ball.bounce_y()

            self.check_paddle_collision()

        else:
            self.ball.x = self.paddle.x

        self.view.draw_paddle(self.paddle)
        self.view.draw_ball(self.ball)
        self.view.update_window()
        self.view.refresh_window(self._game_loop, Config.Screen.FPS)


    def _apply_deflection(self, speed: float) -> None:
        """
        IMPORTANT: Deflection logic
            1. Bounces normally by reversing y-axis movement (bounce_y)
            2. Calculates velocity based on current x and y value upon hit (math.hypot)
            3. Redistributes the velocity by calculating ratio of distribution for horizontal movement based on:
                a. where the ball hits the paddle
                b. direction of the paddle (adds fixed amount of influence)
            4. Clamps the value so x movement doesn't take the entire speed allocation, preventing y=0 situations.
            5. Assigns the y-axis velocity based on speed not allocated to x
        """
        paddle_half = Config.Paddle.half_width()

        ratio = (self.ball.x - self.paddle.x) / paddle_half

        if self.paddle.is_moving_right:
            ratio += Config.Physics.PADDLE_PUSH
        elif self.paddle.is_moving_left:
            ratio -= Config.Physics.PADDLE_PUSH

        ratio = max(-Config.Physics.MAX_RATIO, min(ratio, Config.Physics.MAX_RATIO))

        self.ball.x_move = ratio * speed
        y_magnitude = math.sqrt(max(speed ** 2 - self.ball.x_move ** 2, 0))

        current_y_sign = self.ball.y_move if self.ball.y_move != 0 else 1.0
        self.ball.y_move = math.copysign(y_magnitude, current_y_sign)
