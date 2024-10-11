import streamlit as st
import requests
import pandas as pd
from sys import exit

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
                    # metrics_df = pd.DataFrame(metrics)
                    metrics_df = pd.json_normalize(metrics)

                    # Display Metrics in Streamlit
                    st.write(f'Customer Metrics for {customer_id}')
                    st.table(metrics_df)
                else:
                    st.error('No valid metrics available for the given customer ID.')                    

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
    st.write('Segmentation analysis will be displayed here.')
