# ------------------------------------------------------------------
# Archivo: paginas/mapa.py
# Descripción: Layout y callbacks del mapa coroplético.
# ------------------------------------------------------------------
import pandas as pd
import json
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output

# Rutas a los datos
DATA_CSV = 'ArchivosProcesados/MuertesPorDepartamento.csv'
GEOJSON_FILE = 'ArchivosProcesados/Colombia.geo.json'

# Carga inicial de datos
_df = pd.read_csv(DATA_CSV, sep=';', encoding='utf-8-sig')
_df['departamento'] = _df['DEPARTAMENTO'].str.strip().str.upper()
with open(GEOJSON_FILE, 'r', encoding='utf-8') as f:
    _geojson = json.load(f)

# DataFrame de todos los departamentos para rellenar
_all_departamentos = [feat['properties']['NOMBRE_DPT'].upper() for feat in _geojson['features']]
_df_todos = pd.DataFrame({'departamento': _all_departamentos})


def layout_mapa():
    """
    Devuelve el layout de la página de mapa,
    con filtros y botón 'Siguiente' al lado de los filtros.
    """
    # Barra superior con filtros y botón
    top_bar = html.Div([
        # Filtro sexo
        html.Div([
            html.Label('Sexo:', style={'color': 'white', 'marginRight': '30px'}),
            dcc.Dropdown(
                id='filtro-sexo',
                options=[{'label': s, 'value': s} for s in sorted(_df['SEXO'].unique())],
                placeholder='Todos',
                clearable=True,
                style={'width': '300px', 'backgroundColor': 'fuchsia', 'color': 'black', 'fontWeight': 'bold'}
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '40px'}),
        # Filtro manera de muerte
        html.Div([
            html.Label('Manera de muerte:', style={'color': 'white', 'marginRight': '30px'}),
            dcc.Dropdown(
                id='filtro-manera',
                options=[{'label': m, 'value': m} for m in sorted(_df['MANERA_MUERTE'].unique())],
                placeholder='Todas',
                clearable=True,
                style={'width': '300px', 'backgroundColor': 'fuchsia', 'color': 'black', 'fontWeight': 'bold'}
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': 'auto'}),
        # Botón siguiente
        html.Div(
            dcc.Link(
                html.Button('Siguiente', style={
                    'padding': '15px 30px',
                    'backgroundColor': 'fuchsia',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '6px',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'cursor': 'pointer'
                }), href='/muerte-por-mes'
            ),
            style={'display': 'flex', 'alignItems': 'center'}
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'flex-start',
        'alignItems': 'center',
        'padding': '40px',
        'backgroundColor': 'black'
    })

    # Título
    title = html.H2(
        'Mapa de Muertes por Departamento',
        style={'textAlign': 'center', 'color': 'fuchsia', 'fontSize': '40px', 'margin': '20px 0'}
    )

    # Gráfico
    graph = html.Div(
        dcc.Graph(
            id='mapa-departamentos',
            style={'width': '90vw', 'height': '75vh', 'backgroundColor': 'black'}
        ),
        style={'textAlign': 'center', 'paddingBottom': '40px'}
    )

    return html.Div([
        top_bar,
        title,
        graph
    ], style={
        'backgroundColor': 'black',
        'minHeight': '100vh'
    })


def register_callbacks_mapa(app):
    """
    Registra el callback para filtrar y dibujar el mapa.
    """
    @app.callback(
        Output('mapa-departamentos', 'figure'),
        Input('filtro-sexo', 'value'),
        Input('filtro-manera', 'value')
    )
    def update_map(sexo_sel, manera_sel):
        # Filtrar
        df_filtrado = _df.copy()
        if sexo_sel:
            df_filtrado = df_filtrado[df_filtrado['SEXO'] == sexo_sel]
        if manera_sel:
            df_filtrado = df_filtrado[df_filtrado['MANERA_MUERTE'] == manera_sel]

        # Agregar muertes
        df_agru = df_filtrado.groupby('departamento', as_index=False).agg({'Muertes': 'sum'})
        # Rellenar departamentos faltantes con 0
        df_full = _df_todos.merge(df_agru, on='departamento', how='left').fillna({'Muertes': 0})

        # Coroplético
        fig = px.choropleth(
            df_full,
            geojson=_geojson,
            locations='departamento',
            featureidkey='properties.NOMBRE_DPT',
            color='Muertes',
            color_continuous_scale=['white', 'yellow', 'red'],
            range_color=(0, df_full['Muertes'].max()),
            labels={'Muertes': '# Muertes'}
        )
        fig.update_geos(fitbounds='locations', visible=False, bgcolor='black')
        fig.update_traces(marker_line_width=0.5, marker_line_color='gray', selector=dict(type='choropleth'))
        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',
            margin={'r':0, 't':50, 'l':0, 'b':0},
            title_font_color='fuchsia',
            title_font_size=40
        )
        return fig
