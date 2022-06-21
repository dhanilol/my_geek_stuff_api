from os import environ


DEBUG = environ.get('DEBUG') == 'true' if environ.get('DEBUG') else False

TEMPLATE_DEBUG = environ.get('TEMPLATE_DEBUG') == 'true' if environ.get('TEMPLATE_DEBUG') else False
IS_USER_SANDBOX = environ.get('IS_USER_SANDBOX') == 'true' if environ.get('IS_USER_SANDBOX') else False
SANDBOX = environ.get('SANDBOX') == 'true' if environ.get('SANDBOX') else False

BASE_URL = environ.get('BASE_URL', 'http://127.0.0.1:8000')

SECRET_KEY = environ.get('SECRET_KEY', 's_v4a%jdj#)7b*fs*2!q!82b_l@3&su#o%i!rsw5s2h(gb-!pq')

# DATABASES = {
#     'default': {
#         'ENGINE': environ.get('DB_ENGINE', 'sql_server.pyodbc'),
#         'NAME': environ.get('DB_NAME', 'my_geek_stuff_api'),
#         'USER': environ.get('DB_USER', 'SA'),
#         'PASSWORD': environ.get('DB_PASSWORD', ''),
#         'HOST': environ.get('DB_HOST', 'db'),
#         'PORT': environ.get('DB_PORT', '1433'),
#         'AUTOCOMMIT': True,
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         }
#     },
# }
