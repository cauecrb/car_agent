import asyncio
import json
from typing import Dict, Any, List, Optional
from infra.config.settings import settings
from infra.config.prompts import Prompts
from infra.config.keywords import IntentKeywords
from services.ai_service import AIService
from services.response_service import ResponseService
from services.intent_service import IntentService
from infra.shared.text_utils import sanitize_text
from infra.shared.formatters import format_price_range
from presentation.mcp import CarMCPServer, CarMCPClient

class AIVirtualCarAgent:
    def __init__(self):
        settings.validate()
        
        # Serviços
        self.server = CarMCPServer()
        self.client = CarMCPClient(self.server)
        self.ai_service = AIService()
        self.response_service = ResponseService(self.ai_service)
        self.intent_service = IntentService()
        
        # Estado
        self.conversation_history = []
        self.car_database_context = None

    #agente virtual 
    async def start(self):
        await self.server.start()
        await self._load_database_context()
        
        print("\n" + "~"*60)
        print(f"{settings.APP_NAME} - Usada a API do OpenAI")
        print("Olá! Sou um assistente especializado em carros.")
        print("Posso auxiliar a encontrar o carro com as caracteristicas desejadas que estao em nossa base de dados ")
        print("para sair digite exit, ou sair no terminal ")
        print("~"*60 + "\n")
        
        await self._start_conversation()
        
    async def _load_database_context(self):
        try:
            stats = await self.client.get_car_statistics()
            brands = await self.client.get_available_brands()
            price_range = await self.client.get_price_range()
            year_range = await self.client.get_year_range()
            
            self.car_database_context = {
                "total_cars": stats["total_carros"],
                "brands": brands["marcas"],
                "price_range": price_range,
                "year_range": year_range,
                "brand_distribution": stats["por_marca"],
                "formatted_price_range": format_price_range(price_range)
            }
            
        except Exception as e:
            if settings.DEBUG:
                print(f"Debug: Erro ao carregar contexto: {e}")
            
            self.car_database_context = {
                "total_cars": 0,
                "brands": [],
                "price_range": {"min": 0, "max": 0, "media": 0},
                "year_range": {"min": 0, "max": 0},
                "brand_distribution": {},
                "formatted_price_range": "Não disponível"
            }
    #inicio da conversa        
    async def _start_conversation(self):
        initial_response = await self.ai_service.generate_response(
            Prompts.GREETING, 
            self.conversation_history, 
            self.car_database_context
        )
        print(f"Assistente: {initial_response}")
        
        while True:
            try:
                user_input = input("\nVocê: ").strip()
                user_input = sanitize_text(user_input)
                
                # Usar configuração centralizada para verificar saída
                if IntentKeywords.check_exit_intent(user_input):
                    farewell = await self.ai_service.generate_response(
                        Prompts.FAREWELL, 
                        self.conversation_history, 
                        self.car_database_context
                    )
                    print(f"\nAssistente: {farewell}")
                    break
                    
                response = await self._process_user_input(user_input)
                print(f"\nAssistente: {response}")
                
            except KeyboardInterrupt:
                print("\n\nAté logo!")
                break
            except Exception as e:
                error_msg = sanitize_text(str(e))
                if settings.DEBUG:
                    print(f"\nDebug Error: {error_msg}")
                else:
                    print(f"\nErro: {error_msg}")
                
        await self.server.stop()
        
    async def _process_user_input(self, user_input: str) -> str:
        try:
            # Adicionar à história
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Debug: mostrar entrada do usuário
            if settings.DEBUG:
                print(f"\nDEBUG - Entrada do usuário: {user_input}")
            
            # Processar intenção do usuário
            intent_info = self.intent_service.process_user_intent(
                user_input, 
                self.car_database_context.get("brands", [])
            )
            
            # Verificar se está pedindo métricas dos carros
            if intent_info['is_metrics_request']:
                try:
                    metrics_data = await self.client.get_car_metrics()
                    response = self.intent_service.generate_metrics_response(metrics_data)
                    
                    self.conversation_history.append({"role": "assistant", "content": response})
                    return response
                    
                except Exception as e:
                    if settings.DEBUG:
                        print(f"DEBUG - Erro ao obter métricas: {e}")
                    return "Desculpe, não consegui obter as métricas dos carros no momento."
            
            # Analisar intenção com IA
            intent = await self.ai_service.analyze_intent(user_input)
            
            if settings.DEBUG:
                print(f"DEBUG - Intent detectado: {intent}")
                print(f"DEBUG - Intent info processado: {intent_info}")
            
            if intent["needs_search"]:
                # Extrair filtros e buscar
                filters = await self.ai_service.extract_filters(
                    user_input, 
                    self.car_database_context.get("brands", [])
                )
                
                # Aplicar informações de intenção aos filtros
                if intent_info['detected_color']:
                    filters['cor'] = intent_info['detected_color']
                
                if intent_info['wants_details']:
                    filters['detailed_info'] = True
                    filters['specific_request'] = True
                
                if intent_info['specific_car_request']:
                    filters.update(intent_info['specific_car_request'])
                
                if settings.DEBUG:
                    print(f"DEBUG - Filtros extraídos: {filters}")
                
                search_results = await self._search_cars(filters)
                
                if settings.DEBUG:
                    print(f"DEBUG - Resultados da busca: {search_results['total_encontrados']} carros encontrados")
                
                response = await self.response_service.generate_search_response(
                    user_input, 
                    search_results, 
                    self.conversation_history, 
                    self.car_database_context
                )
            else:
                # Resposta conversacional
                response = await self.ai_service.generate_response(
                    user_input, 
                    self.conversation_history, 
                    self.car_database_context
                )
                
            response = sanitize_text(response)
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_msg = sanitize_text(str(e))
            if settings.DEBUG:
                print(f"DEBUG - Erro no processamento: {error_msg}")
            return f"Desculpe, tive um problema técnico. Pode repetir sua pergunta? (Erro: {error_msg})"
    
    async def _search_cars(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Busca carros com filtros"""
        try:
            if not filters:
                return {"total_encontrados": 0, "carros": []}
            return await self.client.search_cars(filters)
        except Exception as e:
            if settings.DEBUG:
                print(f"Debug - Search error: {e}")
            return {"total_encontrados": 0, "carros": []}

# Função principal
async def main():
    try:
        agent = AIVirtualCarAgent()
        await agent.start()
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        print("\nPor favor, configure as variáveis de ambiente no arquivo .env")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(main())