# Frontend Dockerfile
FROM node:24-slim

WORKDIR /app

COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

ENTRYPOINT ["sh", "./entrypoint.sh"]

CMD ["npm", "run", "start"]