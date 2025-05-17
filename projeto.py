# pip install streamlit
# pip install streamlit-option-menu
# pip install plotly
# python -m streamlit run projeto.py

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurações iniciais
st.set_page_config(page_title='Dashboard de Funcionários', page_icon="📊", layout='wide')

# Carregar dados
df = pd.read_excel('relatorio_funcionarios.xlsx', sheet_name='Funcionarios')

# Verifica se colunas esperadas existem
if 'Setor' not in df.columns or 'Cargo' not in df.columns or 'Nome' not in df.columns:
    st.error("❌ As colunas 'Setor', 'Cargo' ou 'Nome' não foram encontradas na planilha.")
    st.stop()

# Sidebar
st.sidebar.header('🔎 Filtros')

# Filtro por Setor
setores = st.sidebar.multiselect(
    "Setores",
    options=df['Setor'].unique(),
    default=df['Setor'].unique()
)

# Filtro por Cargo
cargos = st.sidebar.multiselect(
    "Cargos",
    options=df['Cargo'].unique(),
    default=df['Cargo'].unique()
)

# Filtrar o DataFrame
df_selecao = df.query("Setor in @setores and Cargo in @cargos")

# Título
st.title("📊 Gráfico de Funcionários por Cargo")

# Gráfico de Barras: Funcionários e seus Cargos
fig_funcionarios = px.bar(
    df_selecao,
    x='Nome',
    color='Cargo',
    title='Funcionários e seus Cargos',
    labels={'Nome': 'Funcionário'},
    height=500
)

fig_funcionarios.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_funcionarios, use_container_width=True)
