#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 14:41:26 2023

@author: hamilton
"""

import pandas as pd

def normalize(word):
    return word.strip().lower()

# Caminho do arquivo Excel
caminho_arquivo = 'dados/final/pesquisa_final.xlsx'

# Número da coluna a ser lida
try:
    numero_coluna = int(input("Digite o número da coluna a ser lida: "))
except ValueError:
    print("Por favor, insira um número válido.")
    exit()

# Lista de palavras a serem buscadas
palavras_buscadas = list(map(normalize, input("Digite as palavras a serem buscadas, separadas por vírgula: ").split(',')))

try:
    # Carregar o arquivo Excel
    df = pd.read_excel(caminho_arquivo, engine='openpyxl')
except FileNotFoundError:
    print("Arquivo não encontrado. Por favor, verifique o caminho do arquivo.")
    exit()

try:
    # Nome da coluna que será lida
    coluna_lida = df.columns[numero_coluna - 1]
except IndexError:
    print("Número de coluna inválido. Por favor, verifique o número da coluna.")
    exit()

# Criar uma nova coluna para o resultado
df['Resultado'] = df[coluna_lida].apply(lambda x: 'SIM' if any(palavra in normalize(str(x)) for palavra in palavras_buscadas) else 'NÃO')

# Criar um novo arquivo Excel com os resultados
novo_caminho_arquivo = 'dados/final/segmentada_pesquisa_final.xlsx'
df.to_csv(novo_caminho_arquivo, index=False, sep = ';')

print("Segmentação concluída. Os resultados foram salvos como uma nova coluna no arquivo")
