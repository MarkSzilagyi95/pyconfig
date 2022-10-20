import logging
import os
import sys
from typing import Union

import yaml
from yaml.loader import SafeLoader


class ConfigReader:

    @staticmethod
    def read_config() -> dict:
        active_profile = ConfigReader.__get_active_profile()
        project_path = ConfigReader.__get_project_path()
        with open(f"{project_path}/resources/application{active_profile}.yml") as f:
            return yaml.load(f, Loader=SafeLoader)

    @staticmethod
    def __get_project_path() -> str:
        return sys.path[1]

    @classmethod
    def __get_active_profile(cls) -> str:
        profile = os.environ.get("ACTIVE_PROFILE", "")
        logging.info(f"Active profile: {profile if profile != '' else 'default'}")
        return profile if profile == "" else "-" + profile


class Config:
    __config: dict = ConfigReader.read_config()

    @staticmethod
    def value(value: str) -> Union[str, list, dict]:
        return Config.__find_property(value)

    @classmethod
    def __find_property(cls, value) -> Union[str, list, dict]:
        keys = value.split(".")
        config = cls.__config
        for key in keys:
            try:
                config = config[key]
            except:
                config = ""
                logging.warning(f"Configuration property [{key}] not found")
                break

        return config
