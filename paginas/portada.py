from dash import html, dcc

def layout_portada():
    """
    Layout de la página de portada con todos los datos centrados y ocupando toda la pantalla.
    """
    return html.Div(
        children=[
            html.H2("Aplicaciones I – Grupo 1", style={"color": "white", "margin": "30px 0"}),
            html.H2("Maestría en Inteligencia Artificial", style={"color": "white", "margin": "20px 0"}),
            html.H3("Ana María García Arias y Diana Carolina Gonzalez Díaz", style={"color": "white", "fontStyle": "italic", "margin": "20px 0"}),
            html.H3("Aplicación web interactiva para el análisis de mortalidad en Colombia", style={"color": "white", "margin": "20px 0"}),
            html.H3("Profesor: Cristian Duney Bermúdez Quintero", style={"color": "white", "margin": "20px 0"}),
            html.H3("Mayo 2025", style={"color": "white", "margin": "20px 0"}),
            # Botón de informe
            html.Div(
                dcc.Link(
                    html.Button(
                        "Informe Mortalidad en Colombia",
                        style={
                            "marginTop": "30px",
                            "padding": "12px 24px",
                            "backgroundColor": "fuchsia",
                            "color": "white",
                            "border": "none",
                            "borderRadius": "4px",
                            "fontSize": "16px",
                            "cursor": "pointer"
                        }
                    ),
                    href='/mapa'
                ),
                style={"textAlign": "center"}
            )
        ],
        style={
            # Fondo y centrado total
            "backgroundImage": "url('assets/fondo_colombia.png')",
            "backgroundSize": "cover",
            "backgroundPosition": "center",
            "backgroundRepeat": "no-repeat",
            "height": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "padding": "20px",
            "textAlign": "center"
        }
    )
