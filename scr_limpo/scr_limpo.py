import pandas as pd
import os
import re
from pathlib import Path
import sys

project_root = Path().resolve().parent
raw_path = project_root / 'data' / 'raw'
processed_path = project_root / 'data' / 'processed'

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scr_limpo.services.processor_scr import Processor_scr
from scr_limpo.services.downloader import Downloader
from scr_limpo.services.processor_espec import Processor_espec

URL_PROD = 'https://ftp.ibge.gov.br/Contas_Regionais/2022/xls/Conta_da_Producao_2002_2022_xls.zip'
URL_ESPEC = 'https://ftp.ibge.gov.br/Contas_Regionais/2022/xls/Especiais_2002_2022_xls.zip'
downloader_prod = Downloader(URL_PROD, raw_path / 'prod')
downloader_prod.run()
download_espec = Downloader(URL_ESPEC, raw_path / 'espec')
download_espec.run()

##################### PROCESSAMENTO DA PLANILHA DE PRODUÇÃO #####################
dfs = {
    'VAB': [],
    'VAB_Agro': [],
    'VAB_Extrativa': [],
    'VAB_Manufatura': [],
    'VAB_SIUP': [],
    'VAB_Construção': [],
    'VAB_Comércio': [],
    'VAB_Transporte': [],
    'VAB_Info e Comunicação': [],
    'VAB_Atividades Financeiras': [],
    'VAB_Imobiliárias': [],
    'VAB_Administrativas': [],
    'VAB_Outros Serviços': []
}
abas = {
    'VAB': '.1',
    'VAB_Agro': '.2',
    'VAB_Extrativa': '.3',
    'VAB_Manufatura': '.4',
    'VAB_SIUP': '.5',
    'VAB_Construção': '.6',
    'VAB_Comércio': '.7',
    'VAB_Transporte': '.8',
    'VAB_Info e Comunicação': '.9',
    'VAB_Atividades Financeiras': '.10',
    'VAB_Imobiliárias': '.11',
    'VAB_Administrativas': '.12',
    'VAB_Outros Serviços': '.13'
}

for arquivo in os.listdir(raw_path / 'prod'):
    if arquivo.endswith(('.xlsx', '.xls')):
        num = re.search(r'Tabela(\d+)', arquivo)
        if num:
            num_tabela = num.group(1)
            path_file = os.path.join(raw_path / 'prod', arquivo)
            for nome, sufixo in abas.items():
                processor = Processor_scr(path_file, f'Tabela{num_tabela}{sufixo}')
                dfs[nome].append(processor.process_prod())

with pd.ExcelWriter(processed_path / 'prod/scr_prod.xlsx') as writer:
    for nome, frames in dfs.items():
        pd.concat(frames, ignore_index=True).to_excel(writer, sheet_name=nome, index=False)