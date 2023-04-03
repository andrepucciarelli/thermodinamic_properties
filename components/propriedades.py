import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd


# ========= Layout ========= #
layout = dbc.Container([
    dbc.Col([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Col([
                            dbc.Row([
                                html.H4('Propriedade 1'),
                                dcc.Dropdown(['Temperatura', 'Pressão', 'Volume Esp.', 'Energia Interna', 'Entalpia', 'Entropia'])
                            ])
                        ], md = 6)
                    ])
                ])
            ])
        ])
    ], md = 6)
], fluid = True)





# =========  Callbacks  =========== #
# Pop-up receita