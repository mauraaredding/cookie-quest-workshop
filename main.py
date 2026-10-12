import math
import random
import pygame

# Cookie Quest — a beginner-friendly graphical game made with Pygame.
# Controls: WASD or arrow keys to move; R to restart after a round.

pygame.init()

WIDTH, HEIGHT = 800, 560
FPS = 60
ROUND_SECONDS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cookie Quest")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (250, 239, 250)
GRID = (239, 220, 242)
INK = (58, 45, 75)
BLUE = (91, 160, 245)
BLUE_DARK = (48, 104, 190)
WHITE = (255, 255, 255)
COOKIE = (190, 120, 66)
CHOCOLATE = (92, 53, 35)
RED = (240, 83, 100)
ORANGE = (255, 174, 73)
GOLD = (255, 211, 83)

font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 22)
big_font = pygame.font.Font(None, 64)

PLAYER_SIZE = 34
PLAYER_SPEED = 5
COOKIE_RADIUS = 13
HAZARD_SIZE = 27
HAZARD_SPAWN_MS = 1050


def new_cookie():
    """Return a cookie at a random position, away from the screen edges."""
    return pygame.Vector2(
        random.randint(35, WIDTH - 35),
        random.randint(75, HEIGHT - 35),
    )


def new_hazard():
    """Start a hazard just outside one edge of the game area."""
    side = random.choice(("top", "left", "right"))
    if side == "top":
        x, y = random.randint(20, WIDTH - 20), -30
    elif side == "left":
        x, y = -30, random.randint(70, HEIGHT - 20)
    else:
        x, y = WIDTH + 30, random.randint(70, HEIGHT - 20)

    target = pygame.Vector2(random.randint(40, WIDTH - 40),
                            random.randint(90, HEIGHT - 40))
    direction = target - pygame.Vector2(x, y)
    if direction.length_squared() == 0:
        direction = pygame.Vector2(1, 0)
    direction = direction.normalize()
    speed = random.uniform(1.7, 3.0)
    return {"pos": pygame.Vector2(x, y), "vel": direction * speed}


def draw_cookie(surface, x, y, radius=COOKIE_RADIUS):
    """Draw a cookie using simple shapes—no image files needed."""
    pygame.draw.circle(surface, COOKIE, (int(x), int(y)), radius)
    pygame.draw.circle(surface, (218, 158, 93),
                       (int(x - 3), int(y - 4)), radius - 4)
    for dx, dy, r in [(-4, -3, 3), (5, 2, 3), (1, -7, 2), (-2, 6, 2)]:
        pygame.draw.circle(surface, CHOCOLATE,
                           (int(x + dx), int(y + dy)), r)


def draw_player(surface, x, y):
    """Draw a friendly blue character with eyes and a smile."""
    center = (int(x), int(y))
    pygame.draw.circle(surface, BLUE_DARK, center, PLAYER_SIZE // 2 + 2)
    pygame.draw.circle(surface, BLUE, center, PLAYER_SIZE // 2)
    pygame.draw.circle(surface, WHITE, (int(x - 6), int(y - 3)), 5)
    pygame.draw.circle(surface, WHITE, (int(x + 6), int(y - 3)), 5)
    pygame.draw.circle(surface, INK, (int(x - 5), int(y - 2)), 2)
    pygame.draw.circle(surface, INK, (int(x + 7), int(y - 2)), 2)
    pygame.draw.arc(surface, INK,
                    (int(x - 7), int(y), 14, 10), 0, math.pi, 2)


def draw_hazard(surface, hazard):
    x, y = int(hazard["pos"].x), int(hazard["pos"].y)
    pygame.draw.circle(surface, RED, (x, y), HAZARD_SIZE // 2)
    pygame.draw.circle(surface, ORANGE, (x, y), HAZARD_SIZE // 4)
    pygame.draw.circle(surface, (255, 224, 177),
                       (x - 3, y - 4), 3)


def draw_background():
    screen.fill(BACKGROUND)
    for x in range(15, WIDTH, 40):
        for y in range(70, HEIGHT, 40):
            pygame.draw.circle(screen, GRID, (x, y), 2)


def draw_text(text, font_obj, color, x, y, center=False):
    image = font_obj.render(text, True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def reset_game():
    return {
        "player": pygame.Vector2(WIDTH / 2, HEIGHT / 2),
        "cookie": new_cookie(),
        "hazards": [],
        "score": 0,
        "started_at": pygame.time.get_ticks(),
        "last_hazard": pygame.time.get_ticks(),
        "state": "playing",
    }


game = reset_game()
running = True

while running:
    dt = clock.tick(FPS)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and game["state"] != "playing":
                game = reset_game()

    if game["state"] == "playing":
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            movement.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            movement.y += 1

        # Normalize diagonal movement so it isn't faster.
        if movement.length_squared() > 0:
            movement = movement.normalize()
            game["player"] += movement * PLAYER_SPEED

        # Keep the player inside the play area.
        game["player"].x = max(PLAYER_SIZE / 2,
                              min(WIDTH - PLAYER_SIZE / 2, game["player"].x))
        game["player"].y = max(70 + PLAYER_SIZE / 2,
                              min(HEIGHT - PLAYER_SIZE / 2, game["player"].y))

        # Spawn hazards on a timer.
        if now - game["last_hazard"] >= HAZARD_SPAWN_MS:
            game["hazards"].append(new_hazard())
            game["last_hazard"] = now

        # Move hazards and remove ones that travel off screen.
        for hazard in game["hazards"]:
            hazard["pos"] += hazard["vel"]
        game["hazards"] = [
            h for h in game["hazards"]
            if -60 < h["pos"].x < WIDTH + 60
            and 50 < h["pos"].y < HEIGHT + 60
        ]

        # Collect the cookie when the player gets close enough.
        if game["player"].distance_to(game["cookie"]) < PLAYER_SIZE / 2 + COOKIE_RADIUS:
            game["score"] += 1
            game["cookie"] = new_cookie()

        # End the round if a hazard hits the player.
        for hazard in game["hazards"]:
            if game["player"].distance_to(hazard["pos"]) < (
                PLAYER_SIZE / 2 + HAZARD_SIZE / 2
            ):
                game["state"] = "game_over"
                break

        elapsed = (now - game["started_at"]) // 1000
        if elapsed >= ROUND_SECONDS:
            game["state"] = "time_up"

    draw_background()

    # Header bar
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 60))
    draw_text("COOKIE QUEST", font, INK, 18, 17)
    draw_text(f"Cookies: {game['score']}", font, INK, 300, 17)
    seconds_left = max(0, ROUND_SECONDS - (now - game["started_at"]) // 1000)
    draw_text(f"Time: {seconds_left}", font, INK, WIDTH - 125, 17)

    if game["state"] == "playing":
        draw_cookie(screen, game["cookie"].x, game["cookie"].y)
        for hazard in game["hazards"]:
            draw_hazard(screen, hazard)
        draw_player(screen, game["player"].x, game["player"].y)
        draw_text("Move: WASD / arrows     Avoid the red hazards!",
                  small_font, INK, WIDTH // 2, HEIGHT - 18, center=True)
    else:
        # A translucent overlay makes the end screen readable.
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 205))
        screen.blit(overlay, (0, 0))
        title = "TIME'S UP!" if game["state"] == "time_up" else "OOPS!"
        draw_text(title, big_font, INK, WIDTH // 2, HEIGHT // 2 - 55, center=True)
        draw_text(f"You collected {game['score']} cookie(s)!",
                  font, INK, WIDTH // 2, HEIGHT // 2, center=True)
        draw_text("Press R to play again  •  Esc to quit",
                  small_font, INK, WIDTH // 2, HEIGHT // 2 + 45, center=True)

    pygame.display.flip()

pygame.quit()
