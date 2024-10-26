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
font = pygame.font.Font('PlayfairDisplay-VariableFont_wght.ttf', 30)

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

# Function to draw dashed lines
def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    # Calculate the total length of the line
    total_length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    num_dashes = int(total_length // dl)

    for i in range(0, num_dashes, 2):
        start = (
            x1 + (x2 - x1) * (i / num_dashes),
            y1 + (y2 - y1) * (i / num_dashes)
        )
        end = (
            x1 + (x2 - x1) * ((i + 1) / num_dashes),
            y1 + (y2 - y1) * ((i + 1) / num_dashes)
        )
        pygame.draw.line(surf, color, start, end, width)

def dijkstra(start, end, maze_rects, step_size=5):
    width, height = 800, 800
    graph = {}

    # Define a buffer to prevent paths from getting too close to wall boundaries
    buffer = 3  # Pixels of buffer around each wall

    # Build the graph with buffered wall detection and diagonal neighbor connections
    for x in range(0, width, step_size):
        for y in range(0, height, step_size):
            node = (x, y)
            if all(not rect.inflate(buffer, buffer).collidepoint(node) for rect in maze_rects):
                graph[node] = []
                # Define possible neighbors, including diagonals
                neighbors = [
                    (x - step_size, y), (x + step_size, y), (x, y - step_size), (x, y + step_size),  # Cardinal directions
                    (x - step_size, y - step_size), (x + step_size, y - step_size),  # Diagonals
                    (x - step_size, y + step_size), (x + step_size, y + step_size)
                ]
                for nx, ny in neighbors:
                    neighbor = (nx, ny)
                    if 0 <= nx < width and 0 <= ny < height and all(
                        not rect.inflate(buffer, buffer).collidepoint(neighbor) for rect in maze_rects
                    ):
                        graph[node].append(neighbor)

    # Find the nearest graph nodes to the start and end positions
    def nearest_node(pos):
        x, y = pos
        return ((x // step_size) * step_size, (y // step_size) * step_size)

    start = nearest_node(start)
    end = nearest_node(end)

    if start not in graph:
        print("Start node is inside an obstacle!")
        return []
    if end not in graph:
        print("End node is inside an obstacle! Adding to graph.")
        graph[end] = []

    # Implement Dijkstra's algorithm
    queue = [(0, start)]
    distances = {start: 0}
    previous_nodes = {start: None}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor in graph.get(current_node, []):
            new_distance = current_distance + ((step_size * 1.4) if abs(neighbor[0] - current_node[0]) == step_size and abs(neighbor[1] - current_node[1]) == step_size else step_size)
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
path = dijkstra((green_x, green_y), (end.centerx, end.centery), maze_rects, step_size=10)

# Main loop
quitVar = False
clock = pygame.time.Clock()
speed = 5  # Movement speed

# Timing variables
start_time = time.time()
line_render_start_time = None  # To track when to start line rendering
line_render_delay = 1  # Seconds to wait before starting to render the line
line_render_index = 0  # To animate line drawing

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
                path = dijkstra((green_x, green_y), (end.centerx, end.centery), maze_rects, step_size=10)
                # Reset line rendering variables
                line_render_start_time = time.time()
                line_render_index = 0

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
        # Recalculate path
        path = dijkstra((green_x, green_y), (end.centerx, end.centery), maze_rects, step_size=10)
        # Reset line rendering variables
        line_render_start_time = time.time()
        line_render_index = 0

    # Draw the maze
    for rect in maze_rects:
        pygame.draw.rect(screen, RED, rect)

    # Draw the end platform
    pygame.draw.rect(screen, BLUE, end)

    # Draw the shortest path after a delay
    current_time = time.time()
    if line_render_start_time is None:
        line_render_start_time = start_time

    if current_time - line_render_start_time >= line_render_delay and path:
        # Calculate how many segments to draw based on time
        segments_to_draw = int((current_time - line_render_start_time - line_render_delay) * 50)  # Adjust speed here
        if segments_to_draw > len(path) - 1:
            segments_to_draw = len(path) - 1

        for i in range(segments_to_draw):
            start_pos = path[i]
            end_pos = path[i + 1]
            # Draw dashed line segment
            draw_dashed_line(screen, BLUE, start_pos, end_pos, width=3, dash_length=10)

    # Draw the character
    screen.blit(image, (green_x, green_y))

    # Check if character has reached the end
    if character_rect.colliderect(end):
        # Display success message
        text = font.render("You've reached the end!", True, BLACK)
        textRect = text.get_rect(center=(400, 50))
        screen.blit(text, textRect)

    pygame.display.update()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()