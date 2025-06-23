# 🧱 שלב 1 – בניית הפרונט עם CRA
FROM node:18 AS frontend

WORKDIR /app/frontend
COPY frontend/ ./
RUN npm install && npm run build

# 🧱 שלב 2 – בניית הבקאנד עם Flask
FROM python:3.11-slim AS backend

WORKDIR /app

# התקנת תלויות מערכת בסיסיות
RUN apt-get update && apt-get install -y curl

# העתקת קוד הבקאנד
COPY backend/ ./backend/
COPY --from=frontend /app/frontend/build/ ./frontend-build/

# התקנת תלויות פייתון
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קובץ הגדרות
COPY .env .env

# הגדרת פורט
ENV PORT=8080

CMD ["python", "backend/app.py"]
