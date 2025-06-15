
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
        ("padaria", 7.5, 6.5),
        ("talho", 1.0, 5.0),
        ("peixaria", 0.5, 0.5),
        ("mercearia", 2.5, 7.5),
        ("frutaria", 2.5, 3.5),
        ("charcutaria", 4.5, 5.5),
        ("congelados", 6.5, 5.5),
        ("laticínios", 5.5, 5.5),
        ("bebidas", 2.5, 2.5),
        ("limpeza", 3.5, 6.5),
        ("higiene", 1.5, 1.5),
        ("doces", 7.0, 2.5),
        ("cereais", 8.0, 1.0),
        ("especiarias", 1.5, 2.5),
        ("ovos", 1.0, 9.5),
        ("teste", 1.5, 3.5),
    ]

    createDataBase()
    for i in range(len(products)):
        addSectionToDataBase(products[i][0],  products[i][1], products[i][2]),

    return sectionsLines

# def FindReRoute(frame, route, lastPosition, walkable_points, ReRoutePlot, Position)


def FindReRoute(goal, Position, walkable_points):
    ReRoute = a_star(Position, goal, walkable_points, 0.5)
    print("ReRoute", ReRoute)
    return ReRoute


def initRoute(sectionsLines, shoppingList, coord):

    entrance = (coord[0], coord[1])
    products = [(x, y) for _, _, x, y in shoppingList]
    print(shoppingList)

    grid_size = 0.5

    def find_full_route(start, product_locations, destination, walkable_points, grid_size):
        route = [start]
        remaining_stops = product_locations[:]
        stops = []

        while remaining_stops:
            next_stop = min(remaining_stops, key=lambda p: (
                abs(heuristic(route[-1], p) / (heuristic(p, destination)))))
            stops.append(next_stop)
            route += a_star(route[-1], next_stop,
                            walkable_points, grid_size)[1:]
            remaining_stops.remove(next_stop)

        route += a_star(route[-1], destination, walkable_points, grid_size)[1:]
        return route, stops

    def can_walk(x, y):
        point = Point(x, y)
        return not any(section.contains(point) for section in sectionsLines.values())

    def generate_grid():
        return {(round(x * grid_size, 1), round(y * grid_size, 1))
                for x in range(int(10 / grid_size))
                for y in range(int(10 / grid_size)) if can_walk(x * grid_size, y * grid_size)}

    walkable_points = generate_grid()
    destination = (2.0, 3.0)

    route, stops = find_full_route(entrance, products, destination,
                                   walkable_points, grid_size)

    return route, walkable_points, stops
