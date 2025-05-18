import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from paginas.portada import layout_portada
from paginas.mapa import layout_mapa, register_callbacks_mapa
from paginas.muertePorMes import layout_muerte_por_mes, register_callbacks_muerte_por_mes
from paginas.CiudadesMasViolentas import (
    layout_ciudades_mas_violentas,
    register_callbacks_ciudades_mas_violentas
)
from paginas.IndiceMortalidad import (
    layout_indice_mortalidad,
    register_callbacks_indice_mortalidad
)
from paginas.TablaCausasMuertes import layout_tabla_causas, register_callbacks_tabla_causas
from paginas.HistogramaMortalidad import (
    layout_histograma_mortalidad,
    register_callbacks_histograma_mortalidad
)
from paginas.MuertesPorSexo import (
    layout_muertes_por_sexo,
    register_callbacks_muertes_por_sexo
)


app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Análisis de Mortalidad en Colombia 2019"
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

register_callbacks_mapa(app)
register_callbacks_muerte_por_mes(app)
register_callbacks_ciudades_mas_violentas(app)
register_callbacks_indice_mortalidad(app)
register_callbacks_tabla_causas(app)
register_callbacks_histograma_mortalidad(app)
register_callbacks_muertes_por_sexo(app)


# Callbacks para la navegación entre páginas

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/mapa':
        return layout_mapa()
    elif pathname == '/muerte-por-mes':
        return layout_muerte_por_mes()
    elif pathname == '/ciudades-mas-violentas':
        return layout_ciudades_mas_violentas()
    elif pathname == '/indice-mortalidad':
        return layout_indice_mortalidad()
    elif pathname == '/tabla-causas-muertes':
        return layout_tabla_causas()
    elif pathname == '/histograma-mortalidad':
        return layout_histograma_mortalidad()
    elif pathname == '/muertes-por-sexo':
        return layout_muertes_por_sexo()
    else:
        return layout_portada()


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8050)
