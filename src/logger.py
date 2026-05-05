import logging


def setup_logging():
    # Setting up the logger
    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)

    # Handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=logging.INFO)

    file_handler = logging.FileHandler(filename="app.log", mode="a", encoding="utf-8")
    file_handler.setLevel(level=logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Formatter
    formatter = logging.Formatter(
        "{asctime} | {levelname} | {name} | {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    return logger











