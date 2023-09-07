from dash import html, callback, Output, Input, dcc, register_page
import pandas as pd
import pathlib
import os
import plotly.express as px
import plotly.graph_objs as go


# Registering page
register_page(__name__, path='/compare')

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
  html.H3("Cryptocurrencies Comparison"),

  html.Div([
    html.Div(className='six columns', children=[
      "Choose Crypto:",
      dcc.Dropdown(options=dropdown_options, value="BTC", id="crypto-dropdown-left"),

      dcc.Graph(figure=go.Figure(go.Candlestick(
        x=data["BTC"]["timestamp"], 
        open=data["BTC"]["open"],
        high=data["BTC"]["high"],
        low=data["BTC"]["low"],
        close=data["BTC"]["close"]
      )), id="candlestick-graph-left"),

      "Choose column:",
      dcc.Checklist(options=column_options, value=["adjclose"], id="column-checklist-left"),

      dcc.Graph(figure=px.line(data["BTC"], x="timestamp", y="adjclose"), id="crypto-graph-left"),
      dcc.Graph(figure=px.box(data["BTC"], y="adjclose", points="all"), id="boxplot-graph-left")
    ]),

    html.Div(className='six columns', children=[
      "Choose Crypto:",
      dcc.Dropdown(options=dropdown_options, value="ETH", id="crypto-dropdown-right"),

      dcc.Graph(figure=go.Figure(go.Candlestick(
        x=data["ETH"]["timestamp"], 
        open=data["ETH"]["open"],
        high=data["ETH"]["high"],
        low=data["ETH"]["low"],
        close=data["ETH"]["close"]
      )), id="candlestick-graph-right"),

      "Choose column:",
      dcc.Checklist(options=column_options, value=["adjclose"], id="column-checklist-right"),

      dcc.Graph(figure=px.line(data["ETH"], x="timestamp", y="adjclose"), id="crypto-graph-right"),
      dcc.Graph(figure=px.box(data["ETH"], y="adjclose", points="all"), id="boxplot-graph-right")
    ])
  ])
])

# Controls and callbacks
columns = ['left', 'right']
for side in columns:
  @callback(
    Output(f"candlestick-graph-{side}", "figure"),
    Output(f"crypto-graph-{side}", "figure"),
    Output(f"boxplot-graph-{side}", "figure"),
    Input(f"crypto-dropdown-{side}", "value"),
    Input(f"column-checklist-{side}", "value")
  )
  def update_graph(crypto_chosen, columns_chosen):
    fig_candlestick = go.Figure(go.Candlestick(
      x=data[crypto_chosen]["timestamp"], 
      open=data[crypto_chosen]["open"],
      high=data[crypto_chosen]["high"],
      low=data[crypto_chosen]["low"],
      close=data[crypto_chosen]["close"]
    ))

    fig_line = px.line()
    for column in columns_chosen:
      fig_line.add_trace(go.Scatter(x=data[crypto_chosen]["timestamp"], y=data[crypto_chosen][column], name=column))

    fig_boxplot = px.box(data[crypto_chosen], y=columns_chosen, points="all")

    return fig_candlestick, fig_line, fig_boxplot
