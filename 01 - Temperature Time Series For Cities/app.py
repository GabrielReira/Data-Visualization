from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import data_treat


# Importando os dados
df = data_treat.load_data()
df_cities = data_treat.get_cities(df)
df_options = data_treat.get_options(df)

# Inicializando o app
app = Dash(__name__)

app.layout = html.Div([
  html.Div(className='row', children=[
    html.H1(children='Temperatura de Cidades Brasileiras'),

    dcc.Checklist(options=df_cities,value=["salvador"], inline=True, id='city-checklist')]),
    html.Div(className='row', children=[
      dcc.Dropdown(options=df_options, value="JAN",id='month-dropdown')
    ]),
    dcc.Input(id='outlier-multiplier', type='number', value=1.5),
    dcc.RadioItems(
      options=[
        {'label': 'nada', 'value': 'nada'},
        {'label': 'último valor válido', 'value': 'fillna'},
        {'label': 'interpolacao linear', 'value': 'interpolacao'}
      ], 
      value="nada",
      id='method-radio'
    ),

    dcc.Graph(figure=px.line(df["salvador"], x='YEAR', y='JAN'), id='graph'),
    dcc.Graph(figure=px.line(df["salvador"], x='YEAR', y='JAN'), id='box-plot')
])

# Gráfico de linhas
@callback(
  Output('graph', 'figure'),
  Input('city-checklist', 'value'),
  Input('month-dropdown', 'value'),
  Input('outlier-multiplier', 'value'),
  Input('method-radio', 'value')
)
def update_graph(cities_chosen, month_chosen, multiplier, filling_method):
  data = data_treat.load_data()
  data1 = data_treat.set_outlier_multiplier(data, multiplier)
  data1 = data_treat.set_fill(data, filling_method)

  fig = px.line()
  for city in cities_chosen:
    fig.add_trace(go.Scatter(x=data1[city]['YEAR'], y=data1[city][month_chosen], name=city))

  return fig

# Gráfico Box Plot
@callback(
  Output('box-plot', 'figure'),
  Input('city-checklist', 'value')
)
def update_box_plot(cities_chosen):
  data = []
  for city in cities_chosen:
    data.append(go.Box(y=df[city][df[city].columns[1:]], name=city))  
  fig = go.Figure(data)

  return fig

if __name__ == '__main__':
  app.run(debug=True)
