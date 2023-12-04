#Impotações Nescessarias
import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, Input, Output

#Importando os dados para o dataframe
dataset = pd.read_csv("acidentes2023_todas_causas_tipos.csv")

#Trabalhando os dados grafico 1
dataset_genero = dataset["sexo"].value_counts()

sexo_column = dataset_genero.values

count_column = dataset_genero.index.tolist()

#Trabalhando os dados do grafico 2
dataset_causa = dataset["causa_acidente"].value_counts().sort_values(ascending=True)[0:9]

causa_column = dataset_causa.values

count2_column = dataset_causa.index.tolist()

#
semana_column = dataset["dia_semana"]

horario_column = horarios_ordenados = sorted(dataset["horario"], key=lambda x: tuple(map(int, x.split(':'))))

#
dataset_uf = dataset["uf"].unique()

#dataset_periodo_acidentes = dataset.sort_values(by=["horario"])

dataset_periodo_acidentes  = dataset.groupby("dia_semana")["horario"].value_counts().sort_values(ascending=True)


#Gerando os graficos
fig = px.pie(dataset_genero, values=sexo_column, names=count_column, title="Distribuição de acidentes por gênero")

fig2 = px.histogram(dataset_causa, x=causa_column, y=count2_column, title = "Top 10 maiores causas de acidentes")

fig2.update_layout(xaxis_title='Número acidentes', yaxis_title='Causas')

fig3 = px.scatter(x=horario_column, y=semana_column)

#Construindo a interface grafica do DashBoard
app = Dash(__name__)

app.layout = html.Div(
   children=[
       html.Div([
            html.H1(children="DashBoard Academico")],
            style={"display" : "block", "width": "100%", "text-align": "center"},
        ),
        
        html.Div([
            dcc.Graph(id="grafico_acidentes_genero", figure=fig)],
            style={"display" : "inline-block", "width": "40%"},
        ),
        
        html.Div([
            dcc.Graph(id="grafico_acidentes_causa", figure=fig2)],
            style={"display" : "inline-block", "width": "60%"},
        ),
        
        html.Div([
            dcc.Graph(id="grafico_data_acidentes", figure=fig3)],
            style={"display" : "inline-block", "width": "100%"},
        ),
        
        html.Div([
            dcc.Dropdown(id="dropdown_uf", options=dataset_uf, value="RN")]
        ),
        
        html.Div([            
            dcc.Graph(id="grafico_acidentes_municipio")],
            style={"display" : "inline-block", "width": "50%"},
        ),
        
        html.Div([            
            dcc.Graph(id="grafico_tipo_acidentes_municipio")],
            style={"display" : "inline-block", "width": "50%"},
        ),
    ],
)

@app.callback(
    [Output("grafico_acidentes_municipio", "figure"), Output("grafico_tipo_acidentes_municipio", "figure")],
    Input("dropdown_uf", "value")
)
def update_municipio(value):   
        dataset_municipio = dataset.loc[dataset["uf"].isin([value])]
        
        dataset_numero_acidente = dataset_municipio["municipio"].value_counts().sort_values(ascending=False)
        
        dataset_tipo_acidente = dataset_municipio["tipo_acidente"].value_counts().sort_values(ascending=True)
                
        fig = px.bar(x=dataset_numero_acidente.values, y=dataset_numero_acidente.index.tolist(), color=dataset_numero_acidente.values, title="Numero de acidentes por municipio", height=500)

        fig2 =px.bar(x=dataset_tipo_acidente.values, y=dataset_tipo_acidente.index.tolist(), color=dataset_tipo_acidente.values, title="Tipos de acidentes por municipio", text_auto='.2s', height=500)

        return fig, fig2

if __name__ == "__main__":
    app.run_server(debug=True)

# Comentário de multiplas linhas  """ ... """