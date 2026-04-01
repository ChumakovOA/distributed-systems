import grpc
import data_pb2
import data_pb2_grpc


def generate_data():
    print("Вводите числа. Для завершения введите 'stop'")

    while True:
        value = input("Введите число: ")

        if value.lower() == "stop":
            break

        yield data_pb2.DataPoint(value=int(value))


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = data_pb2_grpc.DataProcessorStub(channel)

    response = stub.ProcessDataBatch(generate_data())

    print("Сумма:", response.sum)
    print("Среднее:", response.average)


if __name__ == '__main__':
    run()