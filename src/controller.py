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
            if not self._check_bricks_collision():
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


    def _check_bricks_collision(self) -> bool:
        """
        Detects collisions between the ball and bricks using the Slab Method (CCD).

        Iterates through active bricks to calculate ray cast intersections,
        preventing high-speed tunneling. Returns True if a collision was resolved.
        """
        if not self.ball.in_play:
            return False

        r = Config.Ball.radius()

        ball_start_pos = (self.ball.x, self.ball.y)
        ball_velocity = (self.ball.x_move, self.ball.y_move)

        if ball_velocity[0] == 0 and ball_velocity[1] == 0:
            return False

        first_collision: dict[str, float | str | None] = {
            "time": 1.0,
            "brick": None,
            "type": None
        }

        for brick in self.bricks.bricks:
            if brick.is_destroyed:
                continue

            west_side = brick.x - Config.Bricks.half_width() - r
            south_side = brick.y - Config.Bricks.half_height() - r
            east_side = brick.x + Config.Bricks.half_width() + r
            north_side = brick.y + Config.Bricks.half_height() + r

            if ball_velocity[0] == 0:
                if west_side <= ball_start_pos[0] <= east_side:
                    stx, ltx = -math.inf, math.inf
                else:
                    continue
            else:
                time_to_hit_west = (west_side - ball_start_pos[0]) / ball_velocity[0]
                time_to_hit_east = (east_side - ball_start_pos[0]) / ball_velocity[0]
                stx = min(time_to_hit_west, time_to_hit_east)
                ltx = max(time_to_hit_west, time_to_hit_east)

            if ball_velocity[1] == 0:

                if south_side <= ball_start_pos[1] <= north_side:
                    sty, lty = -math.inf, math.inf
                else:
                    continue
            else:
                time_to_hit_south = (south_side - ball_start_pos[1]) / ball_velocity[1]
                time_to_hit_north = (north_side - ball_start_pos[1]) / ball_velocity[1]
                sty = min(time_to_hit_south, time_to_hit_north)
                lty = max(time_to_hit_south, time_to_hit_north)

            t_hit = max(stx, sty)
            t_exit = min(ltx, lty)

            if t_hit < t_exit and 0 < t_hit < first_collision["time"]:
                first_collision["time"] = t_hit
                first_collision["brick"] = brick
                first_collision["type"] = "x" if stx > sty else "y"

        # --- COLLISION RESOLUTION ---
        hit_brick = first_collision["brick"]

        if hit_brick is not None:
            time = first_collision["time"]

            # 1. Move ball to exact point of impact
            self.ball.x = ball_start_pos[0] + (ball_velocity[0] * time)
            self.ball.y = ball_start_pos[1] + (ball_velocity[1] * time)

            # 2. Apply Bounce
            if first_collision["type"] == "x":
                self.ball.bounce_x()
            else:
                self.ball.bounce_y()

            # 3. Calculate remaining movement after the bounce
            remaining_time = 1.0 - time
            self.ball.x += self.ball.x_move * remaining_time
            self.ball.y += self.ball.y_move * remaining_time

            # 4. State Update
            hit_brick.is_destroyed = True
            self.player.one_point()

            # 5. Event-Driven Renders
            self.view.draw_bricks(self.bricks)
            self.view.draw_hud(self.player)

            return True

        return False
