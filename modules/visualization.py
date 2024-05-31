import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.data_processing import numeric_columns

def count_city(df):
    city_counts = df['City'].value_counts()
    df['City_Group'] = df['City'].apply(lambda x: x if city_counts[x] > 10 else 'Other')
    return df

def hotel_price_vs_rating(df):
    if 'City_Group' not in df.columns:
        city_counts = df['City'].value_counts()
        threshold = 50
        df['City_Group'] = df['City'].apply(lambda x: x if city_counts[x] > threshold else 'Other')

    fig = px.scatter(df, x = 'Customers_Rating', 
                 y = "Price", 
                 size = "Max_persons", 
                 size_max = 20,
                 hover_name = "Name",
                 hover_data=['Type_of_room', "City"], 
                 color = "City_Group",
                 labels={ 'Customer_Ratings': 'Customer Ratings', 'Price': 'log_Price (SAR)'},
                log_y = True)
    fig.update_traces(hovertemplate='Hotel: %{hovertext}<br>Rating: %{x}<br>Price: %{y}<br>Room Type: %{customdata[0]}<br>City: %{customdata[1]}')
    return fig

def box_price_cancellation(df):
    fig = px.box(df, x = "Cancelation", y = 'log_price', color = "Star_Rating",hover_data=['Name'])
    return fig

def top_expensive_hotels(df):
    df_sorted_price = df.sort_values('Price', ascending=False)
    fig = px.bar(df_sorted_price.head(10), 
                y='Name', 
                x='Price', 
                orientation='h', 
                hover_data = ["City", 'Star_Rating', "Type_of_room"],
                #title='Top 10 Most Expensive Hotels',
                labels={'Price': 'Price (SAR)', 'Name': 'Hotel Name'},
                color_discrete_sequence=['#6f42c1']
                )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, 
                      
        )
    return fig

def map(df):
    fig = px.scatter_mapbox(df, 
                        lat="Latitude_y", 
                        lon="Longitude_x", 
                        color="Star_Rating", 
                        size="Price",
                        hover_name = "Name",
                        hover_data = ['Type_of_room', 'no_prepayment', 'Cancelation', 'Max_persons', 'Tax', 'Price'] ,
                        size_max=20, 
                        zoom = 3,
                        mapbox_style="carto-positron",
                        )
    fig.update_traces(
        hovertemplate='Hotel: %{hovertext}<br>Room type: %{customdata[0]}<br>No prepayment: %{customdata[1]}<br>Free cancellation: %{customdata[2]}<br>Maximum persons: %{customdata[3]}<br>Taxes: %{customdata[4]}<br>Price: %{customdata[5]}')
    return fig





    
def box_category(df, column_name):
    fig = go.Figure()
    fig.add_trace(go.Box(y=df[column_name].dropna(), name=column_name))

    fig.update_layout(
        title_text='Boxplot of ' + column_name,
        title_x=0.5,
        xaxis_title_text="Value",
        yaxis_title_text=column_name,
        height=400, width=700
    )
    return fig


def pie_star_rating(df):
    star_rating_counts = df['Star_Rating'].value_counts()
    data = go.Pie(labels = star_rating_counts.index, values = star_rating_counts.values, hole = 0.3)
    fig = go.Figure(data)
    fig.update_layout(

        margin=dict(l=20, r=20, t=30, b=20))
    return fig





def customer_rating_gauge(df):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df['Customers_Rating'].mean().round(1),
        title={'text': "Average customer rating", 'font': {'size': 24, 'color': '#6f42c1'}},
        gauge={'axis': {'range': [None, 10]}, 'bar': {'color': "#6f42c1"}},
        number={'font': {'size': 24, 'color': '#6f42c1'}}
    ))

    return fig

def stars_rating_gauge(df):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df[df["Star_Rating"] != 0]["Star_Rating"].mean().round(1),
        title={'text': "Average star rating", 'font': {'size': 24, 'color': '#6f42c1'}},
        gauge={'axis': {'range': [None, 5]}, 'bar': {'color': "#6f42c1"}},
        number={'font': {'size': 24, 'color': '#6f42c1'}}
    ))
    return fig


def top_rating(df):

    average_ratings = df.groupby('City')['Customers_Rating'].mean().sort_values(ascending=False)[:10]
    average_ratings_df = average_ratings.reset_index()
    average_ratings_df = average_ratings_df.iloc[::-1]

    fig = px.bar(average_ratings_df, y='City', x='Customers_Rating',
             title='Average Hotel Customer Ratings by City in Saudi Arabia',
             labels={'Customer_Rating': 'Average Rating'},
             orientation='h',
             height=500, color_discrete_sequence=['#6f42c1'])
    return fig

def heatmap(df):
    numerical_df = df.select_dtypes(include=[np.number])
    correlation_matrix = numerical_df.corr()
    fig = px.imshow(correlation_matrix,
                labels=dict(color="Correlation"),
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                title="Feature Correlation Heatmap",
                color_continuous_scale='Purples')
    return fig