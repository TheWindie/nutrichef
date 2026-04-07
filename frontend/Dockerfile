FROM nginx:alpine

# Zkopíruj frontend soubory do nginx html root
COPY . /usr/share/nginx/html

# Nginx konfigurace (proxy na backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
