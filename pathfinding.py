import heapq
import pygame

# This is a demo change.
def validate_position(pos, width=800, height=800):
    if pos is None:
        return None
    x, y = pos
    x = max(0, min(x, width - 1))
    y = max(0, min(y, height - 1))
    return x, y

def dijkstra(start, end, maze_rects, screen=None, line_color=None):
    width, height = 800, 800
    step_size = 5  # Checking nodes every 5 pixels to reduce computation
    graph = {}

    for x in range(0, width, step_size):
        for y in range(0, height, step_size):
            graph[(x, y)] = {}
            if x > 0:
                graph[(x, y)][(x-step_size, y)] = 1
            if y > 0:
                graph[(x, y)][(x, y-step_size)] = 1
            if x < width - step_size:
                graph[(x, y)][(x+step_size, y)] = 1
            if y < height - step_size:
                graph[(x, y)][(x, y+step_size)] = 1

    print("Graph Size:", len(graph))

    for rect in maze_rects:
        for x in range(rect.left, rect.right, step_size):
            for y in range(rect.top, rect.bottom, step_size):
                if (x, y) in graph:
                    del graph[(x, y)]

    if start not in graph:
        print("Start node is inside an obstacle!")
    if end not in graph:
        print("End node is inside an obstacle! Forcing inclusion.")
        graph[end] = {}

    print("Nodes after removing obstacles:", len(graph))

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

        if screen and line_color and distances[current_node] % 5 == 0:
            current_node = validate_position(current_node)
            previous_node = validate_position(previous_nodes.get(current_node))
            if previous_node and current_node:
                pygame.draw.line(screen, line_color, previous_node, current_node, 2)
                pygame.display.update()

    if end not in previous_nodes:
        print("End node not reachable!")
        return []

    path = []
    node = end
    while node in previous_nodes and previous_nodes[node] is not None:
        path.append(node)
        node = previous_nodes[node]
    path.append(start)
    path.reverse()

    print("Final Path Length:", len(path))

    return path
