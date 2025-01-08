# Use the official Python image as the base
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy Streamlit app code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]