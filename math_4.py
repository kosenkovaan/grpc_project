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
h = 0.2
t = 0
X = (A @ X0 + B * u) * h + X0
T_g = []
X_g = []
Y_g = []
Z_g = []

fig, ax = plt.subplots()
ax.set_xlim(0, 160)
ax.set_ylim(-2, 14)
line0, = ax.plot([], [], lw=2)
line1, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)
ax.set_xlabel('Time')
ax.set_ylabel('X, Y, Z')
ax.set_title('Dynamic Plot of X, Y, Z over Time')
ax.grid(True)

def update(frame):
    global X, X0, t
    if t < 160:
        X_next = X + h * ((3 / 2) * (A @ X + B * u) - (1 / 2) * (A @ X0 + B * u))
        X_g.append(X_next[0])
        print(X_next[0])
        Y_g.append(X_next[1])
        Z_g.append(X_next[2])
        T_g.append(t)
        X0 = X
        X = X_next
        t = t + h
        line0.set_data(T_g, X_g)
        line1.set_data(T_g, Y_g)
        line2.set_data(T_g, Z_g)

        return line0, line1, line2,

ani = FuncAnimation(fig, update, frames=1000, interval=10, blit=True)
plt.show()