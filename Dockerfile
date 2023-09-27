# Use an official Python runtime as a parent image. 
FROM python:3.9-slim

# Download Package Information for system-level packages
RUN apt-get update -y

# upgrade pip as necesssary
RUN pip install --upgrade pip
RUN apt-get install -y libglib2.0-0
RUN apt-get install -y alsa-utils

# Install the Tkinter package
RUN apt-get install tk -y

# Set the working directory in the container
#WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY requirements.txt ./

# Install any specified dependencies for Python packages
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

#Add ALSA configuration file to use a null (dummy) audio device  
COPY asound.conf /etc/asound.conf

# Specify the command to run on container start
CMD ["python", "main-gui.py"]