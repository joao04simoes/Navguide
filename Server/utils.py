import heapq


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
