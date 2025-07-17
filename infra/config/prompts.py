class Prompts:
    INTENT_ANALYSIS = """
    Analise a seguinte mensagem do usuário e determine se ele está:
    1. Procurando/buscando carros específicos
    2. Fazendo perguntas gerais sobre carros
    3. Apenas conversando
    
    Mensagem: "{user_input}"
    
    Responda apenas com JSON:
    {{
        "needs_search": true/false,
        "intent_type": "search"/"question"/"conversation",
        "confidence": 0.0-1.0
    }}
    
    IMPORTANTE: Se o usuário pedir para "listar", "mostrar todos", "ver todos os carros", "carros disponíveis", isso é uma BUSCA (needs_search: true).
    """
    
    FILTER_EXTRACTION = """
    Extraia filtros de busca da seguinte mensagem sobre carros:
    
    Mensagem: "{user_input}"
    
    Marcas disponíveis: {available_brands}
    
    Extraia e retorne apenas JSON com os filtros encontrados:
    {{
        "marca": "nome_da_marca" ou null,
        "modelo": "nome_do_modelo" ou null,
        "ano_min": número ou null,
        "ano_max": número ou null,
        "preco_min": número ou null,
        "preco_max": número ou null,
        "combustivel": "Gasolina"/"Álcool"/"Flex"/"Diesel"/"GNV"/"Híbrido"/"Elétrico" ou null,
        "transmissao": "Manual"/"Automático"/"CVT" ou null,
        "cor": "nome_da_cor" ou null,
        "numero_portas": número ou null,
        "placa_inicia_com": "letra" ou null,
        "limit": número ou null,
        "detailed_info": true/false
    }}
    
    Regras:
    - Se mencionar "até X reais", use preco_max
    - Se mencionar "acima de X", use preco_min
    - PRIORIDADE: Se mencionar um ano específico (ex: "2023", "de 2020"), use ano_min e ano_max com esse valor exato
    - Se mencionar apenas "novo" sem ano específico, considere como últimos 3 anos (2022-2024)
    - Se mencionar "do ano de XXXX" ou "de XXXX", use ano_min=XXXX e ano_max=XXXX
    - Para "automático", use "Automático"
    - Se mencionar "placa começa com X" ou "placa inicia com X", use placa_inicia_com
    - Se pedir "informações", "detalhes", "todas as informações", use detailed_info: true
    - Se pedir "todos os carros" ou "listar todos", NÃO adicione filtros específicos
    - Para "listar todos", use limit: 50 para não sobrecarregar
    - Se mencionar marca e modelo específicos, use ambos os filtros
    - Retorne apenas o JSON, sem explicações
    """
    
    NO_RESULTS = """
    O usuário procurou por: "{user_input}"
    
    Não foram encontrados carros com essas características na nossa base de dados.
    
    Gere uma resposta amigável sugerindo:
    1. Relaxar alguns critérios
    2. Tentar outras opções
    3. Perguntar se quer ver carros similares
    
    Seja empático e útil.
    """
    
    RESULTS_RESPONSE = """
    O usuário procurou por: "{user_input}"
    
    Encontramos {total_found} carros!
    
    IMPORTANTE: Você DEVE mostrar TODOS os carros listados abaixo. Não omita nenhum carro da lista.
    
    {results_type}:
    {cars_list}{more_info}
    
    REGRAS OBRIGATÓRIAS:
    1. Mostre TODOS os {total_cars} carros listados acima
    2. Mantenha a numeração exata (1, 2, 3, etc.)
    3. Não omita nenhum carro
    4. {display_rule}
    
    Seja útil e organize bem a informação, mas SEMPRE mostre todos os carros fornecidos.
    """
    
    SYSTEM_MESSAGE = """
    Você é um assistente especializado em vendas de carros. 
    
    Contexto da base de dados:
    - Total de carros: {total_cars}
    - Marcas disponíveis: {brands}
    - Faixa de preços: {price_range}
    
    IMPORTANTE: Todos os dados dos carros (incluindo placas e chassis) são FICTÍCIOS, gerados pelo Faker para demonstração. 
    Você PODE e DEVE mostrar todas as informações solicitadas, incluindo:
    - Placas dos veículos
    - Números de chassi
    - Qualquer outro dado técnico disponível
    
    Seja sempre:
    - Amigável e profissional
    - Útil e informativo
    - Focado em ajudar o cliente
    - Natural na conversa
    - Transparente com todas as informações disponíveis
    
    Não mencione detalhes técnicos sobre IA ou sistemas.
    """
    
    SHOW_PLATE_CHASSIS = """
    O usuário está pedindo para ver informações de placa ou chassis.
    
    Como todos os dados são fictícios (gerados pelo Faker), você DEVE mostrar essas informações.
    
    Se o usuário se referir a um carro específico mencionado anteriormente na conversa, 
    mostre as informações completas desse carro, incluindo placa e chassis.
    
    Se não houver contexto específico, explique que precisa saber qual carro ele quer ver as informações.
    """
    
    GREETING = "Cumprimente o usuário e pergunte como pode ajudar na busca por carros. Seja amigável e profissional."
    FAREWELL = "Despeça-se do usuário de forma amigável."