from typing import Dict, Any
from .protocols import MCPRequest
from .server import CarMCPServer

class CarMCPClient:    
    def __init__(self, server: CarMCPServer):
        self.server = server
        
    async def search_cars(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        request = MCPRequest(method="search_cars", params=filters)
        response = await self.server.handle_request(request)
        
        if response.error:
            raise Exception(f"Erro no servidor: {response.error}")
            
        return response.result
        
    async def get_car_details(self, car_id: int) -> Dict[str, Any]:
        request = MCPRequest(method="get_car_details", params={"car_id": car_id})
        response = await self.server.handle_request(request)
        
        if response.error:
            raise Exception(f"Erro no servidor: {response.error}")
            
        return response.result
        
    async def get_available_brands(self) -> Dict[str, Any]:
        request = MCPRequest(method="get_available_brands", params={})
        response = await self.server.handle_request(request)
        
        if response.error:
            raise Exception(f"Erro no servidor: {response.error}")
            
        return response.result
        
    async def get_price_range(self) -> Dict[str, Any]:
        request = MCPRequest(method="get_price_range", params={})
        response = await self.server.handle_request(request)
        
        if response.error:
            raise Exception(f"Erro no servidor: {response.error}")
            
        return response.result
        
    async def get_year_range(self) -> Dict[str, Any]:
        request = MCPRequest(method="get_year_range", params={})
        response = await self.server.handle_request(request)
        
        if response.error:
            raise Exception(f"Erro no servidor: {response.error}")
            
        return response.result
        
    async def get_car_metrics(self) -> Dict[str, Any]:
        request = MCPRequest(method="get_car_metrics", params={})
        response = await self.server.handle_request(request)
        
        if response.error:
            raise Exception(f"Erro no servidor: {response.error}")
            
        return response.result
        
    async def get_car_statistics(self) -> Dict[str, Any]:
        request = MCPRequest(method="get_car_statistics", params={})
        response = await self.server.handle_request(request)
        
        if response.error:
            raise Exception(f"Erro no servidor: {response.error}")
            
        return response.result