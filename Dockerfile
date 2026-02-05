FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

COPY index.html /usr/share/nginx/html/
COPY dashboard/ /usr/share/nginx/html/dashboard/

# dashboard/data is a symlink to ../data — resolve it by copying data/ directly
RUN rm -rf /usr/share/nginx/html/dashboard/data
COPY data/ /usr/share/nginx/html/dashboard/data/
COPY data/ /usr/share/nginx/html/data/

EXPOSE 80
