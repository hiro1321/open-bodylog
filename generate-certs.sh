#!/bin/sh

# Create a directory for SSL certificates if it doesn't exist
mkdir -p /etc/nginx/ssl

# Generate a self-signed SSL certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/localhost.key -out /etc/nginx/ssl/localhost.crt -subj "/CN=localhost"
