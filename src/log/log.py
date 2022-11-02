import logging
from config.config import Config


class Log:
    """Main logging class."""

    def __init__(self, conf: Config):
        self.conf = conf

    def debug(self, msg: str):
        """Debug logging message."""
        # toggle debug output in the /config/settings.py file
        if not self.conf.conf.get('debugOutput', False):
            return self

        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.DEBUG,
            filename=self.conf.conf['logDirFile'])
        logging.info("%s", msg)
        print(f"DEBUG: {msg}")
        return self

    def info(self, msg: str):
        """Info logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.INFO,
            filename=self.conf.conf['logDirFile'])
        logging.info("%s", msg)
        print(f"INFO: {msg}")
        return self

    def warn(self, msg: str):
        """Info logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.WARN,
            filename=self.conf.conf['logDirFile'])
        logging.info("%s", msg)
        print(f"WARN: {msg}")
        return self

    def error(self, msg: str):
        """Info logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.ERROR,
            filename=self.conf.conf['logDirFile'])
        logging.info("%s", msg)
        print(f"ERROR: {msg}")
        return self
