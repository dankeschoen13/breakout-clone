from turtle import Turtle, Screen, _Screen
from src import Config, BrickManager, Player, Ball, Paddle


class GameView:

    def __init__(self):
        """
        Constructor for the GameView class and its attributes. Initializes the Turtle
        Screen() and separate Turtle() instances for different UI elements.
        """
        self.window = self._create_screen()
        self.border = self._create_border(*Config.Screen.BORDER_DIM)
        
        self.brick_pen = self._create_brick_pen()
        self.hud_pen = self._create_hud_pen()
        self.paddle_pen = self._create_paddle()
        self.ball_pen = self._create_ball()


    def update_window(self) -> None:
        """
        Helper function to call Turtle's screen.update() method
        """
        self.window.update()

    def refresh_window(self, func, fps) -> None:

        self.window.ontimer(func, int(1000 / fps))


    def hold_window(self) -> None:
        """
        Helper function to call Turtle's screen.mainloop() method
        """
        self.window.mainloop()


    def draw_hud(self, player: 'Player') -> None:
        """
        Draws the Score and Lives on the screen.

        Args:
            player (Player): The player object containing the score and lives.

        """
        self.hud_pen.clear()

        # Draw Score
        self.hud_pen.goto(*Config.HUD.SCORE_POS)
        self.hud_pen.write(
            arg=f"{Config.HUD.SCORE_TXT} {player.score}",
            move=False,
            align='left',
            font=Config.HUD.REG_FONT
        )

        # Draw Lives
        self.hud_pen.goto(*Config.HUD.LIVES_POS)
        self.hud_pen.write(
            arg=f"{Config.HUD.LIVES_TXT} {player.lives}",
            move=False,
            align='right',
            font=Config.HUD.REG_FONT
        )

        if player.lives == 0:
            self.show_game_over()


    def draw_bricks(self, brick_manager: 'BrickManager') -> None:
        """
        Renders the current state of all active bricks onto the screen.

        This method optimizes rendering by using the Turtle `.stamp()` technique
        instead of instantiating multiple objects. It skips any bricks marked
        as destroyed.

        Args:
            brick_manager (BrickManager): The data model containing the level's bricks.
        """
        self.brick_pen.clear()
        self.brick_pen.penup()

        for brick in brick_manager.bricks:
            if not brick.is_destroyed:
                self.brick_pen.goto(brick.x, brick.y)
                self.brick_pen.color(brick.color)
                self.brick_pen.stamp()


    def draw_ball(self, ball: 'Ball') -> None:
        """
        This method renders the current state of the ball.

        Args:
            ball (Ball): The data model containing the level's ball.
        """
        self.ball_pen.goto(ball.x, ball.y)


    def draw_paddle(self, paddle: 'Paddle') -> None:
        """
        This method renders the current state of the paddle.

        Args:
            paddle (Paddle): The data model containing the level's ball.
        """
        self.paddle_pen.goto(paddle.x, paddle.y)


    def show_game_over(self) -> None:
        """
        Draws the final game over text. Called once by the Controller when game is over.
        """
        self.hud_pen.goto(*Config.HUD.GAME_OVER_POS)
        self.hud_pen.write(
            arg=Config.HUD.GAME_OVER_TXT,
            move=False,
            align='center',
            font=Config.HUD.REG_FONT
        )


    @staticmethod
    def _create_screen() -> _Screen:
        """
        Sets up the main window's dimension, app title, background color, and calls
        draw_border() to draw the border on the screen.
        """
        screen = Screen()
        screen.setup(
            width=Config.Screen.WIDTH,
            height=Config.Screen.HEIGHT
        )
        screen.getcanvas().config(highlightthickness=0)
        screen.bgcolor(Config.Screen.BG_COLOR)
        screen.title(Config.Screen.TITLE)
        screen.tracer(0)
        return screen


    @staticmethod
    def _create_border(x1: int, y1: int, x2: int, y2: int) -> Turtle:
        """
        Draws a rectangular boundary on the screen using the provided coordinates.

        The method utilizes the dedicated `border_pen` to draw a continuous
        line connecting the four corners defined by the (x1, y1) and (x2, y2) bounds.

        Drawing starts in the lower left corner of the screen (x1, y1), then follows
        counter-clockwise movement until it completes a rectangular boundary.

        Args:
            x1 (int): The X-coordinate of the first corner.
            y1 (int): The Y-coordinate of the first corner.
            x2 (int): The X-coordinate of the opposite corner.
            y2 (int): The Y-coordinate of the opposite corner.
        """
        border_pen = Turtle()
        border_pen.hideturtle()
        border_pen.speed(0)
        border_pen.pensize(Config.Screen.BORDER_THICKNESS)
        border_pen.pencolor(Config.Screen.BORDER_COL)

        border_pen.penup()
        border_pen.goto(x1, y1)

        border_pen.pendown()
        border_pen.goto(x2, y1)
        border_pen.goto(x2, y2)
        border_pen.goto(x1, y2)
        border_pen.goto(x1, y1)
        return border_pen


    @staticmethod
    def _create_brick_pen() -> Turtle:
        pen = Turtle(shape="square")
        pen.hideturtle()
        pen.shapesize(*Config.Bricks.SHAPESIZE)
        return pen


    @staticmethod
    def _create_hud_pen() -> Turtle:
        pen = Turtle()
        pen.hideturtle()
        pen.penup()
        pen.color(Config.HUD.REG_FONT_COL)
        return pen


    @staticmethod
    def _create_paddle() -> Turtle:
        paddle = Turtle()
        paddle.penup()
        paddle.shape('square')
        paddle.resizemode('user')
        paddle.shapesize(*Config.Paddle.SHAPESIZE)
        paddle.color(Config.Paddle.COLOR)
        return paddle


    @staticmethod
    def _create_ball() -> Turtle:
        ball = Turtle()
        ball.penup()
        ball.shape('circle')
        ball.resizemode('user')
        ball.shapesize(*Config.Ball.SHAPESIZE)
        ball.color(Config.Ball.COLOR)
        return ball