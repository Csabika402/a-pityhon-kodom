
import tkinter as tk
import random

# SPACE BLASTER - 8 BIT
# PC-s valtozat

WIDTH = 850
HEIGHT = 638

BG = "#050711"
WHITE = "#ffffff"
CYAN = "#45e8ff"
GREEN = "#66ff88"
RED = "#ff5268"
YELLOW = "#ffe66d"

root = tk.Tk()
root.title("SPACE BLASTER - 8 BIT")
root.configure(bg="#171923")
root.resizable(False, False)

# Ablakmeret
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 790

root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Az ablak a kepernyo kozepere kerul
pos_x = max(0, (screen_width - WINDOW_WIDTH) // 2)
pos_y = max(0, (screen_height - WINDOW_HEIGHT) // 2)

root.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{pos_x}+{pos_y}"
)

title = tk.Label(
    root,
    text="SPACE BLASTER - 8 BIT",
    font=("Courier New", 22, "bold"),
    fg=CYAN,
    bg="#171923"
)
title.pack(pady=(10, 6))

score_label = tk.Label(
    root,
    text="PONT: 0",
    font=("Courier New", 14, "bold"),
    fg=WHITE,
    bg="#171923"
)
score_label.pack(pady=(0, 6))

# 4:3-as jatekter
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BG,
    highlightthickness=2,
    highlightbackground="#444b66"
)
canvas.pack()

help_label = tk.Label(
    root,
    text="MOZGAS: NYILAK / A-D     LOVES: SZOKOZ     UJRA: R",
    font=("Courier New", 10),
    fg="#c4c8d8",
    bg="#171923"
)
help_label.pack(pady=8)

stars = []
bullets = []
enemies = []
keys = set()

score = 0
player_x = WIDTH // 2
player_y = HEIGHT - 55
player_speed = 7
shoot_cooldown = 0
enemy_timer = 0
game_over = False

def create_stars():
    for _ in range(110):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.choice([1, 2, 3])

        star = canvas.create_rectangle(
            x, y, x + size, y + size,
            fill=random.choice([WHITE, CYAN, "#777799"]),
            outline=""
        )
        stars.append(star)

def create_player():
    return canvas.create_polygon(
        player_x, player_y - 18,
        player_x - 17, player_y + 15,
        player_x, player_y + 7,
        player_x + 17, player_y + 15,
        fill=GREEN,
        outline=WHITE
    )

def shoot():
    bullet = canvas.create_rectangle(
        player_x - 3, player_y - 28,
        player_x + 3, player_y - 15,
        fill=YELLOW,
        outline=""
    )
    bullets.append(bullet)

def spawn_enemy():
    x = random.randint(25, WIDTH - 25)
    y = -20
    size = random.choice([12, 15, 18])

    enemy_id = canvas.create_polygon(
        x, y - size,
        x - size, y,
        x, y + size,
        x + size, y,
        fill=RED,
        outline=WHITE
    )

    enemies.append({
        "id": enemy_id,
        "y": y,
        "speed": random.randint(2, 4)
    })

def overlaps(first, second):
    box1 = canvas.bbox(first)
    box2 = canvas.bbox(second)

    if not box1 or not box2:
        return False

    return (
        box1[0] < box2[2]
        and box1[2] > box2[0]
        and box1[1] < box2[3]
        and box1[3] > box2[1]
    )

def end_game():
    global game_over

    if game_over:
        return

    game_over = True

    canvas.create_rectangle(
        150, 235, WIDTH - 150, 385,
        fill="#111426",
        outline=CYAN,
        width=3,
        tags="gameover"
    )

    canvas.create_text(
        WIDTH // 2, 275,
        text="JATEK VEGE!",
        fill=RED,
        font=("Courier New", 30, "bold"),
        tags="gameover"
    )

    canvas.create_text(
        WIDTH // 2, 325,
        text="Nyomd meg az R gombot az ujrakezdeshez",
        fill=WHITE,
        font=("Courier New", 12),
        tags="gameover"
    )

def restart(event=None):
    global score, player_x, game_over
    global shoot_cooldown, enemy_timer, player

    canvas.delete("all")
    stars.clear()
    bullets.clear()
    enemies.clear()
    keys.clear()

    score = 0
    player_x = WIDTH // 2
    game_over = False
    shoot_cooldown = 0
    enemy_timer = 0

    score_label.config(text="PONT: 0")

    create_stars()
    player = create_player()

def key_down(event):
    global shoot_cooldown

    keys.add(event.keysym)

    if event.keysym == "space" and not game_over:
        if shoot_cooldown <= 0:
            shoot()
            shoot_cooldown = 10

    if event.keysym.lower() == "r":
        restart()

def key_up(event):
    keys.discard(event.keysym)

def game_loop():
    global player_x, score
    global shoot_cooldown, enemy_timer

    if not game_over:
        # Jatekos mozgasa
        if "Left" in keys or "a" in keys or "A" in keys:
            player_x -= player_speed

        if "Right" in keys or "d" in keys or "D" in keys:
            player_x += player_speed

        player_x = max(20, min(WIDTH - 20, player_x))

        canvas.coords(
            player,
            player_x, player_y - 18,
            player_x - 17, player_y + 15,
            player_x, player_y + 7,
            player_x + 17, player_y + 15
        )

        # Csillagok mozgatasa
        for star in stars:
            canvas.move(star, 0, 2)

            box = canvas.bbox(star)
            if box and box[1] > HEIGHT:
                x = random.randint(0, WIDTH)
                canvas.coords(star, x, 0, x + 2, 2)

        # Lovedekek mozgatasa
        for bullet in bullets[:]:
            canvas.move(bullet, 0, -10)
            box = canvas.bbox(bullet)

            if not box or box[3] < 0:
                canvas.delete(bullet)
                bullets.remove(bullet)

        # Ellensegek letrehozasa
        enemy_timer += 1

        if enemy_timer >= 35:
            spawn_enemy()
            enemy_timer = 0

        # Ellensegek mozgatasa
        for enemy in enemies[:]:
            canvas.move(enemy["id"], 0, enemy["speed"])
            enemy["y"] += enemy["speed"]

            box = canvas.bbox(enemy["id"])

            if not box or box[1] > HEIGHT:
                canvas.delete(enemy["id"])
                enemies.remove(enemy)
                continue

            if overlaps(player, enemy["id"]):
                end_game()
                break

        # Talalatok
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if overlaps(bullet, enemy["id"]):
                    canvas.delete(bullet)
                    canvas.delete(enemy["id"])

                    if bullet in bullets:
                        bullets.remove(bullet)

                    if enemy in enemies:
                        enemies.remove(enemy)

                    score += 10
                    score_label.config(text=f"PONT: {score}")
                    break

        if shoot_cooldown > 0:
            shoot_cooldown -= 1

    root.after(20, game_loop)

player = None

create_stars()
player = create_player()

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

root.after(150, root.focus_force)
game_loop()

root.mainloop()
