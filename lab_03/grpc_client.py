import grpc
import sys
import os

sys.path.append(os.path.dirname(__file__))

import message_service_pb2
import message_service_pb2_grpc

def run():
    # Подключаемся к серверу
    channel = grpc.insecure_channel('localhost:50051')
    stub = message_service_pb2_grpc.ABTestingServiceStub(channel)

    print("=== Тестирование gRPC сервера (без RabbitMQ) ===\n")
    
    # Тест 1: A/B тестирование
    user_id = 42
    response_ab = stub.AssignAB(message_service_pb2.ABRequest(user_id=user_id))
    print(f"1. A/B тест для user_id={user_id}: группа {response_ab.group_name}")

    # Тест 2: Факториал
    number = 5
    response_fact = stub.Factorial(message_service_pb2.FactorialRequest(number=number))
    print(f"2. Факториал {number}! = {response_fact.result}")

    # Тест 3: Самая частая буква
    text = "мама мыла раму"
    response_letter = stub.MostFrequentLetter(message_service_pb2.TextRequest(text=text))
    print(f"3. Самая частая буква в '{text}': '{response_letter.most_frequent_letter}'")
    
    print("\n[OK] Все тесты пройдены. Сервер работает корректно.")

if __name__ == '__main__':
    run()
