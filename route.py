from itertools import permutations


def distance(p1, p2):
    return ((abs(p1[0] - p2[0])) + abs((p1[1] - p2[1])))


def generate_non_diagonal_path(route):
    new_route = [route[0]]

    for i in range(len(route) - 1):
        x1, y1 = map(int, new_route[-1])  # Garante que os valores são inteiros
        x2, y2 = map(int, route[i + 1])

        # Movimenta-se primeiro no eixo X (horizontal)
        for x in range(x1, x2, 1 if x2 > x1 else -1):
            new_route.append([x + (1 if x2 > x1 else -1), y1])

        # Depois movimenta-se no eixo Y (vertical)
        for y in range(y1, y2, 1 if y2 > y1 else -1):
            new_route.append([x2, y + (1 if y2 > y1 else -1)])

    new_route.append(route[len(route)-1])

    return new_route


def shortest_path(map_data):
    stations = {s["name"]: s["coords"] for s in map_data["stations"]}
    start = stations["Entrada"]
    end = stations["Caixa 1"]

    waypoints = [stations[name]
                 for name in stations if name not in ["Entrada", "Caixa 1"]]

    min_distance = float("inf")
    best_route = []

    for perm in permutations(waypoints):
        route = [start] + list(perm) + [end]
        dist = sum(distance(route[i], route[i+1]) for i in range(len(route)-1))

        if dist < min_distance:
            min_distance = dist
            best_route = route

    best_route = generate_non_diagonal_path(best_route)
    return best_route, min_distance
