import streamlit as st

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
            customer_metrics = search_customer_metrics(customer_id)       
            st.write('Customer Metrics for:', customer_id)

elif options == 'Customer Segmentation Dashboard':
    st.header('Customer Segmentation Dashboard')
    st.write('Segmentation analysis will be displayed here.')
