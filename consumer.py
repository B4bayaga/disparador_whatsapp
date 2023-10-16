import pika
import json
from disparadorApp import DisparadorApp
from time import sleep


class rabbitMqConsumer:
    def __init__(self, callback) -> None:
        # Configurações de conexão
        self.__host = 'localhost'
        self.__port = 5672
        self.__username = 'admin'
        self.__password = 'admin'

        # Configurações do consumidor
        self.__queue = 'teste_fila'
        self.__callback = callback
        self.__chennel = self.__crate_channel()

    def __crate_channel(self) -> None:
        # Cria uma conexão com o RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.__host, 
                port=self.__port,
                credentials=pika.PlainCredentials(
                    self.__username,
                    self.__password
                )
            )
        )
        channel = connection.channel()

        # Declara a fila e suas configurações
        channel.queue_declare(queue=self.__queue, durable=True)

        # Configura o consumo da fila
        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )
        return channel

    def start(self):
        # Inicia o consumo da fila
        print(f'Escutando porta {self.__port}')
        self.__chennel.basic_get()


def minha_callback(ch, method, properties, body, ):
    # Função de callback para processar as mensagens recebidas
    fila = json.loads(body)
    return fila


if __name__ == '__main__':
    # Cria uma instância do consumidor e inicia o consumo
    consumer = rabbitMqConsumer(minha_callback)
    consumer.start()
