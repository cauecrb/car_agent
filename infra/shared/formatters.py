from typing import Dict, Any, List

def format_price_range(price_range: Dict[str, Any]) -> str:
    try:
        min_price = price_range.get('min', 0)
        max_price = price_range.get('max', 0)
        
        if isinstance(min_price, (int, float)) and isinstance(max_price, (int, float)):
            return f"R$ {min_price:,.2f} - R$ {max_price:,.2f}"
        else:
            return "Não disponível"
    except:
        return "Não disponível"

def format_car_summary(car: Dict[str, Any], index: int) -> str:
    return (f"{index}. {car['marca']} {car['modelo']} ({car['ano']}) - "
            f"R$ {car['preco']:,.2f} - {car['cor']} - "
            f"{car['quilometragem']:,} km - Placa: {car['placa']}")

#informaçoes detalhadas
def format_car_detailed(car: Dict[str, Any], index: int) -> str:
    # Formatação da data de última revisão
    ultima_revisao = car.get('data_ultima_revisao')
    if ultima_revisao:
        from datetime import datetime
        try:
            data_obj = datetime.fromisoformat(ultima_revisao.replace('Z', '+00:00'))
            ultima_revisao_formatada = data_obj.strftime('%d/%m/%Y')
        except:
            ultima_revisao_formatada = 'Data inválida'
    else:
        ultima_revisao_formatada = 'Nunca revisado'
    
    # Formatação da data de cadastro
    data_cadastro = car.get('data_cadastro')
    if data_cadastro:
        try:
            data_obj = datetime.fromisoformat(data_cadastro.replace('Z', '+00:00'))
            data_cadastro_formatada = data_obj.strftime('%d/%m/%Y')
        except:
            data_cadastro_formatada = 'Data inválida'
    else:
        data_cadastro_formatada = 'N/A'
    
    return f"""{index}. {car['marca']} {car['modelo']} ({car.get('ano_fabricacao', 'N/A')})
   • Preço: R$ {car['preco']:,.2f}
   • Cor: {car['cor']}
   • Quilometragem: {car['quilometragem']:,} km
   • Combustível: {car.get('tipo_combustivel', 'N/A').title()}
   • Transmissão: {car.get('transmissao', 'N/A').title()}
   • Número de portas: {car.get('numero_portas', 'N/A')}
   • Motorização: {car.get('motorizacao', 'N/A')}
   • Tipo de veículo: {car.get('tipo_veiculo', 'N/A').title()}
   • Ano de fabricação: {car.get('ano_fabricacao', 'N/A')}
   • Ano do modelo: {car.get('ano_modelo', 'N/A')}
   • Placa: {car['placa']}
   • Chassi: {car.get('chassi', 'N/A')}
   • Data de cadastro: {data_cadastro_formatada}
   • Última revisão: {ultima_revisao_formatada}"""