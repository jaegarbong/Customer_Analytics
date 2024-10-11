from flask import Flask, jsonify, request, make_response
import pandas as pd
import numpy as np
import datetime as dt

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
        'Digital Wallet': 'UPI'
    })

    return df

def calculate_recency(customer_id):
    global data 
    current_date = dt.datetime.now()
    customer_data = data[data['Customer ID'] == customer_id]
    if not customer_data.empty:
        last_order_date = customer_data['Order Date and Time'].max()
        recency = (current_date - last_order_date).days
        return pd.DataFrame({'Metric': ['Recency'], 'Value': [recency]})
    return None

def calculate_frequency(customer_id):
    global data
    customer_data = data[data['Customer ID'] == customer_id]
    if not customer_data.empty:
        frequency = len(customer_data)
        return pd.DataFrame({'Metric': ['Frequency'], 'Value': [frequency]})
    return None

def calculate_monetary(customer_id):
    global data
    customer_data = data[data['Customer ID'] == customer_id]
    if not customer_data.empty:
        monetary = customer_data['Order Value'].sum()
        return pd.DataFrame({'Metric': ['Monetary'], 'Value': [monetary]})
    return None

def calculate_average_order_value(customer_id):
    global data
    customer_df = data[data['Customer ID'] == customer_id]
    
    if not customer_df.empty:
        # Calculate total value of orders (monetary) and frequency
        monetary = customer_df['Order Value'].sum()
        frequency = len(customer_df)
        
        # Calculate Average Order Value
        aov = monetary / frequency
        return pd.DataFrame({'Metric': ['Average Order Value'], 'Value': [round(aov,2)]})
    
    return None

def calculate_preferred_order_period(customer_id):
    global data
    customer_data = data[data['Customer ID'] == customer_id]
    if not customer_data.empty:
        preferred_period = customer_data['Order Period'].mode()[0]
        return pd.DataFrame({'Metric': ['Preferred Order Period'], 'Value': [preferred_period]})
    return None

def calculate_average_days_between_orders(customer_id):
    global data
    customer_data = data[data['Customer ID'] == customer_id].sort_values(by='Order Date and Time')
    if len(customer_data) > 1:
        customer_data['Time Difference'] = customer_data['Order Date and Time'].diff().dt.days
        avg_time_between_orders = customer_data['Time Difference'].mean()
        return pd.DataFrame({'Metric': ['Average Time Between Orders'], 'Value': [avg_time_between_orders]})
    return None

def calculate_preferred_payment_method(customer_id):
    global data
    customer_data = data[data['Customer ID'] == customer_id]
    if not customer_data.empty:
        preferred_payment_method = customer_data['Payment Method'].mode()[0]
        return pd.DataFrame({'Metric': ['Preferred Payment Method'], 'Value': [preferred_payment_method]})
    return None

# Load the data from file and apply feature engineering
data = pd.read_csv(r'data\delhi_data.csv')
data = feature_engg(data)

@app.route('/api/customer_metrics/<customer_id>', methods= ['GET'])
def get_customer_metrics(customer_id):
    
    customer_data = data[data['Customer ID'] == customer_id]

    if customer_data.empty:        
        response = make_response(jsonify({'message': 'Customer ID not found'}), 404)
        return response

    try:   
        customer_metrics = pd.DataFrame(columns=['Metric', 'Value'])
        recency_df = calculate_recency(customer_id)
        frequency_df = calculate_frequency(customer_id)
        monetary_df= calculate_monetary(customer_id)
        aov_df = calculate_average_order_value(customer_id)    
        preferred_order_period_df = calculate_preferred_order_period(customer_id)
        average_days_between_orders_df = calculate_average_days_between_orders(customer_id)
        preferred_payment_method_df = calculate_preferred_payment_method(customer_id)

        # Create a list of DataFrames, filter out None values, and concatenate them
        metrics_list = [
            recency_df,
            frequency_df,
            monetary_df,        
            aov_df,
            preferred_order_period_df,
            average_days_between_orders_df,
            preferred_payment_method_df
        ]
        
        customer_metrics = pd.concat([df for df in metrics_list if df is not None], ignore_index=True)   
        
        # Return the customer metrics as JSON
        return jsonify(customer_metrics.to_dict(orient='records'))
    
    except Exception as e:
        # Log the error for debugging purposes
        # print(f"Error while calculating metrics for customer ID {customer_id}: {e}")        
        return make_response(jsonify({'message': 'An error occurred while processing metrics.'}), 500):


if __name__ == '__main__':
    app.run(debug=True, port=5000)
