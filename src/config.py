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

@dataclass(frozen=True)
class Paddle:
    SHAPESIZE: tuple = (0.60, 6)
    BASESIZE: int = 20
    COLOR: str = "#916BBF"
    INIT_POS: tuple[int, int] = (0, -280)

@dataclass(frozen=True)
class Ball:
    LIVES: int = 3
    COLOR: str = "white"
    SHAPESIZE: tuple = (0.80, 0.80)  # (stretch_wid, stretch_len) scale factor of 20
    BASESIZE: int = 20
    SPEED: int = 5

@dataclass
class Config:
    Screen: Screen = Screen()
    HUD: HUD = HUD()
    Bricks: Bricks = Bricks()
    Paddle: Paddle = Paddle()
    Ball: Ball = Ball()
