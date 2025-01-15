# Use Ubuntu 22.04.4 LTS as the base image
FROM ubuntu:22.04.4

# Update and install necessary packages
RUN apt-get update && apt-get install -y python3.9.19

# Set the working directory
WORKDIR /application

# Copy the application code into the container
COPY . /application

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Gunicorn server
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]