import time

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        
        self.enterL = ctk.CTkEntry(master=self.root, placeholder_text="Введите L, например, 10", justify='center', width=300, height=50)
        self.enterL.place(relx=0.04, rely=0.05)

        self.enterT = ctk.CTkEntry(master=self.root, placeholder_text="Введите T, например, 10", justify='center', width=300, height=50)
        self.enterT.place(relx=0.04, rely=0.15)

        self.enterNx = ctk.CTkEntry(master=self.root, placeholder_text="Введите nx, например, 100", justify='center', width=300, height=50)
        self.enterNx.place(relx=0.04, rely=0.25)

        self.enterNt = ctk.CTkEntry(master=self.root, placeholder_text="Введите nt, например, 1000", justify='center', width=300, height=50)
        self.enterNt.place(relx=0.04, rely=0.35)

        self.enterC = ctk.CTkEntry(master=self.root, placeholder_text="Введите C, например, 1", justify='center', width=300, height=50)
        self.enterC.place(relx=0.04, rely=0.45)

        self.button = ctk.CTkButton(master=self.root, text="Вывести график", width=300, height=50, command=self.output_graph)
        self.button.place(relx=0.04, rely=0.65)

        self.root.mainloop()
    
    def output_graph(self):
        try:
            L = float(self.enterL.get())
            T = float(self.enterT.get())
            nx = float(self.enterNx.get())
            nt = float(self.enterNt.get())
            c = float(self.enterC.get())
        except ValueError:
            print("Error!")



        plt.ion()

        nx = int(nx)
        nt = int(nt)
        dx, dt = L / nx, T / nt

        X = np.zeros((nt, nx))
        Y = np.zeros((nt, nx))
        Z = np.zeros((nt, nx))



        u = np.zeros((nt, nx))  # Вертикальное смещение
        v = np.zeros((nt, nx))  # Вертикальная скорость

        u[0, :] = np.sin(np.pi * np.arange(0, L, L / nx))  # Начальные условия
        v[0, :] = np.sin(np.pi * np.arange(0, L, L / nx))

        u[:, 0] = u[:, -1] = v[:, 0] = v[:, -1] = 0  # Граничные условия

        figure = plt.figure(figsize=(9.7, 7), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, master=self.root)
        figure_canvas.get_tk_widget().place(relx=0.33, rely=0.025)

        for n in range(0, nt - 1):  # Применение метода конечных разностей
            plt.clf()
            axes = figure.add_subplot(projection='3d')
            axes.plot_surface(X, Y, Z, cmap=cm.coolwarm)
            axes.set_xlabel('x')
            axes.set_ylabel('t')
            axes.set_zlabel('u')
            for i in range(1, nx - 1):
                X[n + 1, i] = u[n, i] + dt * v[n, i]
                Y[n + 1, i] = v[n, i] + c ** 2 * (dt / dx ** 2) * (u[n, i + 1] - 2 * u[n, i] + u[n, i - 1])
                Z[n+1, i] = u[n, i]
            plt.draw()
            plt.gcf().canvas.flush_events()
            time.sleep(0.05)


        plt.ioff()
        plt.show()
if __name__ == '__main__':        
    app = App()