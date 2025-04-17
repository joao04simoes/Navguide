
from shapely.geometry import Point, Polygon
import heapq
import random

from utils import heuristic, a_star
from dataBase import addSectionToDataBase, getSectionsFromDataBase, createDataBase


def InitMap():
    sectionsLines = {
        "Produce": Polygon([(2, 8.1), (4, 8.1), (4, 7.9), (2, 7.9)]),
        "Dairy": Polygon([(6, 8.1), (8, 8.1), (8, 7.9), (6, 7.9)]),
        "Bakery": Polygon([(2, 6.1), (4, 6.1), (4, 5.9), (2, 5.9)]),
        "Frozen Foods": Polygon([(6, 6.1), (8, 6.1), (8, 5.9), (6, 5.9)]),
        "Snacks": Polygon([(2, 4.1), (4, 4.1), (4, 3.9), (2, 3.9)]),
    }

    products = [
        ("der", 5, 7.5), ("fer", 6.5, 7.5), ("ilo", 2.5,
                                             5.5), ("wfe", 6.5, 5.5), ("pol", 2.5, 3.5),
        ("oiu", 5.5, 5.5), ("pkl ", 4.5, 5.5), ("ref",
                                                2.5, 2.5), ("ter", 1.5, 2.5), ("kji", 2.5, 7.5),
        ("hji", 1, 9.5), ("ghh", 1.5, 1.5), ("fcv", 0.5,
                                             0.5), ("vbn", 3.5, 6.5), ("vpn", 7.5, 6.5),
        ("das", 5.0, 4.0), ("fds", 7.0, 2.5), ("ctrl",
                                               6.0, 3.5), ("jyt", 1.0, 5.0), ("ultimo", 8.0, 1.0)
    ]
    createDataBase()
    for i in range(len(products)):
        addSectionToDataBase(products[i][0],  products[i][1], products[i][2]),

    return sectionsLines

# def FindReRoute(frame, route, lastPosition, walkable_points, ReRoutePlot, Position)


def FindReRoute(route, Position, walkable_points):
    goal = min(route, key=lambda p: (heuristic(Position, p)))
    ReRoute = a_star(Position, goal, walkable_points, 0.5)
    # print("ReRouting")
    # if route:
    #    rx, ry = zip(*ReRoute)
    #    ReRoutePlot.set_data(rx, ry)
    #
    # lastPosition.set_data(Position[0], Position[1])
    return ReRoute


def initRoute(sectionsLines):

    entrance = (5, 9.0)
    allsections = getSectionsFromDataBase()
    products = [(x, y) for _, _, x, y in allsections]

    print(allsections)

    grid_size = 0.5

    def find_full_route(start, product_locations, destination, walkable_points, grid_size):
        route = [start]
        remaining_stops = product_locations[:]

        while remaining_stops:
            next_stop = min(remaining_stops, key=lambda p: (
                abs(heuristic(route[-1], p) / (heuristic(p, destination)))))
            route += a_star(route[-1], next_stop,
                            walkable_points, grid_size)[1:]
            remaining_stops.remove(next_stop)

        route += a_star(route[-1], destination, walkable_points, grid_size)[1:]
        return route

    def can_walk(x, y):
        point = Point(x, y)
        return not any(section.contains(point) for section in sectionsLines.values())

    def generate_grid():
        return {(round(x * grid_size, 1), round(y * grid_size, 1))
                for x in range(int(10 / grid_size))
                for y in range(int(10 / grid_size)) if can_walk(x * grid_size, y * grid_size)}

    walkable_points = generate_grid()
    destination = (2.0, 3.0)

    route = find_full_route(entrance, products, destination,
                            walkable_points, grid_size)

    return route, walkable_points
