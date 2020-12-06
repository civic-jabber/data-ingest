import os
import pathlib
import yaml


PATH = pathlib.Path(__file__).parent.absolute()
CONFIG_PATH = os.path.join(PATH, "..", "config")


def read_config(name):
    """Reads in a YAML config and converts it to a Python dictionary.

    Paraemters
    ----------
    name : str
        The name of the config. This should match the name of the config file in the
        config directory. The .yml extension should be omitted.

    Returns
    -------
    config : dict
        A dictionary containing the configurations.
    """
    filename = f"{CONFIG_PATH}/{name}.yml"
    with open(filename, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config
