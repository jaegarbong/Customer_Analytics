from flask import Flask, jsonify, request, make_response, send_file
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import io
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Place the CSV reading and feature engineering outside the route functions
# Global variable to store the processed data
data = None

# Function to load and process the data
def load_and_prepare_data():
    
    df = pd.read_csv(r'data/delhi_data.csv')    
    df = feature_engg(df)
    
    return df

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

# Execute once when the app starts: Load and preprocess the data
data = load_and_prepare_data()

def calculate_rfm(df):       
    reference_date = df['Order Date and Time'].max()
    
    # Recency: Time since the last order for each customer
    recency = df.groupby('Customer ID')['Order Date and Time'].max().reset_index()
    recency['Recency'] = (reference_date - recency['Order Date and Time']).dt.days

    # Frequency: Total number of orders per customer
    frequency = df.groupby('Customer ID')['Order ID'].count().reset_index()
    frequency.columns = ['Customer ID', 'Frequency']

    # Monetary: Total amount spent by each customer
    monetary = df.groupby('Customer ID')['Order Value'].sum().reset_index()
    monetary.columns = ['Customer ID', 'Monetary']

    # Merge the RFM metrics into one dataframe
    rfm = recency.merge(frequency, on='Customer ID').merge(monetary, on='Customer ID')
    return rfm

def scale_rfm_features(rfm):
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
    return rfm_scaled,scaler

def perform_kmeans_clustering(rfm_scaled, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(rfm_scaled)
    
    # Return the clusters and the cluster centroids
    return clusters, kmeans.cluster_centers_

def cluster_customers(df):
    # Step 1: Calculate RFM
    rfm = calculate_rfm(df)
    
    # Step 2: Scale the RFM features
    rfm_scaled,scaler = scale_rfm_features(rfm)
    
    # Step 3: Perform K-Means with 3 clusters
    clusters, centroids = perform_kmeans_clustering(rfm_scaled, n_clusters=3)
    
    # Add the cluster labels to the original RFM dataframe
    rfm['Cluster'] = clusters

    # Convert centroids to DataFrame here
    centroids_df = pd.DataFrame(centroids, columns=['Recency', 'Frequency', 'Monetary'])
        
    # Return the RFM dataframe with clusters and centroids
    return rfm,centroids_df,scaler

def plot_rfm_distribution(rfm_with_clusters):
    # Set the aesthetic style of the plots
    sns.set(style="whitegrid")
    
    # Create a figure with subplots for each RFM metric
    fig, axes = plt.subplots(1, 3, figsize=(16,10))
    
    # Recency distribution by cluster
    sns.histplot(data=rfm_with_clusters, x='Recency', hue='Cluster', multiple='stack', palette='Set1', ax=axes[0], kde=True)
    axes[0].set_title('Recency Distribution by Cluster')
    axes[0].set_xlabel('Recency (Days)')
    
    # Frequency distribution by cluster
    sns.histplot(data=rfm_with_clusters, x='Frequency', hue='Cluster', multiple='stack', palette='Set2', ax=axes[1], kde=True)
    axes[1].set_title('Frequency Distribution by Cluster')
    axes[1].set_xlabel('Frequency (Orders)')
    
    # Monetary distribution by cluster
    sns.histplot(data=rfm_with_clusters, x='Monetary', hue='Cluster', multiple='stack', palette='Set3', ax=axes[2], kde=True)
    axes[2].set_title('Monetary Distribution by Cluster')
    axes[2].set_xlabel('Monetary (Amount Spent)')

    # Save the figure to a BytesIO object
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)        
    plt.close(fig)
    return buf    


def calculate_clv(rfm_df, avg_customer_lifetime=12):  # avg_customer_lifetime in months
    """
    Calculate the Customer Lifetime Value (CLV) for each customer based on RFM metrics.
    
    Parameters:
        rfm_df (pd.DataFrame): Dataframe containing Recency, Frequency, Monetary columns for each customer.
        avg_customer_lifetime (int): Estimated customer lifetime in months.
    
    Returns:
        pd.Series: A series containing CLV values for each customer.
    """
    # Average Purchase Value (Monetary / Frequency)
    avg_purchase_value = rfm_df['Monetary'] / rfm_df['Frequency']
    
    # Purchase Frequency is already in the Frequency column
    purchase_frequency = rfm_df['Frequency']
    
    # Estimating CLV
    clv = avg_purchase_value * purchase_frequency * avg_customer_lifetime
    
    return clv

# API endpoint to get customer segmentation data (clusters and centroids)
@app.route('/api/customer_segmentation_data', methods=['GET'])
def customer_segmentation_data():
    global data
    try:
        rfm_with_clusters, centroids_df, scaler = cluster_customers(data)

        # Use scaler to inverse transform centroids to original scale
        centroids_original = scaler.inverse_transform(centroids_df)
        centroids_df = pd.DataFrame(centroids_original, columns=['Recency', 'Frequency', 'Monetary']).round(0)

        cluster_data = rfm_with_clusters.to_dict(orient='records')       
        centroids_data = centroids_df.to_dict(orient='records')
        return jsonify({
            "clusters": cluster_data,
            "centroids": centroids_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to get the RFM distribution plot as an image
@app.route('/api/customer_segmentation_image', methods=['GET'])
def customer_segmentation_image():
    global data
    try:
        rfm_with_clusters,centroids,scaler = cluster_customers(data)
        img_buf = plot_rfm_distribution(rfm_with_clusters)
        return send_file(img_buf, mimetype='image/png', as_attachment=False, download_name='rfm_plot.png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


@app.route('/api/clv', methods=['GET'])
def customer_lifetime_value():
    global data
    try:
        rfm_with_clusters, centroids_df, _ = cluster_customers(data)
        
        # Apply the CLV calculation to rfm_with_clusters
        rfm_with_clusters['CLV'] = calculate_clv(rfm_with_clusters)     
        rfm_with_clusters = rfm_with_clusters.to_dict(orient='records')

        return jsonify({
            "clv":rfm_with_clusters
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

