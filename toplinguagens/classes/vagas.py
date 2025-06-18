import json
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


class Vagas:
    def __init__(self):
        self.path_file = Path.cwd() / 'data/vagas.json'
        load_dotenv()
        self.url = os.getenv('URL')
        self.vagas = None
        self.df_vagas = None

    def obtem_vagas(self):
        VALID_STATUS = 200
        response = requests.get(self.url, timeout=10)
        if response.status_code == VALID_STATUS:
            self.vagas = response.json()['jobs']
        else:
            print(f'Error: {response.status_code}')

    def dump_vagas(self):
        with open(self.path_file, 'w', encoding='utf-8') as arq:
            json.dump(self.vagas, arq, ensure_ascii=False, indent=4)

    def organiza_vagas(self):
        file_vagas = Path.cwd() / 'data/arq_vagas.parquet'
        self.df_vagas = pd.DataFrame.from_dict(self.vagas)[
            [
                'id',
                'category',
                'tags',
                'title',
                'company_name',
                'job_type',
                'candidate_required_location',
                'salary',
                'url',
                'publication_date',
            ]
        ]
        df_info = self.df_vagas[
            [
                'id',
                'category',
                'title',
                'company_name',
                'job_type',
                'salary',
                'url',
                'publication_date',
            ]
        ].copy()
        df_info.loc[df_info['salary'] == '', 'salary'] = 'N/A'
        df_info['publication_date'] = pd.to_datetime(
            df_info['publication_date']
        ).dt.date
        df_info.to_parquet(file_vagas)

    def organiza_tecnologias(self):
        file_tecnologias = Path.cwd() / 'data/arq_tecnologias.parquet'
        df_tecnologias = (
            self.df_vagas[['id', 'tags']]
            .explode('tags', ignore_index=True)
            .reset_index(drop=True)
        )
        df_tecnologias.to_parquet(file_tecnologias)

    @staticmethod
    def formata_texto(texto):
        return [t.strip() for t in texto.split(',')]

    def organiza_locais(self):
        file_locais = Path.cwd() / 'data/arq_locais.parquet'
        self.df_vagas['candidate_required_location'] = self.df_vagas[
            'candidate_required_location'
        ].apply(self.formata_texto)
        df_locais = (
            self.df_vagas[['id', 'candidate_required_location']]
            .explode('candidate_required_location', ignore_index=True)
            .reset_index(drop=True)
        )
        df_locais.to_parquet(file_locais)
