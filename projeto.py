import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregamento dos dados
@st.cache_data
def load_data():
    df_func = pd.read_excel("funcionarios_corrigido.xlsx")
    df_freq = pd.read_excel("frequencia_corrigida.xlsx")
    df = pd.merge(df_freq, df_func, on="Id_funcionario", how="left")
    df['Data'] = pd.to_datetime(df['Data'])
    df['Horas_extras'] = pd.to_numeric(df['Horas_extras'], errors='coerce').fillna(0)
    df['Faltou'] = df['Falta_analisada'] == 'Falta'
    df['Dia_da_semana'] = df['Data'].dt.day_name()
    return df

df = load_data()

st.title("Delicias do Campo - Analise do Departamento de RH")

# Filtros interativos
setores = st.multiselect("Filtrar por setor:", options=df['Setor'].unique(), default=df['Setor'].unique())
turnos = st.multiselect("Filtrar por turno:", options=df['Turno'].unique(), default=df['Turno'].unique())
cargos = st.multiselect("Filtrar por cargo:", options=df['Cargo'].unique(), default=df['Cargo'].unique())

df = df[df['Setor'].isin(setores) & df['Turno'].isin(turnos) & df['Cargo'].isin(cargos)]

st.header("Horas Extras por Setor")
extras_setor = df.groupby("Setor")["Horas_extras"].sum().sort_values(ascending=False)
st.bar_chart(extras_setor)

st.header("Horas Extras por Funcionário (Top 10)")
extras_func = df.groupby(["Id_funcionario", "Nome"])["Horas_extras"].sum().sort_values(ascending=False).head(10)
st.dataframe(extras_func.reset_index())

st.header("Faltas por Setor")
faltas_setor = df[df["Faltou"]].groupby("Setor")["Faltou"].count().sort_values(ascending=False)
st.bar_chart(faltas_setor)

st.header("Faltas por Funcionário (Top 10)")
faltas_func = df[df["Faltou"]].groupby(["Id_funcionario", "Nome"])["Faltou"].count().sort_values(ascending=False).head(10)
st.dataframe(faltas_func.reset_index())

st.header("Dias com Mais Faltas")
faltas_dia = df[df["Faltou"]].groupby("Data")["Faltou"].count().sort_values(ascending=False).head(10)
st.line_chart(faltas_dia)

st.header("Padrões de Faltas por Dia da Semana")
faltas_semana = df[df["Faltou"]].groupby("Dia_da_semana")["Faltou"].count()
ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
faltas_semana = faltas_semana.reindex(ordem_dias)

fig, ax = plt.subplots()
sns.barplot(x=faltas_semana.index, y=faltas_semana.values, ax=ax)
plt.xticks(rotation=45)
plt.ylabel("Faltas")
plt.title("Faltas por Dia da Semana")
st.pyplot(fig)

st.header("Setores com Potencial Sobrecarga")

sobrecarga = pd.DataFrame({
    'Horas_extras': df.groupby('Setor')['Horas_extras'].sum(),
    'Faltas': df[df['Faltou']].groupby('Setor')['Faltou'].count()
}).fillna(0)
sobrecarga['Indice_sobrecarga'] = sobrecarga['Horas_extras'] * 0.7 + sobrecarga['Faltas'] * 0.3
sobrecarga = sobrecarga.sort_values(by='Indice_sobrecarga', ascending=False)
st.dataframe(sobrecarga.reset_index())
