# 🎮 Roguelike Pygame Project

This is a Roguelike game project built in Python using the `pygame` module.

### 📸 Project Previews

| Gameplay 1 | Gameplay 2 |
| :---: | :---: |
| ![Gameplay 1](assets/photo.png) | ![Gameplay 2](assets/photo3.png) |

**The story behind the project:**
It all started with the idea of making a farming game like *Stardew Valley*. However, while looking for tutorials, I got frustrated seeing that 99% of videos use Pygame to make *Flappy Bird* clones. So, I decided to take my own path and build something different from scratch.

This is the first step. There is still a lot missing, but the goal is to keep improving little by little.

## 🚀 Roadmap (Upcoming features)
The project is currently in its first version. The next goals are:
- [ ] Add more player animations.
- [ ] (Note: Sprite sizes are documented in the file with the same name inside the project).

## ⚙️ Installation and running

Python 3.10 or newer is required. From the project root, create and activate a virtual environment, install Pygame, and start the game:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pygame
python main.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead of the `source` command. When you are done playing, run `deactivate` to leave the virtual environment.

## 🧠 Development Philosophy & AI Usage
In this project, I use AI tools (like Codex CLI on Gentoo) to make improvements and learn. I don't believe in "vibecoding" (letting the AI do everything), but rather in AI as a means to solve problems.

I see it like the historical **Garry Kasparov vs. Deep Blue** match: the machine's victory didn't mean the death of chess, but its transformation. I feel the same is happening with programming. AI is a tool, and we are still the players.

## 🛠️ Tech Stack
- Python 3
- Pygame

## 🤝 Feedback & Contributions
This is my first version and I'm open to learning. If you want to suggest an improvement, report a bug, or tell me what flaws this first version has, I will gladly accept your feedback!


## 🌊 Update: Wave System & Roguelike Upgrades
* **Wave Manager (`oleadas.py`)**: Implemented a modular, time-based wave progression system (`WaveManager` & `WaveConfig`). Enemies dynamically spawn off-screen around the edges using delta time, scaling in quantity, speed, and health as rounds progress.
* **Between-Round Upgrades (`mejoras.py`)**: Clearing a wave pauses the game and displays 3 randomized upgrade cards selectable via keyboard (`1`, `2`, `3`) or mouse click. Players can boost fire rate, projectile damage, movement speed, max health, or heal (filtered out when already at full HP).
* **Sprite & Hitbox Optimization**: Enemy sprites are loaded once from a sprite sheet using `.convert_alpha()` and sliced via `.subsurface()`. Each spawned enemy keeps a fair `24x24` collision hitbox while rendering its sprite centered on top.

---
*Thanks for reading and for checking out my project. Have a nice day and be careful :3!*
