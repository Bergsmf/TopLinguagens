from pathlib import Path

import pandas as pd
import streamlit as st


def combinacoes(habilidade: str) -> list:
    df = pd.read_parquet(Path.cwd() / 'data/arq_tecnologias.parquet')
    list_id = df.loc[df['tags'] == habilidade, 'id'].unique()
    list_tec = (
        df[(df['id'].isin(list_id)) & (df['tags'] != habilidade)]['tags']
        .value_counts()
        .to_frame(name='ocorrencias')
        .sort_values(by=['ocorrencias'], ascending=False)
        .head(5)
        .index.to_list()
    )
    return list_tec


def obtem_datas():
    st.title('Vagas disponíveis por data de abertura')
    df_days = (
        pd.read_parquet(Path.cwd() / 'data/arq_vagas.parquet')[
            ['id', 'publication_date']
        ]
        .groupby('publication_date')['id']
        .nunique()
        .to_frame(name='qt_vagas')
        .sort_values(by=['publication_date'])
    )
    st.line_chart(data=df_days['qt_vagas'], use_container_width=True)


def areas_mais_requisitadas():
    st.title('Áreas mais requisitadas')
    st.markdown('### Vagas por área')
    df_area = pd.read_parquet(Path.cwd() / 'data/arq_vagas.parquet')
    df_area = (
        df_area['category']
        .value_counts()
        .to_frame(name='vagas')
        .reset_index()
        .sort_values(by='vagas', ascending=False)
    )
    pd.set_option('display.max_colwidth', None)
    st.bar_chart(data=df_area['vagas'], use_container_width=True)
    st.dataframe(df_area.reset_index(drop=True), use_container_width=True)


def tec_mais_requisitadas():
    st.title('Habilidades mais requisitadas')
    st.markdown('### E habilidades que são também pedidas  junto com elas')
    df_habilidades = (
        pd.read_parquet(Path.cwd() / 'data/arq_tecnologias.parquet')[['tags']]
        .groupby('tags')
        .value_counts()
        .to_frame(name='ocorrencias')
        .sort_values(by=['ocorrencias'], ascending=False)
        .reset_index()
        .head(10)
    )
    df_habilidades['combina_com'] = df_habilidades['tags'].apply(combinacoes)
    pd.set_option('display.max_colwidth', None)
    st.dataframe(df_habilidades, use_container_width=True)


def busca_vaga():
    st.title('Busque sua vaga')
    df_lista_vagas = pd.read_parquet(
        Path.cwd() / 'data/arq_tecnologias.parquet'
    )
    df_lista_vagas['tags'] = df_lista_vagas['tags'].apply(
        lambda tec: tec.title() if isinstance(tec, str) else tec
    )
    df_lista_locais = pd.read_parquet(Path.cwd() / 'data/arq_locais.parquet')
    df_lista_locais['candidate_required_location'] = df_lista_locais[
        'candidate_required_location'
    ].apply(lambda loc: loc.upper())
    df_listas = pd.DataFrame(
        df_lista_vagas['tags'].unique(), columns=['Tecnologia']
    )
    df_listas = df_listas.sort_values(by='Tecnologia').reset_index(drop=True)
    tec_select = st.selectbox('Escolha sua tecnologia', df_listas)
    local_select = st.radio(
        'Escolha o local de atuação',
        [
            'Todos',
            'Atuando do Brasil: Worldwide, Americas, LATAM, South America, '
            'Brazil',
            'Somente Brasil',
        ],
        index=0,
    )
    lista_id_vagas = (
        df_lista_vagas[df_lista_vagas['tags'] == tec_select]['id']
        .unique()
        .tolist()
    )
    df_vagas = pd.read_parquet(Path.cwd() / 'data/arq_vagas.parquet')

    match local_select:
        case 'Todos':
            lista_loc = df_lista_locais['id'].unique().tolist()
        case (
            'Atuando do Brasil: Worldwide, Americas, LATAM'
            ', South America, Brazil'
        ):
            locais = [
                'WORLDWIDE',
                'AMERICAS',
                'LATAM',
                'SOUTH AMERICA',
                'BRAZIL',
            ]
            lista_loc = (
                df_lista_locais[
                    df_lista_locais['candidate_required_location'].isin(locais)
                ]['id']
                .unique()
                .tolist()
            )
        case 'Somente Brasil':
            lista_loc = (
                df_lista_locais[
                    df_lista_locais['candidate_required_location'] == 'BRAZIL'
                ]['id']
                .unique()
                .tolist()
            )

    df_tec_escolhida = df_vagas[
        (df_vagas['id'].isin(lista_id_vagas))
        & (df_vagas['id'].isin(lista_loc))
    ]
    if not (df_tec_escolhida.empty):
        st.dataframe(df_tec_escolhida, use_container_width=True)
    else:
        st.write('Nenhuma vaga encontrada para esses filtros')


if __name__ == '__main__':
    obtem_datas()
    areas_mais_requisitadas()
    tec_mais_requisitadas()
    busca_vaga()
