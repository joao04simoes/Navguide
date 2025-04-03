import random

from utils import heuristic, a_star


def GetPosition():
    x = random.randint(0, 10)
    y = random.randint(0, 10)
    return (x, y)


def personWalking(frame, route, lastPosition, walkable_points, ReRoutePlot):

    NextPosition = route[frame]
    RealPosition = GetPosition()
    if (RealPosition in route):
        print("on route")
    else:
        goal = min(route, key=lambda p: (heuristic(RealPosition, p)))
        ReRoute = a_star(RealPosition, goal, walkable_points, 0.5)
        print("ReRouting")
        if route:
            rx, ry = zip(*ReRoute)
            ReRoutePlot.set_data(rx, ry)

    lastPosition.set_data(RealPosition[0], RealPosition[1])
    return lastPosition,
