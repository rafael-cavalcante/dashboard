import pandas as pd
import plotly.express as px
import streamlit as st

import json

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

#dataset_uf = list(dataset_uf)

#dataset_uf.insert(0, "TODOS")

estado = st.sidebar.selectbox("Estado", dataset_uf)

fig1_height = st.sidebar.slider('Specify plot height', 400, 1000, 400)

st.sidebar.divider()

st.sidebar.markdown("<h3 style='text-align: center;'>Desenvolvido por Rafael Cavalcante</h3>", unsafe_allow_html=True)

#Gráfico de Número Acidentes Por Municipio
if(estado != "TODOS"):
    dataset_municipios = dataset[dataset["uf"] == estado]
else:
    dataset_municipios = dataset


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
dataset2 = dataset_municipios[["dia_semana", "data_inversa", "horario"]]

ordem_dias_semana = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']

dataset2 = dataset2.copy()

dataset3 = dataset2.copy()

dataset2['horario'] = pd.to_datetime(dataset2['data_inversa'], format='%Y-%m-%d')

dataset3['horario'] = pd.to_datetime(dataset3['horario'], format='%H:%M:%S').dt.time

dataset2['dia_semana'] = pd.Categorical(dataset2['dia_semana'], categories=ordem_dias_semana, ordered=True)

dataset3['dia_semana'] = pd.Categorical(dataset3['dia_semana'], categories=ordem_dias_semana, ordered=True)

dataset2 = dataset2.sort_values(by=["dia_semana", "horario"]).reset_index(drop=True)

dataset3 = dataset3.sort_values(by=["dia_semana", "horario"]).reset_index(drop=True)

fig3 = px.scatter(dataset2, x="horario", y="dia_semana", color="dia_semana", title=f"Concentração de acidentes por dia/horario <br>{estado}")
fig3.update_layout(xaxis_title="Horario Acidentes", yaxis_title="Dias Semana", height=500)

fig5 = px.scatter(dataset3, x="horario", y="dia_semana", color="dia_semana", title=f"Concentração de acidentes por dia/horario <br>{estado}")
fig5.update_layout(xaxis_title="Horario Acidentes", yaxis_title="Dias Semana", height=500)

st.plotly_chart(fig3, use_container_width=True)

df = dataset2.copy()

df2 = dataset2.copy()

df['ano_mes'] = dataset2['horario'].dt.to_period('M')

valores_unicos = dataset2['horario'].dt.date.unique()

options = st.multiselect(
    'What are your favorite colors',
    valores_unicos)

df2= dataset2[dataset2['horario'].dt.date.isin(options)]

df2

st.plotly_chart(fig5, use_container_width=True)


#Gráfico distribuição dos acidentes nos estados brasileiros
geojson = json.load(open("database/uf.json"))

acidentes = dataset["uf"].value_counts().reset_index()
acidentes.columns = ["uf", "quantidade"]

fig_mapa = px.choropleth(
    acidentes,
    geojson=geojson,
    locations="uf",
    featureidkey="properties.UF_05",
    projection="mercator", 
    hover_data="uf",
    color="quantidade",
    color_continuous_scale="Reds",
    range_color=(0, acidentes["quantidade"].max()),
    scope="south america"
)

st.plotly_chart(fig_mapa, use_container_width=True)

fig4 = px.choropleth_mapbox(
    acidentes,
    geojson=geojson,  # Seu GeoJSON
    featureidkey="properties.UF_05",  # Chave de identificação no GeoJSON
    locations="uf",
    color="quantidade",
    color_continuous_scale="Reds",
    range_color=(0, acidentes["quantidade"].max()),
    mapbox_style="carto-positron",  # Escolha um estilo do Mapbox
    center={"lat": -14.235, "lon": -51.9253},  # Coordenadas do centro do Brasil
    zoom=2.0,  # Nível de zoom inicial
    opacity=0.7,
    title="Choropleth Map of Accidents in Brazilian States",
)

mapbox_token = "pk.eyJ1IjoicmFmYWVsY2F2YWxjYW50ZSIsImEiOiJjbHB0dGZsZngwZXl2Mmpxa2pqY3Ryb3p4In0.kb1XHjIXDxDopdsDA0a_jA"

fig4.update_layout(mapbox=dict(accesstoken=mapbox_token))  # Substitua 'mapbox_token' pelo seu token Mapbox

st.plotly_chart(fig4, use_container_width=True)
