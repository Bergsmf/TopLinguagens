from pathlib import Path

import pandas as pd
import streamlit as st


class App:
    def __init__(self):
        self.df_tecs = pd.read_parquet(
            Path.cwd() / 'data/arq_tecnologias.parquet'
        )
        self.df_tecs['tags'] = self.df_tecs['tags'].apply(
            lambda tec: tec.title() if isinstance(tec, str) else tec
        )

        self.df_locais = pd.read_parquet(
            Path.cwd() / 'data/arq_locais.parquet'
        )
        self.df_locais['candidate_required_location'] = self.df_locais[
            'candidate_required_location'
        ].apply(lambda loc: loc.upper())

        self.df_vagas = pd.read_parquet(Path.cwd() / 'data/arq_vagas.parquet')
        self.list_locais = [
            'Todos',
            'Atuando do Brasil: Worldwide, Americas, LATAM, South America, '
            'Brazil',
            'Somente Brasil',
        ]

        self.ids_vagas = self.df_vagas['id'].to_list()

        self.list_categorias = sorted(set(self.df_vagas['category'].to_list()))

    def combinacoes(self, habilidade: str) -> list:
        list_id = self.df_tecs.loc[
            (self.df_tecs['tags'] == habilidade)
            & (self.df_tecs['id'].isin(self.ids_vagas)),
            'id',
        ].unique()
        list_tec = (
            self.df_tecs[
                (self.df_tecs['id'].isin(list_id))
                & (self.df_tecs['tags'] != habilidade)
            ]['tags']
            .value_counts()
            .to_frame(name='ocorrencias')
            .sort_values(by=['ocorrencias'], ascending=False)
            .head(5)
            .index.to_list()
        )
        return list_tec

    def obtem_datas(self):
        st.title('Vagas disponíveis por data de abertura')
        df_days = (
            self.df_vagas[['id', 'publication_date']]
            .groupby('publication_date')['id']
            .nunique()
            .to_frame(name='qt_vagas')
            .sort_values(by=['publication_date'])
        )
        st.line_chart(data=df_days['qt_vagas'], use_container_width=True)

    def areas_mais_requisitadas(self):
        st.title('Áreas mais requisitadas')
        st.markdown('### Vagas por área')
        df_area = (
            self.df_vagas['category']
            .value_counts()
            .to_frame(name='vagas')
            .reset_index()
            .sort_values(by='vagas', ascending=False)
        )
        pd.set_option('display.max_colwidth', None)
        st.bar_chart(data=df_area['vagas'], use_container_width=True)
        st.dataframe(df_area.reset_index(drop=True), use_container_width=True)

    def tec_mais_requisitadas(self):
        st.title('Habilidades mais requisitadas')
        st.markdown('### E habilidades que são também pedidas  junto com elas')
        opcoes_categoria = ['Todas as categorias', 'Escolher categoria']
        area_select = st.radio('Deseja listar', opcoes_categoria, index=0)
        if area_select == opcoes_categoria[0]:
            pass
        elif area_select == opcoes_categoria[1]:
            area_select = st.selectbox(
                'Escolha sua categoria', self.list_categorias
            )
            self.ids_vagas = self.df_vagas[
                self.df_vagas['category'] == area_select
            ]['id'].to_list()

        df_habilidades = (
            self.df_tecs[self.df_tecs['id'].isin(self.ids_vagas)]['tags']
            # .groupby("tags")
            .value_counts()
            .to_frame(name='ocorrencias')
            .sort_values(by=['ocorrencias'], ascending=False)
            .reset_index()
            .head(10)
        )
        df_habilidades['combina_com'] = df_habilidades['tags'].apply(
            self.combinacoes
        )
        pd.set_option('display.max_colwidth', None)
        st.dataframe(df_habilidades, use_container_width=True)

    def busca_vaga(self):
        st.title('Busque sua vaga')
        list_atuando_br = [
            'WORLDWIDE',
            'AMERICAS',
            'LATAM',
            'SOUTH AMERICA',
            'BRAZIL',
        ]
        df_lista_vagas = self.df_tecs
        df_lista_locais = self.df_locais
        df_listas = pd.DataFrame(
            df_lista_vagas['tags'].unique(), columns=['Tecnologia']
        )
        df_listas = df_listas.sort_values(by='Tecnologia').reset_index(
            drop=True
        )
        tec_select = st.selectbox('Escolha sua tecnologia', df_listas)
        local_select = st.radio(
            'Escolha o local de atuação',
            self.list_locais,
            index=0,
        )
        lista_id_vagas = (
            df_lista_vagas[df_lista_vagas['tags'] == tec_select]['id']
            .unique()
            .tolist()
        )
        if local_select == self.list_locais[0]:
            lista_loc = df_lista_locais['id'].unique().tolist()
        elif local_select == self.list_locais[1]:
            lista_loc = (
                df_lista_locais[
                    df_lista_locais['candidate_required_location'].isin(
                        list_atuando_br
                    )
                ]['id']
                .unique()
                .tolist()
            )
        elif local_select == self.list_locais[2]:
            lista_loc = (
                df_lista_locais[
                    df_lista_locais['candidate_required_location'] == 'BRAZIL'
                ]['id']
                .unique()
                .tolist()
            )

        df_tec_escolhida = self.df_vagas[
            (self.df_vagas['id'].isin(lista_id_vagas))
            & (self.df_vagas['id'].isin(lista_loc))
        ]
        if not (df_tec_escolhida.empty):
            st.dataframe(df_tec_escolhida, use_container_width=True)
        else:
            st.write('Nenhuma vaga encontrada para esses filtros')


if __name__ == '__main__':
    app = App()
    app.obtem_datas()
    app.areas_mais_requisitadas()
    app.tec_mais_requisitadas()
    app.busca_vaga()
