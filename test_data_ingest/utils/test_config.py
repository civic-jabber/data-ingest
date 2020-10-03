import data_ingest.utils.config as config


def test_read_config():
    newspaper_config = config.read_config("newspaper")
    assert isinstance(newspaper_config, dict)
