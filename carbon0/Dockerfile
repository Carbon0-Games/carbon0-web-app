# Credit to Mausam Gaurav, who posted the Dockerfile I used as a starting point
# on this blog: 
# https://datagraphi.com/blog/post/2020/8/30/docker-guide-build-a-fully-production-ready-machine-learning-app-with-react-django-and-postgresql-on-docker

###########
# BUILDER #
###########

# pull official base image
FROM node:15.2.1-alpine3.10 as builder

# set work directory
WORKDIR /usr/src/app/

# install dependencies and avoid `node-gyp rebuild` errors
COPY ./package.json .
COPY ./webpack.config.js .
RUN apk add --no-cache --virtual .gyp \
        python \
        make \
        g++ \
    && npm install \
    && apk del .gyp

# copy our react project
COPY ./react_leaderboard .
COPY ./.babelrc .
RUN ls

# perform npm build
# ARG API_SERVER
# ENV REACT_APP_API_SERVER=${API_SERVER}
# RUN REACT_APP_API_SERVER=${API_SERVER} \
RUN npm run build ./src

#########
# FINAL #
#########

# pull official base image
FROM node:15.2.1-alpine3.10

# set work directory
WORKDIR /usr/src/app

# install serve - deployment static server suggested by official create-react-app
RUN npm install -g serve

# copy our build files from our builder stage
COPY --from=builder /usr/src/app/build ./build