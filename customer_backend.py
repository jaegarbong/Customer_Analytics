from flask import Flask, jsonify, request
import pandas as pd
import numpy as np

app = Flask(__name__)



# Create order_period column based on order time
def get_order_period(order_time):
    if pd.to_datetime('06:00:00').time() <= order_time < pd.to_datetime('12:00:00').time():
        return 'Morning'
    elif pd.to_datetime('12:00:00').time() <= order_time < pd.to_datetime('18:00:00').time():
        return 'Afternoon'
    else:
        return 'Night'

def get_week_of_month(date):
    first_day = date.replace(day=1)
    day_of_month = date.day
    adjusted_dom = day_of_month + first_day.weekday()
    return (adjusted_dom - 1) // 7 + 1

def feature_engg(df):
    df['Order Date and Time'] = pd.to_datetime(df['Order Date and Time'])

    # Convert 'Order Date and Time' and 'Delivery Date and Time' to datetime format
    df['Order Date and Time'] = pd.to_datetime(df['Order Date and Time'])
    df['Delivery Date and Time'] = pd.to_datetime(df['Delivery Date and Time'])

    # Extracting separate columns for order and delivery date and time
    df['Order Date'] = df['Order Date and Time'].dt.date
    df['Order Time'] = df['Order Date and Time'].dt.time
    df['Delivery Date'] = df['Delivery Date and Time'].dt.date
    df['Delivery Time'] = df['Delivery Date and Time'].dt.time

    # Extract numerical value of discount from 'Discounts and Offers' column
    df['Discount'] = df['Discounts and Offers'].str.extract(r"(\d+\.?\d*)").astype('Int8').fillna(0)

    df['Order Period'] = df['Order Time'].apply(get_order_period)
    df['Order Week'] = df['Order Date'].apply(get_week_of_month)

    # Convert 'Order Week of Month' to an ordered categorical type
    df['Order Week'] = df['Order Date and Time'].apply(lambda x: get_week_of_month(x))
    week_categories = [1, 2, 3, 4, 5]
    df['Order Week'] = pd.Categorical(df['Order Week'], categories=week_categories, ordered=True)

    # Replace values in 'Payment Method' column
    df['Payment Method'] = df['Payment Method'].replace({
        'Cash on Delivery': 'COD',
        'Credit Card': 'CC',
        'Digital Wallet': 'UPI'
    })

    return df


@app.route('/api/customer_metrics/<customer_id>', methods= ['GET'])
def get_customer_metrics(customer_id):
    customer_data = data[data['Customer ID'] == customer_id]
    if not customer_data.empty:
        return jsonify(customer_data.to_dict(orient='records'))
    else:
        return jsonify({'error': 'Customer ID not found'}), 404

if __name__ == '__main__':
    # Load the data from file and apply feature engineering
    data = pd.read_csv('data/customer_data.csv')
    data = feature_engg(data)
    app.run(debug=True, port=5000)
