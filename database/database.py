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


def get_databases(cnx=None):
    """Returns databases in this connextion"""
    if not cnx:
        cnx = get_connection()
    result = list()
    try:
        with cnx.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            result = [db[0] for db in cursor]
    except Error:
        logger.error('Ошибка взаимодействия с базой данных', exc_info=True)
    finally:
        return result


def create_database(cnx=None):
