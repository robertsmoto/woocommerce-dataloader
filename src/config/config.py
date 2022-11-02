from os.path import exists
import json
import os
import sys


class Config:
    def __init__(self, settings: dict, config_path: str = ''):
        print("Loading app config ...")
        self.conf = settings
        self.config_path = config_path
        self.config = {}

    def load(self):
        config_file = "/var/wcdataloader/config.json"
        if self.config_path:
            config_file = self.config_path
        env_path = os.getenv("CONFIG_PATH", None)
        if env_path:
            config_file = env_path
        is_available = exists(config_file)

        if not is_available:
            sys.exit("Config file is not available.")

        with open(config_file) as f:
            data = json.load(f)

        for key, value in data.items():
            self.config[key] = str(value)

        ## combines the settings
        self.conf = {**self.conf, **self.config}

        return self


