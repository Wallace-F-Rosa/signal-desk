from node:22-slim as builder
workdir /app

copy . /app

run npm ci

run npm run build

from nginx:stable-alpine-slim as server

# TODO: make this work with runtime user
run addgroup -S runtime && adduser -S runtime -G runtime

workdir /usr/share/nginx/html

copy --from=builder /app/dist/signal-desk/browser .

copy --from=builder /app/nginx.template.conf /etc/nginx/nginx.conf

run mkdir -p /var/cache/nginx /var/run /etc/nginx/logs
run touch /etc/nginx/logs/error.log
run chown -R nginx:nginx /usr/share/nginx/html \
    /var/cache/nginx \
    /var/run \
    /etc/nginx

EXPOSE 8080

cmd ["nginx", "-g", "daemon off;"]

healthcheck --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "wget", "--spider", "-q", "127.0.0.1:8080", "-s", "-f", "-o", "/dev/null", "||", "echo 'Web service down'" , "||", "exit 1" ]

