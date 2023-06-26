#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 12:45:24 2023

@author: hamilton
"""

"""UNIFICAR TODOs OS ARQUIVOS CSV EM UMA PASTA"""

import pandas as pd
import os
import glob

# Definir o caminho para a pasta com os arquivos CSV
path = "dados/final/"

# Obtém todos os nomes de arquivo
all_files = glob.glob(os.path.join(path, "*.csv"))

# Cria uma lista para armazenar cada DataFrame
df_list = []

# lê o CSV em um DataFrame e adicione-o à lista
for file in all_files:
    df_list.append(pd.read_csv(file, sep=';', header=None))

# Concatena todos os DataFrames na lista em um único DataFrame
merged_df = pd.concat(df_list, ignore_index=True)

# Salva o DataFrame unificado em um novo arquivo CSV
merged_df.to_csv("dados/final/pesquisa_final.csv", index=False, sep=';', header=None)

all_files = glob.glob(os.path.join(path, "*.csv"))
print(all_files)
