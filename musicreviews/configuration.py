import os
import click
from configparser import ConfigParser
from pkg_resources import Requirement, resource_filename


APP_NAME = 'musicreviews'
CONFIG_FILENAME = 'config.cfg'
TEMPLATE_FILENAME = 'config/config.template.cfg'


def write_config(config):
    """Writes config in local config path and returns this path"""
    directory = config_directory()
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = config_path()
    with open(path, 'w') as configfile:
        config.write(configfile)
    return path


def load_config(load_template=False):
    """Loads configuration and returns configuration and path"""
    config = ConfigParser()
    path = template_config_path() if load_template else config_path()
    if os.path.exists(path):
        config.read(path)
    else:
        config = None
    return path, config


def template_config_path():
    """Returns package template configuration path"""
    return resource_filename(Requirement.parse("music-reviews"), TEMPLATE_FILENAME)


def config_path():
    """Returns local package configuration path"""
    return os.path.join(config_directory(), CONFIG_FILENAME)


def config_directory():
    """Returns local package configuration directory"""
    return os.path.join(click.get_app_dir(APP_NAME))
