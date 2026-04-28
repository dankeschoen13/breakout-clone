from src import GameView, BrickManager, Player, Ball, Paddle, Rules, Config, Brick, SoundManager
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
        self.audio = SoundManager()
        self.bricks = BrickManager()
        self.player = Player()
        self.paddle = Paddle(*Config.Paddle.INIT_POS)
        self.ball = Ball(*Config.Ball.init_pos())


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

            if self.ball.x < Config.Ball.X_BOUNDS[0]:
                self.ball.x = Config.Ball.X_BOUNDS[0]
                self.ball.bounce_x()
                self.audio.play_wall()

            elif self.ball.x > Config.Ball.X_BOUNDS[1]:
                self.ball.x = Config.Ball.X_BOUNDS[1]
                self.ball.bounce_x()
                self.audio.play_wall()

            if self.ball.y > Config.Ball.Y_BOUNDS[1]:
                self.ball.y = Config.Ball.Y_BOUNDS[1]
                self.ball.bounce_y()

            self._check_paddle_collision()
        else:
            self.ball.x = self.paddle.x

        self.view.render_paddle(self.paddle)
        self.view.render_ball(self.ball)
        self.view.update_window()
        self.view.refresh_window(self._game_loop, Config.Screen.FPS)


    def _bind_keys(self) -> None:
        """
        Hooks up the physical keyboard to the Paddle Model's state,
        """
        self.view.window.listen()
        self.view.window.onkeypress(self.paddle.press_left, "Left")
        self.view.window.onkeyrelease(self.paddle.release_left, "Left")
        self.view.window.onkeypress(self.paddle.press_right, "Right")
        self.view.window.onkeyrelease(self.paddle.release_right, "Right")
        self.view.window.onkeypress(self._launch_ball, "space")

    def _launch_ball(self) -> None:
        """
        Controller logic to launch the ball if it isn't already in play.
        """
        if not self.ball.in_play:
            self.ball.in_play = True
            self._apply_deflection(speed=Config.Ball.SPEED)

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

        *Added in line comments to explain logic
        """
        if not self.ball.in_play:
            return False

        r = Config.Ball.radius()

        # Initializing current state of the game in this frame
        ball_current_pos = (self.ball.x, self.ball.y)
        ball_velocity = (self.ball.x_move, self.ball.y_move)

        if ball_velocity[0] == 0 and ball_velocity[1] == 0:
            return False

        hit_time = 1.0
        hit_brick: 'Brick | None' = None
        hit_axis: str | None = None

        # --- COLLISION MONITORING ---
        for brick in self.bricks.bricks: # iterates through each bricks

            if brick.is_destroyed:
                continue

            # 1. calculate the brick's edges with ball as radius buffer
            # which will then form the slab model for that brick

            # current brick's coordinates
            west_side = brick.x - Config.Bricks.half_width() - r
            south_side = brick.y - Config.Bricks.half_height() - r
            east_side = brick.x + Config.Bricks.half_width() + r
            north_side = brick.y + Config.Bricks.half_height() + r

            # LEGEND:
            # stx = the shortest time to hit an x side of the block (up or down/north or south)
            # ltx = the longest time to hit an x side of the block
            # sty = the shortest time to hit a y side of the block (left or right/west or east)
            # lty = the longest time to hit a y side of the block

            # 2. Figure out the time to hit the brick's left and right slab/coordinates
            if ball_velocity[0] == 0:
                # if ball movement is completely vertical set time to hit brick's x-cor slab as
                # infinity (will never hit)
                if west_side <= ball_current_pos[0] <= east_side:
                    # negative infinity for the shortest time and positive infinity for longest time
                    stx, ltx = -math.inf, math.inf
                else:
                    # bugfix: skip to next brick if a ball is not under the current brick
                    continue

            else:
                # if ball movement is diagonal, calculate the trajectory based on brick's coordinates and ball distance
                time_to_hit_west = (west_side - ball_current_pos[0]) / ball_velocity[0]
                time_to_hit_east = (east_side - ball_current_pos[0]) / ball_velocity[0]
                stx = min(time_to_hit_west, time_to_hit_east)
                ltx = max(time_to_hit_west, time_to_hit_east)

            # 3. Figure out the time to hit the brick's bottom and top slab/coordinates
            if ball_velocity[1] == 0:
                # if ball movement is completely horizontal, set time to hit brick's y-cor slab as
                # infinity (will never hit)
                if south_side <= ball_current_pos[1] <= north_side:
                    # negative infinity for the shortest time and positive infinity for longest time
                    sty, lty = -math.inf, math.inf
                else:
                    # bugfix: skip to next brick if a ball is not next to the current brick
                    continue

            else:
                # if ball movement is diagonal, calculate the trajectory based on brick's coordinates and ball distance
                time_to_hit_south = (south_side - ball_current_pos[1]) / ball_velocity[1]
                time_to_hit_north = (north_side - ball_current_pos[1]) / ball_velocity[1]
                sty = min(time_to_hit_south, time_to_hit_north)
                lty = max(time_to_hit_south, time_to_hit_north)

            # 4. Obtain the calculated hit and exit values
            t_hit = max(stx, sty)
            t_exit = min(ltx, lty)

            # 5. Check if the hit is valid. A valid hit must happen before calculated exits
            # and within the current frame.
            if t_hit < t_exit and 0 < t_hit < hit_time:
                print(f"Time of hit:{t_hit}. Chosen from STX:{stx} STY:{sty}")
                print(f"Time to exit:{t_exit}. Chosen fro LTX:{ltx} LTY:{lty}")
                hit_time = t_hit
                hit_brick = brick
                hit_axis = "x" if stx > sty else "y"

        # 6. Resolve the brick hit
        if hit_brick is not None and hit_axis is not None:
            self._resolve_brick_hit(
                hit_brick=hit_brick,
                hit_time=hit_time,
                hit_axis=hit_axis
            )
            return True

        return False

    def _resolve_brick_hit(self, hit_brick: Brick, hit_time: float, hit_axis: str) -> None:
        """
        Handles the physics resolution and state updates when a brick is hit.
        """
        self.ball.x += self.ball.x_move * hit_time
        self.ball.y += self.ball.y_move * hit_time

        if hit_axis == "x":
            self.ball.bounce_x()
        else:
            self.ball.bounce_y()

        remaining_time = 1.0 - hit_time
        self.ball.x += self.ball.x_move * remaining_time
        self.ball.y += self.ball.y_move * remaining_time

        hit_brick.is_destroyed = True

        self.audio.play_brick()
        self.player.one_point()

        self.view.draw_bricks(self.bricks)
        self.view.draw_hud(self.player)

    def _check_paddle_collision(self) -> None:
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
            self.audio.play_paddle()

        elif self.ball.y < Config.Screen.BORDER_DIM[1] + Config.Ball.radius():
            self.ball.reset_position(*Config.Ball.init_pos())
            self.player.ball_dies()
            self.view.draw_hud(self.player)
