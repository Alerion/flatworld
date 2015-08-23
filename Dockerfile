FROM ubuntu:14.04
RUN apt-get update && apt-get upgrade
RUN apt-get install -y build-essential libssl-dev libpq-dev libffi-dev python3.4 python3.4-dev \
    python3-pip nodejs libopenblas-dev liblapack-dev git binutils libproj-dev gdal-bin curl \
    postgresql-client
RUN pip3 install -U pip
# RUN ln -s /usr/bin/python3.4 /usr/bin/python

# Lets install system packages, because pip requires to much time
RUN apt-get install -y python3-numpy python3-scipy python3-gdal

# Install JS packages
RUN curl --silent --location https://deb.nodesource.com/setup_0.12 | sudo bash -
RUN apt-get install -y nodejs
RUN npm install -g npm
RUN npm install -g gulp bower
ADD static/bower.json /flatworld/static/bower.json
RUN cd /flatworld/static && bower --allow-root install

# Install Tile Stache dependency
RUN apt-get install -y python2.7 python-dev python-pip python-mapnik2
ADD tilestache/requirements.txt /flatworld/tilestache/requirements.txt
RUN pip2 install -r flatworld/tilestache/requirements.txt

# ENV REFRESHED_AT 2014-06-01
WORKDIR /flatworld
# If requirements.txt is changed, all next steps will be invalidated
ADD requirements.txt /flatworld/requirements.txt
RUN pip3.4 install -r requirements.txt

USER ${USER}
CMD ['make', 'help']
