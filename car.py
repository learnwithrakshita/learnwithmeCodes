import tkinter as tk
import random
import math

# ============================================================
#                 🚗 ENDLESS CAR RACING 🚗
#                    LEARN WITH RAKSHITA
# ============================================================

WIDTH = 900
HEIGHT = 700

root = tk.Tk()
root.title("🚗 Endless Car Racing - Learn with Rakshita")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    highlightthickness=0
)
canvas.pack()

# ============================================================
#                    GAME VARIABLES
# ============================================================

running = True
paused = False
game_over = False

score = 0
coins = 0
lives = 3

speed = 7
max_speed = 18

road_y = 0
frame = 0

player_x = WIDTH // 2
player_y = HEIGHT - 120

player_width = 58
player_height = 105

enemy_cars = []
coin_objects = []
particles = []

keys = set()

high_score = 0

# Road boundaries
ROAD_LEFT = 190
ROAD_RIGHT = 710

# Lanes
LANES = [
    275,
    385,
    495,
    605
]

# ============================================================
#                         COLORS
# ============================================================

SKY = "#101827"
ROAD = "#30343B"
ROAD_DARK = "#25282D"
GRASS = "#16351F"
WHITE = "#FFFFFF"
YELLOW = "#FFD43B"
RED = "#FF3B30"
CYAN = "#00E5FF"
GREEN = "#39FF88"

# ============================================================
#                     BACKGROUND
# ============================================================

def draw_background():

    canvas.delete("background")

    # Sky
    canvas.create_rectangle(
        0, 0, WIDTH, HEIGHT,
        fill=SKY,
        outline="",
        tags="background"
    )

    # Moon
    canvas.create_oval(
        65, 70,
        135, 140,
        fill="#F5F3CE",
        outline="",
        tags="background"
    )

    # Stars
    random.seed(10)

    for i in range(70):
        x = random.randint(10, WIDTH - 10)
        y = random.randint(20, 300)
        r = random.choice([1, 1, 2])

        canvas.create_oval(
            x-r,
            y-r,
            x+r,
            y+r,
            fill="#FFFFFF",
            outline="",
            tags="background"
        )

    # Grass
    canvas.create_rectangle(
        0, 250,
        ROAD_LEFT, HEIGHT,
        fill=GRASS,
        outline="",
        tags="background"
    )

    canvas.create_rectangle(
        ROAD_RIGHT, 250,
        WIDTH, HEIGHT,
        fill=GRASS,
        outline="",
        tags="background"
    )

    # Road
    canvas.create_rectangle(
        ROAD_LEFT,
        0,
        ROAD_RIGHT,
        HEIGHT,
        fill=ROAD,
        outline="",
        tags="background"
    )

    # Road edges
    canvas.create_rectangle(
        ROAD_LEFT - 8,
        0,
        ROAD_LEFT,
        HEIGHT,
        fill="#D9D9D9",
        outline="",
        tags="background"
    )

    canvas.create_rectangle(
        ROAD_RIGHT,
        0,
        ROAD_RIGHT + 8,
        HEIGHT,
        fill="#D9D9D9",
        outline="",
        tags="background"
    )


draw_background()

# ============================================================
#                     ROAD MARKINGS
# ============================================================

lane_markings = []

def create_road_markings():

    global lane_markings

    for obj in lane_markings:
        canvas.delete(obj)

    lane_markings = []

    for x in [330, 440, 550]:

        for y in range(-100, HEIGHT, 100):

            line = canvas.create_rectangle(
                x - 4,
                y,
                x + 4,
                y + 55,
                fill="#F4F4F4",
                outline="",
                tags="road"
            )

            lane_markings.append(line)


create_road_markings()

# ============================================================
#                     PLAYER CAR
# ============================================================

def draw_player():

    canvas.delete("player")

    x = player_x
    y = player_y

    # Shadow
    canvas.create_oval(
        x - 36,
        y + 42,
        x + 36,
        y + 62,
        fill="#151515",
        outline="",
        tags="player"
    )

    # Wheels
    canvas.create_rectangle(
        x - 34,
        y - 30,
        x - 22,
        y + 30,
        fill="#111111",
        outline="",
        tags="player"
    )

    canvas.create_rectangle(
        x + 22,
        y - 30,
        x + 34,
        y + 30,
        fill="#111111",
        outline="",
        tags="player"
    )

    # Main body
    canvas.create_polygon(
        x - 27, y + 45,
        x - 31, y + 10,
        x - 25, y - 40,
        x - 15, y - 52,
        x + 15, y - 52,
        x + 25, y - 40,
        x + 31, y + 10,
        x + 27, y + 45,
        fill="#E63946",
        outline="#FFFFFF",
        width=2,
        tags="player"
    )

    # Roof
    canvas.create_polygon(
        x - 20, y - 10,
        x - 14, y - 38,
        x + 14, y - 38,
        x + 20, y - 10,
        fill="#202A44",
        outline="#80DEEA",
        width=2,
        tags="player"
    )

    # Front windshield
    canvas.create_polygon(
        x - 15, y - 8,
        x - 12, y - 30,
        x + 12, y - 30,
        x + 15, y - 8,
        fill="#57D3FF",
        outline="",
        tags="player"
    )

    # Center racing stripe
    canvas.create_rectangle(
        x - 4,
        y - 48,
        x + 4,
        y + 43,
        fill="#FFFFFF",
        outline="",
        tags="player"
    )

    # Headlights
    canvas.create_oval(
        x - 23,
        y + 25,
        x - 12,
        y + 35,
        fill="#FFFACD",
        outline="",
        tags="player"
    )

    canvas.create_oval(
        x + 12,
        y + 25,
        x + 23,
        y + 35,
        fill="#FFFACD",
        outline="",
        tags="player"
    )

    # Red tail lights
    canvas.create_oval(
        x - 24,
        y - 48,
        x - 14,
        y - 38,
        fill="#FF1744",
        outline="",
        tags="player"
    )

    canvas.create_oval(
        x + 14,
        y - 48,
        x + 24,
        y - 38,
        fill="#FF1744",
        outline="",
        tags="player"
    )


# ============================================================
#                     ENEMY CAR
# ============================================================

def create_enemy():

    lane = random.choice(LANES)

    colors = [
        "#2196F3",
        "#9C27B0",
        "#FF9800",
        "#00C853",
        "#FDD835",
        "#00BCD4"
    ]

    enemy = {
        "x": lane,
        "y": -130,
        "color": random.choice(colors),
        "width": 55,
        "height": 100,
        "speed": random.uniform(0.8, 1.5)
    }

    enemy_cars.append(enemy)


def draw_enemy(enemy):

    x = enemy["x"]
    y = enemy["y"]
    color = enemy["color"]

    canvas.create_oval(
        x - 34,
        y + 40,
        x + 34,
        y + 58,
        fill="#111111",
        outline="",
        tags="enemy"
    )

    # Wheels
    canvas.create_rectangle(
        x - 32,
        y - 30,
        x - 21,
        y + 28,
        fill="#111111",
        outline="",
        tags="enemy"
    )

    canvas.create_rectangle(
        x + 21,
        y - 30,
        x + 32,
        y + 28,
        fill="#111111",
        outline="",
        tags="enemy"
    )

    # Body
    canvas.create_polygon(
        x - 27, y + 45,
        x - 31, y + 8,
        x - 24, y - 40,
        x - 14, y - 50,
        x + 14, y - 50,
        x + 24, y - 40,
        x + 31, y + 8,
        x + 27, y + 45,
        fill=color,
        outline="#FFFFFF",
        width=2,
        tags="enemy"
    )

    # Window
    canvas.create_polygon(
        x - 19, y - 10,
        x - 13, y - 35,
        x + 13, y - 35,
        x + 19, y - 10,
        fill="#18233B",
        outline="#8BE9FD",
        width=2,
        tags="enemy"
    )

    # Windshield reflection
    canvas.create_line(
        x - 12,
        y - 31,
        x + 10,
        y - 12,
        fill="#FFFFFF",
        width=2,
        tags="enemy"
    )

    # Headlights
    canvas.create_oval(
        x - 23,
        y + 25,
        x - 12,
        y + 35,
        fill="#FFF59D",
        outline="",
        tags="enemy"
    )

    canvas.create_oval(
        x + 12,
        y + 25,
        x + 23,
        y + 35,
        fill="#FFF59D",
        outline="",
        tags="enemy"
    )


# ============================================================
#                         COINS
# ============================================================

def create_coin():

    lane = random.choice(LANES)

    coin_objects.append({
        "x": lane,
        "y": -40,
        "rotation": 0
    })


def draw_coin(coin):

    x = coin["x"]
    y = coin["y"]

    size = 13 + int(
        abs(math.sin(math.radians(coin["rotation"]))) * 5
    )

    canvas.create_oval(
        x - size,
        y - size,
        x + size,
        y + size,
        fill=YELLOW,
        outline="#FFF4A3",
        width=2,
        tags="coin"
    )

    canvas.create_text(
        x,
        y,
        text="$",
        fill="#9C6B00",
        font=("Arial", 13, "bold"),
        tags="coin"
    )


# ============================================================
#                       PARTICLES
# ============================================================

def create_crash_particles(x, y):

    for i in range(35):

        angle = random.uniform(0, math.pi * 2)
        velocity = random.uniform(2, 8)

        particles.append({
            "x": x,
            "y": y,
            "dx": math.cos(angle) * velocity,
            "dy": math.sin(angle) * velocity,
            "life": random.randint(20, 45)
        })


def update_particles():

    canvas.delete("particle")

    for particle in particles[:]:

        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]
        particle["dy"] += 0.15
        particle["life"] -= 1

        if particle["life"] <= 0:
            particles.remove(particle)
            continue

        r = random.randint(2, 5)

        canvas.create_oval(
            particle["x"] - r,
            particle["y"] - r,
            particle["x"] + r,
            particle["y"] + r,
            fill=random.choice([
                "#FF3D00",
                "#FFEA00",
                "#FFFFFF",
                "#FF9100"
            ]),
            outline="",
            tags="particle"
        )


# ============================================================
#                       COLLISION
# ============================================================

def collision(ax, ay, aw, ah, bx, by, bw, bh):

    return (
        abs(ax - bx) < (aw + bw) / 2
        and
        abs(ay - by) < (ah + bh) / 2
    )


def check_collisions():

    global lives, game_over

    for enemy in enemy_cars[:]:

        if collision(
            player_x,
            player_y,
            player_width,
            player_height,
            enemy["x"],
            enemy["y"],
            enemy["width"],
            enemy["height"]
        ):

            enemy_cars.remove(enemy)

            lives -= 1

            create_crash_particles(
                player_x,
                player_y
            )

            if lives <= 0:
                game_over = True


    for coin in coin_objects[:]:

        if collision(
            player_x,
            player_y,
            50,
            95,
            coin["x"],
            coin["y"],
            25,
            25
        ):

            coin_objects.remove(coin)

            global coins
            coins += 1


# ============================================================
#                    UPDATE ROAD
# ============================================================

def update_road():

    global road_y

    road_y += speed

    if road_y >= 100:
        road_y = 0

    canvas.delete("road")

    for x in [330, 440, 550]:

        for y in range(-100, HEIGHT + 100, 100):

            real_y = y + road_y

            canvas.create_rectangle(
                x - 4,
                real_y,
                x + 4,
                real_y + 55,
                fill="#F4F4F4",
                outline="",
                tags="road"
            )

    canvas.tag_raise("road")


# ============================================================
#                       UPDATE ENEMIES
# ============================================================

def update_enemies():

    for enemy in enemy_cars[:]:

        enemy["y"] += speed * enemy["speed"]

        if enemy["y"] > HEIGHT + 150:

            enemy_cars.remove(enemy)

            global score
            score += 10


# ============================================================
#                       UPDATE COINS
# ============================================================

def update_coins():

    for coin in coin_objects[:]:

        coin["y"] += speed
        coin["rotation"] += 10

        if coin["y"] > HEIGHT + 50:
            coin_objects.remove(coin)


# ============================================================
#                     DRAW OBJECTS
# ============================================================

def draw_objects():

    canvas.delete("enemy")
    canvas.delete("coin")

    for enemy in enemy_cars:
        draw_enemy(enemy)

    for coin in coin_objects:
        draw_coin(coin)


# ============================================================
#                        HUD
# ============================================================

def draw_hud():

    canvas.delete("hud")

    # Top panel
    canvas.create_rectangle(
        0,
        0,
        WIDTH,
        75,
        fill="#080B16",
        outline="",
        tags="hud"
    )

    # Score
    canvas.create_text(
        30,
        25,
        anchor="w",
        text=f"🏆 SCORE  {score}",
        fill=WHITE,
        font=("Arial", 17, "bold"),
        tags="hud"
    )

    # Coins
    canvas.create_text(
        30,
        52,
        anchor="w",
        text=f"🪙 COINS  {coins}",
        fill=YELLOW,
        font=("Arial", 14, "bold"),
        tags="hud"
    )

    # Speed
    canvas.create_text(
        450,
        25,
        text=f"⚡ {int(speed * 10)} KM/H",
        fill=CYAN,
        font=("Arial", 17, "bold"),
        tags="hud"
    )

    # Lives
    hearts = "❤️ " * lives

    canvas.create_text(
        WIDTH - 30,
        35,
        anchor="e",
        text=hearts,
        fill=RED,
        font=("Arial", 18),
        tags="hud"
    )


# ============================================================
#                    SPAWN SYSTEM
# ============================================================

def spawn_objects():

    if random.random() < 0.035:
        create_enemy()

    if random.random() < 0.018:
        create_coin()


# ============================================================
#                    SPEED SYSTEM
# ============================================================

def increase_speed():

    global speed

    if speed < max_speed:
        speed += 0.002


# ============================================================
#                     PLAYER CONTROL
# ============================================================

def move_player():

    global player_x

    movement = 7

    if "Left" in keys:
        player_x -= movement

    if "Right" in keys:
        player_x += movement

    if "Up" in keys:
        player_x += 0

        global speed

        if speed < max_speed:
            speed += 0.08

    if "Down" in keys:

        speed -= 0.08

        if speed < 4:
            speed = 4

    # Keep inside road
    min_x = ROAD_LEFT + 40
    max_x = ROAD_RIGHT - 40

    player_x = max(
        min_x,
        min(max_x, player_x)
    )


# ============================================================
#                       PAUSE SCREEN
# ============================================================

def draw_pause():

    canvas.create_rectangle(
        0,
        0,
        WIDTH,
        HEIGHT,
        fill="#000000",
        stipple="gray50",
        outline="",
        tags="pause"
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 - 40,
        text="⏸ PAUSED",
        fill=WHITE,
        font=("Arial", 48, "bold"),
        tags="pause"
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 30,
        text="Press P to continue",
        fill=CYAN,
        font=("Arial", 18),
        tags="pause"
    )


# ============================================================
#                     GAME OVER SCREEN
# ============================================================

def draw_game_over():

    canvas.delete("gameover")

    canvas.create_rectangle(
        0,
        0,
        WIDTH,
        HEIGHT,
        fill="#000000",
        stipple="gray50",
        outline="",
        tags="gameover"
    )

    canvas.create_text(
        WIDTH // 2,
        230,
        text="💥 CRASHED! 💥",
        fill=RED,
        font=("Arial", 45, "bold"),
        tags="gameover"
    )

    canvas.create_text(
        WIDTH // 2,
        300,
        text=f"Score: {score}",
        fill=WHITE,
        font=("Arial", 25, "bold"),
        tags="gameover"
    )

    canvas.create_text(
        WIDTH // 2,
        340,
        text=f"Coins: {coins}",
        fill=YELLOW,
        font=("Arial", 20, "bold"),
        tags="gameover"
    )

    canvas.create_text(
        WIDTH // 2,
        400,
        text="Press R to Race Again",
        fill=GREEN,
        font=("Arial", 22, "bold"),
        tags="gameover"
    )

    canvas.create_text(
        WIDTH // 2,
        445,
        text="Press ESC to Quit",
        fill="#AAAAAA",
        font=("Arial", 14),
        tags="gameover"
    )


# ============================================================
#                     RESTART GAME
# ============================================================

def restart_game():

    global score
    global coins
    global lives
    global speed
    global player_x
    global game_over
    global paused

    score = 0
    coins = 0
    lives = 3
    speed = 7

    player_x = WIDTH // 2

    enemy_cars.clear()
    coin_objects.clear()
    particles.clear()

    game_over = False
    paused = False

    canvas.delete("gameover")
    canvas.delete("pause")

    draw_player()


# ============================================================
#                     KEYBOARD EVENTS
# ============================================================

def key_down(event):

    global paused

    key = event.keysym

    keys.add(key)

    if key.lower() == "p":

        if not game_over:

            paused = not paused

            canvas.delete("pause")

            if paused:
                draw_pause()

    if key.lower() == "r" and game_over:
        restart_game()

    if key == "Escape":
        root.destroy()


def key_up(event):

    keys.discard(event.keysym)


root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

# ============================================================
#                         GAME LOOP
# ============================================================

def game_loop():

    global frame

    frame += 1

    if not paused and not game_over:

        move_player()

        increase_speed()

        update_road()

        spawn_objects()

        update_enemies()

        update_coins()

        check_collisions()

        update_particles()

        draw_objects()

        draw_player()

        draw_hud()

        # Increase score with time
        global score

        if frame % 10 == 0:
            score += 1

    elif game_over:

        update_particles()

        canvas.delete("player")

        draw_game_over()

    root.after(30, game_loop)


# ============================================================
#                         START GAME
# ============================================================

draw_player()
draw_hud()

game_loop()

root.mainloop()