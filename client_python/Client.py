import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class App:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.geometry("1200x600")
        self.root.title("Grpc project")
        self.root.update()

        self.frame = ctk.CTkFrame(master=self.root, height=self.root.winfo_height()*0.75, width=self.root.winfo_width()*0.52, fg_color='#242424')
        self.frame.place(relx=0.33, rely=0.025)
        
        self.enterT = ctk.CTkEntry(master=self.root, placeholder_text="Введите начальное значение t, с", justify='center', width=300, height=50)
        self.enterT.place(relx=0.04, rely=0.05)

        self.enterT_max = ctk.CTkEntry(master=self.root, placeholder_text="Введите конечное значение t, с", justify='center', width=300, height=50)
        self.enterT_max.place(relx=0.04, rely=0.15)

        self.enterH = ctk.CTkEntry(master=self.root, placeholder_text="Введите шаг h", justify='center', width=300, height=50)
        self.enterH.place(relx=0.04, rely=0.25)


        self.button = ctk.CTkButton(master=self.root, text="Вывести график", width=300, height=50, command=self.output_graph)
        self.button.place(relx=0.04, rely=0.65)

        self.root.mainloop()
    
    def output_graph(self):

        a0 = 1
        a1 = 4.4
        a2 = 53.2
        a3 = 12
        u = 10
        X0 = np.array([[0], [0], [0]])
        t = 0
        t_max = 160


        z1 = (-a0 / a3)
        z2 = (-a1 / a3)
        z3 = (-a2 / a3)
        z4 = (1 / a3)

        A = np.array([[0, 1, 0], [0, 0, 1], [z1, z2, z3]])
        B = np.array([[0], [0], [z4]])
        h = 0.2
        X = (A @ X0 + B * u) * h + X0
        T_g = []
        X_g = []

        Y_g = []
        Z_g = []

        fig, ax = plt.subplots()
        ax.set_xlim(0, t_max)
        ax.set_ylim(-2, 14)
        line0, = ax.plot([], [], lw=2)
        line1, = ax.plot([], [], lw=2)
        line2, = ax.plot([], [], lw=2)
        ax.set_xlabel('Time')
        ax.set_ylabel('X')
        ax.set_title('Решение ДУ')
        ax.grid(True)

        def update(frame, X, X0, t, t_max):
            if t < t_max:
                X_next = X + h * ((3 / 2) * (A @ X + B * u) - (1 / 2) * (A @ X0 + B * u))
                X_g.append(X_next[0])
                Y_g.append(X_next[1])
                Z_g.append(X_next[2])
                T_g.append(t)
                X0 = X
                X = X_next
                t = t + h
                line0.set_data(T_g, X_g)
                line1.set_data(T_g, Y_g)
                line2.set_data(T_g, Z_g)
                ax.relim()
                ax.autoscale_view()
                return line0, line1, line2,

        ani = FuncAnimation(fig, update, frames=1000, interval=10, blit=True, fargs=(X, X0, t, t_max))
        plt.show()
if __name__ == '__main__':        
    app = App()