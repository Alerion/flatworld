# Installation

## Install system packages:

    $ sudo apt-get install build-essential libssl-dev libffi-dev python3.4 python3.4-dev nodejs
    $ sudo npm install --global bower gulp

## Clone repo.

## Create virtual environment:

    $ virtualenv-3.4 env --system-site-packages
    $ . env/bin/activate

## Install GeoDjango, PostGIS, GDAL and other

https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/

## Install PostgreSQL

    $ sudo apt-get install postgresql-9.4 postgresql-contrib-9.4 libpq-dev

If packages are not available follow [this instruction](<http://www.postgresql.org/download/linux/ubuntu/>)
how to add repository. (Check Ubuntu version ``lsb_release -a``)

## Create database

    $ sudo su - postgres
    $ createdb fantasy_map
    $ createuser -P fantasy_map

        Enter password for new role: fantasy_map
        Enter it again: fantasy_map

    $ psql

        postgres=# GRANT ALL PRIVILEGES ON DATABASE fantasy_map TO fantasy_map;

    $ psql flatworld

        flatworld=# CREATE EXTENSION postgis;

    $ ./manage.py migrate
    $ ./manage.py import_map

## Install dependency:

    (env)$ pip install -r requirements.txt
