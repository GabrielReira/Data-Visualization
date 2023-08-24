from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import data_treat

# Importando os dados
df = data_treat.data
df_cities = data_treat.get_cities(df)
df_options = data_treat.get_options(df)

# Inicializando o app
app = Dash(__name__)

app.layout = html.Div([
  html.Div(className='row', children=[
  html.H1(children='Temperatura de Cidades Brasileiras'),

  dcc.RadioItems(options=df_cities,value="salvador", inline=True, id='city-radio')]),

  html.Div(className='row', children=[
    dcc.Dropdown(options=df_options, value="JAN",id='month-radio')
  ]),
  dcc.Graph(figure=px.line(df["salvador"], x='YEAR', y='JAN'), id='graph')
])

@callback(
  Output(component_id='graph', component_property='figure'),
  Input(component_id='city-radio', component_property='value'),
  Input(component_id='month-radio', component_property='value')
)

def update_graph(city_chosen, month_chosen):
  fig = px.line(df[city_chosen], x='YEAR', y=month_chosen)
  return fig

if __name__ == '__main__':
  app.run(debug=True)
