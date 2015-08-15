import asyncio
import inspect
import ujson

from autobahn.asyncio.websocket import WebSocketServerProtocol

from pprint import pprint


class BaseRpcProtocol(WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._methods = {}

    def register(self, name, func):
        self._methods[name] = func

    def onMessage(self, payload, isBinary):
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
