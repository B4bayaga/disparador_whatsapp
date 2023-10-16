from typing import Dict
import pika
import json


class RabbitMqPublisher:
    def __init__(self) -> None:
        # Configurações de conexão
        self.__host = 'localhost'
        self.__port = 5672
        self.__username = 'admin'
        self.__password = 'admin'

        # Configurações do publicador
        self.__exchange = 'teste_exchange'
        self.__routing_key = ''
        self.__chennel = self.__crate_channel()

    def __crate_channel(self):
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
        return channel

    def send_message(self, body: Dict) -> None:
        # Envia uma mensagem para o RabbitMQ
        self.__chennel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )


if __name__ == '__main__':
    # Cria uma instância do publicador
    publisher = RabbitMqPublisher()

    # Exemplo de envio de mensagens
    teste = [
        {'Cliente': 'Rafael', 'numero': 77992129494},
        {"Cliente": "Renata", "numero": "77992129494"},
        {"Cliente": "Lucas", "numero": "77992129494"},
        {"Cliente": "Louise", "numero": "77992129494"},
        {"Cliente": "Rafael Benício", "numero": "77992129494"},
    ]
    for i in teste:
        publisher.send_message(i)
