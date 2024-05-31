from modules import data_processing as proc, visualization as vis
import dash
from dash import dcc,  html
import dash_bootstrap_components as dbc
from modules.data_processing import  df

dash.register_page(__name__,
                   path = "/pricing",
                   title="Pricing",
                   name="Pricing analysis")
box_plot = dcc.Graph(
    figure=vis.box_price_cancellation(df),
    id='box_plot'
)

expensive_hotels = dcc.Graph(
    figure=vis.top_expensive_hotels(df),
    id='top-hotels',
    
)


scatter = dcc.Graph(
    figure = vis.hotel_price_vs_rating(df),
    id = 'scatter'
    )

layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1("Explore Pricing"), width = 12, className='text-center')
    ]),
    dbc.Row([
        dbc.Col(html.Hr(), width = 12)
        ]),
    dbc.Row([
        dbc.Col(html.H2('Box plot of price vs Cancellation policy'), width = 5, className='text-center'),
        dbc.Col(html.H2('Top-10 Expensive Hotels'), width = 7, className='text-center')
    ]),

    dbc.Row([
        dbc.Col(box_plot, width = 5, className="card-text"),
        dbc.Col(expensive_hotels, width = 7, className="card-text")
    ]),
    dbc.Row([
        dbc.Col(html.H2('Scatter plot for price vs customer ratings'), width = 12, className='text-center')
    ]),
    dbc.Row([
        dbc.Col(scatter, width = 12)
    ])
])