import configparser

config = configparser.ConfigParser()
config.read("configs.ini")


def get_database_config():
    return config["Database"]


if __name__ == "__main__":
    print(config["Database"]["name"])
