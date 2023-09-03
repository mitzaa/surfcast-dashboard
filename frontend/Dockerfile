# Use the nginx:alpine image as a base
FROM nginx:alpine

# Copy the index.html and static files to the nginx HTML directory
COPY ./templates/index.html /usr/share/nginx/html/
COPY ./static /usr/share/nginx/html/static/

# Copy the Nginx configuration file
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for the nginx server
EXPOSE 80

# Start the nginx server in the foreground (so Docker can track it)
CMD ["nginx", "-g", "daemon off;"]


