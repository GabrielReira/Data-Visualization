from dash import html, callback, Output, Input, dcc, register_page
import pandas as pd
import pathlib
import os
import plotly.express as px
import plotly.graph_objs as go


# Registering page
register_page(__name__, path='/')

# Incorporating data
data_dir = pathlib.Path("data")
data = {}
dropdown_options = []
for file_name in os.listdir(data_dir):
  crypto_name = file_name.split("-")[0]
  dropdown_options.append(
    {"label": crypto_name, "value": crypto_name}
  )
  data[crypto_name] = pd.read_csv(os.path.join(data_dir, file_name))

column_options = []
for column in data["BTC"].columns[1:]:
  column_options.append(column)


# App layout
layout = html.Div([
  html.H3("[Time Series] Crypto Currency"),
  html.Div([
    "Choose Crypto(s):",
    dcc.Dropdown(options=dropdown_options, value=["BTC"], multi=True, id="crypto-dropdown")
  ]),
  html.Div([
    "Choose column:",
    dcc.Checklist(options=column_options, value=["adjclose"], id="column-checklist")
  ]),
  dcc.Graph(figure=px.line(data["BTC"], x="timestamp", y="adjclose"), id="crypto-graph")
])

# Controls and callbacks
@callback(
  Output("crypto-graph", "figure"),
  Input("crypto-dropdown", "value"),
  Input("column-checklist", "value")
)
def update_graph(crypto_chosen, columns_chosen):
  fig = px.line()

  for crypto in crypto_chosen:
    for column in columns_chosen:
      fig.add_trace(go.Scatter(
        x=data[crypto]["timestamp"], 
        y=data[crypto][column], 
        name=f'{crypto} - {column}'
      ))

  return fig
