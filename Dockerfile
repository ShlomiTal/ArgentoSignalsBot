# 🔧 Build React Frontend
FROM node:20 AS frontend
WORKDIR /app/frontend
COPY frontend/ .
RUN npm install
RUN npm run build

# 🔧 Build Python Backend
FROM python:3.11-slim AS backend
WORKDIR /app
COPY backend/ ./backend
COPY --from=frontend /app/frontend/dist ./frontend_dist
COPY backend/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# ✅ Run Backend API
EXPOSE 8000
ENV PORT=8000
WORKDIR /app/backend
CMD ["python", "main.py"]
