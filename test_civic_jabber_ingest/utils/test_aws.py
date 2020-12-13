import subprocess

import pytest

import civic_jabber_ingest.utils.aws as aws


def aws_s3_sync_runs(monkeypatch):
    monkeypatch.setattr(subprocess, "run", lambda *args: True)
    result = aws.s3_sync("/fake/directory", "s3://fake-bucket")
    assert result is True


def aws_s3_raises_with_unavailable_command(monkeypatch):
    def mock_subprocess(*args):
        raise FileNotFoundError


    monkeypatch.setattr(subprocess, "run", mock_subprocess)
    with pytest.raises(ValueError):
        aws.s3_sync("/fake/directory", "s3://fake-bucket")
