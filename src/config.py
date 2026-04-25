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

@dataclass
class Config:
    Screen: Screen = Screen()
    Bricks: Bricks = Bricks()