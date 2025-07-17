from datetime import datetime
from .enums import TipoCombustivel, TipoTransmissao, TipoVeiculo

MARCAS_MODELOS = {
    'Toyota': ['Corolla', 'Camry', 'Prius', 'RAV4', 'Hilux', 'Etios', 'Yaris'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Fit', 'HR-V', 'City'],
    'Volkswagen': ['Gol', 'Polo', 'Jetta', 'Passat', 'Tiguan', 'T-Cross', 'Virtus'],
    'Chevrolet': ['Onix', 'Prisma', 'Cruze', 'Tracker', 'S10', 'Spin'],
    'Ford': ['Ka', 'Fiesta', 'Focus', 'EcoSport', 'Ranger', 'Territory'],
    'Fiat': ['Uno', 'Palio', 'Siena', 'Toro', 'Argo', 'Cronos', 'Mobi'],
    'Hyundai': ['HB20', 'Elantra', 'Tucson', 'Creta', 'ix35'],
    'Nissan': ['March', 'Versa', 'Sentra', 'Kicks', 'Frontier'],
    'Renault': ['Sandero', 'Logan', 'Duster', 'Captur', 'Kwid'],
    'Peugeot': ['208', '2008', '3008', '5008', 'Partner'],
    'BMW': ['320i', '328i', 'X1', 'X3', 'X5', 'Serie 1'],
    'Mercedes': ['C180', 'C200', 'A200', 'GLA200', 'CLA200'],
    'Audi': ['A3', 'A4', 'Q3', 'Q5', 'TT'],
    'Tesla': ['Model 3', 'Model Y', 'Model S', 'Model X'],
    'BYD': ['Dolphin', 'Yuan Plus', 'Han', 'Tang']
}

CATEGORIAS_MARCAS = {
    'popular': ['Fiat', 'Volkswagen', 'Chevrolet', 'Ford', 'Hyundai', 'Renault'],
    'medio': ['Toyota', 'Honda', 'Nissan', 'Peugeot'],
    'premium': ['BMW', 'Mercedes', 'Audi'],
    'eletrico': ['Tesla', 'BYD']
}

# Função auxiliar para obter categoria por marca
def get_categoria_por_marca(marca: str) -> str:
    for categoria, marcas in CATEGORIAS_MARCAS.items():
        if marca in marcas:
            return categoria
    return 'medio'

class Carro:
    def __init__(self, marca, modelo, ano_fabricacao, ano_modelo, motorizacao, 
                 tipo_combustivel, transmissao, numero_portas, tipo_veiculo, 
                 quilometragem, cor, preco=None, placa=None, chassi=None, 
                 data_ultima_revisao=None):
        
        self.marca = marca
        self.modelo = modelo
        self.ano = ano_fabricacao
        self.ano_modelo = ano_modelo
        self.motorizacao = motorizacao
        self.tipo_combustivel = tipo_combustivel
        self.transmissao = transmissao
        self.numero_portas = numero_portas
        self.tipo_veiculo = tipo_veiculo
        self.quilometragem = quilometragem
        self.cor = cor
        self.preco = preco
        self.chassi = chassi
        self.placa = placa
        self.data_ultima_revisao = data_ultima_revisao
        self.data_cadastro = datetime.now()
    
    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - R$ {self.preco}"

carro = Carro