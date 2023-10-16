import pika
import json


def consumidor():
    # Configurar a conexão com o RabbitMQ
    connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='localhost',
                    port=5672,
                    credentials=pika.PlainCredentials('admin', 'admin')
                ))
    channel = connection.channel()

    # Declarar a fila que você deseja consumir
    queue_name = 'teste_fila'
    channel.queue_declare(queue=queue_name, durable=True)

    # Consumir uma única mensagem da fila
    method_frame, header_frame, body = channel.basic_get(
        queue=queue_name,
        auto_ack=True
    )

    return body


if __name__ == '__main__':
    corpo = consumidor()
    print(corpo)
