
import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from modules.data_processing import  df, numeric_columns, categories
import modules.visualization as vis


dash.register_page(__name__, path="/more", title="More Details", name="More Details")

heatmap = dcc.Graph(figure= vis.heatmap(df), className='no-frame')
layout = dbc.Container([
    dbc.Row([dbc.Col(html.H1("Explore more statistical details"), className='text-center' , width = 12)]),
    dbc.Row([
        dbc.Col(html.P("Select column you want to see histogram for"))
    ]),


    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='pg3--dropdown',
                options=[{'label': col, 'value': col} for col in numeric_columns],
                value=numeric_columns[0],
                multi=False
            ),
            dcc.Graph(id='pg3--histogram')
        ], width = 10)
    ], className='ms-2'),
    dbc.Row([
        dbc.Col(html.H2("Heatmap"),width = 10)
    ], className='text-center'),
    dbc.Row([
        dbc.Col(heatmap, width = 10, className='heatmap')
    ])
])

@callback(
    Output(component_id='pg3--histogram', component_property='figure'),
    Input(component_id='pg3--dropdown', component_property='value'),   
)
def update_graph(selected_col):
    fig = px.histogram(data_frame=df, x=selected_col, color_discrete_sequence=['#6f42c1'])

    fig.update_layout(
        title_text=f'Histogram of {selected_col}',
        title_font_size = 30 , 
        title_x=0.5,
        xaxis_title_text='Value',
        yaxis_title_text='Count',
        height=400, width=700,
        title_font=dict(color='#6f42c1')
    )
    return fig
