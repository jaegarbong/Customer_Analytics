import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO

st.title('Customer Dashboard')
st.sidebar.title('Navigation')

# Sidebar for navigation with a tab-like feel
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select a Task:', ['Search Customer Metrics', 'Customer Segmentation Dashboard',],index=None)

if options == 'Search Customer Metrics':
    st.header('Search Customer Metrics')
    customer_id = st.sidebar.text_input('Enter Customer ID:') 
    
    if customer_id:        
        try:
            response = requests.get(f'http://127.0.0.1:5000/api/customer_metrics/{customer_id}')            

            if response.status_code == 200:
                ## Convert the json response to dataframe
                metrics  = response.json()                    

                if metrics and isinstance(metrics, list) and all(isinstance(i, dict) for i in metrics):          
                    # Create a DataFrame from the metrics data if it is valid                    
                    metrics_df = pd.json_normalize(metrics)

                    # Display Metrics in Streamlit
                    st.write(f'Customer Metrics for {customer_id}')
                    st.table(metrics_df)
                else:
                    st.error('Customer Not Found.')                    

            elif response.status_code == 404:
                # Handle case when customer ID is not found
                st.error('Customer ID not found. Please enter a valid ID.')
            else:
                # Handle other unexpected status codes
                st.error(f"Error Occurred: {response.status_code} - {response.reason}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error Occurred while making request: {e}")
            
            
elif options == 'Customer Segmentation Dashboard':
    st.header('Customer Segmentation Dashboard')

    # Section 1: Display Cluster Table
    st.subheader("Customer Segmentation Table")
    segmentation_data = requests.get("http://127.0.0.1:5000/api/customer_segmentation_data").json()
    cluster_data = segmentation_data['clusters']
    cluster_df = pd.DataFrame(cluster_data)
    st.dataframe(cluster_df)  # Display cluster data in a table

    # Section 2: Cluster Interpretation
    st.subheader("Cluster Interpretation")
    centroids_data = segmentation_data['centroids']
    centroids_data = pd.DataFrame(centroids_data).astype('int')

    # Add a new column explaining the cluster in brief
    centroids_data['Cluster Interpretation'] = [
    'Low Recency, Low Frequency, High Monetary (High-value customers)',
    'High Recency, Low Frequency, Moderate Monetary (Inactive customers)',
    'Moderate Recency, High Frequency, High Monetary (Frequent and high-value customers)'
]
    st.table(centroids_data)    
 
    # Section 3: Display RFM Distribution Plot
    st.subheader("RFM Distribution Plot")
    try:    
        response = requests.get("http://127.0.0.1:5000/api/customer_segmentation_image")
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            st.image(img, caption="RFM Distribution by Cluster", use_column_width=True)            
        else:
            st.error("Failed to load the plot. Status Code: " + str(response.status_code))
    except Exception as e:
        st.error(f"Error fetching plot: {str(e)}")
