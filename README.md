This README file provides detailed instructions for running both the Streamlit front end and Flask back end applications to analyze and visualize customer metrics.

## Project Overview
This project aims to create a customer analytics dashboard by integrating:
- **Flask** as a backend API to compute customer metrics.
- **Streamlit** as a front end for user interaction, where users can enter a customer ID and visualize the metrics fetched from the Flask API.

This project is designed to create a comprehensive customer analytics dashboard by integrating a backend API with a user-friendly front end. The goal is to:

1. Provide detailed customer insights through metrics such as recency, frequency, and monetary value.
2. Allow interactive visualization and exploration of customer data to better understand customer behavior and segmentation.
3. The backend is powered by Flask, which serves as an API to calculate metrics, while the front end is implemented using Streamlit, providing an interactive way for users to input customer IDs and visualize key metrics.

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

### Sharing the Application with Others
Now that the application is running locally in Docker, there are a few ways to share it with others so that they can run it easily:

#### **Option 1: Share the Docker Image**
1. **Save the Docker Image** to a file:
   ```sh
   docker save -o customer-analytics-app.tar customer-analytics-app
   ```
   This creates a `.tar` file containing your Docker image, which can be shared via cloud storage or USB.

2. **Load the Image** on another machine:
   ```sh
   docker load -i customer-analytics-app.tar
   ```
   Then, run the container:
   ```sh
   docker run -p 5000:5000 -p 8501:8501 customer-analytics-app
   ```

#### **Option 2: Publish to Docker Hub**
1. **Tag the Image** for Docker Hub:
   ```sh
   docker tag customer-analytics-app your-dockerhub-username/customer-analytics-app
   ```

2. **Push the Image** to Docker Hub:
   ```sh
   docker push your-dockerhub-username/customer-analytics-app
   ```

3. **Share the Repository** so others can pull it:
   ```sh
   docker pull your-dockerhub-username/customer-analytics-app
   ```
   They can then run the container:
   ```sh
   docker run -p 5000:5000 -p 8501:8501 your-dockerhub-username/customer-analytics-app
   ```

#### **Option 3: Deploy to the Cloud**
- You can deploy the Docker container to a cloud provider like **AWS**, **Google Cloud**, **Azure**, **DigitalOcean**, or **Heroku**. This makes the application accessible via a public URL, eliminating the need for others to install Docker locally.

#### **Option 4: Share the Project Code**
- **Share the entire project folder** including the **Dockerfile**, **requirements.txt**, and Python scripts.
- The recipient can **build and run** the Docker image themselves using:
  ```sh
  docker build -t customer-analytics-app .
  docker run -p 5000:5000 -p 8501:8501 customer-analytics-app
  ```

### How to Use This Image on Another Local System
1. **Receive the Docker Image** (either via a `.tar` file or by pulling from Docker Hub).

2. **Load the Image** if received as a `.tar` file:
   ```sh
   docker load -i customer-analytics-app.tar
   ```

3. **Pull the Image** from Docker Hub if it was published there:
   ```sh
   docker pull your-dockerhub-username/customer-analytics-app
   ```

4. **Run the Docker Container**:
   ```sh
   docker run -p 5000:5000 -p 8501:8501 customer-analytics-app
   ```
   This will start the application, making it accessible at `http://localhost:5000` for the Flask backend and `http://localhost:8501` for the Streamlit front end.

### Recommendations
- **Colleagues Familiar with Docker**: Use **Option 1** (save image) or **Option 2** (Docker Hub).
- **General Users**: Deploy the application using **Option 3** to make it accessible via a URL.



## Summary
- Set up and run the Flask backend using `customer_backend.py` to serve customer metrics.
- Set up and run the Streamlit front end using `customer_ui.py` to allow interaction with the backend.
- Access both applications locally to perform end-to-end customer analytics.

Feel free to extend the application by adding new features or improving the user interface. For any questions, refer to the official documentation for **Flask** or **Streamlit**.



### Author
This project was developed to help visualize customer analytics by integrating a simple backend API with an interactive front-end dashboard.

