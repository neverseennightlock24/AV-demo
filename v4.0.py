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

# Maze boundaries (same as in v2)
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

# Dijkstra's algorithm with adjusted start and end positions
def dijkstra(start, end, maze_rects, step_size=5):
    width, height = 800, 800
    graph = {}

    # Build the graph
    for x in range(0, width, step_size):
        for y in range(0, height, step_size):
            graph[(x, y)] = []
            if x > 0:
                graph[(x, y)].append((x - step_size, y))
            if y > 0:
                graph[(x, y)].append((x, y - step_size))
            if x < width - step_size:
                graph[(x, y)].append((x + step_size, y))
            if y < height - step_size:
                graph[(x, y)].append((x, y + step_size))

    # Remove nodes inside obstacles
    obstacle_nodes = set()
    for rect in maze_rects:
        for x in range(rect.left, rect.right, step_size):
            for y in range(rect.top, rect.bottom, step_size):
                obstacle_nodes.add((x, y))
    for node in obstacle_nodes:
        if node in graph:
            del graph[node]
    for node in graph:
        graph[node] = [neighbor for neighbor in graph[node] if neighbor not in obstacle_nodes]

    # Adjust start and end positions to nearest nodes in the graph
    def nearest_node(pos):
        x, y = pos
        x = int(round(x / step_size)) * step_size
        y = int(round(y / step_size)) * step_size
        return (x, y)

    start = nearest_node(start)
    end = nearest_node(end)

    if start not in graph:
        print("Start node is inside an obstacle!")
        return []
    if end not in graph:
        print("End node is inside an obstacle! Forcing inclusion.")
        graph[end] = []

    # Dijkstra's algorithm
    queue = [(0, start)]
    distances = {start: 0}
    previous_nodes = {start: None}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor in graph.get(current_node, []):
            new_distance = current_distance + step_size
            if new_distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (new_distance, neighbor))

    if end not in previous_nodes:
        print("No path found!")
        return []

    # Reconstruct path
    path = []
    node = end
    while node != start:
        path.append(node)
        node = previous_nodes[node]
    path.append(start)
    path.reverse()

    return path

# Get the path using Dijkstra's algorithm
path = dijkstra((green_x, green_y), (end.centerx, end.centery), maze_rects, step_size=5)

# Main loop
quitVar = False
clock = pygame.time.Clock()
speed = 5  # Movement speed

while not quitVar:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitVar = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset position
                green_x = 385
                green_y = 700
                # Recalculate path
                path = dijkstra((green_x, green_y), (end.centerx, end.centery), maze_rects, step_size=5)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        green_y -= speed
    if keys[pygame.K_DOWN]:
        green_y += speed
    if keys[pygame.K_LEFT]:
        green_x -= speed
    if keys[pygame.K_RIGHT]:
        green_x += speed

    # Collision detection
    character_rect = image.get_rect()
    character_rect.x = green_x
    character_rect.y = green_y

    if any(character_rect.colliderect(rect) for rect in maze_rects):
        # Reset position
        green_x = 385
        green_y = 700

    # Draw the maze
    for rect in maze_rects:
        pygame.draw.rect(screen, RED, rect)

    # Draw the shortest path
    if path:
        for i in range(len(path) - 1):
            pygame.draw.line(screen, BLUE, path[i], path[i + 1], 5)

    # Draw the character
    screen.blit(image, (green_x, green_y))

    # Draw the end platform
    pygame.draw.rect(screen, BLUE, end)

    # Check if character has reached the end
    if character_rect.colliderect(end):
        # Display success message
        text = font.render("You've reached the end!", True, BLACK)
        textRect = text.get_rect(center=(400, 100))
        screen.blit(text, textRect)

    pygame.display.update()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()


# Patch Notes:
# Have the blue line be dotted like a pirate map
# Have the blue line render a few seconds after the map itself is rendered
# Have the blue line be in the middle of the path
# Have the original djikstra scan be shown
