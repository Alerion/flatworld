import asyncio
import os
import sys
import ujson
import msgpack
from http import cookies
from types import MethodType

from autobahn.asyncio.websocket import WebSocketServerProtocol
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '../webapp'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
django.setup()

from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.contrib.auth import get_user

from engine.exceptions import RequestError

RPC = 'rpc'
EVENT = 'event'


class Error(Exception):
    """Base RPC exception"""


class NotFoundError(Error, LookupError):
    """Error raised by server if RPC namespace/method lookup failed."""


class RpcRequestError(Exception):
    """Error raised from RPC method and send as error to client."""

    def __init__(self, errors):
        self.errors = errors


def method(func):
    func.__websocket_rpc__ = {}
    return func


# FIXME: Add subscription on server, so we do not send notification to client if it is not
# really subscribed. Not it is checked on client.
class WebsocketRpc(WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError

    def onConnect(self, request):
        # TODO: move this to other server or thread and call with async
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
        assert isBinary
        # Not sure this can happen, but lets check
        if not self._user:
            self.authentication_failed()

        # TODO: add better validation
        data = msgpack.unpackb(payload, encoding='utf8')
        if data.get('type') == RPC:
            try:
                func = self.dispatch(data.get('method'))
            except NotFoundError:
                self.send_exception(data, 'Method does not exist')
            else:
                args = self.check_args(func, data.get('args'))

                try:
                    if asyncio.iscoroutinefunction(func):
                        value = yield from func(*args)
                        self.send_success(data, value)
                    else:
                        self.send_success(data, func(*args))
                except (RequestError, RpcRequestError) as error:
                    self.send_error(data, error)
                except:
                    self.send_exception(data, 'Server error')
                    raise

    def check_args(self, func, args):
        # TODO: Add validation like here
        # https://github.com/aio-libs/aiozmq/blob/master/aiozmq/rpc/base.py#L205
        if not args:
            args = []

        return args

    def _send(self, msg):
        # FIXME: exceptions from here are not displayed in docker logs
        self.sendMessage(msgpack.packb(msg), isBinary=True)

    def dispatch(self, method):
        try:
            func = self[method]
        except KeyError:
            raise NotFoundError(method)
        else:
            if isinstance(func, MethodType):
                holder = func.__func__
            else:
                holder = func
            if not hasattr(holder, '__websocket_rpc__'):
                raise NotFoundError(method)
            return func

    def authentication_failed(self):
        self.sendClose()

    def register(self, name, func):
        self._methods[name] = func

    def send_success(self, data, value):
        msg = {
            'id': data['id'],
            'type': data['type'],
            'event': 'success',
            'value': value
        }
        self._send(msg)

    def send_error(self, data, error):
        msg = {
            'id': data['id'],
            'type': data['type'],
            'event': 'error',
            'message': error.errors
        }
        self._send(msg)

    def send_exception(self, data, message):
        msg = {
            'id': data['id'],
            'type': data['type'],
            'event': 'exception',
            'message': message
        }
        self._send(msg)

    def publish(self, topic, message):
        msg = {
            'type': EVENT,
            'topic': topic,
            'message': message
        }
        self._send(msg)
