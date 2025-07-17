from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from .models import CarroDB
from .database import DatabaseManager
from .car_filters import CarFilters
from .response_models import CarResponse, SearchResponse

class CarRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def search_cars_optimized(self, filters: Dict[str, Any]) -> SearchResponse:
        """Busca otimizada usando Pydantic filters e response models"""
        session = self.db_manager.get_session()
        try:
            # Validar e criar filtros
            car_filters = CarFilters(**filters)
            
            # Query base usando select
            stmt = select(CarroDB)
            
            # Aplicar filtros automaticamente
            stmt = car_filters.apply_to_statement(stmt)
            
            # Contar total
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total_count = session.execute(count_stmt).scalar()
            
            # Aplicar ordenação e paginação
            stmt = self._apply_ordering(stmt, car_filters.order_by)
            stmt = stmt.offset(car_filters.offset).limit(car_filters.limit)
            
            # Executar query
            result = session.execute(stmt)
            carros = result.scalars().all()
            
            # Converter para CarResponse usando Pydantic
            car_responses = [CarResponse.from_orm(car) for car in carros]
            
            return SearchResponse(
                total_encontrados=total_count,
                total_exibidos=len(car_responses),
                offset=car_filters.offset,
                limit=car_filters.limit,
                carros=car_responses
            )
        finally:
            session.close()
    
    def get_car_by_id(self, car_id: int) -> CarResponse:
        """Obtém um carro específico por ID usando CarResponse"""
        session = self.db_manager.get_session()
        try:
            car = session.query(CarroDB).filter(CarroDB.id == car_id).first()
            
            if not car:
                raise ValueError(f"Carro com ID {car_id} não encontrado")
            
            return CarResponse.from_orm(car)
        finally:
            session.close()
    
    def get_available_brands(self) -> Dict[str, Any]:
        """Retorna marcas disponíveis usando agregação SQL otimizada"""
        session = self.db_manager.get_session()
        try:
            stmt = select(distinct(CarroDB.marca)).order_by(CarroDB.marca)
            result = session.execute(stmt)
            marcas = [row[0] for row in result]
            
            return {"marcas": marcas, "total": len(marcas)}
        finally:
            session.close()
    
    def get_car_statistics(self) -> Dict[str, Any]:
        session = self.db_manager.get_session()
        try:
            from sqlalchemy import func
            from .models import CarroDB
            
            # Total de carros
            total_carros = session.query(CarroDB).count()
            
            if total_carros == 0:
                return {
                    "total_carros": 0,
                    "por_marca": {},
                    "por_combustivel": {},
                    "por_transmissao": {},
                    "faixa_preco": {"min": 0, "max": 0, "media": 0}
                }
            
            # Estatísticas por marca
            por_marca = {}
            marca_stats = session.query(
                CarroDB.marca, 
                func.count(CarroDB.id)
            ).group_by(CarroDB.marca).all()
            
            for marca, count in marca_stats:
                por_marca[marca] = count
            
            # Estatísticas por combustível
            por_combustivel = {}
            combustivel_stats = session.query(
                CarroDB.tipo_combustivel,
                func.count(CarroDB.id)
            ).group_by(CarroDB.tipo_combustivel).all()
            
            for combustivel, count in combustivel_stats:
                por_combustivel[combustivel.value] = count
            
            # Estatísticas por transmissão
            por_transmissao = {}
            transmissao_stats = session.query(
                CarroDB.transmissao,
                func.count(CarroDB.id)
            ).group_by(CarroDB.transmissao).all()
            
            for transmissao, count in transmissao_stats:
                por_transmissao[transmissao.value] = count
            
            # Faixa de preços
            preco_stats = session.query(
                func.min(CarroDB.preco),
                func.max(CarroDB.preco),
                func.avg(CarroDB.preco)
            ).first()
            
            min_preco, max_preco, avg_preco = preco_stats
            
            return {
                "total_carros": total_carros,
                "por_marca": por_marca,
                "por_combustivel": por_combustivel,
                "por_transmissao": por_transmissao,
                "faixa_preco": {
                    "min": float(min_preco) if min_preco else 0,
                    "max": float(max_preco) if max_preco else 0,
                    "media": float(avg_preco) if avg_preco else 0
                }
            }
            
        finally:
            session.close()
    
    def get_price_range(self) -> Dict[str, Any]:
        """Retorna faixa de preços usando agregação SQL"""
        session = self.db_manager.get_session()
        try:
            price_stats = session.query(
                func.min(CarroDB.preco).label('min_preco'),
                func.max(CarroDB.preco).label('max_preco'),
                func.avg(CarroDB.preco).label('avg_preco')
            ).first()
            
            return {
                "min": float(price_stats.min_preco) if price_stats.min_preco else 0,
                "max": float(price_stats.max_preco) if price_stats.max_preco else 0,
                "media": float(price_stats.avg_preco) if price_stats.avg_preco else 0
            }
        finally:
            session.close()
    
    def get_year_range(self) -> Dict[str, Any]:
        """Retorna faixa de anos usando agregação SQL"""
        session = self.db_manager.get_session()
        try:
            year_stats = session.query(
                func.min(CarroDB.ano_fabricacao).label('min_ano'),
                func.max(CarroDB.ano_fabricacao).label('max_ano')
            ).first()
            
            return {
                "min": year_stats.min_ano if year_stats.min_ano else 0,
                "max": year_stats.max_ano if year_stats.max_ano else 0
            }
        finally:
            session.close()
    
    def _apply_ordering(self, stmt, order_by: str):
        """Aplica ordenação de forma dinâmica"""
        order_mapping = {
            'preco_asc': CarroDB.preco.asc(),
            'preco_desc': CarroDB.preco.desc(),
            'quilometragem_asc': CarroDB.quilometragem.asc(),
            'ano_desc': CarroDB.ano_fabricacao.desc()
        }
        
        if order_by and order_by in order_mapping:
            stmt = stmt.order_by(order_mapping[order_by])
        
        return stmt