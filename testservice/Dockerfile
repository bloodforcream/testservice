FROM python:3.8-alpine

ENV APP_HOME=/src

RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk --no-cache add musl-dev linux-headers g++

COPY requirements.txt /src/
RUN pip install -r requirements.txt

COPY . $APP_HOME