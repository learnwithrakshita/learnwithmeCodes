import turtle
import random
import math

# ============================================================
# 🐍 REALISTIC GROWING SNAKE GAME
# Learn with Rakshita
# ============================================================

screen = turtle.Screen()
screen.setup(1000, 760)
screen.title("🐍 Realistic Growing Snake | Learn with Rakshita")
screen.bgcolor("#061009")
screen.tracer(0)

# ============================================================
# GAME SETTINGS
# ============================================================

WIDTH = 880
HEIGHT = 560
GRID = 20

score = 0
high_score = 0

direction = "right"
next_direction = "right"

game_running = False
game_over = False

speed = 90

# ⭐ ACTUAL LENGTH OF THE SNAKE
snake_length = 12

# Position history of head
positions = []

# Visible body
body_parts = []

# Scale marks
scale_marks = []

# Particles
particles = []

tongue_timer = 0
animation_timer = 0


# ============================================================
# BACKGROUND
# ============================================================

background = turtle.Turtle()
background.hideturtle()
background.penup()

background.goto(-WIDTH // 2, -HEIGHT // 2)
background.pendown()

background.pensize(5)
background.pencolor("#1aff75")

for _ in range(2):
    background.forward(WIDTH)
    background.left(90)
    background.forward(HEIGHT)
    background.left(90)

background.penup()

# Inner border
background.goto(
    -WIDTH // 2 + 10,
    -HEIGHT // 2 + 10
)

background.pendown()
background.pensize(1)
background.pencolor("#123c20")

for _ in range(2):
    background.forward(WIDTH - 20)
    background.left(90)
    background.forward(HEIGHT - 20)
    background.left(90)

background.penup()


# ============================================================
# TITLE
# ============================================================

title = turtle.Turtle()
title.hideturtle()
title.penup()

title.color("#7CFF6B")
title.goto(0, 325)

title.write(
    "🐍 REALISTIC GROWING SNAKE",
    align="center",
    font=("Arial", 26, "bold")
)


# ============================================================
# SCORE
# ============================================================

score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()

score_writer.color("white")
score_writer.goto(0, 288)


def update_score():

    score_writer.clear()

    score_writer.write(
        f"SCORE : {score}       🏆 HIGH SCORE : {high_score}       🐍 LENGTH : {snake_length}",
        align="center",
        font=("Arial", 14, "bold")
    )


# ============================================================
# MESSAGE
# ============================================================

message = turtle.Turtle()
message.hideturtle()
message.penup()


def show_start():

    message.clear()

    message.goto(0, 80)
    message.color("#7CFF6B")

    message.write(
        "🐍 REALISTIC SNAKE",
        align="center",
        font=("Arial", 40, "bold")
    )

    message.goto(0, 25)
    message.color("white")

    message.write(
        "Eat apples and WATCH YOUR SNAKE GROW!",
        align="center",
        font=("Arial", 17, "bold")
    )

    message.goto(0, -25)
    message.color("#00ffff")

    message.write(
        "PRESS SPACE TO START",
        align="center",
        font=("Arial", 21, "bold")
    )

    message.goto(0, -65)
    message.color("#aaaaaa")

    message.write(
        "Arrow Keys / W A S D",
        align="center",
        font=("Arial", 14, "normal")
    )


# ============================================================
# SNAKE HEAD
# ============================================================

head = turtle.Turtle()
head.penup()
head.speed(0)

head.shape("circle")

head.shapesize(
    stretch_wid=1.25,
    stretch_len=1.7
)

head.color("#42d65c")


# ============================================================
# HEAD HIGHLIGHT
# ============================================================

head_highlight = turtle.Turtle()
head_highlight.shape("circle")
head_highlight.penup()

head_highlight.shapesize(
    stretch_wid=0.35,
    stretch_len=0.65
)

head_highlight.color("#79ff8b")


# ============================================================
# EYES
# ============================================================

left_eye = turtle.Turtle()
left_eye.shape("circle")
left_eye.penup()
left_eye.shapesize(0.30)
left_eye.color("white")

right_eye = turtle.Turtle()
right_eye.shape("circle")
right_eye.penup()
right_eye.shapesize(0.30)
right_eye.color("white")


# ============================================================
# PUPILS
# ============================================================

left_pupil = turtle.Turtle()
left_pupil.shape("circle")
left_pupil.penup()
left_pupil.shapesize(0.15)
left_pupil.color("black")

right_pupil = turtle.Turtle()
right_pupil.shape("circle")
right_pupil.penup()
right_pupil.shapesize(0.15)
right_pupil.color("black")


# ============================================================
# EYE HIGHLIGHTS
# ============================================================

left_eye_glow = turtle.Turtle()
left_eye_glow.shape("circle")
left_eye_glow.penup()
left_eye_glow.shapesize(0.05)
left_eye_glow.color("white")

right_eye_glow = turtle.Turtle()
right_eye_glow.shape("circle")
right_eye_glow.penup()
right_eye_glow.shapesize(0.05)
right_eye_glow.color("white")


# ============================================================
# TONGUE
# ============================================================

tongue = turtle.Turtle()
tongue.hideturtle()
tongue.penup()

tongue.color("#ff3155")
tongue.pensize(3)


def draw_tongue():

    global tongue_timer

    tongue_timer += 1

    tongue.clear()

    if tongue_timer % 30 < 10:

        x = head.xcor()
        y = head.ycor()

        if direction == "right":

            tongue.goto(x + 18, y)
            tongue.pendown()

            tongue.goto(x + 38, y)
            tongue.goto(x + 48, y + 7)

            tongue.penup()

            tongue.goto(x + 38, y)
            tongue.pendown()

            tongue.goto(x + 48, y - 7)

        elif direction == "left":

            tongue.goto(x - 18, y)
            tongue.pendown()

            tongue.goto(x - 38, y)
            tongue.goto(x - 48, y + 7)

            tongue.penup()

            tongue.goto(x - 38, y)
            tongue.pendown()

            tongue.goto(x - 48, y - 7)

        elif direction == "up":

            tongue.goto(x, y + 18)
            tongue.pendown()

            tongue.goto(x, y + 38)
            tongue.goto(x - 7, y + 48)

            tongue.penup()

            tongue.goto(x, y + 38)
            tongue.pendown()

            tongue.goto(x + 7, y + 48)

        elif direction == "down":

            tongue.goto(x, y - 18)
            tongue.pendown()

            tongue.goto(x, y - 38)
            tongue.goto(x - 7, y - 48)

            tongue.penup()

            tongue.goto(x, y - 38)
            tongue.pendown()

            tongue.goto(x + 7, y - 48)

        tongue.penup()


# ============================================================
# FACE
# ============================================================

def update_face():

    x = head.xcor()
    y = head.ycor()

    if direction == "right":

        left_eye.goto(x + 10, y + 10)
        right_eye.goto(x + 10, y - 10)

        left_pupil.goto(x + 13, y + 10)
        right_pupil.goto(x + 13, y - 10)

        left_eye_glow.goto(x + 15, y + 12)
        right_eye_glow.goto(x + 15, y - 8)

        head_highlight.goto(x - 4, y + 9)

    elif direction == "left":

        left_eye.goto(x - 10, y + 10)
        right_eye.goto(x - 10, y - 10)

        left_pupil.goto(x - 13, y + 10)
        right_pupil.goto(x - 13, y - 10)

        left_eye_glow.goto(x - 15, y + 12)
        right_eye_glow.goto(x - 15, y - 8)

        head_highlight.goto(x + 4, y + 9)

    elif direction == "up":

        left_eye.goto(x - 10, y + 10)
        right_eye.goto(x + 10, y + 10)

        left_pupil.goto(x - 10, y + 13)
        right_pupil.goto(x + 10, y + 13)

        left_eye_glow.goto(x - 8, y + 15)
        right_eye_glow.goto(x + 12, y + 15)

        head_highlight.goto(x - 8, y - 3)

    elif direction == "down":

        left_eye.goto(x - 10, y - 10)
        right_eye.goto(x + 10, y - 10)

        left_pupil.goto(x - 10, y - 13)
        right_pupil.goto(x + 10, y - 13)

        left_eye_glow.goto(x - 8, y - 15)
        right_eye_glow.goto(x + 12, y - 15)

        head_highlight.goto(x - 8, y + 3)


# ============================================================
# CREATE BODY PART
# ============================================================

def create_body_part(index):

    body = turtle.Turtle()
    body.penup()
    body.speed(0)

    body.shape("circle")

    # ⭐ BODY GETS SMALLER TOWARDS THE TAIL
    size = max(
        0.42,
        1.02 - index * 0.012
    )

    body.shapesize(
        stretch_wid=size,
        stretch_len=size * 1.35
    )

    if index % 4 == 0:
        body.color("#319d49")

    elif index % 4 == 1:
        body.color("#287f3c")

    elif index % 4 == 2:
        body.color("#1d6832")

    else:
        body.color("#145426")

    body_parts.append(body)

    return body


# ============================================================
# ⭐ UPDATE VISIBLE BODY
# ============================================================

def update_body():

    # --------------------------------------------------------
    # CREATE MORE BODY PARTS IF NEEDED
    # --------------------------------------------------------

    while len(body_parts) < snake_length - 1:

        create_body_part(
            len(body_parts)
        )

    # --------------------------------------------------------
    # HIDE EXTRA BODY PARTS
    # --------------------------------------------------------

    for i in range(
        snake_length - 1,
        len(body_parts)
    ):

        body_parts[i].hideturtle()

    # --------------------------------------------------------
    # POSITION EVERY BODY PART
    # --------------------------------------------------------

    for i in range(
        len(body_parts)
    ):

        if i >= snake_length - 1:
            continue

        history_index = (i + 1) * 1

        if history_index < len(positions):

            px, py = positions[
                history_index
            ]

            body_parts[i].goto(
                px,
                py
            )

            body_parts[i].showturtle()


# ============================================================
# ⭐ GROW SNAKE
# ============================================================

def grow_snake():

    global snake_length

    # --------------------------------------------------------
    # THIS IS THE IMPORTANT PART
    # --------------------------------------------------------

    # Every apple adds TWO visible body parts.
    # Change 2 to 1 if you want slower growth.

    snake_length += 2

    # Make sure history is long enough
    last_position = positions[-1]

    while len(positions) < snake_length * 2:

        positions.append(
            last_position
        )

    update_body()

    update_scales()

    update_score()


# ============================================================
# SCALES
# ============================================================

def create_scale(x, y, size=0.12):

    scale = turtle.Turtle()

    scale.shape("circle")
    scale.penup()

    scale.shapesize(size)

    scale.color("#8be69d")

    scale.goto(
        x,
        y
    )

    scale_marks.append(
        scale
    )


def clear_scales():

    for scale in scale_marks:

        scale.hideturtle()

    scale_marks.clear()


def update_scales():

    clear_scales()

    # ⭐ MORE BODY = MORE SCALES
    for i in range(
        1,
        min(
            snake_length - 1,
            len(positions)
        ),
        2
    ):

        x, y = positions[i]

        create_scale(
            x - 5,
            y + 5,
            0.13
        )

        create_scale(
            x + 3,
            y + 2,
            0.10
        )

        create_scale(
            x - 3,
            y - 5,
            0.10
        )


# ============================================================
# APPLE
# ============================================================

food = turtle.Turtle()
food.shape("circle")
food.penup()

food.shapesize(0.95)
food.color("#ff304f")


apple_shine = turtle.Turtle()
apple_shine.shape("circle")
apple_shine.penup()

apple_shine.shapesize(0.18)
apple_shine.color("#ffb0bb")


leaf = turtle.Turtle()
leaf.shape("circle")
leaf.penup()

leaf.shapesize(
    stretch_wid=0.20,
    stretch_len=0.50
)

leaf.color("#45ff63")


def place_food():

    while True:

        x = random.randrange(
            -WIDTH // 2 + 35,
            WIDTH // 2 - 35,
            GRID
        )

        y = random.randrange(
            -HEIGHT // 2 + 35,
            HEIGHT // 2 - 35,
            GRID
        )

        valid = True

        # Don't place apple on snake
        for px, py in positions:

            if math.dist(
                (x, y),
                (px, py)
            ) < 35:

                valid = False
                break

        if valid:
            break

    food.goto(
        x,
        y
    )

    apple_shine.goto(
        x - 5,
        y + 5
    )

    leaf.goto(
        x + 9,
        y + 10
    )


# ============================================================
# FOOD ANIMATION
# ============================================================

def animate_food():

    pulse = (
        1.0
        + math.sin(
            animation_timer * 0.15
        ) * 0.10
    )

    food.shapesize(
        pulse
    )

    apple_shine.goto(
        food.xcor() - 5,
        food.ycor() + 5
    )

    leaf.goto(
        food.xcor() + 9,
        food.ycor() + 10
    )


# ============================================================
# PARTICLES
# ============================================================

def create_particles(x, y):

    for _ in range(25):

        particle = turtle.Turtle()

        particle.shape("circle")
        particle.penup()

        particle.shapesize(
            random.uniform(
                0.08,
                0.20
            )
        )

        particle.color(
            random.choice([
                "#7CFF6B",
                "#00ffff",
                "#ffff00",
                "#ff5577",
                "#ffffff"
            ])
        )

        particle.goto(
            x,
            y
        )

        angle = random.uniform(
            0,
            math.pi * 2
        )

        velocity = random.uniform(
            2,
            5
        )

        particle.dx = (
            math.cos(angle)
            * velocity
        )

        particle.dy = (
            math.sin(angle)
            * velocity
        )

        particle.life = random.randint(
            12,
            25
        )

        particles.append(
            particle
        )


def update_particles():

    for particle in particles[:]:

        particle.goto(
            particle.xcor()
            + particle.dx,

            particle.ycor()
            + particle.dy
        )

        particle.life -= 1

        if particle.life <= 0:

            particle.hideturtle()

            particles.remove(
                particle
            )


# ============================================================
# INITIALIZE SNAKE
# ============================================================

def initialize_snake():

    global positions
    global snake_length

    # Initial length
    snake_length = 12

    positions.clear()

    # Create a straight initial body
    start_x = -100
    start_y = 0

    for i in range(
        snake_length * 3
    ):

        positions.append(
            (
                start_x - i * GRID,
                start_y
            )
        )

    head.goto(
        start_x,
        start_y
    )

    # Create body turtles
    for body in body_parts:

        body.hideturtle()

    body_parts.clear()

    for i in range(
        snake_length - 1
    ):

        create_body_part(i)

    update_body()

    update_scales()

    update_face()


# ============================================================
# CONTROLS
# ============================================================

def go_up():

    global next_direction

    if direction != "down":

        next_direction = "up"


def go_down():

    global next_direction

    if direction != "up":

        next_direction = "down"


def go_left():

    global next_direction

    if direction != "right":

        next_direction = "left"


def go_right():

    global next_direction

    if direction != "left":

        next_direction = "right"


# ============================================================
# START GAME
# ============================================================

def start_game():

    global direction
    global next_direction
    global score
    global speed
    global game_running
    global game_over

    score = 0

    speed = 90

    direction = "right"
    next_direction = "right"

    game_running = True
    game_over = False

    message.clear()

    initialize_snake()

    place_food()

    update_score()


# ============================================================
# SPACE BAR
# ============================================================

def space_start():

    if not game_running:

        start_game()


# ============================================================
# KEYBOARD
# ============================================================

screen.listen()

# Arrow keys
screen.onkeypress(
    go_up,
    "Up"
)

screen.onkeypress(
    go_down,
    "Down"
)

screen.onkeypress(
    go_left,
    "Left"
)

screen.onkeypress(
    go_right,
    "Right"
)

# W A S D
screen.onkeypress(
    go_up,
    "w"
)

screen.onkeypress(
    go_down,
    "s"
)

screen.onkeypress(
    go_left,
    "a"
)

screen.onkeypress(
    go_right,
    "d"
)

# ⭐ SPACE
screen.onkeypress(
    space_start,
    "space"
)


# ============================================================
# GAME OVER
# ============================================================

def show_game_over():

    message.clear()

    message.goto(
        0,
        85
    )

    message.color(
        "#ff3355"
    )

    message.write(
        "💀 GAME OVER",
        align="center",
        font=(
            "Arial",
            40,
            "bold"
        )
    )

    message.goto(
        0,
        30
    )

    message.color("white")

    message.write(
        f"YOUR SCORE : {score}",
        align="center",
        font=(
            "Arial",
            21,
            "bold"
        )
    )

    message.goto(
        0,
        -15
    )

    message.color(
        "#7CFF6B"
    )

    message.write(
        f"🏆 HIGH SCORE : {high_score}",
        align="center",
        font=(
            "Arial",
            18,
            "bold"
        )
    )

    message.goto(
        0,
        -65
    )

    message.color(
        "#00ffff"
    )

    message.write(
        "PRESS SPACE TO PLAY AGAIN",
        align="center",
        font=(
            "Arial",
            18,
            "bold"
        )
    )


# ============================================================
# MOVE SNAKE
# ============================================================

def move_snake():

    global direction
    global score
    global high_score
    global speed
    global game_running
    global game_over

    if not game_running:

        return

    direction = next_direction

    # Current head
    x = head.xcor()
    y = head.ycor()

    # New position
    if direction == "up":

        y += GRID

    elif direction == "down":

        y -= GRID

    elif direction == "left":

        x -= GRID

    elif direction == "right":

        x += GRID

    # ========================================================
    # WALL COLLISION
    # ========================================================

    if (
        x >= WIDTH // 2 - 18
        or x <= -WIDTH // 2 + 18
        or y >= HEIGHT // 2 - 18
        or y <= -HEIGHT // 2 + 18
    ):

        game_running = False
        game_over = True

        show_game_over()

        return

    # ========================================================
    # BODY COLLISION
    # ========================================================

    # Ignore the very end of the tail
    # because it moves forward.
    for i in range(
        0,
        min(
            snake_length - 2,
            len(positions)
        )
    ):

        px, py = positions[i]

        if math.dist(
            (x, y),
            (px, py)
        ) < 14:

            game_running = False
            game_over = True

            show_game_over()

            return

    # ========================================================
    # ADD NEW HEAD POSITION
    # ========================================================

    positions.insert(
        0,
        (x, y)
    )

    # ========================================================
    # KEEP HISTORY LONG ENOUGH
    # ========================================================

    max_history = (
        snake_length * 2
        + 30
    )

    if len(positions) > max_history:

        positions.pop()

    # Move actual head
    head.goto(
        x,
        y
    )

    # ========================================================
    # ⭐ UPDATE BODY
    # ========================================================

    update_body()

    update_scales()

    # ========================================================
    # 🍎 FOOD COLLISION
    # ========================================================

    if head.distance(
        food
    ) < 27:

        score += 10

        if score > high_score:

            high_score = score

        # Particle explosion
        create_particles(
            food.xcor(),
            food.ycor()
        )

        # ====================================================
        # 🐍🐍🐍 ACTUAL GROWTH
        # ====================================================

        grow_snake()

        # New apple
        place_food()

        # Faster movement
        if speed > 45:

            speed -= 2

        update_score()

    update_face()

    draw_tongue()


# ============================================================
# GAME LOOP
# ============================================================

def game_loop():

    global animation_timer

    animation_timer += 1

    animate_food()

    update_particles()

    if game_running:

        move_snake()

        screen.ontimer(
            game_loop,
            speed
        )

    else:

        screen.ontimer(
            game_loop,
            40
        )

    screen.update()


# ============================================================
# START PROGRAM
# ============================================================

show_start()

update_score()

game_loop()

screen.listen()

'screen.mainloop()