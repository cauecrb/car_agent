import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, CarroDB
from model.carros import carro
from infra.config.settings import settings

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = settings.DATABASE_PATH
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        return self.SessionLocal()
        
    def insert_carros(self, carros_list):
        session = self.get_session()
        try:
            carros_db = []
            for carro_obj in carros_list:
                carro_db = CarroDB(
                    marca=carro_obj.marca,
                    modelo=carro_obj.modelo,
                    ano_fabricacao=carro_obj.ano,
                    ano_modelo=carro_obj.ano_modelo,
                    motorizacao=carro_obj.motorizacao,
                    tipo_combustivel=carro_obj.tipo_combustivel,
                    transmissao=carro_obj.transmissao,
                    numero_portas=carro_obj.numero_portas,
                    tipo_veiculo=carro_obj.tipo_veiculo,
                    quilometragem=carro_obj.quilometragem,
                    cor=carro_obj.cor,
                    preco=carro_obj.preco,
                    placa=carro_obj.placa,
                    chassi=carro_obj.chassi,
                    data_cadastro=carro_obj.data_cadastro,
                    data_ultima_revisao=carro_obj.data_ultima_revisao
                )
                carros_db.append(carro_db)
            
            session.add_all(carros_db)
            session.commit()
            return len(carros_db)
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def get_all_carros(self):
        session = self.get_session()
        try:
            return session.query(CarroDB).all()
        finally:
            session.close()
            
    def get_carros_by_marca(self, marca):
        session = self.get_session()
        try:
            return session.query(CarroDB).filter(CarroDB.marca == marca).all()
        finally:
            session.close()
            
    def get_carros_by_preco_range(self, preco_min, preco_max):
        session = self.get_session()
        try:
            return session.query(CarroDB).filter(
                CarroDB.preco >= preco_min,
                CarroDB.preco <= preco_max
            ).all()
        finally:
            session.close()
            
    def get_carros_by_ano(self, ano):
        session = self.get_session()
        try:
            return session.query(CarroDB).filter(CarroDB.ano_fabricacao == ano).all()
        finally:
            session.close()
            
    def count_carros(self):
        session = self.get_session()
        try:
            return session.query(CarroDB).count()
        finally:
            session.close()
            
    def search_by_placa(self, placa):
        session = self.get_session()
        try:
            return session.query(CarroDB).filter(CarroDB.placa == placa).first()
        finally:
            session.close()
            
    def search_by_chassi(self, chassi):
        session = self.get_session()
        try:
            return session.query(CarroDB).filter(CarroDB.chassi == chassi).first()
        finally:
            session.close()
    
    def get_car_metrics(self):
        from sqlalchemy import inspect
        
        inspector = inspect(CarroDB)
        columns = inspector.columns
        
        metrics = []
        
        # Mapear nomes di banco
        friendly_names = {
            'id': 'ID do carro',
            'marca': 'Marca',
            'modelo': 'Modelo', 
            'ano_fabricacao': 'Ano de fabricação',
            'ano_modelo': 'Ano do modelo',
            'motorizacao': 'Motorização',
            'tipo_combustivel': 'Tipo de combustível',
            'transmissao': 'Tipo de transmissão',
            'numero_portas': 'Número de portas',
            'tipo_veiculo': 'Tipo de veículo',
            'quilometragem': 'Quilometragem do carro',
            'cor': 'Cor do carro',
            'preco': 'Preço do carro',
            'placa': 'Placa do veículo',
            'chassi': 'Chassi do veículo',
            'data_cadastro': 'Data de cadastro',
            'data_ultima_revisao': 'Data da última revisão'
        }
        
        for column in columns:
            column_name = column.name
            friendly_name = friendly_names.get(column_name, column_name)
            
            # tipo da coluna de forma simples
            column_type = str(column.type)
            if 'ENUM' in column_type:
                column_type = 'Lista de opções'
            elif 'INTEGER' in column_type:
                column_type = 'Número'
            elif 'FLOAT' in column_type:
                column_type = 'Valor decimal'
            elif 'STRING' in column_type:
                column_type = 'Texto'
            
            metrics.append({
                'campo': column_name,
                'nome': friendly_name,
                'tipo': column_type,
                'obrigatorio': not column.nullable
            })
        
        return {
            'total_metricas': len(metrics),
            'metricas': metrics
        }