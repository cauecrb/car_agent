#!/bin/bash

echo "Iniciando Agente IA de Carros..."
echo

if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Instalando dependências..."
pip install -r requirements.txt

echo
echo "Iniciando agente IA..."
python3 ai_virtual_agent.py

read -p "Pressione Enter para continuar..."