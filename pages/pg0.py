from modules import data_processing as proc, visualization as vis
import dash
from dash import dcc,  html
import dash_bootstrap_components as dbc
from modules.data_processing import  df

dash.register_page(__name__,
                   path = "/",
                   title="Home",
                   name="Home")
                   

hotel_num =  proc.number_of_hotels(df)
avg_price = proc.average_price(df)

card_hotels = dbc.Card(
    [
        dbc.CardImg(src="/assets/hotels.png", top=True, className="card-image", style={'width': '30%'}),
        dbc.CardBody(
            [
                html.H4("Total number of hotels", className="card-title"),
                html.P(f"{hotel_num}", className="card-text"),
            ]
        )
    ],
    className="card-body",  
)

card_price = dbc.Card(
    [
        dbc.CardImg(src="/assets/price_tag.png", top=True, className="card-image", style={'width': '30%'}),
        dbc.CardBody(
            [
                html.H4("Average price", className="card-title"),
                html.P(f"{avg_price} SAR", className="card-text"),
            ]
        ),
    ],
    className="card-body",
)


stars_gauge = dcc.Graph(
    figure=vis.stars_rating_gauge(df),
    className='framed-graph'
)

custom_gauge = dcc.Graph(
    figure = vis.customer_rating_gauge(df),
    className='framed-graph'
)

pie_chart = dcc.Graph(
    figure = vis.pie_star_rating(df),
    className = 'framed-graph'
)

top_hotels = dcc.Graph(
    figure = vis.top_rating(df),
    className = 'framed-graph'
)

layout = dbc.Container([
     dbc.Row([
         dbc.Col(html.H1("Overview"), width = 12, className='text-center')
     ]),
    dbc.Row([
        dbc.Col(html.Hr(), width = 12)
        ]),
    dbc.Row([
        dbc.Col(html.H2("Hotel Stars"), width =5),
        dbc.Col(html.H2('Top-10 Rated Hotels'), width = 7)
        
    ]),
    dbc.Row([
        dbc.Col(pie_chart, width = 5),
        dbc.Col(top_hotels, width = 7)
    ],className="mb-3" ),
    dbc.Row([
        dbc.Col(card_hotels, width= 6),
        dbc.Col(card_price, width = 6),
    ],className="mb-3"),

    dbc.Row([
        dbc.Col(stars_gauge, width = 6),

        dbc.Col(custom_gauge, width=6)
    ], className="mb-3"),
    
    
], fluid=True)