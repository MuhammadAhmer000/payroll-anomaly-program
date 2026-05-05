# import statements
from src.config_loader import set_config


# TODO: add endpoint for /config here...
def main_set_config():

    # require: from src.config_loader import set_config
    return set_config()


# Note: main will eventually be left for testing, React will be the "main" frontend
# TODO: add endpoint for /test here...
def main():

    config = main_set_config()
    






if __name__ == "__main__":
    main()
