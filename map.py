import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapely.geometry import Point, Polygon
import heapq
import random

from person import personWalking
from utils import heuristic, a_star

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
    (1, 9.5), (1.5, 1.5), (0.5, 0.5), (3.5, 6.5), (7.5, 6.5),
    (5.0, 4.0), (7.0, 2.5), (6.0, 3.5), (1.0, 5.0), (8.0, 1.0)
]

grid_size = 0.5


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
ax.plot()

lastPosition, = ax.plot([], [], 'ro', markersize=10)
ReRoutePlot, = ax.plot([], [], '*', linewidth=2, label='ReRoute')

ani = animation.FuncAnimation(fig, personWalking, frames=len(route),
                              fargs=(route, lastPosition, walkable_points, ReRoutePlot), interval=1000)
plt.show()
