# Build frontend
FROM node:20 AS frontend
WORKDIR /app/frontend
COPY frontend/ .
RUN npm install && npm run build

# Backend with Flask
FROM python:3.10-slim AS backend
WORKDIR /app
COPY backend/ /app/backend/
COPY --from=frontend /app/frontend/dist /app/frontend/dist
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8080
EXPOSE 8080
CMD ["python", "backend/app.py"]
