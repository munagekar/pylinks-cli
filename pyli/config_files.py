import logging
import pathlib

import toml

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONFIG_DIR = pathlib.Path.home() / pathlib.Path(".pylinks")
CONF_FILE = CONFIG_DIR / "pylinks.toml"

if not CONF_FILE.exists():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONF_FILE.open("w")
    CONF_FILE.write_text(toml.dumps({}))
    logger.info("Initialized Empty pylinks config file")
