from dataclasses import dataclass

@dataclass(frozen=True)
class Screen:
    WIDTH: int = 650
    HEIGHT: int = 750
    FPS: int = 60
    BG_COLOR: str = "#03001C"
    TITLE: str = "Breakout!"
    BORDER_DIM: tuple[int, int, int, int] = (-280, -325, 280, 293)
    BORDER_COL: str = "#787A91"
    BORDER_THICKNESS: int = 2

@dataclass(frozen=True)
class HUD:
    REG_FONT: tuple[str, int, str] = ("Helvetica", 16, "normal")
    REG_FONT_COL: str = "white"
    SCORE_TXT: str = "SCORE: "
    SCORE_POS: tuple = (-270, 310)
    LIVES_TXT: str = "LIVES: "
    LIVES_POS: tuple = (270, 310)
    GAME_OVER_TXT: str = "GAME OVER!"
    GAME_OVER_POS: tuple = (-5, 0)

@dataclass(frozen=True)
class Bricks:
    CELL_WIDTH: int = 80
    COLORS: tuple[str, ...] = ("red", "orange", "yellow", "green", "blue")
    X_BOUNDS: tuple = (-280, 280)
    Y_BOUNDS: tuple = (280, 0)
    ROW_SPACING: int = 25
    SHAPESIZE: tuple = (0.75, 3.50, 0)
    BASESIZE: int = 20

    @classmethod
    def width(cls) -> float:
        return cls.SHAPESIZE[1] * cls.BASESIZE

    @classmethod
    def half_width(cls) -> float:
        return cls.width() / 2

    @classmethod
    def height(cls) -> float:
        return cls.SHAPESIZE[0] * cls.BASESIZE

    @classmethod
    def half_height(cls) -> float:
        return cls.height() / 2

@dataclass(frozen=True)
class Paddle:
    SPEED: int = 5
    SHAPESIZE: tuple = (0.60, 6)
    BASESIZE: int = 20
    COLOR: str = "#916BBF"
    INIT_POS: tuple[int, int] = (0, -280)

    @classmethod
    def width(cls) -> float:
        return cls.SHAPESIZE[1] * cls.BASESIZE

    @classmethod
    def half_width(cls) -> float:
        return cls.width() / 2

    @classmethod
    def height(cls) -> float:
        return cls.SHAPESIZE[0] * cls.BASESIZE

    @classmethod
    def half_height(cls) -> float:
        return cls.height() / 2

@dataclass(frozen=True)
class Ball:
    LIVES: int = 3
    COLOR: str = "white"
    SHAPESIZE: tuple = (0.80, 0.80)  # (stretch_wid, stretch_len) scale factor of 20
    BASESIZE: int = 20
    X_BOUNDS: tuple = (-265, 265)
    Y_BOUNDS: tuple = (-275, 275)
    SPEED: int = 5

    @classmethod
    def diameter(cls) -> float:
        return cls.SHAPESIZE[0] * cls.BASESIZE

    @classmethod
    def radius(cls) -> float:
        return cls.diameter() / 2

    @classmethod
    def init_pos(cls) -> tuple[float, float]:
        return Paddle.INIT_POS[0], Rules.ball_start_y()

@dataclass(frozen=True)
class Physics:
    MAX_RATIO: float = 0.95
    PADDLE_PUSH: float = 0.25

@dataclass
class Config:
    Screen: Screen = Screen()
    HUD: HUD = HUD()
    Bricks: Bricks = Bricks()
    Paddle: Paddle = Paddle()
    Ball: Ball = Ball()
    Physics: Physics = Physics()

class Rules:

    @classmethod
    def paddle_x_limit(cls) -> float:
        """
        - excludes distance between border inner edge & paddle's center so paddle doesn't exceed the border
        :return: effective paddle horizontal movement limit
        """
        border_loc = abs(Config.Screen.BORDER_DIM[0])
        border_inner_edge = border_loc - Config.Screen.BORDER_THICKNESS / 2
        return border_inner_edge - Config.Paddle.half_width()

    @classmethod
    def ball_start_y(cls):
        """
        :return: the correct y-axis coordinate so the ball appears correctly on top of the paddle
        """
        paddle_top = Config.Paddle.INIT_POS[1] + Config.Paddle.half_height()
        return paddle_top + Config.Ball.radius()