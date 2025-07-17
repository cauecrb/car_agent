from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CarResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    ano: int
    ano_modelo: Optional[int] = None
    cor: str
    quilometragem: int
    preco: float
    combustivel: str
    transmissao: str
    placa: str
    numero_portas: int
    motorizacao: str
    tipo_veiculo: str
    chassi: str
    data_cadastro: Optional[datetime] = None
    data_ultima_revisao: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Para Pydantic v2
        # Mapeamento de campos do modelo SQLAlchemy
        field_mapping = {
            'ano': 'ano_fabricacao',
            'combustivel': 'tipo_combustivel',
        }
    
    @classmethod
    def from_orm(cls, car):
        """Converte CarroDB para CarResponse"""
        return cls(
            id=car.id,
            marca=car.marca,
            modelo=car.modelo,
            ano=car.ano_fabricacao,
            ano_modelo=car.ano_modelo,
            cor=car.cor,
            quilometragem=car.quilometragem,
            preco=float(car.preco),
            combustivel=car.tipo_combustivel.value,
            transmissao=car.transmissao.value,
            placa=car.placa,
            numero_portas=car.numero_portas,
            motorizacao=car.motorizacao,
            tipo_veiculo=car.tipo_veiculo.value,
            chassi=car.chassi,
            data_cadastro=car.data_cadastro,
            data_ultima_revisao=car.data_ultima_revisao
        )

class SearchResponse(BaseModel):
    total_encontrados: int
    total_exibidos: int
    offset: int
    limit: int
    carros: List[CarResponse]

class StatsResponse(BaseModel):
    total_carros: int
    preco_stats: dict
    por_marca: dict

class BrandsResponse(BaseModel):
    marcas: List[str]
    total: int

class RangeResponse(BaseModel):
    min: float
    max: float
    media: Optional[float] = None