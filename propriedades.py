import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
import dash
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output, State
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import FluidsList
import pytz,os, time
import datetime

pio.renderers.default='browser'

engine = create_engine('sqlite://', echo=False)

app = Dash(__name__)


fluidos = FluidsList()
propriedades = ['Pressão (em Pa)', 'Temperatura (em K)', 'Densidade (em kg/m³)', 'Volume Espec. (em m³/kg)', 'Energia Interna (em kJ/kg)', 'Entalpia (em kJ/kg)', 'Entropia (em kJ/kg.K)', 'Título de Vapor']

###################### Criação do Layout ######################################
app.layout = html.Div(children = [
   
    ### Div para Lado Esquerdo (Propriedades)
    html.Div(children = [
        ## Div para Selecionar Fluido
        html.Div(children = [
            html.H3('Selecione o Fluido:'),
            dcc.Dropdown(fluidos, placeholder = 'Selecione',style = {'width': '75%'}, id = 'fluido', value = 'Water')
            ], style = {'margin': '10px', 'width': '100%'}),




##Div para Propriedade 1
        html.Div(children = [
            #Div Prop 1
            html.Div(children = [
                html.H4('Propriedade 1:'),
                dcc.Dropdown(propriedades, placeholder = 'Selecione',style = {'width': '95%'}, id = 'prop1', value = 'Pressão (em Pa)')
                ], style = {'width': '48%', 'marginLeft': '2%'}),
            #Div Valor Prop1
            html.Div(children = [
                html.H4('Valor Prop. 1:'),
                dcc.Input(id = 'v_prop1', type = 'number', min = 0, step = 0.1, placeholder = 'S.I', style = {'height': '25px', 'width': '75%'})
                ], style = {'width': '48%', 'marginLeft': '2%'})
            ], style = {'display': 'flex'}),
        ##Div para Propriedade 2
        html.Div(children = [
            #Div Prop 2
            html.Div(children = [
                html.H4('Propriedade 2:'),
                dcc.Dropdown(propriedades, placeholder = 'Selecione',style = {'width': '95%'}, id = 'prop2', value = 'Pressão (em Pa)')
                ], style = {'width': '48%', 'marginLeft': '2%'}),
            #Div Valor Prop2
            html.Div(children = [
                html.H4('Valor Prop. 2:'),
                dcc.Input(id = 'v_prop2', type = 'number', min = 0, step = 0.1, placeholder = 'S.I', style = {'height': '25px', 'width': '75%'})
                ], style = {'width': '48%', 'marginLeft': '2%'})
            ], style = {'display': 'flex', 'marginTop': '25px'}),
       
        ##Div para Calcular
        html.Div(children = [
            html.Button(' Calcular', id = 'btn-calcular', style = {'cursor': 'pointer', 'width': '33%', 'height': '35px', 'fontSize': '22px'})
            ], style = {'textAlign': 'center', 'marginTop': '35px', 'width': '98%'})
       
       
        ], style = {'border':'solid', 'width': '24%', 'marginRight': '1%'}),
   
    ### Div para Lado Centro (Resultados)
    html.Div(children = [
        html.H3('Resultados:'),
        html.H4(id = 'resultados')
        ], style = {'border':'solid', 'width': '24%', 'marginRight': '1%', 'height': '200px', 'paddingLeft': '0.5%'}),
   
    ### Div para Lado Direito (Gráficos)
    html.Div(children = [
        html.H3(id = 'historico')
        ], style = {'border':'solid', 'width': '48%'})
   
    ], style = {'display': 'flex'})


###################### Criação dos Callbacks ##################################

@app.callback(
    Output('resultados', 'children'),
    Output('historico', 'children'),
    Input('btn-calcular', 'n_clicks'),
    State('fluido', 'value'),
    State('prop1', 'value'),
    State('v_prop1', 'value'),
    State('prop2', 'value'),
    State('v_prop2', 'value'))

def calcula_propriedades(n_clicks, fluido, prop1, v_prop1, prop2, v_prop2):
    lista_prop = ['P', 'T', 'D', 'U', 'H', 'S', 'Q']
    lista_resultados = []
    for props in lista_prop:
        propriedade = round(float(CP.PropsSI(props,prop1,v_prop1,prop2,v_prop2,fluido)),1)
        texto = f' {props} = {propriedades}'
        lista_resultados.append(propriedade)
        return texto, ''


if __name__ == '__main__':
    app.run_server(debug=True)
