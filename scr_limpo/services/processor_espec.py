import pandas as pd
import os
import re

class Processor_espec:
    def __init__(self, path_file, year_slice=slice(2, 22), region_slice=slice(5, 37)):
        self.path_file = path_file
        self.year_slice = year_slice
        self.region_slice = region_slice

    def process_espec(self):
        df = pd.read_excel(self.path_file)
        year = df.iloc[4, self.year_slice]
        region = df.iloc[self.region_slice, 0]
        corrente = df.iloc[self.region_slice, self.year_slice]*1000000

        return pd.DataFrame({
            'ano': year,
            'regiao': region,
            'valores_correntes': corrente
        })