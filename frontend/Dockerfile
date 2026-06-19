# --- Le Build ---
FROM node:20-alpine AS builder

WORKDIR /frontapp

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# --- Le Serveur de Production ---
FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]