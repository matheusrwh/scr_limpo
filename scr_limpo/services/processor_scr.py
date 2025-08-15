import pandas as pd
import os
import re

class Processor_scr:
    '''
    Com essa classe é possível processar as planilhas do Sistema de Contas Regionais do IBGE (SCR).
    Basta incluir todas as tabelas do SCR na pasta 'data/raw' do projeto (ou em qualquer outra, desde que você ajuste o caminho) e executar o script.
    A classe processa as tabelas por abas, retornando uma planilha com as seguintes colunas:
    - ano: Ano da série histórica
    - regiao: região do país ou UF
    - setor: setor da atividade econômica
    - valores_correntes: valores correntes do VAB
    - deflator: deflator regional do VAB
    - valores_reais: valores reais do VAB
    Por hora, apenas o VAB é processado, mas a caso haja necessidade é relativamente fácil adaptar o script para processar também os dados do VBP e do CI.
    '''
    def __init__(self, path_file, aba, year_slice=slice(59, 80), region_row=56, setor_row=57):
        self.path_file = path_file
        self.aba = aba
        self.year_slice = year_slice
        self.region_row = region_row
        self.setor_row = setor_row

    def process_prod(self):
        df = pd.read_excel(self.path_file, sheet_name=self.aba)
        year = df.iloc[self.year_slice, 0]
        price = df.iloc[self.year_slice, 4]
        corrente = df.iloc[self.year_slice, 5]*1000000 # NOTAR QUE O SCRIPT JÁ APLICA O FATOR DE CONVERSÃO PARA MILHÕES DE REAIS
        region = df.iloc[self.region_row, 0]
        setor = df.iloc[self.setor_row, 0]

        acumulado = price.copy()
        acumulado.iloc[0] = 1
        for i in range(1, len(acumulado)):
            acumulado.iloc[i] = price.iloc[i] * acumulado.iloc[i-1]

        deflator = acumulado/acumulado.iloc[-1]
        reais = corrente/deflator

        return pd.DataFrame({
            'ano': year,
            'regiao': region,
            'setor': setor,
            'valores_correntes': corrente,
            'deflator': deflator,
            'valores_reais': reais
        })