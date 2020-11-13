###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.0-slim as builder

# set work directory
WORKDIR /usr/src/app

# Don't write to pyc files, and log messages (helps with debugging)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./carbon0/requirements.txt .
RUN python pip install -r carbon0/requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9.0-slim

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint.sh
RUN apt-get update && apt-get install -y --no-install-recommends netcat && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install dependencies
COPY --from=builder /usr/src/app/requirements.txt .

# set work directory
WORKDIR /usr/src/app

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy our django project
COPY ./carbon0 .

# run entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]