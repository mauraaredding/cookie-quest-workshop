# Cookie Quest — Cookies & Code workshop

A small graphical arcade game built with Python and Pygame. It uses drawn shapes, so no extra image assets are needed.

## Run it

1. Open this folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Install Pygame:

   **macOS/Linux**
   ```bash
   python3 -m pip install pygame
   ```

   **Windows**
   ```bash
   py -m pip install pygame
   ```

4. Run the game:

   **macOS/Linux**
   ```bash
   python3 main.py
   ```

   **Windows**
   ```bash
   py main.py
   ```

## Controls

- Move: WASD or arrow keys
- Restart after the round ends: R
- Quit: Esc or close the window

## How the game works

- `setup` is not used here; Pygame initializes the window directly.
- The main `while running` loop processes events, updates the game, draws the screen, and repeats.
- `new_cookie()` chooses a random collectible position.
- `new_hazard()` creates a hazard with a velocity aimed toward a random point.
- `distance_to()` checks whether the player has collected a cookie or hit a hazard.
- `reset_game()` resets the round's state.

## Workshop challenges

### Easy
1. Change the background and player colors.
2. Change `PLAYER_SPEED` to make movement faster or slower.
3. Change `ROUND_SECONDS` to make a shorter or longer round.
4. Make each cookie worth 2 points.

### Medium
5. Add a golden cookie worth 5 points.
6. Give the player three lives before the game ends.
7. Make hazards spawn faster as the score increases.
8. Add a shield power-up that protects the player for 5 seconds.

### Hard
9. Add a second level when the player reaches 10 cookies.
10. Add a dash move activated by Space.
11. Track and display a best score for the current session.
12. Replace the shape-based character with a PNG sprite.

## Suggested 60-minute workshop

- 0–5 min: Demo and explain the goal.
- 5–10 min: Install Pygame and run the starter.
- 10–20 min: Explore the main game loop and drawing functions.
- 20–35 min: Change movement, scoring, and collision rules.
- 35–50 min: Add a self-chosen challenge.
- 50–60 min: Playtest and share games.

Facilitator tip: test the installation and starter file on the presentation computer before the meeting. Ask participants to change one thing at a time and run the game frequently.
