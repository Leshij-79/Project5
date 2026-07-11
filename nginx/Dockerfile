FROM ubuntu:latest
LABEL authors="Alex"

ENTRYPOINT ["top", "-b"]

FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

COPY html/ /usr/share/nginx/html/

