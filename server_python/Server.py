import grpc
from concurrent import futures
import numpy as np

import CalculateService_pb2_grpc as pb2_grpc
import CalculateService_pb2 as pb2

class CalculateService(pb2_grpc.CalculateServiceServicer):

    def Calculate(self, input, context):
        L = input.L                     # Длина струны
        T = input.T                     # Максимальное время
        nx = int(input.nx)              # Количество точек по x
        nt = int(input.nt)              # Количество точек по t
        c = input.c                     # Скорость волны в струне

        dx, dt = L/nx,  T/nt

        u = np.zeros((nt, nx))          # Вертикальное смещение
        v = np.zeros((nt, nx))          # Вертикальная скорость

        u[0,:] = np.sin(np.pi * np.arange(0, L, L/nx))      # Начальные условия
        v[0,:] = np.sin(np.pi * np.arange(0, L, L/nx))

        u[:,0] = u[:,-1] = v[:,0] = v[:,-1] = 0             # Граничные условия

        for n in range(0, nt-1):                            # Применение метода конечных разностей
            for i in range(1, nx-1):
                u[n+1, i] = u[n, i] + dt * v[n, i]
                v[n+1, i] = v[n, i] + c**2 * (dt / dx**2) * (u[n, i+1] - 2 * u[n, i] + u[n, i-1])

        X, T = np.meshgrid(np.linspace(0, L, nx), np.linspace(0, T, nt))        # Данные для формирования ответа

        return pb2.Output(X=X.reshape(nx*nt), T=T.reshape(nx*nt), u=u.reshape(nx*nt))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_CalculateServiceServicer_to_server(
        CalculateService(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination() 

if __name__ == "__main__":
    serve()