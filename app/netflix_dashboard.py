import streamlit as st
import pandas as pd
import plotly.express as px
import os


# Configuração da página
st.set_page_config(page_title="Análise Netflix", page_icon="🎬", layout="wide")

# Carregamento de dados (caminho seguro)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 2 níveis acima de app/
DATA_PATH = os.path.join(BASE_DIR, 'data', 'netflix_titles.csv')

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['main_genre'] = df['listed_in'].str.split(',').str[0]
    return df

df = load_data()

# Título e descrição
st.title("🎬 Dashboard - Análise Exploratória da Netflix")
st.markdown("Visualize tendências de conteúdo, gêneros e países na plataforma Netflix.")

# Filtros
col1, col2 = st.columns(2)

with col1:
    tipo = st.multiselect("Filtrar por Tipo", df['type'].unique(), default=df['type'].unique())

with col2:
    ano = st.slider("Ano de Lançamento", int(df['release_year'].min()), int(df['release_year'].max()), (2010, 2020))

df_filtered = df[(df['type'].isin(tipo)) & 
                 (df['release_year'].between(ano[0], ano[1]))]

# Visão geral
st.header(" Visão Geral dos Dados")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Títulos", len(df_filtered))
col2.metric("Países Diferentes", df_filtered['country'].nunique())
col3.metric("Gêneros Principais", df_filtered['main_genre'].nunique())

# Visualizações
tab1, tab2, tab3, tab4 = st.tabs(["Tipo de Conteúdo", "Países", "Gêneros", "Tendência por Ano"])

with tab1:
    st.subheader("Distribuição de Tipos de Conteúdo")
    type_counts = df_filtered['type'].value_counts()
    fig = px.pie(values=type_counts.values, names=type_counts.index, 
                 color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Top 10 Países com Mais Produções")
    top_countries = df_filtered['country'].value_counts().head(10)
    fig = px.bar(x=top_countries.values, y=top_countries.index, orientation='h', 
                 color=top_countries.values, color_continuous_scale='reds',
                 labels={'x':'Quantidade', 'y':'País'})
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Gêneros Mais Comuns")
    top_genres = df_filtered['main_genre'].value_counts().head(10)
    fig = px.bar(x=top_genres.index, y=top_genres.values, 
                 color=top_genres.values, color_continuous_scale='blues',
                 labels={'x':'Gênero','y':'Quantidade'})
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Evolução de Lançamentos por Ano")
    releases_per_year = df_filtered['release_year'].value_counts().sort_index()
    fig = px.line(x=releases_per_year.index, y=releases_per_year.values, markers=True,
                  labels={'x':'Ano','y':'Quantidade de Títulos'})
    st.plotly_chart(fig, use_container_width=True)

# Séries vs Filmes
st.header("🎞️ Séries vs Filmes ao Longo dos Anos")
type_year = df_filtered.groupby(['release_year', 'type']).size().unstack().fillna(0)
fig = px.line(type_year, x=type_year.index, y=type_year.columns, markers=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Feito por Justino Felipe — Dados da Netflix (Kaggle)")
