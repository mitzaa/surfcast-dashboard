# Use the nginx:alpine image as a base
FROM nginx:alpine

# Copy the index.html file to the nginx HTML directory
COPY ./index.html /usr/share/nginx/html

# Expose port 80 for the nginx server
EXPOSE 80

# Start the nginx server in the foreground (so Docker can track it)
CMD ["nginx", "-g", "daemon off;"]
