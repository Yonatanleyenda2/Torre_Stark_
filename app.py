import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# ============================
# DATOS FIJOS DEL TABLERO
# ============================
df = pd.DataFrame({
    "ZONA": ["P1_CASA", "P1_LOCAL", "P2_H1", "P2_H2", "P2_H3", "P2_H4","P2_H5","P2_H6","P2_H7","P2_H8","P2_H9",
             "P3_H1","P3_H2","P3_H3","P3_H4","P3_H5","P3_H6","P3_H7","P3_H8","P3_H9"],
    "Precio": [5000,550,550,550,450,550,450,550,450,550,550,600,600,600,600,600,600,600,600,600],
    "PISO": [1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3],
    "OCUPACION": ["SI","SI","SI","SI","NO","SI","SI","SI","SI","NO","SI","NO",
                  "NO","NO","NO","NO","NO","NO","NO","NO"]
})

# ============================
# DASH APP
# ============================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1("Torre STARK Dashboard", className="text-center mt-4 mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Filtrar por PISO (Estrato):"),
            dcc.Dropdown(
                id="estrato_dd",
                options=[{"label": str(e), "value": e} for e in sorted(df["PISO"].unique())],
                value=None,
                placeholder="Seleccione un estrato"
            )
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="precio_graf")
        ])
    ]),

    html.H3("Tabla de resultados", className="mt-3"),
    html.Div(id="tabla_div"),

    html.H3("Valor Total MES", className="mt-4"),
    html.Div(id="valor_total", style={"font-size": "30px", "font-weight": "bold", "color": "green"})
], fluid=True)


@app.callback(
    [Output("precio_graf", "figure"),
     Output("tabla_div", "children"),
     Output("valor_total", "children")],
    Input("estrato_dd", "value")
)
def actualizar_tablero(estrato):
    suma = []

    # Filtrar
    dff = df[df["PISO"] == estrato] if estrato else df

    # Gráfica
    fig = px.bar(
        dff,
        x="ZONA",
        y="Precio",
        title="Precio por ZONA",
        labels={"Precio": "Precio (COP)"},
        text="Precio"
    )
    fig.update_traces(textposition='outside')

    # Tabla
    tabla = dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)

    # KPI
    for i in range(len(dff)):
        if dff.iloc[i]["OCUPACION"] == "SI":
            suma.append(float(dff.iloc[i]["Precio"]))

    Valor = sum(suma) * 1000

    return fig, tabla, f"${Valor:,.0f}"


if __name__ == "__main__":
    app.run_server(debug=True)
