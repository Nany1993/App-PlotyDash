# ------------------------------------------------------------------
# Archivo: paginas/ciudades_mas_violentas.py
# Descripción: Layout y callbacks para mostrar las 5 ciudades (municipios)
#              con mayor número de muertes, con filtros de Mes y Sexo,
#              y navegación.
# ------------------------------------------------------------------
import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output

# Ruta al CSV procesado
# CSV con columnas: COD_MUNICIPIO;MES;SEXO;Muertes;MUNICIPIO
DATA_CSV = 'ArchivosProcesados/MuertesPorMunicipio.csv'

df = pd.read_csv(DATA_CSV, sep=';', encoding='utf-8-sig')

# Convertir tipos
df['MES'] = df['MES'].astype(int)
df['Muertes'] = df['Muertes'].astype(int)

# Mapear MES numérico a nombre
mes_map = {
    1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
    7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'
}
df['mes_nombre'] = df['MES'].map(mes_map)

# Opciones de Mes y Sexo
o_months = list(mes_map.values())
sexos = sorted(df['SEXO'].unique())


def layout_ciudades_mas_violentas():
    """
    Layout para el Top 5 municipios con más muertes.
    Incluye filtros de Mes y Sexo, y navegación.
    """
    controls = html.Div([
        # Filtro Mes
        html.Div([
            html.Label('Mes:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-mes',
                options=[{'label': m, 'value': m} for m in o_months],
                placeholder='Todos', clearable=True,
                style={'width':'160px','backgroundColor':'fuchsia','color':'black','fontWeight':'bold'}
            )
        ], style={'marginRight':'20px'}),
        # Filtro Sexo
        html.Div([
            html.Label('Sexo:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-sexo',
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
                }), href='/muerte-por-mes'
            ), style={'marginRight':'10px','alignSelf':'center'}
        ),
        # Botón Siguiente
        html.Div(
            dcc.Link(
                html.Button('Siguiente', style={
                    'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
                    'border':'none','borderRadius':'5px','fontSize':'14px','cursor':'pointer'
                }), href='/indice-mortalidad'
            ), style={'alignSelf':'center'}
        )
    ], style={
        'display':'flex','alignItems':'center','padding':'20px','backgroundColor':'black'
    })

    title = html.H2(
        'TOP 5 Ciudades más violentas de Colombia',
        style={'textAlign':'center','color':'fuchsia','fontSize':'32px','margin':'20px 0'}
    )

    graph = dcc.Graph(id='grafico-ciudades', style={'backgroundColor':'black','height':'70vh'})

    return html.Div([controls, title, graph], style={'backgroundColor':'black','minHeight':'100vh'})


def register_callbacks_ciudades_mas_violentas(app):
    """
    Registra callback para graficar top 5 municipios.
    """
    @app.callback(
        Output('grafico-ciudades','figure'),
        Input('filtro-mes','value'),
        Input('filtro-sexo','value')
    )
    def update_ciudades(mes_sel, sexo_sel):
        # Filtrar datos
        df_f = df.copy()
        if mes_sel:
            df_f = df_f[df_f['mes_nombre']==mes_sel]
        if sexo_sel:
            df_f = df_f[df_f['SEXO']==sexo_sel]

        # Agrupar y seleccionar top 5
        df_grp = df_f.groupby('MUNICIPIO', as_index=False).agg({'Muertes':'sum'})
        df_top = df_grp.nlargest(5, 'Muertes')

        # Gráfico de barras verticales con escala rojo→amarillo→verde
        fig = px.bar(
            df_top,
            x='MUNICIPIO', y='Muertes',
            labels={'CIUDAD':'Ciudad', 'Muertes':'# Muertes por Homicidio en colombia'},
            color='Muertes',
            color_continuous_scale=['red','yellow','green'],
            range_color=(df_top['Muertes'].min(), df_top['Muertes'].max())
        )
        fig.update_layout(
            paper_bgcolor='black', plot_bgcolor='black', font_color='white',
            title='Top 5 Ciudades Con mas Muertes por Homicidio',
            title_font_color='fuchsia', title_font_size=28,
            margin={'r':0,'t':50,'l':0,'b':0},
            xaxis_tickangle=-45
        )
        fig.update_traces(marker_line_color='white', marker_line_width=1)
        return fig
