# --- Le Build ---
FROM node:20-alpine AS builder

WORKDIR /frontapp

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# --- Le Serveur de Production ---
FROM nginx:stable-alpine

COPY --from=builder /frontapp/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]