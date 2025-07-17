import pytest
import asyncio
import os
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any

# Configurar variáveis de ambiente para testes
os.environ['OPENAI_API_KEY'] = 'test-key'
os.environ['DEBUG'] = 'True'

@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para toda a sessão de testes"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_openai_client():
    """Mock do cliente OpenAI"""
    with patch('openai.OpenAI') as mock:
        client = Mock()
        mock.return_value = client
        
        # Mock das respostas da API
        response_mock = Mock()
        response_mock.choices = [Mock()]
        response_mock.choices[0].message.content = '{"needs_search": true, "intent_type": "search", "confidence": 0.9}'
        
        client.chat.completions.create.return_value = response_mock
        yield client

@pytest.fixture
def mock_database_context():
    """Contexto mock do banco de dados"""
    return {
        "total_cars": 100,
        "brands": ["Toyota", "Honda", "Ford"],
        "price_range": {"min": 20000, "max": 80000, "media": 45000},
        "year_range": {"min": 2015, "max": 2024},
        "brand_distribution": {"Toyota": 30, "Honda": 25, "Ford": 20},
        "formatted_price_range": "R$ 20.000 - R$ 80.000"
    }

@pytest.fixture
def mock_search_results():
    """Resultados mock de busca"""
    return {
        "total_encontrados": 2,
        "carros": [
            {
                "id": 1,
                "marca": "Toyota",
                "modelo": "Corolla",
                "ano": 2022,
                "preco": 85000,
                "cor": "Branco",
                "combustivel": "flex",
                "transmissao": "automatica",
                "portas": 4
            },
            {
                "id": 2,
                "marca": "Honda",
                "modelo": "Civic",
                "ano": 2023,
                "preco": 95000,
                "cor": "Preto",
                "combustivel": "flex",
                "transmissao": "manual",
                "portas": 4
            }
        ]
    }

@pytest.fixture
def mock_car_mcp_server():
    """Mock do servidor MCP"""
    server = AsyncMock()
    server.start = AsyncMock()
    server.stop = AsyncMock()
    return server

@pytest.fixture
def mock_car_mcp_client(mock_search_results, mock_database_context):
    """Mock do cliente MCP"""
    client = AsyncMock()
    client.search_cars = AsyncMock(return_value=mock_search_results)
    client.get_car_statistics = AsyncMock(return_value={"total_carros": 100, "por_marca": {"Toyota": 30}})
    client.get_available_brands = AsyncMock(return_value={"marcas": ["Toyota", "Honda", "Ford"]})
    client.get_price_range = AsyncMock(return_value={"min": 20000, "max": 80000, "media": 45000})
    client.get_year_range = AsyncMock(return_value={"min": 2015, "max": 2024})
    client.get_car_metrics = AsyncMock(return_value={"metricas": [], "total_metricas": 0})
    return client