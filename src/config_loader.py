# imports
import yaml
import logging
from pathlib import Path

# preamble
logger = logging.getLogger(__name__)


def set_config(CONFIG_PATH: str = Path(__file__).parent.parent / "config/configuration.yml"):

    with open(CONFIG_PATH, 'r') as f:
        try:
            config = yaml.safe_load(f)
            logger.info("configuration loaded successfully")

            return config

        except yaml.YAMLError as exc:
            logger.exception("error loading configuration")

            return None
