FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM node:20-alpine AS admin-builder
WORKDIR /app
COPY admin/package.json admin/package-lock.json* ./
RUN npm ci
COPY admin/ .
RUN npm run build

FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev nginx && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt uvicorn

COPY backend/ .

COPY --from=frontend-builder /app/dist /frontend-dist
COPY --from=admin-builder /app/dist /admin-dist

RUN rm -f /etc/nginx/sites-enabled/default
COPY <<'NGINX' /etc/nginx/nginx.conf
events {
    worker_connections 1024;
}
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    sendfile on;
    keepalive_timeout 65;

    server {
        listen __PORT__;

        # Frontend
        location / {
            root /frontend-dist;
            index index.html;
            try_files $uri $uri/ /index.html;
        }

        # Admin
        location /admin {
            alias /admin-dist;
            index index.html;
            try_files $uri $uri/ /admin/index.html;
        }

        # API
        location /api/ {
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
NGINX

COPY <<'SCRIPT' /start.sh
#!/bin/bash
cd /app
python init_prod.py
# Use 8000 for nginx, 8001 for uvicorn (same as railway PORT env)
NGINX_PORT=${PORT:-8000}
API_PORT=8001
sed "s/__PORT__/${NGINX_PORT}/g" /etc/nginx/nginx.conf > /tmp/nginx.conf
mv /tmp/nginx.conf /etc/nginx/nginx.conf
cd /app
uvicorn app.main:app --host 127.0.0.1 --port ${API_PORT} --workers 2 &
nginx -g "daemon off;"
SCRIPT

RUN chmod +x /start.sh

EXPOSE 8000
CMD ["/start.sh"]
