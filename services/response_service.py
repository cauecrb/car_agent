from typing import Dict, Any, List
from infra.config.settings import settings
from infra.config.prompts import Prompts
from infra.shared.formatters import format_car_summary, format_car_detailed
from infra.shared.text_utils import sanitize_text

# Classe de serviço de resposta
class ResponseService:
    def __init__(self, ai_service):
        self.ai_service = ai_service
    
    async def generate_search_response(self, user_input: str, search_results: Dict[str, Any], conversation_history: list, database_context: Dict) -> str:
        if search_results["total_encontrados"] == 0:
            prompt = Prompts.NO_RESULTS.format(user_input=sanitize_text(user_input))
        else:
            cars_summary = []
            total_found = search_results["total_encontrados"]
            
            # Verificar se é uma busca específica ou listagem geral
            is_specific_search = total_found <= 5 or any(word in user_input.lower() for word in ['informações', 'detalhes', 'específico', 'numero', 'número'])
            
            if is_specific_search:
                # Mostrar informações completas
                for i, car in enumerate(search_results["carros"][:settings.MAX_CARS_DETAILED], 1):
                    car_info = format_car_detailed(car, i)
                    cars_summary.append(sanitize_text(car_info))
                results_type = "Informações detalhadas"
                display_rule = "Para buscas específicas, destaque as informações completas."
            else:
                # Mostrar resumo
                for i, car in enumerate(search_results["carros"][:settings.MAX_CARS_DISPLAY], 1):
                    car_info = format_car_summary(car, i)
                    cars_summary.append(sanitize_text(car_info))
                results_type = f"Lista dos {len(cars_summary)} carros"
                display_rule = "Para listagens, mencione que pode fornecer mais detalhes se solicitado."
            
            # Informação sobre mais carros
            more_info = ""
            if total_found > len(search_results["carros"]):
                shown = len(search_results["carros"])
                more_info = f"\n\n(Mostrando {shown} de {total_found} carros encontrados)"
            
            prompt = Prompts.RESULTS_RESPONSE.format(
                user_input=sanitize_text(user_input),
                total_found=total_found,
                results_type=results_type,
                cars_list=chr(10).join(cars_summary),
                more_info=more_info,
                total_cars=len(cars_summary),
                display_rule=display_rule
            )
        
        return await self.ai_service.generate_response(prompt, conversation_history, database_context)