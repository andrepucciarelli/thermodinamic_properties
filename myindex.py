from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from app import *
from components import sidebar
from components import propriedades




# =========  Layout  =========== #
app.layout = dbc.Container([
    dbc.Col([
        sidebar.layout
    ], md = 3),
    dbc.Col([
        dbc.Container(id = 'page_content', fluid = True, style = {'widht': '100%', 'height': '100%'})      
    ],md = 9, style = {'padding': '0%'})
], fluid=True,)


# ========= Callbacks ========== #
app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
)
def renderizar_pagina(pathname):
    if pathname == '/' or '/inicio':
        return propriedades.layout
    else:
        dbc.Container([
            html.H1('Página não encontrada')
        ])





if __name__ == '__main__':
    app.run(debug=True)