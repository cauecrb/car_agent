import re
from typing import Dict, Any, Optional
from infra.config.keywords import IntentKeywords

#processar as intençoes do usuario
#aqui vao varios casos para checar
class IntentService:
    
    @staticmethod
    def check_specific_car_request(user_input: str) -> Optional[Dict[str, Any]]:
        number_match = re.search(r'(?:numero|número|carro)\s*(\d+)', user_input.lower())
        if number_match:
            car_number = int(number_match.group(1))
            return {
                'limit': 50, 
                'specific_request': True, 
                'car_number': car_number
            }
        return None
    
    @staticmethod
    def process_user_intent(user_input: str, available_brands: list = None) -> Dict[str, Any]:
        if available_brands is None:
            available_brands = []
            
        intent_info = {
            'is_metrics_request': IntentKeywords.check_metrics_intent(user_input),
            'is_exit_request': IntentKeywords.check_exit_intent(user_input),
            'wants_details': IntentKeywords.check_detail_intent(user_input),
            'wants_list_all': IntentKeywords.check_list_all_intent(user_input, available_brands),
            'detected_color': IntentKeywords.detect_color(user_input),
            'specific_car_request': IntentService.check_specific_car_request(user_input)
        }
        
        return intent_info
    
    @staticmethod
    def generate_metrics_response(metrics_data: Dict[str, Any]) -> str:
        response = "Aqui estão todas as métricas/informações disponíveis sobre os carros na base de dados:\n\n"
        
        for i, metric in enumerate(metrics_data['metricas'], 1):
            response += f"{i}. **{metric['nome_amigavel']}**\n"
            response += f"   - Campo técnico: `{metric['campo_tecnico']}`\n"
            response += f"   - Tipo: {metric['tipo']}\n"
            if metric['obrigatorio']:
                response += f"   - Campo obrigatório\n"
            if metric['chave_primaria']:
                response += f"   - Chave primária\n"
            if metric['unico']:
                response += f"   - Valor único\n"
            response += "\n"
        
        response += f"\n**Total de métricas disponíveis: {metrics_data['total_metricas']}**\n\n"
        response += "Essas métricas são geradas dinamicamente baseadas no modelo do banco de dados, "
        response += "então se o banco for alterado, a lista será atualizada automaticamente!"
        
        return response