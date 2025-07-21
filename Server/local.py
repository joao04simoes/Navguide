import numpy as np


import numpy as np


def trilateracao_2d(p1, d1, p2, d2):
    x1, y1 = p1
    x2, y2 = p2

    dx, dy = x2 - x1, y2 - y1
    dist = np.hypot(dx, dy)

    # Verifica se há interseção dos círculos
    if dist > d1 + d2 or dist < abs(d1 - d2):
        return None  # Sem solução

    a = (d1**2 - d2**2 + dist**2) / (2 * dist)
    px = x1 + a * dx / dist
    py = y1 + a * dy / dist

    h = np.sqrt(d1**2 - a**2)
    rx = -dy * (h / dist)
    ry = dx * (h / dist)

    sol1 = (px + rx, py + ry)
    sol2 = (px - rx, py - ry)

    return sol1
