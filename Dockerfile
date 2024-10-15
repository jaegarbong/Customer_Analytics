# Step 1: Use a base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file to install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the application code into the container
COPY . /app/

# Step 5: Expose the necessary ports
EXPOSE 5000 8501

# Step 6: Command to run the app
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:5000 customer_backend:app & streamlit run customer_ui.py --server.port 8501 --server.address 0.0.0.0"]
