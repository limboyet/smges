import secrets

class Config(object):
    SECRET_KEY = secrets.token_urlsafe(64)
    SESSION_TIMEOUT = 900
    SERVER_PORT = 5000
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    LOG_LEVEL = "ERROR"
    JWT_ALGORITHM = 'HS256'

    # Mysql database
    # DB_PORT = 3306
    # DB_SERVER = "localhost"
    # DB_TYPE = "mysql"
    # DB_DRIVER = "mysqldb"
    # Postgres database
    # DB_PORT = 5432
    # DB_SERVER = "localhost"
    # DB_TYPE = "postgresql"
    # DB_DRIVER = "psycopg2"
