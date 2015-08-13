import asyncio


from os import environ
import datetime

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import register


class TimeService(object):

    @register('utcnow')
    def utcnow(self):
        now = datetime.datetime.utcnow()
        return now.strftime("%Y-%m-%dT%H:%M:%SZ")


class Component(ApplicationSession):

    @asyncio.coroutine
    def onJoin(self, details):
        yield from self.register(TimeService())


if __name__ == '__main__':
    runner = ApplicationRunner('ws://localhost:8080/ws', realm='frontend',
                               debug=True, debug_wamp=False, debug_app=True)
    runner.run(Component)
