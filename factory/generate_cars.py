import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.carros import *
from faker import Faker
from faker.providers import automotive
import random
import json
from datetime import datetime, timedelta
from typing import List
from infra.database import DatabaseManager
from infra.config.settings import settings

fake = Faker('pt_BR')
fake.add_provider(automotive)

cores = [
    'Branco', 'Prata', 'Preto', 'Cinza', 'Azul', 'Vermelho',
    'Verde', 'Amarelo', 'Marrom', 'Bege', 'Dourado', 'Bronze'
]

motorizacoes = {
    'popular': ['1.0', '1.0 Turbo', '1.3', '1.4'],
    'medio': ['1.4 16V', '1.6', '1.6 16V', '1.8', '2.0'],
    'premium': ['2.0 Turbo', '2.4', '3.0 V6', '3.5 V6', '4.0 V8'],
    'eletrico': ['Motor Elétrico', 'Híbrido']
}

def generate_chassi() -> str:
    return fake.vin()

def generate_placa() -> str:
    letras1 = ''.join(fake.random_letters(length=3)).upper()
    num1 = fake.random_digit()
    letra2 = fake.random_letter().upper()
    numeros2 = ''.join([str(fake.random_digit()) for _ in range(2)])
    return f"{letras1}{num1}{letra2}{numeros2}"

#sugestão da IA para gerar preço baseado na categoria e ano
#---------------------------------------------------------------------------------------
def get_preco_por_categoria(categoria: str, ano: int) -> float:
    ano_atual = datetime.now().year
    depreciacao = (ano_atual - ano) * 0.08  # 8% por ano
    
    precos_base = {
        'popular': random.uniform(25000, 60000),
        'medio': random.uniform(50000, 120000),
        'premium': random.uniform(150000, 500000),
        'eletrico': random.uniform(120000, 400000)
    }
    
    preco_base = precos_base.get(categoria, 50000)
    preco_final = preco_base * (1 - depreciacao)
    return max(preco_final, preco_base * 0.3)

def gerar_carro() -> carro:
    marca = random.choice(list(MARCAS_MODELOS.keys()))
    modelo = random.choice(MARCAS_MODELOS[marca])
    categoria = get_categoria_por_marca(marca)
    
    ano_fabricacao = random.randint(2010, 2024)
    ano_modelo = ano_fabricacao + random.choice([0, 1])
    cor = random.choice(cores)
    motorizacao = random.choice(motorizacoes[categoria])
    
    # aqui serve para manter uma consistencia no tipo de carro validando transmiçao, combustivel usado e numero de portas
    #------------------------------------------------------------------------------------------------
    if categoria == 'eletrico':
        combustivel = random.choice([TipoCombustivel.ELETRICO, TipoCombustivel.HIBRIDO])
    elif categoria == 'premium':
        combustivel = random.choice([TipoCombustivel.GASOLINA, TipoCombustivel.FLEX])
    else:
        combustivel = random.choice([TipoCombustivel.FLEX, TipoCombustivel.GASOLINA, TipoCombustivel.ETANOL])
    
    if categoria in ['premium', 'eletrico']:
        transmissao = random.choice([TipoTransmissao.AUTOMATICA, TipoTransmissao.CVT])
    else:
        transmissao = random.choice(list(TipoTransmissao))
    
    tipo_veiculo = random.choice(list(TipoVeiculo))
    
    if tipo_veiculo in [TipoVeiculo.COUPE, TipoVeiculo.CONVERSIVEL]:
        numero_portas = 2
    elif tipo_veiculo == TipoVeiculo.PICKUP:
        numero_portas = random.choice([2, 4])
    else:
        numero_portas = random.choice([4, 5])
    
    #estimativa de quilometragem
    #---------------------------------------------------------------------------------------------
    anos_uso = datetime.now().year - ano_fabricacao
    quilometragem = anos_uso * random.randint(5000, 20000)

    preco = get_preco_por_categoria(categoria, ano_fabricacao)
    placa = generate_placa()
    chassi = generate_chassi()
    
    data_revisao = None
    if quilometragem > 10000 and random.choice([True, False]):
        dias_atras = random.randint(30, 365)
        data_revisao = datetime.now() - timedelta(days=dias_atras)
    
    return carro(
        marca=marca,
        modelo=modelo,
        ano_fabricacao=ano_fabricacao,
        ano_modelo=ano_modelo,
        motorizacao=motorizacao,
        tipo_combustivel=combustivel,
        transmissao=transmissao,
        numero_portas=numero_portas,
        tipo_veiculo=tipo_veiculo,
        quilometragem=quilometragem,
        cor=cor,
        preco=round(preco, 2),
        placa=placa,
        chassi=chassi,
        data_ultima_revisao=data_revisao
    )

def gerar_multiplos_carros(quantidade: int) -> List[carro]:
    carros = []
    chassis_usados = set()
    placas_usadas = set()
    
    for i in range(quantidade):
        tentativas = 0
        while tentativas < 10:
            try:
                carro_obj = gerar_carro()
                
                # Verifica se tem apenas um chassi
                if carro_obj.chassi and carro_obj.chassi in chassis_usados:
                    carro_obj.chassi = generate_chassi() + str(i)
                if carro_obj.chassi:
                    chassis_usados.add(carro_obj.chassi)
                
                # Verifica se tem placa repetida
                if carro_obj.placa and carro_obj.placa in placas_usadas:
                    carro_obj.placa = generate_placa()
                if carro_obj.placa:
                    placas_usadas.add(carro_obj.placa)
                
                carros.append(carro_obj)
                break
                
            except Exception as e:
                tentativas += 1
                if tentativas >= 10:
                    print(f"Erro ao gerar carro {i}: {e}")
    
    return carros

#formatar para json
def carro_para_dict(c: carro) -> dict:
    return {
        "marca": c.marca,
        "modelo": c.modelo,
        "ano_fabricacao": c.ano,
        "ano_modelo": c.ano_modelo,
        "motorizacao": c.motorizacao,
        "tipo_combustivel": c.tipo_combustivel.value,
        "transmissao": c.transmissao.value,
        "numero_portas": c.numero_portas,
        "tipo_veiculo": c.tipo_veiculo.value,
        "quilometragem": c.quilometragem,
        "cor": c.cor,
        "preco": c.preco,
        "placa": c.placa,
        "chassi": c.chassi,
        "data_cadastro": c.data_cadastro.isoformat(),
        "data_ultima_revisao": c.data_ultima_revisao.isoformat() if c.data_ultima_revisao else None
    }

def salvar_carros_json(carros: List[carro], arquivo: str = "carros_gerados.json"):
    dados = {
        "total_carros": len(carros),
        "data_geracao": datetime.now().isoformat(),
        "carros": [carro_para_dict(c) for c in carros]
    }
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    quantidade = 150
    carros = gerar_multiplos_carros(quantidade)
    print(f"Gerados {len(carros)} carros com sucesso!")
    
    # Salvar em JSON
    salvar_carros_json(carros)
    print(f"Carros salvos em 'carros_gerados.json'")
    
    # Salvar no banco de dados
    print("Inserindo no banco de dados...")
    db = DatabaseManager(settings.DATABASE_PATH)
    db.create_tables()
    
    try:
        inseridos = db.insert_carros(carros)
        print(f"Inseridos {inseridos} carros no banco SQLite")
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")