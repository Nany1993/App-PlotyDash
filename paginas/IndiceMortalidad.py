# ------------------------------------------------------------------
# Archivo: paginas/indice_mortalidad.py
# Descripción: Layout y callbacks para mostrar las 10 ciudades
#              con menor número de muertes en un gráfico circular.
# ------------------------------------------------------------------
import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output

# Ruta al CSV procesado
# Debe contener columnas: CIUDAD, SEXO, MES, Muertes
DATA_CSV = 'ArchivosProcesados/MuertesPorMunicipio.csv'

# Carga de datos
df = pd.read_csv(DATA_CSV, sep=';', encoding='utf-8-sig')
# Asegurar tipos
df['MES'] = df['MES'].astype(int)
df['Muertes'] = df['Muertes'].astype(int)
# Mapear MES numérico a nombre
mes_map = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
           7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
df['mes_nombre'] = df['MES'].map(mes_map)

# Opciones de filtros
o_months = list(mes_map.values())
sexos = sorted(df['SEXO'].unique())


def layout_indice_mortalidad():
    """
    Layout para el módulo Indice de Mortalidad.
    Gráfico circular de las 10 ciudades con menor muertes.
    """
    # Controles
    controls = html.Div([
        # Filtro Mes
        html.Div([
            html.Label('Mes:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-mes-indice',
                options=[{'label': m, 'value': m} for m in o_months],
                placeholder='Todos', clearable=True,
                style={'width':'160px','backgroundColor':'fuchsia','color':'black','fontWeight':'bold'}
            )
        ], style={'marginRight':'20px'}),
        # Filtro Sexo
        html.Div([
            html.Label('Sexo:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-sexo-indice',
                options=[{'label': s, 'value': s} for s in sexos],
                placeholder='Todos', clearable=True,
                style={'width':'140px','backgroundColor':'fuchsia','color':'black','fontWeight':'bold'}
            )
        ], style={'marginRight':'auto'}),
        # Botón Volver
        html.Div(
            dcc.Link(
                html.Button('Volver', style={
                    'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
                    'border':'none','borderRadius':'5px','fontSize':'14px','cursor':'pointer'
                }), href='/ciudades-mas-violentas'
            ), style={'marginRight':'10px','alignSelf':'center'}
        ),
        # Botón Siguiente
        html.Div(
            dcc.Link(
                html.Button('Siguiente', style={
                    'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
                    'border':'none','borderRadius':'5px','fontSize':'14px','cursor':'pointer'
                }), href='/tabla-causas-muertes'
            ), style={'alignSelf':'center'}
        )
    ], style={
        'display':'flex','alignItems':'center','padding':'20px','backgroundColor':'black'
    })

    title = html.H2(
        'TOP 10 Ciudades con Menor Mortalidad',
        style={'textAlign':'center','color':'fuchsia','fontSize':'32px','margin':'20px 0'}
    )

    graph = dcc.Graph(id='grafico-indice', style={'backgroundColor':'black','height':'65vh'})

    return html.Div([controls, title, graph], style={'backgroundColor':'black','minHeight':'100vh'})


def register_callbacks_indice_mortalidad(app):
    @app.callback(
        Output('grafico-indice', 'figure'),
        Input('filtro-mes-indice', 'value'),
        Input('filtro-sexo-indice', 'value')
    )
    def update_indice(mes_sel, sexo_sel):
        df_f = df.copy()
        if mes_sel:
            df_f = df_f[df_f['mes_nombre'] == mes_sel]
        if sexo_sel:
            df_f = df_f[df_f['SEXO'] == sexo_sel]

        # Agrupar por ciudad y sumar muertes
        df_grp = df_f.groupby('MUNICIPIO', as_index=False).agg({'Muertes': 'sum'})
        # Tomar las 10 ciudades con menos muertes
        df_bot = df_grp.nsmallest(10, 'Muertes')

                # Gráfico circular
        fig = px.pie(
            df_bot,
            values='Muertes', names='MUNICIPIO',
            title='Ciudades con Menor Número de Muertes en el año 2019 para Colombia',
            color_discrete_sequence=['green','yellow','red']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label',
                          marker=dict(line=dict(color='white', width=1)))
        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black', font_color='white',
            title_font_color='fuchsia', title_font_size=28,
            margin={'r':0,'t':50,'l':0,'b':0}
        )
        return fig
