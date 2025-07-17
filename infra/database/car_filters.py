from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from sqlalchemy import select, and_
from .models import CarroDB

class CarFilters(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    cor: Optional[str] = None
    ano_min: Optional[int] = Field(None, ge=1900, le=2030)
    ano_max: Optional[int] = Field(None, ge=1900, le=2030)
    preco_min: Optional[float] = Field(None, ge=0)
    preco_max: Optional[float] = Field(None, ge=0)
    combustivel: Optional[str] = None
    transmissao: Optional[str] = None
    numero_portas: Optional[int] = Field(None, ge=2, le=5)
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    order_by: Optional[str] = None
    
    @validator('ano_max')
    def validate_year_range(cls, v, values):
        if v and 'ano_min' in values and values['ano_min'] and v < values['ano_min']:
            raise ValueError('ano_max deve ser maior que ano_min')
        return v
    
    @validator('preco_max')
    def validate_price_range(cls, v, values):
        if v and 'preco_min' in values and values['preco_min'] and v < values['preco_min']:
            raise ValueError('preco_max deve ser maior que preco_min')
        return v
    
    def apply_to_statement(self, stmt):
        """Aplica filtros a um statement SQLAlchemy"""
        conditions = []
        
        # Mapeamento dinâmico de filtros
        filter_map = {
            'marca': lambda v: CarroDB.marca.ilike(f"%{v}%"),
            'modelo': lambda v: CarroDB.modelo.ilike(f"%{v}%"),
            'cor': lambda v: CarroDB.cor.ilike(f"%{v}%"),
            'ano_min': lambda v: CarroDB.ano_fabricacao >= v,
            'ano_max': lambda v: CarroDB.ano_fabricacao <= v,
            'preco_min': lambda v: CarroDB.preco >= v,
            'preco_max': lambda v: CarroDB.preco <= v,
            'numero_portas': lambda v: CarroDB.numero_portas == v,
        }
        
        # Aplicar filtros dinamicamente
        for field, value in self.dict(exclude_none=True, exclude={'limit', 'offset', 'order_by'}).items():
            if field in filter_map:
                conditions.append(filter_map[field](value))
        
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        return stmt