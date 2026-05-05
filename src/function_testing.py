# import
import yaml

import config_loader
import logging

# preamble
logger = logging.getLogger(__name__)


def test_config_loader():
    try:
        config = config_loader.set_config()
        print("configuration loaded successfully")  # remove once development finishes
        logger.info("test complete: configuration loaded successfully")
        print(config)

    except yaml.YAMLError as exc:
        print("error loading configuration")  # remove once development finishes
        logger.exception("test failed: configuration failed to load")
