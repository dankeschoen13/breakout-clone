from turtle import Turtle, Screen
from src import Config

class GameView:

    def __init__(self):
        self.window = Screen()
        self.border_pen = Turtle()
        self.border_pen.hideturtle()
        self.border_pen.speed(0)

    def draw_border(self, x1, y1, x2, y2):
        self.border_pen.pensize(Config.Screen.BORDER_THICKNESS)
        self.border_pen.pencolor(Config.Screen.BORDER_COL)

        self.border_pen.penup()
        self.border_pen.goto(x1, y1)

        self.border_pen.pendown()
        self.border_pen.goto(x2, y1)
        self.border_pen.goto(x2, y2)
        self.border_pen.goto(x1, y2)
        self.border_pen.goto(x1, y1)

    def window_setup(self):
        self.window.setup(
            width=Config.Screen.WIDTH,
            height=Config.Screen.HEIGHT
        )
        self.window.getcanvas().config(highlightthickness=0)
        self.window.bgcolor(Config.Screen.BG_COLOR)
        self.window.title(Config.Screen.TITLE)
        self.window.tracer(0)
        self.draw_border(*Config.Screen.BORDER_DIM)

    def update_window(self):
        self.window.update()

    def hold_window(self):
        self.window.mainloop()


