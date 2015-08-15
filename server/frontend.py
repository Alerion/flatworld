import asyncio


from os import environ
import datetime

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import auth, register
from autobahn.wamp.exception import ApplicationError


class AuthService(object):

    USERDB = {
        'user':  {
            # 'authid': 'ID09125',  # assign a different auth ID during authentication
            'secret': 'user',
            'role': 'user'
        }
    }

    @register('authenticate')
    def authenticate(self, realm, authid, details):
        print("authenticate called: realm = '{}', authid = '{}'".format(realm, authid))

        if authid in self.USERDB:
            # return a dictionary with authentication information ...
            return self.USERDB[authid]
        else:
            raise ApplicationError(
                ApplicationError.AUTHORIZATION_FAILED,
                "could not authenticate session - no such user {}".format(authid))


class TimeService(object):

    def __init__(self):
        self.value = 1

    @register('count')
    def count(self):
        self.value += 1
        return self.value

    @register('utcnow')
    def utcnow(self):
        now = datetime.datetime.utcnow()
        return now.strftime("%Y-%m-%dT%H:%M:%SZ")


class Component(ApplicationSession):
    # See https://github.com/crossbario/crossbarexamples/blob/master/authenticate/wampcra/client.py
    USER = "server"
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
        yield from self.register(TimeService())


if __name__ == '__main__':
    runner = ApplicationRunner('ws://localhost:9000/ws', realm='frontend',
                               debug=True, debug_wamp=False, debug_app=True)
    runner.run(Component)
