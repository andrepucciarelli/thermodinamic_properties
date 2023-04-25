import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import pandas as pd


# ========= Layout ========= #
layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            dbc.Col([
                dbc.Row([
                    html.Img(src = '/assets/logo.png', style = {'width': '60%', 'display': 'block', 'margin': 'auto'})
                ])
            ], style = {'marginBottom': '30px'}),
            html.Hr(),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Button([html.I(className='fa fa-calculator'), ' \t Calculadora de Propriedades'], href = '/inicio', active=True, style = {'display': 'block', 'margin': 'auto', 'font-size': '25px', 'margin-bottom': '10px', 'width':'90%'})
                    ])
                ])
            ], style = {'marginTop': '30px'})


            
        ])
    ], style = {'height': '90vh'})               
], fluid = True)





# =========  Callbacks  =========== #
# Pop-up receita
