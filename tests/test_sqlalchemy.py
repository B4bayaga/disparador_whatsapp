import pytest
from dados import connection
from sqlalchemy.orm import sessionmaker
from datetime import datetime


@pytest.fixture
def session():
    """
    Cria uma sessão do SQLAlchemy para os testes
    """
    Session = sessionmaker(bind=connection.engine2)
    session = Session()
    yield session
    session.rollback()
    session.close()



def test_repr(session):
    """
    Testa o método __repr__() da classe Mensagens
    """
    mensagem = connection.Mensagens(inscricao=1548, cliente="Rafael", telefone=123456789, enviado=True)
    session.add(mensagem)
    session.commit()

    assert repr(mensagem) == "Incrição: 1548, Cliente: Rafael, Telefone: 123456789, Enviado: True, Data: {}".format(datetime.now().date())


def test_insert(session):
    """
    Testa o método insert da classe Mensagens
    """
    mensagem = connection.Mensagens(inscricao=1548, cliente="Rafa Oliveira", telefone=77999548524, enviado=True)
    session.add(mensagem)
    session.commit()
    pessoas = session.query(connection.Mensagens).filter_by(cliente="Rafa Oliveira").all()
    # Verifica se os valores foram corretamente inseridos no objeto Mensagens
    for pessoa in pessoas:
        assert pessoa.cliente == "Rafa Oliveira"
        assert pessoa.telefone == 77999548524
        assert pessoa.enviado == True
        assert pessoa.data_enviada == datetime.now().date()


def test_insert_session(session):

    """
    Verifica se o objeto foi adicionado à sessão e comitado corretamente
    """
    mensagem = connection.Mensagens(inscricao=1548, cliente="Pax Nacional", telefone=7794247117, enviado=True)
    session.add(mensagem)
    session.commit()
    pessoas = session.query(connection.Mensagens).filter_by(cliente="Pax Nacional").first()
    assert pessoas in session
    session.refresh(pessoas)
    assert pessoas.id is not None


def test_delete_all(session):
    """
    Deleta todas as mensagens do banco de dados
    """
    session.query(connection.Mensagens).delete()
    session.commit()
    assert session.query(connection.Mensagens).count() == 0
