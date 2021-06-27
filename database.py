from config import get_database_config
from peewee import PostgresqlDatabase, Model

config = get_database_config()
conn = PostgresqlDatabase(config["name"], user=config["user"], password=config["password"],
                          host=config["host"], port=config["port"])


class BaseModel(Model):
    class Meta:
        database = conn
