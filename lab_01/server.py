import grpc
from concurrent import futures
import data_pb2
import data_pb2_grpc


class DataProcessor(data_pb2_grpc.DataProcessorServicer):

    def ProcessDataBatch(self, request_iterator, context):
        values = []

        for data in request_iterator:
            print("Получено:", data.value)
            values.append(data.value)

        total = sum(values)
        avg = total / len(values) if values else 0

        print("Сумма:", total)
        print("Среднее:", avg)

        return data_pb2.Result(
            sum=total,
            average=avg
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pb2_grpc.add_DataProcessorServicer_to_server(DataProcessor(), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    print("Server started on port 50051")

    server.wait_for_termination()


if __name__ == '__main__':
    serve()