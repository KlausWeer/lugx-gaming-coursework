# frontend/Dockerfile

# Start from the official, lightweight NGINX image
FROM nginx:1.21-alpine

# Copy all your static website files (index.html, assets/, etc.)
# into the default web root directory inside the container.
COPY . /usr/share/nginx/html

# Overwrite the default NGINX configuration with our custom one.
COPY nginx.conf /etc/nginx/conf.d/default.conf