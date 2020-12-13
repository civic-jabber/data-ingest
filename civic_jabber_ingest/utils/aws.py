import os
import subprocess

import civic_jabber_ingest.utils.config as config


STATES = config.read_config("states")


def s3_sync(src, dst):
    """A wrapper around the AWS CLI that syncs a local directory with an S3 bucket. This
    is necessary because there is not current a boto command for AWS sync.

    Parameters
    ----------
    src : str
        The source destination in the local file system
    dst : str
        The destination bucket

    Returns
    -------
    result : subprocess.CompletedProcess
        The result of the AWS sync command
    """
    try:
        return subprocess.run(["aws", "s3", "sync", src, dst])
    except FileNotFoundError:
        raise ValueError(
            "AWS sync failed. You may need to install the AWS CLI on your system."
        )


def sync_state(state, dev=False):
    """Syncs the local directory with the files from a state register with S3.

    Parameters
    ----------
    state : str
        The state to sync. The state must be one of the states listed in the states
        config file and must also be present on the local file system.
    dev : bool
        If True, syncs to the dev bucket

    Returns
    -------
    result : subprocess.CompletedProcess
        The result of the AWS sync command
    """
    if state.upper() not in STATES:
        raise ValueError(
            "Please choose a valid state, or add the state to states.yml "
            "if it is currently missing."
        )

    src = os.path.join(config.local_regs_directory(), state.lower())
    if not os.path.exists(src):
        raise ValueError(f"Data for {state} does not exist on the local file system.")

    dst = os.path.join(config.regs_s3_bucket(dev=dev), state.lower())
    return s3_sync(src, dst)
