import pika
import sys

def main():
    # Проверяем, передан ли аргумент
    if len(sys.argv) < 2:
        print("Usage: python producer.py '<message>'")
        print("Пример: python producer.py 'subscribe:42'")
        print("Префиксы: subscribe:, pass:, freq:")
        sys.exit(1)
    
    message = ' '.join(sys.argv[1:])
    
    # Подключение к RabbitMQ
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials)
    )
    channel = connection.channel()
    
    # Объявляем очередь (создаем, если ее нет)
    channel.queue_declare(queue='task_queue', durable=True)
    
    # Отправляем сообщение
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    print(f" [Producer] Отправлено сообщение: '{message}'")
    connection.close()

if __name__ == '__main__':
    main()
