import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle


def trilateracao_2d(p1, d1, p2, d2):
    x1, y1 = p1
    x2, y2 = p2

    dx, dy = x2 - x1, y2 - y1
    dist = np.hypot(dx, dy)

    if dist > d1 + d2 or dist < abs(d1 - d2):
        return None

    a = (d1**2 - d2**2 + dist**2) / (2 * dist)
    px = x1 + a * dx / dist
    py = y1 + a * dy / dist

    h = np.sqrt(abs(d1**2 - a**2))
    rx = -dy * (h / dist)
    ry = dx * (h / dist)

    sol1 = (px + rx, py + ry)
    sol2 = (px - rx, py - ry)

    return sol1, sol2

# === Posições fixas dos repetidores ===
anchor1 = np.array([0, 2])
anchor2 = np.array([0, 4.5])

# Subir no eixo Y
t1 = np.linspace(0, 1, 100)
x1 = np.full_like(t1, 3)    # x constante em 3
y1 = 0 + t1 * 3             # y de 0 até 3

# Mover no eixo X para a esquerda
t2 = np.linspace(0, 1, 100)
x2 = 3 - t2 * 3             # x de 3 até 0
y2 = np.full_like(t2, 3)    # y constante em 3

# Junta as duas partes
x = np.concatenate((x1, x2))
y = np.concatenate((y1, y2))
traj = np.vstack((x, y)).T

# === Ruído das medições ===
noise_std = 0.1

# === Configuração do gráfico ===
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-2, 6)
ax.set_ylim(-2, 6)
ax.set_title('Trilateração com 2 Repetidores, Ruído e Circunferências')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.grid(True)

# Desenho dos repetidores
ax.plot(*anchor1, 'ro', label='Repetidor 1')
ax.plot(*anchor2, 'bo', label='Repetidor 2')

prateleiras = [
    Rectangle((4, 4 ), 1, -4, color='gray', alpha=0.6),  # vertical invertida
    Rectangle((4, 4 ), -4, 1, color='gray', alpha=0.6),  # horizontal invertida
    Rectangle((0 , 0 ), 2, 2, color='gray', alpha=0.4)     # quadrado
]
for p in prateleiras:
    ax.add_patch(p)

# Coordenadas dos cantos do retângulo delimitador
x_min, x_max = 0, 5
y_min, y_max = 0, 5

# Pontos do retângulo (fechando o polígono)
corners_x = [x_min, x_max, x_max, x_min, x_min]
corners_y = [y_min, y_min, y_max, y_max, y_min]

# Desenhar as linhas
ax.plot(corners_x, corners_y, 'k-', linewidth=2, label='Limites do mapa')

# Elementos móveis
true_point = ax.plot([], [], 'go', label='Ponto real')[0]
est1_point = ax.plot([], [], 'rx', label='Estimativa 1')[0]
est2_point = ax.plot([], [], 'bx', label='Estimativa 2')[0]

# Circunferências
circle1 = plt.Circle(anchor1, 0, fill=False, edgecolor='r', linestyle='--')
circle2 = plt.Circle(anchor2, 0, fill=False, edgecolor='b', linestyle='--')
ax.add_patch(circle1)
ax.add_patch(circle2)

ax.legend()

# === Atualização da animação ===
def update(frame):
    real_pos = traj[frame]

    # Medições com ruído
    d1 = np.linalg.norm(real_pos - anchor1) + np.random.normal(0, noise_std)
    d2 = np.linalg.norm(real_pos - anchor2) + np.random.normal(0, noise_std)

    # Trilateração
    res = trilateracao_2d(anchor1, d1, anchor2, d2)

    # Atualiza o ponto real
    true_point.set_data(*real_pos)

    # Atualiza estimativas
    if res:
        (x1, y1), (x2, y2) = res
        est1_point.set_data(x1, y1)
        est2_point.set_data(x2, y2)
    else:
        est1_point.set_data([], [])
        est2_point.set_data([], [])

    # Atualiza as circunferências
    circle1.set_radius(d1)
    circle2.set_radius(d2)

    return true_point, est1_point, est2_point, circle1, circle2

ani = FuncAnimation(fig, update, frames=len(traj), interval=50, blit=True)
plt.show()
