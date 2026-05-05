# imports
import yaml
import logging

# preamble
logger = logging.getLogger(__name__)


def set_config(CONFIG_PATH: str):

    with open(CONFIG_PATH, 'r') as f:
        try:
            config = yaml.safe_load(f)
            logger.info("configuration loaded successfully")
            return config
        except yaml.YAMLError as exc:
            logger.exception("error loading configuration")
