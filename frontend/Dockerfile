# Installing stage

FROM node:18.12-alpine as install-stage
WORKDIR /frontend
ENV PATH /frontend/node_modules/.bin:$PATH
COPY package.json ./
RUN npm install

# Building stage

FROM node:18.12-alpine as build-stage
COPY --from=install-stage /frontend/node_modules/ /frontend/node_modules
WORKDIR /frontend
COPY . .
CMD npm run build

# Serving stage
# FROM nginx:1.23.2-alpine
# COPY --from=build-stage /frontend/dist /usr/share/nginx/html

