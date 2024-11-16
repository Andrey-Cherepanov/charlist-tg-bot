from environs import Env
from dataclasses import dataclass

@dataclass
class Bot:
    token:str
    admin_ids:list[int]

@dataclass
class Database:
    pass

@dataclass
class Config:
    tg_bot:Bot
    #database:Database

def load_config(path=None):
    env = Env()
    env.read_env(path)

    return Config(tg_bot=Bot(
                             token=env['BOT_TOKEN'],
                             admin_ids=map(int, env.list('ADMIN_IDS')))
                  )
