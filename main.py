import pgzrun
import random
FONT_COLOR = (0, 0, 0) 
WIDTH = 1200
HEIGHT = 802
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
START_SPEED=5
COLORS=["yellow","green"]
score = 0 
high_score = 0
current_level=1
final_level=5
game_over=False
game_complete=False
game_started = False
help_clicked = False
containers=[]
animations=[]
custom_font = "fontt.otf"
from pygame import Rect

class Button:
    def __init__(self, text, center):
        self.text = text
        self.center = center
        self.width = 200
        self.height = 50
        self.rect = Rect(self.center[0] - self.width // 2, self.center[1] - self.height // 2, self.width, self.height)

    def draw(self):
        screen.draw.filled_rect(self.rect, (50, 50, 50))  
        screen.draw.text(self.text, center=self.center, fontsize=25, color=(255, 255, 255),fontname="fontt.otf")

start_button = Button("Start", (WIDTH // 2, HEIGHT // 2 - 50))
help_button = Button("Help", (WIDTH // 2, HEIGHT // 2 + 20))
exit_button = Button("Exit", (WIDTH // 2, HEIGHT // 2 + 90))
main_menu_button = Button("Main Menu", (WIDTH // 2, HEIGHT - 50))  

def draw_start_screen():
    screen.blit("background", (0, 0))  
    start_button.draw()
    help_button.draw()
    exit_button.draw()
    if help_clicked:
        screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 180)) 
        help_text = (
            "As the Financial Director at a bustling port, your task is clear:\n"
            "identify and click on the containers with crucial cargo - the red ones.\n\n"
            "Instructions:\n"
            "- Click only on the red containers to earn points.\n"
            "- Avoid clicking other colored containers, as they do not carry cargo.\n\n"
            "Gameplay:\n"
            "1. Click 'Start' to begin.\n"
            "2. Use your mouse to select the red containers.\n"
            "3. Each correct selection advances you, earning points.\n"
            "4. Avoid wrong selections to prevent ending the game prematurely.\n"
            "5. Reach the final level to win!\n\n"
            "Notes:\n"
            "- Press Spacebar to retry or ESC to return to the main menu.\n"
            "- Precision is key; only the red containers carry cargo!\n\n"
            "Ready to showcase your financial skills?"
        )

        screen.draw.text(
            "Welcome to 'Container Quest'!",
            fontsize=35,
            center=(WIDTH / 2, HEIGHT / 10),
            color=(255, 255, 255),
            fontname=custom_font
        )
        screen.draw.text(
            help_text,
            fontsize=22,
            center=(WIDTH / 2, HEIGHT / 2),
            color=(255, 255, 255),
            fontname=custom_font
        )
        main_menu_button.draw()

def display_end_game_popup():
    global current_level, game_over, high_score

    popup_width = 600
    popup_height = 300
    popup_rect = Rect((CENTER_X - popup_width / 2), (CENTER_Y - popup_height / 2), popup_width, popup_height)
    screen.draw.filled_rect(popup_rect, (50, 50, 50))

    display_level = current_level - 1 if game_over and current_level > 1 else 0 if game_over else current_level

    screen.draw.text("Game Over" if game_over else "You Won", fontsize=40, center=(CENTER_X, CENTER_Y - 100), color=(255, 255, 255), fontname="fontt.otf")
    screen.draw.text("High Score: " + str(high_score), fontsize=30, center=(CENTER_X, CENTER_Y - 40), color=(255, 255, 255), fontname="fontt.otf")
    screen.draw.text("Level: " + str(display_level) + " / " + str(final_level), fontsize=30, center=(CENTER_X, CENTER_Y + 20), color=(255, 255, 255), fontname="fontt.otf")
    screen.draw.text(
        "Want to Retry? Hit Spacebar!\nHit Esc to Main Menu",
        fontsize=23,
        center=(CENTER_X, CENTER_Y + 80),
        color=(255, 255, 255),
        fontname="fontt.otf"
    )

def draw():
    global containers,current_level,game_over,game_complete, score
    if game_started:
        screen.clear()
        screen.blit("dark",(0,0))
        screen.draw.text("Score: " + str(score), fontsize=40, color=(0, 0, 0), topleft=(10, 10))
        screen.draw.text("Level: " + str(current_level), fontsize=40, color=(0, 0, 0), topleft=(10,60))
        if game_over or game_complete:
            display_end_game_popup()
        else:
            for con in containers:
                con.draw()
    else:
        draw_start_screen()
def return_to_main_menu():
    global game_started, help_clicked, game_over, game_complete, score, current_level, containers, animations
    game_started = False
    help_clicked = False
    game_over = False
    game_complete = False
    score = 0
    current_level = 1
    containers = []
    animations = []
def update():
    global containers,current_level,game_over,game_complete, game_started
    if game_started:
        if len(containers)==0:
            containers=make_containers(current_level)
        if (game_over or game_complete) and keyboard.space:
            containers=[]
            current_level=1
            game_complete=False
            game_over=False
            reset_score()
        if keyboard[keys.ESCAPE]:
            return_to_main_menu()

def make_containers(number_of_containers):
    colors_to_create=get_colors_to_create(number_of_containers)
    new_containers=create_containers(colors_to_create)
    layout_containers(new_containers)
    animate_containers(new_containers)
    return new_containers

def get_colors_to_create(number_of_containers):
    colors_to_create=["red"]
    for i in range(0,number_of_containers):
        random_color=random.choice(COLORS)
        colors_to_create.append(random_color)
    return colors_to_create

def create_containers(colors_to_create):
    new_containers=[]
    for color in colors_to_create:
        container=Actor(color + "-con")
        new_containers.append(container)
    return new_containers

def layout_containers(containers_to_layout):
    number_of_gaps = len(containers_to_layout) + 1
    gap_size= WIDTH/number_of_gaps
    random.shuffle(containers_to_layout)
    for index, container in enumerate(containers_to_layout):
        new_x_pos= (index+1)*gap_size
        container.x=new_x_pos

def animate_containers(containers_to_animate):
    for container in containers_to_animate:
        duration = max(1, START_SPEED - current_level)
        container.anchor = ("center","bottom")
        animation = animate(container, duration=duration, on_finished=handle_game_over, y=HEIGHT)
        animations.append(animation)

def handle_game_over():
    global game_over, score, high_score
    game_over = True
    sounds.gameover.play()
    if score > high_score:
        high_score = score
    score = 0

def reset_score():
    global score
    score = 0 

def on_mouse_down(pos):
    global containers, current_level, game_started, help_clicked
    if not game_started:
        if start_button.rect.collidepoint(pos):
            game_started = True
        elif help_button.rect.collidepoint(pos):
            help_clicked = True
        elif exit_button.rect.collidepoint(pos):
            exit()
        elif help_clicked and main_menu_button.rect.collidepoint(pos): 
            help_clicked = False
    else:
        for container in containers:
            if container.collidepoint(pos):
                if "red" in container.image:
                    red_container_click()
                    sounds.point.play()
                else:
                    handle_game_over()
                    sounds.die.play()
 
def red_container_click():
   global current_level, containers, animations, game_complete, score
   stop_animations(animations)
   if current_level == final_level:
       game_complete = True
       score += 20
   else:
       current_level = current_level + 1
       containers = []
       animations = []
       score += 20

def stop_animations(animations_to_stop):
    for animation in animations_to_stop:
        if animation.running:
            animation.stop()
    
pgzrun.go()




