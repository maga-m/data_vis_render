import numpy as np
import pandas as pd
import os

script_dir = os.path.dirname(__file__)
relative_path = os.path.join(script_dir, '..', 'data', 'vis_data.csv')

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print("The specified file was not found.")
        return None

def preprocess_data(df):
    if df is None:
        return None

    # Rename columns
    df = df.rename(columns={
        'Canelation': 'Cancelation',
        'Credit_card': 'reservation_without_card',
        'reservations_Payment': 'no_prepayment'
    })

    # Clean and convert price
    df['Price'] = df['Price'].replace('[^0-9.]', '', regex=True).astype(float)

    # Simplify maximum persons
    df['Max_persons'] = df['Max_persons'].str.extract('(\d+)').astype(int)

    # Handle customer reviews
    df['Customers_Review'] = pd.to_numeric(df['Customers_Review'].str.replace(' reviews', '').str.replace(',', ''), errors='coerce')

    # Boolean transformations
    df['reservation_without_card'] = df['reservation_without_card'].notna()
    df['Cancelation'] = df['Cancelation'].str.contains('FREE cancellation', na=False)
    df['no_prepayment'] = df['no_prepayment'].str.contains('No prepayment needed', na=False)

    # Splitting and cleaning bed types
    df[['num_beds', 'bed_type']] = df['Bed_type'].str.extract('(\d+) (.*)')
    df['bed_type'] = df['bed_type'].str.replace(r'\(.*\)', '').str.strip()
    df = df.drop(columns='Bed_type')

    # Drop unnecessary columns
    df = df.drop(columns=['Unnamed: 0', "Breakfst_included", "Property_Demand"])

    # Calculate taxes
    df['Tax'] = get_taxes(df['Tax'].str.split().to_list())

    # Log of price
    df['log_price'] = np.log(df['Price'])

    return df

def get_taxes(column):
    taxes=[]
    for i in column:
        if "+SAR" in i:
            taxes.append(float(i[1]))
        elif "includes" in i:
            taxes.append(0)
        else:
            taxes.append(np.nan)
    return taxes

categories= ['num_beds', "Star_Rating", 'no_prepayment', 'Cancelation', 'Max_persons']


def number_of_hotels(df):
    return len(df)

def average_price(df):
    return df['Price'].mean().round(2)

df = load_data(relative_path)
df = preprocess_data(df)

numeric_columns = ['Price', 'Customers_Rating', 'Customers_Review', 'Tax', 'Longitude_x', 'Latitude_y', 'log_price', 'num_beds', 'Star_Rating', 'no_prepayment', 'Cancelation', 'Max_persons']



def group_cities(df, threshold=10):
    city_counts = df['City'].value_counts()
    df['City_Group'] = df['City'].apply(lambda x: x if city_counts[x] > threshold else 'Other')
    return df