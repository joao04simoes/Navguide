import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapely.geometry import Point, Polygon
import heapq
import random

# Define supermarket sections and products
sections = {
    "Produce": Polygon([(2, 8.1), (4, 8.1), (4, 7.9), (2, 7.9)]),
    "Dairy": Polygon([(6, 8.1), (8, 8.1), (8, 7.9), (6, 7.9)]),
    "Bakery": Polygon([(2, 6.1), (4, 6.1), (4, 5.9), (2, 5.9)]),
    "Frozen Foods": Polygon([(6, 6.1), (8, 6.1), (8, 5.9), (6, 5.9)]),
    "Snacks": Polygon([(2, 4.1), (4, 4.1), (4, 3.9), (2, 3.9)]),
}

entrance = (5, 9.0)
products = [
    (5, 7.5), (6.5, 7.5), (2.5, 5.5), (6.5, 5.5), (2.5, 3.5),
    (5.5, 5.5), (4.5, 5.5), (2.5, 2.5), (1.5, 2.5), (2.5, 7.5),
    (8.5, 8.5), (1.5, 1.5), (0.5, 0.5), (3.5, 6.5), (7.5, 6.5),
    (5.0, 4.0), (7.0, 2.5), (6.0, 3.5), (1.0, 5.0), (8.0, 1.0)
]

grid_size = 0.5


def heuristic(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]))


def a_star(start, goal, walkable_points, grid_size):

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {point: float('inf') for point in walkable_points}
    g_score[start] = 0
    f_score = {point: float('inf') for point in walkable_points}
    f_score[start] = heuristic(start, goal)

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dx, dy in [(-grid_size, 0), (grid_size, 0), (0, -grid_size), (0, grid_size)]:
            neighbor = (round(current[0] + dx, 1), round(current[1] + dy, 1))
            if neighbor in walkable_points:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + \
                        heuristic(neighbor, goal)
                    if neighbor not in [n[1] for n in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []


def find_full_route(start, product_locations, destination, walkable_points, grid_size):
    route = [start]
    remaining_stops = product_locations[:]

    while remaining_stops:
        next_stop = min(remaining_stops, key=lambda p: (
            abs(heuristic(route[-1], p) / (heuristic(p, destination)))))
        route += a_star(route[-1], next_stop, walkable_points, grid_size)[1:]
        remaining_stops.remove(next_stop)

    route += a_star(route[-1], destination, walkable_points, grid_size)[1:]
    return route


def can_walk(x, y):
    point = Point(x, y)
    return not any(section.contains(point) for section in sections.values())


def generate_grid():
    return {(round(x * grid_size, 1), round(y * grid_size, 1))
            for x in range(int(10 / grid_size))
            for y in range(int(10 / grid_size)) if can_walk(x * grid_size, y * grid_size)}


walkable_points = generate_grid()
destination = (2.0, 3.0)

route = find_full_route(entrance, products, destination,
                        walkable_points, grid_size)

fig, ax = plt.subplots(figsize=(6, 6))


def update(frame):
    ax.clear()
    for polygon in sections.values():
        x, y = polygon.exterior.xy
        ax.fill(x, y, alpha=0.4)

    for px, py in products:
        ax.plot(px, py, 'bs', markersize=5)

    ax.plot(entrance[0], entrance[1], 'g^', markersize=10, label='Entrance')
    if route:
        rx, ry = zip(*route)
        ax.plot(rx, ry, 'c--', linewidth=2, label='Best Route')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.legend()
    ax.set_title("Optimized Shopping Route")


ani = animation.FuncAnimation(fig, update, interval=1000)
plt.show()
