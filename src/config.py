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
class Bricks:
    CELL_WIDTH: int = 80
    COLORS: tuple[str, ...] = ("red", "orange", "yellow", "green", "blue")
    X_BOUNDS: tuple = (-280, 280)
    Y_BOUNDS: tuple = (280, 0)
    ROW_SPACING: int = 25
    SHAPESIZE: tuple = (0.75, 3.50, 0)


@dataclass(frozen=True)
class Text:
    REG_FONT: tuple[str, int, str] = ("Helvetica", 16, "normal")
    REG_FONT_COL: str = "white"
    SCORE_TXT: str = "SCORE: "
    SCORE_POS: tuple = (-270, 310)
    LIVES: int = 3
    LIVES_TXT: str = "LIVES: "
    LIVES_POS: tuple = (270, 310)
    GAME_OVER_TXT: str = "GAME OVER!"
    GAME_OVER_POS: tuple = (-5, 0)


@dataclass
class Config:
    Screen: Screen = Screen()
    Bricks: Bricks = Bricks()
    Text: Text = Text()