from tkinter import *
import random

# Define constants for game parameters
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Snake class to manage snake's properties and behavior
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize snake's starting coordinates
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create initial snake squares on canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Food class to manage food's properties and behavior
class Food:
    def __init__(self):
        # Randomly position the food on the canvas
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        # Draw the food on the canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Function to advance the game to the next turn
def next_turn(snake, food):
    # Move the snake's head in the specified direction
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert the new head position into the snake's coordinates
    snake.coordinates.insert(0, (x, y))

    # Create a new square for the snake's head
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    # Check if the snake ate the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        # Increment the score and update the label
        global score
        score += 1
        label.config(text="Score:{}".format(score))

        # Delete the eaten food and generate a new one
        canvas.delete("food")
        food = Food()

    else:
        # Remove the last part of the snake (tail) as it moves
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        game_over()
    else:
        # Schedule the next turn after a specified time (SPEED)
        window.after(SPEED, next_turn, snake, food)

# Function to change the direction of the snake
def change_direction(new_direction):
    global direction

    # Check if the new direction is allowed based on the current direction
    if new_direction in ['left', 'right', 'up', 'down']:
        if (new_direction == 'left' and direction != 'right') or \
           (new_direction == 'right' and direction != 'left') or \
           (new_direction == 'up' and direction != 'down') or \
           (new_direction == 'down' and direction != 'up'):
            direction = new_direction

# Function to check for collisions (wall or self)
def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

# Function to handle game over scenario
def game_over():
    # Clear the canvas and display game over text
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")

# Initialize the main game window
window = Tk()
window.title("Snake game")
window.resizable(False, False)

# Initialize variables for score and direction
score = 0
direction = 'down'

# Create a label to display the score
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# Create the game canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Get window dimensions and position it in the center of the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow keys to change direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Create instances of Snake and Food
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Start the main event loop
window.mainloop()
