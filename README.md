# Installation

Build docker images:

    $ docker-compose build

## Create DB

Start DB:

    $ docker-compose up db

In other terminal connect and create DB(without password):

    $ psql -h localhost -U postgres -p 9999

        postgres=# CREATE DATABASE flatworld;
        postgres=# \connect flatworld;
        flatworld=# CREATE EXTENSION postgis;

## Prepare data

Run bash:

    $ docker-compose run webapp make createsuperuser
    $ docker-compose run webapp make generateworld

Start docker images:

    $ docker-compose up

## Working with Dockerfile

After changes run:

    $ docker-compose build
