from re import template
from dash import Input, html, Dash, dcc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px

# Read data
df = pd.read_csv('fetched_data.csv')

# print(__name__)
fig = px.line(df, x='Date', y=['Open'], title='Close')

app = Dash(__name__)
# app.title = 'Main Title'
# app.layout = html.Div(
#     id='app-container',
#     children=[
#         html.H1('Stock Analysis'),
#         html.P('Open'),
#         dcc.Graph(figure=fig)
#     ]
# )

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="header-area",
            children=[
                html.H1(
                    id="header-title",
                    children="Stock Price Analysis",

                ),
                html.P(
                    id="header-description",
                    children=("Stock price for the year 2021"),
                ),
            ],
        ),
        html.Div(
            id='drop-menu',
            children=[
                html.Div(
                    children=[
                        html.Div(
                            className='menu-title',
                            children='Select'
                        )
                    ]
                ),
                dcc.Dropdown(
                    id='filter-columns',
                    className='dropdown',
                    options=[{'label': col_name, 'value': col_name}
                             for col_name in df.columns[1:]],
                    clearable=False,
                    value='Close'
                )
            ]
        ),
        html.Div(
            id="graph-container",
            children=dcc.Graph(
                id="stock-price",
                figure=fig,
                config={"displayModeBar": False}
            ),
        ),
    ]
)


@app.callback(
    Output('stock-price', 'figure'),
    Input('filter-columns', 'value')
)
def update_chart(col_name):
    fig = px.line(df, x='Date', y=[col_name], title=col_name)

    fig.update_layout(template='plotly_dark')

    return fig


app.run(debug=True)
