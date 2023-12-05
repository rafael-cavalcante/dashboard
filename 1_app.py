import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

if "dataset" not in st.session_state:
    st.session_state["dataset"] = pd.read_csv("src/acidentes2023_todas_causas_tipos.csv")

dataset = st.session_state["dataset"]
    
dataset_uf = dataset["uf"].unique()

estado = st.sidebar.selectbox("Estado", dataset_uf)

st.sidebar.markdown("Desenvolvido por Rafael Cavalcante")

dataset_municipios = dataset[dataset["uf"] == estado]
        
dataset_numero_acidente = dataset_municipios["municipio"].value_counts().sort_values(ascending=True)
        
dataset_tipo_acidente = dataset_municipios["tipo_acidente"].value_counts().sort_values(ascending=True)
                
fig = px.bar(x=dataset_numero_acidente.values, y=dataset_numero_acidente.index.tolist(), color=dataset_numero_acidente.values, title=f"Numero de acidentes por municipio <br>{estado}")
fig.update_layout(xaxis_title="Quantidade Acidentes", yaxis_title="Municipios")

fig2 =px.bar(x=dataset_tipo_acidente.values, y=dataset_tipo_acidente.index.tolist(), color=dataset_tipo_acidente.values, title=f"Tipos de acidentes por municipio <br>{estado}")
fig2.update_layout(xaxis_title="Quantidade", yaxis_title="Municipios")

st.title(":bar_chart: DashBoard Acidentes Rodoviarios PRF - 2023")

dataset_numero_acidente 

dataset_municipios

#col2, col3 = st.columns(2)

#col1.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, height=500)
#col2.plotly_chart(fig2, use_container_width=True)

st.subheader(f"Estado Selecionado {estado}")

tab1, tab2 = st.tabs(["Distribuição de Acidentes", "Variação de Acidentes"])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    col4, col5, col6 = st.columns([0.4, 0.4, 0.4])
    col4.metric("Maior número de Acidentes", dataset_numero_acidente.values[-1])
    col5.metric("Média número de Acidentes", round(dataset_numero_acidente.values.sum() / len(dataset_numero_acidente.values), 2))
    col6.metric("Menor número de Acidentes", dataset_numero_acidente.values[0])

    st.markdown("""---""")
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    col1 = st.columns(1)[0]
    col1.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False}, height=500)
    #st.plotly_chart(fig2, theme=None, use_container_width=True)