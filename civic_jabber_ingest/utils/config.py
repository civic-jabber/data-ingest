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


def local_regs_directory():
    """Sets the local data directory for storing downloaded regulations. First looks for
    the CIVIC_JABBER_DATA_DIR environmental variable. If that doesn't exist, the data
    directory defaults to ~/.civic_jabber/regs

    Returns
    -------
    local_directory : path-like
        The directory for storing locally downloaded files
    """
    civic_jabber_dir = os.environ.get("CIVIC_JABBER_DATA_DIR", None)
    if not civic_jabber_dir:
        civic_jabber_dir = os.path.join(os.path.expanduser("~"), ".civic_jabber")

        if not os.path.exists(civic_jabber_dir):
            os.mkdir(civic_jabber_dir)

    local_directory = os.path.join(civic_jabber_dir, "regs")
    if not os.path.exists(local_directory):
        os.mkdir(local_directory)

    return local_directory
