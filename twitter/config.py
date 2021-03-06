##this modules handles application configuration

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

##environmental variable
TESTING = config("TESTING", cast=bool, default=False)
DEBUG = config("DEBUG", cast=bool, default=False)
LIVE = config("LIVE", cast=bool, default=False)


POSTGRES_USER = config("POSTGRES_USER", cast=Secret)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=Secret)
POSTGRES_PORT = config("POSTGRES_PORT", cast=Secret)
POSTGRES_DB = config("POSTGRES_DB", cast=Secret)

DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
SECRET_KEY = config("SECRET_KEY", cast=Secret)
ALGORITHM = config("ALGORITHM", cast=Secret)

