import grpc
from concurrent import futures
import random
import math
import sys
import os

# Добавляем текущую директорию в путь для импорта сгенерированных модулей
sys.path.append(os.path.dirname(__file__))

import message_service_pb2
import message_service_pb2_grpc

# Класс, реализующий логику, описанную в .proto файле
class ABTestingServicer(message_service_pb2_grpc.ABTestingServiceServicer):

    # --- 1. Задание: A/B тестирование ---
    def AssignAB(self, request, context):
        user_id = request.user_id
        # Простая логика распределения: четные - в группу A, нечетные - в B
        if user_id % 2 == 0:
            group = "A"
        else:
            group = "B"
        print(f"[gRPC Server] A/B запрос: user_id={user_id} -> группа {group}")
        return message_service_pb2.ABResponse(group_name=group)

    # --- 2. Задание: Факториал ---
    def Factorial(self, request, context):
        n = request.number
        if n < 0:
            result = -1
        else:
            result = math.factorial(n)
        print(f"[gRPC Server] Факториал запрос: number={n} -> result={result}")
        return message_service_pb2.FactorialResponse(result=result)

    # --- 3. Задание: Самая частая буква ---
    def MostFrequentLetter(self, request, context):
        text = request.text
        if not text:
            return message_service_pb2.LetterResponse(most_frequent_letter="")

        # Приводим к нижнему регистру для учета регистра
        text_lower = text.lower()
        
        # Считаем частоту только букв
        freq = {}
        for char in text_lower:
            if char.isalpha():
                freq[char] = freq.get(char, 0) + 1
        
        if not freq:
            return message_service_pb2.LetterResponse(most_frequent_letter="")
        
        # Находим букву с максимальной частотой
        most_frequent = max(freq, key=freq.get)
        print(f"[gRPC Server] Поиск букв запрос: text='{text[:30]}...' -> буква='{most_frequent}'")
        return message_service_pb2.LetterResponse(most_frequent_letter=most_frequent)


def serve():
    # Создаем gRPC сервер с пулом потоков
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Регистрируем наш сервис
    message_service_pb2_grpc.add_ABTestingServiceServicer_to_server(ABTestingServicer(), server)
    # Слушаем порт 50051 на всех интерфейсах
    server.add_insecure_port('[::]:50051')
    print("[gRPC Server] Запущен на порту 50051...")
    server.start()
    # Блокируем main поток, чтобы сервер работал вечно
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
