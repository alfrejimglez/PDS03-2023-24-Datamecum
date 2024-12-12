# Usage instructions:
# docker build -t fast-api-server .
# docker run -p 8080:8080 fast-api-server

# Use the latest version of the Ubuntu base image
FROM ubuntu:latest

# Set the working directory to /app
# YOUR CODE HERE

# Copy app folder to /app
# YOUR CODE HERE

# Copy requirements.txt to /app
# YOUR CODE HERE

# Copy the model pkl to /app
# YOUR CODE HERE

# Install the dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Install the application dependencies
RUN pip3 install -r requirements.txt

# Expose port 8080
# YOUR CODE HERE

# Run the application with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
