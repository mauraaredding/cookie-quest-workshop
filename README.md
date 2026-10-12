# Cookie Quest: Deluxe — Cookies & Code

## Run it
Open this folder in VS Code, then Terminal → New Terminal.

macOS/Linux:
```bash
python3 -m pip install pygame
python3 main.py
```

Windows:
```bash
py -m pip install pygame
py main.py
```

## Controls
- Move: WASD or arrow keys
- Dash: Space (recharges)
- Pause/resume: P
- Restart after game ends: R
- Quit: Esc

## Features
- Animated character and chasing enemies
- Cookies, golden bonus cookies, score, timer, lives, and levels
- Three power-ups: shield, speed boost, cookie magnet
- Dash move, particle bursts, title/pause/end screens
- No image or sound files required

## Workshop outline (60 minutes)
1. 0–5: Demo the game and challenge.
2. 5–10: Install Pygame and run.
3. 10–20: Explain the game loop, coordinates, and drawing functions.
4. 20–35: Change game rules and values.
5. 35–50: Build a custom feature.
6. 50–60: Playtest and share.

## Challenges
Easy:
- Change the palette, player speed, round length, or starting lives.
- Make regular cookies worth 2 points.

Medium:
- Add a slow-enemy power-up.
- Add a double-points power-up.
- Add a new enemy movement pattern.
- Adjust how often golden cookies appear.

Advanced:
- Add a boss after a score threshold.
- Create a second stage with a different background.
- Save a high score to a file.
- Replace the drawn character with a sprite sheet.
- Add sound effects using `pygame.mixer`.

Tip: make one change at a time and run the game frequently. Beginners can change constants and colors while experienced programmers implement new mechanics.
