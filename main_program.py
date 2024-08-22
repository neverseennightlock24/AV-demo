import pygame
import time
from pathfinding import dijkstra  # Importing the Dijkstra function

pygame.init()
pygame.display.set_caption("Maze Runner")
screen = pygame.display.set_mode((800, 800))

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 50, 50]
BLUE = [0, 127, 255]
GREEN = [0, 255, 0]

userDifficulty = ["Easy", "Medium", "Hard"]

FPS = 5
fpsClock = pygame.time.Clock()
clock = pygame.time.Clock()

speed = 0
elapsed_time = 0
maze_cleared = False
character_visible = True  # New variable to control character visibility

while True:
    print("\nWelcome to the Maze Runner video game.\nUse the UP, DOWN, LEFT, and RIGHT keys to move your character through the maze.\nTouching a wall will reset your position, as will the R key, which will also restart your timer as well as your difficulty selection.\n")
    userInput = input("Type continue to continue. ")
    if userInput.lower() == "continue":
        break
    else:
        print("Sorry, that is not a valid response! \n")

def difficulty():
    global maze_cleared
    if maze_cleared == False:
        while True:
            print("Your options are: ")
            print(userDifficulty)
            userInput2 = input("What difficulty level would you like to try out? ")
            if userInput2.capitalize() in userDifficulty:
                global speed
                speed = ((userDifficulty.index(userInput2.capitalize()) + 1) * 2)
                break
            else:
                print("Sorry, that is not a valid response! \n")
                    
    if maze_cleared == True:
        global myText
        myText = "Congrats! You Beat The Game!"
        return myText

difficulty()

print(speed)

image = pygame.image.load("Pixel-Image_08.png")
image = pygame.transform.scale(image, (30, 30))
green_x = 385
green_y = 700

start_time = time.time()

quitVar = False
font = pygame.font.Font('PlayfairDisplay-VariableFont_wght.ttf', 50)
myText = "Get to the blue platform!"

# Define the maze boundaries
maze_rects = [
    pygame.Rect(100, 600, 50, 50),
    pygame.Rect(150, 600, 50, 50),
    pygame.Rect(200, 600, 50, 50),
    pygame.Rect(250, 600, 50, 50),
    pygame.Rect(300, 600, 50, 50),
    pygame.Rect(450, 600, 50, 50),
    pygame.Rect(500, 600, 50, 50),
    pygame.Rect(550, 600, 50, 50),
    pygame.Rect(600, 600, 50, 50),
    pygame.Rect(650, 600, 50, 50),
    pygame.Rect(650, 550, 50, 50),
    pygame.Rect(650, 500, 50, 50),
    pygame.Rect(650, 450, 50, 50),
    pygame.Rect(650, 400, 50, 50),
    pygame.Rect(100, 550, 50, 50),
    pygame.Rect(100, 500, 50, 50),
    pygame.Rect(100, 450, 50, 50),
    pygame.Rect(100, 400, 50, 50),
    pygame.Rect(100, 200, 50, 200),
    pygame.Rect(650, 200, 50, 200),
    pygame.Rect(150, 200, 200, 50),
    pygame.Rect(450, 200, 200, 50),
    
    pygame.Rect(350, 550, 100, 5),
    pygame.Rect(450, 450, 5, 105),
    pygame.Rect(350, 450, 5, 100),
    pygame.Rect(500, 550, 100, 5),
    pygame.Rect(300, 450, 50, 5),
    pygame.Rect(200, 550, 100, 5),
    pygame.Rect(200, 450, 5, 100),
    pygame.Rect(200, 450, 50, 5),
    pygame.Rect(250, 405, 5, 50),
    pygame.Rect(150, 405, 100, 5),
    pygame.Rect(300, 450, 5, 50),
    pygame.Rect(255, 500, 50, 5),
    pygame.Rect(500, 500, 5, 55),
    pygame.Rect(550, 400, 5, 100),
    pygame.Rect(500, 500, 100, 5),
    pygame.Rect(600, 450, 50, 5),
    pygame.Rect(500, 350, 5, 100),
    pygame.Rect(550, 400, 50, 5),
    pygame.Rect(500, 350, 100, 5),
    pygame.Rect(400, 400, 100, 5),
    pygame.Rect(300, 400, 50, 5),
    pygame.Rect(400, 400, 5, 100),
    pygame.Rect(300, 300, 5, 100),
    pygame.Rect(350, 300, 5, 105),
    pygame.Rect(200, 350, 100, 5),
    pygame.Rect(150, 300, 100, 5),
    pygame.Rect(350, 200, 5, 105),
    pygame.Rect(350, 275, 50, 5),
    pygame.Rect(450, 300, 100, 5),
    pygame.Rect(450, 300, 5, 50),
    pygame.Rect(350, 350, 105, 5),
    pygame.Rect(595, 250, 5, 100),
    pygame.Rect(335, 142.5, 20, 80),
    pygame.Rect(355, 142.5, 95, 20),
    pygame.Rect(450, 142.5, 20, 80)
]

# Reduce the size of the end block to ensure it doesn't overlap with obstacles
end = pygame.Rect(360, 167.5, 85, 85)

# Function to find the nearest valid position
def find_nearest_valid_position(point, maze_rects, step_size=5):
    x, y = point
    while any(rect.collidepoint(x, y) for rect in maze_rects):
        x += step_size
        y += step_size
        # Check bounds to avoid moving out of the screen
        if x >= 800 or y >= 800:
            x, y = point
            break
    return x, y

# Adjust end position to be valid
end_x, end_y = find_nearest_valid_position((end.centerx, end.centery), maze_rects)
end = pygame.Rect(end_x - end.width//2, end_y - end.height//2, 85, 85)

# Debugging: Print the start and end positions
print(f"Start position: {(green_x, green_y)}, End position: {end.center}")

# Use Dijkstra's algorithm to find the path and display it
path = dijkstra((green_x, green_y), (end.centerx, end.centery), maze_rects, screen=screen, line_color=GREEN)

# Print the calculated path for debugging
print("Calculated Path:", path)

# Main loop begins after Dijkstra finishes scanning
while not quitVar:
    
    screen.fill(WHITE)
                   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitVar = True  

        # Check for reset key regardless of character visibility
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                green_x = 385
                green_y = 700
                elapsed_time = 0
                start_time = time.time()
                myText = "Get to the blue platform!"
                maze_cleared = False
                character_visible = True  # Make the character visible again
                difficulty()
                # Re-run Dijkstra after resetting
                path = dijkstra((green_x, green_y), (end.centerx, end.centery), maze_rects, screen=screen, line_color=GREEN)
                print("Recalculated Path:", path)  # Debugging path after reset

    # Only display and allow movement if the maze hasn't been cleared
    if character_visible:
        screen.blit(image, (green_x, green_y))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            green_y -= speed
        if keys[pygame.K_DOWN]:
            green_y += speed
        if keys[pygame.K_LEFT]:
            green_x -= speed
        if keys[pygame.K_RIGHT]:
            green_x += speed
        if keys[pygame.K_i]:
            green_x = 360
            green_y = 170

    if not maze_cleared:
        elapsed_time = time.time() - start_time
        elapsed_time2 = elapsed_time

        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time - seconds - minutes * 60) * 1000)
        elapsed_time2 = "%s:%s:%s" % (minutes, seconds, milliseconds)

    text = font.render(myText, True, BLACK)
    textRect = text.get_rect(center=(400, 100))
    screen.blit(text, textRect)

    timer = font.render("Time: " + str(elapsed_time2), True, GREEN)
    timerRect = timer.get_rect(center=(385, 750))
    screen.blit(timer, timerRect)
    clock.tick(60)
    
    mazeRect = pygame.draw.rect(screen, RED, (100, 600, 50, 50))
    mazeRect0 = pygame.draw.rect(screen, RED, (150, 600, 50, 50))
    mazeRect1 = pygame.draw.rect(screen, RED, (200, 600, 50, 50))
    mazeRect2 = pygame.draw.rect(screen, RED, (250, 600, 50, 50))
    mazeRect3 = pygame.draw.rect(screen, RED, (300, 600, 50, 50))
    mazeRect4 = pygame.draw.rect(screen, RED, (450, 600, 50, 50))
    mazeRect5 = pygame.draw.rect(screen, RED, (500, 600, 50, 50))
    mazeRect6 = pygame.draw.rect(screen, RED, (550, 600, 50, 50))
    mazeRect7 = pygame.draw.rect(screen, RED, (600, 600, 50, 50))
    mazeRect8 = pygame.draw.rect(screen, RED, (650, 600, 50, 50))
    mazeRect9 = pygame.draw.rect(screen, RED, (650, 550, 50, 50))
    mazeRect10 = pygame.draw.rect(screen, RED, (650, 500, 50, 50))
    mazeRect11 = pygame.draw.rect(screen, RED, (650, 450, 50, 50))
    mazeRect12 = pygame.draw.rect(screen, RED, (650, 400, 50, 50))
    mazeRect13 = pygame.draw.rect(screen, RED, (100, 550, 50, 50))
    mazeRect14 = pygame.draw.rect(screen, RED, (100, 500, 50, 50))
    mazeRect15 = pygame.draw.rect(screen, RED, (100, 450, 50, 50))
    mazeRect16 = pygame.draw.rect(screen, RED, (100, 400, 50, 50))
    mazeRect17 = pygame.draw.rect(screen, RED, (100, 200, 50, 200))
    mazeRect18 = pygame.draw.rect(screen, RED, (650, 200, 50, 200))
    mazeRect19 = pygame.draw.rect(screen, RED, (150, 200, 200, 50))
    mazeRect20 = pygame.draw.rect(screen, RED, (450, 200, 200, 50))

    mazeLine = pygame.draw.rect(screen, RED, (350, 550, 100, 5))
    mazeLine1 = pygame.draw.rect(screen, RED, (450, 450, 5, 105))
    mazeLine2 = pygame.draw.rect(screen, RED, (350, 450, 5, 100))
    mazeLine3 = pygame.draw.rect(screen, RED, (500, 550, 100, 5))
    mazeLine4 = pygame.draw.rect(screen, RED, (300, 450, 50, 5))
    mazeLine5 = pygame.draw.rect(screen, RED, (200, 550, 100, 5))
    mazeLine6 = pygame.draw.rect(screen, RED, (200, 450, 5, 100))
    mazeLine7 = pygame.draw.rect(screen, RED, (200, 450, 50, 5))
    mazeLine8 = pygame.draw.rect(screen, RED, (250, 405, 5, 50))
    mazeLine9 = pygame.draw.rect(screen, RED, (150, 405, 100, 5))
    mazeLine10 = pygame.draw.rect(screen, RED, (300, 450, 5, 50))
    mazeLine11 = pygame.draw.rect(screen, RED, (255, 500, 50, 5))
    mazeLine12 = pygame.draw.rect(screen, RED, (500, 500, 5, 55))
    mazeLine13 = pygame.draw.rect(screen, RED, (550, 400, 5, 100))
    mazeLine14 = pygame.draw.rect(screen, RED, (500, 500, 100, 5))  
    mazeLine15 = pygame.draw.rect(screen, RED, (600, 450, 50, 5))
    mazeLine16 = pygame.draw.rect(screen, RED, (500, 350, 5, 100))
    mazeLine17 = pygame.draw.rect(screen, RED, (550, 400, 50, 5))
    mazeLine18 = pygame.draw.rect(screen, RED, (500, 350, 100, 5))
    
    mazeLine20 = pygame.draw.rect(screen, RED, (400, 400, 100, 5))
    mazeLine21 = pygame.draw.rect(screen, RED, (300, 400, 50, 5))
    mazeLine22 = pygame.draw.rect(screen, RED, (400, 400, 5, 100))
    mazeLine23 = pygame.draw.rect(screen, RED, (300, 300, 5, 100))
    mazeLine23 = pygame.draw.rect(screen, RED, (350, 300, 5, 105))
    mazeLine24 = pygame.draw.rect(screen, RED, (200, 350, 100, 5))
    mazeLine25 = pygame.draw.rect(screen, RED, (150, 300, 100, 5))
    mazeLine26 = pygame.draw.rect(screen, RED, (350, 200, 5, 105))
    mazeLine27 = pygame.draw.rect(screen, RED, (350, 275, 50, 5))
    mazeLine28 = pygame.draw.rect(screen, RED, (450, 300, 100, 5))
    mazeLine29 = pygame.draw.rect(screen, RED, (450, 300, 5, 50))
    mazeLine30 = pygame.draw.rect(screen, RED, (350, 350, 105, 5))
    mazeLine31 = pygame.draw.rect(screen, RED, (595, 250, 5, 100))

    mazeLine32 = pygame.draw.rect(screen, RED, (335, 142.5, 20, 80))
    mazeLine33 = pygame.draw.rect(screen, RED, (355, 142.5, 95, 20))
    mazeLine34 = pygame.draw.rect(screen, RED, (450, 142.5, 20, 80))

    end = pygame.draw.rect(screen, BLUE, (360, 167.5, 85, 85))

    rect1 = image.get_rect()
    rect1.x = green_x
    rect1.y = green_y

    # Draw the shortest path
    if path:
        for i in range(len(path) - 1):
            pygame.draw.line(screen, BLUE, path[i], path[i + 1], 10)  # Increase line width to 10 for better visibility

    if rect1.colliderect(mazeRect) or rect1.colliderect(mazeRect0) or rect1.colliderect(mazeRect1) or rect1.colliderect(mazeRect2) or rect1.colliderect(mazeRect3) or rect1.colliderect(mazeRect4) or rect1.colliderect(mazeRect5) or rect1.colliderect(mazeRect6) or rect1.colliderect(mazeRect7) or rect1.colliderect(mazeRect8) or rect1.colliderect(mazeRect9) or rect1.colliderect(mazeRect10) or rect1.colliderect(mazeRect11) or rect1.colliderect(mazeRect12) or rect1.colliderect(mazeRect13) or rect1.colliderect(mazeRect14) or rect1.colliderect(mazeRect15) or rect1.colliderect(mazeRect16) or rect1.colliderect(mazeRect17) or rect1.colliderect(mazeRect18) or rect1.colliderect(mazeRect19) or rect1.colliderect(mazeRect20) or rect1.colliderect(mazeLine) or rect1.colliderect(mazeLine1) or rect1.colliderect(mazeLine2) or rect1.colliderect(mazeLine3) or rect1.colliderect(mazeLine4) or rect1.colliderect(mazeLine5) or rect1.colliderect(mazeLine6) or rect1.colliderect(mazeLine7) or rect1.colliderect(mazeLine8) or rect1.colliderect(mazeLine9) or rect1.colliderect(mazeLine10) or rect1.colliderect(mazeLine11) or rect1.colliderect(mazeLine12) or rect1.colliderect(mazeLine13) or rect1.colliderect(mazeLine14) or rect1.colliderect(mazeLine15) or rect1.colliderect(mazeLine16) or rect1.colliderect(mazeLine17) or rect1.colliderect(mazeLine18) or rect1.colliderect(mazeLine20) or rect1.colliderect(mazeLine21) or rect1.colliderect(mazeLine22) or rect1.colliderect(mazeLine23) or rect1.colliderect(mazeLine24) or rect1.colliderect(mazeLine25) or rect1.colliderect(mazeLine26) or rect1.colliderect(mazeLine27) or rect1.colliderect(mazeLine28) or rect1.colliderect(mazeLine29) or rect1.colliderect(mazeLine30) or rect1.colliderect(mazeLine31) or rect1.colliderect(mazeLine32) or rect1.colliderect(mazeLine33) or rect1.colliderect(mazeLine34):
        green_x = 385
        green_y = 700

    if green_x <= 25:
        green_x = 780

    if green_y <= 25:
        green_y = 780

    if green_x >= 790:
        green_x = 35

    if green_y >= 790:
        green_y = 35

    if rect1.colliderect(end):
        maze_cleared = True
        character_visible = False  # Hide the controllable character
        screen.blit(image, (end.centerx - 15, end.centery - 15))  # Show the character centered on the end platform
        difficulty()
    
    pygame.display.update()

pygame.quit()
