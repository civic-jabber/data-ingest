import subprocess


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
        raise ValueError("AWS sync failed. You may need to install the AWS CLI on "
                         "your system.")


