from string import hexdigits
from tkinter import *
import random

#constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "yellow"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"



class Snake:
    def __init__ (self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range (0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, GAME_WIDTH/SPACE_SIZE - 1) * SPACE_SIZE
        y = random.randint(0, GAME_HEIGHT/SPACE_SIZE - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOR, tag = "food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0,(x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake")
    snake.squares.insert(0, square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1

        label.config(text = "Score: {}".format(score))
        canvas.delete("food")

        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        print ("Game Over")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print ("Game Over")
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print ("Game Over")
            return True

    return False
    
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font = ('Times New Roman', 70), text = "GAME OVER", fill = "red", tag = "gameover")


def new_game():
    canvas.delete(ALL)

    new_snake = Snake()
    new_food = Food()
    next_turn(new_snake, new_food)

window = Tk()
window.title("Snake Game")
window.resizable(False, False)


score = 0
direction = 'down'

#score
label = Label(window, text="Score: {}".format(score), font=('Times New Roman', 40))
label.pack()
#game field
canvas = Canvas(window, bg = BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()
#creating the reset button
reset_button = Button(text = "Restart", font = ('Times New Roman', 20), command = new_game)
reset_button.pack(side="left")

#when you start the game, the window will be centered
window.update()
#calculating the width and height of window and screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
#adjusting the placement of the screen
window.geometry(f"{window_width}x{window_height}+{x}+{y}")


#creating binds for keys
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))



#creating the snake and food objects
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()


"""
To Do:
Add difficulty
Restart Button
"""