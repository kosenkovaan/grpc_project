import grpc
import numpy as np
import customtkinter as ctk
from matplotlib import cm
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

        X, T, u = calculate(L, T, nx, nt, c)

        figure = Figure(figsize=(9.7, 7), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, master=self.root)
        
        axes = figure.add_subplot(111, projection='3d')  
        axes.plot_surface(X, T, u, cmap=cm.coolwarm)
        axes.set_xlabel('x')
        axes.set_ylabel('t')
        axes.set_zlabel('u')  
 
        figure_canvas.get_tk_widget().place(relx=0.33, rely=0.025)

def calculate(L, T, nx, nt, c):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.CalculateServiceStub(channel)
        response = stub.Calculate(pb2.Input(L=L, T=T, nx=nx, nt=nt, c=c))
        
        X = np.asarray(response.X)
        T = np.asarray(response.T)
        u = np.asarray(response.u)

        X = X.reshape(int(nx), int(nt))
        T = T.reshape(int(nx), int(nt))
        u = u.reshape(int(nx), int(nt))

        return X, T, u

if __name__ == '__main__':        
    app = App()