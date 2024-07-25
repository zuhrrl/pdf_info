# Use the official Python image as the base image
FROM --platform=linux/amd64 python:3.7

# Set the working directory inside the container
WORKDIR /app

# Install LibreOffice and other necessary packages
RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 80 (or the port your FastAPI app is running on)
EXPOSE 80

# Command to run your FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9292"]
