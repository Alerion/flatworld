import asyncio
import inspect
import os
import sys
import ujson
from http import cookies

from autobahn.asyncio.websocket import WebSocketServerProtocol
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'webapp'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
django.setup()

from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.contrib.auth import get_user

from pprint import pprint


class BaseRpcProtocol(WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._methods = {}
        self._user = None

    def onConnect(self, request):
        # TODO: move this to other server and call with async
        cookie = cookies.SimpleCookie()
        cookie.load(request.headers.get('cookie', ''))
        session_cookie = cookie.get(settings.SESSION_COOKIE_NAME)

        if session_cookie is None:
            self.authentication_failed()

        session = SessionStore(session_cookie.value)

        class RequestMock(object):
            pass

        request = RequestMock()
        request.session = session
        user = get_user(request)

        if user.is_authenticated():
            self._user = {
                'id': user.id,
                'username': user.username
            }
        else:
            self.authentication_failed()

    @asyncio.coroutine
    def onMessage(self, payload, isBinary):
        # Not sure this can happen, but lets check
        if not self._user:
            self.authentication_failed()

        # TODO: add better validation
        if not isBinary:
            data = ujson.loads(payload)

            if data.get('method') not in self._methods:
                self.send_error(data, 'Method does not exist')
            else:
                method = self._methods[data.get('method')]

            if 'args' in data and data['args']:
                args = data['args']
            else:
                args = []

            # TODO: add async call
            try:
                if (asyncio.iscoroutinefunction(method)):
                    value = yield from method(*args)
                    self.send_success(data, value)
                else:
                    self.send_success(data, method(*args))
            except TypeError:
                self.send_error(data, 'Invalid method call. Check arguments.')

    def authentication_failed(self):
        self.sendClose()

    def register(self, name, func):
        self._methods[name] = func

    def send_success(self, data, value):
        response = {
            'id': data['id'],
            'type': data['type'],
            'event': 'success',
            'value': value
        }
        self.sendMessage(ujson.dumps(response).encode('utf8'), isBinary=False)


    def send_error(self, data, message):
        response = {
            'id': data['id'],
            'type': data['type'],
            'event': 'error',
            'message': message
        }
        self.sendMessage(ujson.dumps(response).encode('utf8'), isBinary=False)



def register(name):
    def decorate(func):
        assert(callable(func))
        if not hasattr(func, '_rpc_method_name'):
            func._rpc_method_name = name
        return func
    return decorate
