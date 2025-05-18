# ------------------------------------------------------------------
# Archivo: paginas/TablaCausasMuertes.py
# Descripción: Layout y callbacks para mostrar las 10 principales causas de muerte.
# ------------------------------------------------------------------
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output
from dash_table import DataTable

# Ruta al CSV de causas
# Estructura: COD_MUERTE;SEXO;MES;Muertes;MUNICIPIO;Descripcion de códigos mortalidad a cuatro caracteres
DATA_CSV = 'ArchivosProcesados/MuertesPorMunicipioTabla.csv'

df_c = pd.read_csv(DATA_CSV, sep=';', encoding='utf-8-sig')
# Mapear MES numérico a nombre
mes_map = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
           7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
df_c['MES'] = df_c['MES'].astype(int).map(mes_map)

# Opciones de filtros
o_months = list(mes_map.values())
sexos = sorted(df_c['SEXO'].unique())
municipios = sorted(df_c['MUNICIPIO'].dropna().unique())



def layout_tabla_causas():
    """
    Layout para la tabla de las 10 principales causas de muerte en Colombia.
    Permite filtrar por MES, SEXO y MUNICIPIO.
    """
    controls = html.Div([
        html.Div([
            html.Label('Mes:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-mes-causas',
                options=[{'label': m, 'value': m} for m in o_months],
                placeholder='Todos', clearable=True,
                style={'width':'150px','backgroundColor':'fuchsia','color':'black'}
            )
        ], style={'marginRight':'20px'}),

        html.Div([
            html.Label('Sexo:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-sexo-causas',
                options=[{'label': s, 'value': s} for s in sexos],
                placeholder='Todos', clearable=True,
                style={'width':'130px','backgroundColor':'fuchsia','color':'black'}
            )
        ], style={'marginRight':'20px'}),

        html.Div([
            html.Label('Municipio:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-municipio-causas',
                options=[{'label': m, 'value': m} for m in municipios],
                placeholder='Todos', clearable=True,
                style={'width':'180px','backgroundColor':'fuchsia','color':'black'}
            )
        ], style={'marginRight':'auto'})
    ], style={'display':'flex','padding':'20px','backgroundColor':'black'})

    title = html.H2(
        '10 Principales Causas de Muerte en Colombia',
        style={'textAlign':'center','color':'fuchsia','margin':'20px 0'}
    )

    table = DataTable(
        id='tabla-causas',
        columns=[
            {'name':'Código', 'id':'COD_MUERTE'},
            {'name':'Causa','id':'Descripcion'},
            {'name':'Casos','id':'Muertes'}
        ],
        style_table={'overflowX': 'auto','backgroundColor':'black'},
        style_header={'backgroundColor':'fuchsia','color':'white','fontWeight':'bold'},
        style_cell={'backgroundColor':'black','color':'white','textAlign':'left'}
    )

    nav = html.Div([
        dcc.Link(html.Button('Volver', style={
            'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
            'border':'none','borderRadius':'5px','cursor':'pointer'
        }), href='/indice-mortalidad'),
        html.Span(' '),
        dcc.Link(html.Button('Siguiente', style={
            'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
            'border':'none','borderRadius':'5px','cursor':'pointer'
        }), href='/histograma-mortalidad')
    ], style={'textAlign':'center','padding':'20px','backgroundColor':'black'})

    return html.Div([controls, title, table, nav], style={'backgroundColor':'black','minHeight':'100vh'})


def register_callbacks_tabla_causas(app):
    """
    Registra callback para actualizar la tabla de causas.
    """
    @app.callback(
        Output('tabla-causas','data'),
        Input('filtro-mes-causas','value'),
        Input('filtro-sexo-causas','value'),
        Input('filtro-municipio-causas','value')
    )
    def update_tabla(mes_sel, sexo_sel, muni_sel):
        dff = df_c.copy()
        if mes_sel:
            dff = dff[dff['MES']==mes_sel]
        if sexo_sel:
            dff = dff[dff['SEXO']==sexo_sel]
        if muni_sel:
            dff = dff[dff['MUNICIPIO']==muni_sel]

        # Agrupar por causa
        df_grp = dff.groupby(['COD_MUERTE','Descripcion  de códigos mortalidad a cuatro caracteres'], as_index=False).agg({'Muertes':'sum'})
        df_top = df_grp.sort_values('Muertes', ascending=False).head(10)

        # Renombrar columna Descripcion a Descripcion
        df_top = df_top.rename(columns={'Descripcion  de códigos mortalidad a cuatro caracteres':'Descripcion'})
        return df_top[['COD_MUERTE','Descripcion','Muertes']].to_dict('records')
