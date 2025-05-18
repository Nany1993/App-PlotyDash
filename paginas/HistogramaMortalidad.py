# ------------------------------------------------------------------
# Archivo: paginas/HistogramaMortalidad.py
# Descripción: Distribución de muertes por rangos de edad quinquenales.
# ------------------------------------------------------------------
import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output

# Ruta al CSV de edades
# Debe contener columnas: GRUPO_EDAD1 (numérico), SEXO, MES
DATA_CSV = 'ArchivosProcesados/MuertesPorEdad.csv'

df = pd.read_csv(DATA_CSV, sep=';', encoding='utf-8-sig')
# Tipos
df['GRUPO_EDAD1'] = pd.to_numeric(df['GRUPO_EDAD1'], errors='coerce').fillna(0).astype(int)
df['MES'] = pd.to_numeric(df['MES'], errors='coerce').fillna(0).astype(int)

# Mapear MES numérico a nombre
dict_mes = {
    1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
    7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'
}
df['mes_nombre'] = df['MES'].map(dict_mes)

# Mapear grupo edad a rango quinquenal
grupo_map = {i: f"{(i-5)*5}-{(i-5)*5+4}" for i in range(5,22)}
grupo_map[22] = '85+'
df['edad_rango'] = df['GRUPO_EDAD1'].map(grupo_map)

# Filtros
o_months = list(dict_mes.values())
sexos = sorted(df['SEXO'].unique())

# Orden de categorías de rango de edad
e_order = list(grupo_map.values())


def layout_histograma_mortalidad():
    """
    Layout para distribución de muertes por rangos de edad.
    Incluye filtros de Mes y Sexo, más navegación.
    """
    controls = html.Div([
        html.Div([
            html.Label('Mes:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-mes-histo',
                options=[{'label': m, 'value': m} for m in o_months],
                placeholder='Todos', clearable=True,
                style={'width':'160px','backgroundColor':'fuchsia','color':'black','fontWeight':'bold'}
            )
        ], style={'marginRight':'20px'}),

        html.Div([
            html.Label('Sexo:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-sexo-histo',
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
                }), href='/tabla-causas-muertes'
            ),
            style={'marginRight':'10px','alignSelf':'center'}
        ),
        # Botón Siguiente
        html.Div(
            dcc.Link(
                html.Button('Siguiente', style={
                    'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
                    'border':'none','borderRadius':'5px','fontSize':'14px','cursor':'pointer'
                }), href='/muertes-por-sexo'
            ),
            style={'alignSelf':'center'}
        )
    ], style={'display':'flex','alignItems':'center','padding':'20px','backgroundColor':'black'})

    title = html.H2(
        'Distribución de Muertes por Rango de Edad',
        style={'textAlign':'center','color':'fuchsia','fontSize':'28px','margin':'20px 0'}
    )

    graph = dcc.Graph(id='grafico-histo', style={'backgroundColor':'black','height':'70vh'})

    return html.Div([controls, title, graph], style={'backgroundColor':'black','minHeight':'100vh'})


def register_callbacks_histograma_mortalidad(app):
    """
    Registra callback para actualizar el histograma por rangos de edad.
    """
    @app.callback(
        Output('grafico-histo', 'figure'),
        Input('filtro-mes-histo', 'value'),
        Input('filtro-sexo-histo', 'value')
    )
    def update_histograma(mes_sel, sexo_sel):
        dff = df.copy()
        if mes_sel:
            dff = dff[dff['mes_nombre'] == mes_sel]
        if sexo_sel:
            dff = dff[dff['SEXO'] == sexo_sel]

        # Histograma por rango de edad
        fig = px.histogram(
            dff,
            x='edad_rango',
            category_orders={'edad_rango': e_order},
            color_discrete_sequence=['#f8e2fc']  # rosa menos intenso
,
            labels={'edad_rango':'Rango de Edad','count':'# Muertes'},
            title='Muertes por Rango de Edad (quinquenales)'
        )
        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',
            title_font_color='fuchsia',
            title_font_size=24,
            margin={'r':0,'t':50,'l':0,'b':0}
        )
        return fig
