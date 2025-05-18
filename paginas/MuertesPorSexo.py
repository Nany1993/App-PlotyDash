# ------------------------------------------------------------------
# Archivo: paginas/MuertesPorSexo.py
# Descripción: Gráfico de barras apiladas horizontal de muertes por departamento y sexo.
# ------------------------------------------------------------------
import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output

# Ruta al CSV procesado
# Debe contener: DEPARTAMENTO, SEXO, MANERA_MUERTE, Muertes
DATA_CSV = 'ArchivosProcesados/MuertesPorDepartamento.csv'

df = pd.read_csv(DATA_CSV, sep=';', encoding='utf-8-sig')
# Asegurar tipos
df['Muertes'] = pd.to_numeric(df['Muertes'], errors='coerce').fillna(0).astype(int)

# Opciones de filtro
maneras = sorted(df['MANERA_MUERTE'].unique())


def layout_muertes_por_sexo():
    """
    Layout para muertes por departamento discriminadas por sexo.
    """
    controls = html.Div([
        html.Div([
            html.Label('Manera de muerte:', style={'color':'white','marginRight':'8px'}),
            dcc.Dropdown(
                id='filtro-manera-sexo',
                options=[{'label': m, 'value': m} for m in maneras],
                placeholder='Todas', clearable=True,
                style={'width':'250px','backgroundColor':'fuchsia','color':'black','fontWeight':'bold'}
            )
        ], style={'marginRight':'auto'}),
         # Botón Volver
        html.Div(
            dcc.Link(
                html.Button('Volver', style={
                    'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
                    'border':'none','borderRadius':'5px','fontSize':'14px','cursor':'pointer'
                }), href='/histograma-mortalidad'
            ),
            style={'marginRight':'10px','alignSelf':'center'}
        ),
        html.Div(
            dcc.Link(
                html.Button('Inicio', style={
                    'padding':'10px 20px','backgroundColor':'fuchsia','color':'white',
                    'border':'none','borderRadius':'5px','cursor':'pointer'
                }), href='/'
            ), style={'alignSelf':'center'}
        )
    ], style={'display':'flex','alignItems':'center','padding':'20px','backgroundColor':'black'})

    title = html.H2(
        'Muertes por Departamento y Sexo',
        style={'textAlign':'center','color':'fuchsia','margin':'20px 0'}
    )

    graph = dcc.Graph(id='grafico-sexo-dep', style={'backgroundColor':'black','height':'75vh'})

    return html.Div([controls, title, graph], style={'backgroundColor':'black','minHeight':'100vh'})


def register_callbacks_muertes_por_sexo(app):
    """
    Registra callback para actualizar gráfico apilado.
    """
    @app.callback(
        Output('grafico-sexo-dep','figure'),
        Input('filtro-manera-sexo','value')
    )
    def update_graph(manera_sel):
        dff = df.copy()
        if manera_sel:
            dff = dff[dff['MANERA_MUERTE']==manera_sel]
        # Agrupar por departamento y sexo
        df_grp = dff.groupby(['DEPARTAMENTO','SEXO'], as_index=False).agg({'Muertes':'sum'})
        # Ordenar departamentos por total muertes descendente
        total_dep = df_grp.groupby('DEPARTAMENTO')['Muertes'].sum().sort_values(ascending=False)
        departments_ordered = total_dep.index.tolist()

        # Crear gráfico
        fig = px.bar(
            df_grp,
            x='Muertes',
            y='DEPARTAMENTO',
            color='SEXO',
            orientation='h',
            category_orders={'DEPARTAMENTO': departments_ordered},
            labels={'Muertes':'# Muertes','DEPARTAMENTO':'Departamento'},
            title='Muertes por Departamento y Sexo',
            color_discrete_map={'Masculino':'#ff66b2','Femenino':'#66ccff'}
        )
        fig.update_layout(
            barmode='stack',
            paper_bgcolor='black', plot_bgcolor='black', font_color='white',
            title_font_color='fuchsia', title_font_size=28,
            legend_title_text='Sexo',
            margin={'r':0,'t':50,'l':0,'b':0}
        )
        fig.update_traces(marker_line_color='white', marker_line_width=0.5)
        return fig
