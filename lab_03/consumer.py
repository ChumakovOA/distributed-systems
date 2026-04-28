import pika
import grpc
import sys
import os

# Добавляем путь к папке с gRPC модулями
sys.path.append(os.path.join(os.path.dirname(__file__), '../grpc_part'))
import message_service_pb2
import message_service_pb2_grpc

def process_via_grpc(prefix, data):
    """
    Функция, которая в зависимости от префикса вызывает
    соответствующий метод gRPC сервера.
    """
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_service_pb2_grpc.ABTestingServiceStub(channel)
        
        if prefix == 'subscribe':
            # A/B тестирование
            try:
                user_id = int(data.strip())
                request = message_service_pb2.ABRequest(user_id=user_id)
                response = stub.AssignAB(request)
                return f"Пользователь {user_id} попал в группу {response.group_name}"
            except ValueError:
                return f"Ошибка: для A/B теста нужно число (ID пользователя), получено: '{data}'"
                
        elif prefix == 'pass':
            # Факториал
            try:
                num = int(data.strip())
                if num < 0:
                    return f"Ошибка: факториал для отрицательного числа ({num}) не определен."
                request = message_service_pb2.FactorialRequest(number=num)
                response = stub.Factorial(request)
                return f"Факториал {num}! = {response.result}"
            except ValueError:
                return f"Ошибка: для факториала нужно число, получено: '{data}'"
                
        elif prefix == 'freq':
            # Самая частая буква
            text = data.strip()
            request = message_service_pb2.TextRequest(text=text)
            response = stub.MostFrequentLetter(request)
            if response.most_frequent_letter:
                return f"Самая частая буква в '{text}': '{response.most_frequent_letter}'"
            else:
                return f"В тексте '{text}' нет букв."
        else:
            return f"Неизвестный префикс: '{prefix}'. Используйте 'subscribe:', 'pass:' или 'freq:'."

def callback(ch, method, properties, body):
    """Функция, которая будет вызвана при получении сообщения из очереди."""
    message_str = body.decode('utf-8')
    print(f" [Consumer] Получено сообщение: '{message_str}'")
    
    if ':' not in message_str:
        result = f"Ошибка: Неверный формат сообщения. Нет двоеточия. Пример: 'subscribe:123'"
        print(f" [Consumer] {result}")
    else:
        prefix, data = message_str.split(':', 1)
        print(f" [Consumer] Префикс: '{prefix}', Данные: '{data}'")
        result = process_via_grpc(prefix, data)
        print(f" [Consumer] Результат: {result}")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials)
    )
    channel = connection.channel()
    
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    
    print(' [Consumer] Ожидание сообщений. Для выхода нажмите CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' [Consumer] Завершение работы...')
        sys.exit(0)
