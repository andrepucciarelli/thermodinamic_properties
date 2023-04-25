import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from CoolProp.CoolProp import PropsSI
from CoolProp.CoolProp import FluidsList
from dash import dash_table

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd


# ========= Layout ========= #
layout = html.Div([
    dbc.Row([
        dbc.Card([
            dbc.CardBody([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row([
                                                html.H4('Propriedade 1'),
                                                dcc.Dropdown([{'label':'Temperatura (°C)', 'value': 'T'},{'label':'Pressão (kPa)', 'value': 'P'},{'label':'Volume Esp.', 'value': 'V'},{'label':'Energ. Interna', 'value': 'U'},{'label':'Entalpia', 'value': 'H'},{'label':'Entropia', 'value': 'S'},{'label':'Título', 'value': 'Q'}], id = 'propriedade1', style = {'font-size':'20px'})
                                            ])
                                        ], md = 6),
                                        dbc.Col([
                                            dbc.Row([
                                                html.H4('Valor Prop. 1'),
                                                dbc.Input(id = 'valor_prop1',type = 'number', step = 0.01, style = {'font-size':'15px'})
                                            ])
                                        ], md = 6)
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row([
                                                html.H4('Propriedade 2'),
                                                dcc.Dropdown([{'label':'Temperatura (°C)', 'value': 'T'},{'label':'Pressão (kPa)', 'value': 'P'},{'label':'Volume Esp.', 'value': 'V'},{'label':'Energ. Interna', 'value': 'U'},{'label':'Entalpia', 'value': 'H'},{'label':'Entropia', 'value': 'S'},{'label':'Título', 'value': 'Q'}], id = 'propriedade2', style = {'font-size':'20px'})
                                            ])
                                        ], md = 6),
                                        dbc.Col([
                                            dbc.Row([
                                                html.H4('Valor Prop. 2'),
                                                dbc.Input(id = 'valor_prop2',type = 'number', step = 0.01, style = {'font-size':'15px'})
                                            ])
                                        ], md = 6)
                                    ], style = {'marginTop': '45px'}),
                                    dbc.Row([
                                    dbc.Col([
                                            html.H4('Fluido:'),
                                            dcc.Dropdown(FluidsList(), value = 'water',id = 'fluidos', style = {'font-size':'20px'})
                                    ], md = 6),
                                    dbc.Col([
                                            html.H4(id = 'mensagem')
                                    ], md = 6) 
                                    ], style = {'marginTop': '45px'}),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button('Calcular', id = 'botao_calcular', style = {'color': 'dark', 'width': '40%', 'font-size':'25px'})
                                        ], md = 12, style = {'margin': 'auto', 'textAlign': 'center'})
                                    ], style = {'marginTop': '45px'})  
                                ])
                            ], style = {'paddingRight': '10px'})
                        ], md = 6),
                        dbc.Col([
                            html.Div(id = 'respostas') 
                        ], md = 6)
                    ])
                ], md = 12)
            ])   
        ], style = {'width': '90%'})      
    ]),
    dbc.Row([
        html.Div(id = 'tabela')
    ])
    
])



# =========  Callbacks  =========== #
@app.callback(
    Output('respostas', 'children'),
    Output('tabela', 'children'),
    Input('botao_calcular', 'n_clicks'),
    State('propriedade1', 'value'),
    State('valor_prop1', 'value'),
    State('propriedade2', 'value'),
    State('valor_prop2', 'value'),
    State('fluidos', 'value')
)
def calcular_propriedade(n,prop1,v_prop1,prop2,v_prop2,fluido):
    props_zero = []
    tabela = []
    df_props = pd.DataFrame(props_zero, columns = ['T', 'P', 'D', 'V', 'U', 'H', 'S', 'Q', 'Est.'])

    if n:

        if prop1 == 'T':
            v_prop1 = v_prop1 + 273.15
        elif prop2 == 'T':
            v_prop2 = v_prop2 + 273.15
        elif prop1 == 'P':
            v_prop1 = v_prop1*1000
        elif prop2 == 'P':
            v_prop2 = v_prop2*1000
        else:
            v_prop1 = v_prop1
            v_prop2 = v_prop2

        # Calcular as propriedades
        T = round(PropsSI('T', prop1, v_prop1, prop2,v_prop2, fluido),2)
        P = round(PropsSI('P', prop1, v_prop1, prop2,v_prop2, fluido),3)
        D = round(PropsSI('D', prop1, v_prop1, prop2,v_prop2, fluido),3)
        V = round(1/D,4) 
        U = round(PropsSI('U', prop1, v_prop1, prop2,v_prop2, fluido)/1000,3)
        H = round(PropsSI('H', prop1, v_prop1, prop2,v_prop2, fluido)/1000,3)
        S = round(PropsSI('S', prop1, v_prop1, prop2,v_prop2, fluido)/1000,3)
        Q = round(PropsSI('Q', prop1, v_prop1, prop2,v_prop2, fluido),3)
        estado = PropsSI('Phase', prop1, v_prop1, prop2,v_prop2, fluido)
        if estado == 5:
            E = 'Vapor Superaquecido'
        elif estado == 0:
            E = 'Líquido Comprimido'
        else:
            E = 'Líquido + Vapor'
        
        df_props.loc[df_props.shape[0]] = [T,P,D,V,U,H,S,Q,E]
        tabela = dash_table.DataTable(df_props.to_dict('records'), [{"name": i, "id": i} for i in df_props.columns])
        
        return dbc.Card([
            dbc.CardBody([
                html.Div([html.P(f'T = {T} K ou {round(T-273.15,2)} °C'),
                                html.P(f'P = {P} kPa'),
                                html.P(f'V = {V} m³/kg'),
                                html.P(f'D = {D} kg/m³'),
                                html.P(f'U = {U} kJ/kg'),
                                html.P(f'H = {H} kJ/kg'),
                                html.P(f'S = {S} kJ/kg.K'),
                                html.P(f'x = {Q}'),
                                html.P(f'Estado = {E}')], style = {'fontSize': '20px'})
            ])
        ]), tabela               
