import tkinter as tk
import math

WIDTH = 850
HEIGHT = 300
GROUND = 235

root = tk.Tk()
root.title("Ball Runner")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

running = True
jumping = False
jump_speed = 0
score = 0


# ---------------- BALL CHARACTER ----------------
def create_ball():
    global ball

    ball = canvas.create_oval(
        80, 180,
        120, 220,
        fill="deepskyblue",
        outline="blue",
        width=3
    )


def move_ball(x, y):
    canvas.move(ball, x, y)


def ball_box():
    return canvas.bbox(ball)


# ---------------- SPIKE OBSTACLE ----------------
def create_spike():
    return canvas.create_polygon(
        WIDTH, 235,
        WIDTH + 15, 205,
        WIDTH + 30, 235,

        WIDTH + 30, 235,
        WIDTH + 45, 205,
        WIDTH + 60, 235,

        fill="gray20",
        outline="black",
        width=2
    )


# ---------------- RESET ----------------
def reset():
    global spike, score_text, score, running, jumping

    canvas.delete("all")

    # Ground
    canvas.create_line(0, GROUND, WIDTH, GROUND, width=2)

    create_ball()

    spike = create_spike()

    score = 0

    score_text = canvas.create_text(
        740, 25,
        text="Score: 0",
        font=("Arial", 14)
    )

    running = True
    jumping = False


# ---------------- CONTROLS ----------------
def jump(event):
    global jumping, jump_speed

    if running and not jumping:
        jumping = True
        jump_speed = -15


def restart(event):
    reset()
    game()


root.bind("<space>", jump)
root.bind("r", restart)


# ---------------- GAME LOOP ----------------
def game():
    global jump_speed, jumping, running, score

    if not running:
        return

    # Jump physics
    if jumping:
        move_ball(0, jump_speed)
        jump_speed += 1

        x1, y1, x2, y2 = ball_box()

        if y2 >= 220:
            move_ball(0, 220 - y2)
            jumping = False

    # Spike movement
    canvas.move(spike, -10, 0)

    c = canvas.coords(spike)

    if max(c[::2]) < 0:
        canvas.move(spike, WIDTH + 100, 0)
        score += 1
        canvas.itemconfig(score_text, text=f"Score: {score}")

    # Collision
    dx1, dy1, dx2, dy2 = ball_box()

    cx1 = min(c[::2])
    cx2 = max(c[::2])
    cy1 = min(c[1::2])

    if dx2 > cx1 and dx1 < cx2 and dy2 > cy1:
        running = False

        canvas.create_text(
            420, 100,
            text="GAME OVER\nPress R",
            fill="red",
            font=("Arial", 22)
        )
        return

    root.after(25, game)


# START
reset()
game()
root.mainloop()