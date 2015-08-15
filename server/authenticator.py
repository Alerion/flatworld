import asyncio

import sys
from pprint import pprint
import os
import datetime
from http import cookies

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import auth, register
from autobahn.wamp.exception import ApplicationError

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'webapp'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
django.setup()

from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.contrib.auth import get_user


class RequestMock(object):
    pass


class AuthService(object):

    @register('authenticate')
    def authenticate(self, realm, authid, details):
        print("authenticate called: realm = '{}', authid = '{}'".format(realm, authid))

        cookie = cookies.SimpleCookie()
        cookie.load(details['transport']['http_headers_received'].get('cookie', ''))
        session_cookie = cookie.get(settings.SESSION_COOKIE_NAME)

        if session_cookie is None:
            raise ApplicationError(ApplicationError.AUTHORIZATION_FAILED)

        session = SessionStore(session_cookie.value)

        request = RequestMock()
        request.session = session
        user = get_user(request)

        if user.is_authenticated():
            return {
                'authid': user.username,
                'secret': 'user',
                'role': 'user'
            }
        else:
            raise ApplicationError(
                ApplicationError.AUTHORIZATION_FAILED,
                "could not authenticate session - no such user {}".format(authid))


class Component(ApplicationSession):
    # TODO: Run like crossbar.io component when it supports Python 3
    # See https://github.com/crossbario/crossbarexamples/blob/master/authenticate/wampcra/client.py
    USER = "authenticator"
    PASSWORD = "password"

    def onConnect(self):
        self.join(self.config.realm, ["wampcra"], self.USER)

    def onChallenge(self, challenge):
        if challenge.method == "wampcra":
            signature = auth.compute_wcs(self.PASSWORD.encode('utf8'),
                                         challenge.extra['challenge'].encode('utf8'))
            return signature.decode('ascii')
        else:
            raise Exception("don't know how to handle authmethod {}".format(challenge.method))

    @asyncio.coroutine
    def onJoin(self, details):
        yield from self.register(AuthService())


if __name__ == '__main__':
    runner = ApplicationRunner('ws://localhost:9000/ws', realm='frontend',
                               debug=True, debug_wamp=False, debug_app=True)
    runner.run(Component)
