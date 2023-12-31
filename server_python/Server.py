import grpc
import numpy as np
from concurrent import futures

import CalculateService_pb2_grpc as pb2_grpc
import CalculateService_pb2 as pb2

class CalculateService(pb2_grpc.CalculateServiceServicer):

    def Calculate(self, input, context):

        a0 = 1.0
        a1 = 4.4
        a2 = 53.2
        a3 = 12.0
        u = 10.0
        X0_0 = input.X0_0
        X0_1 = input.X0_1
        X0_2 = input.X0_2

        z1 = (-a0 / a3)
        z2 = (-a1 / a3)
        z3 = (-a2 / a3)
        z4 = (1 / a3)
        h = input.h

        A = np.array([[0, 1, 0], [0, 0, 1], [z1, z2, z3]])
        B = np.array([[0], [0], [z4]])

        X0 = np.array([[X0_0], [X0_1], [X0_2]])
        X = (A @ X0 + B * u) * h + X0
        X_next = X + h * ((3 / 2) * (A @ X + B * u) - (1 / 2) * (A @ X0 + B * u))

        return pb2.Output(X_0=X[0][0], X_1=X[1][0], X_2=X[2][0], X_next_0=X_next[0][0], X_next_1=X_next[1][0], X_next_2=X_next[2][0])

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