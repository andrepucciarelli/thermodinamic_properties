from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import sidebar




# =========  Layout  =========== #
app.layout = dbc.Container([
    dbc.Col([
        sidebar.layout
    ], md = 2),
    dbc.Col([
        dbc.Container(id = 'page_content', fluid = True, style = {'widht': '100%', 'height': '100%'})      
    ],md = 10, style = {'padding': '0%'})
], fluid=True,)


# ========= Callbacks ========== #
app.callback(
    Output('page_content', 'childre'),
    Input('url', 'pathname')
)
def renderizar_pagina(pathname):
    if pathname == '/' or '/inicio':
        return home.layout
    else:
        return html.H3('Página não existe')





if __name__ == '__main__':
    app.run(debug=True)