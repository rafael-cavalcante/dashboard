import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Dashboard PRF",
    page_icon=":bar_chart:",
    layout="wide")

if "dataset" not in st.session_state:
    st.session_state["dataset"] = pd.read_csv("database/acidentes2023_todas_causas_tipos.csv")

dataset = st.session_state["dataset"]
    
dataset_uf = dataset["uf"].unique()

st.sidebar.success("Selecione uma pagina acima.")

st.sidebar.header("Dashboard `version 2`")

st.sidebar.subheader('DashMob')

estado = st.sidebar.selectbox("Estado", dataset_uf)

fig1_height = st.sidebar.slider('Specify plot height', 400, 1000, 400)

st.sidebar.divider()

st.sidebar.markdown("<h3 style='text-align: center;'>Desenvolvido por Rafael Cavalcante</h3>", unsafe_allow_html=True)

#Gráfico de Número Acidentes Por Municipio
dataset_municipios = dataset[dataset["uf"] == estado]

dataset_numero_acidente = dataset_municipios["municipio"].value_counts().sort_values(ascending=True)

fig = px.bar(x=dataset_numero_acidente.values, y=dataset_numero_acidente.index, color=dataset_numero_acidente.index, title=f"Numero de acidentes por municipio <br>{estado}")
fig.update_layout(xaxis_title="Quantidade Acidentes", yaxis_title="Municipios", height=fig1_height, margin=dict(l=0, r=0, b=0, t=40))

#Gráfico de Número de Tipos Acidentes Por Municipio
dataset_tipo_acidente = dataset_municipios["tipo_acidente"].value_counts().sort_values(ascending=True)

fig2 =px.bar(x=dataset_tipo_acidente.values, y=dataset_tipo_acidente.index, color=dataset_tipo_acidente.index, title=f"Tipos de acidentes por municipio <br>{estado}")
fig2.update_layout(xaxis_title="Quantidade Acidentes", yaxis_title="Municipios", height=500)

#Interface do Dashboard
st.title(":bar_chart: DashBoard Acidentes Rodoviarios PRF - 2023")

st.subheader(f"Estado Selecionado {estado}")

tab1, tab2 = st.tabs(["Distribuição de Acidentes", "Variação de Acidentes"])

total_acidentes_estado = dataset_numero_acidente.values.sum()

total_municipios_estado = len(dataset_numero_acidente.values)

with tab1:
    col1, col2, col3 = st.columns([0.4, 0.4, 0.4])
    col1.metric("Maior número de Acidentes", dataset_numero_acidente.values[-1])
    col2.metric("Média número de Acidentes", round(total_acidentes_estado / total_municipios_estado, 2))
    col3.metric("Menor número de Acidentes", dataset_numero_acidente.values[0])

    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.plotly_chart(fig2, use_container_width=True)
    
#Gráfico de Concentração de acidentes
dataset2 = dataset_municipios[["dia_semana", "horario", "data_inversa"]]
    
ordem_dias_semana = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
dataset2['dia_semana'] = pd.Categorical(dataset2['dia_semana'], categories=ordem_dias_semana, ordered=True)

dataset2['data_hora'] = pd.to_datetime(dataset2['data_inversa'] + ' ' + dataset2['horario'], format='%Y-%m-%d %H:%M:%S')

#dataset2['horario'] = pd.to_datetime(dataset2['horario'], format='%H:%M:%S').dt.time

dataset2 = dataset2.sort_values(by=["dia_semana", "data_hora"])

fig3 = px.scatter(dataset2, x="data_hora", y="dia_semana", color="dia_semana", title=f"Concentração de acidentes por dia/horario <br>{estado}")
fig3.update_layout(xaxis_title="Horario Acidentes", yaxis_title="Dias Semana", height=500)

st.plotly_chart(fig3, use_container_width=True)