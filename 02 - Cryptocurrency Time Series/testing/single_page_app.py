from dash import Dash, html, callback, Output, Input, dcc
import pandas as pd
import pathlib
import os
import plotly.express as px
import plotly.graph_objs as go

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

# Initializing app
app = Dash(__name__)

# App layout
app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  html.Div(id='page-content'),
])

# Define as páginas
page_1_layout = html.Div([
  html.H1("[Time Series] Crypto Currency - Page 1"),

  html.Div([
    "Choose Crypto",
    dcc.Dropdown(options=dropdown_options, value="BTC", id="crypto-dropdown")
  ]),
  html.Div([
    "Choose a column",
    dcc.Checklist(options=column_options, value=["adjclose"], id="column-checklist")
  ]),

  dcc.Graph(figure=px.line(data["BTC"], x="timestamp", y="adjclose"), id="crypto-graph")
])

page_2_layout = html.Div([
  html.H1("[Time Series] Crypto Currency - Page 2"),

  html.Div([
    "Choose Crypto",
    dcc.Dropdown(options=dropdown_options, value="ETH", id="crypto-dropdown")
  ]),
  html.Div([
    "Choose a column",
    dcc.Checklist(options=column_options, value=["open"], id="column-checklist")
  ]),

  dcc.Graph(figure=px.line(data["ETH"], x="timestamp", y="open"), id="crypto-graph")
])

# Callback to refresh app content
@app.callback(
  Output('page-content', 'children'),
  Input('url', 'pathname')
)
def display_page(pathname):
  if pathname == '/page-2':
    return page_2_layout
  else:
    return page_1_layout

# Controls and callbacks
@app.callback(
  Output("crypto-graph", "figure"),
  Input("crypto-dropdown", "value"),
  Input("column-checklist", "value")
)
def update_graph(crypto_chosen, columns_chosen):
  fig = px.line()
  for column in columns_chosen:
      fig.add_trace(go.Scatter(x=data[crypto_chosen]["timestamp"], y=data[crypto_chosen][column], name=column))
  return fig

# Run app
if __name__ == "__main__":
  app.run_server(debug=True)
