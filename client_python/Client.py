from functools import partial
import grpc
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import CalculateService_pb2_grpc as pb2_grpc
import CalculateService_pb2 as pb2

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
        
        self.enterA0 = ctk.CTkEntry(master=self.root, placeholder_text="Введите a0, например, 1", justify='center', width=300, height=50)
        self.enterA0.place(relx=0.04, rely=0.05)

        self.enterA1 = ctk.CTkEntry(master=self.root, placeholder_text="Введите a1, например, 4.4", justify='center', width=300, height=50)
        self.enterA1.place(relx=0.04, rely=0.15)

        self.enterA2 = ctk.CTkEntry(master=self.root, placeholder_text="Введите a2, например, 53.2", justify='center', width=300, height=50)
        self.enterA2.place(relx=0.04, rely=0.25)

        self.enterA3 = ctk.CTkEntry(master=self.root, placeholder_text="Введите a3, например, 12", justify='center', width=300, height=50)
        self.enterA3.place(relx=0.04, rely=0.35)

        self.enterU = ctk.CTkEntry(master=self.root, placeholder_text="Введите u, например, 10", justify='center', width=300, height=50)
        self.enterU.place(relx=0.04, rely=0.45)

        self.button = ctk.CTkButton(master=self.root, text="Вывести график", width=300, height=50, command=self.output_graph)
        self.button.place(relx=0.04, rely=0.65)

        self.root.mainloop()
    
    def output_graph(self):
        try:
            a0 = float(self.enterA0.get())
            a1 = float(self.enterA1.get())
            a2 = float(self.enterA2.get())
            a3 = float(self.enterA3.get())
            u = float(self.enterU.get())
        except ValueError:
            print("Error!")

        T_g = []
        X_g = []
        Y_g = []
        Z_g = []


        figure, axes = plt.subplots()
        figure_canvas = FigureCanvasTkAgg(figure, master=self.root)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().place(relx=0.33, rely=0.025)

        axes.set_xlim(0, 160)
        axes.set_ylim(-2, 14)
        line0, = axes.plot([], [], lw=2)
        line1, = axes.plot([], [], lw=2)
        line2, = axes.plot([], [], lw=2)
        axes.set_xlabel('Time')
        axes.set_ylabel('X, Y, Z')
        axes.set_title('Dynamic Plot of X, Y, Z over Time')
        axes.grid(True)

        def update(frame):
            global X0, t, h
            if t < 160:
                X_0, X_1, X_2, X_next_0, X_next_1, X_next_2 = calculate(a0, a1, a2, a3, u, X0[0][0], X0[1][0], X0[2][0])
                X_g.append(X_next_0)
                Y_g.append(X_next_1)
                Z_g.append(X_next_2)
                T_g.append(t)
                X0 = np.array([[X_0], [X_1], [X_2]])
                X = np.array([[X_next_0], [X_next_1], [X_next_2]])
                t = t + h
                line0.set_data(T_g, X_g)
                line1.set_data(T_g, Y_g)
                line2.set_data(T_g, Z_g)

                return line0, line1, line2,

        ani = FuncAnimation(figure, update, frames=1000, interval=10, blit=True)
        plt.show()

def calculate(a0, a1, a2, a3, u, X0_0, X0_1, X0_2):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.CalculateServiceStub(channel)
        response = stub.Calculate(pb2.Input(a0=a0, a1=a1, a2=a2, a3=a3, u=u, X0_0=X0_0, X0_1=X0_1, X0_2=X0_2))

        return response.X_0, response.X_1, response.X_2, response.X_next_0, response.X_next_1, response.X_next_2

h = 0.2
t = 0
X0 = np.array([[0], [0], [0]])

if __name__ == '__main__':        
    app = App()