# Use the official lightweight Nginx image.
FROM nginx:alpine

# Copy all files from the current directory (the frontend static files)
# to the default Nginx HTML directory.
COPY . /usr/share/nginx/html

# Expose port 80 so the container can be accessed on that port.
EXPOSE 80

# Nginx is already configured to run on container start.
