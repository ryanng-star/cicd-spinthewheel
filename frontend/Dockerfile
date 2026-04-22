# 1. The Engine: A super lightweight web server
FROM nginx:alpine

# 2. The Code: Copy your HTML file into the Nginx public folder
COPY index.html /usr/share/nginx/html/index.html

# 3. The Port: Tell Cloud Run this container listens on port 80 (default for Nginx)
EXPOSE 80

# 4. The Ignition: Start the web server
CMD ["nginx", "-g", "daemon off;"]