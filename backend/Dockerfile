# 📦 Frontend Build
FROM node:18 AS frontend
WORKDIR /app/frontend
COPY frontend/ ./
RUN npm install && npm run build

# 🧠 Backend with Python + ML
FROM python:3.11-slim AS backend
WORKDIR /app

# 📂 Copy backend files
COPY backend/ ./backend/
COPY backend/requirements.txt ./requirements.txt
COPY .env .env

# 🛠 System dependencies for ML + TA
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 📦 Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 🧱 Include frontend static build
COPY --from=frontend /app/frontend/build/ ./frontend-build/

# 🚀 Start app
CMD ["python", "backend/app.py"]
