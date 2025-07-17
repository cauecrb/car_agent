# AI Virtual Car Agent
Um assistente virtual para busca e consulta de carros usando IA e arquitetura MCP (Model Context Protocol).

## Como Executar
### Pré-requisitos
- Python 3.12+
- OpenAI API Key

### Instalação
1. **Clone o repositório e navegue até a pasta:**
```bash
cd agent_carros
```
2. **execute o script de execuçao:**

```bash
./run_ai_agent.sh
```
o script automaticamente ativara o ambiente virtual, instalara as dependencias e executara o sistema.

# OU


2. **Crie e ative o ambiente virtual:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env e adicione sua OPENAI_API_KEY
```

5. **Gere dados de teste (caso ja nao os tenha ):**

Os dados ficam em infra/data/database/carros.db.

A geraçao de dados do banco cria uma copia em JSON caso queira conferir manualmente os carros que foram gerados, o arquivo JSON fica na pasta raiz como arquivo carros_gerados.json
```bash
python factory/generate_cars.py
```

### Executando o Sistema
**Modo Principal:**

 executar o script 

```bash
run_ai_agent.sh
```
# OU

```bash
python ai_virtual_agent.py
```

**Executar Testes:**
```bash
# Todos os testes
python -m pytest

# Teste específico de busca real
python tests/test_real_car_search.py

# Testes com cobertura
bash run_coverage.sh
```

## Arquitetura do Sistema
### Visão Geral
O sistema segue uma arquitetura em camadas com separação clara de responsabilidades:

┌─────────────────┐
│   Presentation  │ ← Interface do usuário
├─────────────────┤
│    Services     │ ← Lógica de negócio
├─────────────────┤
│  Infrastructure │ ← Configurações e dados
├─────────────────┤
│     Model       │ ← Entidades de domínio
└─────────────────┘

### Componentes Principais

#### 1. AI Virtual Agent (`ai_virtual_agent.py`)
- **Função:** Ponto de entrada principal do sistema
- **Responsabilidade:** Orquestração da conversa e coordenação entre componentes

#### 2. Services Layer (`services/`)
- **AIService:** Integração com OpenAI para análise de intenção e geração de respostas
- **IntentService:** Processamento de intenções do usuário
- **ResponseService:** Formatação de respostas para o usuário

#### 3. Presentation Layer (`presentation/mcp/`)
- **CarMCPServer:** Servidor MCP que expõe funcionalidades de busca
- **CarMCPClient:** Cliente para comunicação com o servidor MCP
- **Protocols:** Definições de protocolos de comunicação

#### 4. Infrastructure Layer (`infra/`)
- **Database:** Gerenciamento de dados e repositórios
- **Config:** Configurações, prompts e palavras-chave
- **Shared:** Utilitários compartilhados

#### 5. Model Layer (`model/`)
- **Carros:** Entidades de domínio
- **Enums:** Enumerações do sistema

## Organização dos Arquivos

### Estrutura Detalhada

agent_carros/
├── ai_virtual_agent.py          # Ponto de entrada principal
├── carros_gerados.json          # Dados de carros (gerados)
│
├─- services/                    # Camada de Serviços
│   ├── ai_service.py           # Integração com OpenAI
│   ├── intent_service.py       # Processamento de intenções
│   └── response_service.py     # Formatação de respostas
│
├── presentation/mcp/            # Camada de Apresentação (MCP)
│   ├── server.py               # Servidor MCP
│   ├── client.py               # Cliente MCP
│   └── protocols.py            # Protocolos de comunicação
│
├── infra/                       # Camada de Infraestrutura
│   ├── config/                 # Configurações
│   │   ├── settings.py         # Configurações gerais
│   │   ├── prompts.py          # Prompts para IA
│   │   └── keywords.py         # Palavras-chave e detecção
│   │
│   ├── database/               # Gerenciamento de Dados
│   │   ├── database.py         # Gerenciador de banco
│   │   ├── car_repository.py   # Repositório de carros
│   │   ├── car_filters.py      # Filtros de busca
│   │   ├── models.py           # Modelos SQLAlchemy
│   │   └── response_models.py  # Modelos de resposta
│   │
│   └── shared/                 # Utilitários Compartilhados
│       ├── formatters.py       # Formatadores de dados
│       └── text_utils.py       # Utilitários de texto
│
├── model/                       # Camada de Modelo
│   ├── carros.py               # Entidades de carros
│   └── enums.py                # Enumerações
│
├── factory/                     # Geração de Dados
│   ├── generate_cars.py        # Gerador de carros fictícios
│   └── carros_gerados.json     # Dados gerados
│
├── tests/                       # Testes
│   ├── test_real_car_search.py # Teste de busca real
│   ├── test_ai_service.py      # Testes do AIService
│   ├── test_intent_service.py  # Testes do IntentService
│   └── conftest.py             # Configurações de teste

### Finalidade de Cada Diretório

#### `services/` - Lógica de Negócio
- Processamento de linguagem natural
- Análise de intenções do usuário
- Geração de respostas inteligentes
- Extração de filtros de busca

#### `presentation/mcp/` - Interface MCP
- Servidor que expõe funcionalidades via MCP
- Cliente para comunicação interna
- Protocolos de requisição/resposta

#### `infra/` - Infraestrutura
- **config/:** Todas as configurações do sistema
- **database/:** Acesso a dados e persistência
- **shared/:** Utilitários reutilizáveis

#### `model/` - Entidades de Domínio
- Definições de carros e suas propriedades
- Enumerações para tipos padronizados

#### `factory/` - Geração de Dados
- Scripts para criar dados de teste
- Dados fictícios para demonstração

#### `tests/` - Testes Automatizados
- Testes unitários e de integração
- Testes de busca com dados reais
- Configurações de teste

## Configuração

### Variáveis de Ambiente (`.env`)

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-3.5-turbo
DEBUG=true
DATABASE_URL=sqlite:///carros.db
```

### Configurações Principais
- **Prompts IA:** `infra/config/prompts.py`
- **Palavras-chave:** `infra/config/keywords.py`
- **Settings:** `infra/config/settings.py`

## Fluxo de Execução

1. **Entrada do Usuário** → `ai_virtual_agent.py`
2. **Análise de Intenção** → `services/ai_service.py`
3. **Processamento** → `services/intent_service.py`
4. **Busca de Dados** → `presentation/mcp/server.py` → `infra/database/`
5. **Formatação** → `services/response_service.py`
6. **Resposta** → Usuário

## Exemplos de Uso

Usuário: "Quero um carro Toyota preto até 50000 reais"

1. Análise: intent_type="search"
2. Filtros: {marca: "Toyota", cor: "preto", preco_max: 50000}
3. Busca: CarMCPServer.search_cars(filtros)
4. Resposta: Lista formatada de carros encontrados

## Debugging

- Ative `DEBUG=true` no `.env` para logs detalhados