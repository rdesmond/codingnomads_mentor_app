# pull base image
FROM python:3.8.0-alpine


# install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

# set environment variables

# prevents python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# prevents buffering of stdout and stderr
ENV PYTHONUNBUFFERED 1


# set working directory
WORKDIR /usr/src/app


# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh


# add app
COPY . /usr/src/app
