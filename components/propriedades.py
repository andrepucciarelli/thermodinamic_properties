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


props_zero = []
df_props = pd.DataFrame(props_zero, columns = ['Fluido','T (°C)', 'P (Pa)', 'D (kg/m³)', 'V (m³/kg)', 'U (kJ/kg)', 'H (kJ/kg)', 'S (kJ/kg.K)', 'Q', 'Estado'])


# ========= Layout ========= #
layout = html.Div([
    dcc.Store(id = 'dados', data = df_props.to_dict()),
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
                                                html.H4('Propriedade 1:'),
                                                dcc.Dropdown([{'label':'Temperatura (°C)', 'value': 'T'},{'label':'Pressão (Pa)', 'value': 'P'},{'label':'Volume Específico', 'value': 'V'},{'label':'Energia Interna', 'value': 'U'},{'label':'Entalpia', 'value': 'H'},{'label':'Entropia', 'value': 'S'},{'label':'Título', 'value': 'Q'}], id = 'propriedade1', style = {'font-size':'20px'})
                                            ])
                                        ], md = 6, sm = 12),
                                        dbc.Col([
                                            dbc.Row([
                                                html.H4('Valor Propriedade 1:'),
                                                dbc.Input(id = 'valor_prop1', placeholder = 'Valores divididos por ponto (.)',type = 'number', step = 0.01, style = {'font-size':'15px'})
                                            ])
                                        ], md = 6, sm = 12)
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row([
                                                html.H4('Propriedade 2:'),
                                                dcc.Dropdown([{'label':'Temperatura (°C)', 'value': 'T'},{'label':'Pressão (Pa)', 'value': 'P'},{'label':'Volume Específico', 'value': 'V'},{'label':'Energia Interna', 'value': 'U'},{'label':'Entalpia', 'value': 'H'},{'label':'Entropia', 'value': 'S'},{'label':'Título', 'value': 'Q'}], id = 'propriedade2', style = {'font-size':'20px'})
                                            ])
                                        ], md = 6, sm = 12),
                                        dbc.Col([
                                            dbc.Row([
                                                html.H4('Valor Propriedade 2:'),
                                                dbc.Input(id = 'valor_prop2',placeholder = 'Valores divididos por ponto (.)', type = 'number', step = 0.01, style = {'font-size':'15px'})
                                            ])
                                        ], md = 6, sm = 12)
                                    ], style = {'marginTop': '45px'}),
                                    dbc.Row([
                                    dbc.Col([
                                            html.H4('Fluido:'),
                                            dcc.Dropdown(FluidsList(), value = 'water',id = 'fluidos', style = {'font-size':'20px'})
                                    ], md = 6, sm = 12),
                                    dbc.Col([
                                            html.H4(id = 'mensagem')
                                    ], md = 6) 
                                    ], style = {'marginTop': '45px'}),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button('Calcular', id = 'botao_calcular', style = {'color': 'dark', 'width': '40%', 'font-size':'25px', 'marginBottom': '20px'})
                                        ], md = 12, style = {'margin': 'auto', 'textAlign': 'center'})
                                    ], style = {'marginTop': '45px'})  
                                ])
                            ], style = {'paddingRight': '10px'})
                        ], md = 6, sm = 12),
                        dbc.Col([
                            html.Div(id = 'respostas') 
                        ], md = 6, sm = 12)
                    ])
                ], md = 12)
            ])   
        ], style = {'width': '90%'})      
    ]),
    dbc.Row([
        html.H3('Histórico:'),
        html.Div(id = 'tabela')
    ], style = {'marginTop': '40px'})
    
])



# =========  Callbacks  =========== #
@app.callback(
    Output('respostas', 'children'),
    Output('tabela', 'children'),
    Output('dados','data'),
    Input('botao_calcular', 'n_clicks'),
    Input('dados','data'),
    State('propriedade1', 'value'),
    State('valor_prop1', 'value'),
    State('propriedade2', 'value'),
    State('valor_prop2', 'value'),
    State('fluidos', 'value')
)
def calcular_propriedade(n,dados,prop1,v_prop1,prop2,v_prop2,fluido):
    
    tabela = ['Histórico:']

    df =  pd.DataFrame(dados)

    if n:

        try:
            if prop1 == 'T':
                v_prop1 = v_prop1 + 273.15
            elif prop2 == 'T':
                v_prop2 = v_prop2 + 273.15
            elif prop1 == 'P':
                v_prop1 = v_prop1
            elif prop2 == 'P':
                v_prop2 = v_prop2
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
            
            df.loc[df.shape[0]] = [fluido, T-273.15,P,D,V,U,H,S,Q,E]
            tabela = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], style_cell={'text-align': 'center'})
            
            return dbc.Card([
                dbc.CardBody([
                    html.Div([html.P(f'T = {T} K ou {round(T-273.15,2)} °C', style={"font-weight": "bold"}),
                                    html.P(f'P = {P} Pa', style={"font-weight": "bold"}),
                                    html.P(f'V = {V} m³/kg', style={"font-weight": "bold"}),
                                    html.P(f'D = {D} kg/m³', style={"font-weight": "bold"}),
                                    html.P(f'U = {U} kJ/kg', style={"font-weight": "bold"}),
                                    html.P(f'H = {H} kJ/kg', style={"font-weight": "bold"}),
                                    html.P(f'S = {S} kJ/kg.K', style={"font-weight": "bold"}),
                                    html.P(f'x = {Q}', style={"font-weight": "bold"}),
                                    html.P(f'Estado = {E}', style={"font-weight": "bold"})], style = {'fontSize': '20px', 'paddingLeft': '40px'})
                ])
            ]), tabela, df.to_dict()

        except:
            df.loc[df.shape[0]] = [fluido,'-','-','-','-','-','-','-','-','-']
            tabela = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
            return html.H4(f'Valores inválidos para o {fluido}', style = {'color': 'red', 'textAlign': 'center', 'fontSize': '40px', 'marginTop': '40px'}),tabela, df.to_dict()               
