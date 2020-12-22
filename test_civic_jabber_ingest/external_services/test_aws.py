import os
import subprocess

import pytest

import civic_jabber_ingest.external_services.aws as aws
from civic_jabber_ingest.utils.environ import modified_environ


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


def test_sync_raises_with_missing_state(tmpdir, monkeypatch):
    monkeypatch.setattr(aws, "s3_sync", lambda src, dst: True)
    env = {"CIVIC_JABBER_DATA_DIR": tmpdir.dirname}
    with modified_environ(**env):
        with pytest.raises(ValueError):
            aws.sync_state("pa")


def test_sync_raises_with_invalid_state(monkeypatch):
    monkeypatch.setattr(aws, "s3_sync", lambda src, dst: True)
    with pytest.raises(ValueError):
        aws.sync_state("koala")


def test_sync_works_with_existing_state(tmpdir, monkeypatch):
    monkeypatch.setattr(aws, "s3_sync", lambda src, dst: True)
    os.makedirs(f"{tmpdir.dirname}/regs/pa")
    env = {"CIVIC_JABBER_DATA_DIR": tmpdir.dirname}
    with modified_environ(**env):
        assert aws.sync_state("pa") is True
