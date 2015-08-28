import hashlib
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def avatar(self):
        return 'http://www.gravatar.com/avatar/%s.jpg?d=wavatar' % self.getMD5()

    def getMD5(self):
        m = hashlib.md5()
        m.update(self.email.encode('utf8'))
        return m.hexdigest()
