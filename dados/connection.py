from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Criando coneção com banco de dados
engine = create_engine('sqlite:///banco.db', echo=True)

# Declarando base da classe
Base = declarative_base()
# Criando um sessão com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()


# Declarando/Mapeando tabela usando base criada
class Mensagens(Base):
    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True)
    cliente = Column(String, nullable=False)
    telefone = Column(Integer, nullable=False)
    enviado = Column(Boolean, nullable=False)
    data_enviada = Column(Date, default=datetime.now().date())

    def __repr__(self):
        return f"Cliente: {self.cliente}, Telefone: {self.telefone}, Enviado: {self.enviado}, Data: {self.data_enviada}"


# Criando tabelas
Base.metadata.create_all(engine)
