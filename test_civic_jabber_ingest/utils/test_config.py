import os.path as path

import pytest

import civic_jabber_ingest.utils.config as config
from civic_jabber_ingest.utils.environ import modified_environ


@pytest.mark.slow
def test_news_config_is_well_formed():
    newspaper_config = config.read_config("newspaper")
    for value in newspaper_config:
        assert "id" in value
        assert "url" in value
        assert "states" in value
        assert isinstance(value["states"], list)


@pytest.mark.slow
def test_news_ids_are_unique():
    newspaper_config = config.read_config("newspaper")
    ids = [value["id"] for value in newspaper_config]
    assert len(ids) == len(set(ids))


def test_local_regs_get_dir_from_env(tmpdir):
    env = {"CIVIC_JABBER_DATA_DIR": tmpdir.dirname}
    with modified_environ(**env):
        assert config.local_regs_directory() == path.join(tmpdir.dirname, "regs")


def test_local_regs_makes_dir_with_no_env_var(monkeypatch, tmpdir):
    monkeypatch.setattr(path, "expanduser", lambda x: tmpdir.dirname)
    correct_directory = path.join(tmpdir.dirname, ".civic_jabber", "regs")
    local_directory = config.local_regs_directory()
    assert path.exists(correct_directory)
    assert local_directory == correct_directory


def test_regs_s3_bucket_returns_prod_and_dev():
    assert config.regs_s3_bucket() == "s3://us-registers"
    assert config.regs_s3_bucket(dev=True) == "s3://us-registers-dev"
