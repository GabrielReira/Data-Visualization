from dash import Dash, html, callback, Output, Input, dcc
import pandas as pd
import pathlib
import os
import dash_bootstrap_components as dbc
import plotly.express as px


# Incorporating data
data_dir = pathlib.Path("data")
data = {}
for file_name in os.listdir(data_dir):
  crypto_name = file_name.split("-")[0]
  data[crypto_name] = pd.read_csv(os.path.join(data_dir, file_name))

# Dropdown
dropdown_items = []
for file_name in os.listdir(data_dir):
  crypto = file_name.split("-")[0]
  item = dbc.DropdownMenuItem(crypto, id=f"dropdown-item-{crypto}")
  dropdown_items.append(item)


# Initilizing app
app = Dash(__name__)


# App layout
app.layout = dbc.Container([
  html.H1("[Time Series] Crypto Currency"),

  html.Div(
    [
      dbc.DropdownMenu(
        label="Choose Crypto",
        children=dropdown_items,
        id="crypto-dropdown",
        color="primary",
        className="m-1"
      )
    ],
    style={"display": "flex", "flexWrap": "wrap"}
  ),

  html.Div([
    dbc.Row([
      dcc.Graph(
        figure=px.line(data["BTC"], x="timestamp", y="adjclose"), 
        id="crypto-graph")
    ])
  ])
])

# # Controls and callbacks
# @callback(
#   Output("crypto-graph", "figure"),
#   Input("crypto-dropdown", "value")
# )


# Run app
if __name__ == "__main__":
  app.run()
