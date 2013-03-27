import os
from django.conf import settings


VERSION = (0, 0, 1)

__version__ = ".".join(map(str, VERSION[0:3])) + "".join(VERSION[3:])
__author__ = "George li"
__contact__ = "goblin.george@gmail.com"
__homepage__ = "http://github.com/georgefs/picasa_admin"
__docformat__ = "markdown"
__license__ = "BSD (3 clause)"




PICASA_ROOT = os.path.join(settings.MEDIA_ROOT, "picasa_storage" )
PICASA_TMP = os.path.join(PICASA_ROOT, 'tmp')

settings.PICASA_ROOT = PICASA_ROOT
settings.PICASA_TMP = PICASA_TMP
