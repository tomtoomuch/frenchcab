FROM node:22

WORKDIR /app

COPY package*.json ./

RUN npm install --build-from-source=sqlite3

COPY . .

EXPOSE 3001

CMD ["npm", "run", "start"]