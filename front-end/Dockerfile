FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
# Cette ligne cherche le dossier de build et copie son contenu de manière intelligente
COPY --from=build /app/dist/*/browser /usr/share/nginx/html/
# Si votre version d'Angular ne crée pas de sous-dossier /browser, on copie la racine du dist :
COPY --from=build /app/dist/* /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]