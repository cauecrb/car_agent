#aqui foi testes atras de testes para ir aprimorando as intençoes
class IntentKeywords:

    
    # Palavras-chave para detecção de métricas
    METRICS_KEYWORDS = [
        'métricas', 'metricas', 'campos', 'informações disponíveis', 
        'dados disponíveis', 'características disponíveis', 'atributos',
        'propriedades', 'especificações', 'detalhes técnicos'
    ]
    
    # Palavras-chave para comandos de saída
    EXIT_KEYWORDS = [
        'sair', 'exit', 'quit', 'tchau', 'bye', 'adeus', 'até logo'
    ]
    
    SEARCH_KEYWORDS = [
        'buscar', 'procurar', 'quero', 'preciso', 'encontrar', 'carro', 'placa',
        'listar', 'mostrar', 'ver', 'todos', 'disponíveis', 'disponivel', 'lista'
    ]
    
    # Palavras-chave para listagem geral
    LIST_ALL_KEYWORDS = [
        'todos', 'listar', 'disponíveis', 'disponivel', 'mostrar todos',
        'ver todos', 'carros disponíveis'
    ]
    
    # Palavras-chave para detalhes específicos
    DETAIL_KEYWORDS = [
        'portas', 'motor', 'motorização', 'detalhes', 'informações', 
        'especificações', 'características'
    ]
    
    # Mapeamento de cores
    COLOR_MAPPING = {
        'branco': 'Branco', 'branca': 'Branco', 'brancos': 'Branco',
        'preto': 'Preto', 'preta': 'Preto', 'pretos': 'Preto',
        'azul': 'Azul', 'vermelho': 'Vermelho', 'vermelha': 'Vermelho',
        'verde': 'Verde', 'amarelo': 'Amarelo', 'amarela': 'Amarelo',
        'cinza': 'Cinza', 'prata': 'Prata', 'dourado': 'Dourado',
        'marrom': 'Marrom', 'bege': 'Bege', 'roxo': 'Roxo', 'rosa': 'Rosa'
    }
    
    @classmethod
    def check_metrics_intent(cls, user_input):
        return any(keyword in user_input.lower() for keyword in cls.METRICS_KEYWORDS)
    
    @classmethod
    def check_exit_intent(cls, user_input):
        return user_input.lower() in cls.EXIT_KEYWORDS
    
    @classmethod
    def detect_color(cls, user_input):
        for color_variant, standard_color in cls.COLOR_MAPPING.items():
            if color_variant in user_input.lower():
                return standard_color
        return None    
    @classmethod
    def check_detail_intent(cls, user_input: str) -> bool:
        return any(keyword in user_input.lower() for keyword in cls.DETAIL_KEYWORDS)
    
    @classmethod
    def check_list_all_intent(cls, user_input: str, available_brands: list) -> bool:
        has_list_keyword = any(keyword in user_input.lower() for keyword in cls.LIST_ALL_KEYWORDS)
        has_brand_filter = any(brand.lower() in user_input.lower() for brand in available_brands)
        return has_list_keyword and not has_brand_filter
