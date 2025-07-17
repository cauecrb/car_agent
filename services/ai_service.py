import json
from typing import Dict, Any, List
from openai import OpenAI
from infra.config.settings import settings
from infra.config.prompts import Prompts
from infra.shared.text_utils import sanitize_text
from infra.config.keywords import IntentKeywords

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
    async def analyze_intent(self, user_input: str) -> Dict[str, Any]:
        prompt = Prompts.INTENT_ANALYSIS.format(user_input=sanitize_text(user_input))
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": sanitize_text(prompt)}],
                temperature=settings.INTENT_TEMPERATURE
            )
            
            content = sanitize_text(response.choices[0].message.content)
            return json.loads(content)
        except Exception as e:
            # Fallback
            search_keywords = [
                'buscar', 'procurar', 'quero', 'preciso', 'encontrar', 'carro', 'placa',
                'listar', 'mostrar', 'ver', 'todos', 'disponíveis', 'disponivel', 'lista'
            ]
            needs_search = any(keyword in user_input.lower() for keyword in search_keywords)
            return {
                "needs_search": needs_search, 
                "intent_type": "search" if needs_search else "conversation", 
                "confidence": 0.5
            }
    
    async def extract_filters(self, user_input: str, available_brands: List[str]) -> Dict[str, Any]:
        import re
        
        # Verificar se está pedindo informações de um carro específico por número
        number_match = re.search(r'(?:numero|número|carro)\s*(\d+)', user_input.lower())
        if number_match:
            car_number = int(number_match.group(1))
            return {'limit': 50, 'specific_request': True, 'car_number': car_number}
        
        # Usar configuração centralizada para detecção de cores
        detected_color = IntentKeywords.detect_color(user_input)
        
        # Verificar se está pedindo detalhes específicos
        wants_detailed_info = IntentKeywords.check_detail_intent(user_input)
        
        prompt = Prompts.FILTER_EXTRACTION.format(
            user_input=sanitize_text(user_input),
            available_brands=available_brands
        )
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": sanitize_text(prompt)}],
                temperature=settings.INTENT_TEMPERATURE
            )
            
            content = sanitize_text(response.choices[0].message.content)
            filters = json.loads(content)
            
            # Se detectamos uma cor usando configuração
            if detected_color:
                filters['cor'] = detected_color
            
            # Se está pedindo detalhes específicos
            if wants_detailed_info:
                filters['detailed_info'] = True
                filters['specific_request'] = True
            
            #verificar listagem geral
            if IntentKeywords.check_list_all_intent(user_input, available_brands):
                if detected_color:
                    filters = {'cor': detected_color, 'limit': settings.DEFAULT_SEARCH_LIMIT}
                else:
                    filters = {k: v for k, v in filters.items() if k in ['limit', 'detailed_info'] and v is not None}
                    if 'limit' not in filters:
                        filters['limit'] = settings.DEFAULT_SEARCH_LIMIT
            
            return {k: v for k, v in filters.items() if v is not None}
            
        except Exception as e:
            fallback_filters = {}
            if detected_color:
                fallback_filters['cor'] = detected_color
            if wants_detailed_info:
                fallback_filters['detailed_info'] = True
                fallback_filters['specific_request'] = True
            
            if fallback_filters:
                fallback_filters['limit'] = settings.DEFAULT_SEARCH_LIMIT
                return fallback_filters
            
            if IntentKeywords.check_list_all_intent(user_input, available_brands):
                return {'limit': settings.DEFAULT_SEARCH_LIMIT}
            return {}
    
    #resposta gerada
    async def generate_response(self, prompt: str, conversation_history: List[Dict], database_context: Dict) -> str:
        system_message = Prompts.SYSTEM_MESSAGE.format(
            total_cars=database_context.get('total_cars', 0),
            brands=', '.join(database_context.get('brands', [])),
            price_range=database_context.get('formatted_price_range', 'Não disponível')
        )
        
        try:
            messages = [{"role": "system", "content": sanitize_text(system_message)}]
            
            # Adicionar histórico recente
            recent_history = conversation_history[-settings.MAX_HISTORY_MESSAGES:] if len(conversation_history) > settings.MAX_HISTORY_MESSAGES else conversation_history
            for msg in recent_history:
                sanitized_msg = {
                    "role": msg["role"],
                    "content": sanitize_text(msg["content"])
                }
                messages.append(sanitized_msg)
            
            messages.append({"role": "user", "content": sanitize_text(prompt)})
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS
            )
            
            content = response.choices[0].message.content.strip()
            return sanitize_text(content)
            
        except Exception as e:
            error_msg = sanitize_text(str(e))
            return f"Desculpe, tive um problema técnico. Pode repetir sua pergunta? (Erro: {error_msg})"