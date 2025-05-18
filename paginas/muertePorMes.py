# ------------------------------------------------------------------
# Archivo: paginas/muertePorMes.py
# Descripción: Layout y callbacks para muertes por mes con filtros de Sexo, Hora y Manera de muerte.
# ------------------------------------------------------------------
import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output

# Ruta al CSV procesado
DATA_CSV = 'ArchivosProcesados/MuertesPorMes.csv'

# Carga de datos
# Se espera columnas: MES (numérico), SEXO, HORA, MANERA_MUERTE, Muertes
df = pd.read_csv(DATA_CSV, sep=';', encoding='utf-8-sig')
# Asegurar MES numérico
try:
    df['MES'] = df['MES'].astype(int)
except Exception:
    pass

# Orden cronológico de los meses
o_months = [
    'Enero','Febrero','Marzo','Abril','Mayo','Junio',
    'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'
]

def layout_muerte_por_mes():
    """
    Layout para muertes por mes (2019), con filtros y navegación.
    """
    # Controles de filtros y botón siguiente
    controls = html.Div([
        # Filtro Sexo
        html.Div([
            html.Label('Sexo:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-sexo-mes',
                options=[{'label': s, 'value': s} for s in sorted(df['SEXO'].unique())],
                placeholder='Todos', clearable=True,
                style={'width':'150px','backgroundColor':'fuchsia','color':'black','fontWeight':'bold'}
            )
        ], style={'marginRight':'20px'}),
        # Filtro Hora
        html.Div([
            html.Label('Hora:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-hora-mes',
                options=[{'label': h, 'value': h} for h in sorted(df['HORA'].unique())],
                placeholder='Todas', clearable=True,
                style={'width':'120px','backgroundColor':'fuchsia','color':'black','fontWeight':'bold'}
            )
        ], style={'marginRight':'20px'}),
        # Filtro Manera de muerte
        html.Div([
            html.Label('Manera:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-manera-mes',
                options=[{'label': m, 'value': m} for m in sorted(df['MANERA_MUERTE'].unique())],
                placeholder='Todas', clearable=True,
                style={'width':'180px','backgroundColor':'fuchsia','color':'black','fontWeight':'bold'}
            )
        ], style={'marginRight':'auto'}),
        # Botón siguiente a CiudadesMasViolentas
        html.Div(
            dcc.Link(
                html.Button('Siguiente', style={
                    'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
                    'border':'none','borderRadius':'5px','fontSize':'14px','cursor':'pointer'
                }), href='/ciudades-mas-violentas'
            ),
            style={'alignSelf':'center'}
        )
    ], style={
        'display':'flex','alignItems':'center','padding':'15px','backgroundColor':'black'
    })

    # Título fijo
    title = html.H2(
        'Muertes por mes para el año 2019',
        style={'textAlign':'center','color':'fuchsia','fontSize':'32px','margin':'20px 0'}
    )

    # Gráfico de líneas
    graph = dcc.Graph(id='grafico-mes', style={'backgroundColor':'black','height':'65vh'})

    # Botón volver al mapa
    back_button = html.Div([
        dcc.Link(
            html.Button('Volver al Mapa', style={
                'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
                'border':'none','borderRadius':'5px','fontSize':'14px','cursor':'pointer'
            }), href='/mapa'
        )
    ], style={'textAlign':'center','padding':'20px','backgroundColor':'black'})

    return html.Div([
        controls,
        title,
        html.Div(graph),
        back_button
    ], style={'backgroundColor':'black','minHeight':'100vh'})


def register_callbacks_muerte_por_mes(app):
    """
    Registra callback para actualizar gráfico de líneas.
    """
    @app.callback(
        Output('grafico-mes','figure'),
        Input('filtro-sexo-mes','value'),
        Input('filtro-hora-mes','value'),
        Input('filtro-manera-mes','value')
    )
    def update_line(sexo_sel, hora_sel, manera_sel):
        # Filtrar datos
        df_f = df.copy()
        if sexo_sel:
            df_f = df_f[df_f['SEXO']==sexo_sel]
        if hora_sel:
            df_f = df_f[df_f['HORA']==hora_sel]
        if manera_sel:
            df_f = df_f[df_f['MANERA_MUERTE']==manera_sel]

        # 'MES' en este CSV ya es nombre (Enero, Febrero, ...)
        # Agrupar muertes por mes_nombre directamente
        df_agg = df_f.groupby('MES', as_index=False).agg({'Muertes':'sum'})
        df_agg = df_agg.rename(columns={'MES':'mes_nombre'})
        # Ordenar cronológicamente
        df_agg['mes_nombre'] = pd.Categorical(df_agg['mes_nombre'], categories=o_months, ordered=True)
        df_agg = df_agg.sort_values('mes_nombre')

        # Gráfico de línea con tema oscuro
        fig = px.line(
            df_agg, x='mes_nombre', y='Muertes', markers=True,
            labels={'mes_nombre':'Mes','Muertes':'# Muertes'}
        )
        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black', font_color='white',
            title_font_color='fuchsia', title_font_size=28,
            xaxis_title=None, yaxis_title=None,
            margin={'r':0,'t':50,'l':0,'b':0}
        )
        return fig
