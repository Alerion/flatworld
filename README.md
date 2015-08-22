# Installation

Build docker images:

    $ docker-compose build

## Create DB

Open terminal in webapp container:

    $ docker-compose run --rm webapp /bin/bash
    root@50c6583102fd:/flatworld# psql -h $(DB_PORT_5432_TCP_ADDR) -U postgres -p $(DB_PORT_5432_TCP_PORT)

    postgres=# CREATE DATABASE flatworld;
    postgres=# \connect flatworld;
    flatworld=# CREATE EXTENSION postgis;
    flatworld=# \q

    root@50c6583102fd:/flatworld# exit

## Prepare data

Create user and world:

    $ docker-compose run --rm webapp make createsuperuser
    $ docker-compose run --rm webapp make generateworld

## Run

Start docker images:

    $ docker-compose build
    $ docker-compose start

Now you can visit http://127.0.0.1:8000/

To stop run:

    $ docker-compose stop

Check status:

    $ docker-compose ps

## Working with Dockerfile

After changes run:

    $ docker-compose build

Stop all containers and remove:

    $ docker stop $(docker ps -a -q)
    $ docker rm $(docker ps -a -q)