import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Оцінка вартості картки"    

server = app.server

app.layout = dbc.Container([
    html.Br(),
    dbc.Card([
        dbc.CardHeader(html.H2("💳 Оцінка вартості колекційної картки", className="text-center")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Базова ціна (грн):", className="fw-bold"),
                    dbc.Input(id="base_price", type="number", min=0, value=100, placeholder="Введіть базову ціну"),
                ], md=6),
                dbc.Col([
                    dbc.Label("Мова:", className="fw-bold"),
                    dcc.Dropdown(
                        id="language",
                        options=[
                            {"label": "Українська", "value": "uk"},
                            {"label": "Англійська", "value": "en"},
                            {"label": "Японська", "value": "jp"},
                            {"label": "Італійська", "value": "it"}
                        ],
                        value="uk",
                        placeholder="Оберіть мову"
                    ),
                ], md=6)
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    dbc.Checklist(
                        options=[{"label": "Фольговане покриття", "value": "foil"}],
                        value=[],
                        id="foil",
                        switch=True
                    )
                ], md=6),
                dbc.Col([
                    dbc.Checklist(
                        options=[{"label": "Альтернативний малюнок", "value": "alt"}],
                        value=[],
                        id="alt_art",
                        switch=True
                    )
                ], md=6),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Стан картки:", className="fw-bold"),
                    dcc.Dropdown(
                        id="condition",
                        options=[
                            {"label": "Ідеальний", "value": "perfect"},
                            {"label": "Трохи пошкоджений", "value": "minor"},
                            {"label": "Пошкоджений", "value": "damaged"},
                            {"label": "Сильно пошкоджений", "value": "heavily"}
                        ],
                        value="perfect",
                        placeholder="Оберіть стан"
                    ),
                ], md=12)
            ], className="mb-4"),

            dbc.Row([
                dbc.Col([
                    dbc.Button("🔍 Розрахувати вартість", id="calc_btn", color="primary", className="w-100"),
                ], md=12)
            ]),

            html.Hr(),

            dbc.Row([
                dbc.Col(html.Div(id="result", className="text-center fw-bold fs-4 text-success"))
            ])
        ])
    ], className="shadow-lg p-4 bg-light")
], fluid=True)


@app.callback(
    Output("result", "children"),
    Input("calc_btn", "n_clicks"),
    State("base_price", "value"),
    State("language", "value"),
    State("foil", "value"),
    State("alt_art", "value"),
    State("condition", "value")
)
def calculate_price(n_clicks, base_price, language, foil_list, alt_art_list, condition):
    if not n_clicks:
        return ""

    price = base_price

    # Стан
    condition_modifiers = {
        "perfect": 0.0,
        "minor": -0.25,
        "damaged": -0.5,
        "heavily": -0.75
    }
    price *= (1 + condition_modifiers.get(condition, 0))

    # Мова
    language_modifiers = {
        "uk": 0.10,
        "en": 0.05,
        "jp": 0.25,
        "it": 0.20
    }
    price *= (1 + language_modifiers.get(language, 0))

    # Обмеження на фольгування
    if "foil" in foil_list:
        if language in ["jp", "it"]:
            return "❌ Обрана мова не підтримує фольговані картки!"
        price *= 1.5

    # Обмеження на альтернативний арт
    if "alt" in alt_art_list:
        if language == "it":
            return "❌ Італійські картки не мають альтернативного малюнка!"
        price *= 1.5

    return f"💰 Орієнтовна вартість картки: {round(price, 2)} грн"


if __name__ == "__main__":
    app.run(debug=True)
