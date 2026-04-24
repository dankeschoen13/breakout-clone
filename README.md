# Breakout: Professional Edition

A modern, object-oriented clone of the classic arcade game Breakout, built entirely with Python and the built-in Turtle graphics library. This project was developed with a strong emphasis on clean software architecture, utilizing the Model-View-Controller (MVC) design pattern and modern UI principles.

## ✨ Features

* **MVC Architecture:** Strict separation of concerns between game data (Models), rendering (View), and game logic (Controller).
* **Modern Aesthetics:** Utilizes high-performance Turtle rendering (`tracer(0)`) for smooth 60 FPS gameplay, clean typography, and a modern color palette.
* **Optimized Rendering:** Uses Turtle `.stamp()` methods for the brick grid, significantly improving rendering speed and resource management compared to traditional multi-object instantiation.
* **Modular Configuration:** Centralized configuration settings for easy adjustment of game physics, screen dimensions, and UI styling.

## 🗂 Project Structure

The codebase is organized into a scalable package structure:

```text
breakout-game/
├── assets/                 # Sound effects and image assets
├── src/                    # Source code package
│   ├── __init__.py         # Exposes public API classes
│   ├── config.py           # Centralized game constants and styling
│   ├── controller.py       # Game loop, state management, and logic
│   ├── models.py           # Pure data classes (Paddle, Ball, Bricks)
│   └── view.py             # Screen setup and unified UI rendering
├── main.py                 # Application entry point
└── README.md               # Project documentation
```

## 🚀 Getting Started

### Prerequisites
* Python 3.x installed on your machine.
* Built-in `turtle` module (included with standard Python installations).

### Installation & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/breakout-game.git
   cd breakout-game
   ```

2. **Run the game:**
   ```bash
   python main.py
   ```

## 🎮 How to Play
* **Left Arrow / Right Arrow:** Move the paddle left and right.
* **Objective:** Clear all the colored bricks from the screen without letting the ball fall past your paddle. 

## 👨‍💻 Author

**Marco Bernacer**
* GitHub: [@dankeschoen13](https://github.com/dankeschoen13)
* LinkedIn: [https://www.linkedin.com/in/marcobernacer/](https://www.linkedin.com/in/marcobernacer/)

## 📄 License

This project is open-source and available under the MIT License.