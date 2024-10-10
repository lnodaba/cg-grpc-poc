
import os

HOST = os.getenv('HOST', 'oracle-db')
PORT = os.getenv('PORT', 1521)
DATABASE = os.getenv('DATABASE', 'FREEPDB1')
USER = os.getenv('USER', 'oracle')
PASSWORD = os.getenv('PASSWORD', 'oracle')

DATABASE_CONFIG = {
    'connections': {
        'default': {
            'engine': 'oracle',
            'credentials': {
                'host': HOST,
                'port': PORT,
                'database': DATABASE,
                'user': USER,
                'password': PASSWORD,
                'driver': '/opt/oracle/instantclient_23_5/libsqora.so.23.1',
            },
        },
    },
    'apps': {
        'models': {
            'models': [
                'models.acronyms',
                'models.acronyms_traindata',
                'models.trainset',
                'models.trainset_contents',
                'aerich.models',
            ],
            'default_connection': 'default',
        },
    },
}

# POSTGRESS_CONNECTON = "postgres://farm:farm@localhost:5432/acronyms"

# DATABASE_CONFIG = {
#     'connections': {
#         'default': POSTGRESS_CONNECTON
#     },
#     'apps': {
#         'models': {
#             'models': [
#                 'models.acronyms',
#                 'models.acronyms_traindata',
#                 'models.trainset',
#                 'models.trainset_contents',
#                 'aerich.models',
#             ],
#             'default_connection': 'default',
#         },
#     },
# }