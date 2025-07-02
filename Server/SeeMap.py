import matplotlib.pyplot as plt
import matplotlib.animation as animation

from map import InitMap, initRoute
from dataBase import getSectionsFromDataBase

fig, ax = plt.subplots(figsize=(6, 6))


def PlotMap():
    sectionsLines = InitMap()

    products = getSectionsFromDataBase()
    entrance = (0.5, 9.0)
    route, walkPoints, stops = initRoute(sectionsLines, products, entrance)

    ax.clear()
    for polygon in sectionsLines.values():
        x, y = polygon.exterior.xy
        ax.fill(x, y, alpha=0.4)

    for coor in products:
        ax.plot(coor[2], coor[3], 'bs', markersize=5)

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


ani = animation.FuncAnimation(fig, PlotMap(), interval=1000)
plt.show()
