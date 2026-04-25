from turtle import Turtle, Screen
from src import Config, BrickManager, Player

class GameView:

    def __init__(self):
        """
        Constructor for the GameView class and its attributes. Initializes the Turtle
        Screen() and separate Turtle() instances for different UI elements.
        """
        self.window = Screen()

        self.border_pen = Turtle()
        self.border_pen.hideturtle()
        self.border_pen.speed(0)

        self.brick_pen = Turtle(shape="square")
        self.brick_pen.hideturtle()

        self.text_pen = Turtle()
        self.text_pen.hideturtle()
        self.text_pen.penup()
        self.text_pen.color(Config.Text.REG_FONT_COL)


    def window_setup(self) -> None:
        """
        Sets up the main window's dimension, app title, background color, and calls
        draw_border() to draw the border on the screen.
        """
        self.window.setup(
            width=Config.Screen.WIDTH,
            height=Config.Screen.HEIGHT
        )
        self.window.getcanvas().config(highlightthickness=0)
        self.window.bgcolor(Config.Screen.BG_COLOR)
        self.window.title(Config.Screen.TITLE)
        self.window.tracer(0)
        self.draw_border(*Config.Screen.BORDER_DIM)


    def update_window(self) -> None:
        """
        Helper function to call Turtle's screen.update() method
        """
        self.window.update()


    def hold_window(self) -> None:
        """
        Helper function to call Turtle's screen.mainloop() method
        """
        self.window.mainloop()


    def draw_border(self, x1: int, y1: int, x2: int, y2: int) -> None:
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
        self.border_pen.pensize(Config.Screen.BORDER_THICKNESS)
        self.border_pen.pencolor(Config.Screen.BORDER_COL)

        self.border_pen.penup()
        self.border_pen.goto(x1, y1)

        self.border_pen.pendown()
        self.border_pen.goto(x2, y1)
        self.border_pen.goto(x2, y2)
        self.border_pen.goto(x1, y2)
        self.border_pen.goto(x1, y1)


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

        self.brick_pen.shapesize(*Config.Bricks.SHAPESIZE)

        for brick in brick_manager.bricks:
            if not brick.is_destroyed:
                self.brick_pen.goto(brick.x, brick.y)
                self.brick_pen.color(brick.color)
                self.brick_pen.stamp()


    def draw_hud(self, player: 'Player') -> None:
        """
        Draws the Score and Lives on the screen.

        Args:
            player (Player): The player object containing the score and lives.

        """
        self.text_pen.clear()

        # Draw Score
        self.text_pen.goto(*Config.Text.SCORE_POS)
        self.text_pen.write(
            arg=f"{Config.Text.SCORE_TXT} {player.score}",
            move=False,
            align='left',
            font=Config.Text.REG_FONT
        )

        # Draw Lives
        self.text_pen.goto(*Config.Text.LIVES_POS)
        self.text_pen.write(
            arg=f"{Config.Text.LIVES_TXT} {player.lives}",
            move=False,
            align='right',
            font=Config.Text.REG_FONT
        )

    def show_game_over(self) -> None:
        """
        Draws the final game over text. Called once by the Controller when game is over.
        """
        self.text_pen.goto(*Config.Text.GAME_OVER_POS)
        self.text_pen.write(
            arg=Config.Text.GAME_OVER_TXT,
            move=False,
            align='center',
            font=Config.Text.REG_FONT
        )