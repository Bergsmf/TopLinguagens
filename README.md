# TopLinguagens
![Python](https://img.shields.io/badge/Python-3.12%2B-2a9d8f)
![Pandas](https://img.shields.io/badge/Pandas-2.3.0-e9c46a)
![Pytest](https://img.shields.io/badge/Pytest-8.4.0-e76f51)
![Requests](https://img.shields.io/badge/Requests-2.32.4-f4a261)
![Ruff](https://img.shields.io/badge/Ruff-0.11.13-8a4fff)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-ff4b4b)
![Taskipy](https://img.shields.io/badge/Taskipy-1.14.1-2e7d32)


## Descrição
Utilizei a API do site [Remotive](https://remotive.com/) para obter os dados sobre vagas disponíveis. Sabe quando quer tentar entender o mercado de trabalho? Quais as tecnologias estão sendo mais requisitades? O que precisa estudar além do requisito principal? Esse projeto tem como objetivo responder essas perguntas.

### 1. Leitura dos dados:
- Os dados são baixados através de um requisição pelo Requests;
- Em seguida é salvo o arquivo vagas.json;

### 2. Organização dos dados:
- Como as vagas podem aceitar diferentes localizações e requisitar diversas tecnologias, os dados foram separados em 3 arquivos;
- arq_vagas.parquet: São as informações gerais da vaga;
- arq_locais.parquet: Um explode() das localizações aceitas de cada vaga;
- arq_tecnologias.parquet: Um explode() dos requisitos técnicos da vaga;

### 3. Visualização de Dados:
- Foi utilizado o Streamlit para a visualização dos dados:

### CI
- A branch main foi bloqueada para push. Utilizo a branch develop e pull request. Além de uma etapa de CI:

### Taskipy

Coloquei no projeto o taskipy para facilitar a execução de comandos comuns durante o desenvolvimento. Abaixo estão as tarefas disponíveis:

poetry run task <nome_da_tarefa>
Tarefas disponíveis
| Tarefa | Descrição |
| --- | --- |
| lint | Executa o linter ruff para verificar problemas de formatação e estilo. |
| pre_format | Corrige automaticamente problemas detectados pelo ruff. |
| format | Aplica o estilo de formatação definido (ruff format). |
| pre_run | Executa o script main.py para processar e carregar os dados. |
| run | Inicia a aplicação com Streamlit (toplinguagens/app.py). |
| pre_test | Executa o lint automaticamente antes dos testes. |
| test | Executa os testes usando pytest em modo verboso. |

Observação: as tarefas pre_run e pre_test são chamadas automaticamente antes das tarefas run e test, respectivamente.

## Estrutura de Diretórios
<pre lang="markdown"><code>.
.
├── .github
│   └── workflows
│       └── CI.yaml
├── README.md
├── data
│   ├── arq_locais.parquet
│   ├── arq_tecnologias.parquet
│   ├── arq_vagas.parquet
│   └── vagas.json
├── poetry.lock
├── pyproject.toml
├── tests
│   └── test_vagas.py
└── toplinguagens
    ├── app.py
    ├── classes
    │   └── vagas.py
    └── loader.py
</code></pre>

## Imagens

### Vendas no mês
![Vagas abertas por data](toplinguagens/img/Vagas_abertas_data.png)

### Linguagens mais requisitadas
![Mais requisitadas](toplinguagens/img/Principais_requisitos.png)

### Produtos mais vendidos por mês
![Filtro tecnologia](toplinguagens/img/Filtro_requisitos.png)
![Filtro localizacao](toplinguagens/img/Filtro_localizacao.png)
![Vagas Filtradas](toplinguagens/img/Vagas_filtradas.png)