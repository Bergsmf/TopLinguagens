import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import json

class Vagas:

    def __init__(self):
        self.path_file = Path.cwd()/'data/vagas.json'
        load_dotenv()
        self.url = os.getenv('URL')
        self.vagas = None
    
    def obtem_vagas(self):
        VALID_STATUS = 200
        response = requests.get(self.url)
        if response.status_code == VALID_STATUS:
            self.vagas = response.json()["jobs"]
        else:
            print(f'Error: {response.status_code}')

    def dump_vagas(self):
        with open(self.path_file, "w", encoding="utf-8") as arq:
            json.dump(self.vagas, arq, ensure_ascii=False, indent=4)
        
    