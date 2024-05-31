from modules import visualization as vis
import dash
from dash import dcc,  Output, Input, html, callback
import dash_bootstrap_components as dbc
from modules.data_processing import  df
import plotly.express as px
import numpy as np

dash.register_page(__name__,
                   path = "/map",
                   title="Map",
                   name="Geographical analysis")
step_value = 1
max_price = df['Price'].max()
rounded_max_price = np.ceil(max_price / step_value) * step_value  # Round up to the nearest step_value

slider_marks = {i: f'${i}' for i in range(int(df['Price'].min()), int(rounded_max_price)+1, step_value*1000)}
scatter = dcc.Graph(figure = vis.hotel_price_vs_rating(df))
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("View hotels on the map"), width=12, className='text-center'),
        dbc.Col(html.P("Use the sliders and selectors to refine your search:"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.RangeSlider(
            id='price-range-slider',
            min=int(df['Price'].min()),
            max=int(rounded_max_price),
            step=step_value,
            value=[int(df['Price'].min()), int(rounded_max_price)],
            marks=slider_marks,
            tooltip={"placement": "bottom", "always_visible": True}
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='star-rating-dropdown',
            options=[{'label': f'{i} stars', 'value': i} for i in range(6)],
            value=[0, 1, 2, 3, 4, 5],  # Default all selected
            multi=True,
            placeholder="Select star ratings",
        ), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='hotel-map'), width=12)
    ])
], fluid=True)



@callback(
    Output('hotel-map', 'figure'),
    Input('price-range-slider', 'value'),
     Input('star-rating-dropdown', 'value')
)
def update_map(price_range, star_ratings):
    
    filtered_df = df[
        (df['Price'] >= price_range[0]) & 
        (df['Price'] <= price_range[1]) &
        (df['Star_Rating'].isin(star_ratings))
    ]
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude_y",
        lon="Longitude_x",
        color = 'Star_Rating',
        size="Price",
        hover_name="Name",
        hover_data=['Type_of_room', 'no_prepayment', 'Cancelation', 'Max_persons', 'Tax'],
        size_max=30,
        zoom=3,
        mapbox_style="carto-positron",
        color_continuous_scale = 'Purples'
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
