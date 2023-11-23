from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey 
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Criando coneção com banco de dados
engine = create_engine('sqlite:///dados/banco.db', echo=True)
engine2 = create_engine('sqlite:///dados/banco_test.db', echo=True)
engine3 = create_engine('sqlite:///dados/boot.db', echo=True)


# Declarando base da classe
Base = declarative_base()
# Criando um sessão com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()


# Declarando/Mapeando tabela usando base criada
class Mensagens(Base):
    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True)
    inscricao = Column(Integer, nullable=False)
    cliente = Column(String, nullable=False)
    telefone = Column(Integer, nullable=False)
    enviado = Column(Boolean, nullable=False)
    data_enviada = Column(Date, default=datetime.now().date())

    def __repr__(self):
        return f"Incrição: {self.inscricao}, Cliente: {self.cliente}, Telefone: {self.telefone}, Enviado: {self.enviado}, Data: {self.data_enviada}"


class BootRespostasMenu(Base):
    __tablename__ = "boot_respostas"

    id = Column(Integer, primary_key=True)
    cliente = Column(String, nullable=False)
    telefone = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    data_enviada = Column(Date, default=datetime.now().date())

    def __repr__(self):
        return f"Cliente: {self.cliente}, Telefone: {self.telefone}, Status: {self.status}, Data: {self.data_enviada}"


class BootHistorico(Base):
    __tablename__ = "boot_historico"

    id = Column(Integer, primary_key=True)
    cliente = Column(String, nullable=False)
    telefone = Column(Integer, nullable=False)
    mensagem_cliente = Column(String, nullable=False)
    mensagem_boot = Column(String, nullable=False)

    def __repr__(self):
        return f"Cliente: {self.cliente}, Telefone: {self.telefone}, Mensagem do cliente: {self.mensagem_cliente}, Mensagem do Boot: {self.mensagem_boot}"


# Criando tabelas
# Base.metadata.create_all(engine)
# Base.metadata.create_all(engine2)
