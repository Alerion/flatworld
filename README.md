# Installation

Install Python 3.4:

    $ sudo apt-get install build-essential libssl-dev libffi-dev python3.4 python3.4-dev nodejs
    $ sudo npm install --global bower gulp

Clone repo.

Create virtual environment:

    $ virtualenv-3.4 env --system-site-packages
    $ . env/bin/activate

Install dependency:

    (env)$ pip install -r requirements.txt

## Install Crossbar.io

You need Python 2.7 (this is a crap, but autobahn support Python 3 and need Crossbar.io, that
does not support Python 3).

    $ cd crossbar
    $ virtualenv-2.7 env/
    $ . env/bin/activate
    (env)$ pip install -r requirements.txt

Start:

    (env)$ crossbar start
