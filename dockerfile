# שלב בנייה
FROM node:18 AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# שלב ריצה
FROM node:18
WORKDIR /app
COPY --from=builder /app/build ./build
COPY backend ./backend
COPY package.json ./
RUN npm install --omit=dev
EXPOSE 8080
CMD ["node", "backend/server.js"]