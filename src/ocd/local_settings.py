import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.abspath(os.path.join(PROJECT_PATH, "db", "ocd.db"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': DB_PATH,
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

_host = 'www.opencommunity.org.il'
HOST_URL = "http://%s" % _host
ALLOWED_HOSTS = [_host]
FROM_EMAIL = "noreply@opencommunity.org.il"

# Uncomment the following line to enable the debug toolbar
# INTERNAL_IPS = ('127.0.0.1',)
