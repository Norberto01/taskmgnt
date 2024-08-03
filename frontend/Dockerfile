FROM node:20-alpine AS build
WORKDIR /app
COPY ./src/package.json ./src/yarn.lock ./
RUN yarn install --frozen-lockfile --production
COPY ./src .
RUN yarn build
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
RUN chmod -R 755 /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]