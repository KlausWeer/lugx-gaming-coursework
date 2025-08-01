# Step 1: Start with an official, lightweight Python base image.
# This is like choosing the right size of box to start with.
FROM python:3.9-slim

# Step 2: Set a working directory inside the container.
# All subsequent commands will run from this folder inside the container.
WORKDIR /app

# Step 3: Copy the requirements file into the container.
# We copy this first to take advantage of Docker's caching. If this file doesn't change,
# Docker won't re-install the libraries every time, making builds faster.
COPY requirements.txt .

# Step 4: Install the Python libraries from the requirements file.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code (i.e., app.py) into the container.
COPY . .

# Step 6: Tell Docker what command to run when the container starts up.
# This is the same command you used to run the server manually.
CMD ["python", "app.py"]