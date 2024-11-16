import logging
from mysql.connector import connect, Error
from config import load_config

logger = logging.getLogger(__name__)

def get_connection(connection_params=None):
    """ Get connection to DB
    connection_params must be {'host':'<host>', 'user':'<user>', 'password':'<password>'}
    if not connection_params dict given, it will be obtained from the configs"""

    try:
        if connection_params:
            host, user, password = connection_params['host'], connection_params['user'], connection_params['password']
        else:
            config = load_config()
            host, user, password = config.database.db_host, config.database.db_user, config.database.db_password
        cnx = connect(host=host, user=user, password=password)
    except Error:
        logger.error('Ошибка подключения к базе данных', exc_info=True)
        return None
    return cnx
