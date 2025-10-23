import secrets

class Config(object):
    SECRET_KEY = secrets.token_urlsafe(64)
    SESSION_TIMEOUT = 900
    SERVER_PORT = 5000