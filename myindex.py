from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from app import *
from components import sidebar,propriedades




# =========  Layout  =========== #
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Location(id = 'url'),
            sidebar.layout
            ], md = 3, style = {'padding': '0px'}),
        dbc.Col([
            dbc.Col([
            dbc.Container(id = 'page_content', fluid = True)
        ])],md = 9)
    ])
], fluid=True, style = {'padding': '15px'})


# ========= Callbacks ========== #
@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
)
def renderizar_pagina(pathname):
    if pathname == '/' or '/inicio':
        return propriedades.layout
    else:
        return html.Div([html.H1('Página não encontrada')])
        

if __name__ == '__main__':
    app.run(debug=True)
