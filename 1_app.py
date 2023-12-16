import pandas as pd
import plotly.express as px
import streamlit as st
import json as jn

st.set_page_config(
    page_title="DashMob",
    page_icon="📊",
    layout="wide")

if ("dataset" not in st.session_state):
    st.session_state["dataset"] = pd.read_csv("database/acidentes2023_todas_causas_tipos.csv")

df = st.session_state["dataset"]
    
df2 = df.copy() 

try:
    with open("database/uf.json", "r", encoding="utf-8") as f:
        geojson_estados = jn.load(f)
except Exception as e:
    print(f"Erro ao carregar o arquivo JSON: {e}")
    
try:
    with open("database/municipio.json", "r", encoding="utf-8") as f:
        geojson_municipios = jn.load(f)
except Exception as e:
    print(f"Erro ao carregar o arquivo JSON: {e}")

st.title("📊 DashMobv2 Acidentes Rodoviarios PRF - 2023")

st.sidebar.header("DashMob `version 2`")

df_estados = df2["uf"].unique()

list_estados = list(df_estados)

list_estados.insert(0, "TODOS")

estado = st.sidebar.selectbox("Estado", list_estados)

if(estado == "TODOS"):
    df_municipios = df2
else:
    df_municipios = df2[df2["uf"] == estado]

st.sidebar.divider()

st.sidebar.markdown("<h4 style='text-align: center;'>Desenvolvido por Rafael Cavalcante</h4>", unsafe_allow_html=True)

#Conjuntos Estaticos
ordem_dias_semana = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']

ordem_dias_semana2 = ['domingo',  'sábado', 'sexta-feira', 'quinta-feira', 'quarta-feira',  'terça-feira', 'segunda-feira']

nomes_meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

#Novas Colunas DateTime
df2["data"] = pd.to_datetime(df2["data_inversa"], format="%Y-%m-%d")

df2["mes"] = df2["data"].dt.month

df2["horario"] = pd.to_datetime(df2["horario"])

df2["hora"] = df2["horario"].dt.hour
    
#Gráfico 01 
df_acidentes_estado = df2["uf"].value_counts().reset_index(name="acidentes")

fig_acidentes_estado = px.choropleth_mapbox(df_acidentes_estado, geojson=geojson_estados, featureidkey="properties.UF_05", 
    locations="uf", color="acidentes", color_continuous_scale="Reds", range_color=(0, df_acidentes_estado["acidentes"].max()),
    mapbox_style="carto-positron", center={"lat": -14.235, "lon": -51.9253},  zoom=2.0, opacity=0.7,
    title="Distribuição Acidentes nos Estados Brasileiros")

#Gráfico 02
df_acidentes_municipio = df_municipios["municipio"].value_counts().reset_index(name="acidentes")

fig_acidentes_municipio = px.choropleth_mapbox(df_acidentes_municipio, geojson=geojson_municipios, featureidkey="properties.MICROREGIA", 
    locations="municipio",color="acidentes", color_continuous_scale="Reds", range_color=(0, df_acidentes_municipio["acidentes"].max()),
    mapbox_style="carto-positron", center={"lat": -14.235, "lon": -51.9253},  zoom=2.5, opacity=0.7,
    title=f"Distribuição Acidentes nos Municipios Brasileiros <br>{estado}")

col1, col2 = st.columns(2)

col1.plotly_chart(fig_acidentes_estado, use_container_width=True)

col2.plotly_chart(fig_acidentes_municipio, use_container_width=True)

#Gráfico 03
df_tipos_acidentes = df_municipios[df_municipios["causa_principal"] == "Sim"].value_counts("tipo_acidente").reset_index(name="acidentes")

fig_tipos_acidentes = px.treemap(df_tipos_acidentes, path=["tipo_acidente"], values="acidentes", color="acidentes", title=f"Tipos Causadores de Acidentes <br>{estado}")

#Gráfico 04
df_acidentes_genero = df_municipios["sexo"].value_counts().reset_index(name="acidentes")

fig_acidentes_genero = px.pie(df_acidentes_genero, names="sexo", values="acidentes", title=f"Distribuição de Acidentes por Gênero <br>{estado}")

col3, col4 = st.columns(2)

col3.plotly_chart(fig_tipos_acidentes, use_container_width=True)

col4.plotly_chart(fig_acidentes_genero, use_container_width=True)

#Gráfico 05
df_acidentes_municipio_top = df_municipios["municipio"].value_counts().sort_values()[-10:].reset_index(name="total")

fig_acidentes_municipio_top = px.bar(df_acidentes_municipio_top, x="total", y="municipio", color="total", title=f"Top 10 municipios com Indice de Acidentes no Estado <br>{estado}")

#Gráfico 06
df_acidentes_causa_top = df2[df2["municipio"].isin(df_acidentes_municipio_top["municipio"])]

df_acidentes_causa_top = df_acidentes_causa_top["causa_acidente"].value_counts().sort_values(ascending=True)[-10:].reset_index(name="total")

fig_acidentes_causa_top = px.histogram(df_acidentes_causa_top, x="total", y="causa_acidente", title=f"Top 10 Maiores Causas de Acidentes <br>{estado}")
fig_acidentes_causa_top.update_layout(xaxis_title='Número acidentes', yaxis_title='Causas')

col5, col6 = st.columns(2)

col5.plotly_chart(fig_acidentes_municipio_top, use_container_width=True)

col6.plotly_chart(fig_acidentes_causa_top, use_container_width=True)

#Gráfico 07
df_acidentes_veiculo = df2.groupby(['tipo_veiculo', 'dia_semana']).size().reset_index(name="quantidade")

df_acidentes_veiculo['dia_semana'] = pd.Categorical(df_acidentes_veiculo['dia_semana'], categories=ordem_dias_semana2, ordered=True)

df_acidentes_veiculo = df_acidentes_veiculo.sort_values(by=["dia_semana", "quantidade"], ascending=False).reset_index(drop=True)

fig_acidentes_veiculo = px.histogram(df_acidentes_veiculo, x="dia_semana", y="quantidade", color="tipo_veiculo", title=f"Quantidade de acidentes <br> Dia da semana x Tipo veiculo", text_auto=True, labels={'tipo_veiculo': 'Tipo de veiculo'})
fig_acidentes_veiculo.update_layout(xaxis_title= "Dia da semana", yaxis_title= "Quantidade")

#Gráfico 08
df_acidentes_mes = df2.groupby('mes')[['feridos_leves', 'feridos_graves', 'mortos']].sum().reset_index()

df_acidentes_mes["mes"] = [nomes_meses[mes - 1] for mes in df_acidentes_mes["mes"]]

df_acidentes_mes = pd.melt(df_acidentes_mes, id_vars="mes", var_name='tipo', value_name='quantidade')

fig_acidentes_mes = px.line(df_acidentes_mes, x="mes", y="quantidade", color="tipo", title="Quantidade de Acidentes por Mês")
fig_acidentes_mes.update_layout(xaxis_title= "Meses", yaxis_title= "Acidentes")

col7, col8 = st.columns(2)

col5.plotly_chart(fig_acidentes_veiculo, use_container_width=True)

col6.plotly_chart(fig_acidentes_mes, use_container_width=True)

#Grpafico 09
df_acidentes_mes = df2.groupby("mes")[["dia_semana"]].value_counts().reset_index(name="quantidade")

df_acidentes_mes['dia_semana'] = pd.Categorical(df_acidentes_mes['dia_semana'], categories=ordem_dias_semana, ordered=True)

df_acidentes_mes = df_acidentes_mes.sort_values(by=["mes", "dia_semana"]).reset_index(drop=True)

df_acidentes_mes["mes"] = [nomes_meses[mes - 1] for mes in df_acidentes_mes["mes"]]

fig_acidentes_mes = px.scatter(df_acidentes_mes, x="dia_semana", y="mes", color="mes", size="quantidade", title=f"Concentração de acidentes por mês/dia")
fig_acidentes_mes.update_layout(xaxis_title="Horario Acidentes", yaxis_title="Dias Semana", height=500)

#Gráfico 10
df_acidentes_hora = df2.groupby("dia_semana")[["hora"]].value_counts().reset_index(name="quantidade")

df_acidentes_hora['dia_semana'] = pd.Categorical(df_acidentes_hora['dia_semana'], categories=ordem_dias_semana, ordered=True)

df_acidentes_hora = df_acidentes_hora.sort_values(by=["dia_semana", "hora"]).reset_index(drop=True)

df_acidentes_hora['hora'] = pd.to_datetime(df_acidentes_hora['hora'], format='%H').dt.time

fig_acidentes_hora = px.scatter(df_acidentes_hora, x="hora", y="dia_semana", color="dia_semana", size="quantidade", title=f"Concentração de acidentes por dia/horario")
fig_acidentes_hora.update_layout(xaxis_title="Horario Acidentes", yaxis_title="Dias Semana", height=500)

col9, col10 = st.columns(2)

col9.plotly_chart(fig_acidentes_mes, use_container_width=True)

col10.plotly_chart(fig_acidentes_hora, use_container_width=True)

#Gráfico 11
df_acidentes_semana = df2["dia_semana"].value_counts().reset_index(name="total")

ordem_dias_semana = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']

df_acidentes_semana['dia_semana'] = pd.Categorical(df_acidentes_semana['dia_semana'], categories=ordem_dias_semana, ordered=True)

df_acidentes_semana = df_acidentes_semana.sort_values(by=["dia_semana"]).reset_index(drop=True)

fig_acidentes_semana = px.bar(df_acidentes_semana, x="dia_semana", y="total", color="dia_semana", labels={"dia_semana" : "Dias da Semana"})
fig_acidentes_semana.update_layout(xaxis_title="Dias da Semana", yaxis_title="Quantidade")

#Gráfico 12
df_feridos_mortos = df2.groupby('dia_semana')[['feridos_leves', 'feridos_graves', 'mortos']].sum().reset_index()

df_feridos_mortos['dia_semana'] = pd.Categorical(df_feridos_mortos['dia_semana'], categories=ordem_dias_semana, ordered=True)

df_feridos_mortos = df_feridos_mortos.sort_values(by=["dia_semana"]).reset_index(drop=True)

df_feridos_mortos = pd.melt(df_feridos_mortos, id_vars='dia_semana', var_name='tipo', value_name='quantidade')

fig_feridos_mortos = px.bar(df_feridos_mortos, x='dia_semana', y='quantidade', color='tipo',
             barmode='group', labels={'quantidade': 'Quantidade', 'tipo': 'Tipo'})

#Abas de Gráficos de Acidentes na Semana
tab1, tab2 = st.tabs(["Distribuição de Acidentes Na Semana", "Gravidade de Acidentes Na Semana"])

df_acidentes_semana["estatistica"] = df_acidentes_semana["total"].pct_change() * 100

estatistica_causa = df_feridos_mortos.groupby("tipo")["quantidade"].mean().reset_index(name="estatistica")

with tab1:
    st.subheader("Crescimento dos Acidentes na Semana")

    col_segunda, col_terca, col_quarta, col_quinta, col_sexta, col_sabado, col_domingo = st.columns([0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4])
    col_segunda.metric("Segunda-Feira", round(df_acidentes_semana["total"][0]), delta="0%", delta_color="off")
    col_terca.metric("Terça-Feira", round(df_acidentes_semana["total"][1]), f"{round(df_acidentes_semana['estatistica'][1])}%")
    col_quarta.metric("Quarta-Feira", round(df_acidentes_semana["total"][2]), f"{round(df_acidentes_semana['estatistica'][2])}%")
    col_quinta.metric("Quinta-Feira", round(df_acidentes_semana["total"][3]), f"{round(df_acidentes_semana['estatistica'][3])}%")
    col_sexta.metric("Sexta-Feira", round(df_acidentes_semana["total"][4]), f"{round(df_acidentes_semana['estatistica'][4])}%")
    col_sabado.metric("Sábado", round(df_acidentes_semana["total"][5]), f"{round(df_acidentes_semana['estatistica'][5])}%")
    col_domingo.metric("Domingo", round(df_acidentes_semana["total"][6]), f"{round(df_acidentes_semana['estatistica'][6])}%")

    st.plotly_chart(fig_acidentes_semana, use_container_width=True)
with tab2:
    st.subheader("Médias Geral das Gravidades de Acidentes")
    
    col_leves, col_graves, col_mortos = st.columns(3)
    col_leves.metric("Feridos Leves", round(estatistica_causa[estatistica_causa["tipo"] == "feridos_leves"]["estatistica"]))
    col_graves.metric("Feridos Graves", round(estatistica_causa[estatistica_causa["tipo"] == "feridos_graves"]["estatistica"]))
    col_mortos.metric("Mortos", round(estatistica_causa[estatistica_causa["tipo"] == "mortos"]["estatistica"]))
    
    st.plotly_chart(fig_feridos_mortos, use_container_width=True)