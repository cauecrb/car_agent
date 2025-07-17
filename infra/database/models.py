from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum as SQLEnum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Importar os Enums do modelo existente
from model.enums import TipoCombustivel, TipoTransmissao, TipoVeiculo

Base = declarative_base()

class CarroDB(Base):
    __tablename__ = 'carros'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String(50), nullable=False, index=True)
    modelo = Column(String(100), nullable=False, index=True)
    ano_fabricacao = Column(Integer, nullable=False, index=True)
    ano_modelo = Column(Integer, nullable=False)
    motorizacao = Column(String(20), nullable=False)
    tipo_combustivel = Column(SQLEnum(TipoCombustivel), nullable=False)
    transmissao = Column(SQLEnum(TipoTransmissao), nullable=False)
    numero_portas = Column(Integer, nullable=False)
    tipo_veiculo = Column(SQLEnum(TipoVeiculo), nullable=False)
    quilometragem = Column(Integer, nullable=False)
    cor = Column(String(30), nullable=False)
    preco = Column(Float, nullable=False, index=True)
    placa = Column(String(10), unique=True, nullable=False)
    chassi = Column(String(20), unique=True, nullable=False)
    data_cadastro = Column(DateTime, default=datetime.now)
    data_ultima_revisao = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Carro(marca='{self.marca}', modelo='{self.modelo}', ano={self.ano_fabricacao})>"
    
    # Índices compostos para consultas comuns
    __table_args__ = (
        Index('idx_marca_modelo', 'marca', 'modelo'),
        Index('idx_preco_ano', 'preco', 'ano_fabricacao'),
    )