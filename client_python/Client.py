import asyncio
import threading
import time
import tkinter
import traceback

import customtkinter as ctk
import grpc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import CalculateService_pb2 as pb2
import CalculateService_pb2_grpc as pb2_grpc


class App:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.geometry("1200x600")
        self.root.title("Grpc project")
        self.root.update()

        self.frame = ctk.CTkFrame(master=self.root, height=self.root.winfo_height() * 0.75,
                                  width=self.root.winfo_width() * 0.52, fg_color='#242424')
        self.frame.place(relx=0.33, rely=0.025)

        self.enterTStart = ctk.CTkEntry(master=self.root, placeholder_text="Введите начальное время t",
                                        justify='center', width=300, height=50)
        self.enterTStart.place(relx=0.04, rely=0.05)

        self.enterTEnd = ctk.CTkEntry(master=self.root, placeholder_text="Введите конечное время t", justify='center',
                                      width=300, height=50)
        self.enterTEnd.place(relx=0.04, rely=0.15)

        self.enterH = ctk.CTkEntry(master=self.root, placeholder_text="Введите шаг h", justify='center', width=300,
                                   height=50)
        self.enterH.place(relx=0.04, rely=0.25)

        self.button = ctk.CTkButton(master=self.root, text="Вывести график", width=300, height=50,
                                    command=self.output_graph)
        self.button.place(relx=0.04, rely=0.65)

        self.root.mainloop()


    def output_graph(self):
        try:
            tStart = float(self.enterTStart.get())
            tEnd = float(self.enterTEnd.get())
            hInput = float(self.enterH.get())
            if hasattr(self, 'figure_canvas'):
                self.figure_canvas.get_tk_widget().destroy()

            global X0
            X0 = np.array([[0], [0], [0]])
            global t
            t = 0
            global h
            h = hInput

            T_g = []
            X_g = []
            Y_g = []
            Z_g = []

            current_value = tkinter.DoubleVar()

            def get_current_value():
                cur_val = current_value.get()
                t_val = min(T_g, key=lambda x: abs(x - cur_val))
                t_index = T_g.index(t_val)
                x_val = X_g[t_index]
                y_val = Y_g[t_index]
                z_val = Z_g[t_index]
                return 'Текущее значение: {: .2f}\nx: {: .2f}\ny: {: .2f}\nz: {: .2f}'.format(cur_val, x_val, y_val, z_val)

            def slider_changed(event):
                value_label.configure(text=get_current_value())

            value_label = ctk.CTkLabel(self.root, text="Выберите значение")
            value_label.grid(row=2, columnspan=2, ipadx=10, ipady=6, padx=100, pady=300, sticky='n')

            figure, axes = plt.subplots()
            figure_canvas = FigureCanvasTkAgg(figure, master=self.root)
            figure_canvas.draw()
            figure_canvas.get_tk_widget().place(relx=0.33, rely=0.025)
            
            time_slider = ctk.CTkSlider(self.root, from_=tStart, to=tStart+hInput, command=slider_changed, variable=current_value)
            time_slider.place(relx=0.04, rely=0.35)
            time_slider.set(tStart)

            axes.set_xlim(tStart, tEnd)
            axes.set_ylim(-2, 16)
            line0, = axes.plot([], [], lw=2, label="x(t)")
            line1, = axes.plot([], [], lw=2, label="y(t)")
            line2, = axes.plot([], [], lw=2, label="z(t)")
            axes.set_xlabel('Время')
            axes.set_ylabel('x, y, z')
            axes.set_title('Решение ду')
            axes.legend()
            axes.grid(True)

            def update(frame):
                global X0, t, h
                if t < tEnd:
                    X_0, X_1, X_2, X_next_0, X_next_1, X_next_2 = calculate(h, X0[0][0], X0[1][0], X0[2][0])
                    X_g.append(X_next_0)
                    Y_g.append(X_next_1)
                    Z_g.append(X_next_2)
                    T_g.append(t)
                    X0 = np.array([[X_0], [X_1], [X_2]])
                    t = t + h
                    line0.set_data(T_g, X_g)
                    line1.set_data(T_g, Y_g)
                    line2.set_data(T_g, Z_g)
                    if t > tStart:
                        time_slider.configure(to=t)

                    return line0, line1, line2,

            ani = FuncAnimation(figure, update, frames=1000, interval=10, blit=True)
            plt.show()
        except ValueError as e:
            traceback.print_tb(e.__traceback__)
            print("Неккоректные данные")
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print("Error!", e)


def calculate(h, X0_0, X0_1, X0_2):
    retry_delay = 1
    max_retries = 10

    for _ in range(max_retries):
        try:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = pb2_grpc.CalculateServiceStub(channel)
                response = stub.Calculate(pb2.Input(h=h, X0_0=X0_0, X0_1=X0_1, X0_2=X0_2))

                return response.X_0, response.X_1, response.X_2, response.X_next_0, response.X_next_1, response.X_next_2
        except grpc.RpcError as e:
            print(f"Ошибка RPC: {e}")
            time.sleep(retry_delay)
            retry_delay *= 2
    print("Достигнуто максимальное количество попыток, сервер недоступен.")


t = 0
h = 0.2
X0 = np.array([[0], [0], [0]])

if __name__ == '__main__':
    app = App()
