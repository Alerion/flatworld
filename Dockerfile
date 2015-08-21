FROM ubuntu:14.04
RUN apt-get update && apt-get upgrade
RUN apt-get install -y build-essential libssl-dev libpq-dev libffi-dev python3.4 python3.4-dev \
    python3-pip nodejs libopenblas-dev liblapack-dev git binutils libproj-dev gdal-bin python-gdal
RUN pip3 install -U pip
# RUN ln -s /usr/bin/python3.4 /usr/bin/python

# Lets install system packages, because pip requires to much time
RUN  apt-get install -y python3-numpy python3-scipy python3-gdal

ADD requirements.txt /flatworld/requirements.txt
WORKDIR /flatworld
RUN pip3.4 install -r requirements.txt

RUN apt-get install -y curl
RUN curl --silent --location https://deb.nodesource.com/setup_0.12 | sudo bash -
RUN apt-get install -y nodejs
RUN apt-get install -y build-essential
RUN npm install -g npm
RUN npm install -g gulp
