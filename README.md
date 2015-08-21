# Installation

Build docker images:

    $ docker-compose build

## Create DB

Start DB:

    $ docker-compose up db

//FIXME: Move to some initial script
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

Start static watch:

    $ docker-compose run webapp make watchstatic

Now you can visit

## Working with Dockerfile

After changes run:

    $ docker-compose build
