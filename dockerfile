# # Use official Python 3.12.2 slim image
# FROM python:3.11.2-slim

# # Environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Set working directory
# WORKDIR /app

# # Install system packages
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# # Copy project files
# COPY . /app

# # Install Python dependencies from requirements.txt
# COPY requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Expose Streamlit default port
# EXPOSE 8501




# Step 1: Specify the base imag
FROM python:3.12.2-slim
RUN apt-get update
# # Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 2: Set the working director
WORKDIR /app
# Step 3: Copy application code into the containe
COPY . /app
COPY requirements.txt /app/
# Step 4: Install dependencie
RUN pip install --no-cache-dir -r requirements.txt
# Step 5: Expose the application por
EXPOSE 5000

# Run the Streamlit app using -m pattern
CMD ["python", "-m", "streamlit", "run", "Streamlit_UI/chatbot_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
