import logging
import os

import daiquiri
import tqdm as _tqdm


def get_logger(level=None):
    """Returns the logger for the ingest package."""
    level = logging.INFO if not level else level
    daiquiri.setup(level=level)
    return daiquiri.getLogger(__name__)


def tqdm(*args, **kwargs):
    """Disables or enables the tqdm progress bar based on an environmental variable."""
    disable = os.environ.get("CIVIC_JABBER_TQDM", None) == "True"
    kwargs["disable"] = disable
    return _tqdm.tqdm(*args, **kwargs)
