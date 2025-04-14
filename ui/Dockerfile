FROM nginx:alpine

# Copy the UI files to Nginx's default serving directory
COPY . /usr/share/nginx/html/

# Copy our custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for web traffic
EXPOSE 80

# Nginx will start automatically when the container runs 