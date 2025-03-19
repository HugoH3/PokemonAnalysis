#! Importação de bibliotecas
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pd.read_csv('data/pokemon.csv')
df['Type'] = df['Type'].apply(lambda x: ' '.join(sorted(x.split(' '))))
tipos_options = df['Type'].value_counts().to_dict()

#! Variáveis dos temas do site, com modo claro e escuro
url_theme_claro = dbc.themes.MATERIA
url_theme_escuro = dbc.themes.SLATE

# LAYOUT da pagina web
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Pokémon Dashboard =)'))
    ]),
    dbc.Col(ThemeSwitchAIO(aio_id='theme', themes=[url_theme_claro, url_theme_escuro])),
    dbc.Row([
        dbc.Col(dcc.Dropdown( # uma aba para o usuario escolher filtros
            id='tipo_escolha',
            options=[{'label': tipo, 'value': tipo} for tipo in tipos_options.keys()],
            value=list(tipos_options.keys())[:2],
            multi=True
        ))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar_tipo')) #! cria o layout do gráfico
    ])
])

#! Funções
@app.callback(
    Output('bar_tipo', 'figure'),
    [Input('tipo_escolha', 'value')]
)
def update_bar_chart(selected_types):
    filtered_df = df[df['Type'].isin(selected_types)]
    fig = px.bar(filtered_df, x='Type', y='HP') # O callback retorna um grafico
    return fig

if __name__ == '__main__':
    app.run(debug=True, port='8051')