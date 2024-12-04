from environs import Env
from dataclasses import dataclass

ORIGIN = 'origin'
MASTER_TABLE = 'master'
PREFIX = 'charlist'

@dataclass
class Bot:
    token:str
    admin_ids:list[int]

@dataclass
class Database:
    db_host:str
    db_user:str
    db_password:str
    db_origin:str
    db_master_table:str
    db_prefix:str

@dataclass
class Config:
    tg_bot:Bot
    database:Database

def load_config(path=None):
    env = Env()
    env.read_env(path)

    return Config(tg_bot=Bot(
                             token=env('BOT_TOKEN'),
                             admin_ids=map(int, env.list('ADMIN_IDS'))),
                  database=Database(
                             db_host=env('DB_HOST'),
                             db_user=env('DB_USER'),
                             db_password=env('DB_PASSWORD'),
                             db_origin=ORIGIN,
                             db_master_table=MASTER_TABLE,
                             db_prefix=PREFIX
                  )
                  )
