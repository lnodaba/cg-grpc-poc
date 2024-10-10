import os


HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', 1521)
DATABASE = os.getenv('DATABASE', 'FREEPDB1')
USER = os.getenv('USER', 'oracle')
PASSWORD = os.getenv('PASSWORD', 'oracle')
MIN_POOL_SIZE = os.getenv('MIN_POOL_SIZE', 1)
MAX_POOL_SIZE = os.getenv('MAX_POOL_SIZE', 5)
POOL_INCREMENT = os.getenv('POOL_INCREMENT', 1)
NUM_WORKERS = os.getenv('NUM_WORKERS', 1)
NATIVE_SQL_DEBUG = os.getenv('NATIVE_SQL_DEBUG', False)
