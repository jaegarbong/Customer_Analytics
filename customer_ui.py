import streamlit as st
import requests
import pandas as pd

st.title('Customer Dashboard')

st.sidebar.title('Navigation')

# Sidebar for navigation with a tab-like feel
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select a Task:', ['Search Customer Metrics', 'Customer Segmentation Dashboard',],index=None)

if options == 'Search Customer Metrics':
    st.header('Search Customer Metrics')
    customer_id = st.sidebar.text_input('Enter Customer ID:') 
    
    if customer_id:
        if st.sidebar.button('Get Customer Metrics'):
            try:
                response = requests.get(f'http://127.0.0.1:5000/api/customer_metrics/{customer_id}')

                if response.status_code == 200:

                    ## Convert the json response to dataframe
                    metrics  = response.json
                    metrics = pd.DataFrame(metrics)

                    ## Display Metrics in Streamlit
                    st.write(f'Customer Metrics for {customer_id}')
                    st.dataframe(metrics)

            except requests.exceptions.RequestException as e:
                st.error(f"Error Occurred while making request: {e}")

                
elif options == 'Customer Segmentation Dashboard':
    st.header('Customer Segmentation Dashboard')
    st.write('Segmentation analysis will be displayed here.')
