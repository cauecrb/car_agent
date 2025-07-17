import asyncio
from typing import Dict, Any, Callable
from functools import wraps
from infra.database.database import DatabaseManager
from infra.database.car_repository import CarRepository
from infra.database.response_models import SearchResponse, CarResponse
from infra.database.car_filters import CarFilters
from .protocols import MCPRequest, MCPResponse

# Decorador para métodos para tratamento de erro
def mcp_method(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            raise Exception(f"Erro em {func.__name__}: {str(e)}")
    return wrapper

class CarMCPServer:
    
    def __init__(self):
        self.db = DatabaseManager()
        self.car_repo = CarRepository(self.db)
        self.running = False
        
        # Mapeamento de métodos
        self._method_handlers = {
            "search_cars": self._search_cars,
            "get_car_details": self._get_car_details,
            "get_available_brands": self._get_available_brands,
            "get_price_range": self._get_price_range,
            "get_year_range": self._get_year_range,
            "get_car_statistics": self._get_car_statistics,
            "get_car_metrics": self._get_car_metrics
        }
    
    async def start(self):
        self.running = True
        print("Servidor iniciado...")
        
    async def stop(self):
        self.running = False
        print("Servidor parado.")
        
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        try:
            handler = self._method_handlers.get(request.method)
            if not handler:
                return MCPResponse(
                    error=f"Método não suportado: {request.method}", 
                    id=request.id
                )
            
            # Chama o handler apropriado
            if request.method in ["search_cars", "get_car_details", "get_car_metrics"]:
                result = await handler(request.params)
            else:
                result = await handler()
                
            return MCPResponse(result=result, id=request.id)
            
        except Exception as e:
            return MCPResponse(error=str(e), id=request.id)
    
    @mcp_method
    async def _search_cars(self, params: Dict[str, Any]) -> Dict[str, Any]:
        validated_params = self._validate_search_params(params)
        search_response = self.car_repo.search_cars_optimized(validated_params)
        return search_response.dict()
    
    @mcp_method
    async def _get_car_details(self, params: Dict[str, Any]) -> Dict[str, Any]:
        car_id = params.get("car_id")
        if not car_id:
            raise ValueError("ID do carro é obrigatório")
            
        car_response = self.car_repo.get_car_by_id(car_id)
        return car_response.dict()
    
    #apartir daqui vamos retornar dados especificos
    #marcas
    @mcp_method
    async def _get_available_brands(self) -> Dict[str, Any]:
        return self.car_repo.get_available_brands()
    
    #faixa de preços
    @mcp_method
    async def _get_price_range(self) -> Dict[str, Any]:
        return self.car_repo.get_price_range()

    #anos 
    @mcp_method
    async def _get_year_range(self) -> Dict[str, Any]:
        return self.car_repo.get_year_range()
    
    #estatisticas gerais de um carro
    @mcp_method
    async def _get_car_statistics(self) -> Dict[str, Any]:
        return self.car_repo.get_car_statistics()
    
    @mcp_method
    async def _get_car_metrics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            return self.db.get_car_metrics()
        except Exception as e:
            raise Exception(f"Erro ao obter métricas dos carros: {str(e)}")
    
    def _validate_search_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            from infra.database.car_filters import CarFilters
            filters = CarFilters(**params)
            return filters.dict(exclude_none=True)
        except Exception:
            return {k: v for k, v in params.items() if v is not None}