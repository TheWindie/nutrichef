FROM nginx:alpine

ARG BUILD_DATE=unknown
LABEL build_date=$BUILD_DATE

COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
