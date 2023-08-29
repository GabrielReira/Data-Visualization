from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import data_treat
import copy


# Importando os dados
df = data_treat.load_data()
df_cities = data_treat.get_cities(df)
df_options = data_treat.get_options(df)

# Inicializando o app
app = Dash(__name__)

app.layout = html.Div(children=[
  html.H1("Temperatura de Capitais Brasileiras"),

  html.Div([
    "Selecione a(s) cidade(s):",
    dcc.Checklist(options=df_cities,value=["salvador"], inline=True, id='city-checklist')
  ]),
  html.Br(),
  html.Div(children=[
    "Selecione o período de interesse:",
    dcc.Dropdown(options=df_options, value="JAN", clearable=False,id='month-dropdown')
  ]),
  html.Br(),
  html.Div(children=[
    "Informe um multiplicador para o outlier: ",
    dcc.Input(id='outlier-multiplier', type='number', value=1.5)
  ]),
  html.Br(),
  html.Div(children=[
    "Escolha um método de preenchimento para os valores ausentes nos dados:",
    dcc.RadioItems(
      options=[
        {'label': 'nulo', 'value': 'nulo'},
        {'label': 'último valor válido', 'value': 'fillna'},
        {'label': 'interpolação linear', 'value': 'interpolacao'}
      ], 
      value="nulo",
      id='method-radio'
    )
  ]),

  dcc.Graph(figure=px.line(df["salvador"], x='YEAR', y='JAN'), id='graph'),
  dcc.Graph(figure=px.line(df["salvador"], x='YEAR', y='JAN'), id='box-plot'),
  dcc.Graph(figure=px.line(df["salvador"], x='YEAR', y='JAN'), id='histogram')
])

# Gráfico de linhas
@callback(
  Output('graph', 'figure'),
  Output('box-plot', 'figure'),
  Output('histogram', 'figure'),
  Input('city-checklist', 'value'),
  Input('month-dropdown', 'value'),
  Input('outlier-multiplier', 'value'),
  Input('method-radio', 'value')
)
def update_graphs(cities_chosen, month_chosen, multiplier, filling_method):
  # Foi necessário utilizar deepcopy pois a variável global "df" estava sendo alterada
  filtered_data = copy.deepcopy(df)
  filtered_data = data_treat.set_outlier_multiplier(filtered_data, multiplier)
  filtered_data = data_treat.set_fill(filtered_data, filling_method)

  fig_lines = px.line()
  box_plot_data = []
  histogram_data = []

  for city in cities_chosen:
    fig_lines.add_trace(go.Scatter(x=filtered_data[city]['YEAR'], y=filtered_data[city][month_chosen], name=city))
    box_plot_data.append(go.Box(y=filtered_data[city][filtered_data[city].columns[1:]], name=city))  
    histogram_data.append(go.Histogram(x=filtered_data[city][month_chosen], name=city))
  fig_box_plot = go.Figure(box_plot_data)
  fig_histogram = go.Figure(histogram_data)

  return fig_lines, fig_box_plot, fig_histogram


if __name__ == '__main__':
  app.run(debug=True)
