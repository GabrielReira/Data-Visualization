import dash
from dash import Dash, html, dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

app.layout = html.Div([
  html.H1('Cryptocurrency Over Years'),

  html.Div([
    html.Div([
      dcc.Link('Home Page', href='/'),
      html.Span(' | '),
      dcc.Link('Compare Cryptos', href='/compare')
    ])
  ]),
  html.Hr(),
  
  dash.page_container
])

if __name__ == '__main__':
  app.run(debug=True)
