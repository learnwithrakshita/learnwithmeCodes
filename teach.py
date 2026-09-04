import tkinter as tk
import random
import math

# -----------------------------
# WINDOW
# -----------------------------
root = tk.Tk()
root.title("💜 A Special Letter to My Teacher")
root.geometry("900x600")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=900,
    height=600,
    bg="#15152b",
    highlightthickness=0
)
canvas.pack()


# -----------------------------
# COLORS
# -----------------------------
PURPLE = "#8e7dff"
PINK = "#ff8fab"
WHITE = "#ffffff"
YELLOW = "#ffe66d"
BLUE = "#72ddf7"


# -----------------------------
# CLASSROOM
# -----------------------------

# Blackboard
canvas.create_rectangle(
    80, 55, 820, 360,
    fill="#202b2b",
    outline="#b58b5b",
    width=12
)

# Blackboard heading
canvas.create_text(
    450, 95,
    text="✨ THANK YOU, TEACHER ✨",
    fill=YELLOW,
    font=("Arial", 28, "bold")
)

# Chalk line
canvas.create_line(
    160, 125, 740, 125,
    fill="#ffffff",
    width=2
)

# Small drawings
canvas.create_text(
    200, 190,
    text="★",
    fill=YELLOW,
    font=("Arial", 45)
)

canvas.create_text(
    700, 190,
    text="♥",
    fill=PINK,
    font=("Arial", 45)
)

canvas.create_text(
    450, 190,
    text="Knowledge",
    fill=WHITE,
    font=("Arial", 25, "italic")
)

canvas.create_text(
    450, 235,
    text="is the light",
    fill=BLUE,
    font=("Arial", 24, "italic")
)

canvas.create_text(
    450, 280,
    text="that guides our future.",
    fill=WHITE,
    font=("Arial", 22, "italic")
)


# -----------------------------
# DESK
# -----------------------------

canvas.create_rectangle(
    250, 390, 650, 440,
    fill="#8b5e3c",
    outline=""
)

canvas.create_rectangle(
    280, 440, 310, 520,
    fill="#65432c",
    outline=""
)

canvas.create_rectangle(
    590, 440, 620, 520,
    fill="#65432c",
    outline=""
)


# -----------------------------
# BOOK
# -----------------------------

canvas.create_rectangle(
    365, 365, 535, 405,
    fill="#f8f1df",
    outline="#d8c9a8",
    width=2
)

canvas.create_text(
    450, 385,
    text="📖",
    font=("Arial", 20)
)


# -----------------------------
# LETTER
# -----------------------------

letter = canvas.create_rectangle(
    210, 150, 690, 480,
    fill="#fff8e7",
    outline="#f5d58a",
    width=5
)

letter_title = canvas.create_text(
    450, 190,
    text="Dear Teacher,",
    fill="#5c3d2e",
    font=("Georgia", 30, "bold")
)

message = canvas.create_text(
    450, 270,
    text="",
    fill="#5c3d2e",
    font=("Georgia", 20),
    width=400,
    justify="center"
)

signature = canvas.create_text(
    450, 400,
    text="",
    fill="#8e7dff",
    font=("Georgia", 18, "italic")
)


# -----------------------------
# HIDE LETTER INITIALLY
# -----------------------------

canvas.itemconfig(letter, state="hidden")
canvas.itemconfig(letter_title, state="hidden")
canvas.itemconfig(message, state="hidden")
canvas.itemconfig(signature, state="hidden")


# -----------------------------
# FLOATING HEARTS / STARS
# -----------------------------

particles = []

symbols = ["♥", "★", "✦", "✿"]

for i in range(25):

    x = random.randint(20, 880)
    y = random.randint(10, 590)

    symbol = random.choice(symbols)

    item = canvas.create_text(
        x, y,
        text=symbol,
        fill=random.choice(
            [PINK, PURPLE, YELLOW, BLUE]
        ),
        font=("Arial", random.randint(12, 25))
    )

    particles.append({
        "item": item,
        "x": x,
        "y": y,
        "speed": random.uniform(0.4, 1.2)
    })


def animate_particles():

    for p in particles:

        p["y"] -= p["speed"]

        if p["y"] < -20:
            p["y"] = 620
            p["x"] = random.randint(20, 880)

        canvas.coords(
            p["item"],
            p["x"],
            p["y"]
        )

    root.after(40, animate_particles)


animate_particles()


# -----------------------------
# TYPING ANIMATION
# -----------------------------

messages = [
    "You taught us more than subjects...",
    "You taught us to believe in ourselves.",
    "You corrected our mistakes...",
    "You celebrated our little victories.",
    "And you believed in our dreams...",
    "even when we doubted ourselves.",
]

current_message = 0
typing_index = 0


def type_message():

    global typing_index

    text = messages[current_message]

    if typing_index <= len(text):

        canvas.itemconfig(
            message,
            text=text[:typing_index]
        )

        typing_index += 1

        root.after(55, type_message)

    else:

        root.after(1200, next_message)


def next_message():

    global current_message
    global typing_index

    current_message += 1
    typing_index = 0

    if current_message < len(messages):

        type_message()

    else:

        show_final_message()


# -----------------------------
# FINAL MESSAGE
# -----------------------------

def show_final_message():

    canvas.itemconfig(
        message,
        text="A teacher doesn't just teach lessons...\n\n"
             "A teacher creates FUTURES. 💜"
    )

    canvas.itemconfig(
        signature,
        text="Thank you for being our inspiration. ✨"
    )

    root.after(3000, final_screen)


def final_screen():

    canvas.delete("all")

    # Background stars
    for i in range(70):

        x = random.randint(0, 900)
        y = random.randint(0, 600)

        canvas.create_text(
            x, y,
            text=random.choice(["★", "✦", "♥"]),
            fill=random.choice(
                [YELLOW, PINK, PURPLE, BLUE]
            ),
            font=("Arial", random.randint(10, 28))
        )

    canvas.create_text(
        450, 190,
        text="🎓",
        font=("Arial", 70)
    )

    canvas.create_text(
        450, 285,
        text="HAPPY TEACHER'S DAY!",
        fill=YELLOW,
        font=("Arial", 38, "bold")
    )

    canvas.create_text(
        450, 345,
        text="To every teacher who turns\n"
             "ordinary students into extraordinary people.",
        fill=WHITE,
        font=("Arial", 20),
        justify="center"
    )

    canvas.create_text(
        450, 450,
        text="💜 Thank You, Teacher 💜",
        fill=PINK,
        font=("Arial", 27, "bold")
    )

    canvas.create_text(
        450, 525,
        text="— Learn with Rakshita —",
        fill=PURPLE,
        font=("Arial", 16, "italic")
    )


# -----------------------------
# START ANIMATION
# -----------------------------

def start():

    canvas.itemconfig(letter, state="normal")
    canvas.itemconfig(letter_title, state="normal")
    canvas.itemconfig(message, state="normal")
    canvas.itemconfig(signature, state="normal")

    type_message()


root.after(2500, start)

root.mainloop()