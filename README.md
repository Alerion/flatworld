# Installation

Create config with env variables from template:

    $ cp .env.template .env

Build docker images:

    $ docker-compose build

## Create DB

Open terminal in webapp container:

    $ docker-compose run --rm webapp /bin/bash
    root@50c6583102fd:/flatworld# psql -h $DB_PORT_5432_TCP_ADDR -U postgres -p $DB_PORT_5432_TCP_PORT

    postgres=# CREATE DATABASE flatworld;
    postgres=# \connect flatworld;
    flatworld=# CREATE EXTENSION postgis;

## Prepare data

Create user and world:

    $ docker-compose run --rm webapp make createsuperuser
    $ docker-compose run --rm webapp make removeworlds
    $ docker-compose run --rm webapp make generateworld

## Run

Create and start containers:

    $ docker-compose up

Now you can visit http://127.0.0.1:8000/

Stop services:

    $ docker-compose stop

Start services:

    $ $ docker-compose start

Check status:

    $ docker-compose ps

Watch service logs:

    $ docker-compose logs staticwatch

Run terminal in service:

    $ docker-compose run --rm webapp /bin/bash

## Update containers

    $ docker-compose stop
    $ docker-compose build
    $ docker-compose up
    $ docker-compose start

## Working with Dockerfile

After changes run:

    $ docker-compose build
    $ docker-compose up
    $ docker-compose start

Stop all containers and remove:

    $ docker-compose stop
    $ docker-compose rm

or with Docker:

    $ docker stop $(docker ps -a -q)
    $ docker rm $(docker ps -a -q)