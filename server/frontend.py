import asyncio


from os import environ
import datetime

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    A simple time service application component.
    """

    @asyncio.coroutine
    def onJoin(self, details):

        def utcnow():
            now = datetime.datetime.utcnow()
            return now.strftime("%Y-%m-%dT%H:%M:%SZ")

        yield from self.register(utcnow, 'utcnow')


if __name__ == '__main__':
    runner = ApplicationRunner('ws://localhost:8080/ws', realm='frontend')
    runner.run(Component)
