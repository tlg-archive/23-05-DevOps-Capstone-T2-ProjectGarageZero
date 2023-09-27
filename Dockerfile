# Use an official Python runtime as a parent image. 
FROM python:3.9-slim

# Download Package Information for system-level packages
RUN apt-get update -y

# upgrade pip as necesssary
RUN pip install --upgrade pip

# Install the Tkinter package
RUN apt-get install tk -y

# Set the working directory in the container
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY . /app

# Install any specified dependencies for Python packages
RUN pip install --no-cache-dir -r requirements.txt


# Specify the command to run on container start
CMD ["python", "./main-gui.py"]