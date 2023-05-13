FROM node:14-alpine

WORKDIR /usr/src/app

COPY ui/package*.json ./

RUN npm install

COPY ui .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
