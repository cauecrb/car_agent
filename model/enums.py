from enum import Enum

class TipoCombustivel(Enum):
    GASOLINA = "gasolina"
    ETANOL = "etanol"
    FLEX = "flex"
    DIESEL = "diesel"
    ELETRICO = "eletrico"
    HIBRIDO = "hibrido"
    GNV = "gnv"

class TipoTransmissao(Enum):
    MANUAL = "manual"
    AUTOMATICA = "automatica"
    CVT = "cvt"

class TipoVeiculo(Enum):
    HATCH = "hatch"
    SEDAN = "sedan"
    SUV = "suv"
    PICKUP = "pickup"
    CONVERSIVEL = "conversivel"
    COUPE = "coupe"
    WAGON = "wagon"
    VAN = "van"