"""MCP (Model Context Protocol) package for car operations

Este módulo implementa um cliente e servidor MCP para operações
com carros, incluindo busca, detalhes e estatísticas.
"""

from .protocols import MCPRequest, MCPResponse
from .server import CarMCPServer
from .client import CarMCPClient

# Versão do protocolo
__version__ = "1.0.0"

__all__ = [
    'MCPRequest',
    'MCPResponse', 
    'CarMCPServer',
    'CarMCPClient',
    '__version__'
]