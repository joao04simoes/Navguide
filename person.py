import random
import keyboard

from utils import heuristic, a_star


def FindReRoute(frame, route, lastPosition, walkable_points, ReRoutePlot, Position):

    goal = min(route, key=lambda p: (heuristic(Position, p)))
    ReRoute = a_star(Position, goal, walkable_points, 0.5)
    print("ReRouting")
    if route:
        rx, ry = zip(*ReRoute)
        ReRoutePlot.set_data(rx, ry)

    lastPosition.set_data(Position[0], Position[1])
    return lastPosition,
