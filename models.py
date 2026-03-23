from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True)
    assunto = Column(String)
    acao = Column(String)
    descricao = Column(String)
    observacoes = Column(String)
    status = Column(String)
    prioridade = Column(String)
    responsavel = Column(String)
    envolvidos = Column(String)
    prazo = Column(String)
    data_criacao = Column(DateTime, default=datetime.now)
    ultima_atualizacao = Column(DateTime, default=datetime.now)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    perfil = Column(String)