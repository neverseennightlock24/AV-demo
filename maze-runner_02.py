import pygame
import time
import heapq

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Autonomous Vehicle Pathfinding")
screen = pygame.display.set_mode((800, 800))

# Colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 50, 50]
BLUE = [0, 127, 255]
GREEN = [0, 255, 0]

# Load character image and set initial position
image = pygame.image.load("Pixel-Image_08.png")
image = pygame.transform.scale(image, (30, 30))
green_x = 385
green_y = 700

# Font for text
font = pygame.font.Font('PlayfairDisplay-VariableFont_wght.ttf', 50)

# Maze boundaries
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

# Blue end platform
end = pygame.Rect(355, 162.5, 95, 88)

# Dijkstra's algorithm implementation
def dijkstra(start, end, maze_rects):
    width, height = 800, 800
    graph = {}
    
    for x in range(width):
        for y in range(height):
            graph[(x, y)] = {}
            if x > 0:
                graph[(x, y)][(x-1, y)] = 1
            if y > 0:
                graph[(x, y)][(x, y-1)] = 1
            if x < width - 1:
                graph[(x, y)][(x+1, y)] = 1
            if y < height - 1:
                graph[(x, y)][(x, y+1)] = 1

    for rect in maze_rects:
        for x in range(rect.left, rect.right):
            for y in range(rect.top, rect.bottom):
                if (x, y) in graph:
                    del graph[(x, y)]
    
    queue = [(0, start)]
    distances = {start: 0}
    previous_nodes = {start: None}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor, distance in graph.get(current_node, {}).items():
            new_distance = current_distance + distance
            if new_distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (new_distance, neighbor))

    path = []
    node = end
    while previous_nodes[node] is not None:
        path.append(node)
        node = previous_nodes[node]
    path.append(start)
    path.reverse()
    
    return path

# Get the path using Dijkstra's algorithm
path = dijkstra((green_x, green_y), (end.centerx, end.centery), maze_rects)

# Main loop
quitVar = False
while not quitVar:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitVar = True

    # Draw the maze
    for rect in maze_rects:
        pygame.draw.rect(screen, RED, rect)
    
    # Draw the shortest path
    for i in range(len(path) - 1):
        pygame.draw.line(screen, BLUE, path[i], path[i + 1], 5)
    
    # Draw the character
    screen.blit(image, (green_x, green_y))

    # Draw the end platform
    pygame.draw.rect(screen, BLUE, end)

    pygame.display.update()

pygame.quit()
