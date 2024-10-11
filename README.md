# Project README: Streamlit and Flask Integration

This README file provides detailed instructions for running both the Streamlit front end and Flask back end applications to analyze and visualize customer metrics.

## Project Overview
This project aims to create a customer analytics dashboard by integrating:
- **Flask** as a backend API to compute customer metrics.
- **Streamlit** as a front end for user interaction, where users can enter a customer ID and visualize the metrics fetched from the Flask API.

## Prerequisites
To run this project, you need:

1. **Python 3.x**: Installed on your system.
2. **Required Packages**: Flask, Streamlit, pandas, requests, etc. You can install all dependencies using:
   ```sh
   pip install -r requirements.txt
   ```
   Ensure you have `requirements.txt` listing all necessary packages:
   ```
   Flask
   Streamlit
   pandas
   requests
   numpy
   ```

## File Structure
- **customer_backend.py**: Flask API to compute and serve customer metrics.
- **customer_ui.py**: Streamlit front end for interacting with the backend.
- **data/customer_data.csv**: Data file containing customer order information.

## Step-by-Step Instructions

### Step 1: Running the Flask API Backend
The Flask backend computes metrics such as recency, frequency, average order value, etc., for a given customer ID. Follow these steps to run the Flask app:

1. **Open Terminal in VSCode**
   - Use the shortcut `Ctrl + \`` (backtick) or go to **View > Terminal** to open the integrated terminal in VSCode.

2. **Set Environment Variable `FLASK_APP`**
   - This tells Flask which file to run as the app.
   - Depending on the terminal type, run the appropriate command:
     
     **PowerShell (Windows default terminal in VSCode)**:
     ```powershell
     $env:FLASK_APP = "customer_backend.py"
     flask run
     ```
     
     **Command Prompt (cmd.exe)**:
     ```cmd
     set FLASK_APP=customer_backend.py
     flask run
     ```
     
     **Linux or Git Bash**:
     ```bash
     export FLASK_APP=customer_backend.py
     flask run
     ```

3. **Run Flask Server**
   - Execute the command `flask run` after setting the environment variable.
   - Flask should start and serve the API at `http://127.0.0.1:5000/`.
   
   **Example Output**:
   ```
   * Serving Flask app "customer_backend.py"
   * Environment: development
   * Debug mode: on
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```

4. **Testing the Flask API**
   - You can use tools like **Postman** or `curl` to manually test the API.
   - Example using `curl` to get metrics for a customer:
     ```sh
     curl http://127.0.0.1:5000/api/customer_metrics/C001
     ```

### Step 2: Running the Streamlit Front End
The Streamlit front end allows you to input a customer ID and view customer metrics via the Flask API.

1. **Open a New Terminal** (or use the existing one if Flask is running in the background).
2. **Navigate to the Project Directory**
   - Make sure you are in the directory containing `customer_ui.py`.
3. **Run Streamlit Application**
   - Execute the following command:
   ```sh
   streamlit run customer_ui.py
   ```
4. **Access Streamlit**
   - Streamlit will start a local server, typically running at `http://localhost:8501/`.
   - Open this URL in your browser to view the dashboard.

### Step 3: Testing End-to-End Functionality
- **Enter Customer ID**: In the Streamlit app, enter a customer ID in the sidebar input field.
- **Click "Get Customer Metrics"**: This button sends a request to the Flask backend, and metrics are fetched and displayed on the Streamlit interface.

### Troubleshooting
1. **Flask Server Not Running**
   - Make sure the `FLASK_APP` variable is set correctly.
   - Ensure there are no typos in your file names.

2. **Streamlit Not Connecting to Flask**
   - Ensure Flask is running before starting Streamlit.
   - Check the Flask server URL and the port to ensure they match in your Streamlit request.

3. **Module Not Found Error**
   - Run `pip install` for any missing module, for example:
     ```sh
     pip install Flask
     ```

### Helpful Commands
- **Run Flask with Debug Mode**:
  ```sh
  flask run --reload
  ```
  This automatically reloads Flask when code changes are detected.

- **Terminate the Server**:
  Press `CTRL + C` in the terminal where Flask or Streamlit is running.

### Additional Information
- **Environment Variables**: Set environment variables (`FLASK_APP`, `FLASK_ENV`) as needed for development.
- **Data File**: Ensure `data/customer_data.csv` exists in the correct location and has all the required columns for metric calculations.

## Summary
- Set up and run the Flask backend using `customer_backend.py` to serve customer metrics.
- Set up and run the Streamlit front end using `customer_ui.py` to allow interaction with the backend.
- Access both applications locally to perform end-to-end customer analytics.

Feel free to extend the application by adding new features or improving the user interface. For any questions, refer to the official documentation for **Flask** or **Streamlit**.

### Author
This project was developed to help visualize customer analytics by integrating a simple backend API with an interactive front-end dashboard.

