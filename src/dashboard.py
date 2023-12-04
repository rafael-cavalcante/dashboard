import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

dataset = pd.read_csv("src/acidentes2023_todas_causas_tipos.csv")

dataset_uf = dataset["uf"].unique()

estado = st.sidebar.selectbox("Estado", dataset_uf)

dataset_municipios = dataset[dataset["uf"] == estado]
        
dataset_numero_acidente = dataset_municipios["municipio"].value_counts().sort_values(ascending=False)
        
dataset_tipo_acidente = dataset_municipios["tipo_acidente"].value_counts().sort_values(ascending=True)
                
fig = px.bar(x=dataset_numero_acidente.values, y=dataset_numero_acidente.index.tolist(), color=dataset_numero_acidente.values, title=f"Numero de acidentes por municipio <br><sup>{estado}</sup>")
fig.update_layout(xaxis_title="Quantidade Acidentes", yaxis_title="Municipios")

fig2 =px.bar(x=dataset_tipo_acidente.values, y=dataset_tipo_acidente.index.tolist(), color=dataset_tipo_acidente.values, title=f"Tipos de acidentes por municipio <br><sup>{estado}</sup>")
fig2.update_layout(xaxis_title="Quantidade", yaxis_title="Municipios")

st.title("DashBoard Acidentes Rodoviarios PRF - 2023")

dataset_municipios

st.subheader(f"Estado Selecionado {estado}")

col1 = st.columns(1)[0]
col2, col3 = st.columns(2)

col1.plotly_chart(fig, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)