import sys
import os
import asyncio
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from infra.database.database import DatabaseManager
from services.ai_service import AIService
from services.response_service import ResponseService
from presentation.mcp.server import CarMCPServer
from presentation.mcp.client import CarMCPClient
from infra.config.settings import settings

class RealCarSearchTester:
    def __init__(self):
        # Inicializar componentes reais
        self.db_manager = DatabaseManager()
        self.ai_service = AIService()
        self.response_service = ResponseService(self.ai_service)
        self.mcp_server = CarMCPServer()
        self.mcp_client = CarMCPClient(self.mcp_server)
        
        # Verificar se o banco tem dados
        self.total_cars = self.db_manager.count_carros()
        print(f"\n=== TESTE COM BANCO REAL ===")
        print(f"Total de carros no banco: {self.total_cars}")
        
        if self.total_cars == 0:
            print("AVISO: Banco de dados vazio! Execute o script de geração de carros primeiro.")
            return
    
    async def test_search_scenarios(self):
        """Testa vários cenários de busca com dados reais"""
        if self.total_cars == 0:
            return
            
        test_scenarios = [
            # Busca por marca
            "Quero ver carros da Toyota",
            "Mostre-me carros Honda",
            "Tem algum Volkswagen disponível?",
            
            # Busca por cor
            "Quero um carro preto",
            "Tem carros brancos?",
            "Procuro um carro azul",
            
            # Busca por preço
            "Carros até 50000 reais",
            "Quero algo entre 30000 e 80000",
            "Carros baratos, até 40000",
            
            # Busca por ano
            "Carros de 2020",
            "Quero um carro novo, de 2023",
            "Tem carros de 2019?",
            
            # Busca combinada
            "Toyota Corolla preto",
            "Honda branco até 60000",
            "Volkswagen de 2021",
            
            # Busca por transmissão
            "Carros automáticos",
            "Quero manual",
            
            # Listagem geral
            "Quais carros vocês têm?",
            "Mostre todos os carros",
            
            # Busca específica (se houver dados)
            "Carro número 1",
            "Detalhes do carro 5",
        ]
        
        print(f"\n=== EXECUTANDO {len(test_scenarios)} CENÁRIOS DE TESTE ===")
        
        # Primeiro, obter marcas disponíveis para o extract_filters
        try:
            brands_response = await self.mcp_client.get_available_brands()
            available_brands = brands_response.get('marcas', []) if isinstance(brands_response, dict) else []
            
            # Preparar contexto do banco para as respostas
            database_context = {
                'total_cars': self.total_cars,
                'brands': available_brands,
                'formatted_price_range': 'R$ 10.000 - R$ 150.000'
            }
        except:
            available_brands = []
            database_context = {
                'total_cars': self.total_cars,
                'brands': [],
                'formatted_price_range': 'R$ 10.000 - R$ 150.000'
            }
        
        for i, query in enumerate(test_scenarios, 1):
            print(f"\n--- Teste {i}/{len(test_scenarios)} ---")
            print(f"Pergunta: '{query}'")
            
            try:
                # 1. Analisar intenção
                intent_result = await self.ai_service.analyze_intent(query)
                print(f"Resultado da análise: {intent_result}")
                
                # Verificar se tem a chave correta (intent_type ou intent)
                intent_type = intent_result.get('intent_type') or intent_result.get('intent', 'conversation')
                confidence = intent_result.get('confidence', 0.5)
                print(f"Intenção detectada: {intent_type} (confiança: {confidence})")
                
                # 2. Extrair filtros
                filters = await self.ai_service.extract_filters(query, available_brands)
                print(f"Filtros extraídos: {filters}")
                
                # 3. Buscar no banco
                if intent_type == 'search' or intent_result.get('needs_search', False):
                    search_results = await self.mcp_client.search_cars(filters)
                    print(f"Resultados encontrados: {search_results.get('total_encontrados', 0)} carros")
                    
                    # 4. Gerar resposta
                    if search_results.get('total_encontrados', 0) > 0:
                        response = await self.response_service.generate_search_response(
                            query,                    # user_input
                            search_results,           # search_results  
                            [],                       # conversation_history (vazio para teste)
                            database_context         # database_context
                        )
                        print(f"Resposta gerada: {response[:200]}..." if len(response) > 200 else f"Resposta: {response}")
                    else:
                        print("Nenhum carro encontrado com esses critérios.")
                        
                else:
                    # Para conversação, usar o histórico vazio
                    database_context = {
                        'total_cars': self.total_cars,
                        'brands': available_brands,
                        'formatted_price_range': 'R$ 10.000 - R$ 150.000'
                    }
                    response = await self.ai_service.generate_response(query, [], database_context)
                    print(f"Resposta conversacional: {response}")
                    
            except Exception as e:
                print(f"Erro no teste: {str(e)}")
                import traceback
                traceback.print_exc()
                
            print("-" * 50)
    
    def test_database_queries(self):
        """Testa consultas diretas no banco"""
        print(f"\n=== TESTE DE CONSULTAS DIRETAS NO BANCO ===")
        
        try:
            # Buscar todas as marcas disponíveis
            all_cars = self.db_manager.get_all_carros()
            marcas = set(car.marca for car in all_cars)
            print(f"Marcas disponíveis ({len(marcas)}): {', '.join(sorted(marcas))}")
            
            # Buscar cores disponíveis
            cores = set(car.cor for car in all_cars)
            print(f"Cores disponíveis ({len(cores)}): {', '.join(sorted(cores))}")
            
            # Faixa de preços
            precos = [car.preco for car in all_cars]
            print(f"Faixa de preços: R$ {min(precos):,.2f} - R$ {max(precos):,.2f}")
            
            # Faixa de anos
            anos = [car.ano_fabricacao for car in all_cars]
            print(f"Faixa de anos: {min(anos)} - {max(anos)}")
            
            # Teste de busca por marca específica
            if marcas:
                primeira_marca = sorted(marcas)[0]
                carros_marca = self.db_manager.get_carros_by_marca(primeira_marca)
                print(f"\nCarros da marca {primeira_marca}: {len(carros_marca)} encontrados")
                
                if carros_marca:
                    primeiro_carro = carros_marca[0]
                    print(f"Exemplo: {primeiro_carro.marca} {primeiro_carro.modelo} {primeiro_carro.ano_fabricacao} - R$ {primeiro_carro.preco:,.2f}")
            
            # Teste de busca por faixa de preço
            carros_baratos = self.db_manager.get_carros_by_preco_range(0, 50000)
            print(f"\nCarros até R$ 50.000: {len(carros_baratos)} encontrados")
            
        except Exception as e:
            print(f"Erro nas consultas: {str(e)}")
    
    async def test_mcp_components(self):
        """Testa os componentes MCP com dados reais"""
        print(f"\n=== TESTE DOS COMPONENTES MCP ===")
        
        try:
            # Teste do cliente MCP
            print("Testando CarMCPClient...")
            
            # Buscar marcas disponíveis
            brands = await self.mcp_client.get_available_brands()
            print(f"Marcas via MCP: {brands}")
            
            # Buscar faixa de preços
            price_range = await self.mcp_client.get_price_range()
            print(f"Faixa de preços via MCP: {price_range}")
            
            # Buscar faixa de anos
            year_range = await self.mcp_client.get_year_range()
            print(f"Faixa de anos via MCP: {year_range}")
            
            # Buscar métricas
            metrics = await self.mcp_client.get_car_metrics()
            print(f"Métricas disponíveis: {metrics['total_metricas']} campos")
            
            # Teste de busca simples
            if brands and isinstance(brands, list) and len(brands) > 0:
                primeira_marca = brands[0]
                resultados = await self.mcp_client.search_cars({'marca': primeira_marca})
                cars_list = resultados.get('cars', [])
                print(f"Busca por {primeira_marca}: {len(cars_list)} carros encontrados")
                
                if cars_list:
                    # Testar detalhes de um carro
                    primeiro_id = cars_list[0]['id']
                    detalhes = await self.mcp_client.get_car_details(primeiro_id)
                    print(f"Detalhes do carro {primeiro_id}: {detalhes['marca']} {detalhes['modelo']}")
            
        except Exception as e:
            print(f"Erro nos componentes MCP: {str(e)}")
            import traceback
            traceback.print_exc()

async def main():
    """Função principal para executar todos os testes"""
    print("INICIANDO TESTES COM BANCO DE DADOS REAL")
    print("=" * 60)
    
    # Verificar configurações
    try:
        settings.validate()
        print("Configurações validadas")
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        print("Configure a OPENAI_API_KEY no arquivo .env")
        return
    
    # Inicializar tester
    tester = RealCarSearchTester()
    
    if tester.total_cars == 0:
        print("\nPara popular o banco, execute:")
        print("   python factory/generate_cars.py")
        return
    
    # Executar testes
    print("\nExecutando testes...")
    
    # 1. Testar consultas diretas
    tester.test_database_queries()
    
    # 2. Testar componentes MCP
    await tester.test_mcp_components()
    
    # 3. Testar cenários de busca completos
    await tester.test_search_scenarios()
    
    print("\nTESTES CONCLUÍDOS!")
    print("=" * 60)

if __name__ == "__main__":
    # Executar testes
    asyncio.run(main())