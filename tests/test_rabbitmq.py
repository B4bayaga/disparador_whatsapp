import pytest
from RabbitMQ.consumidor_basico import consumidor
from RabbitMQ.publisher import RabbitMqPublisher
import json


@pytest.fixture
def session_publisher() -> None:
    """
    Publicando uma mensagem RabbitMQ
    """
    publisher = RabbitMqPublisher()
    publisher.send_message({'Cliente': 'Rafael', 'numero': 77992129494})
    return None


def test_consumidor_basico_menssageria_none():
    """
    Verifica se o objeto foi adicionado à sessão e comitado corretamente
    """
    mensagem = consumidor()
    assert mensagem is None


def test_consumidor_basico_menssageria_comitado(session_publisher):
    """
    Verifica se o objeto foi adicionado à sessão e comitado corretamente
    """
    mensagem = consumidor()
    assert mensagem is not None


def test_consumidor_basico_testa_conteudo_mensagem(session_publisher):
    """
    Verifica se o objeto foi adicionado à sessão e comitado corretamente
    """
    mensagem = consumidor()
    mensagem = json.loads(mensagem)
    assert mensagem == {'Cliente': 'Rafael', 'numero': 77992129494}
