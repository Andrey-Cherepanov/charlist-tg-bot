import logging
from mysql.connector import connect, Error
from config import load_config
from services.features import translitirate

logger = logging.getLogger(__name__)

def get_connection(connection_params=None, database=None):
    """ Get connection to DB
    connection_params must be {'host':'<host>', 'user':'<user>', 'password':'<password>'}
    if not connection_params dict given, it will be obtained from the configs"""

    try:
        if connection_params:
            host, user, password = connection_params['host'], connection_params['user'], connection_params['password']
        else:
            config = load_config()
            host, user, password = config.database.db_host, config.database.db_user, config.database.db_password
        if database:
            cnx = connect(host=host, user=user, password=password, database=database)
        else:
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

def get_tables(cnx=None, database=None):
    """ get tables from database"""
    if not database:
        config = load_config()
        database = config.database.db_origin()
    if not cnx:
        cnx = get_connection()

    result = list()

    try:
        with cnx.cursor() as cursor:
            cursor.execute(f"SHOW TABLES FROM {database}")
            result = [table[0] for table in cursor]
    except Error:
        logger.error('Ошибка взаимодействия с базой данных', exc_info=True)
    finally:
        return result



def create_database(cnx=None):
    """ Create database and origin table if not exists"""
    if not cnx:
        cnx = get_connection()
    config = load_config()
    origin = config.database.db_origin
    databases = get_databases()
    if not origin in databases:
        try:
            with cnx.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {origin}")
        except Error:
            logger.error('Ошибка взаимодействия с базой данных', exc_info=True)
            return False
    return True

def create_master_table(cnx=None):
    """ Creates master table if not exists"""
    config = load_config()
    master = config.database.db_master_table
    origin = config.database.db_origin
    prefix = config.database.db_prefix
    if not cnx:
        cnx = get_connection(database=origin)
    tables = get_tables(cnx, origin)
    if not f'{prefix}_{master}' in tables:
        try:
            with cnx.cursor() as cursor:
                cursor.execute(f"create table {origin}.{prefix}_{master} (id INT AUTO_INCREMENT PRIMARY KEY, master_id INT, table_name CHAR(50), columns TEXT)")
        except Error:
            logger.error('Ошибка взаимодействия с базой данных', exc_info=True)
            return False
    return True

def _columns_to_string(columns):
    res = ''
    for column, column_type in columns:
        res += f'column_{translitirate(column)},{column_type};'
    return res[:-1]

def _string_to_columns(string):
    res = dict()
    for key, value in map(lambda x: x.split(','), string.split(';')):
        res[key] = value
    return res

def create_table(name, master_id, columns, cnx=None):
    # TODO: add types to columns
    """ Creates a new table with given columns
        Makes a new write in master table """
    config = load_config()
    prefix = config.database.db_prefix
    origin = config.database.db_origin
    master = prefix + '_' + config.database.db_master_table
    table_name = f'{prefix}_{translitirate(name)}'
    columns_line = _columns_to_string(columns)
    if not cnx:
        cnx = get_connection()
    try:
        with cnx.cursor() as cursor:
            query = f"""
            INSERT INTO {origin}.{master} (master_id, table_name, columns)
            VALUES
                ({master_id}, \"{table_name}\", \"{columns_line}\")
            """
            cursor.execute(query)
        with cnx.cursor() as cursor:
            query = f"create table {origin}.{table_name} (id INT AUTO_INCREMENT PRIMARY KEY, char_owner INT, "
            query += ', '.join(map(lambda x: f'column_{translitirate(x[0])} {x[1].upper()}', columns))
            query += ')'
            cursor.execute(query)
    except Error:
        logger.error('Ошибка взаимодействия с базой данных', exc_info=True)
