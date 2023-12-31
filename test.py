import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

a0 = 1
a1 = 4.4
a2 = 53.2
a3 = 12
u = 10
X0 = np.array([[0], [0], [0]])

z1 = (-a0 / a3)
z2 = (-a1 / a3)
z3 = (-a2 / a3)
z4 = (1 / a3)

A = np.array([[0, 1, 0], [0, 0, 1], [z1, z2, z3]])
B = np.array([[0], [0], [z4]])
E = np.eye(3)
h = 0.2
t = 0
X = (A @ X0 + B * u) * h + X0
T_g = []
X_g = []
i = 1

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlabel('Time')
ax.set_ylabel('X')
ax.set_title('Dynamic Plot of X over Time')
ax.grid(True)

def update(frame):
    global X, X0, t, i
    if t <= 160:
        X_next = X + h * ((3 / 2) * (A @ X + B * u) - (1 / 2) * (A @ X0 + B * u))
        X_g.append(X_next[0])
        T_g.append(t)
        X0 = X
        X = X_next
        t = t + h
        i = i + 1
        line.set_data(T_g, X_g)
        ax.relim()
        ax.autoscale_view()
        return line,

ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.show()
